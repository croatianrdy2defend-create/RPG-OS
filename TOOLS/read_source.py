#!/usr/bin/env python3
"""Optional, standard-library source reader. It reports delivery, not comprehension.

Line numbers are one-based, inclusive, and refer to the original UTF-8 file.
Character/byte offsets are zero-based and end-exclusive. Newlines are never
normalized. Heading paths use ``Parent > Child`` (or a list of names in Python).
An optional JSONL receipt must be outside the source root and never proves that
a host transcript is complete, or that a recipient read or understood a source.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import ntpath
import os
from pathlib import Path
import re
import sqlite3
import stat
import sys
import tempfile


class SourceError(Exception):
    """A bounded, machine-readable reader failure."""

    def __init__(self, message: str, code: str = "source_error", **details):
        super().__init__(message)
        self.code = code
        self.details = details

    def as_dict(self) -> dict:
        return {"code": self.code, "message": str(self), **self.details}


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_link(info) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400
    )


def _validate_component(part: str, code: str = "unsafe_path") -> None:
    stem = part.split(".", 1)[0].upper()
    if (
        part in ("", ".", "..") or ":" in part
        or any(ord(character) < 32 for character in part)
        or part.endswith((".", " "))
        or stem in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
        or re.fullmatch(r"(?:COM|LPT)[0-9¹²³]", stem)
    ):
        raise SourceError("Traversal, device names, alternate streams, and ambiguous path components are forbidden.", code)


def _check_components(path: Path, *, allow_missing_leaf: bool = False) -> None:
    """Check the lexical absolute path before any resolution follows links."""
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for index, part in enumerate(absolute.parts[1:]):
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            if allow_missing_leaf and index == len(absolute.parts) - 2:
                return
            raise SourceError("Path does not exist.", "unsafe_path") from exc
        except OSError as exc:
            raise SourceError("Path cannot be inspected.", "unsafe_path") from exc
        if _is_link(info):
            raise SourceError("Symlinks and reparse points are not allowed.", "unsafe_path")
        if index != len(absolute.parts) - 2 and not stat.S_ISDIR(info.st_mode):
            raise SourceError("A parent component is not a directory.", "unsafe_path")


def _checked_root(root: Path) -> Path:
    root = Path(root)
    # Reject traversal before abspath can erase an unsafe component.
    if ".." in root.parts:
        raise SourceError("Root must not contain parent traversal.", "invalid_root")
    _check_components(root)
    try:
        canonical = root.resolve(strict=True)
        if not canonical.is_dir():
            raise SourceError("Root is not a directory.", "invalid_root")
    except OSError as exc:
        raise SourceError("Root cannot be resolved.", "invalid_root") from exc
    return canonical


def root_identity(root: Path) -> str:
    """An opaque identity of the checked absolute root, stable on this host."""
    canonical = _checked_root(root)
    name = os.path.normcase(str(canonical)).replace("\\", "/")
    return "root-" + _digest(name.encode("utf-8"))


def resolve_source(root: Path, relative: str) -> Path:
    """Resolve one regular file strictly below root without following links."""
    canonical_root = _checked_root(root)
    if not isinstance(relative, str) or not relative or "\x00" in relative:
        raise SourceError("Source path must be a nonempty relative path.", "unsafe_path")
    portable = relative.replace("\\", "/")
    if ntpath.splitdrive(relative)[0] or portable.startswith("/"):
        raise SourceError("Source path must be relative to root.", "unsafe_path")
    parts = portable.split("/")
    # Windows aliases (trailing dot/space and device names) are unsafe even when
    # this checkout is tested on another operating system.
    for part in parts:
        _validate_component(part)
    source = canonical_root.joinpath(*parts)
    _check_components(source)
    try:
        resolved = source.resolve(strict=True)
        resolved.relative_to(canonical_root)
        info = resolved.stat()
    except (OSError, ValueError) as exc:
        raise SourceError("Source is unavailable or outside the read root.", "unsafe_path") from exc
    if not stat.S_ISREG(info.st_mode):
        raise SourceError("Source must be a regular file.", "not_regular_file")
    return resolved


def _stat_signature(info) -> tuple:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _exact_lines(text: str) -> list[str]:
    # LF, CRLF, and CR are source line endings. Unicode paragraph separators
    # remain source characters instead of silently changing line coordinates.
    return re.findall(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$", text)


def load_document(root: Path, relative: str, expected_sha256=None) -> dict:
    canonical_root = _checked_root(Path(root))
    source = resolve_source(canonical_root, relative)
    try:
        before_path = source.stat()
        descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
        with os.fdopen(descriptor, "rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or _stat_signature(before) != _stat_signature(before_path):
                raise SourceError("Source changed while opening it.", "source_changed")
            raw = stream.read()
            after = os.fstat(stream.fileno())
        checked_again = resolve_source(canonical_root, relative)
        if checked_again != source or _stat_signature(before) != _stat_signature(after) or _stat_signature(after) != _stat_signature(source.stat()) or len(raw) != after.st_size:
            raise SourceError("Source changed while reading it.", "source_changed")
    except OSError as exc:
        raise SourceError("Source could not be read.", "unreadable_source") from exc
    digest = _digest(raw)
    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256):
            raise SourceError("Expected SHA-256 must contain 64 hexadecimal characters.", "invalid_revision")
        if digest != expected_sha256.lower():
            raise SourceError("Source revision no longer matches the requested SHA-256.", "stale_revision", expected_sha256=expected_sha256.lower(), actual_sha256=digest)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SourceError("Source is not valid UTF-8 text.", "invalid_utf8") from exc
    if "\x00" in text:
        raise SourceError("Source contains NUL bytes and is not supported as text.", "binary_source")
    lines = _exact_lines(text)
    return {
        "root_id": root_identity(canonical_root),
        "path": source.relative_to(canonical_root).as_posix(),
        "sha256": digest,
        "text": text,
        "lines": lines,
        "line_count": len(lines),
        "source_size_bytes": len(raw),
    }


def list_sections(document: dict) -> list[dict]:
    """List Markdown ATX/setext sections; parent sections contain their children."""
    lines = document["lines"]
    headings = []
    fence = None
    frontmatter = None
    previous = None
    for index, original in enumerate(lines):
        line = original.rstrip("\r\n")
        if index == 0:
            line = line.lstrip("\ufeff")
            if line in ("---", "+++"):
                frontmatter = line
                continue
        if frontmatter is not None:
            if line == frontmatter or (frontmatter == "---" and line == "..."):
                frontmatter = None
            continue
        if fence is not None:
            closing = re.fullmatch(r" {0,3}(" + re.escape(fence[0]) + r"{" + str(fence[1]) + r",})[ \t]*", line)
            if closing:
                fence = None
            previous = None
            continue
        opener = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", line)
        if opener and not (opener[1][0] == "`" and "`" in opener[2]):
            fence = (opener[1][0], len(opener[1]))
            previous = None
            continue
        atx = re.match(r" {0,3}(#{1,6})(?:[ \t]+(.*)|$)", line)
        if atx:
            heading = re.sub(r"[ \t]+#+[ \t]*$", "", atx[2] or "").strip()
            # A heading consisting only of a closing hash sequence is empty.
            if re.fullmatch(r"#+", heading):
                heading = ""
            headings.append((index + 1, len(atx[1]), heading))
            previous = None
            continue
        setext = re.fullmatch(r" {0,3}(=+|-+)[ \t]*", line)
        if setext and previous is not None:
            headings.append((previous[0], 1 if setext[1][0] == "=" else 2, previous[1]))
            previous = None
            continue
        # Indented code, block quotes, list markers, and thematic breaks cannot
        # become a setext heading. This deliberately does not parse HTML blocks.
        if line.strip() and not re.match(r"(?: {4}|\t| {0,3}(?:>|[-+*][ \t]|\d+[.)][ \t]))", line) and not re.fullmatch(r" {0,3}(?:[-*_][ \t]*){3,}", line):
            previous = (index + 1, line.strip())
        else:
            previous = None
    result = []
    stack = []
    for index, (start, level, heading) in enumerate(headings):
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, heading))
        end = len(lines)
        for following_start, following_level, _ in headings[index + 1:]:
            if following_level <= level:
                end = following_start - 1
                break
        identity = "\x00".join((document["root_id"], document["path"], document["sha256"], str(start), str(level)))
        result.append({
            "section_id": "sec-" + _digest(identity.encode("utf-8")),
            "heading": heading,
            "heading_path": [entry[1] for entry in stack],
            "level": level,
            "start_line": start,
            "end_line": end,
        })
    return result


def select_passage(document: dict, section_id=None, heading=None, start_line=None, end_line=None, max_chars=None) -> dict:
    selectors = int(section_id is not None) + int(heading is not None) + int(start_line is not None or end_line is not None)
    if selectors > 1:
        raise SourceError("Choose one of section ID, heading, or line span.", "invalid_selection")
    if max_chars is not None and (type(max_chars) is not int or max_chars < 0):
        raise SourceError("max_chars must be a nonnegative integer.", "invalid_selection")
    section = None
    kind = "whole_file"
    count = len(document["lines"])
    if section_id is not None or heading is not None:
        candidates = []
        for item in list_sections(document):
            if section_id is not None:
                match = item["section_id"] == section_id
            elif isinstance(heading, (list, tuple)):
                match = item["heading_path"] == list(heading)
            elif isinstance(heading, str):
                match = heading in (item["heading"], " > ".join(item["heading_path"]))
            else:
                raise SourceError("Heading must be a string or a list of names.", "invalid_selection")
            if match:
                candidates.append(item)
        if not candidates:
            raise SourceError("Section was not found in this source revision.", "section_not_found")
        if len(candidates) > 1:
            raise SourceError("Heading is ambiguous; choose a candidate section ID or full heading path.", "ambiguous_heading", candidates=candidates)
        section = candidates[0]
        start_line, end_line = section["start_line"], section["end_line"]
        kind = "section"
    elif selectors:
        kind = "line_span"
        if start_line is None or end_line is None or type(start_line) is not int or type(end_line) is not int or not 1 <= start_line <= end_line <= count:
            raise SourceError("A line span needs start and end within the source, inclusive.", "invalid_selection", source_line_count=count)
    else:
        start_line, end_line = 1, count
    lines = document["lines"]
    selected = "".join(lines[start_line - 1:end_line])
    returned = selected if max_chars is None else selected[:max_chars]
    start_offset = sum(map(len, lines[:start_line - 1]))
    end_offset = start_offset + len(selected)
    returned_end_offset = start_offset + len(returned)
    returned_lines = _exact_lines(returned)
    complete = len(returned) == len(selected)
    source_complete = start_offset == 0 and returned_end_offset == len(document["text"])
    returned_end_line = start_line + len(returned_lines) - 1 if returned else None
    return {
        "root_id": document["root_id"], "path": document["path"],
        "sha256": document["sha256"], "source_size_bytes": document["source_size_bytes"],
        "source_line_count": count, "selection_kind": kind,
        "section_id": section["section_id"] if section else None,
        "heading": section["heading"] if section else None,
        "heading_path": section["heading_path"] if section else None,
        "start_line": start_line, "end_line": end_line,
        "start_char_offset": start_offset, "end_char_offset": end_offset,
        "start_byte_offset": len(document["text"][:start_offset].encode("utf-8")),
        "end_byte_offset": len(document["text"][:end_offset].encode("utf-8")),
        "text": returned,
        "returned_start_line": start_line if returned else None,
        "returned_end_line": returned_end_line,
        "returned_end_char_offset": returned_end_offset,
        "returned_end_byte_offset": len(document["text"][:returned_end_offset].encode("utf-8")),
        "returned_end_line_complete": not returned or complete or returned_end_offset == sum(map(len, lines[:returned_end_line])),
        "returned_sha256": _digest(returned.encode("utf-8")),
        "selection_sha256": _digest(selected.encode("utf-8")),
        "source_char_count": len(document["text"]),
        "requested_char_count": len(selected), "returned_char_count": len(returned),
        "returned_size_bytes": len(returned.encode("utf-8")), "max_chars": max_chars,
        "complete": complete, "selection_complete": complete,
        "source_complete": source_complete, "truncated": not complete,
        "omitted_selection_chars": len(selected) - len(returned),
        "omitted_source_chars_before": start_offset,
        "omitted_source_chars_after": len(document["text"]) - returned_end_offset,
        "completeness_note": (
            "Entire source returned. Delivery is not evidence of comprehension."
            if source_complete else
            "The selected passage is complete; source context outside the selection is omitted."
            if complete else
            "The selected passage is truncated; omitted text may contain conditions, exceptions, or other qualifiers."
        ),
    }


def _receipt_target(root: Path, destination: Path) -> Path:
    root = _checked_root(root)
    destination = Path(destination)
    if ".." in destination.parts:
        raise SourceError("Receipt path must not contain parent traversal.", "unsafe_receipt")
    for part in (destination.parts[1:] if destination.anchor else destination.parts):
        _validate_component(part, "unsafe_receipt")
    destination = Path(os.path.abspath(destination))
    for part in destination.parts[1:]:
        _validate_component(part, "unsafe_receipt")
    _check_components(destination, allow_missing_leaf=True)
    destination = destination.resolve(strict=False)
    try:
        destination.relative_to(root)
    except ValueError:
        pass
    else:
        raise SourceError("Receipt must be outside the source read root.", "unsafe_receipt")
    if destination.exists():
        info = destination.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise SourceError("Receipt must be a regular file without hard links.", "unsafe_receipt")
    return destination


def write_receipt(root: Path, relative: str, passage: dict, destination: Path) -> dict:
    """Append an explicitly requested receipt; never invoked by ordinary reads."""
    target = _receipt_target(root, destination)
    document = load_document(root, relative, expected_sha256=passage["sha256"])
    selection = {"max_chars": passage.get("max_chars")}
    if passage.get("selection_kind") == "section":
        selection["section_id"] = passage.get("section_id")
    elif passage.get("selection_kind") == "line_span":
        selection.update(start_line=passage.get("start_line"), end_line=passage.get("end_line"))
    elif passage.get("selection_kind") != "whole_file":
        raise SourceError("Receipt does not describe a recognized source selection.", "invalid_receipt")
    if select_passage(document, **selection) != passage:
        raise SourceError("Receipt passage does not match an exact source read.", "invalid_receipt")
    receipt = {
        "receipt_version": 1,
        "kind": "tool_generated_delivery_receipt",
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "producer": "TOOLS/read_source.py",
        "claim": "The tool produced the recorded passage. This is not proof of comprehension, recipient observation, or host transcript completeness.",
        "passage": passage,
    }
    payload = (json.dumps(receipt, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    try:
        prior = target.stat() if target.exists() else None
        descriptor = os.open(target, os.O_RDWR | os.O_APPEND | os.O_CREAT | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0), 0o600)
        with os.fdopen(descriptor, "a+b") as stream:
            info = os.fstat(stream.fileno())
            checked = _receipt_target(root, target)
            current = checked.stat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or (info.st_dev, info.st_ino) != (current.st_dev, current.st_ino) or (prior is not None and (prior.st_dev, prior.st_ino) != (info.st_dev, info.st_ino)):
                raise SourceError("Receipt destination changed while opening.", "unsafe_receipt")
            stream.seek(0)
            existing = stream.read()
            if existing:
                try:
                    records = existing.decode("utf-8").splitlines()
                    valid = existing.endswith(b"\n") and all(
                        isinstance(record := json.loads(line), dict)
                        and record.get("kind") == "tool_generated_delivery_receipt"
                        for line in records
                    )
                except (UnicodeDecodeError, ValueError):
                    valid = False
                if not valid:
                    raise SourceError("Existing destination is not a complete delivery-receipt JSONL file.", "invalid_receipt")
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        load_document(root, relative, expected_sha256=passage["sha256"])
    except OSError as exc:
        raise SourceError("Receipt could not be written.", "receipt_write_failed") from exc
    return {"path": str(target), "receipt_sha256": _digest(payload), "kind": receipt["kind"], "claim": receipt["claim"]}


def probe() -> dict:
    """Demonstrate this Python runtime's actual reader/FTS, using disposable data."""
    sample = "# Probe\r\nRead exactly: č.\r\nOnly if the condition holds."
    with tempfile.TemporaryDirectory(prefix="rpg-os-source-probe-") as folder:
        root = Path(folder)
        (root / "probe.md").write_bytes(sample.encode("utf-8"))
        document = load_document(root, "probe.md")
        passage = select_passage(document, heading="Probe")
        reader_result = {"performed": True, "exact_utf8_and_crlf": passage["text"] == sample, "sha256": document["sha256"], "line_count": document["line_count"]}
    fts = {"performed": True, "available": False, "matching_rows": 0}
    try:
        with sqlite3.connect(":memory:") as connection:
            connection.execute("CREATE VIRTUAL TABLE probe USING fts5(body)")
            connection.execute("INSERT INTO probe(body) VALUES (?)", (sample,))
            rows = connection.execute("SELECT rowid FROM probe WHERE probe MATCH ?", ("condition",)).fetchall()
            fts.update(available=True, matching_rows=len(rows))
    except sqlite3.Error as exc:
        fts["reason"] = str(exc)
    return {
        "kind": "local_python_capability_probe", "python_version": sys.version.split()[0],
        "source_reader": reader_result, "sqlite_fts5": fts,
        "scope": "Only this Python process and disposable local sample data were tested.",
        "host_chat_export": {"observed": False, "claim": "No host chat export or transcript capture was inspected or demonstrated."},
        "comprehension_proven": False,
    }


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise SourceError(message, "invalid_arguments")


def main(argv=None) -> int:
    parser = _ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "read"):
        command = subcommands.add_parser(name)
        command.add_argument("--root", required=True, type=Path)
        command.add_argument("--path", required=True)
        command.add_argument("--expected-sha256")
        if name == "read":
            command.add_argument("--section-id")
            command.add_argument("--heading")
            command.add_argument("--start-line", type=int)
            command.add_argument("--end-line", type=int)
            command.add_argument("--max-chars", type=int)
            command.add_argument("--receipt", type=Path)
    subcommands.add_parser("probe")
    try:
        args = parser.parse_args(argv)
        if args.command == "probe":
            result = probe()
        else:
            document = load_document(args.root, args.path, args.expected_sha256)
            if args.command == "list":
                result = {key: value for key, value in document.items() if key not in ("text", "lines")}
                result.update(sections=list_sections(document), complete=True, heading_parser="ATX and single-line setext; frontmatter and fenced/indented code excluded; HTML containers are not parsed")
            else:
                result = select_passage(document, section_id=args.section_id, heading=args.heading, start_line=args.start_line, end_line=args.end_line, max_chars=args.max_chars)
                if args.receipt is not None:
                    result["receipt"] = write_receipt(args.root, args.path, result.copy(), args.receipt)
        print(json.dumps({"ok": True, **result}, ensure_ascii=True))
        return 0
    except SourceError as exc:
        print(json.dumps({"ok": False, "error": exc.as_dict()}, ensure_ascii=True))
        return 2
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": {"code": "operation_failed", "message": str(exc)}}, ensure_ascii=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
