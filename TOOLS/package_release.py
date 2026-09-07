#!/usr/bin/env python3
"""Package the committed, structurally valid, unbound RPG OS kit (stdlib + Git).

Local untracked files never enter the archive. Tracked changes are rejected.
Run from the repository: python -B TOOLS/package_release.py
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Iterator
import zipfile

sys.dont_write_bytecode = True

ROOT_FILES = {
    ".gitignore", "ARCHITECTURE.md", "CHANGELOG.md", "COMMANDS.md",
    "CONTRIBUTING.md", "INSTALLATION.md", "LICENSE", "MECHANICS.md",
    "QUICKSTART.md", "README.md", "SHARE.md", "VERIFICATION.md", "VERSION",
}
ROOT_DIRS = {".github", "ADMIN", "ARCHIVE", "ENGINE", "EVIDENCE", "INSTANCE", "MODULES", "OS", "TOOLS"}
SCOPED_FILES = {
    "EVIDENCE": {"README.md"},
    "MODULES": {"README.md", "_CONTRACT.md"},
    "ENGINE": {"_CONTRACT.md", "freeform.md"},
    "INSTANCE": {
        "_SCHEMA.md", "CURRENT_SAVE.md", "CAMPAIGN_CONTRACT.md", "BEARING.md",
        "SAFETY.md", "KNOWN.md", "NOW.md", "CAST_STATUS.md", "CORRECTIONS.md",
        "CHAR/README.md", "PEOPLE/README.md",
    },
    "ARCHIVE": {"_SCHEMA.md", "INDEX.md", "MESSAGES_LEDGER.md", "RELATION_LEDGER.md"},
}
PRIVATE_COMPONENTS = {
    ".git", ".work", ".release", ".codex", ".agents", "__pycache__",
    "recovery", "handover", "local_campaigns", "private-campaigns",
}
SAVE_VALUES = {
    "engine": "unbound", "module": "unbound", "pc_record": "none",
    "campaign_id": "none", "save_id": "none", "save_rev": "0",
    "save_parent": "none", "commit_kind": "unbound", "archive_ref": "none",
    "evidence_through": "none", "safety_state": "floor-only",
    "datetime": "none", "place": "none",
}
CONTRACT_VALUES = {
    "campaign_id": "none", "contract_id": "none", "contract_rev": "0",
    "contract_parent": "none", "status": "unbound", "module": "unbound",
}
VERSION_PATTERN = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
WINDOWS_RESERVED = re.compile(r"(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", re.IGNORECASE)


class PackageError(RuntimeError):
    pass


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise PackageError(f"Git failed: {detail}")
    return result.stdout


@contextmanager
def isolated_directory() -> Iterator[Path]:
    """Delete only the verified child created for this invocation."""
    parent = Path(tempfile.gettempdir()).resolve()
    child = Path(tempfile.mkdtemp(prefix="rpg-os-release-", dir=parent))
    try:
        yield child
    finally:
        resolved = child.resolve()
        if child.is_symlink() or resolved.parent != parent or not resolved.name.startswith("rpg-os-release-"):
            raise PackageError("Refusing temporary cleanup outside its verified directory")
        def remove_readonly(function, path, exception_info):
            target = Path(path)
            if (not isinstance(exception_info[1], PermissionError) or target.is_symlink()
                    or resolved not in target.resolve().parents):
                raise exception_info[1]
            # Git fixture objects can be read-only on Windows.
            target.chmod(target.stat().st_mode | stat.S_IWRITE)
            function(path)

        shutil.rmtree(resolved, onerror=remove_readonly)


def portable_path(raw: str) -> PurePosixPath:
    if not raw or raw.startswith("/") or "\\" in raw or "\x00" in raw:
        raise PackageError(f"Unsafe archive path: {raw!r}")
    parts = raw.rstrip("/").split("/")
    if any(part in {"", ".", ".."} or ":" in part or part.endswith((".", " "))
           or WINDOWS_RESERVED.fullmatch(part) or any(ord(char) < 32 for char in part)
           for part in parts):
        raise PackageError(f"Nonportable archive path: {raw!r}")
    return PurePosixPath(*parts)


def assert_public_paths(paths: set[str]) -> None:
    """Allow only the public kit layout, including empty campaign registers."""
    for raw in sorted(paths):
        path = portable_path(raw)
        if any(part.casefold() in PRIVATE_COMPONENTS for part in path.parts):
            raise PackageError(f"Private/output path is tracked: {raw}")
        if len(path.parts) == 1:
            if raw not in ROOT_FILES and not re.fullmatch(r"V[0-9]+(?:\.[0-9]+){1,2}_(?:CHANGES|TRIALS)\.md", raw):
                raise PackageError(f"Unexpected root file in fresh install: {raw}")
            continue
        top = path.parts[0]
        if top not in ROOT_DIRS:
            raise PackageError(f"Unexpected directory in fresh install: {raw}")
        if top in SCOPED_FILES and "/".join(path.parts[1:]) not in SCOPED_FILES[top]:
            raise PackageError(f"Campaign/module content is not part of a fresh install: {raw}")
        if path.suffix.casefold() in {".zip", ".tar", ".gz", ".pyc", ".pyo", ".bak", ".tmp"}:
            raise PackageError(f"Generated output is tracked: {raw}")


def tracked_manifest(root: Path, commit: str) -> dict[str, str]:
    manifest = {}
    folded = set()
    for entry in git(root, "ls-tree", "-rz", "--full-tree", commit).split(b"\x00"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, kind, object_id = metadata.decode("ascii").split()
        path = name.decode("utf-8")
        portable_path(path)
        if mode not in {"100644", "100755"} or kind != "blob":
            raise PackageError(f"Release cannot contain symlinks, submodules or special files: {path}")
        if path.casefold() in folded:
            raise PackageError(f"Case-colliding tracked path: {path}")
        folded.add(path.casefold())
        manifest[path] = object_id
    assert_public_paths(set(manifest))
    return manifest


def safe_extract(archive: Path, destination: Path, prefix: str) -> dict[str, bytes]:
    """Validate every ZIP entry before extracting; never follow ZIP symlinks."""
    destination = destination.resolve()
    entries = {}
    seen = set()
    with zipfile.ZipFile(archive) as source:
        for info in source.infolist():
            # orig_filename retains backslashes/NULs that ZipInfo may normalize.
            path = portable_path(info.orig_filename)
            if path.parts[0] != prefix or (len(path.parts) == 1 and not info.is_dir()):
                raise PackageError(f"ZIP entry is outside its single release folder: {info.filename}")
            folded = path.as_posix().casefold()
            if folded in seen:
                raise PackageError(f"Duplicate or case-colliding ZIP entry: {info.filename}")
            seen.add(folded)
            mode = info.external_attr >> 16
            file_type = stat.S_IFMT(mode)
            if file_type not in {0, stat.S_IFREG, stat.S_IFDIR} or stat.S_ISLNK(mode):
                raise PackageError(f"ZIP contains a link or special file: {info.filename}")
            if info.is_dir() != (file_type == stat.S_IFDIR) and file_type != 0:
                raise PackageError(f"ZIP entry type disagrees with its path: {info.filename}")
            target = destination.joinpath(*path.parts)
            if destination not in target.resolve().parents:
                raise PackageError(f"ZIP target escapes extraction directory: {info.filename}")
            if not info.is_dir():
                entries[path.as_posix()] = source.read(info)
        bad = source.testzip()
        if bad is not None:
            raise PackageError(f"ZIP CRC verification failed: {bad}")
    for path, data in entries.items():
        target = destination.joinpath(*PurePosixPath(path).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as output:
            output.write(data)
    return {path[len(prefix) + 1:]: data for path, data in entries.items()}


def assert_fields(root: Path, relative: str, expected: dict[str, str]) -> None:
    text = (root / relative).read_text(encoding="utf-8")
    for key, value in expected.items():
        matches = re.findall(r"^\|\s*" + re.escape(key) + r"\s*\|\s*([^|]*?)\s*\|\s*$", text, re.MULTILINE)
        if matches != [value]:
            raise PackageError(f"Fresh install requires {relative}: {key} = {value}")


def validate_fresh_install(root: Path) -> None:
    paths = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    assert_public_paths(paths)
    assert_fields(root, "INSTANCE/CURRENT_SAVE.md", SAVE_VALUES)
    assert_fields(root, "INSTANCE/CAMPAIGN_CONTRACT.md", CONTRACT_VALUES)
    bearing = root / "INSTANCE/BEARING.md"
    if bearing.exists():
        assert_fields(root, "INSTANCE/BEARING.md", {
            "campaign_id": "none", "base_save_id": "none", "base_contract_id": "none", "status": "none",
        })
        text = bearing.read_text(encoding="utf-8")
        for heading in ("Sources reviewed", "Provisional notes"):
            sections = re.findall(r"^## " + re.escape(heading) + r"\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
            if len(sections) != 1 or sections[0].strip() != "none":
                raise PackageError(f"Fresh install contains campaign review notes: {heading}")
    result = subprocess.run(
        [sys.executable, "-B", str(root / "TOOLS/validate.py"), "--root", str(root), "--json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PackageError(f"Frozen structural validator did not return JSON: {result.stderr.strip()}") from exc
    if result.returncode or report.get("structural", {}).get("result") != "PASS":
        findings = "; ".join(f"{item['code']}: {item['message']}" for item in report.get("findings", []))
        raise PackageError(f"Frozen fresh-install validation failed: {findings}")
    if not report.get("tree_stable_during_run") or not report.get("target_validator_matches_executed"):
        raise PackageError("Frozen structural validation was not stable or did not use its own validator")


def assert_clean(root: Path, expected_commit: str | None = None) -> str:
    if Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve() != root:
        raise PackageError("--root must name the Git repository root")
    commit = git(root, "rev-parse", "HEAD").decode().strip()
    if expected_commit and commit != expected_commit:
        raise PackageError("HEAD changed during packaging")
    if git(root, "status", "--porcelain=v1", "-z", "--untracked-files=no"):
        raise PackageError("Tracked tree has staged or unstaged changes; commit the intended release first")
    return commit


def package(root: Path, output_dir: Path | None = None, overwrite: bool = False) -> tuple[Path, Path]:
    root = root.resolve()
    commit = assert_clean(root)
    version = git(root, "show", f"{commit}:VERSION").decode("ascii").strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise PackageError("Committed VERSION must contain one canonical major.minor.patch version")
    manifest = tracked_manifest(root, commit)
    if f"V{version}_CHANGES.md" not in manifest:
        raise PackageError(f"Release notes V{version}_CHANGES.md are missing from the commit")
    prefix = f"RPG_OS_v{version}"
    output_dir = (output_dir or root / ".release").resolve()
    archive_path = output_dir / f"{prefix}.zip"
    sums_path = output_dir / "SHA256SUMS"
    for target in (archive_path, sums_path):
        if target.is_symlink() or (target.exists() and (not overwrite or not target.is_file())):
            raise PackageError(f"Output exists or is unsafe; use a new directory or explicit --overwrite: {target}")
    with isolated_directory() as temporary:
        archive = temporary / archive_path.name
        # Archive canonical committed bytes, independent of checkout line-ending
        # preferences. Keep the blob verification below as the authority.
        git(root, "-c", "core.autocrlf=false", "-c", "core.eol=lf",
            "archive", "--format=zip", f"--prefix={prefix}/", f"--output={archive}", commit)
        contents = safe_extract(archive, temporary / "export", prefix)
        if set(contents) != set(manifest):
            raise PackageError("Git archive does not contain exactly the committed files (check export-ignore attributes)")
        object_format = git(root, "rev-parse", "--show-object-format").decode().strip()
        if object_format not in {"sha1", "sha256"}:
            raise PackageError(f"Unsupported Git object format: {object_format}")
        for path, data in contents.items():
            object_data = f"blob {len(data)}\0".encode("ascii") + data
            if hashlib.new(object_format, object_data).hexdigest() != manifest[path]:
                raise PackageError(f"Archive differs from committed file bytes: {path}")
        validate_fresh_install(temporary / "export" / prefix)
        assert_clean(root, commit)
        archive_bytes = archive.read_bytes()
        checksum = hashlib.sha256(archive_bytes).hexdigest()
        sums = f"{checksum}  {archive_path.name}\n".encode("ascii")
        output_dir.mkdir(parents=True, exist_ok=True)
        mode = "wb" if overwrite else "xb"
        for target, data in ((archive_path, archive_bytes), (sums_path, sums)):
            if target.is_symlink():
                raise PackageError(f"Refusing symlink output: {target}")
            with target.open(mode) as output:
                output.write(data)
        if hashlib.sha256(archive_path.read_bytes()).hexdigest() != checksum or sums_path.read_bytes() != sums:
            raise PackageError("Written release failed checksum verification")
        with zipfile.ZipFile(archive_path) as published:
            if published.testzip() is not None:
                raise PackageError("Written release failed ZIP CRC verification")
    return archive_path, sums_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output-dir", type=Path, help="destination (default: repository .release)")
    parser.add_argument("--overwrite", action="store_true", help="explicitly replace existing release outputs")
    args = parser.parse_args(argv)
    try:
        archive, sums = package(args.root, args.output_dir, args.overwrite)
    except (PackageError, OSError, UnicodeError, zipfile.BadZipFile) as exc:
        print(f"Release packaging refused: {exc}", file=sys.stderr)
        return 1
    print(f"Fresh-install release: {archive}\nSHA-256 checksums: {sums}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
