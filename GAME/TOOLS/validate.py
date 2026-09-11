#!/usr/bin/env python3
"""Read-only structural validator for RPG OS v0.9.0 experimental.

The validator writes no report and performs no repair.  Its output is a
point-in-time observation of the supplied tree, not a host or semantic test.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Optional


VALIDATOR_VERSION = "VALIDATE-v3.2.1"

CURRENT_SAVE_FIELDS = (
    "engine", "module", "pc_record", "campaign_id", "save_id", "save_rev",
    "save_parent", "commit_kind", "archive_ref", "evidence_through",
    "safety_state", "datetime", "place",
)
SAVE_SECTIONS = (
    "Situation", "Character state", "Open matters", "Active processes", "Relevant records",
)
SESSION_FIELDS = ("session_id", "phase", "opening_save", "feedback")
PREPARATION_FIELDS = ("campaign_id", "base_save_id", "base_contract_id")
CONTRACT_FIELDS = (
    "campaign_id", "contract_id", "contract_rev", "contract_parent", "status", "module",
)
CONTRACT_SECTIONS = (
    "Campaign promise", "Player control", "GM initiative", "Time and transitions", "Presentation",
)
CONTRACT_CLAUSES = {
    "Play form": "Campaign promise",
    "Form selection": "GM initiative",
    "Structure disclosure": "Presentation",
    "Cuts": "Time and transitions",
    "Retcon": "Player control",
}

SETTING_BRIEF_SECTIONS = (
    "World identity",
    "What is ordinary",
    "Available depth",
)

REQUIRED_FILES = (
    "OS/AGENTS.md",
    "OS/BOOTSTRAP.md",
    "OS/LAW.md",
    "OS/RETRIEVAL.md",
    "OS/AGENT_STATE.md",
    "ENGINE/_CONTRACT.md",
    "ENGINE/freeform.md",
    "MODULES/_CONTRACT.md",
    "MODULES/README.md",
    "INSTANCE/_SCHEMA.md",
    "INSTANCE/CURRENT_SAVE.md",
    "INSTANCE/CAMPAIGN_CONTRACT.md",
    "INSTANCE/SAFETY.md",
    "INSTANCE/KNOWN.md",
    "INSTANCE/NOW.md",
    "INSTANCE/CAST_STATUS.md",
    "INSTANCE/CORRECTIONS.md",
    "INSTANCE/CHAR/README.md",
    "INSTANCE/PEOPLE/README.md",
    "ARCHIVE/_SCHEMA.md",
    "ARCHIVE/INDEX.md",
    "ADMIN/ADD_ENGINE.md",
    "ADMIN/ADD_SETTING_BRIEF.md",
    "ADMIN/CAMPAIGN_BUILD.md",
    "ADMIN/CHARACTER_BUILD.md",
    "ADMIN/CLOSE_CONTRACT.md",
    "ADMIN/SESSION.md",
    "ADMIN/RECOVERY.md",
    "ADMIN/CORRECT.md",
    "ADMIN/UPGRADE_V07.md",
    "ADMIN/UPGRADE_V08.md",
    "ADMIN/LOAD.md",
    "ADMIN/MIGRATE_V05.md",
    "ADMIN/NEW_GAME.md",
    "ADMIN/REFINE_SETTING_BRIEF.md",
    "ADMIN/REVIEW.md",
    "ADMIN/RECALIBRATE.md",
    "ADMIN/SCENE_HANDOVER.md",
    "ADMIN/VALIDATE.md",
    "ADMIN/SOURCE_ACCESS.md",
    "ADMIN/EVIDENCE_AUDIT.md",
    "EVIDENCE/README.md",
    "TOOLS/validate.py",
    "TOOLS/handover.py",
    "TOOLS/read_source.py",
    "TOOLS/search_index.py",
    "TOOLS/evidence.py",
    "TOOLS/LICENSE",
    "QUICKSTART.md",
    "INSTALLATION.md",
    "COMMANDS.md",
    "README.md",
    "VERSION",
    "LICENSE",
)

CAPABILITIES = {
    "WORLD",
    "PEOPLE",
    "INST",
    "SEEDS",
    "CLOCKS",
    "TRUTH",
    "VISUAL",
    "RULES_HOOKS",
}

CHARACTER_BUILD_SUPPORT = {
    "self-contained",
    "operator-values-required",
    "no-mechanical-sheet",
}
PC_ROUTING_CLASS = "character-routing-index"

SENTINELS = {"", "none", "unbound", "null", "n/a"}
PLACEHOLDERS = {"", "none", "none.", "[]", "n/a", "tbd", "todo", "fixme", "placeholder", "-", "—"}
SEVERITY_ORDER = {"ERROR": 0, "INCOMPLETE": 1, "WARNING": 2, "INFO": 3}
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HTML_BLOCK_TAGS = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|"
    "fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|"
    "menu|menuitem|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|"
    "title|tr|track|ul"
)



EMPTY_INSTANCE_TEMPLATES = {
    'INSTANCE/KNOWN.md': '# KNOWN\n\nWhat the PC has actually learned, with scope, source and uncertainty when material. Hearing a rumor establishes that it was heard, not that it is true. Knowing a public description does not establish every detail of its subject. Do not replace this record with general world lore or copy full source passages when an exact pointer suffices.\n\n## Learned facts\n\nnone\n',
    'INSTANCE/NOW.md': '# NOW\n\nNonresident current private conditions and mutable campaign/world-system state. Keep complete operative values and the minimum established system rules needed to continue; use explicit shards when independently useful. Public resume cues belong in CURRENT_SAVE, not a second hot roster.\n\nA specifically named MODULE T0 snapshot supplies continuity only before later accepted change/current override and while no declared transition is due. At the next save, materialize complete current state here or in its selected shard, applying each unsaved transition once. Do not merge it with the older snapshot afterward.\n\n## Current conditions and systems\n\nnone\n',
    'INSTANCE/CAST_STATUS.md': '# CAST_STATUS\n\nCompact stable person-id and exact-record mapping, used for an already relevant person. This is not a menu for introducing cast or a second relationship summary. Promote only established durable identity/state; transient occupants may remain transient.\n\n## Person routes\n\nnone\n',
    'INSTANCE/CORRECTIONS.md': '# CORRECTIONS\n\nAccepted rulings and narrow corrections, with their scope and source. These may supersede an earlier claim without erasing its historical record. Record an exact affected source and the replacement qualification when relevant; preserve unrelated accepted play. An OOC correction is not a new fictional event.\n\n## Rulings and corrections\n\nnone\n',
}

@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: Optional[int]
    message: str


class ValidationExecutionError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strip_code_ticks(value: str) -> str:
    value = value.strip()
    match = re.match(r"^(`+)(.*)\1$", value, flags=re.DOTALL)
    return match.group(2).strip() if match else value


def is_sentinel(value: str) -> bool:
    return strip_code_ticks(value).strip().casefold() in SENTINELS


def is_placeholder(value: str) -> bool:
    normalized = value.strip()
    while True:
        reduced = re.sub(r"^(?:>\s*|[-*+]\s+|[0-9]+[.)]\s+)", "", normalized)
        if reduced == normalized:
            break
        normalized = reduced.strip()
    normalized = strip_code_ticks(normalized).strip()
    core = normalized.rstrip(".!?:;").strip().casefold()
    square = re.fullmatch(r"\[([^\[\]]+)\]", normalized)
    square_core = square.group(1).rstrip(".!?:;").strip().casefold() if square else ""
    return core in PLACEHOLDERS or (square is not None and square_core in PLACEHOLDERS) or bool(re.fullmatch(r"<[^>]*>", normalized))


def strip_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """Blank HTML comments while preserving columns and inline-code literals."""

    output = list(line)
    index = 0
    code_delimiter = 0
    while index < len(line):
        if in_comment:
            end = line.find("-->", index)
            if end < 0:
                for position in range(index, len(output)):
                    output[position] = " "
                return "".join(output), True
            for position in range(index, end + 3):
                output[position] = " "
            index = end + 3
            in_comment = False
            continue
        if line[index] == "`":
            end = index
            while end < len(line) and line[end] == "`":
                end += 1
            run = end - index
            if code_delimiter == 0:
                code_delimiter = run
            elif run == code_delimiter:
                code_delimiter = 0
            index = end
            continue
        if code_delimiter == 0 and line.startswith("<!--", index):
            in_comment = True
            continue
        index += 1
    return "".join(output), in_comment


def is_indented_code(line: str) -> bool:
    columns = 0
    for char in line:
        if char == " ":
            columns += 1
        elif char == "\t":
            columns += 4 - (columns % 4)
        else:
            break
    return columns >= 4


def split_markdown_row(line: str) -> Optional[list[str]]:
    """Split a pipe table row, respecting escaped pipes and inline code spans."""

    raw = line.strip()
    if not (raw.startswith("|") and raw.endswith("|")):
        return None
    raw = raw[1:-1]
    cells: list[str] = []
    cell: list[str] = []
    code_delimiter = 0
    index = 0
    while index < len(raw):
        char = raw[index]
        if char == "\\" and index + 1 < len(raw):
            following = raw[index + 1]
            if following == "|":
                cell.append("|")
                index += 2
                continue
            cell.extend((char, following))
            index += 2
            continue
        if char == "`":
            end = index
            while end < len(raw) and raw[end] == "`":
                end += 1
            run = end - index
            if code_delimiter == 0:
                code_delimiter = run
            elif run == code_delimiter:
                code_delimiter = 0
            cell.append(raw[index:end])
            index = end
            continue
        if char == "|" and code_delimiter == 0:
            cells.append("".join(cell).strip())
            cell = []
        else:
            cell.append(char)
        index += 1
    cells.append("".join(cell).strip())
    return cells


def split_table_like_row(line: str) -> Optional[list[str]]:
    """Parse a GFM-style pipe row with optional outer pipes for shadow checks."""

    strict = split_markdown_row(line)
    if strict is not None:
        return strict
    raw = line.strip()
    if "|" not in raw:
        return None
    wrapped = raw
    if not wrapped.startswith("|"):
        wrapped = "|" + wrapped
    if not wrapped.endswith("|"):
        wrapped += "|"
    cells = split_markdown_row(wrapped)
    return cells if cells is not None and len(cells) >= 2 else None


def is_separator_cell(cell: str) -> bool:
    return bool(re.fullmatch(r":?-{3,}:?", cell.strip()))


def structural_markdown_lines(lines: list[str]) -> tuple[list[bool], list[str]]:
    """Return a live-line mask and comment-sanitized Markdown source lines."""

    result: list[bool] = []
    sanitized: list[str] = []
    fence_char: Optional[str] = None
    fence_length = 0
    html_comment = False
    raw_html_end: Optional[re.Pattern[str]] = None
    raw_html_until_blank = False
    frontmatter_end = -1
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                frontmatter_end = index
                break
    for index, line in enumerate(lines):
        if index <= frontmatter_end:
            result.append(False)
            sanitized.append("")
            continue
        if raw_html_until_blank:
            if not line.strip():
                raw_html_until_blank = False
            result.append(False)
            sanitized.append("")
            continue
        if raw_html_end is not None:
            if raw_html_end.search(line):
                raw_html_end = None
            result.append(False)
            sanitized.append("")
            continue
        # Once a code fence is open, only its matching close delimiter is
        # structural. Comment-looking text inside the example must not alter
        # the state used for lines after the fence.
        if fence_char is not None:
            fence = re.match(r"^[ ]{0,3}(`{3,}|~{3,})[ \t]*$", line)
            if fence:
                run = fence.group(1)
                if run[0] == fence_char and len(run) >= fence_length:
                    fence_char, fence_length = None, 0
            result.append(False)
            sanitized.append("")
            continue
        structural_line, html_comment = strip_html_comments(line, html_comment)
        if not structural_line.strip():
            result.append(False)
            sanitized.append(structural_line)
            continue
        raw_html = re.match(r"^[ ]{0,3}<(script|pre|style|textarea)(?:\s|>|$)", structural_line, flags=re.IGNORECASE)
        if raw_html:
            tag = raw_html.group(1).casefold()
            if not re.search(rf"</{re.escape(tag)}\s*>", structural_line, flags=re.IGNORECASE):
                raw_html_end = re.compile(rf"</{re.escape(tag)}\s*>", flags=re.IGNORECASE)
            result.append(False)
            sanitized.append("")
            continue
        raw_marker: Optional[re.Pattern[str]] = None
        stripped_left = structural_line.lstrip(" ") if len(structural_line) - len(structural_line.lstrip(" ")) <= 3 else structural_line
        if stripped_left.startswith("<?"):
            raw_marker = re.compile(r"\?>")
        elif stripped_left.startswith("<![CDATA["):
            raw_marker = re.compile(r"\]\]>")
        elif re.match(r"^<![A-Z]", stripped_left):
            raw_marker = re.compile(r">")
        if raw_marker is not None:
            if not raw_marker.search(structural_line):
                raw_html_end = raw_marker
            result.append(False)
            sanitized.append("")
            continue
        block_tag = re.match(rf"^[ ]{{0,3}}</?(?:{HTML_BLOCK_TAGS})(?:\s|/?>|$)", structural_line, flags=re.IGNORECASE)
        complete_tag = re.match(r"^[ ]{0,3}</?[A-Za-z][^<>]*>[ \t]*$", structural_line)
        if block_tag or complete_tag:
            raw_html_until_blank = True
            result.append(False)
            sanitized.append("")
            continue
        fence = re.match(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$", structural_line)
        if fence:
            run = fence.group(1)
            info = fence.group(2)
            if run[0] != "`" or "`" not in info:
                fence_char, fence_length = run[0], len(run)
                result.append(False)
                sanitized.append("")
                continue
        result.append(not is_indented_code(structural_line))
        sanitized.append(structural_line)
    return result, sanitized


def outside_fence_mask(lines: list[str]) -> list[bool]:
    """Mark structurally live Markdown lines, excluding metadata, code, and comments."""

    return structural_markdown_lines(lines)[0]


def iter_literal_headings(text: str) -> Iterable[tuple[int, int, str]]:
    """Yield visible ATX headings outside metadata, code, and comments."""

    lines = text.splitlines()
    visible, structural = structural_markdown_lines(lines)
    for number, line in enumerate(lines, 1):
        if not visible[number - 1]:
            continue
        line = structural[number - 1]
        heading = re.match(r"^[ ]{0,3}(#{1,6})[ \t]+(.+?)[ \t]*$", line)
        if not heading:
            continue
        title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(2)).strip()
        yield number, len(heading.group(1)), title


def section_text(text: str, wanted: str, level: int = 2) -> tuple[Optional[str], Optional[int], int]:
    """Return an exact ATX section body, its first source line, and match count."""

    headings = list(iter_literal_headings(text))
    matches = [(line, heading_level) for line, heading_level, title in headings if heading_level == level and title == wanted]
    if not matches:
        return None, None, 0
    start = matches[0][0]
    later = [line for line, heading_level, _title in headings if line > start and heading_level <= level]
    end = min(later) - 1 if later else len(text.splitlines())
    lines = text.splitlines()
    return "\n".join(lines[start:end]), start + 1, len(matches)


def heading_body(text: str, start_line: int, level: int) -> str:
    """Return the body after one known heading through the next peer/ancestor."""

    headings = list(iter_literal_headings(text))
    later = [line for line, heading_level, _title in headings if line > start_line and heading_level <= level]
    end = min(later) - 1 if later else len(text.splitlines())
    lines = text.splitlines()
    return "\n".join(lines[start_line:end])


def backticked_markdown_paths(text: str) -> list[tuple[int, str]]:
    """Extract explicit backticked .md routes outside metadata, code, and comments."""

    routes: list[tuple[int, str]] = []
    lines = text.splitlines()
    visible, structural = structural_markdown_lines(lines)
    for number, line in enumerate(lines, 1):
        if not visible[number - 1]:
            continue
        line = structural[number - 1]
        for match in re.finditer(r"`([^`\r\n]+\.md(?:#[^`\r\n]+)?)`", line, flags=re.IGNORECASE):
            routes.append((number, match.group(1).strip()))
    return routes


def heading_map(text: str) -> dict[str, list[int]]:
    result: dict[str, list[int]] = defaultdict(list)
    for line, _level, title in iter_literal_headings(text):
        result[title].append(line)
    return dict(result)


def declares_routing_index(frontmatter: dict[str, str]) -> bool:
    """Return whether scalar front matter explicitly marks a routing index."""

    marker = frontmatter.get("class", "").strip().casefold()
    return marker == "routing-index" or marker.endswith("-routing-index")


def empty_template_signature(text: str) -> tuple[str, ...]:
    """Normalize whitespace/table spacing while retaining every content token."""

    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = re.sub(r"(?<!\\)\|", " | ", normalized)
    return tuple(normalized.split())


def extract_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, []
    closing: Optional[int] = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return {}, ["front matter has no closing delimiter"]
    values: dict[str, str] = {}
    errors: list[str] = []
    for offset, line in enumerate(lines[1:closing], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)\s*$", line)
        if not match:
            # Nested/list YAML is outside the scalar subset used by the validator.
            continue
        key, value = match.group(1), match.group(2)
        if key in values:
            errors.append(f"duplicate front-matter key {key!r} at line {offset}")
        values[key] = strip_code_ticks(value.strip("\"'"))
    return values, errors


def snapshot_tree(root: Path) -> tuple[dict[str, str], str]:
    entries: dict[str, str] = {}

    def walk_error(error: OSError) -> None:
        raise ValidationExecutionError(f"cannot scan tree: {error}")

    try:
        for directory, dirnames, filenames in os.walk(root, topdown=True, onerror=walk_error, followlinks=False):
            dirnames.sort()
            filenames.sort()
            base = Path(directory)
            retained: list[str] = []
            for name in dirnames:
                path = base / name
                relative = path.relative_to(root).as_posix() + "/"
                if path.is_symlink():
                    entries[relative] = "L:" + os.readlink(path)
                else:
                    entries[relative] = "D:directory"
                    retained.append(name)
            dirnames[:] = retained
            for name in filenames:
                path = base / name
                relative = path.relative_to(root).as_posix()
                if path.is_symlink():
                    entries[relative] = "L:" + os.readlink(path)
                    continue
                if not path.is_file():
                    entries[relative] = "S:special"
                    continue
                data = path.read_bytes()
                entries[relative] = f"F:{len(data)}:{sha256_bytes(data)}"
    except (OSError, ValueError) as exc:
        raise ValidationExecutionError(f"cannot snapshot tree: {exc}") from exc
    digest = hashlib.sha256()
    for relative, descriptor in sorted(entries.items()):
        digest.update(relative.encode("utf-8", "surrogateescape"))
        digest.update(b"\0")
        digest.update(descriptor.encode("utf-8", "surrogateescape"))
        digest.update(b"\n")
    return entries, digest.hexdigest()


class Validator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[Finding] = []
        self.metrics: dict[str, Any] = {}
        self._text_cache: dict[Path, str] = {}
        self.current: dict[str, str] = {}
        self.contract: dict[str, str] = {}
        self.bound = False
        self.engine_ids: dict[str, list[Path]] = defaultdict(list)
        self.archive_rows: list[dict[str, Any]] = []
        self.archive_folders: set[Path] = set()
        self.archive_folder_ids: dict[Path, str] = {}
        self._parsed_sessions: set[tuple[Path, str]] = set()

    def add(
        self,
        severity: str,
        code: str,
        path: str = ".",
        message: str = "",
        line: Optional[int] = None,
    ) -> None:
        self.findings.append(Finding(severity, code, path, line, message))

    def relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    def read_text(self, path: Path, code: str = "FILE_READ") -> Optional[str]:
        if path in self._text_cache:
            return self._text_cache[path]
        relative = self.relative(path)
        try:
            probe = path
            while probe != self.root and probe.parent != probe:
                if probe.is_symlink():
                    self.add("ERROR", "PATH_SYMLINK", relative, "authoritative path crosses a symlink")
                    return None
                probe = probe.parent
            data = path.read_bytes()
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            self.add("ERROR", code, relative, f"not valid UTF-8: {exc}")
            return None
        except OSError as exc:
            self.add("INCOMPLETE", code, relative, f"could not read: {exc}")
            return None
        self._text_cache[path] = text
        return text

    def find_table(
        self,
        text: str,
        expected_header: list[str],
        path: str,
        code: str,
        required: bool = True,
        line_offset: int = 0,
        strict_tail: bool = True,
    ) -> Optional[list[dict[str, Any]]]:
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        expected = [item.casefold() for item in expected_header]
        matches: list[int] = []
        for index, line in enumerate(lines):
            if not visible[index]:
                continue
            cells = split_markdown_row(structural[index])
            if cells is not None and [strip_code_ticks(cell).casefold() for cell in cells] == expected:
                matches.append(index)
        if not matches:
            if required:
                self.add("ERROR", code + "_MISSING", path, f"missing table header: {' | '.join(expected_header)}")
            return None
        if len(matches) > 1:
            self.add("ERROR", code + "_DUPLICATE", path, "table header occurs more than once")
        start = matches[0]
        if start + 1 >= len(lines) or not visible[start + 1]:
            self.add("ERROR", code + "_SEPARATOR", path, "table has no separator row", start + 2 + line_offset)
            return []
        separator = split_markdown_row(structural[start + 1])
        if separator is None or len(separator) != len(expected) or not all(is_separator_cell(cell) for cell in separator):
            self.add("ERROR", code + "_SEPARATOR", path, "invalid table separator row", start + 2 + line_offset)
            return []
        rows: list[dict[str, Any]] = []
        parsed_end = start + 2
        for index in range(start + 2, len(lines)):
            if not visible[index] or not structural[index].strip():
                parsed_end = index
                break
            cells = split_markdown_row(structural[index])
            if cells is None:
                parsed_end = index
                break
            parsed_end = index + 1
            if len(cells) != len(expected):
                self.add(
                    "ERROR",
                    code + "_COLUMNS",
                    path,
                    f"expected {len(expected)} cells, found {len(cells)}",
                    index + 1 + line_offset,
                )
                continue
            row = {expected[column]: cells[column].strip() for column in range(len(expected))}
            row["_line"] = index + 1 + line_offset
            rows.append(row)
        if strict_tail:
            for index in range(parsed_end, len(lines)):
                if not visible[index] or not structural[index].strip():
                    continue
                cells = split_table_like_row(structural[index])
                if cells is None or all(is_separator_cell(cell) for cell in cells):
                    continue
                self.add(
                    "ERROR",
                    code + "_SHADOW_ROW",
                    path,
                    "table-shaped row occurs outside the one contiguous authoritative table",
                    index + 1 + line_offset,
                )
        return rows

    def exact_field_record(
        self,
        text: str,
        relative: str,
        fields: tuple[str, ...],
        code: str,
    ) -> Optional[dict[str, str]]:
        """Parse required metadata; warn about benign extension fields."""

        # Metadata ends at the first literal H2. Tables in readable sections are
        # legitimate content, not shadow metadata. Shadow rows before that H2
        # are still rejected by the strict table parser.
        first_section = next((line for line, level, _title in iter_literal_headings(text) if level == 2), None)
        metadata = "\n".join(text.splitlines()[:first_section - 1]) if first_section else text
        rows = self.find_table(metadata, ["Field", "Value"], relative, code + "_TABLE")
        if first_section:
            section_lines = text.splitlines()[first_section - 1:]
            visible, structural = structural_markdown_lines(section_lines)
            for offset, line in enumerate(structural):
                cells = split_markdown_row(line) if visible[offset] else None
                if cells and [strip_code_ticks(cell).casefold() for cell in cells] == ["field", "value"]:
                    self.add("ERROR", code + "_SHADOW_METADATA", relative,
                             "Field/Value is reserved for the one metadata table; section tables need descriptive column headings",
                             first_section + offset)
        if rows is None:
            return None
        values: dict[str, str] = {}
        allowed = set(fields)
        for row in rows:
            field = strip_code_ticks(row["field"]).strip()
            value = strip_code_ticks(row["value"]).strip()
            if field in values:
                self.add("ERROR", code + "_DUPLICATE_FIELD", relative, f"duplicate field {field!r}", row["_line"])
                continue
            if field not in allowed:
                self.add("WARNING", code + "_UNKNOWN_FIELD", relative, f"extension metadata {field!r} is not interpreted by this validator", row["_line"])
            if not value:
                self.add("ERROR", code + "_EMPTY_FIELD", relative, f"field {field!r} is blank", row["_line"])
            values[field] = value
        for field in fields:
            if field not in values:
                self.add("ERROR", code + "_MISSING_FIELD", relative, f"missing required field {field!r}")
        return values

    @staticmethod
    def canonical_revision(value: str) -> Optional[int]:
        if not re.fullmatch(r"0|[1-9][0-9]*", value):
            return None
        return int(value)

    @staticmethod
    def choice_or_custom(value: str, choices: set[str]) -> bool:
        return value in choices or bool(re.fullmatch(r"custom:\s+\S(?:.*\S)?", value))

    def safe_path(
        self,
        raw_value: str,
        base: Path,
        boundary: Path,
        code: str,
        source_path: str,
        line: Optional[int] = None,
        root_prefix: Optional[str] = None,
        allow_parent_segments: bool = False,
    ) -> Optional[Path]:
        value = strip_code_ticks(raw_value).strip()
        if is_sentinel(value):
            self.add("ERROR", code, source_path, "path is empty or a sentinel", line)
            return None
        if "\x00" in value or "\\" in value or re.match(r"^[A-Za-z]:", value):
            self.add("ERROR", code, source_path, f"unsafe/non-POSIX path {value!r}", line)
            return None
        raw_parts = value.split("/")
        pure = PurePosixPath(value)
        prohibited = {"", "."} if allow_parent_segments else {"", ".", ".."}
        if pure.is_absolute() or any(part in prohibited for part in raw_parts):
            self.add("ERROR", code, source_path, f"absolute or traversing path {value!r}", line)
            return None
        if root_prefix and pure.parts and pure.parts[0] == root_prefix:
            candidate = self.root.joinpath(*pure.parts)
            self.add("WARNING", code + "_NONCANONICAL", source_path, f"prefer path relative to {root_prefix}/: {value!r}", line)
        else:
            candidate = base.joinpath(*pure.parts)
        try:
            resolved_boundary = boundary.resolve(strict=False)
            resolved = candidate.resolve(strict=False)
            resolved.relative_to(resolved_boundary)
        except (OSError, ValueError):
            self.add("ERROR", code, source_path, f"path escapes its authority boundary: {value!r}", line)
            return None
        probe = candidate
        while True:
            if probe.is_symlink():
                self.add("ERROR", code, source_path, f"path crosses symlink: {value!r}", line)
                return None
            if probe == boundary or probe == self.root or probe.parent == probe:
                break
            probe = probe.parent
        return candidate

    def check_required_files(self) -> None:
        for relative in REQUIRED_FILES:
            path = self.root / relative
            if not path.is_file() or path.is_symlink():
                self.add("ERROR", "CORE_REQUIRED_FILE", relative, "required regular file is missing")
                continue
            text = self.read_text(path, "CORE_REQUIRED_READ")
            if text is not None and not text.strip():
                self.add("ERROR", "CORE_REQUIRED_EMPTY", relative, "required text file is empty")

    def check_snapshot_types(self, snapshot: dict[str, str]) -> None:
        for relative, descriptor in snapshot.items():
            if descriptor.startswith("L:"):
                self.add("WARNING", "TREE_SYMLINK", relative, "unrouted symlink is nonportable; any required or authoritative route through it is an error")
            elif descriptor.startswith("S:"):
                self.add("WARNING", "TREE_SPECIAL_FILE", relative, "special file is outside portable Markdown validation")
        folded: dict[str, list[str]] = defaultdict(list)
        for relative in snapshot:
            folded[relative.casefold()].append(relative)
        for paths in folded.values():
            if len(paths) > 1:
                self.add("ERROR", "TREE_CASE_COLLISION", paths[0], "case-insensitive collision: " + ", ".join(sorted(paths)))

    def check_law(self) -> None:
        # Record the observed core for provenance; revisions are allowed.
        text = self.read_text(self.root / "OS/LAW.md", "LAW_READ")
        if text is not None:
            self.metrics["law_sha256"] = sha256_bytes((self.root / "OS/LAW.md").read_bytes())

    def check_sections(self, text: str, relative: str, sections: tuple[str, ...],
                       code: str, unbound: bool = False) -> dict[str, str]:
        bodies: dict[str, str] = {}
        for section in sections:
            body, line, count = section_text(text, section, 2)
            if count != 1:
                self.add("ERROR", code + "_SECTION_COUNT", relative,
                         f"expected exactly one level-two {section!r} section; found {count}")
                continue
            compact = (body or "").strip()
            bodies[section] = compact
            if unbound and compact != "none":
                self.add("ERROR", code + "_UNBOUND_SECTION", relative,
                         f"unbound section {section!r} must contain only 'none'", line)
            elif not compact or (compact != "none" and not self.meaningful_payload(compact)):
                self.add("ERROR", code + "_SECTION_EMPTY", relative,
                         f"section {section!r} requires readable content or explicit 'none'", line)
        return bodies

    def check_current_routes(self, text: str) -> None:
        # Only explicit backticked Markdown routes are machine-checked. A cue
        # need not reveal its private content to establish a resolvable route.
        relative = "INSTANCE/CURRENT_SAVE.md"
        for line, raw in backticked_markdown_paths(text):
            file_part, separator, heading = raw.partition("#")
            target = self.safe_path(file_part, self.root, self.root, "SAVE_RECORD_PATH", relative, line)
            if target is None:
                continue
            if not target.is_file():
                self.add("ERROR", "SAVE_RECORD_MISSING", relative, f"record route is missing: {raw!r}", line)
                continue
            target_text = self.read_text(target, "SAVE_RECORD_READ")
            if separator and target_text is not None and len(heading_map(target_text).get(heading, [])) != 1:
                self.add("ERROR", "SAVE_RECORD_HEADING", relative,
                         f"record heading must resolve exactly once: {raw!r}", line)

    def check_session_continuity(self, text: str, relative: str, initial: bool = False) -> None:
        """Check optional administrative structure, never infer a session trigger."""
        body, line, count = section_text(text, "Session continuity", 2)
        # A misplaced control table cannot masquerade as harmless extra prose.
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        heading_lines = list(iter_literal_headings(text))
        owner = ""
        headings = {number: (level, title) for number, level, title in heading_lines}
        for number, content in enumerate(structural, 1):
            if number in headings and headings[number][0] <= 2:
                owner = headings[number][1] if headings[number][0] == 2 else ""
            cells = split_table_like_row(content) if visible[number - 1] else None
            if cells and [strip_code_ticks(cell).casefold() for cell in cells] == ["session item", "value"]:
                if owner != "Session continuity":
                    self.add("ERROR", "SESSION_TABLE_SCOPE", relative,
                             "session control table must be inside the level-two Session continuity section", number)
                elif split_markdown_row(content) is None:
                    self.add("ERROR", "SESSION_TABLE_NONCANONICAL", relative,
                             "session control requires outer pipes; another rendered table cannot shadow it", number)
        if count == 0:
            if relative == "INSTANCE/CURRENT_SAVE.md":
                self.metrics["session_continuity"] = "legacy/unrecorded"
            return
        if count != 1:
            self.add("ERROR", "SESSION_SECTION_COUNT", relative,
                     f"expected at most one level-two Session continuity section; found {count}")
            return
        compact = (body or "").strip()
        if compact == "none":
            if relative == "INSTANCE/CURRENT_SAVE.md":
                self.metrics["session_continuity"] = "not-started"
            return
        if initial:
            self.add("ERROR", "SESSION_INITIAL_CONTENT", relative,
                     "unbound/bind/T0 session continuity must be absent or literal none; never inherit played-session state", line)
        rows = self.find_table(body or "", ["Session item", "Value"], relative, "SESSION_TABLE", line_offset=(line or 1) - 1)
        if rows is None:
            return
        body_visible, body_structural = structural_markdown_lines((body or "").splitlines())
        for offset, content in enumerate(body_structural):
            cells = split_table_like_row(content) if body_visible[offset] else None
            if cells and [strip_code_ticks(cell).casefold() for cell in cells] == ["session item", "value"] and split_markdown_row(content) is not None:
                break
            if cells and strip_code_ticks(cells[0]).strip() in SESSION_FIELDS:
                self.add("ERROR", "SESSION_TABLE_SHADOW_ROW", relative,
                         "session item occurs before the authoritative table", (line or 1) + offset)
        values: dict[str, str] = {}
        for row in rows:
            field = strip_code_ticks(row["session item"]).strip()
            value = strip_code_ticks(row["value"]).strip()
            if field in values:
                self.add("ERROR", "SESSION_DUPLICATE_FIELD", relative, f"duplicate session item {field!r}", row["_line"])
                continue
            if field not in SESSION_FIELDS:
                self.add("ERROR", "SESSION_UNKNOWN_FIELD", relative, f"unknown session item {field!r}; outstanding items use prose", row["_line"])
            if not value:
                self.add("ERROR", "SESSION_EMPTY_FIELD", relative, f"session item {field!r} is blank", row["_line"])
            values[field] = value
        for field in SESSION_FIELDS:
            if field not in values:
                self.add("ERROR", "SESSION_MISSING_FIELD", relative, f"missing session item {field!r}")
        session_id = values.get("session_id", "")
        if not SAFE_ID.fullmatch(session_id) or is_sentinel(session_id) or is_placeholder(session_id):
            self.add("ERROR", "SESSION_ID_FORMAT", relative, "session_id requires a portable non-placeholder play-session id")
        if values.get("phase") not in {"active", "closing", "ended"}:
            self.add("ERROR", "SESSION_PHASE", relative, "session phase must be active, closing or ended")
        opening = values.get("opening_save", "")
        if opening != "unknown" and (not SAFE_ID.fullmatch(opening) or is_sentinel(opening) or is_placeholder(opening)):
            self.add("ERROR", "SESSION_OPENING_SAVE", relative, "opening_save requires a portable save id or honest unknown")
        if values.get("feedback") not in {"not-due", "pending", "received", "declined", "not-provided"}:
            self.add("ERROR", "SESSION_FEEDBACK", relative, "feedback must be not-due, pending, received, declined or not-provided")
        elif values.get("phase") in {"closing", "ended"} and values.get("feedback") == "not-due":
            self.add("ERROR", "SESSION_FEEDBACK_DUE", relative,
                     "closing/ended sessions require an actual feedback disposition; an owed invitation or reply stays pending")
        if relative == "INSTANCE/CURRENT_SAVE.md":
            self.metrics["session_continuity"] = values.get("phase", "unrecognized")
            self.metrics["session_id"] = session_id

    def check_current_save(self) -> None:
        relative = "INSTANCE/CURRENT_SAVE.md"
        text = self.read_text(self.root / relative, "SAVE_READ")
        if text is None:
            return
        frontmatter, errors = extract_frontmatter(text)
        for error in errors:
            self.add("ERROR", "SAVE_FRONTMATTER", relative, error)
        for field, expected in {"id": "instance.current_save", "class": "live-checkpoint", "temperature": "resident"}.items():
            if frontmatter.get(field) != expected:
                self.add("ERROR", "SAVE_FRONTMATTER_VALUE", relative, f"front-matter {field} must be {expected!r}")
        values = self.exact_field_record(text, relative, CURRENT_SAVE_FIELDS, "SAVE")
        if values is None:
            return
        self.current = values
        if "evidence_through" not in values and any(field in values for field in ("immediate_scene", "hot_identifiers", "causal_frontier")):
            self.add("ERROR", "SAVE_REQUIRES_UPGRADE", relative,
                     "legacy save format requires explicit ADMIN/UPGRADE_V07.md mapping; validator will not migrate it")
        commit = values.get("commit_kind", "")
        revision = self.canonical_revision(values.get("save_rev", ""))
        if revision is None:
            self.add("ERROR", "SAVE_REVISION", relative, "save_rev must be a canonical nonnegative ASCII integer")
            revision = -1
        if commit not in {"unbound", "bind", "checkpoint", "close"}:
            self.add("ERROR", "SAVE_COMMIT_KIND", relative, f"invalid commit_kind {commit!r}")
        if values.get("safety_state") not in {"floor-only", "active"}:
            self.add("ERROR", "SAVE_SAFETY_STATE", relative, "safety_state must be floor-only or active")
        engine, module = values.get("engine", ""), values.get("module", "")
        if (engine == "unbound") != (module == "unbound"):
            self.add("ERROR", "SAVE_PARTIAL_BINDING", relative, "engine and module binding states disagree")
        self.bound = engine != "unbound" and module != "unbound"
        sections = self.check_sections(text, relative, SAVE_SECTIONS, "SAVE", not self.bound)
        self.check_session_continuity(text, relative, initial=not self.bound or commit == "bind")
        if not self.bound:
            expected = {field: "none" for field in CURRENT_SAVE_FIELDS}
            expected.update(engine="unbound", module="unbound", save_rev="0",
                            commit_kind="unbound", safety_state="floor-only")
            for field, value in expected.items():
                if values.get(field) != value:
                    self.add("ERROR", "SAVE_UNBOUND_VALUE", relative, f"unbound save requires {field}: {value}")
        else:
            if commit not in {"bind", "checkpoint", "close"}:
                self.add("ERROR", "SAVE_BOUND_COMMIT", relative, "bound save requires bind/checkpoint/close")
            for field in ("engine", "module", "campaign_id", "save_id"):
                value = values.get(field, "")
                if not SAFE_ID.fullmatch(value) or is_placeholder(value) or is_sentinel(value):
                    self.add("ERROR", "SAVE_ID_FORMAT", relative, f"{field} requires a portable non-placeholder id")
            if revision < 1 or (commit == "bind" and revision != 1) or (commit in {"checkpoint", "close"} and revision < 2):
                self.add("ERROR", "SAVE_BOUND_REVISION", relative, "bind requires revision 1; later commits require revision >= 2")
            parent = values.get("save_parent", "")
            if commit == "bind" and parent != "none":
                self.add("ERROR", "SAVE_BIND_PARENT", relative, "bind requires save_parent none")
            elif commit in {"checkpoint", "close"} and (not SAFE_ID.fullmatch(parent) or is_sentinel(parent) or is_placeholder(parent)):
                self.add("ERROR", "SAVE_PARENT_FORMAT", relative, "later commits require the prior portable save id")
            if parent == values.get("save_id"):
                self.add("ERROR", "SAVE_PARENT_SELF", relative, "save_id must not equal save_parent")
            for field in ("datetime", "place"):
                if is_placeholder(values.get(field, "")) or is_sentinel(values.get(field, "")):
                    self.add("ERROR", "SAVE_BOUND_VALUE", relative, f"bound {field} needs a value; use honest 'unspecified' if unknown")
            for section in ("Situation", "Character state"):
                if sections.get(section) == "none":
                    self.add("ERROR", "SAVE_BOUND_SECTION", relative, f"bound {section!r} needs accepted present content")
            archive_ref, evidence = values.get("archive_ref", ""), values.get("evidence_through", "")
            if (archive_ref == "none") != (evidence == "none"):
                self.add("ERROR", "SAVE_EVIDENCE_PAIR", relative, "archive_ref and evidence_through must both be none or both identify archived evidence")
            if commit == "bind" and (archive_ref != "none" or evidence != "none"):
                self.add("ERROR", "SAVE_BIND_EVIDENCE", relative, "bind has no archived play evidence")
            if commit == "close" and (archive_ref == "none" or evidence != values.get("save_id")):
                self.add("ERROR", "SAVE_CLOSE_EVIDENCE", relative, "full save requires its archive_ref and evidence_through equal to save_id")
            if evidence != "none" and (not SAFE_ID.fullmatch(evidence) or is_sentinel(evidence) or is_placeholder(evidence)):
                self.add("ERROR", "SAVE_EVIDENCE_ID", relative, "evidence_through requires a portable archived save id")
            if archive_ref != "none":
                self.archive_path(archive_ref, relative, None, "SAVE_ARCHIVE_PATH")
            if commit == "checkpoint" and evidence == values.get("save_id"):
                self.add("ERROR", "SAVE_CHECKPOINT_EVIDENCE", relative, "checkpoint cannot claim new archived evidence under its own save_id")
            pc = self.safe_path(values.get("pc_record", ""), self.root, self.root, "SAVE_PC_PATH", relative)
            if pc is not None:
                if self.relative(pc) != "INSTANCE/CHAR/PC.md":
                    self.add("ERROR", "SAVE_PC_OVERLAY", relative, "pc_record must be INSTANCE/CHAR/PC.md")
                if not pc.is_file():
                    self.add("ERROR", "SAVE_PC_MISSING", relative, "bound PC overlay does not exist")
                else:
                    pc_text = self.read_text(pc, "SAVE_PC_READ")
                    if pc_text is not None and not self.meaningful_authoritative_payload(pc_text):
                        self.add("ERROR", "SAVE_PC_EMPTY", relative, "bound PC overlay requires a non-placeholder body")
            self.check_current_routes(text)
        candidate = self.root / "INSTANCE/CURRENT_SAVE.candidate.md"
        if candidate.exists() or candidate.is_symlink():
            self.add("ERROR", "SAVE_STALE_CANDIDATE", self.relative(candidate), "unfinished candidate exists; validator will not delete it")

    def check_contract_clauses(self, text: str, relative: str) -> None:
        """Check named prose clauses, never their accepted semantic meaning."""
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        headings = {line: (level, title) for line, level, title in iter_literal_headings(text)}
        pattern = re.compile(r"^\s*(?:[-*+]\s+)?(" + "|".join(re.escape(label) for label in CONTRACT_CLAUSES) + r"):\s*(.*?)\s*$")
        current_section: Optional[str] = None
        occurrences: dict[str, list[int]] = defaultdict(list)
        for number, line in enumerate(structural, 1):
            if number in headings:
                level, title = headings[number]
                if level <= 2:
                    current_section = title if level == 2 else None
            if not visible[number - 1]:
                continue
            match = pattern.fullmatch(line)
            if match is None:
                continue
            label, value = match.groups()
            occurrences[label].append(number)
            expected_section = CONTRACT_CLAUSES[label]
            if current_section != expected_section:
                self.add("ERROR", "CONTRACT_CLAUSE_SECTION", relative,
                         f"{label!r} belongs in {expected_section!r}, not {current_section or 'outside a section'!r}", number)
            if is_placeholder(value) or is_sentinel(value) or not self.meaningful_payload(value):
                self.add("ERROR", "CONTRACT_CLAUSE_EMPTY", relative,
                         f"{label!r} requires substantive accepted wording, not a blank or placeholder", number)
        for label, expected_section in CONTRACT_CLAUSES.items():
            found = occurrences[label]
            if not found:
                self.add("ERROR", "CONTRACT_CLAUSE_MISSING", relative,
                         f"missing {label!r} clause in {expected_section!r}; an existing agreement needs accepted supplementation through RECALIBRATE")
            elif len(found) > 1:
                self.add("ERROR", "CONTRACT_CLAUSE_DUPLICATE", relative,
                         f"{label!r} must occur exactly once; found {len(found)}", found[1])

    def check_campaign_contract(self) -> None:
        relative = "INSTANCE/CAMPAIGN_CONTRACT.md"
        text = self.read_text(self.root / relative, "CONTRACT_READ")
        if text is None:
            return
        frontmatter, errors = extract_frontmatter(text)
        for error in errors:
            self.add("ERROR", "CONTRACT_FRONTMATTER", relative, error)
        for field, expected in {"id": "instance.campaign_contract", "class": "campaign-contract", "temperature": "resident"}.items():
            if frontmatter.get(field) != expected:
                self.add("ERROR", "CONTRACT_FRONTMATTER_VALUE", relative, f"front-matter {field} must be {expected!r}")
        values = self.exact_field_record(text, relative, CONTRACT_FIELDS, "CONTRACT")
        if values is None:
            return
        self.contract = values
        if any(field in values for field in ("campaign_promise", "creative_mandate", "structural_direction")) and not any(
            level == 2 and title == "Campaign promise" for _line, level, title in iter_literal_headings(text)
        ):
            self.add("ERROR", "CONTRACT_REQUIRES_UPGRADE", relative,
                     "legacy axis-based agreement requires explicit ADMIN/UPGRADE_V07.md mapping and acceptance")
        sections = self.check_sections(text, relative, CONTRACT_SECTIONS, "CONTRACT", not self.bound)
        revision = self.canonical_revision(values.get("contract_rev", ""))
        if revision is None:
            self.add("ERROR", "CONTRACT_REVISION", relative, "contract_rev must be a canonical nonnegative ASCII integer")
            revision = -1
        candidate = self.root / "INSTANCE/CAMPAIGN_CONTRACT.candidate.md"
        if candidate.exists() or candidate.is_symlink():
            self.add("ERROR", "CONTRACT_STALE_CANDIDATE", self.relative(candidate), "unfinished contract candidate exists")
        if not self.bound:
            for field, expected in dict(campaign_id="none", contract_id="none", contract_rev="0", contract_parent="none", status="unbound", module="unbound").items():
                if values.get(field) != expected:
                    self.add("ERROR", "CONTRACT_UNBOUND_VALUE", relative, f"unbound contract requires {field}: {expected}")
            return
        if values.get("status") != "accepted":
            self.add("ERROR", "CONTRACT_BOUND_STATUS", relative, "bound run requires status accepted")
        self.check_contract_clauses(text, relative)
        for field in ("campaign_id", "module"):
            if values.get(field) != self.current.get(field):
                self.add("ERROR", "CONTRACT_BINDING_MISMATCH", relative, f"contract {field} does not match CURRENT_SAVE")
        identity, parent = values.get("contract_id", ""), values.get("contract_parent", "")
        if not SAFE_ID.fullmatch(identity) or is_sentinel(identity) or is_placeholder(identity):
            self.add("ERROR", "CONTRACT_ID_FORMAT", relative, "contract_id requires a portable non-placeholder id")
        if revision < 1:
            self.add("ERROR", "CONTRACT_BOUND_REVISION", relative, "accepted contract requires revision >= 1")
        if revision == 1 and parent != "none":
            self.add("ERROR", "CONTRACT_INITIAL_PARENT", relative, "first agreement requires contract_parent none")
        if revision > 1 and (not SAFE_ID.fullmatch(parent) or is_sentinel(parent) or is_placeholder(parent) or parent == identity):
            self.add("ERROR", "CONTRACT_PARENT_FORMAT", relative, "recalibration requires a distinct prior contract id")
        for section, body in sections.items():
            if body == "none":
                self.add("ERROR", "CONTRACT_REQUIRED_CONTENT", relative, f"accepted section {section!r} requires actual agreed terms")
        self.metrics["contract_rev"] = revision

    def check_bearing(self) -> None:
        # Cold optional notes cannot veto an otherwise valid campaign.
        relative = "INSTANCE/BEARING.md"
        path = self.root / relative
        if not path.exists() and not path.is_symlink():
            self.metrics["bearing_status"] = "absent (optional)"
            return
        start = len(self.findings)
        text = self.read_text(path, "BEARING_READ")
        if text is not None:
            values = self.exact_field_record(text, relative, ("campaign_id", "base_save_id", "base_contract_id", "status"), "BEARING") or {}
            status = values.get("status", "")
            if status not in {"none", "provisional"}:
                self.add("WARNING", "BEARING_STATUS", relative, "optional review notes should be none or provisional; never canon")
            if status == "provisional":
                bases = {"campaign_id": self.current.get("campaign_id"), "base_save_id": self.current.get("save_id"), "base_contract_id": self.contract.get("contract_id")}
                if any(values.get(key) != value for key, value in bases.items()):
                    self.add("WARNING", "BEARING_STALE_BASE", relative, "review notes do not match current save/agreement; they are cold historical notes, not current authority")
            self.metrics["bearing_status"] = status or "unrecognized (optional)"
        for index in range(start, len(self.findings)):
            finding = self.findings[index]
            self.findings[index] = Finding("WARNING", finding.code, finding.path, finding.line, finding.message)

    def check_preparation(self) -> None:
        """Optional derivative notes cannot certify facts or veto sound continuity."""
        relative = "INSTANCE/PREP.md"
        path = self.root / relative
        candidate = self.root / "INSTANCE/PREP.candidate.md"
        if candidate.exists() or candidate.is_symlink():
            self.add("ERROR", "PREP_STALE_CANDIDATE", self.relative(candidate),
                     "unfinished preparation candidate exists; resolve its recorded operation")
        if not path.exists() and not path.is_symlink():
            self.metrics["preparation_status"] = "absent (optional)"
            return
        start = len(self.findings)
        text = self.read_text(path, "PREP_READ")
        if text is not None:
            frontmatter, errors = extract_frontmatter(text)
            for error in errors:
                self.add("WARNING", "PREP_FRONTMATTER", relative, error)
            for field, expected in {"id": "instance.preparation", "class": "campaign-preparation", "temperature": "cold"}.items():
                if frontmatter.get(field) != expected:
                    self.add("WARNING", "PREP_FRONTMATTER_VALUE", relative, f"preparation front-matter {field} should be {expected!r}")
            first_section = next((line for line, level, _title in iter_literal_headings(text) if level == 2), None)
            metadata = "\n".join(text.splitlines()[:first_section - 1]) if first_section else text
            rows = self.find_table(metadata, ["Preparation basis", "Value"], relative, "PREP_TABLE")
            if first_section:
                visible, structural = structural_markdown_lines(text.splitlines())
                for number in range(first_section - 1, len(structural)):
                    cells = split_table_like_row(structural[number]) if visible[number] else None
                    if cells and [strip_code_ticks(cell).casefold() for cell in cells] == ["preparation basis", "value"]:
                        self.add("WARNING", "PREP_TABLE_SCOPE", relative,
                                 "preparation basis belongs in one header table before the body sections", number + 1)
            values: dict[str, str] = {}
            for row in rows or []:
                field = strip_code_ticks(row["preparation basis"]).strip()
                value = strip_code_ticks(row["value"]).strip()
                if field in values:
                    self.add("WARNING", "PREP_DUPLICATE_FIELD", relative, f"duplicate preparation basis {field!r}", row["_line"])
                    continue
                if field not in PREPARATION_FIELDS:
                    self.add("WARNING", "PREP_UNKNOWN_FIELD", relative, f"unrecognized preparation basis {field!r}", row["_line"])
                if not SAFE_ID.fullmatch(value) or is_sentinel(value) or is_placeholder(value):
                    self.add("WARNING", "PREP_BASIS_ID", relative, f"preparation basis {field!r} needs an actual portable id", row["_line"])
                values[field] = value
            for field in PREPARATION_FIELDS:
                if field not in values:
                    self.add("WARNING", "PREP_MISSING_FIELD", relative, f"missing preparation basis {field!r}")
            if values.get("campaign_id") != self.current.get("campaign_id"):
                self.add("WARNING", "PREP_FOREIGN_CAMPAIGN", relative,
                         "preparation does not identify this campaign; ignore it and recover useful work from actual authority")
            elif values.get("base_save_id") != self.current.get("save_id") or values.get("base_contract_id") != self.contract.get("contract_id"):
                self.add("WARNING", "PREP_STALE_BASE", relative,
                         "preparation basis differs from current save/agreement; recheck relevant sources, never refresh provenance merely because of saving")
            self.metrics["preparation_status"] = "derivative (basis checked only)"
        # Malformed/unreadable derivative content is nonfatal; path safety is not.
        for index in range(start, len(self.findings)):
            finding = self.findings[index]
            if finding.code.startswith("PREP_"):
                self.findings[index] = Finding("WARNING", finding.code, finding.path, finding.line, finding.message)
        if text is not None:
            for line, raw in backticked_markdown_paths(text):
                file_part, _separator, _heading = raw.partition("#")
                target = self.safe_path(file_part, self.root, self.root, "PREP_SOURCE_PATH", relative, line)
                if target is not None and not target.is_file():
                    self.add("WARNING", "PREP_SOURCE_MISSING", relative,
                             f"derivative source route is missing: {raw!r}; recover from actual authority", line)

    def check_recovery(self) -> None:
        marker = self.root / "RECOVERY/ACTIVE.md"
        if marker.exists() or marker.is_symlink():
            self.add("ERROR", "RECOVERY_PENDING", "RECOVERY/ACTIVE.md",
                     "active recovery marker exists; inspect ADMIN/RECOVERY.md and finish or restore before PLAY; validator makes no repairs")

    def check_handover(self) -> None:
        relative = "HANDOVER/ACTIVE.md"
        marker = self.root / relative
        # Check ancestors before the marker; never follow a linked package tree.
        for probe in (marker.parent, marker):
            if probe.is_symlink():
                self.add("ERROR", "PATH_SYMLINK", relative, "authoritative path crosses a symlink")
                return
        if not marker.exists():
            return
        if self.bound:
            self.add("WARNING", "HANDOVER_PAUSED", relative,
                     "active handover marker exists; source PLAY is paused; the standalone TOOLS/handover.py checker and ADMIN/SCENE_HANDOVER.md reconciliation are required; this validator does not inspect the package")
        else:
            self.add("ERROR", "HANDOVER_UNBOUND", relative,
                     "an unbound kit cannot have an active scene handover; preserve transfer records and use a clean separate kit")

    def check_engines(self) -> None:
        engine_root = self.root / "ENGINE"
        candidates: list[tuple[Path, str]] = []
        if engine_root.is_dir():
            for path in sorted(engine_root.glob("*.md")):
                if path.name.startswith("_") or path.name.casefold() == "readme.md":
                    continue
                candidates.append((path, path.stem))
            for path in sorted(engine_root.glob("*/ENGINE.md")):
                candidates.append((path, path.parent.name))
        for path, expected_id in candidates:
            text = self.read_text(path, "ENGINE_READ")
            if text is None:
                continue
            frontmatter, errors = extract_frontmatter(text)
            for error in errors:
                self.add("ERROR", "ENGINE_FRONTMATTER", self.relative(path), error)
            engine_class = frontmatter.get("class", "").strip()
            engine_id = frontmatter.get("id", "").strip()
            if not engine_id:
                declared_engine = engine_class == "engine" or path.name == "ENGINE.md"
                severity = "ERROR" if path.name == "freeform.md" or declared_engine else "WARNING"
                code = "ENGINE_ID_MISSING" if severity == "ERROR" else "ENGINE_NONENGINE_FILE"
                self.add(severity, code, self.relative(path), "no scalar front-matter id; excluded from engine enumeration")
                continue
            if engine_class != "engine":
                self.add("ERROR", "ENGINE_CLASS_INVALID", self.relative(path), "engine requires exact scalar front-matter class: engine")
            if not SAFE_ID.fullmatch(expected_id):
                self.add("ERROR", "ENGINE_PATH_ID_UNSAFE", self.relative(path), f"engine filename/directory id is not a portable safe token: {expected_id!r}")
            if not SAFE_ID.fullmatch(engine_id):
                self.add("ERROR", "ENGINE_ID_UNSAFE", self.relative(path), f"front-matter id is not a portable safe token: {engine_id!r}")
            character_build_support = frontmatter.get("character_build_support", "").strip()
            if not character_build_support:
                self.add(
                    "ERROR",
                    "ENGINE_CHARACTER_BUILD_SUPPORT_MISSING",
                    self.relative(path),
                    "engine requires scalar front-matter character_build_support",
                )
            elif character_build_support not in CHARACTER_BUILD_SUPPORT:
                self.add(
                    "ERROR",
                    "ENGINE_CHARACTER_BUILD_SUPPORT_INVALID",
                    self.relative(path),
                    f"character_build_support must be one of {', '.join(sorted(CHARACTER_BUILD_SUPPORT))}; found {character_build_support!r}",
                )
            if engine_id != expected_id:
                self.add("ERROR", "ENGINE_ID_MISMATCH", self.relative(path), f"front-matter id {engine_id!r} does not match {expected_id!r}")
            self.engine_ids[engine_id].append(path)
        for engine_id, paths in self.engine_ids.items():
            if len(paths) > 1:
                self.add("ERROR", "ENGINE_DUPLICATE_ID", self.relative(paths[0]), f"engine id {engine_id!r} resolves to: " + ", ".join(self.relative(path) for path in paths))
        folded: dict[str, list[str]] = defaultdict(list)
        for engine_id in self.engine_ids:
            folded[engine_id.casefold()].append(engine_id)
        for ids in folded.values():
            if len(ids) > 1:
                self.add("ERROR", "ENGINE_CASE_COLLISION", "ENGINE", "case-insensitive engine id collision: " + ", ".join(sorted(ids)))
        if self.bound:
            bound_id = self.current.get("engine", "")
            if len(self.engine_ids.get(bound_id, [])) != 1:
                self.add("ERROR", "ENGINE_BOUND_RESOLUTION", "INSTANCE/CURRENT_SAVE.md", f"bound engine {bound_id!r} does not resolve exactly once")
        self.metrics["installed_engine_ids"] = sorted(self.engine_ids)

    def check_initial_instance(self) -> None:
        """Unbound kits and revision-one binds retain empty live registers."""
        if self.bound and self.current.get("commit_kind") != "bind":
            return
        for relative, expected in EMPTY_INSTANCE_TEMPLATES.items():
            text = self.read_text(self.root / relative, "INSTANCE_INITIAL_READ")
            if text is not None and empty_template_signature(text) != empty_template_signature(expected):
                self.add("ERROR", "INSTANCE_INITIAL_REGISTER", relative,
                         "unbound/bind state requires its distributed empty live register; preserve prior evidence and use a clean run")
        allowed = {"_SCHEMA.md", "CURRENT_SAVE.md", "CAMPAIGN_CONTRACT.md", "BEARING.md", "SAFETY.md",
                   "KNOWN.md", "NOW.md", "CAST_STATUS.md", "CORRECTIONS.md", "CHAR", "CHAR/README.md", "PEOPLE", "PEOPLE/README.md"}
        instance_root = self.root / "INSTANCE"
        for entry in sorted(instance_root.rglob("*")):
            relative = entry.relative_to(instance_root).as_posix()
            if self.bound and (relative == "CHAR" or relative.startswith("CHAR/")):
                continue  # Accepted character closure is checked independently.
            if relative not in allowed:
                self.add("ERROR", "INSTANCE_INITIAL_CONTENT", self.relative(entry),
                         "unbound/bind tree contains an unexpected campaign record; use a clean copy without deleting evidence")

    def meaningful_payload(self, text: str) -> bool:
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        table_scaffolding: set[int] = set()
        for index in range(len(lines) - 1):
            header = split_markdown_row(structural[index]) if visible[index] else None
            separator = split_markdown_row(structural[index + 1]) if visible[index + 1] else None
            if header is not None and separator is not None and len(header) == len(separator) and all(is_separator_cell(cell) for cell in separator):
                table_scaffolding.update({index, index + 1})
        for index, line in enumerate(structural):
            stripped = line.strip()
            if not visible[index] or index in table_scaffolding or not stripped or stripped.startswith("#") or stripped.startswith("<!--"):
                continue
            normalized = strip_code_ticks(re.sub(r"^[-*+]\s*", "", stripped)).casefold()
            if not is_placeholder(normalized) and not is_separator_cell(normalized):
                return True
        return False

    def meaningful_fenced_payload(self, text: str) -> bool:
        """Recognize substantive structured data inside a valid Markdown fence."""

        fence_char: Optional[str] = None
        fence_length = 0
        for line in text.splitlines():
            if fence_char is None:
                opener = re.match(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$", line)
                if not opener:
                    continue
                run, info = opener.group(1), opener.group(2)
                if run[0] == "`" and "`" in info:
                    continue
                fence_char, fence_length = run[0], len(run)
                continue
            closer = re.match(r"^[ ]{0,3}(`{3,}|~{3,})[ \t]*$", line)
            if closer:
                run = closer.group(1)
                if run[0] == fence_char and len(run) >= fence_length:
                    fence_char, fence_length = None, 0
                    continue
            candidate = line.strip()
            if candidate and not is_placeholder(candidate):
                return True
        return False

    def meaningful_authoritative_payload(self, text: str) -> bool:
        return self.meaningful_payload(text) or self.meaningful_fenced_payload(text)

    def check_module_index(
        self,
        index_path: Path,
        module_dir: Path,
        visited: set[Path],
    ) -> bool:
        """Validate explicit routes and return whether at least one body is reached."""

        resolved_index = index_path.resolve(strict=False)
        if resolved_index in visited:
            self.add("ERROR", "MODULE_INDEX_CYCLE", self.relative(index_path), "routing-index cycle detected")
            return False
        visited.add(resolved_index)
        text = self.read_text(index_path, "MODULE_INDEX_READ")
        if text is None:
            return False
        routes = backticked_markdown_paths(text)
        if not routes:
            self.add("ERROR", "MODULE_INDEX_EMPTY", self.relative(index_path), "routing index has no explicit backticked .md target")
            return False
        body_found = False
        for source_line, raw_route in routes:
            file_part, separator, fragment = raw_route.partition("#")
            target = self.safe_path(
                file_part,
                index_path.parent,
                module_dir,
                "MODULE_INDEX_TARGET_PATH",
                self.relative(index_path),
                source_line,
                allow_parent_segments=True,
            )
            if target is None:
                continue
            if target.resolve(strict=False) == resolved_index:
                self.add("ERROR", "MODULE_INDEX_SELF_ROUTE", self.relative(index_path), "routing index points to itself", source_line)
                continue
            if not target.is_file():
                self.add("ERROR", "MODULE_INDEX_TARGET_MISSING", self.relative(target), "routing-index target does not exist")
                continue
            target_text = self.read_text(target, "MODULE_BODY_READ")
            if target_text is None:
                continue
            if separator:
                fragment = strip_code_ticks(fragment).strip()
                if not fragment:
                    self.add(
                        "ERROR",
                        "MODULE_INDEX_FRAGMENT_EMPTY",
                        self.relative(index_path),
                        f"route has an empty literal heading fragment: {raw_route!r}",
                        source_line,
                    )
                    continue
                count = len(heading_map(target_text).get(fragment, []))
                if count != 1:
                    self.add(
                        "ERROR",
                        "MODULE_INDEX_FRAGMENT",
                        self.relative(target),
                        f"literal heading {fragment!r} occurs {count} times",
                        source_line,
                    )
            frontmatter, _errors = extract_frontmatter(target_text)
            looks_like_index = target.name.casefold() == "index.md" or declares_routing_index(frontmatter)
            if looks_like_index:
                body_found = self.check_module_index(target, module_dir, visited) or body_found
            elif self.meaningful_authoritative_payload(target_text):
                body_found = True
            else:
                self.add("ERROR", "MODULE_BODY_EMPTY", self.relative(target), "authoritative target has no non-placeholder body")
        visited.remove(resolved_index)
        if not body_found:
            self.add("ERROR", "MODULE_INDEX_NO_BODY", self.relative(index_path), "routing index reaches no non-placeholder authoritative body")
        return body_found

    def scan_pc_tree(self, char_dir: Path, origin: str) -> tuple[dict[str, Path], set[str]]:
        """Return regular Markdown files and directories in one character tree."""

        files: dict[str, Path] = {}
        directories: set[str] = set()
        code_prefix = "MODULE_PC_TREE" if origin == "module" else "INSTANCE_PC_TREE"
        if char_dir.is_symlink():
            self.add("ERROR", code_prefix + "_SYMLINK", self.relative(char_dir), "character-tree root must not be a symlink")
            return files, directories
        if not char_dir.is_dir():
            self.add("ERROR", code_prefix + "_MISSING", self.relative(char_dir), "character-tree directory is missing")
            return files, directories

        walk_errors: list[OSError] = []

        def collect_walk_error(error: OSError) -> None:
            walk_errors.append(error)

        try:
            for directory, dirnames, filenames in os.walk(char_dir, topdown=True, onerror=collect_walk_error, followlinks=False):
                dirnames.sort()
                filenames.sort()
                base = Path(directory)
                retained: list[str] = []
                for name in dirnames:
                    path = base / name
                    relative = path.relative_to(char_dir).as_posix()
                    if path.is_symlink():
                        self.add("ERROR", code_prefix + "_SYMLINK", self.relative(path), "character bundle must not contain symlink directories")
                        continue
                    if not path.is_dir():
                        self.add("ERROR", code_prefix + "_SPECIAL", self.relative(path), "character bundle contains a non-directory tree entry")
                        continue
                    directories.add(relative)
                    retained.append(name)
                dirnames[:] = retained
                for name in filenames:
                    path = base / name
                    relative = path.relative_to(char_dir).as_posix()
                    if path.is_symlink():
                        self.add("ERROR", code_prefix + "_SYMLINK", self.relative(path), "character bundle must not contain symlink files")
                        continue
                    if not path.is_file():
                        self.add("ERROR", code_prefix + "_SPECIAL", self.relative(path), "character bundle contains a non-regular file")
                        continue
                    if path.suffix != ".md":
                        self.add("ERROR", code_prefix + "_NONMARKDOWN", self.relative(path), "character bundle files must use the exact .md suffix")
                        continue
                    files[relative] = path
        except (OSError, ValueError) as exc:
            self.add("INCOMPLETE", code_prefix + "_SCAN", self.relative(char_dir), f"could not scan character tree: {exc}")
        for error in walk_errors:
            self.add("INCOMPLETE", code_prefix + "_SCAN", self.relative(char_dir), f"could not scan character tree: {error}")
        return files, directories

    def check_pc_index(
        self,
        index_path: Path,
        char_dir: Path,
        visited: set[Path],
        reachable: set[str],
    ) -> bool:
        """Validate a PC routing graph constrained to its owning CHAR tree."""

        resolved_index = index_path.resolve(strict=False)
        if resolved_index in visited:
            self.add("ERROR", "PC_INDEX_CYCLE", self.relative(index_path), "PC routing-index cycle detected")
            return False
        visited.add(resolved_index)
        body_found = False
        try:
            text = self.read_text(index_path, "PC_INDEX_READ")
            if text is None:
                return False
            routes = backticked_markdown_paths(text)
            if not routes:
                self.add("ERROR", "PC_INDEX_EMPTY", self.relative(index_path), "PC routing index has no explicit backticked .md target")
                return False
            for source_line, raw_route in routes:
                file_part, separator, fragment = raw_route.partition("#")
                target = self.safe_path(
                    file_part,
                    index_path.parent,
                    char_dir,
                    "PC_INDEX_TARGET_PATH",
                    self.relative(index_path),
                    source_line,
                    allow_parent_segments=True,
                )
                if target is None:
                    continue
                try:
                    target_relative = target.resolve(strict=False).relative_to(char_dir.resolve(strict=False)).as_posix()
                except (OSError, ValueError):
                    # safe_path already reports an escaped boundary.  Retain a
                    # defensive guard in case filesystem resolution changes.
                    continue
                if target_relative == "README.md":
                    self.add("ERROR", "PC_INDEX_RESERVED_TARGET", self.relative(index_path), "CHAR/README.md is reserved documentation and cannot be a routed PC shard", source_line)
                    continue
                if target.resolve(strict=False) == resolved_index:
                    self.add("ERROR", "PC_INDEX_SELF_ROUTE", self.relative(index_path), "PC routing index points to itself", source_line)
                    continue
                if not target.is_file():
                    self.add("ERROR", "PC_INDEX_TARGET_MISSING", self.relative(target), "PC routing-index target does not exist")
                    continue
                reachable.add(target_relative)
                target_text = self.read_text(target, "PC_INDEX_BODY_READ")
                if target_text is None:
                    continue
                if separator:
                    fragment = strip_code_ticks(fragment).strip()
                    if not fragment:
                        self.add(
                            "ERROR",
                            "PC_INDEX_FRAGMENT_EMPTY",
                            self.relative(index_path),
                            f"route has an empty literal heading fragment: {raw_route!r}",
                            source_line,
                        )
                        continue
                    count = len(heading_map(target_text).get(fragment, []))
                    if count != 1:
                        self.add(
                            "ERROR",
                            "PC_INDEX_FRAGMENT",
                            self.relative(target),
                            f"literal heading {fragment!r} occurs {count} times",
                            source_line,
                        )
                        continue
                frontmatter, errors = extract_frontmatter(target_text)
                for error in errors:
                    self.add("ERROR", "PC_INDEX_FRONTMATTER", self.relative(target), error)
                looks_like_index = target.name.casefold() == "index.md" or declares_routing_index(frontmatter)
                if looks_like_index:
                    body_found = self.check_pc_index(target, char_dir, visited, reachable) or body_found
                elif self.meaningful_authoritative_payload(target_text):
                    body_found = True
                else:
                    self.add("ERROR", "PC_INDEX_BODY_EMPTY", self.relative(target), "PC authoritative target has no non-placeholder body")
        finally:
            visited.discard(resolved_index)
        if not body_found:
            self.add("ERROR", "PC_INDEX_NO_BODY", self.relative(index_path), "PC routing index reaches no non-placeholder authoritative body")
        return body_found

    @staticmethod
    def pc_parent_directories(files: Iterable[str]) -> set[str]:
        """Return the relative directory set needed to contain PC bundle files."""

        result: set[str] = set()
        for relative in files:
            parent = PurePosixPath(relative).parent
            while parent != PurePosixPath("."):
                result.add(parent.as_posix())
                parent = parent.parent
        return result

    def validate_pc_graph(
        self,
        char_dir: Path,
        origin: str,
        pc_text: Optional[str],
    ) -> dict[str, Path]:
        """Validate one closed PC graph and return its reachable file closure."""

        pc_path = char_dir / "PC.md"
        files, directories = self.scan_pc_tree(char_dir, origin)
        reachable = {"PC.md"}
        if origin == "module" and "README.md" in files:
            self.add(
                "ERROR",
                "MODULE_PC_RESERVED_README",
                self.relative(files["README.md"]),
                "MODULE/CHAR/README.md is reserved for the INSTANCE distribution guide and cannot be a PC shard",
            )
        if pc_text is not None:
            frontmatter, errors = extract_frontmatter(pc_text)
            for error in errors:
                self.add("ERROR", "PC_INDEX_FRONTMATTER", self.relative(pc_path), error)
            pc_class = frontmatter.get("class", "").strip()
            if pc_class == PC_ROUTING_CLASS:
                self.check_pc_index(pc_path, char_dir, set(), reachable)
            elif declares_routing_index(frontmatter):
                self.add(
                    "ERROR",
                    "PC_ENTRYPOINT_CLASS",
                    self.relative(pc_path),
                    f"a routed CHAR/PC.md requires exact scalar class: {PC_ROUTING_CLASS}",
                )

        code_prefix = "MODULE_PC" if origin == "module" else "INSTANCE_PC"
        for relative in sorted(set(files) - reachable - {"README.md"}):
            self.add(
                "ERROR",
                code_prefix + "_ORPHAN_SHARD",
                self.relative(files[relative]),
                "character shard is not reachable from CHAR/PC.md's explicit routing graph",
            )
        closure = {relative: files[relative] for relative in sorted(reachable) if relative in files and relative != "README.md"}
        closure_directories = self.pc_parent_directories(closure)
        for relative in sorted(directories - closure_directories):
            self.add(
                "ERROR",
                code_prefix + "_ORPHAN_DIRECTORY",
                self.relative(char_dir / relative),
                "character bundle directory contains no reachable shard",
            )
        return closure

    def check_pc_bundle(self, module_dir: Path, module_pc_text: Optional[str]) -> None:
        """Validate MODULE/INSTANCE PC graphs and their revision-one identity."""

        module_char_dir = module_dir / "CHAR"
        module_files = self.validate_pc_graph(module_char_dir, "module", module_pc_text)
        instance_char_dir = self.root / "INSTANCE/CHAR"
        instance_pc_path = instance_char_dir / "PC.md"
        instance_pc_text = self.read_text(instance_pc_path, "INSTANCE_PC_READ") if instance_pc_path.is_file() else None
        instance_files = self.validate_pc_graph(instance_char_dir, "instance", instance_pc_text)

        self.metrics["module_pc_bundle_files"] = sorted(module_files)
        self.metrics["instance_pc_bundle_files"] = sorted(instance_files)
        if self.current.get("commit_kind") != "bind":
            return

        for relative in sorted(set(module_files) - set(instance_files)):
            self.add(
                "ERROR",
                "PC_BIND_COPY_MISSING",
                self.relative(instance_char_dir / relative),
                "revision-one INSTANCE character bundle is missing an accepted MODULE shard",
            )
        for relative in sorted(set(instance_files) - set(module_files)):
            self.add(
                "ERROR",
                "PC_BIND_COPY_EXTRA",
                self.relative(instance_files[relative]),
                "revision-one INSTANCE character bundle contains a file outside the accepted reachable MODULE bundle",
            )
        for relative in sorted(set(module_files) & set(instance_files)):
            try:
                if module_files[relative].read_bytes() != instance_files[relative].read_bytes():
                    self.add(
                        "ERROR",
                        "PC_BIND_COPY_MISMATCH",
                        self.relative(instance_files[relative]),
                        "revision-one INSTANCE character shard is not the exact accepted MODULE copy",
                    )
            except OSError as exc:
                self.add("INCOMPLETE", "PC_BIND_COPY_READ", self.relative(instance_files[relative]), f"could not compare bind PC copy: {exc}")

    def check_module(self) -> None:
        modules_root = self.root / "MODULES"
        if modules_root.is_dir():
            for candidate in sorted(modules_root.glob("*/SETTING_BRIEF.candidate.md")):
                if candidate.exists() or candidate.is_symlink():
                    self.add(
                        "ERROR",
                        "SETTING_BRIEF_STALE_CANDIDATE",
                        self.relative(candidate),
                        "unfinished setting-brief candidate exists; validator will not delete it",
                    )
        if not self.bound:
            self.metrics["bound_module"] = "skipped (unbound)"
            return
        module_id = self.current.get("module", "")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", module_id):
            self.add("ERROR", "MODULE_ID_UNSAFE", "INSTANCE/CURRENT_SAVE.md", f"unsafe module id {module_id!r}")
            return
        module_dir = self.root / "MODULES" / module_id
        required = ("MODULE.md", "SETTING_BRIEF.md", "CHAR/PC.md", "T0_SAVE.md")
        for relative in required:
            required_path = module_dir / relative
            if not required_path.is_file():
                self.add("ERROR", "MODULE_REQUIRED_FILE", self.relative(required_path), "bound module file is missing")
                continue
            required_text = self.read_text(required_path, "MODULE_REQUIRED_READ")
            if required_text is not None and not required_text.strip():
                self.add("ERROR", "MODULE_REQUIRED_EMPTY", self.relative(required_path), "bound module file is empty")
            if relative == "CHAR/PC.md" and required_text is not None and not self.meaningful_authoritative_payload(required_text):
                self.add("ERROR", "MODULE_PC_EMPTY", self.relative(required_path), "PC baseline has no non-placeholder body")
        pc_path = module_dir / "CHAR/PC.md"
        pc_text = self.read_text(pc_path, "MODULE_PC_READ") if pc_path.is_file() else None
        self.check_pc_bundle(module_dir, pc_text)
        setting_brief_path = module_dir / "SETTING_BRIEF.md"
        setting_brief_text = self.read_text(setting_brief_path, "SETTING_BRIEF_READ") if setting_brief_path.is_file() else None
        if setting_brief_text is not None:
            setting_frontmatter, setting_errors = extract_frontmatter(setting_brief_text)
            for error in setting_errors:
                self.add("ERROR", "SETTING_BRIEF_FRONTMATTER", self.relative(setting_brief_path), error)
            unexpected_setting_fields = sorted(set(setting_frontmatter) - {"id", "class"})
            if unexpected_setting_fields:
                self.add(
                    "WARNING",
                    "SETTING_BRIEF_FRONTMATTER_FIELDS",
                    self.relative(setting_brief_path),
                    f"setting brief front matter contains unexpected fields: {', '.join(unexpected_setting_fields)}",
                )
            expected_setting_id = f"{module_id}.setting_brief"
            if setting_frontmatter.get("id") != expected_setting_id:
                self.add(
                    "ERROR",
                    "SETTING_BRIEF_IDENTITY",
                    self.relative(setting_brief_path),
                    f"setting brief id must be {expected_setting_id!r}",
                )
            if setting_frontmatter.get("class") != "setting-brief":
                self.add(
                    "ERROR",
                    "SETTING_BRIEF_CLASS",
                    self.relative(setting_brief_path),
                    "setting brief class must be 'setting-brief'",
                )

            section_lines: list[int] = []
            for section in SETTING_BRIEF_SECTIONS:
                body, start, count = section_text(setting_brief_text, section, 2)
                if count == 0:
                    self.add(
                        "ERROR",
                        "SETTING_BRIEF_SECTION_MISSING",
                        self.relative(setting_brief_path),
                        f"missing exact level-two section {section!r}",
                    )
                    continue
                if count > 1:
                    self.add(
                        "ERROR",
                        "SETTING_BRIEF_SECTION_DUPLICATE",
                        self.relative(setting_brief_path),
                        f"exact level-two section {section!r} occurs {count} times",
                    )
                    continue
                if start is not None:
                    section_lines.append(start)
                if body is None or not self.meaningful_payload(body):
                    self.add(
                        "ERROR",
                        "SETTING_BRIEF_SECTION_EMPTY",
                        self.relative(setting_brief_path),
                        f"section {section!r} has no substantive body",
                        start,
                    )
            if len(section_lines) == len(SETTING_BRIEF_SECTIONS) and section_lines != sorted(section_lines):
                self.add(
                    "ERROR",
                    "SETTING_BRIEF_SECTION_ORDER",
                    self.relative(setting_brief_path),
                    "setting brief sections must appear in contract order",
                )
            self.metrics["setting_brief"] = "checked"
        module_path = module_dir / "MODULE.md"
        module_text = self.read_text(module_path, "MODULE_READ") if module_path.is_file() else None
        if module_text is not None:
            frontmatter, errors = extract_frontmatter(module_text)
            for error in errors:
                self.add("ERROR", "MODULE_FRONTMATTER", self.relative(module_path), error)
            identity = {key: frontmatter.get(key, "") for key in ("id", "title", "engine")}
            descriptor_is_v04 = all(identity.values())
            if not identity.get("id") or not identity.get("engine"):
                identity_rows = self.find_table(
                    module_text,
                    ["Field", "Value"],
                    self.relative(module_path),
                    "MODULE_IDENTITY",
                    required=False,
                    strict_tail=False,
                )
                if identity_rows is not None:
                    identity.update({strip_code_ticks(row["field"]).casefold(): strip_code_ticks(row["value"]) for row in identity_rows})
            if not identity.get("id") or not identity.get("engine"):
                self.add("INCOMPLETE", "MODULE_IDENTITY_UNPARSEABLE", self.relative(module_path), "module id/engine are not in supported scalar front matter or Field/Value table")
            else:
                if identity["id"] != module_id:
                    self.add("ERROR", "MODULE_ID_MISMATCH", self.relative(module_path), f"module id {identity['id']!r} does not match directory/binding {module_id!r}")
                if identity["engine"] != self.current.get("engine"):
                    self.add("ERROR", "MODULE_ENGINE_MISMATCH", self.relative(module_path), f"module engine {identity['engine']!r} does not match current binding")
            if not descriptor_is_v04:
                self.add("INCOMPLETE", "MODULE_DESCRIPTOR_LEGACY", self.relative(module_path), "missing one or more required v0.4 scalar front-matter fields: id, title, engine")
            elif is_placeholder(identity["title"]):
                self.add("ERROR", "MODULE_TITLE_PLACEHOLDER", self.relative(module_path), "module title is empty or a placeholder")

            capability_body, capability_start, capability_count = section_text(module_text, "Capabilities", 2)
            if capability_count == 0:
                self.add("INCOMPLETE", "MODULE_CAPABILITIES_UNPARSEABLE", self.relative(module_path), "no exact level-two Capabilities section")
                capabilities = None
            elif capability_count > 1:
                self.add("ERROR", "MODULE_CAPABILITIES_DUPLICATE_SECTION", self.relative(module_path), "Capabilities section occurs more than once")
                capabilities = None
            elif capability_body is not None and [line.strip().casefold() for line in capability_body.splitlines() if line.strip()] == ["none"]:
                capabilities = []
            else:
                capabilities = self.find_table(
                    capability_body or "",
                    ["Capability", "Entrypoint"],
                    self.relative(module_path),
                    "MODULE_CAPABILITIES",
                    required=True,
                    line_offset=(capability_start or 1) - 1,
                )
                if capabilities == []:
                    self.add(
                        "ERROR",
                        "MODULE_CAPABILITIES_EMPTY_TABLE",
                        self.relative(module_path),
                        "an empty capability set must be written as the single word 'none'",
                        capability_start,
                    )
            if capabilities is not None:
                seen: set[str] = set()
                for row in capabilities:
                    capability_raw = strip_code_ticks(row["capability"]).strip()
                    capability = capability_raw.upper()
                    entry = strip_code_ticks(row["entrypoint"]).strip()
                    if capability in seen:
                        self.add("ERROR", "MODULE_CAPABILITY_DUPLICATE", self.relative(module_path), f"duplicate capability {capability!r}", row["_line"])
                        continue
                    seen.add(capability)
                    if capability_raw != capability:
                        self.add("ERROR", "MODULE_CAPABILITY_CASE", self.relative(module_path), f"capability name must use exact uppercase token {capability!r}", row["_line"])
                    if capability not in CAPABILITIES:
                        self.add("ERROR", "MODULE_CAPABILITY_UNKNOWN", self.relative(module_path), f"unknown capability {capability!r}", row["_line"])
                    entry_path = self.safe_path(entry, module_dir, module_dir, "MODULE_ENTRYPOINT_PATH", self.relative(module_path), row["_line"])
                    if entry_path is None:
                        continue
                    if not entry_path.is_file():
                        self.add("ERROR", "MODULE_ENTRYPOINT_MISSING", self.relative(entry_path), f"entrypoint for {capability} does not exist")
                        continue
                    entry_text = self.read_text(entry_path, "MODULE_ENTRYPOINT_READ")
                    if entry_text is not None and not self.meaningful_authoritative_payload(entry_text):
                        self.add("ERROR", "MODULE_ENTRYPOINT_EMPTY", self.relative(entry_path), f"entrypoint for {capability} has no non-placeholder body")
                    if entry_text is not None:
                        entry_frontmatter, _entry_errors = extract_frontmatter(entry_text)
                        looks_like_index = entry_path.name.casefold() == "index.md" or declares_routing_index(entry_frontmatter)
                        if looks_like_index:
                            self.check_module_index(entry_path, module_dir, set())

        policy_path = module_dir / "POLICY.md"
        policy_text = self.read_text(policy_path, "POLICY_READ") if policy_path.is_file() else None
        if policy_text is not None:
            exact_voice = [(line, title) for line, level, title in iter_literal_headings(policy_text) if level == 2 and title == "Voice"]
            legacy_voice = [(line, level, title) for line, level, title in iter_literal_headings(policy_text) if re.search(r"\bvoice\b", title, flags=re.IGNORECASE)]
            if len(exact_voice) > 1:
                self.add("ERROR", "MODULE_VOICE_DUPLICATE", self.relative(policy_path), "exact Voice heading occurs more than once")
            elif exact_voice:
                voice_body, _start, _count = section_text(policy_text, "Voice", 2)
                if voice_body is None or not self.meaningful_payload(voice_body):
                    self.add("ERROR", "MODULE_VOICE_EMPTY", self.relative(policy_path), "Voice section has no non-placeholder body", exact_voice[0][0])
            elif legacy_voice:
                meaningful = [item for item in legacy_voice if self.meaningful_payload(heading_body(policy_text, item[0], item[1]))]
                if meaningful:
                    self.add(
                        "INCOMPLETE",
                        "MODULE_VOICE_NONCANONICAL",
                        self.relative(policy_path),
                        "voice-like legacy section has content but requires manual confirmation; convert it to exact heading '## Voice'",
                        meaningful[0][0],
                    )
                else:
                    self.add("ERROR", "MODULE_VOICE_EMPTY", self.relative(policy_path), "voice-like legacy headings have no non-placeholder body", legacy_voice[0][0])
            else:
                self.add("ERROR", "MODULE_VOICE_MISSING", self.relative(policy_path), "no heading naming voice")

        t0_path = module_dir / "T0_SAVE.md"
        t0_text = self.read_text(t0_path, "T0_READ") if t0_path.is_file() else None
        if t0_text is not None:
            self.check_session_continuity(t0_text, self.relative(t0_path), initial=True)
        if t0_text is not None and section_text(t0_text, "Situation", 2)[2] == 0:
            legacy_rows = self.find_table(t0_text, ["Field", "Value"], self.relative(t0_path), "T0_TABLE", required=False)
            legacy_fields = {strip_code_ticks(row["field"]).strip() for row in (legacy_rows or [])}
            if "immediate_scene" in legacy_fields and "evidence_through" not in legacy_fields:
                # Accepted upgrades preserve source MODULE bytes. Validate the
                # supported old identity/opening table without demanding a
                # rewrite into the new snapshot representation.
                legacy_values: dict[str, str] = {}
                for row in legacy_rows or []:
                    field, value = strip_code_ticks(row["field"]).strip(), strip_code_ticks(row["value"]).strip()
                    if field in legacy_values:
                        self.add("ERROR", "T0_DUPLICATE_FIELD", self.relative(t0_path), f"duplicate legacy field {field!r}", row["_line"])
                    if not value:
                        self.add("ERROR", "T0_EMPTY_FIELD", self.relative(t0_path), f"blank legacy field {field!r}", row["_line"])
                    legacy_values[field] = value
                for field in ("engine", "module"):
                    if legacy_values.get(field) != self.current.get(field):
                        self.add("ERROR", "T0_BINDING_MISMATCH", self.relative(t0_path), f"legacy T0 {field} differs from current binding")
                if is_placeholder(legacy_values.get("immediate_scene", "")) or is_sentinel(legacy_values.get("immediate_scene", "")):
                    self.add("ERROR", "T0_REQUIRED_FIELD", self.relative(t0_path), "legacy opening requires meaningful immediate_scene")
                self.add("WARNING", "T0_LEGACY_MAPPING", self.relative(t0_path),
                         "legacy source T0 is preserved; identity/opening shape checked, accepted mapping into v0.7 sections is a manual semantic check")
                self.metrics["t0_format"] = "legacy table (mapping not semantically checked)"
                t0_text = None
        if t0_text is not None:
            t0_values = self.exact_field_record(t0_text, self.relative(t0_path), CURRENT_SAVE_FIELDS, "T0")
            t0_sections = self.check_sections(t0_text, self.relative(t0_path), SAVE_SECTIONS, "T0")
            if t0_values is not None:
                expected_template = {"pc_record": "INSTANCE/CHAR/PC.md", "campaign_id": "none", "save_id": "none",
                                     "save_rev": "0", "save_parent": "none", "commit_kind": "unbound",
                                     "archive_ref": "none", "evidence_through": "none"}
                for field, expected in expected_template.items():
                    if t0_values.get(field) != expected:
                        self.add("ERROR", "T0_TEMPLATE_VALUE", self.relative(t0_path), f"opening template requires {field}: {expected}")
                for field in ("engine", "module"):
                    if t0_values.get(field) != self.current.get(field):
                        self.add("ERROR", "T0_BINDING_MISMATCH", self.relative(t0_path), f"T0 {field} differs from current binding")
                if self.current.get("commit_kind") == "bind":
                    for field in ("datetime", "place"):
                        if t0_values.get(field) != self.current.get(field):
                            self.add("ERROR", "T0_BIND_MISMATCH", "INSTANCE/CURRENT_SAVE.md", f"bind {field} differs from accepted T0")
                    current_text = self.read_text(self.root / "INSTANCE/CURRENT_SAVE.md") or ""
                    for section, body in t0_sections.items():
                        current_body, _line, _count = section_text(current_text, section, 2)
                        # Source-to-overlay path substitution is part of LOAD.
                        expected = body.replace(f"MODULES/{module_id}/CHAR/", "INSTANCE/CHAR/")
                        if (current_body or "").strip() != expected:
                            self.add("ERROR", "T0_BIND_SECTION", "INSTANCE/CURRENT_SAVE.md", f"bind {section!r} differs from accepted T0")
        self.metrics["bound_module"] = module_id

    def safety_entries(self, text: str) -> list[str]:
        entries: list[str] = []
        active_section = False
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        for index, line in enumerate(structural):
            if not visible[index]:
                continue
            stripped = line.strip()
            label = re.match(r"^(Hard no|Hard-no|Fade / veil):\s*(.*)$", stripped)
            if label:
                active_section = True
                inline = re.sub(r"^[-*+]\s*", "", label.group(2).strip())
                if not is_placeholder(inline):
                    entries.append(inline)
                continue
            if not active_section or not stripped or stripped.startswith("<!--"):
                continue
            if stripped.startswith("#"):
                active_section = False
                continue
            bullet = re.match(r"^[-*+]\s+(.+)$", stripped)
            if not bullet:
                active_section = False
                continue
            candidate = bullet.group(1).strip()
            if not is_placeholder(candidate):
                entries.append(candidate)
        return entries

    def check_safety(self) -> None:
        path = self.root / "INSTANCE/SAFETY.md"
        text = self.read_text(path, "SAFETY_READ")
        if text is None:
            return
        safety_lines = text.splitlines()
        safety_visible, safety_structural = structural_markdown_lines(safety_lines)
        state_lines = [
            (number, match.group(1).strip())
            for number, line in enumerate(safety_structural, 1)
            if safety_visible[number - 1]
            and (match := re.match(r"^safety_state:\s*(\S.*?)\s*$", line))
        ]
        if len(state_lines) > 1:
            self.add("ERROR", "SAFETY_FLAG_COUNT", "INSTANCE/SAFETY.md", f"optional legacy safety_state line occurs {len(state_lines)} times")
            file_state = ""
        elif state_lines:
            file_state = state_lines[0][1]
            if file_state not in {"floor-only", "active"}:
                self.add("ERROR", "SAFETY_FLAG_VALUE", "INSTANCE/SAFETY.md", f"invalid safety_state {file_state!r}", state_lines[0][0])
        else:
            file_state = ""  # CURRENT_SAVE is the sole required flag owner.
        save_state = self.current.get("safety_state", "")
        if save_state and file_state and save_state != file_state:
            self.add("ERROR", "SAFETY_FLAG_MISMATCH", "INSTANCE/SAFETY.md", f"file is {file_state!r}; CURRENT_SAVE is {save_state!r}")
        entries = self.safety_entries(text)
        self.metrics["safety_entry_candidates"] = len(entries)
        if save_state == "active" and not entries:
            self.add("ERROR", "SAFETY_ACTIVE_EMPTY", "INSTANCE/SAFETY.md", "active safety has no non-placeholder Hard-no/Fade entry")
        if save_state == "floor-only" and entries:
            self.add("ERROR", "SAFETY_ENTRIES_INACTIVE", "INSTANCE/SAFETY.md", "safety entries exist but CURRENT_SAVE is floor-only")

    def archive_path(self, raw: str, source: str, line: Optional[int], code: str, base: Optional[Path] = None) -> Optional[Path]:
        archive_root = self.root / "ARCHIVE"
        return self.safe_path(raw, base or archive_root, archive_root, code, source, line, root_prefix="ARCHIVE")

    def check_archive(self) -> None:
        schema_path = self.root / "ARCHIVE/_SCHEMA.md"
        schema_text = self.read_text(schema_path, "ARCHIVE_SCHEMA_READ")
        if schema_text is not None:
            schema_frontmatter, schema_errors = extract_frontmatter(schema_text)
            for error in schema_errors:
                self.add("ERROR", "ARCHIVE_SCHEMA_FRONTMATTER", "ARCHIVE/_SCHEMA.md", error)
            if schema_frontmatter.get("archive_schema") != "hierarchical-scene-v1":
                self.add("ERROR", "ARCHIVE_SCHEMA_ID", "ARCHIVE/_SCHEMA.md", "archive_schema must be hierarchical-scene-v1")
        index_path = self.root / "ARCHIVE/INDEX.md"
        text = self.read_text(index_path, "ARCHIVE_INDEX_READ")
        if text is None:
            self.add("INCOMPLETE", "ARCHIVE_DEPENDENT_COVERAGE", "ARCHIVE/INDEX.md", "campaign index could not be parsed; ledger scope cannot be established")
            self.check_ledger("ARCHIVE/MESSAGES_LEDGER.md", ["when", "from", "to", "gist", "pointer"], "MESSAGE")
            self.check_ledger("ARCHIVE/RELATION_LEDGER.md", ["when", "persons", "gist", "pointer"], "RELATION")
            return
        index_frontmatter, index_errors = extract_frontmatter(text)
        for error in index_errors:
            self.add("ERROR", "ARCHIVE_INDEX_FRONTMATTER", "ARCHIVE/INDEX.md", error)
        if index_frontmatter.get("archive_schema") != "hierarchical-scene-v1":
            self.add("ERROR", "ARCHIVE_INDEX_SCHEMA", "ARCHIVE/INDEX.md", "archive_schema must be hierarchical-scene-v1")
        rows = self.find_table(
            text,
            ["save_id", "commit_kind", "session", "span", "place", "route_terms", "notes", "folder", "session_index", "event_heading"],
            "ARCHIVE/INDEX.md",
            "ARCHIVE_INDEX",
        )
        if rows is None:
            self.add("INCOMPLETE", "ARCHIVE_DEPENDENT_COVERAGE", "ARCHIVE/INDEX.md", "campaign index table is unparseable; ledger scope cannot be established")
            self.check_ledger("ARCHIVE/MESSAGES_LEDGER.md", ["when", "from", "to", "gist", "pointer"], "MESSAGE")
            self.check_ledger("ARCHIVE/RELATION_LEDGER.md", ["when", "persons", "gist", "pointer"], "RELATION")
            return
        self.archive_rows = rows
        self.metrics["archive_close_rows"] = len(rows)
        current_commit = self.current.get("commit_kind", "")
        if not self.bound and rows:
            self.add(
                "ERROR",
                "ARCHIVE_UNBOUND_HISTORY",
                "ARCHIVE/INDEX.md",
                "unbound CURRENT_SAVE coexists with archived CLOSE rows; use a clean separate folder and do not clear history",
            )
        if self.bound and current_commit == "bind" and rows:
            self.add(
                "ERROR",
                "ARCHIVE_BIND_HISTORY",
                "ARCHIVE/INDEX.md",
                "bind commit coexists with archived CLOSE rows; bind requires a clean run archive",
            )
        if not self.bound or current_commit == "bind":
            allowed_unbound_files = {
                (self.root / "ARCHIVE/_SCHEMA.md").resolve(strict=False),
                (self.root / "ARCHIVE/INDEX.md").resolve(strict=False),
                (self.root / "ARCHIVE/MESSAGES_LEDGER.md").resolve(strict=False),
                (self.root / "ARCHIVE/RELATION_LEDGER.md").resolve(strict=False),
            }
            archive_root = self.root / "ARCHIVE"
            for extra in sorted(path for path in archive_root.rglob("*") if path.is_file() and path.resolve(strict=False) not in allowed_unbound_files):
                code = "ARCHIVE_UNBOUND_CONTENT" if not self.bound else "ARCHIVE_BIND_CONTENT"
                state = "unbound kit" if not self.bound else "bind commit"
                self.add(
                    "ERROR",
                    code,
                    self.relative(extra),
                    f"{state} contains prior-run archive content; use a clean separate folder and do not delete evidence",
                )
        save_ids: set[str] = set()
        folder_routes: dict[Path, int] = {}
        session_indexes: set[Path] = set()
        for row in rows:
            line = row["_line"]
            save_id = strip_code_ticks(row["save_id"]).strip()
            commit = strip_code_ticks(row["commit_kind"]).strip()
            folder_raw = strip_code_ticks(row["folder"]).strip()
            session_raw = strip_code_ticks(row["session_index"]).strip()
            event_heading = strip_code_ticks(row["event_heading"]).strip().lstrip("#")
            if not save_id or is_sentinel(save_id):
                self.add("ERROR", "ARCHIVE_SAVE_ID_EMPTY", "ARCHIVE/INDEX.md", "archive row has empty save_id", line)
            elif save_id in save_ids:
                self.add("ERROR", "ARCHIVE_SAVE_ID_DUPLICATE", "ARCHIVE/INDEX.md", f"duplicate save_id {save_id!r}", line)
            save_ids.add(save_id)
            if commit != "close":
                self.add("ERROR", "ARCHIVE_COMMIT_KIND", "ARCHIVE/INDEX.md", "archive row commit_kind must be close", line)
            folder = self.archive_path(folder_raw, "ARCHIVE/INDEX.md", line, "ARCHIVE_FOLDER_PATH")
            if folder is not None:
                if not folder.is_dir():
                    self.add("ERROR", "ARCHIVE_FOLDER_MISSING", self.relative(folder), "declared close folder does not exist")
                if folder in folder_routes:
                    self.add("ERROR", "ARCHIVE_FOLDER_DUPLICATE", "ARCHIVE/INDEX.md", f"folder is reused from line {folder_routes[folder]}", line)
                folder_routes[folder] = line
                resolved_folder = folder.resolve(strict=False)
                self.archive_folders.add(resolved_folder)
                self.archive_folder_ids[resolved_folder] = save_id
            if not is_sentinel(session_raw):
                session_index = self.archive_path(session_raw, "ARCHIVE/INDEX.md", line, "ARCHIVE_SESSION_INDEX_PATH")
                if session_index is not None:
                    session_indexes.add(session_index)
                    if not session_index.is_file():
                        self.add("ERROR", "ARCHIVE_SESSION_INDEX_MISSING", self.relative(session_index), "session index does not exist")
                    if folder is not None:
                        try:
                            session_index.resolve(strict=False).relative_to(folder.resolve(strict=False))
                        except ValueError:
                            self.add("ERROR", "ARCHIVE_SESSION_INDEX_OUTSIDE", "ARCHIVE/INDEX.md", "session_index is not inside its declared folder", line)
                        if session_index.resolve(strict=False) != (folder / "INDEX.md").resolve(strict=False):
                            self.add(
                                "ERROR",
                                "ARCHIVE_SESSION_INDEX_ROUTE",
                                "ARCHIVE/INDEX.md",
                                "session_index must be the INDEX.md directly inside its declared folder",
                                line,
                            )
                    if session_index.name != "INDEX.md":
                        self.add("ERROR", "ARCHIVE_SESSION_INDEX_NAME", self.relative(session_index), "session index must be named INDEX.md")
                    if session_index.is_file() and (session_index, save_id) not in self._parsed_sessions:
                        self._parsed_sessions.add((session_index, save_id))
                        self.check_session_index(session_index, save_id)
            elif folder is not None and folder.is_dir() and event_heading:
                matches: list[tuple[Path, int]] = []
                for source in sorted(folder.rglob("*.md")):
                    if source.name.casefold() in {
                        "index.md",
                        "_schema.md",
                        "messages_ledger.md",
                        "relation_ledger.md",
                    }:
                        continue
                    source_text = self.read_text(source, "ARCHIVE_LEGACY_READ")
                    if source_text is None:
                        continue
                    for occurrence in heading_map(source_text).get(event_heading, []):
                        matches.append((source, occurrence))
                if len(matches) != 1:
                    self.add("ERROR", "ARCHIVE_LEGACY_HEADING", "ARCHIVE/INDEX.md", f"legacy heading {event_heading!r} resolves {len(matches)} times in folder", line)
            else:
                self.add("ERROR", "ARCHIVE_ROUTE_MISSING", "ARCHIVE/INDEX.md", "row has neither a session index nor a resolvable legacy heading", line)

        evidence = self.current.get("evidence_through", "none")
        archive_ref = self.current.get("archive_ref", "none")
        if self.bound and evidence != "none":
            evidence_rows = [row for row in rows if strip_code_ticks(row["save_id"]).strip() == evidence]
            if len(evidence_rows) != 1:
                self.add("ERROR", "ARCHIVE_EVIDENCE_BOUNDARY", "INSTANCE/CURRENT_SAVE.md", "evidence_through does not resolve to exactly one archived full save")
            elif strip_code_ticks(evidence_rows[0]["folder"]).strip() != archive_ref:
                self.add("ERROR", "ARCHIVE_EVIDENCE_FOLDER", "INSTANCE/CURRENT_SAVE.md", "archive_ref does not match the evidence_through archive row")
        elif self.bound and current_commit == "checkpoint" and rows:
            self.add("ERROR", "ARCHIVE_CHECKPOINT_LOST_BOUNDARY", "INSTANCE/CURRENT_SAVE.md", "checkpoint cannot clear an existing archived evidence boundary")

        current_save_id = self.current.get("save_id", "")
        if self.bound and current_commit == "close":
            matches = [row for row in rows if strip_code_ticks(row["save_id"]).strip() == current_save_id]
            if len(matches) != 1:
                self.add("ERROR", "ARCHIVE_CURRENT_CLOSE_ROW", "ARCHIVE/INDEX.md", f"current close save_id resolves to {len(matches)} rows")
            else:
                row = matches[0]
                folder_raw = strip_code_ticks(row["folder"]).strip()
                archive_ref = strip_code_ticks(self.current.get("archive_ref", "")).strip()
                if folder_raw != archive_ref:
                    self.add("ERROR", "ARCHIVE_CURRENT_FOLDER_MISMATCH", "ARCHIVE/INDEX.md", f"row folder {folder_raw!r} != archive_ref {archive_ref!r}", row["_line"])
                if is_sentinel(row["session_index"]):
                    self.add("ERROR", "ARCHIVE_CURRENT_SESSION_INDEX", "ARCHIVE/INDEX.md", "current close requires a nonempty session_index", row["_line"])
                if is_sentinel(row["route_terms"]):
                    self.add("ERROR", "ARCHIVE_CURRENT_ROUTE_TERMS", "ARCHIVE/INDEX.md", "current close requires compact nonempty route_terms", row["_line"])
                if not is_sentinel(row["event_heading"]):
                    self.add("ERROR", "ARCHIVE_CURRENT_LEGACY_ROUTE", "ARCHIVE/INDEX.md", "new hierarchical CLOSE rows leave legacy event_heading empty", row["_line"])
                folder = self.archive_path(folder_raw, "ARCHIVE/INDEX.md", row["_line"], "ARCHIVE_CURRENT_FOLDER_PATH")
                sessions_root = (self.root / "ARCHIVE/sessions").resolve(strict=False)
                if folder is not None and folder.resolve(strict=False).parent != sessions_root:
                    self.add("ERROR", "ARCHIVE_CURRENT_FOLDER_LAYOUT", "ARCHIVE/INDEX.md", "new hierarchical CLOSE folder must be a direct child of ARCHIVE/sessions", row["_line"])
        elif self.bound and current_commit in {"bind", "checkpoint"} and current_save_id:
            if any(strip_code_ticks(row["save_id"]).strip() == current_save_id for row in rows):
                self.add("ERROR", "ARCHIVE_NONCLOSE_ROW", "ARCHIVE/INDEX.md", f"{current_commit} save_id must not have an archive row")

        sessions_root = self.root / "ARCHIVE/sessions"
        if sessions_root.is_dir():
            declared_folders = {path.resolve(strict=False) for path in folder_routes}
            for directory in sorted(path for path in sessions_root.iterdir() if path.is_dir()):
                if directory.resolve(strict=False) not in declared_folders:
                    self.add("ERROR", "ARCHIVE_ORPHAN_SESSION", self.relative(directory), "session folder has no campaign INDEX row")
        self.check_ledger("ARCHIVE/MESSAGES_LEDGER.md", ["when", "from", "to", "gist", "pointer"], "MESSAGE")
        self.check_ledger("ARCHIVE/RELATION_LEDGER.md", ["when", "persons", "gist", "pointer"], "RELATION")

    def check_session_index(self, index_path: Path, save_id: str) -> None:
        text = self.read_text(index_path, "SESSION_INDEX_READ")
        if text is None:
            return
        lines = text.splitlines()
        visible, structural = structural_markdown_lines(lines)
        headings = [(line, title) for line, level, title in iter_literal_headings(text) if level == 2 and title.startswith("R-")]
        if not headings:
            self.add("ERROR", "SESSION_NO_ENTRIES", self.relative(index_path), "session index has no R-* entries")
            return
        all_level_two = [(line, title) for line, level, title in iter_literal_headings(text) if level == 2]
        for line, title in all_level_two:
            if not title.startswith("R-"):
                self.add(
                    "ERROR",
                    "SESSION_UNEXPECTED_ENTRY_HEADING",
                    self.relative(index_path),
                    f"unexpected level-two heading {title!r}; session INDEX level-two headings must be R-* entries",
                    line,
                )
        heading_starts = [line for line, _title in all_level_two]
        seen_routes: set[tuple[Path, str]] = set()
        seen_r: set[str] = set()
        seen_e: set[str] = set()
        seen_files: set[Path] = set()
        referenced_files: set[Path] = set()
        max_lines = 0
        for line_number, title in headings:
            route_id = re.split(r"\s+|\s*—\s*", title, maxsplit=1)[0]
            if route_id in seen_r:
                self.add("ERROR", "SESSION_ROUTE_ID_DUPLICATE", self.relative(index_path), f"duplicate route id {route_id!r}", line_number)
            seen_r.add(route_id)
            if not re.fullmatch(rf"R-{re.escape(save_id)}-[A-Za-z0-9][A-Za-z0-9._-]*", route_id):
                self.add("ERROR", "SESSION_ROUTE_ID_SAVE", self.relative(index_path), f"route id {route_id!r} does not use save_id {save_id!r}", line_number)
            later = [number for number in heading_starts if number > line_number]
            end = (min(later) - 1) if later else len(lines)
            section = lines[line_number - 1 : end]
            nonblank = sum(1 for line in section if line.strip())
            max_lines = max(max_lines, nonblank)
            if nonblank > 12:
                self.add("ERROR", "SESSION_ENTRY_LINE_BUDGET", self.relative(index_path), f"entry has {nonblank} nonblank lines; maximum is 12 inclusive", line_number)
            fields: dict[str, tuple[str, int]] = {}
            field_order: list[str] = []
            notable_bullets = 0
            after_notable = False
            for offset, raw in enumerate(section[1:], line_number + 1):
                if not visible[offset - 1]:
                    continue
                structural_line = structural[offset - 1].strip()
                match = re.match(r"^(File|Evidence|Time|People|Places|Topics|Notable):\s*(.*)$", structural_line, flags=re.IGNORECASE)
                if match:
                    key = match.group(1).casefold()
                    if key in fields:
                        self.add("ERROR", "SESSION_FIELD_DUPLICATE", self.relative(index_path), f"duplicate {key} field", offset)
                    fields[key] = (match.group(2).strip(), offset)
                    field_order.append(key)
                    after_notable = key == "notable"
                elif after_notable and re.match(r"^[-*+]\s+", structural_line):
                    notable_bullets += 1
            for required in ("file", "evidence", "time", "people", "places", "topics", "notable"):
                if required not in fields:
                    self.add("ERROR", "SESSION_FIELD_MISSING", self.relative(index_path), f"entry lacks {required.title()} field", line_number)
            expected_order = ["file", "evidence", "time", "people", "places", "topics", "notable"]
            if field_order != expected_order:
                self.add(
                    "ERROR",
                    "SESSION_FIELD_ORDER",
                    self.relative(index_path),
                    "entry fields must occur exactly once in File, Evidence, Time, People, Places, Topics, Notable order",
                    line_number,
                )
            for required_value in ("time", "people", "places", "topics"):
                if required_value in fields and not fields[required_value][0].strip():
                    self.add(
                        "ERROR",
                        "SESSION_FIELD_EMPTY",
                        self.relative(index_path),
                        f"{required_value.title()} must contain a value; use 'unknown' or 'none' explicitly when appropriate",
                        fields[required_value][1],
                    )
            if notable_bullets > 2:
                self.add("ERROR", "SESSION_NOTABLE_BUDGET", self.relative(index_path), f"Notable has {notable_bullets} bullets; maximum is 2", line_number)
            if "file" not in fields or "evidence" not in fields:
                continue
            file_raw, file_line = fields["file"]
            evidence = strip_code_ticks(fields["evidence"][0]).strip()
            if evidence.startswith("#"):
                self.add(
                    "ERROR",
                    "SESSION_EVIDENCE_FORMAT",
                    self.relative(index_path),
                    "Evidence names literal heading text and must not begin with '#'",
                    fields["evidence"][1],
                )
            target = self.safe_path(file_raw, index_path.parent, index_path.parent, "SESSION_SHARD_PATH", self.relative(index_path), file_line)
            if target is None:
                continue
            if target.suffix.casefold() != ".md":
                self.add("ERROR", "SESSION_SHARD_EXTENSION", self.relative(index_path), "session File must target a Markdown .md source", file_line)
                continue
            if target.resolve(strict=False) == index_path.resolve(strict=False) or target.name.casefold() in {
                "index.md",
                "_schema.md",
                "messages_ledger.md",
                "relation_ledger.md",
            }:
                self.add(
                    "ERROR",
                    "SESSION_SHARD_SCOPE",
                    self.relative(index_path),
                    "File must target an evidence shard, not an index, ledger, or archive contract",
                    file_line,
                )
                continue
            target_resolved = target.resolve(strict=False)
            referenced_files.add(target.resolve(strict=False))
            if not target.is_file():
                self.add("ERROR", "SESSION_SHARD_MISSING", self.relative(target), "pointed source shard does not exist")
                continue
            if evidence.startswith("E-"):
                if target_resolved in seen_files:
                    self.add(
                        "ERROR",
                        "SESSION_SHARD_DUPLICATE_ENTRY",
                        self.relative(index_path),
                        "one v0.4 E-* session INDEX entry is allowed per semantic evidence shard",
                        line_number,
                    )
                seen_files.add(target_resolved)
                if evidence in seen_e:
                    self.add("ERROR", "SESSION_EVIDENCE_ID_DUPLICATE", self.relative(index_path), f"evidence id {evidence!r} is reused in this session", fields["evidence"][1])
                seen_e.add(evidence)
                if not re.fullmatch(rf"E-{re.escape(save_id)}-[A-Za-z0-9][A-Za-z0-9._-]*", evidence):
                    self.add("ERROR", "SESSION_EVIDENCE_ID_SAVE", self.relative(index_path), f"evidence id {evidence!r} does not use save_id {save_id!r}", fields["evidence"][1])
            else:
                self.add(
                    "WARNING",
                    "SESSION_LEGACY_EVIDENCE_ID",
                    self.relative(index_path),
                    f"non-v0.4 evidence heading {evidence!r} is accepted as a literal legacy route",
                    fields["evidence"][1],
                )
            route = (target.resolve(strict=False), evidence)
            if route in seen_routes:
                self.add("ERROR", "SESSION_ROUTE_DUPLICATE", self.relative(index_path), "duplicate file/evidence route", line_number)
            seen_routes.add(route)
            source_text = self.read_text(target, "SESSION_SHARD_READ")
            if source_text is None:
                continue
            source_headings = list(iter_literal_headings(source_text))
            headings_by_title = heading_map(source_text)
            if evidence.startswith("E-"):
                count = sum(1 for _line, level, title in source_headings if level == 2 and title == evidence)
            else:
                count = len(headings_by_title.get(evidence, []))
            if count != 1:
                expected_level = " at level two" if evidence.startswith("E-") else ""
                self.add("ERROR", "SESSION_EVIDENCE_HEADING", self.relative(target), f"literal heading {evidence!r} occurs {count} times{expected_level}")
            for stable, occurrences in headings_by_title.items():
                if re.match(r"^(?:E|M|ROLL|TX)-", stable):
                    if len(occurrences) > 1:
                        self.add("ERROR", "ARCHIVE_STABLE_HEADING_DUPLICATE", self.relative(target), f"stable heading {stable!r} occurs {len(occurrences)} times")
                    if not re.fullmatch(rf"(?:E|M|ROLL|TX)-{re.escape(save_id)}-[A-Za-z0-9][A-Za-z0-9._-]*", stable):
                        self.add(
                            "ERROR",
                            "ARCHIVE_STABLE_HEADING_SAVE_ID",
                            self.relative(target),
                            f"stable heading {stable!r} does not use owning CLOSE save_id {save_id!r}",
                            occurrences[0] if occurrences else None,
                        )
        self.metrics["session_index_max_entry_lines"] = max(self.metrics.get("session_index_max_entry_lines", 0), max_lines)
        for source in sorted(index_path.parent.rglob("*.md")):
            if source.resolve(strict=False) == index_path.resolve(strict=False):
                continue
            if source.resolve(strict=False) not in referenced_files:
                self.add(
                    "WARNING",
                    "SESSION_ORPHAN_SOURCE",
                    self.relative(source),
                    "session source file has no INDEX entry; it may be retained legacy evidence, but it is not routable",
                )

    def check_ledger(self, relative: str, header: list[str], kind: str) -> None:
        path = self.root / relative
        if not path.exists() and not path.is_symlink():
            return
        text = self.read_text(path, f"{kind}_LEDGER_READ")
        if text is None:
            return
        rows = self.find_table(text, header, relative, f"{kind}_LEDGER")
        if rows is None:
            return
        self.metrics[kind.casefold() + "_ledger_rows"] = len(rows)
        for row in rows:
            for field in header[:-1]:
                if not strip_code_ticks(row[field]).strip():
                    self.add("ERROR", f"{kind}_FIELD_EMPTY", relative, f"ledger field {field!r} is blank; use an explicit routing value", row["_line"])
            pointer = strip_code_ticks(row["pointer"]).strip()
            file_part, separator, fragment = pointer.rpartition("#")
            fragment = strip_code_ticks(fragment).strip()
            if not separator or not file_part or not fragment:
                self.add("ERROR", f"{kind}_POINTER_FORMAT", relative, f"pointer must be path#literal-heading: {pointer!r}", row["_line"])
                continue
            target = self.archive_path(file_part, relative, row["_line"], f"{kind}_POINTER_PATH")
            if target is None:
                continue
            if target.suffix.casefold() != ".md":
                self.add("ERROR", f"{kind}_POINTER_EXTENSION", relative, "ledger pointer must target a Markdown .md source", row["_line"])
                continue
            target_resolved = target.resolve(strict=False)
            in_close_folder = any(
                target_resolved == folder or folder in target_resolved.parents for folder in self.archive_folders
            )
            if not in_close_folder or target.name.casefold() in {
                "index.md",
                "_schema.md",
                "messages_ledger.md",
                "relation_ledger.md",
            }:
                self.add(
                    "ERROR",
                    f"{kind}_POINTER_SCOPE",
                    relative,
                    "ledger pointer must target a source file inside a declared close folder, not an index or archive contract",
                    row["_line"],
                )
                continue
            if not target.is_file():
                self.add("ERROR", f"{kind}_POINTER_FILE", self.relative(target), "ledger target file does not exist")
                continue
            target_text = self.read_text(target, f"{kind}_POINTER_READ")
            if target_text is None:
                continue
            legacy_name = "messages.md" if kind == "MESSAGE" else "transcript.md"
            if target.name.casefold() != legacy_name and not re.fullmatch(r"(?:E|M|ROLL|TX)-[A-Za-z0-9][A-Za-z0-9._-]*", fragment):
                self.add(
                    "ERROR",
                    f"{kind}_POINTER_STABLE_ID",
                    relative,
                    "non-legacy ledger pointers must name a stable E-/M-/ROLL-/TX- heading id",
                    row["_line"],
                )
            if target.name.casefold() != legacy_name:
                owning_folders = [folder for folder in self.archive_folder_ids if target_resolved == folder or folder in target_resolved.parents]
                if owning_folders:
                    owner = max(owning_folders, key=lambda folder: len(folder.parts))
                    owner_save_id = self.archive_folder_ids[owner]
                    if not re.fullmatch(rf"(?:E|M|ROLL|TX)-{re.escape(owner_save_id)}-[A-Za-z0-9][A-Za-z0-9._-]*", fragment):
                        self.add(
                            "ERROR",
                            f"{kind}_POINTER_SAVE_ID",
                            relative,
                            f"stable heading id does not use owning CLOSE save_id {owner_save_id!r}",
                            row["_line"],
                        )
            count = len(heading_map(target_text).get(fragment, []))
            if count != 1:
                self.add("ERROR", f"{kind}_POINTER_HEADING", self.relative(target), f"literal heading {fragment!r} occurs {count} times")

    def run(self, initial_snapshot: dict[str, str]) -> None:
        self.check_snapshot_types(initial_snapshot)
        self.check_required_files()
        self.check_law()
        self.check_current_save()
        self.check_campaign_contract()
        self.check_bearing()
        self.check_preparation()
        self.check_initial_instance()
        self.check_recovery()
        self.check_handover()
        self.check_engines()
        self.check_module()
        self.check_safety()
        self.check_archive()


def sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        set(findings),
        key=lambda item: (
            SEVERITY_ORDER.get(item.severity, 99),
            item.code,
            item.path,
            item.line if item.line is not None else -1,
            item.message,
        ),
    )


def make_report(
    root: Path,
    validator: Validator,
    initial_digest: str,
    final_digest: str,
    tree_stable: bool,
    executed_validator_hash: str,
    executed_validator_final_hash: str,
    target_validator_initial_hash: str,
    target_validator_hash: str,
    validator_identity_matches: bool,
) -> tuple[dict[str, Any], int]:
    findings = sorted_findings(validator.findings)
    has_error = any(item.severity == "ERROR" for item in findings)
    has_incomplete = any(item.severity == "INCOMPLETE" for item in findings)
    has_warning = any(item.severity == "WARNING" for item in findings)
    if has_incomplete:
        structural_result, exit_code = "INCOMPLETE", 2
    elif has_error:
        structural_result, exit_code = "FAIL", 1
    elif has_warning:
        structural_result, exit_code = "PASS WITH WARNINGS", 0
    else:
        structural_result, exit_code = "PASS", 0
    report = {
        "validate": VALIDATOR_VERSION,
        "target_root": str(root),
        "validator_sha256": executed_validator_hash,
        "validator_final_sha256": executed_validator_final_hash,
        "validator_stable_during_run": executed_validator_hash == executed_validator_final_hash,
        "target_validator_initial_sha256": target_validator_initial_hash,
        "target_validator_sha256": target_validator_hash,
        "target_validator_matches_executed": validator_identity_matches,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "validated_tree_digest": final_digest if tree_stable else None,
        "initial_tree_digest": initial_digest,
        "final_tree_digest": final_digest,
        "tree_stable_during_run": tree_stable,
        "structural": {
            "result": structural_result,
            "provenance": "SCRIPT-VERIFIED",
            "coverage": [
                "required playable files including agent-state, upgrade procedures and source/search/evidence tools; explanatory documents and developer tests are not campaign dependencies; executed/target validator identity, whole-tree path types/case, and observed LAW digest (no immutable hash requirement)",
                "CURRENT_SAVE metadata/readable sections, optional Session continuity table, commit/evidence boundary, explicit record routes, PC overlay, and candidate residue",
                "accepted Campaign Contract identity, binding, revision, required readable terms and five named clause locations/counts/content presence, and candidate residue",
                "optional cold Bearing provenance and staleness warnings; active recovery and handover marker presence (handover package integrity requires its separate checker)",
                "optional derivative PREP identity/basis and safe source paths; freshness, faithful causal synthesis, feedback retention, prior omission and once-only session adjudication require source comparison and cannot be proved from one snapshot",
                "clean unbound INSTANCE paths and bound PC overlay",
                "installed engine identity, safe ids, and declared character-build support",
                "bound module using v0.4 descriptor grammar, required setting-brief identity/sections and candidate residue, capabilities/routes, optional POLICY source voice, closed PC routing bundles, and T0/bind consistency where machine-parseable",
                "SAFETY flag and entry presence",
                "campaign/session archive routing, entry budgets, source reachability, and literal headings",
                "optional message/relation ledger pointer scope and resolution",
                "start/end tree digest stability",
            ],
        },
        "host_observation": {"result": "NOT RUN"},
        "semantic": {"result": "NOT CHECKED"},
        "metrics": dict(sorted(validator.metrics.items())),
        "findings": [asdict(item) for item in findings],
    }
    return report, exit_code


def print_human(report: dict[str, Any]) -> None:
    print(report["validate"])
    print(f"Target root: {report['target_root']}")
    print(f"Validator SHA-256: {report['validator_sha256']}")
    print(f"Validator final SHA-256: {report['validator_final_sha256']}")
    print(f"Validator stable during run: {'yes' if report['validator_stable_during_run'] else 'no'}")
    print(f"Initial target validator SHA-256: {report['target_validator_initial_sha256']}")
    print(f"Target validator SHA-256: {report['target_validator_sha256']}")
    print(f"Target validator matches executed: {'yes' if report['target_validator_matches_executed'] else 'no'}")
    print(f"Observed at: {report['observed_at']}")
    print(f"Validated tree digest: {report['validated_tree_digest'] or 'UNAVAILABLE (tree changed)'}")
    print(f"Tree stable during run: {'yes' if report['tree_stable_during_run'] else 'no'}")
    print()
    structural = report["structural"]
    print("STRUCTURAL")
    print(f"Result: {structural['result']}")
    print(f"Provenance: {structural['provenance']}")
    print("Coverage: " + "; ".join(structural["coverage"]))
    print()
    print("HOST OBSERVATION")
    print("Result: NOT RUN")
    print()
    print("SEMANTIC")
    print("Result: NOT CHECKED")
    print()
    if report["metrics"]:
        print("METRICS")
        for key, value in report["metrics"].items():
            print(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        print()
    print("FINDINGS")
    if not report["findings"]:
        print("none")
    else:
        for finding in report["findings"]:
            location = finding["path"]
            if finding["line"] is not None:
                location += f":{finding['line']}"
            print(f"[{finding['severity']}] {finding['code']} {location} — {finding['message']}")


def execution_failure_report(root: Path, message: str) -> dict[str, Any]:
    try:
        executed_hash = sha256_bytes(Path(__file__).resolve().read_bytes())
    except OSError:
        executed_hash = "unavailable"
    return {
        "validate": VALIDATOR_VERSION,
        "target_root": str(root),
        "validator_sha256": executed_hash,
        "validator_final_sha256": executed_hash,
        "validator_stable_during_run": False,
        "target_validator_initial_sha256": "unavailable",
        "target_validator_sha256": "unavailable",
        "target_validator_matches_executed": False,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "validated_tree_digest": None,
        "initial_tree_digest": None,
        "final_tree_digest": None,
        "tree_stable_during_run": False,
        "structural": {
            "result": "INCOMPLETE",
            "provenance": "SCRIPT-VERIFIED",
            "coverage": [],
        },
        "host_observation": {"result": "NOT RUN"},
        "semantic": {"result": "NOT CHECKED"},
        "metrics": {},
        "findings": [asdict(Finding("INCOMPLETE", "VALIDATOR_EXECUTION", ".", None, message))],
    }


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    default_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Read-only structural validator for RPG OS")
    parser.add_argument("--root", type=Path, default=default_root, help="RPG_OS root (default: parent of TOOLS)")
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    if not args.json:
        # A diagnostic must still complete when the operator's terminal cannot
        # encode a path or message. JSON output is ASCII-escaped separately.
        try:
            sys.stdout.reconfigure(errors="backslashreplace")
        except (AttributeError, OSError, ValueError):
            pass
    requested_root = args.root
    root = Path(os.path.abspath(os.fspath(requested_root)))
    try:
        requested_root = requested_root.expanduser()
        root = Path(os.path.abspath(os.fspath(requested_root)))
        if requested_root.is_symlink():
            raise ValidationExecutionError("root must not be a symlink")
        root = requested_root.resolve(strict=False)
        if not root.is_dir():
            raise ValidationExecutionError(f"root is not a directory: {root}")
        executed_validator_path = Path(__file__).resolve()
        executed_validator_hash = sha256_bytes(executed_validator_path.read_bytes())
        initial_snapshot, initial_digest = snapshot_tree(root)
        initial_target_descriptor = initial_snapshot.get("TOOLS/validate.py", "")
        target_validator_initial_hash = (
            initial_target_descriptor.rpartition(":")[2]
            if initial_target_descriptor.startswith("F:")
            else "unavailable"
        )
        validator = Validator(root)
        validator.run(initial_snapshot)
        final_snapshot, final_digest = snapshot_tree(root)
        stable = initial_snapshot == final_snapshot
        if not stable:
            validator.add("INCOMPLETE", "TREE_CHANGED_DURING_VALIDATION", ".", "tree contents or paths changed while validation ran")
        executed_validator_final_hash = sha256_bytes(executed_validator_path.read_bytes())
        target_descriptor = final_snapshot.get("TOOLS/validate.py", "")
        target_validator_hash = target_descriptor.rpartition(":")[2] if target_descriptor.startswith("F:") else "unavailable"
        if executed_validator_hash != executed_validator_final_hash:
            validator.add(
                severity="INCOMPLETE",
                code="VALIDATOR_CHANGED_DURING_RUN",
                path="TOOLS/validate.py",
                message="the executed validator file changed while validation ran",
            )
        validator_identity_matches = (
            executed_validator_hash
            == executed_validator_final_hash
            == target_validator_initial_hash
            == target_validator_hash
        )
        if not validator_identity_matches:
            validator.add(
                severity="INCOMPLETE",
                code="VALIDATOR_TARGET_MISMATCH",
                path="TOOLS/validate.py",
                message="the target validator was not byte-identical to the executed validator for the full run",
            )
        report, exit_code = make_report(
            root,
            validator,
            initial_digest,
            final_digest,
            stable,
            executed_validator_hash,
            executed_validator_final_hash,
            target_validator_initial_hash,
            target_validator_hash,
            validator_identity_matches,
        )
    except Exception as exc:
        report = execution_failure_report(root, str(exc))
        exit_code = 2
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        print_human(report)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
