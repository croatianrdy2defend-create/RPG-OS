#!/usr/bin/env python3
"""Build a standalone, unbound GAME-only ZIP from exact committed bytes.

Requires Python 3.10+ and Git for maintenance, not for playing.
Documentation, tests, workflows, private campaign files and untracked files do
not enter the package. An explicit inventory prevents accidental new content.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('rpg_legacy_package_safety', Path(__file__).parent / 'TOOLS/package_release.py')
assert spec and spec.loader
safety = importlib.util.module_from_spec(spec)
spec.loader.exec_module(safety)
PackageError = safety.PackageError


def selected_manifest(root: Path, commit: str) -> dict[str, str]:
    wanted = json.loads(safety.git(root, 'show', f'{commit}:DEV/game_files.json'))
    if (not isinstance(wanted, list) or not wanted or not all(isinstance(n, str) for n in wanted)
            or len(wanted) != len(set(wanted))):
        raise PackageError('Invalid or duplicate game inventory')
    for name in wanted:
        safety.portable_path(name)
    found = {}
    folded = set()
    for entry in safety.git(root, 'ls-tree', '-rz', '--full-tree', commit, '--', 'GAME').split(b'\0'):
        if not entry:
            continue
        meta, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode('ascii').split()
        full = raw_path.decode('utf-8')
        safety.portable_path(full)
        if not full.startswith('GAME/') or mode not in ('100644', '100755') or kind != 'blob':
            raise PackageError('Unsafe game entry: ' + full)
        relative = full[5:]
        if relative.casefold() in folded:
            raise PackageError('Case-colliding game path: ' + relative)
        folded.add(relative.casefold())
        found[relative] = oid
    if set(found) != set(wanted):
        raise PackageError('Game inventory differs: missing=' + str(sorted(set(wanted) - set(found)))
                           + '; unexpected=' + str(sorted(set(found) - set(wanted))))
    # Retain existing unbound/public-path defenses in addition to exact inventory.
    safety.assert_public_paths(set(found))
    return found


def safe_output(path: Path) -> None:
    for component in (path, *path.parents):
        if component.is_symlink():
            raise PackageError('Output path contains a symlink: ' + str(component))
    if path.exists():
        raise PackageError('Output already exists; use a new output directory: ' + str(path))


def package(root: Path = ROOT, output_dir: Path | None = None):
    root = root.resolve()
    commit = safety.assert_clean(root)
    manifest = selected_manifest(root, commit)
    version = safety.git(root, 'show', f'{commit}:GAME/VERSION').decode('ascii').strip()
    if not safety.VERSION_PATTERN.fullmatch(version):
        raise PackageError('Invalid GAME/VERSION')
    prefix = f'RPG_OS_v{version}'
    name = prefix + '_Game.zip'
    # Do not resolve away a symlink before checking output components.
    output = (output_dir or root / '.release').absolute()
    paths = [output / name, output / (prefix + '_Game.SHA256SUMS'), output / (prefix + '_Game.manifest.json')]
    for path in paths:
        safe_output(path)
    with safety.isolated_directory() as temp:
        archive = temp / name
        hashes = {}
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as result:
            for path, oid in sorted(manifest.items()):
                data = safety.git(root, 'cat-file', 'blob', oid)
                info = zipfile.ZipInfo(prefix + '/' + path, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                result.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
                hashes[path] = hashlib.sha256(data).hexdigest()
        contents = safety.safe_extract(archive, temp / 'extracted', prefix)
        if set(contents) != set(manifest) or any(hashlib.sha256(data).hexdigest() != hashes[p] for p, data in contents.items()):
            raise PackageError('Extracted package differs from selected committed bytes')
        safety.validate_fresh_install(temp / 'extracted' / prefix)
        safety.assert_clean(root, commit)
        payload = archive.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        info = dict(version=version, source_commit=commit, game_tree=safety.git(root, 'rev-parse', f'{commit}:GAME').decode().strip(),
                    file_count=len(manifest), archive=name, sha256=digest, bytes=len(payload),
                    files=hashes, scope='Standalone unbound GAME subtree; no explanatory docs, playtests or developer tooling.')
        outputs = [payload, f'{digest}  {name}\n'.encode('ascii'), (json.dumps(info, indent=2) + '\n').encode('utf-8')]
        output.mkdir(parents=True, exist_ok=True)
        for path, data in zip(paths, outputs):
            safe_output(path)
            with path.open('xb') as stream:
                stream.write(data)
            if path.read_bytes() != data:
                raise PackageError('Published file readback mismatch: ' + str(path))
        print(json.dumps({k: v for k, v in info.items() if k != 'files'}, indent=2))
        return paths


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    try:
        package(args.root, args.output_dir)
    except (PackageError, OSError, ValueError, KeyError) as exc:
        parser.exit(1, 'Game packaging failed: ' + str(exc) + '\n')
