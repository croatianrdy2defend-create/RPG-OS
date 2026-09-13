#!/usr/bin/env python3
"""Preserve supplied evidence and freeze scoped inputs for an externally authored audit.

Standard library only. No platform access, model calls, narrative verdicts or repairs.
Every command prints JSON. Exit 0: requested structural operation succeeded;
1: invalid input/package/report; 2: report still awaits review.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import uuid

import read_source

CAPTURE_SCHEMA = "rpg-evidence-capture-v1"
BUNDLE_SCHEMA = "rpg-evidence-audit-bundle-v1"
REPORT_SCHEMA = "rpg-evidence-audit-report-v1"
SELECTION_SCHEMA = "rpg-source-selection-v1"
RECEIPT_SCHEMA = "rpg-source-delivery-receipt-v1"
RESERVED = re.compile(r"(?:CON|PRN|AUX|NUL|CONIN\$|CONOUT\$|COM[0-9¹²³]|LPT[0-9¹²³])(?:\..*)?\Z", re.I)
HEX = re.compile(r"[0-9a-f]{64}\Z")


class EvidenceError(Exception):
    """An unsafe, stale, malformed, or inconsistent input."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def pairs_unique(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def parse_json(data, label):
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs_unique,
                          parse_constant=lambda value: (_ for _ in ()).throw(
                              EvidenceError(f"non-finite JSON value: {value}")))
    except (UnicodeError, ValueError) as exc:
        raise EvidenceError(f"invalid UTF-8 JSON in {label}: {exc}") from None


def route(value):
    require(isinstance(value, str) and value, "relative path must be a nonempty string")
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value, f"noncanonical relative path: {value}")
    require(all(part not in (".", "..") and not part.endswith((".", " "))
                and not re.search(r'[<>:"\\|?*\x00-\x1f]', part)
                and not RESERVED.fullmatch(part) for part in path.parts),
            f"unsafe relative path: {value}")
    return path


def inspect(path):
    try:
        info = path.lstat()
    except OSError as exc:
        raise EvidenceError(f"cannot inspect {path}: {exc}") from None
    require(not stat.S_ISLNK(info.st_mode)
            and not (getattr(info, "st_file_attributes", 0) & 0x400),
            f"symlink or reparse point refused: {path}")
    require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),
            f"special file refused: {path}")
    return info


def checked_absolute(value, directory=False):
    require(".." not in Path(value).parts, "input path must not contain parent traversal")
    # Validate before abspath: Windows may erase trailing-dot/space aliases.
    for name in Path(value).parts:
        if name != Path(value).anchor:
            route(name)
    path = Path(os.path.abspath(value))
    for name in path.parts[1:]:
        route(name)
    for part in reversed((path, *path.parents)):
        inspect(part)
    require(path.is_dir() if directory else path.is_file(),
            f"expected {'directory' if directory else 'regular file'}: {path}")
    return path.resolve(strict=True)


def rooted(root, relative):
    path = root
    for component in route(relative).parts:
        path /= component
        inspect(path)
    return path


def read_bytes(path):
    path = checked_absolute(path)
    before = inspect(path)
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise EvidenceError(f"cannot read {path}: {exc}") from None
    after = inspect(path)
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
            == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
            and len(data) == before.st_size, f"source changed during read: {path}")
    return data


def read_json(path):
    return parse_json(read_bytes(path), path)


def strings(value, label, allow_empty=True):
    require(isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value),
            f"{label} must be a list of nonempty strings")
    require(allow_empty or bool(value), f"{label} must not be empty")
    return value


def within(path, parent):
    return path == parent or parent in path.parents


def output_path(value, protected):
    require(".." not in Path(value).parts, "output path must not contain parent traversal")
    for name in Path(value).parts:
        if name != Path(value).anchor:
            route(name)
    path = Path(os.path.abspath(value))
    require(not os.path.lexists(path), f"output already exists; no overwrite: {path}")
    for part in reversed((path, *path.parents)):
        if part.name:
            route(part.name)
        if os.path.lexists(part):
            require(stat.S_ISDIR(inspect(part).st_mode), f"output ancestor is not a directory: {part}")
        else:
            route(part.name)
    missing = []
    ancestor = path
    while not os.path.lexists(ancestor):
        missing.append(ancestor.name)
        ancestor = ancestor.parent
    # Resolve only after checking the original chain. This expands Windows 8.3
    # aliases so they cannot hide an output nested inside a protected read root.
    path = ancestor.resolve(strict=True).joinpath(*reversed(missing))
    for source in protected:
        source = checked_absolute(source, directory=Path(source).is_dir())
        require(not within(path, source) and not within(source, path),
                f"output overlaps a protected input: {source}")
    require(not os.path.lexists(path), f"output already exists; no overwrite: {path}")
    return path


def write_package(output, files, protected):
    destination = output_path(output, protected)
    # Validate every planned filename before creating any output.
    folded = set()
    for relative, data in files.items():
        route(relative)
        require(relative.casefold() not in folded, f"case-colliding output: {relative}")
        folded.add(relative.casefold())
        require(isinstance(data, bytes), "package values must be exact bytes")
    missing = []
    ancestor = destination.parent
    while not ancestor.exists():
        missing.append(ancestor)
        ancestor = ancestor.parent
    for parent in reversed(missing):
        parent.mkdir()
        inspect(parent)
    destination.mkdir()  # Atomic no-overwrite reservation.
    for relative, data in files.items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        for component in reversed((path.parent, *path.parent.parents)):
            inspect(component)
        with path.open("xb") as handle:
            handle.write(data)
    return destination


def inventory(root):
    root = checked_absolute(root, directory=True)
    paths = []
    for directory, directories, files in os.walk(root, followlinks=False):
        for name in directories + files:
            path = Path(directory) / name
            info = inspect(path)
            if stat.S_ISREG(info.st_mode):
                relative = path.relative_to(root).as_posix()
                route(relative)
                paths.append(relative)
    require(len({value.casefold() for value in paths}) == len(paths), "case-colliding package files")
    return sorted(paths)


def validate_claims(claims):
    require(isinstance(claims, dict), "metadata must be a JSON object")
    allowed = {"campaign_id", "save_id", "message_boundary", "conversation_complete", "gaps", "notes", "source_description"}
    require(not set(claims) - allowed, f"unknown metadata fields: {sorted(set(claims) - allowed)}")
    for key in ("campaign_id", "save_id", "notes", "source_description"):
        require(key not in claims or isinstance(claims[key], str), f"metadata {key} must be text")
    require(claims.get("conversation_complete") is None
            or type(claims["conversation_complete"]) is bool,
            "conversation_complete must be true, false or null (a caller claim only)")
    if "message_boundary" in claims:
        boundary = claims["message_boundary"]
        require(isinstance(boundary, dict) and not set(boundary) - {"first", "last", "description"}
                and all(isinstance(value, str) for value in boundary.values()),
                "message_boundary must contain text first, last and/or description fields")
    strings(claims.get("gaps", []), "metadata gaps")
    return claims


def capture_metadata_template():
    """Editable caller claims, with no assertion of export completeness."""
    return validate_claims({"campaign_id": "", "save_id": "",
                            "message_boundary": {"first": "", "last": "", "description": ""},
                            "conversation_complete": None, "gaps": [],
                            "notes": "", "source_description": ""})


def source_layout(data, source_format):
    try:
        text = data.decode("utf-8")
    except UnicodeError as exc:
        raise EvidenceError(f"source is not valid UTF-8: {exc}") from None
    require("\x00" not in text, "source contains NUL; expected text evidence")
    require(source_format in ("raw", "jsonl"), "format must be raw or jsonl")
    records = []
    if source_format == "jsonl":
        offset = 0
        # JSONL records are separated by LF; preserve CRLF and every original byte.
        for number, line in enumerate(data.splitlines(keepends=True), 1):
            require(line.strip(), f"JSONL line {number} is blank")
            value = parse_json(line, f"JSONL line {number}")
            require(isinstance(value, dict) and isinstance(value.get("role"), str)
                    and value["role"].strip() and isinstance(value.get("content"), str),
                    f"JSONL line {number} needs nonempty role and string content")
            records.append({"record": number, "start_byte": offset, "end_byte_exclusive": offset + len(line),
                            "role": value["role"]})
            offset += len(line)
    return {"start_byte": 0, "end_byte_exclusive": len(data), "verified_bytes": len(data),
            "source_line_count": len(re.findall(r"[^\r\n]*(?:\r\n|\r|\n)|[^\r\n]+$", text)), "message_records": records}


def import_capture(input_file, output, source_format="raw", metadata=None):
    source = checked_absolute(input_file)
    data = read_bytes(source)
    coverage = source_layout(data, source_format)
    claims = validate_claims({} if metadata is None else metadata)
    filename = "source.txt" if source_format == "raw" else "source.jsonl"
    manifest = {"schema": CAPTURE_SCHEMA, "capture_id": str(uuid.uuid4()),
                "created_at": datetime.now(timezone.utc).isoformat(), "status": "captured", "format": source_format,
                "source": {"path": filename, "sha256": sha(data), "size_bytes": len(data),
                           "encoding": "utf-8", "provided_filename": source.name},
                "byte_coverage": coverage, "caller_claims": claims,
                "conversation_completeness": "unverified_caller_claim"}
    require(read_bytes(source) == data, "input changed before capture creation")
    destination = write_package(output, {filename: data, "manifest.json": json_bytes(manifest)}, [source])
    return check_capture(destination)


def pending_capture(output, metadata=None):
    manifest = {"schema": CAPTURE_SCHEMA, "capture_id": str(uuid.uuid4()),
                "created_at": datetime.now(timezone.utc).isoformat(), "status": "pending",
                "format": None, "source": None, "byte_coverage": None,
                "caller_claims": validate_claims({} if metadata is None else metadata),
                "conversation_completeness": "unverified_caller_claim"}
    return check_capture(write_package(output, {"manifest.json": json_bytes(manifest)}, []))


def valid_uuid(value, label):
    try:
        require(isinstance(value, str) and str(uuid.UUID(value)) == value, f"invalid {label}")
    except (ValueError, AttributeError):
        raise EvidenceError(f"invalid {label}") from None


def check_capture(capture):
    root = checked_absolute(capture, directory=True)
    manifest_bytes = read_bytes(rooted(root, "manifest.json"))
    manifest = parse_json(manifest_bytes, "capture manifest")
    require(isinstance(manifest, dict) and manifest.get("schema") == CAPTURE_SCHEMA, "invalid capture schema")
    valid_uuid(manifest.get("capture_id"), "capture_id")
    claims = validate_claims(manifest.get("caller_claims"))
    require(manifest.get("conversation_completeness") == "unverified_caller_claim",
            "capture cannot verify conversation completeness")
    require(manifest.get("status") in ("pending", "captured"), "invalid capture status")
    if manifest["status"] == "pending":
        require(manifest.get("source") is None and manifest.get("byte_coverage") is None
                and manifest.get("format") is None, "pending capture must contain no invented source")
        require(inventory(root) == ["manifest.json"], "unexpected pending capture files")
        verified_bytes = 0
    else:
        source = manifest.get("source")
        require(isinstance(source, dict), "missing capture source")
        require(manifest.get("format") in ("raw", "jsonl"), "invalid capture format")
        filename = "source.txt" if manifest["format"] == "raw" else "source.jsonl"
        require(source.get("path") == filename and source.get("encoding") == "utf-8", "invalid capture source path/encoding")
        data = read_bytes(rooted(root, filename))
        require(source.get("sha256") == sha(data) and source.get("size_bytes") == len(data), "capture source hash/size mismatch")
        require(json_bytes(manifest.get("byte_coverage")) == json_bytes(source_layout(data, manifest["format"])),
                "capture byte coverage mismatch")
        require(inventory(root) == sorted(["manifest.json", filename]), "unexpected capture files")
        verified_bytes = len(data)
    return {"status": manifest["status"], "capture": str(root), "capture_id": manifest["capture_id"],
            "manifest_sha256": sha(manifest_bytes), "source_sha256": (manifest.get("source") or {}).get("sha256"),
            "exact_bytes_verified": verified_bytes, "conversation_completeness": "unverified_caller_claim",
            "declared_gaps": claims.get("gaps", []), "manifest": manifest,
            "semantic_review": "not_performed"}


def selection_input(root_value, manifest_file, selected, side):
    require(bool(root_value) != bool(manifest_file), f"provide either --{side} or --{side}-manifest")
    identity = {}
    protected = []
    if manifest_file:
        manifest_path = checked_absolute(manifest_file)
        raw = read_bytes(manifest_path)
        declaration = parse_json(raw, manifest_path)
        require(isinstance(declaration, dict) and declaration.get("schema") == SELECTION_SCHEMA, "invalid selection manifest schema")
        require(isinstance(declaration.get("root"), str) and declaration["root"], "selection manifest needs root")
        root_value = manifest_path.parent / declaration["root"]
        selected = list(selected) + strings(declaration.get("selected_paths"), "selected_paths")
        omitted = strings(declaration.get("omitted_scope"), "omitted_scope", allow_empty=False)
        identity = {"selection_manifest": str(manifest_path), "selection_manifest_sha256": sha(raw)}
        protected.append(manifest_path)
    else:
        omitted = ["All paths outside selected_paths; no claim of whole-root or whole-world coverage."]
    root = checked_absolute(root_value, directory=True)
    selected = list(dict.fromkeys(selected))
    require(len({value.casefold() for value in selected}) == len(selected), "case-colliding selections")
    for relative in selected:
        require(route(relative).suffix.lower() == ".md", "audit selections must name Markdown source files")
    return root, selected, omitted, identity, protected


def document(root, relative, expected_sha256=None):
    try:
        return read_source.load_document(root, relative, expected_sha256=expected_sha256)
    except read_source.SourceError as exc:
        raise EvidenceError(str(exc)) from None


def prepare_audit(prior, current, capture, output, selected=(), prior_selected=(), current_selected=(),
                  prior_manifest=None, current_manifest=None, save_boundary=None):
    selections = {}
    protected = []
    for side, root_value, manifest_file, local in (
            ("prior", prior, prior_manifest, prior_selected),
            ("current", current, current_manifest, current_selected)):
        selections[side] = selection_input(root_value, manifest_file, list(selected) + list(local), side)
        root, _, _, _, other_protected = selections[side]
        protected.extend([root, *other_protected])
    captured = check_capture(capture)
    capture_root = checked_absolute(capture, directory=True)
    protected.append(capture_root)
    output_path(output, protected)
    files = {}
    sources = []
    roots = {}
    for side, (root, paths, omitted, identity, _) in selections.items():
        root_ids = set()
        for relative in paths:
            source = document(root, relative)
            root_ids.add(source["root_id"])
            frozen_path = f"sources/{side}/{relative}"
            data = source["text"].encode("utf-8")
            require(sha(data) == source["sha256"], "reader/source byte identity mismatch")
            files[frozen_path] = data
            sources.append({"side": side, "path": relative, "root_id": source["root_id"],
                            "sha256": source["sha256"], "size_bytes": source["source_size_bytes"],
                            "line_count": len(source["lines"]), "snapshot": frozen_path})
        require(len(root_ids) <= 1, "reader returned inconsistent root identities")
        roots[side] = {"original_root": str(root), "root_id": next(iter(root_ids), None),
                       "selected_paths": paths, "omitted_scope": omitted, "coverage": "scoped", **identity}
    require(sources, "select at least one Markdown source; scope must be explicit")
    for relative in inventory(capture_root):
        files[f"capture/{relative}"] = read_bytes(rooted(capture_root, relative))
    require(sha(files["capture/manifest.json"]) == captured["manifest_sha256"], "capture changed while freezing")
    # Re-read selected inputs before creating output; indexes never supply source bytes.
    for source in sources:
        document(selections[source["side"]][0], source["path"], source["sha256"])
    require(check_capture(capture_root)["manifest_sha256"] == captured["manifest_sha256"], "capture changed while freezing")
    selected_prior = set(roots["prior"]["selected_paths"])
    selected_current = set(roots["current"]["selected_paths"])
    manifest = {"schema": BUNDLE_SCHEMA, "bundle_id": str(uuid.uuid4()),
                "created_at": datetime.now(timezone.utc).isoformat(), "roots": roots, "sources": sources,
                "selection_difference": {"prior_only": sorted(selected_prior - selected_current),
                                         "current_only": sorted(selected_current - selected_prior),
                                         "meaning": "Selection differences do not establish file creation or deletion."},
                "capture": {"capture_id": captured["capture_id"], "manifest_sha256": captured["manifest_sha256"],
                            "source_sha256": captured["source_sha256"], "status": captured["status"]},
                "files": {relative: sha(data) for relative, data in sorted(files.items())},
                "coverage": "scoped", "semantic_review": "not_performed"}
    if save_boundary is not None:
        manifest["save_binding"] = make_save_binding(save_boundary, sources, files, captured,
                                                    selections["prior"][0], selections["current"][0])
    files["bundle.json"] = json_bytes(manifest)
    destination = write_package(output, files, protected)
    return check_bundle(destination)


def check_bundle(bundle):
    root = checked_absolute(bundle, directory=True)
    raw = read_bytes(rooted(root, "bundle.json"))
    manifest = parse_json(raw, "bundle manifest")
    require(isinstance(manifest, dict) and manifest.get("schema") == BUNDLE_SCHEMA, "invalid audit bundle schema")
    valid_uuid(manifest.get("bundle_id"), "bundle_id")
    require(manifest.get("coverage") == "scoped" and manifest.get("semantic_review") == "not_performed",
            "bundle cannot establish complete coverage or semantic conclusions")
    files = manifest.get("files")
    require(isinstance(files, dict) and files, "bundle missing files map")
    require("bundle.json" not in files, "bundle manifest cannot self-hash")
    for relative, expected in files.items():
        require(isinstance(expected, str) and HEX.fullmatch(expected), "invalid file digest")
        require(sha(read_bytes(rooted(root, relative))) == expected, f"frozen source hash mismatch: {relative}")
    require(inventory(root) == sorted(["bundle.json", *files]), "unexpected or missing audit bundle files")
    capture = check_capture(rooted(root, "capture"))
    expected_capture = {key: capture[key] for key in ("capture_id", "manifest_sha256", "source_sha256", "status")}
    require(manifest.get("capture") == expected_capture, "bundle capture identity mismatch")
    sources = manifest.get("sources")
    require(isinstance(sources, list) and sources, "bundle needs source entries")
    seen = set()
    indexed_files = {"capture/" + path for path in inventory(root / "capture")}
    for source in sources:
        require(isinstance(source, dict) and source.get("side") in ("prior", "current"), "invalid source side")
        side, relative = source["side"], source.get("path")
        route(relative)
        key = (side, relative.casefold())
        require(key not in seen, "duplicate source reference")
        seen.add(key)
        snapshot = f"sources/{side}/{relative}"
        require(source.get("snapshot") == snapshot and source.get("sha256") == files.get(snapshot),
                "source snapshot reference mismatch")
        doc = document(root, snapshot, source["sha256"])
        require(source.get("size_bytes") == doc["source_size_bytes"]
                and source.get("line_count") == len(doc["lines"]), "source size/line coverage mismatch")
        indexed_files.add(snapshot)
    require(indexed_files == set(files), "unindexed bundle file")
    roots = manifest.get("roots")
    require(isinstance(roots, dict) and set(roots) == {"prior", "current"}, "bundle missing explicit prior/current roots")
    for side, identity in roots.items():
        require(isinstance(identity, dict) and identity.get("coverage") == "scoped", "invalid root scope")
        expected_paths = [source["path"] for source in sources if source["side"] == side]
        require(identity.get("selected_paths") == expected_paths, "selected-path coverage mismatch")
        strings(identity.get("omitted_scope"), "root omitted_scope", allow_empty=False)
        require(all(source.get("root_id") == identity.get("root_id") for source in sources if source["side"] == side),
                "source root identity mismatch")
    prior_paths, current_paths = set(roots["prior"]["selected_paths"]), set(roots["current"]["selected_paths"])
    require(manifest.get("selection_difference") == {
        "prior_only": sorted(prior_paths - current_paths), "current_only": sorted(current_paths - prior_paths),
        "meaning": "Selection differences do not establish file creation or deletion."}, "selection difference coverage mismatch")
    if "save_binding" in manifest:
        validate_save_binding(manifest["save_binding"], manifest, root, capture)
    return {"status": "frozen_inputs_verified", "bundle": str(root), "bundle_id": manifest["bundle_id"],
            "bundle_sha256": sha(raw), "manifest": manifest, "source_count": len(sources),
            "source_coverage": "scoped", "semantic_review": "not_performed"}


def source_references(bundle):
    manifest = bundle["manifest"]
    refs = [{"source": value["side"], "path": value["path"], "sha256": value["sha256"]}
            for value in manifest["sources"]]
    if manifest["capture"]["status"] == "captured":
        captured = check_capture(Path(bundle["bundle"]) / "capture")
        refs.append({"source": "capture", "path": captured["manifest"]["source"]["path"],
                     "sha256": captured["source_sha256"]})
    return refs


def report_template(bundle):
    frozen = check_bundle(bundle)
    captured = check_capture(Path(frozen["bundle"]) / "capture")
    limitations = ["Only explicitly selected Markdown files and supplied capture bytes are frozen.",
                   "Conversation completeness and reviewer independence are caller claims."]
    limitations.extend(f"Caller-declared gap: {gap}" for gap in captured["declared_gaps"])
    if captured["status"] == "pending":
        limitations.append("Capture is pending; no conversation source bytes are available.")
    result = {"schema": REPORT_SCHEMA, "report_id": str(uuid.uuid4()), "review_status": "pending",
            "reviewer": {"kind": "unspecified", "identifier": "", "independence": "unknown"},
            "bundle_id": frozen["bundle_id"], "bundle_sha256": frozen["bundle_sha256"],
            "capture": frozen["manifest"]["capture"],
            "source_coverage": {"status": "unobserved", "indexed_sources": source_references(frozen),
                                "reviewed_sources": [], "limitations": limitations},
            "record_consistency": {"status": "not_reviewed", "summary": "", "citations": []},
            "unresolved_facts": [], "unresolved_instructions": [], "findings": [],
            "repair_eligibility": {"status": "not_requested", "evidentiary_clarity": False,
                                   "consequence_containment": False, "summary": "", "authority_citations": []},
            "evidence_boundaries": {"conversation_completeness": "caller_claim_only",
                                    "source_scope": "selected_paths_only",
                                    "semantic_truth": "not_established_by_checker"}}
    if "save_binding" in frozen["manifest"]:
        result["save_review"] = {
            "binding_sha256": sha(json_bytes(frozen["manifest"]["save_binding"])),
            "review_covered_through": None,
            "source_coherence": {"status": "not_assessed", "summary": "", "citations": []}}
    return result


def ref_key(value):
    require(isinstance(value, dict), "source reference must be an object")
    require(value.get("source") in ("prior", "current", "capture"), "invalid citation source")
    route(value.get("path"))
    require(isinstance(value.get("sha256"), str) and HEX.fullmatch(value["sha256"]), "invalid source reference hash")
    return value["source"], value["path"], value["sha256"]


def citation(bundle, source, path, start_line, end_line):
    """Extract an original-line citation; no review or delivery claim is made."""
    route(path)
    require(source in ("prior", "current", "capture"), "invalid citation source")
    frozen = check_bundle(bundle)
    matches = [ref for ref in source_references(frozen)
               if ref["source"] == source and ref["path"] == path]
    require(len(matches) == 1, "citation source is not available in this frozen bundle")
    ref = matches[0]
    relative = f"capture/{path}" if source == "capture" else f"sources/{source}/{path}"
    original = document(Path(frozen["bundle"]), relative, ref["sha256"])
    lines = original["lines"]
    require(type(start_line) is int and type(end_line) is int
            and 1 <= start_line <= end_line <= len(lines), "invalid original line range")
    binding = frozen["manifest"].get("save_binding")
    if source == "capture" and binding and binding["state_saved_through"]["basis"] == "capture_lines":
        require(end_line <= binding["state_saved_through"]["end_line"],
                "citation uses play after selected save boundary")
    return {**ref, "start_line": start_line, "end_line": end_line,
            "quote": "".join(lines[start_line - 1:end_line])}


def check_report(bundle, report_file, delivery_receipt=None):
    frozen = check_bundle(bundle)
    captured = check_capture(Path(frozen["bundle"]) / "capture")
    report_bytes = read_bytes(report_file)
    report = parse_json(report_bytes, report_file)
    require(isinstance(report, dict) and report.get("schema") == REPORT_SCHEMA, "invalid report schema")
    valid_uuid(report.get("report_id"), "report_id")
    require(report.get("bundle_id") == frozen["bundle_id"]
            and report.get("bundle_sha256") == frozen["bundle_sha256"], "stale report bundle reference")
    require(report.get("capture") == frozen["manifest"]["capture"], "stale report capture reference")
    require(report.get("review_status") in ("pending", "completed"), "invalid review status")
    reviewer = report.get("reviewer")
    require(isinstance(reviewer, dict) and reviewer.get("kind") in ("unspecified", "model", "human")
            and isinstance(reviewer.get("identifier"), str)
            and reviewer.get("independence") in ("unknown", "same_context", "claimed_independent"), "invalid reviewer declaration")
    if report["review_status"] == "completed":
        require(reviewer["kind"] != "unspecified" and reviewer["identifier"].strip(), "completed report needs declared reviewer")
    require(report.get("evidence_boundaries") == {
        "conversation_completeness": "caller_claim_only", "source_scope": "selected_paths_only",
        "semantic_truth": "not_established_by_checker"}, "report must preserve evidence boundaries")
    references = source_references(frozen)
    expected_refs = {ref_key(ref) for ref in references}
    docs = {}
    for ref in references:
        relative = f"capture/{ref['path']}" if ref["source"] == "capture" else f"sources/{ref['source']}/{ref['path']}"
        docs[ref_key(ref)] = document(Path(frozen["bundle"]), relative, ref["sha256"])
    cited = set()
    quote_count = 0

    def citations(values, label, required=False, track=True):
        nonlocal quote_count
        require(isinstance(values, list) and (values or not required), f"{label} needs citations")
        keys = set()
        for citation in values:
            key = ref_key(citation)
            require(key in expected_refs, f"unknown or stale citation source in {label}")
            start, end = citation.get("start_line"), citation.get("end_line")
            lines = docs[key]["lines"]
            require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
                    f"invalid original line range in {label}")
            binding = frozen["manifest"].get("save_binding")
            if key[0] == "capture" and binding and binding["state_saved_through"]["basis"] == "capture_lines":
                require(end <= binding["state_saved_through"]["end_line"], "citation uses play after selected save boundary")
            require(isinstance(citation.get("quote"), str)
                    and citation["quote"] == "".join(lines[start - 1:end]), f"quote does not match original lines in {label}")
            keys.add(key)
            if track:
                cited.add(key)
                quote_count += 1
        return keys

    delivered = set()
    fully_delivered = set()
    receipt_hash = None
    if delivery_receipt:
        receipt_bytes = read_bytes(delivery_receipt)
        receipt_hash = sha(receipt_bytes)
        try:
            receipt = parse_json(receipt_bytes, delivery_receipt)
            records = [receipt]
        except EvidenceError:
            records = [parse_json(line, "delivery receipt JSONL") for line in receipt_bytes.splitlines() if line.strip()]
        require(records, "empty delivery receipt")
        for receipt in records:
            require(isinstance(receipt, dict), "delivery receipt must be an object")
            if receipt.get("schema") == RECEIPT_SCHEMA:
                require(receipt.get("bundle_id") == frozen["bundle_id"]
                        and receipt.get("bundle_sha256") == frozen["bundle_sha256"], "stale delivery receipt")
                delivered |= citations(receipt.get("passages"), "delivery receipt", track=False)
                for passage in receipt["passages"]:
                    key = ref_key(passage)
                    if passage["start_line"] == 1 and passage["end_line"] == len(docs[key]["lines"]):
                        fully_delivered.add(key)
            else:
                require(receipt.get("kind") == "tool_generated_delivery_receipt"
                        and receipt.get("receipt_version") == 1 and receipt.get("producer") == "TOOLS/read_source.py",
                        "invalid delivery receipt schema")
                passage = receipt.get("passage")
                require(isinstance(passage, dict), "reader receipt missing passage")
                matches = [key for key, doc in docs.items() if all(
                    passage.get(field) == doc[field] for field in ("root_id", "path", "sha256"))]
                require(len(matches) == 1, "reader receipt is not for this frozen bundle source")
                key = matches[0]
                selectors = {"max_chars": passage.get("max_chars")}
                if passage.get("selection_kind") == "section":
                    selectors["section_id"] = passage.get("section_id")
                elif passage.get("selection_kind") == "line_span":
                    selectors.update(start_line=passage.get("start_line"), end_line=passage.get("end_line"))
                else:
                    require(passage.get("selection_kind") == "whole_file", "invalid receipt selection kind")
                try:
                    expected_passage = read_source.select_passage(docs[key], **selectors)
                except read_source.SourceError as exc:
                    raise EvidenceError(str(exc)) from None
                require(passage == expected_passage, "reader receipt passage/hash/coverage mismatch")
                if passage["returned_char_count"] or passage["source_complete"]:
                    delivered.add(key)
                if passage["source_complete"]:
                    fully_delivered.add(key)
    coverage = report.get("source_coverage")
    require(isinstance(coverage, dict) and coverage.get("status") in ("unobserved", "partial", "scoped"),
            "source coverage must be unobserved, partial or scoped; never assumed complete")
    require(isinstance(coverage.get("indexed_sources"), list)
            and {ref_key(ref) for ref in coverage["indexed_sources"]} == expected_refs
            and len(coverage["indexed_sources"]) == len(expected_refs), "indexed source coverage mismatch")
    require(isinstance(coverage.get("reviewed_sources"), list), "reviewed_sources must be a list")
    reviewed = {ref_key(ref) for ref in coverage["reviewed_sources"]}
    require(reviewed <= expected_refs and len(reviewed) == len(coverage["reviewed_sources"]), "unknown, stale or duplicate reviewed source")
    strings(coverage.get("limitations"), "source coverage limitations", allow_empty=False)
    consistency = report.get("record_consistency")
    require(isinstance(consistency, dict) and consistency.get("status") in (
        "not_reviewed", "consistent", "inconsistent", "undetermined") and isinstance(consistency.get("summary"), str),
        "invalid record_consistency; this field is separate from unresolved facts/instructions")
    citations(consistency.get("citations"), "record consistency",
              required=consistency["status"] in ("consistent", "inconsistent"))
    for category in ("unresolved_facts", "unresolved_instructions"):
        require(isinstance(report.get(category), list), f"{category} must be a separate list")
        for item in report[category]:
            require(isinstance(item, dict) and isinstance(item.get("summary"), str) and item["summary"].strip(),
                    f"{category} entries need a short summary")
            basis = item.get("basis", "source_text")
            require(basis in ("source_text", "caller_declared_gap", "outside_selected_scope", "pending_capture"),
                    f"invalid evidence basis in {category}")
            require(basis != "caller_declared_gap" or bool(captured["declared_gaps"]),
                    "no caller-declared gap supports this entry")
            require(basis != "pending_capture" or captured["status"] == "pending", "capture is not pending")
            citations(item.get("citations"), category, required=basis == "source_text")
    findings = report.get("findings")
    require(isinstance(findings, list), "findings must be a list")
    ids = set()
    for finding in findings:
        require(isinstance(finding, dict) and isinstance(finding.get("id"), str) and finding["id"].strip()
                and finding["id"] not in ids, "finding requires a unique id")
        ids.add(finding["id"])
        require(finding.get("category") in ("record_consistency", "unresolved_fact", "unresolved_instruction")
                and isinstance(finding.get("summary"), str) and finding["summary"].strip(), "invalid finding category/summary")
        require(finding.get("decision") in ("observation", "correction", "rewind"), "invalid finding decision")
        citations(finding.get("citations"), "finding", required=True)
        citations(finding.get("authority_citations"), "finding authority",
                  required=finding["decision"] in ("correction", "rewind"))
    repair = report.get("repair_eligibility")
    require(isinstance(repair, dict) and repair.get("status") in ("not_requested", "ineligible", "eligible")
            and type(repair.get("evidentiary_clarity")) is bool
            and type(repair.get("consequence_containment")) is bool
            and isinstance(repair.get("summary"), str), "invalid repair_eligibility")
    citations(repair.get("authority_citations"), "repair authority", required=repair["status"] == "eligible")
    require(repair["status"] != "eligible" or (repair["evidentiary_clarity"] and repair["consequence_containment"]),
            "repair requires both evidentiary clarity AND consequence containment")
    require(not any(finding["decision"] in ("correction", "rewind") for finding in findings)
            or repair["status"] != "not_requested", "correction/rewind finding requires an explicit repair eligibility assessment")
    require(reviewed <= (cited | delivered), "reviewed source has no matching citation or delivery receipt")
    require(coverage["status"] != "unobserved" or not reviewed, "unobserved coverage cannot declare reviewed sources")
    require(coverage["status"] != "scoped" or reviewed == expected_refs, "scoped review omits selected inputs")
    require(coverage["status"] != "partial" or bool(reviewed), "partial review needs an observed source")
    if consistency["status"] == "consistent":
        require(coverage["status"] == "scoped" and reviewed == expected_refs,
                "consistent selected records require declared review of all selected inputs")
        require(frozen["manifest"]["capture"]["status"] == "captured", "pending capture cannot support consistent records")
    if report["review_status"] == "completed":
        require(consistency["status"] != "not_reviewed" and consistency["summary"].strip(), "completed report needs record assessment")
    else:
        require(consistency["status"] == "not_reviewed" and repair["status"] != "eligible", "pending report cannot declare review/repair success")
    if repair["status"] == "eligible":
        require(report["review_status"] == "completed" and bool(reviewed), "unreviewed evidence cannot authorize repair")
    if "save_binding" in frozen["manifest"]:
        review = report.get("save_review")
        binding = frozen["manifest"]["save_binding"]
        require(isinstance(review, dict) and set(review) == {
            "binding_sha256", "review_covered_through", "source_coherence"}, "missing save review declaration")
        require(review["binding_sha256"] == sha(json_bytes(binding)), "stale save binding reference")
        covered = review["review_covered_through"]
        require(covered is None or covered == binding["state_saved_through"], "review boundary differs from selected stop")
        if covered is not None:
            require(report["review_status"] == "completed" and binding["state_saved_through"]["basis"] == "capture_lines",
                    "pending review or unavailable capture cannot claim reviewed-through coverage")
            require(coverage["status"] == "scoped", "reviewed-through requires all selected sources declared reviewed")
        if consistency["status"] == "consistent":
            require(covered is not None, "consistent save needs explicit reviewed-through scope")
        coherence = review["source_coherence"]
        require(isinstance(coherence, dict) and set(coherence) == {"status", "summary", "citations"}
                and coherence["status"] in ("not_assessed", "no_conflict_observed", "conflict_observed", "undetermined")
                and isinstance(coherence["summary"], str), "invalid source coherence declaration")
        if report["review_status"] == "pending":
            require(coherence["status"] == "not_assessed", "pending review cannot assess source coherence")
        if coherence["status"] != "not_assessed":
            require(bool(coherence["summary"].strip()), "source coherence assessment needs explanation")
        citations(coherence["citations"], "source coherence", required=coherence["status"] == "conflict_observed")
        # Matching a contradictory source is not a clean review, even if copying was exact.
        require(coherence["status"] != "conflict_observed" or consistency["status"] != "consistent",
                "source conflict must remain unresolved, not a consistent-save badge")
    elif "save_review" in report:
        raise EvidenceError("save review declaration requires a save-bound bundle")
    return {"status": "report_structure_verified" if report["review_status"] == "completed" else "pending_review",
            "report_sha256": sha(report_bytes), "bundle_id": frozen["bundle_id"], "bundle_sha256": frozen["bundle_sha256"],
            "capture_manifest_sha256": frozen["manifest"]["capture"]["manifest_sha256"],
            "capture_coverage": {"status": captured["status"], "exact_bytes_verified": captured["exact_bytes_verified"],
                                 "declared_gaps": captured["declared_gaps"], "conversation_completeness": "unverified_caller_claim"},
            "verified_operations": {"frozen_file_hashes": True, "report_references": True,
                                    "exact_original_line_quotes": quote_count, "eligibility_declarations_consistent": True},
            "source_coverage": {"indexed": len(expected_refs), "receipt_delivered": len(delivered),
                                "receipt_fully_delivered": len(fully_delivered),
                                "citation_observed": len(cited), "declared_reviewed": len(reviewed),
                                "scope": "selected_paths_only", "review_not_verified": True},
            "delivery_receipt_sha256": receipt_hash, "reviewer_identity_and_independence": "unverified_declarations",
            "semantic_review": "not_performed", "repair_authorized": False,
            "limitation": "Hash, quote and schema checks establish byte/reference consistency, not semantic truth, actual reading, independent review, or permission to repair."}


# Save-review support is optional. It certifies selected bytes and references, never
# source meaning, consent, chronology, or completeness of the caller's write set.
SAVE_BOUNDARY_SCHEMA = "rpg-save-review-boundary-v1"
SAVE_BINDING_SCHEMA = "rpg-save-review-binding-v1"
SAVE_PATH = "INSTANCE/CURRENT_SAVE.md"
SAVE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


def save_review_plan(policy="off", kind="checkpoint", source_review=False):
    """Pure planning over an already accepted policy; cannot grant permission."""
    require(policy in ("off", "tiered", "every-save"), "unknown save review policy")
    require(kind in ("checkpoint", "close"), "unknown save kind")
    require(type(source_review) is bool, "source_review must be boolean")
    level = "source" if source_review or policy == "every-save" or (policy == "tiered" and kind == "close") else "lightweight"
    return {"status": "planned", "policy": policy, "save_kind": kind, "review_level": level,
            "capture_required_for_source_review": level == "source", "semantic_review": "not_performed",
            "repair_authorized": False, "policy_acceptance": "caller_responsibility",
            "limitation": "Lightweight is not transcript-grounded semantic review. A source reviewer remains fallible."}


def _save_fields(data):
    """Read the existing Field/Value table without treating unrelated prose as metadata."""
    text = data.decode("utf-8")
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if re.fullmatch(r"\|\s*Field\s*\|\s*Value\s*\|", line.strip())]
    require(len(starts) == 1, "save needs exactly one Field/Value table")
    fields = {}
    for line in lines[starts[0] + 1:]:
        if not line.strip().startswith("|"):
            break
        cells = [v.strip() for v in line.strip().strip("|").split("|")]
        require(len(cells) == 2, "malformed save metadata row")
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        key, value = cells
        require(key not in fields and value, "duplicate or blank save metadata")
        fields[key] = value
    names = ("campaign_id", "save_id", "save_rev", "save_parent", "commit_kind", "archive_ref", "evidence_through")
    require(all(name in fields for name in names), "missing save identity/evidence metadata")
    require(all(SAVE_ID.fullmatch(fields[key]) for key in ("campaign_id", "save_id", "save_parent", "evidence_through")),
            "unsafe save identity")
    require(fields["campaign_id"] != "none" and fields["save_id"] != "none", "save audit requires a bound campaign")
    require(re.fullmatch(r"[0-9]+", fields["save_rev"]) is not None, "invalid save revision")
    require(fields["commit_kind"] in ("bind", "checkpoint", "close"), "invalid bound save kind")
    require((fields["archive_ref"] == "none") == (fields["evidence_through"] == "none"), "incomplete archive boundary")
    if fields["archive_ref"] != "none":
        route(fields["archive_ref"])
    result = {key: fields[key] for key in names}
    result["save_rev"] = int(result["save_rev"])
    return result


def _save_transition(prior, current):
    require(prior["campaign_id"] == current["campaign_id"], "save campaign mismatch")
    require(current["save_parent"] == prior["save_id"] and current["save_id"] != prior["save_id"]
            and current["save_rev"] == prior["save_rev"] + 1, "save parent/id/revision mismatch")
    require(current["commit_kind"] in ("checkpoint", "close"), "review supports checkpoint or close, not a new bind")
    if current["commit_kind"] == "checkpoint":
        require(all(prior[key] == current[key] for key in ("archive_ref", "evidence_through")),
                "checkpoint changed archived evidence boundary")
    else:
        require(current["evidence_through"] == current["save_id"] and current["archive_ref"] != "none"
                and current["archive_ref"] != prior["archive_ref"], "full save needs its own new archive boundary")


def _optional_bytes(root, relative):
    """Absence is allowed; unsafe/symlinked ancestors are not mistaken for absence."""
    path = root
    for part in route(relative).parts:
        require(path.is_dir(), "source ancestor must be a directory")
        path /= part
        if not os.path.lexists(path):
            return None
        inspect(path)
    return read_bytes(path)


def _path_list(value, label):
    strings(value, label)
    require(len({path.casefold() for path in value}) == len(value), f"duplicate/case-colliding {label}")
    for path in value:
        require(route(path).suffix.lower() == ".md", f"{label} must name Markdown files")
    return value


def save_diff(prior, current, selected=()):
    """No capture, model call or file writes. Selected files only, not a full validator."""
    before = checked_absolute(prior, directory=True)
    after = checked_absolute(current, directory=True)
    paths = sorted(set([SAVE_PATH, *selected]))
    _path_list(paths, "selected paths")
    old = _save_fields(read_bytes(rooted(before, SAVE_PATH)))
    new = _save_fields(read_bytes(rooted(after, SAVE_PATH)))
    _save_transition(old, new)
    changes = []
    for path in paths:
        a, b = _optional_bytes(before, path), _optional_bytes(after, path)
        require(a is not None or b is not None, f"selected path absent on both sides: {path}")
        changes.append({"path": path, "prior_sha256": sha(a) if a is not None else None,
                        "current_sha256": sha(b) if b is not None else None,
                        "change": "unchanged" if a == b else "added" if a is None else "removed" if b is None else "changed"})
    return {"status": "selected_diff_verified", "prior_save": old, "current_save": new, "files": changes,
            "history_archived_through": new["evidence_through"], "state_saved_through": "not_observed",
            "review_covered_through": None, "review_level": "lightweight", "semantic_review": "not_performed",
            "repair_authorized": False, "limitation": "Selected hashes and save identity only; no action-completion, source-meaning or omission guarantee."}


def _validate_stop(stop, captured):
    require(isinstance(stop, dict), "state_saved_through must be an object")
    if stop.get("basis") == "unavailable":
        require(set(stop) == {"basis", "description"} and isinstance(stop["description"], str)
                and bool(stop["description"].strip()), "unavailable stop needs an honest source limitation")
        return
    require(set(stop) == {"basis", "capture_sha256", "start_line", "end_line", "description"}
            and stop["basis"] == "capture_lines", "invalid state stopping-point schema")
    require(captured["status"] == "captured" and stop["capture_sha256"] == captured["source_sha256"],
            "state boundary has missing or different capture")
    first, last = stop["start_line"], stop["end_line"]
    require(type(first) is int and type(last) is int and 1 <= first <= last <= captured["manifest"]["byte_coverage"]["source_line_count"],
            "state boundary lines are outside capture")
    require(isinstance(stop["description"], str) and bool(stop["description"].strip()), "state boundary needs scope description")


def make_save_binding(request, sources, files, captured, prior_root, current_root):
    require(isinstance(request, dict) and set(request) == {
        "schema", "state_saved_through", "write_paths", "removed_paths", "limitations"}
        and request["schema"] == SAVE_BOUNDARY_SCHEMA, "invalid save boundary request")
    _validate_stop(request["state_saved_through"], captured)
    strings(request["limitations"], "boundary limitations")
    writes = _path_list(request["write_paths"], "write_paths")
    removed = _path_list(request["removed_paths"], "removed_paths")
    require(SAVE_PATH in writes and not set(writes) & set(removed), "write set must include current save and exclude removals")
    indexed = {(s["side"], s["path"]): s for s in sources}
    require(all((side, SAVE_PATH) in indexed for side in ("prior", "current")), "select prior and current CURRENT_SAVE")
    old = _save_fields(files[indexed[("prior", SAVE_PATH)]["snapshot"]])
    new = _save_fields(files[indexed[("current", SAVE_PATH)]["snapshot"]])
    _save_transition(old, new)
    require(all(("current", path) in indexed for path in writes), "write path is outside frozen current selection")
    for path in removed:
        require(("prior", path) in indexed and ("current", path) not in indexed, "removal needs prior-only selected source")
        require(_optional_bytes(current_root, path) is None, "declared removed path still exists in proposed save")
    # Never equate every prior-only selection with a deletion. Explicit removals only.
    for source in sources:
        if source["side"] != "current":
            continue
        previous = indexed.get(("prior", source["path"]))
        if previous and source["sha256"] != previous["sha256"]:
            require(source["path"] in writes, "changed selected record omitted from write_paths")
    return {"schema": SAVE_BINDING_SCHEMA, "prior_save": old, "current_save": new,
            "state_saved_through": request["state_saved_through"],
            "history_archived_through": {"evidence_through": new["evidence_through"], "archive_ref": new["archive_ref"]},
            "write_paths": writes, "removed_paths": removed, "limitations": request["limitations"],
            "scope": "selected_paths_only", "boundary_and_write_scope": "caller_declared_not_semantically_verified"}


def validate_save_binding(binding, manifest, root, captured):
    require(isinstance(binding, dict) and set(binding) == {
        "schema", "prior_save", "current_save", "state_saved_through", "history_archived_through", "write_paths",
        "removed_paths", "limitations", "scope", "boundary_and_write_scope"}, "invalid save binding fields")
    require(binding["schema"] == SAVE_BINDING_SCHEMA and binding["scope"] == "selected_paths_only"
            and binding["boundary_and_write_scope"] == "caller_declared_not_semantically_verified", "invalid save binding scope")
    _validate_stop(binding["state_saved_through"], captured)
    strings(binding["limitations"], "binding limitations")
    indexed = {(s["side"], s["path"]): s for s in manifest["sources"]}
    for side in ("prior", "current"):
        require((side, SAVE_PATH) in indexed, "binding missing selected save identity")
        actual = _save_fields(read_bytes(rooted(root, indexed[(side, SAVE_PATH)]["snapshot"])))
        require(binding[side + "_save"] == actual, "binding does not match frozen save identity")
    _save_transition(binding["prior_save"], binding["current_save"])
    new = binding["current_save"]
    require(binding["history_archived_through"] == {"evidence_through": new["evidence_through"], "archive_ref": new["archive_ref"]},
            "binding archive boundary mismatch")
    writes = _path_list(binding["write_paths"], "write_paths")
    removed = _path_list(binding["removed_paths"], "removed_paths")
    require(SAVE_PATH in writes and not set(writes) & set(removed), "invalid bound write/removal set")
    require(all(("current", path) in indexed for path in writes), "unselected bound write")
    require(all(("prior", path) in indexed and ("current", path) not in indexed for path in removed), "invalid bound removal")
    for (side, path), source in indexed.items():
        previous = indexed.get(("prior", path))
        if side == "current" and previous and previous["sha256"] != source["sha256"]:
            require(path in writes, "changed selected record absent from bound write set")


def prepare_save_audit(prior, current, capture, output, boundary_file, selected=(), prior_selected=(), current_selected=()):
    boundary_path = checked_absolute(boundary_file)
    request_bytes = read_bytes(boundary_path)
    output_path(output, [boundary_path])
    request = parse_json(request_bytes, boundary_path)
    common = list(dict.fromkeys([SAVE_PATH, *selected]))
    return prepare_audit(prior, current, capture, output, common, prior_selected, current_selected, save_boundary=request)


def check_save_audit(bundle, report_file, saved, delivery_receipt=None, proposed=None):
    """Read-only final comparison. Success is byte matching, not semantic approval."""
    frozen = check_bundle(bundle)
    require("save_binding" in frozen["manifest"], "bundle is not save-bound")
    checked = check_report(bundle, report_file, delivery_receipt)
    report = read_json(report_file)
    require(sha(read_bytes(report_file)) == checked["report_sha256"], "report changed after reference check")
    binding = frozen["manifest"]["save_binding"]
    root = checked_absolute(saved, directory=True)
    matched = []
    before_publication = proposed is not None
    proposed = {} if proposed is None else proposed
    require(isinstance(proposed, dict) and all(isinstance(v, bytes) for v in proposed.values()),
            "proposed save must contain exact affected-file bytes")
    for source in frozen["manifest"]["sources"]:
        if before_publication and source["side"] == "prior":
            require(sha(read_bytes(rooted(root, source["path"]))) == source["sha256"],
                    f"prior review dependency changed before publication: {source['path']}")
        if source["side"] == "current":
            actual = proposed[source['path']] if source['path'] in proposed else read_bytes(rooted(root, source['path']))
            require(sha(actual) == source["sha256"],
                    f"saved file differs from reviewed version: {source['path']}")
            matched.append(source["path"])
    for path in binding["removed_paths"]:
        require(path not in proposed and _optional_bytes(root, path) is None, f"reviewed removal not applied: {path}")
    return {"status": "selected_saved_bytes_verified", "save_id": binding["current_save"]["save_id"],
            "matched_paths": matched, "removed_paths_verified": binding["removed_paths"],
            "state_saved_through": binding["state_saved_through"], "history_archived_through": binding["history_archived_through"],
            "review_covered_through": report["save_review"]["review_covered_through"],
            "review_status": report["review_status"], "record_consistency": report["record_consistency"]["status"],
            "source_coverage": report["source_coverage"], "source_coherence": report["save_review"]["source_coherence"],
            "limitations": binding["limitations"] + checked["capture_coverage"]["declared_gaps"],
            "report_sha256": checked["report_sha256"], "bundle_sha256": frozen["bundle_sha256"],
            "semantic_review": "not_performed_by_tool", "repair_authorized": False,
            "limitation": "Selected byte identity only. This does not publish a save, prove atomicity, authenticate a reviewer or establish semantic truth."}


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("metadata-template", help="Emit editable capture metadata with unknown completeness")
    capture = commands.add_parser("import", help="Copy exact supplied UTF-8 bytes into a new capture")
    capture.add_argument("--input", required=True, help="Real caller-supplied text file")
    capture.add_argument("--output", required=True, help="New capture folder (never overwritten)")
    capture.add_argument("--format", choices=("raw", "jsonl"), default="raw",
                         help="jsonl: one object per line, nonempty role and string content; other fields retained verbatim")
    capture.add_argument("--metadata", help="JSON caller claims: campaign_id, save_id, message_boundary {first,last,description}, conversation_complete, gaps, notes, source_description")
    pending = commands.add_parser("pending", help="Create metadata-only pending evidence without inventing source bytes")
    pending.add_argument("--output", required=True)
    pending.add_argument("--metadata")
    check = commands.add_parser("check", help="Verify capture or frozen audit bundle files and coverage")
    check.add_argument("package")
    prepare = commands.add_parser("prepare-audit", help="Freeze explicitly selected Markdown + capture outside input roots")
    for side in ("prior", "current"):
        group = prepare.add_mutually_exclusive_group(required=True)
        group.add_argument("--" + side, help="Explicit source root")
        group.add_argument("--" + side + "-manifest", help="rpg-source-selection-v1 JSON: root, selected_paths, omitted_scope")
        prepare.add_argument("--" + side + "-select", action="append", default=[], help="Relative Markdown file selected only from this root")
    prepare.add_argument("--select", action="append", default=[], help="Relative Markdown file selected from both roots; repeat as needed")
    prepare.add_argument("--capture", required=True)
    prepare.add_argument("--output", required=True)
    template = commands.add_parser("report-template", help="Emit a pending report for an external model/human to complete")
    template.add_argument("--bundle", required=True)
    quote = commands.add_parser("citation", help="Emit exact original lines from a verified frozen bundle; no review claim")
    quote.add_argument("--bundle", required=True)
    quote.add_argument("--source", choices=("prior", "current", "capture"), required=True)
    quote.add_argument("--path", required=True)
    quote.add_argument("--start-line", type=int, required=True)
    quote.add_argument("--end-line", type=int, required=True)
    report = commands.add_parser("check-report", help="Check an externally authored report; never certify semantic truth or perform repairs")
    report.add_argument("--bundle", required=True)
    report.add_argument("--report", required=True)
    report.add_argument("--delivery-receipt", help="Optional read_source.py JSONL receipts for bundle sources, or rpg-source-delivery-receipt-v1 JSON: bundle_id, bundle_sha256, passages (original-line citations)")
    plan = commands.add_parser("save-review-plan", help="Choose a declared review tier; no source or campaign access")
    plan.add_argument("--policy", choices=("off", "tiered", "every-save"), default="off")
    plan.add_argument("--kind", choices=("checkpoint", "close"), required=True)
    plan.add_argument("--source-review", action="store_true", help="Explicit one-off source review")
    diff = commands.add_parser("save-diff", help="Read-only selected-state diff and save identity checks; no semantic verdict")
    diff.add_argument("--prior", required=True)
    diff.add_argument("--current", required=True)
    diff.add_argument("--select", action="append", default=[])
    bound = commands.add_parser("prepare-save-audit", help="Freeze a source-review bundle tied to an exact proposed save")
    bound.add_argument("--prior", required=True)
    bound.add_argument("--current", required=True)
    bound.add_argument("--capture", required=True)
    bound.add_argument("--output", required=True)
    bound.add_argument("--boundary", required=True, help="rpg-save-review-boundary-v1 JSON; see ADMIN/EVIDENCE_AUDIT.md")
    bound.add_argument("--select", action="append", default=[])
    bound.add_argument("--prior-select", action="append", default=[])
    bound.add_argument("--current-select", action="append", default=[])
    finish = commands.add_parser("check-save-audit", help="Check review references and exact selected saved bytes; no campaign writes")
    finish.add_argument("--bundle", required=True)
    finish.add_argument("--report", required=True)
    finish.add_argument("--saved", required=True, help="Actual published or stable proposed save root to read back")
    finish.add_argument("--delivery-receipt")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "metadata-template":
            value = capture_metadata_template()
        elif args.command == "citation":
            value = citation(args.bundle, args.source, args.path, args.start_line, args.end_line)
        elif args.command == "import":
            value = import_capture(args.input, args.output, args.format, read_json(args.metadata) if args.metadata else None)
        elif args.command == "pending":
            value = pending_capture(args.output, read_json(args.metadata) if args.metadata else None)
        elif args.command == "check":
            root = checked_absolute(args.package, directory=True)
            value = check_bundle(root) if (root / "bundle.json").exists() else check_capture(root)
        elif args.command == "prepare-audit":
            value = prepare_audit(args.prior, args.current, args.capture, args.output, args.select,
                                  args.prior_select, args.current_select, args.prior_manifest, args.current_manifest)
        elif args.command == "report-template":
            value = report_template(args.bundle)
        elif args.command == "save-review-plan":
            value = save_review_plan(args.policy, args.kind, args.source_review)
        elif args.command == "save-diff":
            value = save_diff(args.prior, args.current, args.select)
        elif args.command == "prepare-save-audit":
            value = prepare_save_audit(args.prior, args.current, args.capture, args.output,
                                       args.boundary, args.select, args.prior_select, args.current_select)
        elif args.command == "check-save-audit":
            value = check_save_audit(args.bundle, args.report, args.saved, args.delivery_receipt)
        else:
            value = check_report(args.bundle, args.report, args.delivery_receipt)
        # ASCII JSON escapes round-trip all Unicode and original line endings even
        # when the host's redirected stdout uses a legacy Windows encoding.
        print(json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False))
        return 2 if value.get("status") == "pending_review" or (args.command == "check-save-audit" and value.get("review_status") == "pending") else 0
    except (EvidenceError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc), "semantic_review": "not_performed"}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
