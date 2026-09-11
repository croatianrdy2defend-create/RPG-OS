#!/usr/bin/env python3
"""Actual split-layout/package tests, separate from legacy-layout fixtures."""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True
import package_game as package
ROOT = Path(__file__).resolve().parent.parent


class LayoutTests(unittest.TestCase):
    def test_only_game_is_needed_for_validation(self):
        with tempfile.TemporaryDirectory(prefix='rpg-game-alone-') as tmp:
            root = Path(tmp) / 'game'
            shutil.copytree(ROOT / 'GAME', root)
            result = subprocess.run([sys.executable, '-B', str(root / 'TOOLS/validate.py'), '--root', str(root), '--json'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['structural']['result'], 'PASS')
            self.assertFalse((root.parent / 'DOCS').exists())

    def test_game_has_no_explanations_developer_suites_or_playtest_data(self):
        paths = {p.relative_to(ROOT / 'GAME').as_posix() for p in (ROOT / 'GAME').rglob('*') if p.is_file()}
        self.assertEqual(paths, set(json.loads((ROOT / 'DEV/game_files.json').read_text())))
        for p in paths:
            self.assertFalse(p.startswith(('DOCS/', 'TEST_REPORTS/', 'DEV/', '.github/', 'TOOLS/test_')) or Path(p).name.startswith(('TEST', 'PLAYTEST')))
        for p in ('ARCHITECTURE.md', 'MECHANICS.md', 'VERIFICATION.md', 'HOST_CONTRACT.md', 'TOOLS/package_release.py'):
            self.assertNotIn(p, paths)

    def test_local_game_links_stay_inside_standalone_workspace(self):
        root = (ROOT / 'GAME').resolve()
        for path in root.rglob('*.md'):
            for link in re.findall(r'\]\(([^\s)]+)\)', path.read_text()):
                if re.match(r'^(?:[a-z]+:|#|//)', link, re.I):
                    continue
                target = (path.parent / link.split('#')[0]).resolve()
                with self.subTest(source=str(path.relative_to(root)), link=link):
                    self.assertTrue(target.is_relative_to(root), 'Local game link escapes standalone workspace')
                    self.assertTrue(target.exists(), 'Local game link is missing')

    def test_runtime_rules_remain_inside_game(self):
        for path in ('OS/LAW.md', 'OS/BOOTSTRAP.md', 'ADMIN/CLOSE_CONTRACT.md', 'ADMIN/RECOVERY.md', 'ADMIN/EVIDENCE_AUDIT.md', 'ADMIN/AUTOSAVE.md', 'ENGINE/freeform.md', 'TOOLS/evidence.py'):
            self.assertGreater((ROOT / 'GAME' / path).stat().st_size, 100)

    def test_homepage_distinguishes_download_documentation_and_tests(self):
        text = (ROOT / 'README.md').read_text()
        for label in ('GAME/README.md', 'DOCS/README.md', 'TEST_REPORTS/', '_Game.zip', 'Code → Download ZIP'):
            self.assertIn(label, text)


@unittest.skipUnless(shutil.which('git'), 'Git required for packaging tests')
class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='rpg-distribution-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        self.root.mkdir()
        shutil.copytree(ROOT / 'GAME', self.root / 'GAME')
        (self.root / 'DEV').mkdir()
        shutil.copyfile(ROOT / 'DEV/game_files.json', self.root / 'DEV/game_files.json')
        (self.root / '.gitignore').write_text('.release/\n')
        for command in (('init', '-q'), ('config', 'user.name', 'RPG OS distribution tests'),
                        ('config', 'user.email', 'rpg-tests@example.invalid'), ('config', 'core.autocrlf', 'false'),
                        ('config', 'commit.gpgsign', 'false')):
            package.safety.git(self.root, *command)
        self.commit()

    def commit(self):
        package.safety.git(self.root, 'add', '-A')
        package.safety.git(self.root, 'commit', '-qm', 'Synthetic package fixture')

    def build(self, output=None):
        with contextlib.redirect_stdout(io.StringIO()):
            return package.package(self.root, output)

    def test_package_is_exactly_game_and_validates_after_extraction(self):
        (self.root / 'DOCS').mkdir()
        (self.root / 'DOCS/MECHANICS.md').write_text('Not a game dependency.\n')
        (self.root / 'TEST_REPORTS').mkdir()
        (self.root / 'TEST_REPORTS/test.txt').write_text('Not game state.\n')
        self.commit()
        archive, sums, manifest = self.build()
        data = json.loads(manifest.read_text())
        prefix = 'RPG_OS_v' + data['version'] + '/'
        with zipfile.ZipFile(archive) as z:
            self.assertEqual({n.removeprefix(prefix) for n in z.namelist()}, set(data['files']))
            for name in data['files']:
                self.assertEqual(z.read(prefix + name), (self.root / 'GAME' / name).read_bytes())
            self.assertIsNone(z.testzip())
        self.assertEqual(sums.read_text(), hashlib.sha256(archive.read_bytes()).hexdigest() + '  ' + archive.name + '\n')

    def test_untracked_private_file_does_not_enter_package(self):
        (self.root / 'GAME/INSTANCE/CHAR/PC.md').write_text('Untracked private character.\n')
        archive, _, _ = self.build()
        with zipfile.ZipFile(archive) as z:
            self.assertFalse(any(n.endswith('/PC.md') for n in z.namelist()))

    def test_tracked_campaign_file_is_rejected(self):
        path = self.root / 'GAME/INSTANCE/CHAR/PC.md'
        path.write_text('Private character.\n'); self.commit()
        with self.assertRaisesRegex(package.PackageError, 'inventory differs'):
            self.build()

    def test_missing_runtime_file_is_rejected(self):
        (self.root / 'GAME/OS/LAW.md').unlink(); self.commit()
        with self.assertRaisesRegex(package.PackageError, 'missing='):
            self.build()

    def test_bound_campaign_is_not_a_fresh_install(self):
        path = self.root / 'GAME/INSTANCE/CURRENT_SAVE.md'
        path.write_text(path.read_text().replace('| campaign_id | none |', '| campaign_id | played |'))
        self.commit()
        with self.assertRaises(package.PackageError):
            self.build()

    def test_dirty_tracked_game_is_rejected(self):
        path = self.root / 'GAME/OS/LAW.md'
        path.write_text(path.read_text() + '\nUncommitted change.\n')
        with self.assertRaisesRegex(package.PackageError, 'Tracked tree'):
            self.build()

    def test_repeated_output_does_not_overwrite(self):
        paths = self.build(); originals = [p.read_bytes() for p in paths]
        with self.assertRaisesRegex(package.PackageError, 'already exists'):
            self.build()
        self.assertEqual(originals, [p.read_bytes() for p in paths])

    def test_documentation_only_change_keeps_zip_bytes_identical(self):
        first, _, _ = self.build(self.base / 'first')
        (self.root / 'DOCS').mkdir()
        (self.root / 'DOCS/new.md').write_text('New optional explanation.\n'); self.commit()
        second, _, _ = self.build(self.base / 'second')
        self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_tracked_symlink_mode_rejected_even_without_os_symlink_support(self):
        path = 'GAME/OS/LAW.md'
        oid = package.safety.git(self.root, 'rev-parse', 'HEAD:' + path).decode().strip()
        package.safety.git(self.root, 'update-index', '--cacheinfo', '120000', oid, path)
        package.safety.git(self.root, 'commit', '-qm', 'Synthetic unsafe mode')
        with self.assertRaisesRegex(package.PackageError, 'Unsafe game entry'):
            package.selected_manifest(self.root, 'HEAD')

    def test_duplicate_inventory_is_rejected(self):
        path = self.root / 'DEV/game_files.json'; value = json.loads(path.read_text()); value.append(value[0]); path.write_text(json.dumps(value)); self.commit()
        with self.assertRaisesRegex(package.PackageError, 'duplicate'):
            self.build()


if __name__ == '__main__':
    unittest.main(verbosity=2)
