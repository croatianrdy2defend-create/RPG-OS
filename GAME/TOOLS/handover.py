#!/usr/bin/env python3
"""Read-only structural checks for scene handover; never imports narrative state.

Run with -B. Exit 0: structurally valid (coverage warnings may remain),
1: invalid, 2: incomplete because a file could not be inspected.
This is a point-in-time check, not a prose-fidelity or trust verdict.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat


TREES = ("OS", "ADMIN", "ENGINE", "MODULES", "INSTANCE", "ARCHIVE")
LOG_RUNTIME = ("persistence.py", "play_log.py", "codex_exchange.py", "evidence.py",
               "read_source.py", "handover.py")
GM_SECTIONS = ("Manifest", "Stop point", "Current state", "People and relationships",
               "Private state and processes", "Pending decisions and uncertainty",
               "Source map", "Receiving GM instructions")
RETURN_SECTIONS = ("Manifest", "Resume point", "Events and dialogue", "State changes",
                   "Private changes", "Pending decisions", "Coverage")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
DIGEST = re.compile(r"[0-9a-fA-F]{64}\Z")
RESERVED = re.compile(r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z", re.I)


class Invalid(Exception):
    pass


class Incomplete(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def portable_id(value, label):
    require(isinstance(value, str) and ID.fullmatch(value) is not None
            and not value.endswith(".") and not RESERVED.fullmatch(value),
            f"{label}: expected a portable identifier")
    return value


def route(value):
    require(isinstance(value, str) and value, "empty or non-string route")
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value, f"non-canonical route: {value}")
    for part in path.parts:
        require(part not in (".", "..") and not part.endswith((".", " "))
                and not re.search(r'[<>:"\\|?*\x00-\x1f]', part)
                and not RESERVED.fullmatch(part), f"unsafe route: {value}")
    return path


def no_link(path):
    try:
        info = path.lstat()
    except FileNotFoundError:
        raise Invalid(f"missing path: {path}") from None
    except OSError as exc:
        raise Incomplete(f"cannot inspect {path}: {exc}") from None
    require(not stat.S_ISLNK(info.st_mode)
            and not (getattr(info, "st_file_attributes", 0) & 0x400),
            f"symlink or reparse point refused: {path}")
    return info


def root_path(value):
    path = Path(os.path.abspath(value))
    for component in reversed((path, *path.parents)):
        no_link(component)
    require(path.is_dir(), "root must be a directory")
    return path


def safe_path(root, relative):
    path = root
    for part in route(relative).parts:
        path = path / part
        no_link(path)
    return path


def read_bytes(path):
    before = no_link(path)
    require(stat.S_ISREG(before.st_mode), f"expected regular file: {path}")
    try:
        value = path.read_bytes()
    except OSError as exc:
        raise Incomplete(f"cannot read {path}: {exc}") from None
    after = no_link(path)
    require((before.st_size, before.st_mtime_ns, before.st_ino)
            == (after.st_size, after.st_mtime_ns, after.st_ino),
            f"file changed while reading: {path}")
    return value


def digest(path):
    # Stream large visuals rather than loading the whole snapshot into memory.
    before = no_link(path)
    require(stat.S_ISREG(before.st_mode), f"expected regular file: {path}")
    result = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                result.update(block)
    except OSError as exc:
        raise Incomplete(f"cannot hash {path}: {exc}") from None
    after = no_link(path)
    require((before.st_size, before.st_mtime_ns, before.st_ino)
            == (after.st_size, after.st_mtime_ns, after.st_ino),
            f"file changed while hashing: {path}")
    return result.hexdigest()


def text_file(path):
    try:
        return read_bytes(path).decode("utf-8-sig")
    except UnicodeDecodeError:
        raise Invalid(f"expected UTF-8 text: {path}") from None


def children(path):
    try:
        return sorted(path.iterdir(), key=lambda child: child.name)
    except OSError as exc:
        raise Incomplete(f"cannot list {path}: {exc}") from None


def log_dependencies(root):
    """The selected log runtime and retained review proofs, never host transcripts."""
    head_path = "INSTANCE/JOURNAL/HEAD.json"
    if not os.path.lexists(root / head_path):
        return set()

    def object_at(relative):
        try:
            value = json.loads(text_file(safe_path(root, relative)), object_pairs_hook=unique_object)
        except (ValueError, TypeError) as exc:
            raise Invalid(f"invalid retained JSON {relative}: {exc}") from None
        require(isinstance(value, dict), f"expected JSON object: {relative}")
        return value

    head = object_at(head_path)
    if head.get("schema") != "rpg-journal-v2" or head.get("recording") != "write-only-log":
        return set()
    selected = {"TOOLS/" + name for name in LOG_RUNTIME}
    current = text_file(safe_path(root, "INSTANCE/CURRENT_SAVE.md"))
    # Required explicit routes remain required even when their file is missing.
    reviews = set(re.findall(r"EVIDENCE/incremental-reviews/([A-Za-z0-9._-]+\.json)", current))
    published = head.get("published_save_ids", [])
    require(isinstance(published, list), "journal published_save_ids must be a list")
    for save_id in published:
        name = portable_id(save_id, "published save id") + ".json"
        if os.path.lexists(root / "EVIDENCE/incremental-reviews" / name):
            reviews.add(name)
    for name in sorted(reviews):
        relative = "EVIDENCE/incremental-reviews/" + name
        record = object_at(relative)
        selected.add(relative)
        review = record.get("review", {})
        require(isinstance(review, dict), f"malformed retained review: {relative}")
        receipt = review.get("receipt")
        if receipt is None:
            continue
        require(isinstance(receipt, dict), f"malformed review receipt: {relative}")
        for key in ("bundle", "report", "delivery_receipt"):
            dependency = receipt.get(key)
            if dependency is None and key == "delivery_receipt":
                continue
            parts = route(dependency).parts
            require(len(parts) > 1 and parts[0] == "EVIDENCE",
                    f"handover review {key} must be retained under EVIDENCE")
            path = safe_path(root, dependency)
            require(path.is_dir() if key == "bundle" else path.is_file(),
                    f"invalid retained review {key}: {dependency}")
            selected.add(dependency)
    # Public-source anchors are already retained by ARCHIVE; the legacy floor
    # proof is under INSTANCE/JOURNAL. Never follow their old external host paths.
    return selected


def snapshot(root):
    files = {}
    seen = set()

    def visit(path):
        relative = path.relative_to(root).as_posix()
        route(relative)
        require(relative.casefold() not in seen, f"case-colliding route: {relative}")
        seen.add(relative.casefold())
        info = no_link(path)
        if stat.S_ISDIR(info.st_mode):
            for child in children(path):
                visit(child)
        else:
            require(stat.S_ISREG(info.st_mode), f"non-regular snapshot entry: {relative}")
            files[relative] = digest(path)

    for name in TREES:
        directory = safe_path(root, name)
        require(directory.is_dir(), f"snapshot tree must be a directory: {name}")
        visit(directory)
    for path in children(root):
        if path.suffix.lower() == ".md":
            require(not stat.S_ISDIR(no_link(path).st_mode), f"root markdown is a directory: {path.name}")
            visit(path)
    included = []
    for relative in sorted(log_dependencies(root)):
        path = safe_path(root, relative)
        if not any(path.is_relative_to(parent) for parent in included):
            visit(path)
            included.append(path)
    return dict(sorted(files.items()))


def sections(text, required, label):
    result = {}
    current = None
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            if current is not None:
                result[current].append(line)
            continue
        heading = re.fullmatch(r"## ([^\r\n]+?)\s*", line) if fence is None else None
        if heading:
            current = heading.group(1)
            require(current not in result, f"{label}: duplicate heading {current}")
            result[current] = []
        elif current is not None:
            result[current].append(line)
    require(fence is None, f"{label}: unclosed fenced block")
    result = {name: "\n".join(lines).strip() for name, lines in result.items()}
    for name in required:
        require(bool(result.get(name)), f"{label}: missing or empty ## {name}")
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def manifest(section, schema):
    match = re.fullmatch(r"```json\s*\n([\s\S]+?)\n```", section)
    require(match is not None, "Manifest must contain exactly one fenced json object")
    try:
        result = json.loads(match.group(1), object_pairs_hook=unique_object,
                            parse_constant=lambda value: (_ for _ in ()).throw(Invalid(f"invalid JSON constant: {value}")))
    except (ValueError, TypeError) as exc:
        raise Invalid(f"invalid manifest JSON: {exc}") from None
    require(isinstance(result, dict), "Manifest must be a JSON object")
    require(result.get("schema") == schema, f"expected manifest schema {schema}")
    for key in ("handover_id", "campaign_id", "base_save_id", "base_contract_id"):
        portable_id(result.get(key), key)
    return result


def table_fields(text):
    result = {}
    for line in text.splitlines():
        match = re.fullmatch(r"\s*\|\s*([a-z_]+)\s*\|\s*([^|]+?)\s*\|\s*", line)
        if match:
            key, value = match.groups()
            require(key not in result, f"duplicate identity table field: {key}")
            result[key] = value.strip()
    return result


def plain_fields(text, required, label):
    result = {}
    for line in text.splitlines():
        match = re.fullmatch(r"\s*(?:- )?([a-z_][a-z0-9_]*):\s*(.*?)\s*", line)
        if match:
            key, value = match.groups()
            require(key not in result, f"{label}: duplicate field {key}")
            result[key] = value
    for key in required:
        require(bool(result.get(key)), f"{label}: missing field {key}")
    return result


def validate_digest(value, label):
    require(isinstance(value, str) and DIGEST.fullmatch(value) is not None,
            f"{label}: expected SHA-256 digest")
    return value.lower()


def validate_events(events, label):
    require(isinstance(events, list), f"{label} must be a list")
    for event in events:
        portable_id(event, f"{label} entry")
    require(len(events) == len(set(events)), f"duplicate {label}")
    return events


def resolved_receipt(path, outgoing):
    receipt = plain_fields(text_file(path),
                           ("status", "handover_id", "campaign_id", "base_save_id",
                            "base_contract_id", "resulting_save_id"), "RECEIPT")
    require(receipt["status"] in ("imported", "cancelled"), "malformed RECEIPT status")
    for key in ("handover_id", "campaign_id", "base_save_id", "base_contract_id", "resulting_save_id"):
        portable_id(receipt[key], f"RECEIPT {key}")
    for key in ("handover_id", "campaign_id", "base_save_id", "base_contract_id"):
        require(receipt[key] == outgoing[key], f"RECEIPT {key} mismatch")
    if receipt["status"] == "imported":
        validate_digest(receipt.get("return_sha256"), "RECEIPT return_sha256")
        try:
            events = json.loads(receipt.get("accepted_event_ids", ""))
        except (ValueError, TypeError):
            raise Invalid("RECEIPT accepted_event_ids must be a JSON list") from None
        validate_events(events, "RECEIPT accepted_event_ids")
    else:
        require(bool(receipt.get("reason")), "RECEIPT cancelled status requires reason")
    # The live campaign may already have advanced after this completed handover.
    # Compare receipt lineage with its frozen package, never current live state.
    raise Invalid(f"handover already resolved: {receipt['status']}")


def check(root, package, include_return=False):
    package_route = route(package)
    require(len(package_route.parts) == 2 and package_route.parts[0] == "HANDOVER",
            "package must be HANDOVER/<handover_id>")
    package_id = portable_id(package_route.parts[1], "package basename")
    package_path = safe_path(root, package)
    require(package_path.is_dir(), "package must be a directory")
    # Inspect every package entry to refuse hidden symlinks even if not read below.
    package_seen = set()
    def inspect(path):
        relative = path.relative_to(root).as_posix()
        route(relative)
        require(relative.casefold() not in package_seen, f"case-colliding package route: {relative}")
        package_seen.add(relative.casefold())
        info = no_link(path)
        if stat.S_ISDIR(info.st_mode):
            for child in children(path):
                inspect(child)
        else:
            require(stat.S_ISREG(info.st_mode), f"non-regular package entry: {path}")
    inspect(package_path)
    receipt_path = package_path / "RECEIPT.md"

    gm_path = safe_path(root, f"{package}/GM_STATE.md")
    gm = sections(text_file(gm_path), GM_SECTIONS, "GM_STATE")
    require(gm["Stop point"].lower() != "none", "Stop point cannot be none")
    outgoing = manifest(gm["Manifest"], "scene-handover-v1")
    require(outgoing["handover_id"] == package_id, "handover_id differs from package basename")
    if os.path.lexists(receipt_path):
        resolved_receipt(receipt_path, outgoing)
    require(outgoing.get("source_coverage") in ("complete", "partial", "summary"),
            "source_coverage must declare complete, partial, or summary")
    gaps = outgoing.get("source_gaps")
    require(isinstance(gaps, list) and all(isinstance(gap, str) and gap.strip() for gap in gaps),
            "source_gaps must be a list of nonempty strings")
    require((outgoing["source_coverage"] == "complete" and not gaps)
            or (outgoing["source_coverage"] != "complete" and bool(gaps)),
            "complete coverage must have no gaps; partial/summary coverage must describe gaps")

    active = plain_fields(text_file(safe_path(root, "HANDOVER/ACTIVE.md")),
                          ("handover_id", "campaign_id", "base_save_id", "base_contract_id", "package",
                           "gm_state_sha256"),
                          "ACTIVE")
    for key in ("handover_id", "campaign_id", "base_save_id", "base_contract_id"):
        require(active[key] == outgoing[key], f"ACTIVE {key} mismatch")
    require(active["package"] == package, "ACTIVE package mismatch")
    require(validate_digest(active["gm_state_sha256"], "ACTIVE gm_state_sha256") == digest(gm_path),
            "ACTIVE GM_STATE hash mismatch")
    save = table_fields(text_file(safe_path(root, "INSTANCE/CURRENT_SAVE.md")))
    agreement = table_fields(text_file(safe_path(root, "INSTANCE/CAMPAIGN_CONTRACT.md")))
    require(save.get("campaign_id") == outgoing["campaign_id"] == agreement.get("campaign_id"),
            "base campaign identity mismatch")
    require(save.get("save_id") == outgoing["base_save_id"], "base save identity mismatch")
    require(agreement.get("contract_id") == outgoing["base_contract_id"], "base contract identity mismatch")
    require(agreement.get("status") == "accepted", "base agreement is not accepted")

    expected = outgoing.get("snapshot_files")
    require(isinstance(expected, dict) and expected, "snapshot_files must be a nonempty dictionary")
    for relative, sha in expected.items():
        route(relative)
        validate_digest(sha, f"snapshot_files[{relative}]")
    actual = snapshot(root)
    missing = sorted(set(actual) - set(expected))
    extra = sorted(set(expected) - set(actual))
    require(not missing and not extra, f"snapshot coverage mismatch: omitted={missing}, extra={extra}")
    changed = [relative for relative in actual if expected[relative].lower() != actual[relative]]
    require(not changed, f"snapshot hash mismatch: {changed}")
    conversation_path = safe_path(root, f"{package}/CONVERSATION.md")
    sections(text_file(conversation_path), ("Coverage", "Messages"), "CONVERSATION")
    require(validate_digest(outgoing.get("conversation_sha256"), "conversation_sha256")
            == digest(conversation_path), "conversation hash mismatch")

    event_count = None
    if include_return:
        returned = sections(text_file(safe_path(root, f"{package}/SCENE_RETURN.md")),
                            RETURN_SECTIONS, "SCENE_RETURN")
        incoming = manifest(returned["Manifest"], "scene-return-v1")
        for key in ("handover_id", "campaign_id", "base_save_id", "base_contract_id"):
            require(incoming[key] == outgoing[key], f"return {key} mismatch")
        require(validate_digest(incoming.get("gm_state_sha256"), "gm_state_sha256") == digest(gm_path),
                "return GM_STATE hash mismatch")
        events = validate_events(incoming.get("event_ids"), "event_ids")
        event_count = len(events)
    warnings = []
    if outgoing["source_coverage"] != "complete":
        warnings.append(f"WARNING: {outgoing['source_coverage']} conversation coverage; missing evidence cannot be reconstructed: {gaps}")
    return {"status": "pass_with_warnings" if warnings else "pass", "handover_id": package_id,
            "checked": "return" if include_return else "outgoing", "snapshot_file_count": len(actual),
            "source_coverage": outgoing["source_coverage"], "event_count": event_count,
            "warnings": warnings, "note": "Structural check only; no prose evaluated or state imported."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot", help="Print snapshot hash recipe; write nothing")
    snap.add_argument("--root", default=".")
    verify = commands.add_parser("check", help="Check a frozen outgoing package or proposed return")
    verify.add_argument("--root", default=".")
    verify.add_argument("--package", required=True)
    verify.add_argument("--return", dest="include_return", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = root_path(args.root)
        if args.command == "snapshot":
            report = {"status": "pass", "recipe": "six-trees-and-root-markdown-v1",
                      "included_trees": list(TREES), "root_files": "*.md (case-insensitive)",
                      "excluded_root_trees": ["RECOVERY", "HANDOVER", ".release", ".work", "output"],
                      "snapshot_files": snapshot(root)}
        else:
            report = check(root, args.package, args.include_return)
        code = 0
    except Invalid as exc:
        report, code = {"status": "error", "errors": [str(exc)]}, 1
    except (Incomplete, OSError) as exc:
        report, code = {"status": "incomplete", "errors": [str(exc)]}, 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
