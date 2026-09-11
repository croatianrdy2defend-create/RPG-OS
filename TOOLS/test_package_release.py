#!/usr/bin/env python3
"""Regression tests for clean public release exports; uses isolated synthetic Git repos."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import shutil
import stat
import sys
import unittest
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pack = load_module("rpg_os_package_release", HERE / "package_release.py")
validator = load_module("rpg_os_release_validator", HERE / "validate.py")


def record(title: str, values: dict[str, str], sections: tuple[str, ...], identity: str, kind: str) -> str:
    rows = "\n".join(f"| {key} | {value} |" for key, value in values.items())
    bodies = "\n\n".join(f"## {section}\n\nnone" for section in sections)
    return (f"---\nid: {identity}\nclass: {kind}\ntemperature: resident\n---\n\n"
            f"# {title}\n\n| Field | Value |\n|---|---|\n{rows}\n\n{bodies}\n")


@unittest.skipUnless(shutil.which("git"), "Git is required for release packaging")
class PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = pack.isolated_directory()
        self.base = self.temporary.__enter__()
        self.addCleanup(self.temporary.__exit__, None, None, None)
        self.root = self.base / "repo"
        self.root.mkdir()
        for relative in validator.REQUIRED_FILES:
            self.write(relative, "# Synthetic fixture\n\nFor release regression only.\n")
        for relative, content in validator.EMPTY_INSTANCE_TEMPLATES.items():
            self.write(relative, content)
        self.write("TOOLS/validate.py", (HERE / "validate.py").read_text(encoding="utf-8"))
        self.write("VERSION", "0.8.0\n")
        self.write("V0.8.0_CHANGES.md", "# v0.8.0 experimental\n\nSynthetic release notes.\n")
        self.write(".gitignore", ".release/\n.work/\n")
        self.write("ENGINE/freeform.md", "---\nid: freeform\nclass: engine\ncharacter_build_support: no-mechanical-sheet\n---\n# Freeform\n\nResolve declared intent using accepted fictional stakes.\n")
        self.write("ARCHIVE/_SCHEMA.md", "---\narchive_schema: hierarchical-scene-v1\n---\n# Archive\n\nAccepted evidence only.\n")
        self.write("ARCHIVE/INDEX.md", "---\narchive_schema: hierarchical-scene-v1\n---\n# Archive index\n\n| save_id | commit_kind | session | span | place | route_terms | notes | folder | session_index | event_heading |\n|---|---|---|---|---|---|---|---|---|---|\n")
        self.write("INSTANCE/SAFETY.md", "# SAFETY\n\nHard no:\n\nFade / veil:\n")
        self.write("INSTANCE/CURRENT_SAVE.md", record("CURRENT_SAVE", pack.SAVE_VALUES, validator.SAVE_SECTIONS, "instance.current_save", "live-checkpoint"))
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", record("CAMPAIGN_CONTRACT", pack.CONTRACT_VALUES, validator.CONTRACT_SECTIONS, "instance.campaign_contract", "campaign-contract"))
        pack.git(self.root, "init", "-q")
        for key, value in {
            "user.name": "RPG OS release tests", "user.email": "rpg-os-tests@example.invalid",
            "commit.gpgsign": "false", "core.autocrlf": "false", "core.safecrlf": "false",
            "core.hooksPath": str(self.base / "no-hooks"),
        }.items():
            pack.git(self.root, "config", key, value)
        self.commit()

    def write(self, relative: str, content: str) -> None:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")

    def commit(self) -> None:
        pack.git(self.root, "add", "-A")
        pack.git(self.root, "commit", "-qm", "Synthetic fixture")

    def test_host_contract_and_case_report_ship_as_exact_documentation(self) -> None:
        documents = {
            "HOST_CONTRACT.md": "# Host boundary\n\nDocumentation, not a gameplay dependency.\n",
            "V0.9.1_TRIALS.md": "# Reported diagnostic\n\nSource limitations remain explicit.\n",
        }
        version_before = (self.root / "VERSION").read_bytes()
        for relative, body in documents.items():
            self.write(relative, body)
        self.commit()
        archive, _sums = pack.package(self.root)
        with zipfile.ZipFile(archive) as result:
            for relative, body in documents.items():
                self.assertEqual(result.read(f"RPG_OS_v0.8.0/{relative}"), body.encode("utf-8"))
            self.assertEqual(result.read("RPG_OS_v0.8.0/VERSION"), version_before)
        self.assertEqual((self.root / "VERSION").read_bytes(), version_before)

    def test_host_documentation_does_not_open_unlisted_root_paths(self) -> None:
        pack.assert_public_paths({"HOST_CONTRACT.md", "V0.9.1_TRIALS.md"})
        for relative in ("HOST_CONTRACT_PRIVATE.md", "host_contract.md", "creature_notes.txt"):
            with self.subTest(path=relative):
                with self.assertRaises(pack.PackageError):
                    pack.assert_public_paths({relative})

    def test_optional_encounter_helper_ships_without_binding_the_fresh_install(self) -> None:
        relative = "ENGINE/_shared/ENCOUNTER_GENERATION.md"
        body = "# Optional generic encounter support\n\nSelected by a bound engine and accepted agreement.\n"
        save_before = (self.root / "INSTANCE/CURRENT_SAVE.md").read_bytes()
        self.write(relative, body)
        self.commit()
        archive, _sums = pack.package(self.root)
        with zipfile.ZipFile(archive) as result:
            self.assertEqual(result.read(f"RPG_OS_v0.8.0/{relative}"), body.encode("utf-8"))
            self.assertEqual(result.read("RPG_OS_v0.8.0/INSTANCE/CURRENT_SAVE.md"), save_before)
        self.assertEqual((self.root / "INSTANCE/CURRENT_SAVE.md").read_bytes(), save_before)

    def test_clean_export_matches_committed_tree_and_checksum(self) -> None:
        self.write(".work/private/notes.md", "Untracked private scene, not for publication.\n")
        self.write(".release/old.zip", "Untracked old artifact.\n")
        self.write("untracked-secret.md", "Not in Git.\n")
        archive, sums = pack.package(self.root)
        self.assertEqual(archive.parent, self.root / ".release")
        checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(sums.read_text(), f"{checksum}  RPG_OS_v0.8.0.zip\n")
        with zipfile.ZipFile(archive) as result:
            self.assertIsNone(result.testzip())
            files = {item.filename.removeprefix("RPG_OS_v0.8.0/") for item in result.infolist() if not item.is_dir()}
            self.assertEqual(files, set(pack.tracked_manifest(self.root, "HEAD")))
            self.assertEqual(result.read("RPG_OS_v0.8.0/VERSION"), b"0.8.0\n")
            self.assertNotIn("untracked-secret.md", files)

    def test_repository_reports_stay_on_github_not_in_fresh_install(self) -> None:
        relative = "TEST_REPORTS/synthetic-report.md"
        body = "# Published test report\n\nRepository-only evidence.\n"
        self.write(relative, body)
        self.commit()
        archive, _sums = pack.package(self.root)
        with zipfile.ZipFile(archive) as result:
            self.assertFalse(any("TEST_REPORTS/" in name for name in result.namelist()))
            self.assertIn("RPG_OS_v0.8.0/VERSION", result.namelist())
        self.assertEqual((self.root / relative).read_text(), body)
        self.assertNotIn(relative, pack.tracked_manifest(self.root, "HEAD"))

    def test_report_exclusion_does_not_allow_other_tracked_campaign_content(self) -> None:
        self.write("TEST_REPORTS/synthetic-report.md", "Repository-only report.\n")
        self.write("PRIVATE_CAMPAIGN/player.md", "Not distributable.\n")
        self.commit()
        with self.assertRaises(pack.PackageError):
            pack.package(self.root)

    def test_committed_version_still_controls_archive_name(self) -> None:
        # Exercise historical version naming with a structurally current fixture;
        # this does not claim that the current validator certifies an old kit.
        self.write("VERSION", "0.7.3\n")
        self.write("V0.7.3_CHANGES.md", "# v0.7.3\n\nSynthetic historical release notes.\n")
        self.commit()
        archive, sums = pack.package(self.root)
        self.assertEqual(archive.name, "RPG_OS_v0.7.3.zip")
        self.assertTrue(sums.read_text().endswith("  RPG_OS_v0.7.3.zip\n"))
        with zipfile.ZipFile(archive) as result:
            self.assertEqual(result.read("RPG_OS_v0.7.3/VERSION"), b"0.7.3\n")

    def test_windows_checkout_preferences_do_not_change_release_bytes(self) -> None:
        committed = pack.git(self.root, "show", "HEAD:README.md")
        self.assertNotIn(b"\r\n", committed)
        pack.git(self.root, "config", "core.autocrlf", "true")
        pack.git(self.root, "config", "core.eol", "crlf")
        # Recreate only this disposable fixture's README from its unchanged LF
        # index; removing it first prevents Git's unchanged-file optimization.
        (self.root / "README.md").unlink()
        pack.git(self.root, "checkout-index", "--", "README.md")
        self.assertIn(b"\r\n", (self.root / "README.md").read_bytes())
        # Refresh conversion metadata after changing fixture configuration, and
        # prove this refresh did not change any indexed committed content.
        pack.git(self.root, "add", "--renormalize", ".")
        self.assertEqual(pack.git(self.root, "write-tree"), pack.git(self.root, "rev-parse", "HEAD^{tree}"))
        pack.assert_clean(self.root)
        archive, _sums = pack.package(self.root)
        with zipfile.ZipFile(archive) as result:
            self.assertEqual(result.read("RPG_OS_v0.8.0/README.md"), committed)
            self.assertEqual(result.read("RPG_OS_v0.8.0/TOOLS/validate.py"),
                             pack.git(self.root, "show", "HEAD:TOOLS/validate.py"))
        for key, expected in (("core.autocrlf", b"true"), ("core.eol", b"crlf")):
            self.assertEqual(pack.git(self.root, "config", "--get", key).strip(), expected)

    def test_existing_output_is_preserved_until_explicit_overwrite(self) -> None:
        archive, sums = pack.package(self.root, self.base / "output")
        original = archive.read_bytes(), sums.read_bytes()
        with self.assertRaisesRegex(pack.PackageError, "Output exists"):
            pack.package(self.root, self.base / "output")
        self.assertEqual((archive.read_bytes(), sums.read_bytes()), original)
        pack.package(self.root, self.base / "output", overwrite=True)
        self.assertEqual((archive.read_bytes(), sums.read_bytes()), original)

    def test_dirty_tracked_tree_is_rejected(self) -> None:
        self.write("README.md", "Uncommitted change\n")
        with self.assertRaisesRegex(pack.PackageError, "Tracked tree"):
            pack.package(self.root)
        pack.git(self.root, "add", "README.md")
        with self.assertRaisesRegex(pack.PackageError, "Tracked tree"):
            pack.package(self.root)
        self.assertFalse((self.root / ".release").exists())

    def test_bound_identity_is_rejected(self) -> None:
        save = dict(pack.SAVE_VALUES, campaign_id="private-campaign", save_rev="1")
        self.write("INSTANCE/CURRENT_SAVE.md", record("CURRENT_SAVE", save, validator.SAVE_SECTIONS, "instance.current_save", "live-checkpoint"))
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "Fresh install requires"):
            pack.package(self.root)

    def test_accepted_contract_is_rejected(self) -> None:
        values = dict(pack.CONTRACT_VALUES, contract_id="private-agreement", contract_rev="1", status="accepted")
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", record("CAMPAIGN_CONTRACT", values, validator.CONTRACT_SECTIONS, "instance.campaign_contract", "campaign-contract"))
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "Fresh install requires"):
            pack.package(self.root)

    def test_live_state_in_permitted_register_fails_structural_validation(self) -> None:
        self.write("INSTANCE/NOW.md", validator.EMPTY_INSTANCE_TEMPLATES["INSTANCE/NOW.md"].replace("\nnone\n", "\nPrivate faction clock: 3.\n"))
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "Frozen fresh-install validation failed"):
            pack.package(self.root)

    def test_session_procedure_and_unstarted_section_ship_without_preparation(self) -> None:
        procedure = "# Session procedure\n\nPrepare on actual begin; invite feedback at actual end.\n"
        self.write("ADMIN/SESSION.md", procedure)
        save = self.root / "INSTANCE/CURRENT_SAVE.md"
        self.write("INSTANCE/CURRENT_SAVE.md", save.read_text(encoding="utf-8") + "\n## Session continuity\n\nnone\n")
        self.commit()
        archive, _sums = pack.package(self.root)
        with zipfile.ZipFile(archive) as result:
            self.assertEqual(result.read("RPG_OS_v0.8.0/ADMIN/SESSION.md"), procedure.encode("utf-8"))
            self.assertIn(b"## Session continuity\n\nnone", result.read("RPG_OS_v0.8.0/INSTANCE/CURRENT_SAVE.md"))
            self.assertNotIn("RPG_OS_v0.8.0/INSTANCE/PREP.md", result.namelist())

    def test_live_session_and_feedback_in_public_save_are_rejected(self) -> None:
        original = (self.root / "INSTANCE/CURRENT_SAVE.md").read_text(encoding="utf-8")
        for body in (
            "| Session item | Value |\n|---|---|\n| session_id | private-session |\n| phase | ended |\n| opening_save | private-save |\n| feedback | received |\n",
            "none\n\nPlayer feedback: a private request.\n",
            "none\n\n<!-- Private feedback retained in a comment. -->\n",
        ):
            with self.subTest(body=body):
                self.write("INSTANCE/CURRENT_SAVE.md", original + "\n## Session continuity\n\n" + body)
                self.commit()
                with self.assertRaisesRegex(pack.PackageError, "session continuity or feedback"):
                    pack.package(self.root)

    def test_preparation_is_never_a_public_install_path_even_when_empty(self) -> None:
        for relative in ("INSTANCE/PREP.md", "INSTANCE/PREP.candidate.md", "INSTANCE/PREP/session.md"):
            with self.subTest(relative=relative):
                with self.assertRaisesRegex(pack.PackageError, "Campaign/module content"):
                    pack.assert_public_paths({relative})

    def test_missing_session_procedure_fails_fresh_install_validation(self) -> None:
        (self.root / "ADMIN/SESSION.md").unlink()
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "CORE_REQUIRED_FILE"):
            pack.package(self.root)

    def test_real_module_is_rejected(self) -> None:
        self.write("MODULES/example_world/MODULE.md", "# Private campaign module\n")
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "Campaign/module content"):
            pack.package(self.root)

    def test_private_paths_and_additional_bodies_are_rejected(self) -> None:
        for relative in (
            "RECOVERY/operation/preimage.md", "HANDOVER/export/GM_STATE.md",
            "INSTANCE/CHAR/PC.md", "INSTANCE/PEOPLE/liv.md", "ARCHIVE/sessions/test/scene.md",
            "ENGINE/gurps.md", "TEST_RUN.md", "secret/notes.md", ".work/private.md",
            "ENGINE/_shared/ENCOUNTER_GENERATION_PRIVATE.md", "ENGINE/_shared/encounter_generation.md",
            "ENGINE/_shared/setting/ENCOUNTER_GENERATION.md", "ENGINE/campaign/ENCOUNTER_GENERATION.md",
            "ENGINE/_shared/CAMPAIGN_GENERATION.md",
            "TOOLS/.release/private.zip",
            "EVIDENCE/captures/session-001/source.txt", "EVIDENCE/private.jsonl",
            "EVIDENCE/captures/session-001/manifest.json", "EVIDENCE/audit-report.json",
        ):
            with self.subTest(path=relative):
                with self.assertRaises(pack.PackageError):
                    pack.assert_public_paths({relative})

    def test_missing_required_document_fails_frozen_validator(self) -> None:
        (self.root / "OS/LAW.md").unlink()
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "Frozen fresh-install validation failed"):
            pack.package(self.root)

    def test_missing_v08_extension_document_cannot_ship(self) -> None:
        for relative in ("OS/AGENT_STATE.md", "ADMIN/UPGRADE_V08.md", "ADMIN/PLAYTEST_V08.md",
                         "TOOLS/read_source.py", "TOOLS/search_index.py", "TOOLS/evidence.py",
                         "ADMIN/EVIDENCE_AUDIT.md", "ADMIN/SOURCE_ACCESS.md", "EVIDENCE/README.md"):
            original = (self.root / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                (self.root / relative).unlink()
                self.commit()
                with self.assertRaisesRegex(pack.PackageError, "Frozen fresh-install validation failed"):
                    pack.package(self.root)
                self.write(relative, original)
                self.commit()

    def test_git_export_attributes_cannot_silently_omit_committed_files(self) -> None:
        self.write("TOOLS/.gitattributes", "validate.py export-ignore\n")
        self.commit()
        with self.assertRaisesRegex(pack.PackageError, "exactly the committed files"):
            pack.package(self.root)

    def test_tracked_symlink_is_rejected_without_needing_os_symlink_support(self) -> None:
        self.write("TOOLS/link", "../../outside\n")
        pack.git(self.root, "add", "TOOLS/link")
        blob = pack.git(self.root, "rev-parse", ":TOOLS/link").decode().strip()
        pack.git(self.root, "update-index", "--cacheinfo", "120000", blob, "TOOLS/link")
        pack.git(self.root, "commit", "-qm", "Synthetic symlink contamination")
        with self.assertRaisesRegex(pack.PackageError, "symlinks, submodules or special files"):
            pack.tracked_manifest(self.root, "HEAD")

    def test_zip_traversal_links_and_collisions_are_rejected_before_extraction(self) -> None:
        cases = [
            ("RPG_OS_v0.7.3/../../escaped.txt", 0),
            ("/absolute.txt", 0),
            ("RPG_OS_v0.7.3/C:/escaped.txt", 0),
            ("RPG_OS_v0.7.3/back\\slash.txt", 0),
            ("RPG_OS_v0.7.3/NUL.txt", 0),
            ("RPG_OS_v0.7.3/link", stat.S_IFLNK | 0o777),
        ]
        for number, (name, mode) in enumerate(cases):
            with self.subTest(path=name):
                archive = self.base / f"unsafe-{number}.zip"
                with zipfile.ZipFile(archive, "w") as output:
                    info = zipfile.ZipInfo(name)
                    info.filename = name  # Preserve hostile backslashes on Windows too.
                    info.create_system = 3
                    info.external_attr = mode << 16
                    output.writestr(info, "../../outside")
                destination = self.base / f"unpacked-{number}"
                with self.assertRaises(pack.PackageError):
                    pack.safe_extract(archive, destination, "RPG_OS_v0.7.3")
                self.assertFalse(destination.exists())
        archive = self.base / "collision.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("RPG_OS_v0.7.3/README.md", "first")
            output.writestr("RPG_OS_v0.7.3/readme.md", "second")
        with self.assertRaisesRegex(pack.PackageError, "case-colliding"):
            pack.safe_extract(archive, self.base / "collision", "RPG_OS_v0.7.3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
