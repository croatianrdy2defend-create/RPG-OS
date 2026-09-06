#!/usr/bin/env python3
"""Self-contained structural regression tests; no model calls or live campaign writes.

Fixtures are generated in .work/test_validate and removed after each test.
Run sequentially, not during a validator scan of their parent workspace.
Run: python -B TOOLS/test_validate.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("rpg_os_validator", HERE / "validate.py")
assert SPEC and SPEC.loader
validate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validate
SPEC.loader.exec_module(validate)


def record(title: str, values: dict[str, str], sections: dict[str, str], front: str = "") -> str:
    metadata = "\n".join(f"| {key} | {value} |" for key, value in values.items())
    bodies = "\n\n".join(f"## {name}\n\n{body}" for name, body in sections.items())
    return f"{front}# {title}\n\n| Field | Value |\n|---|---|\n{metadata}\n\n{bodies}\n"


class StructuralValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_parent = HERE.parent / ".work" / "test_validate"
        self.fixture_parent.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix="case-", dir=self.fixture_parent))
        self.addCleanup(self.remove_fixture)
        for relative in validate.REQUIRED_FILES:
            self.write(relative, "# Synthetic fixture document\n\nFor structural regression only.\n")
        for relative, text in validate.EMPTY_INSTANCE_TEMPLATES.items():
            self.write(relative, text)
        self.write("TOOLS/validate.py", (HERE / "validate.py").read_text(encoding="utf-8"))
        self.write("TOOLS/test_validate.py", Path(__file__).read_text(encoding="utf-8"))
        self.write("ENGINE/freeform.md", "---\nid: freeform\nclass: engine\ncharacter_build_support: no-mechanical-sheet\n---\n# Freeform\n\nResolve declared intent using accepted fictional stakes.\n")
        self.write("ARCHIVE/_SCHEMA.md", "---\narchive_schema: hierarchical-scene-v1\n---\n# Archive\n\nAccepted evidence only.\n")
        self.write("ARCHIVE/INDEX.md", "---\narchive_schema: hierarchical-scene-v1\n---\n# Archive index\n\n| save_id | commit_kind | session | span | place | route_terms | notes | folder | session_index | event_heading |\n|---|---|---|---|---|---|---|---|---|---|\n")
        self.write("INSTANCE/SAFETY.md", "# SAFETY\n\nHard no:\n\nFade / veil:\n")
        self.save = {field: "none" for field in validate.CURRENT_SAVE_FIELDS}
        self.save.update(engine="unbound", module="unbound", save_rev="0", commit_kind="unbound", safety_state="floor-only")
        self.save_sections = {name: "none" for name in validate.SAVE_SECTIONS}
        self.contract = dict(campaign_id="none", contract_id="none", contract_rev="0", contract_parent="none", status="unbound", module="unbound")
        self.contract_sections = {name: "none" for name in validate.CONTRACT_SECTIONS}
        self.flush()

    def remove_fixture(self) -> None:
        # Verify resolved deletion stays under this task's fixture directory.
        resolved = self.root.resolve()
        boundary = self.fixture_parent.resolve()
        if resolved.parent != boundary or not resolved.name.startswith("case-"):
            raise RuntimeError("refusing cleanup outside the isolated fixture directory")
        shutil.rmtree(resolved)

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def read(self, relative: str) -> str:
        return (self.root / relative).read_text(encoding="utf-8")

    def flush(self) -> None:
        save_front = "---\nid: instance.current_save\nclass: live-checkpoint\ntemperature: resident\n---\n\n"
        self.write("INSTANCE/CURRENT_SAVE.md", record("CURRENT_SAVE", self.save, self.save_sections, save_front))
        front = "---\nid: instance.campaign_contract\nclass: campaign-contract\ntemperature: resident\n---\n\n"
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", record("CAMPAIGN_CONTRACT", self.contract, self.contract_sections, front))

    def bind(self) -> None:
        self.save.update(engine="freeform", module="brine", pc_record="INSTANCE/CHAR/PC.md", campaign_id="brine-01", save_id="save-01", save_rev="1", commit_kind="bind", datetime="Third tide", place="Tidal observatory")
        self.save_sections.update({
            "Situation": "Opening scene. The collective observes the rising water; no action declared and no unresolved choice.",
            "Character state": "The player controls the coral collective Iri. Its outer fronds are intact.",
            "Open matters": "none", "Active processes": "none", "Relevant records": "Profile: `INSTANCE/CHAR/PC.md`.",
        })
        self.contract.update(campaign_id="brine-01", contract_id="agreement-01", contract_rev="1", status="accepted", module="brine")
        self.contract_sections.update({
            "Campaign promise": "Play form: Quiet emergent exploration in an original tidal world; no imported franchise lore.",
            "Player control": "Player chooses Iri's voluntary conduct and commitments. No routine authorship delegated.\n\nRetcon: OOC rewind is available; stopping, ending, presentation changes and correction of genuine errors remain distinct.",
            "GM initiative": "GM portrays the world and NPCs, resolves live processes, and may invent ordinary compatible texture.\n\nForm selection: The operator accepts the stated form; selection is not delegated.",
            "Time and transitions": "Carry declared sequences until a meaningful new choice.\n\nCuts: Lived continuity; compress declared or explicitly delegated routine only. No cinematic jumps are granted.",
            "Presentation": "Clear sensory prose with brief public status. Optional guidance in ordinary prose.\n\nStructure disclosure: General form is known, plot details stay hidden; do not repeatedly explain structure.",
        })
        self.flush()
        self.write("MODULES/brine/MODULE.md", "---\nid: brine\ntitle: Brine Observatory\nengine: freeform\n---\n# Brine\n\n## Capabilities\n\nnone\n")
        self.write("MODULES/brine/SETTING_BRIEF.md", "---\nid: brine.setting_brief\nclass: setting-brief\n---\n# Setting brief\n\n## World identity\n\nAn original world of tidal observatories and collective coral people.\n\n## What is ordinary\n\nScent and water movement carry conversation; persons vary independently of reef.\n\n## Available depth\n\nOrdinary open texture may be invented; no detailed cold authority is installed.\n")
        pc = "# Iri\n\nA player-controlled coral collective with intact fronds. Further biography is unspecified.\n"
        self.write("MODULES/brine/CHAR/PC.md", pc)
        self.write("INSTANCE/CHAR/PC.md", pc)
        t0 = dict(self.save)
        t0.update(campaign_id="none", save_id="none", save_rev="0", save_parent="none", commit_kind="unbound", archive_ref="none", evidence_through="none")
        self.write("MODULES/brine/T0_SAVE.md", record("T0_SAVE", t0, self.save_sections))

    def archive_close(self) -> None:
        self.save.update(save_id="save-02", save_rev="2", save_parent="save-01", commit_kind="close", archive_ref="sessions/save-02", evidence_through="save-02")
        self.flush()
        self.write("ARCHIVE/INDEX.md", self.read("ARCHIVE/INDEX.md") + "| save-02 | close | Tidal observation | Third tide | Observatory | Iri, tide | none | sessions/save-02 | sessions/save-02/INDEX.md | |\n")
        self.write("ARCHIVE/sessions/save-02/INDEX.md", "# Session index\n\n## R-save-02-observation\nFile: episode.md\nEvidence: E-save-02-observation\nTime: Third tide\nPeople: Iri\nPlaces: Observatory\nTopics: Tide\nNotable:\n- The player chose to observe the tidal marker.\n")
        self.write("ARCHIVE/sessions/save-02/episode.md", "# Episode\n\n## E-save-02-observation\n\nThe player declared observation of the tide. The GM described the marker rising.\n\nExact complete transcript is unavailable; this records only the available accepted exchange.\n")

    def check(self) -> validate.Validator:
        snapshot, _digest = validate.snapshot_tree(self.root)
        checker = validate.Validator(self.root)
        checker.run(snapshot)
        return checker

    def assert_valid(self) -> validate.Validator:
        checker = self.check()
        failures = [item for item in checker.findings if item.severity in {"ERROR", "INCOMPLETE"}]
        self.assertEqual([], failures)
        return checker

    def assert_code(self, code: str, severity: str = "ERROR") -> None:
        findings = self.check().findings
        self.assertTrue(any(item.code == code and item.severity == severity for item in findings), findings)

    def run_report(self, module=validate) -> tuple[int, dict]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = module.main(["--root", str(self.root), "--json"])
        return code, json.loads(output.getvalue())

    def replace_clause(self, label: str, replacement: str) -> str:
        section = validate.CONTRACT_CLAUSES[label]
        lines = self.contract_sections[section].splitlines()
        original = next(line for line in lines if line.startswith(label + ":"))
        self.contract_sections[section] = "\n".join(replacement if line == original else line for line in lines)
        return original

    def remove_recorded_empty_directories(self, records: list[tuple[str, bool, bool]]) -> list[str]:
        """Fixture-only simulation of the documented manual recovery step.

        Records hold exact path, recorded preexistence, and verified creation
        by this operation. This is not a runtime recovery implementation or
        proof a model follows it.
        """
        removed: list[str] = []
        for relative, preexisting, created_by_operation in sorted(records, key=lambda item: len(Path(item[0]).parts), reverse=True):
            if preexisting or not created_by_operation:
                continue
            pure = Path(relative)
            if not pure.parts or pure.drive or pure.is_absolute() or "\\" in relative or any(part in {".", ".."} for part in pure.parts):
                raise ValueError("unsafe recorded directory")
            target = self.root / pure
            resolved = target.resolve()
            resolved.relative_to(self.root.resolve())
            if resolved == self.root.resolve() or pure.parts[0].casefold() == "recovery":
                raise ValueError("recovery material and workspace root are protected")
            probe = target
            while probe != self.root:
                if probe.is_symlink():
                    raise ValueError("symlink directory route is protected")
                probe = probe.parent
            if target.is_dir() and not any(target.iterdir()):
                target.rmdir()  # Nonrecursive: unexpected content prevents removal.
                removed.append(relative)
        return removed

    def test_required_clause_omissions(self) -> None:
        self.bind()
        accepted = dict(self.contract_sections)
        for label in validate.CONTRACT_CLAUSES:
            with self.subTest(clause=label):
                self.contract_sections = dict(accepted)
                self.replace_clause(label, "")
                self.flush()
                self.assert_code("CONTRACT_CLAUSE_MISSING")

    def test_clause_in_wrong_section_is_rejected(self) -> None:
        self.bind()
        accepted = dict(self.contract_sections)
        for label, intended in validate.CONTRACT_CLAUSES.items():
            with self.subTest(clause=label):
                self.contract_sections = dict(accepted)
                clause = self.replace_clause(label, "")
                other = next(section for section in validate.CONTRACT_SECTIONS if section != intended)
                self.contract_sections[other] += "\n\n" + clause
                self.flush()
                self.assert_code("CONTRACT_CLAUSE_SECTION")

    def test_clause_duplicates_are_rejected(self) -> None:
        self.bind()
        accepted = dict(self.contract_sections)
        for label, section in validate.CONTRACT_CLAUSES.items():
            with self.subTest(clause=label):
                self.contract_sections = dict(accepted)
                clause = next(line for line in accepted[section].splitlines() if line.startswith(label + ":"))
                self.contract_sections[section] += "\n\n- " + clause
                self.flush()
                self.assert_code("CONTRACT_CLAUSE_DUPLICATE")

    def test_clause_placeholders_and_blank_values_are_rejected(self) -> None:
        self.bind()
        accepted = dict(self.contract_sections)
        for label in validate.CONTRACT_CLAUSES:
            for placeholder in ("", "none", "TBD", "<accepted wording>", "[]"):
                with self.subTest(clause=label, value=placeholder):
                    self.contract_sections = dict(accepted)
                    self.replace_clause(label, label + ": " + placeholder)
                    self.flush()
                    self.assert_code("CONTRACT_CLAUSE_EMPTY")

    def test_clause_bullets_and_free_text_are_accepted_without_enums(self) -> None:
        self.bind()
        for label in validate.CONTRACT_CLAUSES:
            self.replace_clause(label, "- " + label + ": A custom accepted arrangement described in ordinary language.")
        self.flush()
        self.assert_valid()  # This certifies structure, not the wording's adequacy.

    def test_required_clause_cannot_hide_in_code_comment_or_quote(self) -> None:
        self.bind()
        original = self.replace_clause("Retcon", "")
        self.contract_sections["Player control"] += "\n\n```text\n" + original + "\n```\n<!-- " + original + " -->\n> " + original
        self.flush()
        self.assert_code("CONTRACT_CLAUSE_MISSING")

    def test_clause_outside_section_is_not_accepted(self) -> None:
        self.bind()
        original = self.replace_clause("Cuts", "")
        self.flush()
        text = self.read("INSTANCE/CAMPAIGN_CONTRACT.md")
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", text.replace("# CAMPAIGN_CONTRACT\n", "# CAMPAIGN_CONTRACT\n\n" + original + "\n"))
        self.assert_code("CONTRACT_CLAUSE_SECTION")

    def test_clean_unbound(self) -> None:
        self.assert_valid()

    def test_bound_without_policy_bearing_or_ledgers(self) -> None:
        self.bind()
        self.assert_valid()

    def test_full_save_and_checkpoint_keep_evidence(self) -> None:
        self.bind()
        self.archive_close()
        self.assert_valid()
        self.save.update(save_id="save-03", save_rev="3", save_parent="save-02", commit_kind="checkpoint")
        self.flush()
        self.assert_valid()

    def test_checkpoint_cannot_clear_existing_evidence_boundary(self) -> None:
        self.bind()
        self.archive_close()
        self.save.update(save_id="save-03", save_rev="3", save_parent="save-02", commit_kind="checkpoint", archive_ref="none", evidence_through="none")
        self.flush()
        self.assert_code("ARCHIVE_CHECKPOINT_LOST_BOUNDARY")

    def test_checkpoint_cannot_claim_its_own_archived_evidence(self) -> None:
        self.bind()
        self.archive_close()
        self.save.update(save_id="save-03", save_rev="3", save_parent="save-02", commit_kind="checkpoint", evidence_through="save-03")
        self.flush()
        self.assert_code("SAVE_CHECKPOINT_EVIDENCE")

    def test_evidence_boundary_cannot_point_at_other_folder(self) -> None:
        self.bind()
        self.archive_close()
        self.save["archive_ref"] = "sessions/another-save"
        self.flush()
        self.assert_code("ARCHIVE_EVIDENCE_FOLDER")

    def test_agreement_identity_mismatch(self) -> None:
        self.bind()
        self.contract["campaign_id"] = "another-campaign"
        self.flush()
        self.assert_code("CONTRACT_BINDING_MISMATCH")

    def test_required_save_and_agreement_sections(self) -> None:
        self.bind()
        del self.save_sections["Active processes"]
        del self.contract_sections["Player control"]
        self.flush()
        self.assert_code("SAVE_SECTION_COUNT")
        self.assert_code("CONTRACT_SECTION_COUNT")

    def test_metadata_extensions_warn_without_rejecting(self) -> None:
        self.bind()
        self.save["operator_note"] = "An optional local label"
        self.contract["display_name"] = "Tides"
        self.flush()
        self.assert_valid()
        self.assert_code("SAVE_UNKNOWN_FIELD", "WARNING")
        self.assert_code("CONTRACT_UNKNOWN_FIELD", "WARNING")

    def test_duplicate_metadata_is_still_rejected(self) -> None:
        self.bind()
        text = self.read("INSTANCE/CURRENT_SAVE.md").replace("| save_rev | 1 |", "| save_rev | 1 |\n| save_rev | 2 |")
        self.write("INSTANCE/CURRENT_SAVE.md", text)
        self.assert_code("SAVE_DUPLICATE_FIELD")

    def test_control_metadata_cannot_hide_in_section_table(self) -> None:
        self.bind()
        self.save_sections["Relevant records"] += "\n\n| Field | Value |\n|---|---|\n| save_id | competing-save |"
        self.flush()
        self.assert_code("SAVE_SHADOW_METADATA")

    def test_legacy_format_requires_explicit_upgrade(self) -> None:
        self.bind()
        del self.save["evidence_through"]
        self.save["immediate_scene"] = "Tidal observatory"
        self.save_sections.clear()
        self.contract["campaign_promise"] = "Quiet exploration"
        self.contract_sections.clear()
        self.flush()
        self.assert_code("SAVE_REQUIRES_UPGRADE")
        self.assert_code("CONTRACT_REQUIRES_UPGRADE")

    def test_current_sections_can_reorder_but_brief_order_is_fixed(self) -> None:
        self.bind()
        self.save.update(save_id="save-02", save_rev="2", save_parent="save-01", commit_kind="checkpoint")
        self.save_sections = dict(reversed(list(self.save_sections.items())))
        self.contract_sections = dict(reversed(list(self.contract_sections.items())))
        self.flush()
        self.assert_valid()
        brief = self.read("MODULES/brine/SETTING_BRIEF.md")
        brief = brief.replace("## World identity", "## Swapped").replace("## What is ordinary", "## World identity").replace("## Swapped", "## What is ordinary")
        self.write("MODULES/brine/SETTING_BRIEF.md", brief)
        self.assert_code("SETTING_BRIEF_SECTION_ORDER")

    def test_active_safety_needs_real_entry_without_duplicate_flag(self) -> None:
        self.bind()
        self.save["safety_state"] = "active"
        self.flush()
        self.assert_code("SAFETY_ACTIVE_EMPTY")
        self.write("INSTANCE/SAFETY.md", "# SAFETY\n\nHard no:\n- No graphic injury descriptions.\n\nFade / veil:\n")
        self.assert_valid()
        self.save["safety_state"] = "floor-only"
        self.flush()
        self.assert_code("SAFETY_ENTRIES_INACTIVE")

    def test_unbound_and_bind_cannot_hide_prior_register_content(self) -> None:
        self.write("INSTANCE/KNOWN.md", self.read("INSTANCE/KNOWN.md").replace("\nnone\n", "\nAn earlier PC learned a secret.\n"))
        self.assert_code("INSTANCE_INITIAL_REGISTER")
        self.bind()
        self.assert_code("INSTANCE_INITIAL_REGISTER")

    def test_missing_metadata_cannot_hide_in_code_or_comments(self) -> None:
        self.bind()
        del self.save["evidence_through"]
        self.flush()
        self.write("INSTANCE/CURRENT_SAVE.md", self.read("INSTANCE/CURRENT_SAVE.md") + "\n```markdown\n| evidence_through | none |\n```\n<!-- | evidence_through | none | -->\n")
        self.assert_code("SAVE_MISSING_FIELD")

    def test_readable_section_tables_are_allowed(self) -> None:
        self.bind()
        table = "\n\n| Condition | Value |\n|---|---|\n| Outer fronds | intact |"
        self.save_sections["Character state"] += table
        self.flush()
        # A later checkpoint need not match the opening template.
        self.save.update(save_id="save-02", save_rev="2", save_parent="save-01", commit_kind="checkpoint")
        self.flush()
        self.assert_valid()

    def test_private_watch_pointer_resolves_without_disclosing_content(self) -> None:
        self.bind()
        self.save.update(save_id="save-02", save_rev="2", save_parent="save-01", commit_kind="checkpoint")
        self.save_sections["Active processes"] = "At the fourth tide inspect `INSTANCE/NOW.md#Watch alpha` before advancing water conditions."
        self.write("INSTANCE/NOW.md", "# NOW\n\n## Watch alpha\n\nPrivate established test state and its actual trigger are recorded here.\n")
        self.flush()
        self.assert_valid()
        self.write("INSTANCE/NOW.md", "# NOW\n\n## Different watch\n\nA different established private process.\n")
        self.assert_code("SAVE_RECORD_HEADING")

    def test_current_record_path_escape(self) -> None:
        self.bind()
        self.save_sections["Relevant records"] = "Read `../outside.md`."
        self.flush()
        self.assert_code("SAVE_RECORD_PATH")

    def test_module_capability_path_escape(self) -> None:
        self.bind()
        self.write("MODULES/brine/MODULE.md", "---\nid: brine\ntitle: Brine\nengine: freeform\n---\n# Brine\n\n## Capabilities\n\n| Capability | Entrypoint |\n|---|---|\n| TRUTH | ../../outside.md |\n")
        self.assert_code("MODULE_ENTRYPOINT_PATH")

    def test_archive_shard_path_escape(self) -> None:
        self.bind()
        self.archive_close()
        self.write("ARCHIVE/sessions/save-02/INDEX.md", self.read("ARCHIVE/sessions/save-02/INDEX.md").replace("File: episode.md", "File: ../../../outside.md"))
        self.assert_code("SESSION_SHARD_PATH")

    def test_pending_recovery_blocks_even_with_completed_text(self) -> None:
        self.bind()
        self.write("RECOVERY/ACTIVE.md", "operation_id: synthetic\nstatus: complete\n")
        self.assert_code("RECOVERY_PENDING")

    def test_active_handover_warns_bound_without_certifying_package(self) -> None:
        self.bind()
        self.write("HANDOVER/retained/RECEIPT.md", "status: imported\n")
        self.assert_valid()
        self.write("HANDOVER/ACTIVE.md", "status: complete\n")
        checker = self.assert_valid()
        finding = next(item for item in checker.findings if item.code == "HANDOVER_PAUSED")
        self.assertEqual("WARNING", finding.severity)
        self.assertIn("standalone TOOLS/handover.py checker", finding.message)
        self.assertIn("does not inspect the package", finding.message)

    def test_active_handover_rejected_in_unbound_kit(self) -> None:
        self.write("HANDOVER/ACTIVE.md", "")
        self.assert_code("HANDOVER_UNBOUND")

    def test_retained_completed_recovery_does_not_block(self) -> None:
        self.bind()
        self.write("RECOVERY/operation-01/RECORD.md", "# Recovery\n\nstatus: complete\n")
        self.assert_valid()

    def test_interrupted_save_directory_recovery_roundtrip(self) -> None:
        self.bind()
        self.archive_close()
        self.assert_valid()
        protected = ("INSTANCE/CURRENT_SAVE.md", "ARCHIVE/INDEX.md")
        before = {relative: (self.root / relative).read_bytes() for relative in protected}
        operation = "interrupted-save-03"
        session_directory = f"ARCHIVE/sessions/{operation}"
        nested_directory = session_directory + "/parts"
        new_files = (session_directory + "/INDEX.md", nested_directory + "/episode.md")
        directory_records = [("ARCHIVE/sessions", True, False), (session_directory, False, True), (nested_directory, False, True)]
        self.write(f"RECOVERY/{operation}/OPERATION.md", "# Recovery\n\nstatus: started\n\n" +
                   "\n".join(f"Directory: {path}; existed before: {old}; created by operation: {created}" for path, old, created in directory_records))
        self.write("RECOVERY/ACTIVE.md", f"operation_id: {operation}\nrecord: RECOVERY/{operation}/OPERATION.md\n")
        for relative, data in before.items():
            preimage = self.root / f"RECOVERY/{operation}/before/{relative}"
            preimage.parent.mkdir(parents=True, exist_ok=True)
            preimage.write_bytes(data)
            self.assertEqual(data, preimage.read_bytes())
        self.write(new_files[0], "# Incomplete session index\n")
        self.write(new_files[1], "# Failed staged evidence\n")
        self.write("INSTANCE/CURRENT_SAVE.md", "# Interrupted partial save\n")
        self.assert_code("RECOVERY_PENDING")

        for relative in protected:
            (self.root / relative).write_bytes((self.root / f"RECOVERY/{operation}/before/{relative}").read_bytes())
        for relative in new_files:
            target = (self.root / relative).resolve()
            target.relative_to(self.root.resolve())
            preserved = self.root / f"RECOVERY/{operation}/failed/{relative}"
            preserved.parent.mkdir(parents=True, exist_ok=True)
            preserved.write_bytes(target.read_bytes())
            target.unlink()
        self.assert_code("ARCHIVE_ORPHAN_SESSION")
        self.assertTrue((self.root / "RECOVERY/ACTIVE.md").exists())
        self.assertTrue((self.root / session_directory).is_dir())
        self.assertEqual([], list((self.root / nested_directory).iterdir()))
        self.assertTrue(all((self.root / relative).read_bytes() == data for relative, data in before.items()))

        removed = self.remove_recorded_empty_directories(directory_records)
        self.assertEqual([nested_directory, session_directory], removed)
        self.assertTrue((self.root / "ARCHIVE/sessions").is_dir())
        self.assertTrue((self.root / "ARCHIVE/sessions/save-02/episode.md").is_file())
        self.assertTrue((self.root / f"RECOVERY/{operation}/failed/{new_files[1]}").is_file())
        self.assertTrue(all((self.root / f"RECOVERY/{operation}/before/{relative}").read_bytes() == data for relative, data in before.items()))
        remaining = self.check().findings
        self.assertEqual({"RECOVERY_PENDING"}, {finding.code for finding in remaining if finding.severity in {"ERROR", "INCOMPLETE"}})
        self.write(f"RECOVERY/{operation}/OPERATION.md", "# Recovery\n\nstatus: restored\n\nProtected files and prior routes verified; listed empty new directories removed.\n")
        (self.root / "RECOVERY/ACTIVE.md").unlink()
        self.assert_valid()

    def test_recovery_preserves_preexisting_nonempty_and_uncreated_directories(self) -> None:
        records = [("scratch/preexisting", True, False), ("scratch/occupied", False, True), ("scratch/uncreated", False, False)]
        for relative, _old, _created in records:
            (self.root / relative).mkdir(parents=True)
        self.write("scratch/occupied/unexpected.md", "# Unrelated evidence\n\nPreserve this content.\n")
        (self.root / "scratch/unlisted").mkdir()
        self.assertEqual([], self.remove_recorded_empty_directories(records))
        self.assertTrue(all((self.root / relative).is_dir() for relative, _old, _created in records))
        self.assertTrue((self.root / "scratch/unlisted").is_dir())
        self.assertEqual("# Unrelated evidence\n\nPreserve this content.\n", self.read("scratch/occupied/unexpected.md"))

    def test_recovery_directory_cleanup_rejects_escapes_and_protected_material(self) -> None:
        self.write("RECOVERY/operation-01/OPERATION.md", "# Retained operation record\n")
        for relative in ("../outside", str(self.root), "RECOVERY/operation-01"):
            with self.subTest(path=relative), self.assertRaises(ValueError):
                self.remove_recorded_empty_directories([(relative, False, True)])
        self.assertTrue((self.root / "RECOVERY/operation-01/OPERATION.md").is_file())

    def test_optional_bearing_staleness_warns(self) -> None:
        self.bind()
        values = dict(campaign_id="brine-01", base_save_id="older-save", base_contract_id="agreement-01", status="provisional")
        self.write("INSTANCE/BEARING.md", record("Review notes", values, {"Provisional thoughts": "No preference inferred from one action."}))
        self.assert_valid()
        self.assert_code("BEARING_STALE_BASE", "WARNING")

    def test_changed_law_is_observed_not_rejected(self) -> None:
        self.write("OS/LAW.md", "# A revised GM core\n\nFollow the accepted agreement and portray the world.\n")
        checker = self.assert_valid()
        self.assertEqual(validate.sha256_bytes((self.root / "OS/LAW.md").read_bytes()), checker.metrics["law_sha256"])

    def test_missing_new_recovery_procedure(self) -> None:
        (self.root / "ADMIN/RECOVERY.md").unlink()
        self.assert_code("CORE_REQUIRED_FILE")

    def test_unbound_cannot_contain_prior_pc(self) -> None:
        self.write("INSTANCE/CHAR/PC.md", "# Prior character\n\nAn earlier campaign character.\n")
        self.assert_code("INSTANCE_INITIAL_CONTENT")

    def test_bind_rejects_changed_character_copy(self) -> None:
        self.bind()
        self.write("INSTANCE/CHAR/PC.md", "# Iri\n\nUnaccepted additional powers.\n")
        self.assert_code("PC_BIND_COPY_MISMATCH")

    def test_bind_rejects_changed_opening_body(self) -> None:
        self.bind()
        self.write("MODULES/brine/T0_SAVE.md", self.read("MODULES/brine/T0_SAVE.md").replace("Opening scene.", "A different accepted opening."))
        self.assert_code("T0_BIND_SECTION")

    def test_bind_rejects_prior_person_record(self) -> None:
        self.bind()
        self.write("INSTANCE/PEOPLE/prior-person.md", "# Prior person\n\nA record carried from another run.\n")
        self.assert_code("INSTANCE_INITIAL_CONTENT")

    def test_upgraded_campaign_preserves_legacy_t0_source(self) -> None:
        self.bind()
        self.save.update(save_id="save-02", save_rev="2", save_parent="save-01", commit_kind="checkpoint")
        self.flush()
        legacy = record("T0_SAVE", dict(engine="freeform", module="brine", immediate_scene="Iri observes the rising water.", datetime="Third tide", place="Tidal observatory"), {})
        self.write("MODULES/brine/T0_SAVE.md", legacy)
        self.assert_valid()
        self.assert_code("T0_LEGACY_MAPPING", "WARNING")
        self.assertEqual(legacy, self.read("MODULES/brine/T0_SAVE.md"))
        self.write("MODULES/brine/T0_SAVE.md", legacy.replace("| engine | freeform |", "| engine | unknown-engine |"))
        self.assert_code("T0_BINDING_MISMATCH")

    def test_no_writes_and_honest_scope_in_json_report(self) -> None:
        self.bind()
        before, _ = validate.snapshot_tree(self.root)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = validate.main(["--root", str(self.root), "--json"])
        after, _ = validate.snapshot_tree(self.root)
        report = json.loads(output.getvalue())
        self.assertEqual(0, code, report["findings"])
        self.assertEqual(before, after)
        self.assertTrue(report["tree_stable_during_run"])
        self.assertTrue(report["target_validator_matches_executed"])
        self.assertEqual("NOT RUN", report["host_observation"]["result"])
        self.assertEqual("NOT CHECKED", report["semantic"]["result"])

    def test_target_validator_mismatch_has_valid_diagnostic_fields(self) -> None:
        self.bind()
        target = self.root / "TOOLS/validate.py"
        target.write_text(target.read_text(encoding="utf-8") + "\n# Different disposable target bytes.\n", encoding="utf-8")
        before, _ = validate.snapshot_tree(self.root)
        code, report = self.run_report()
        after, _ = validate.snapshot_tree(self.root)
        self.assertEqual(2, code)
        self.assertEqual("INCOMPLETE", report["structural"]["result"])
        self.assertFalse(report["target_validator_matches_executed"])
        self.assertTrue(report["tree_stable_during_run"])
        self.assertEqual(before, after)
        finding = next(item for item in report["findings"] if item["code"] == "VALIDATOR_TARGET_MISMATCH")
        self.assertEqual("the target validator was not byte-identical to the executed validator for the full run", finding["message"])
        self.assertEqual("TOOLS/validate.py", finding["path"])
        self.assertIsNone(finding["line"])

    def test_changed_executed_validator_has_valid_diagnostic_fields(self) -> None:
        self.bind()
        module_name = "disposable_validator_" + self.root.name.replace("-", "_")
        spec = importlib.util.spec_from_file_location(module_name, self.root / "TOOLS/validate.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        self.addCleanup(sys.modules.pop, module_name, None)
        spec.loader.exec_module(module)
        original_run = module.Validator.run
        production_bytes = (HERE / "validate.py").read_bytes()

        def mutate_only_disposable_file(checker, initial_snapshot):
            original_run(checker, initial_snapshot)
            path = Path(module.__file__).resolve()
            path.relative_to(self.root.resolve())
            path.write_text(path.read_text(encoding="utf-8") + "\n# Disposable file changed during execution.\n", encoding="utf-8")

        module.Validator.run = mutate_only_disposable_file
        code, report = self.run_report(module)
        self.assertEqual(2, code)
        self.assertEqual("INCOMPLETE", report["structural"]["result"])
        self.assertFalse(report["tree_stable_during_run"])
        self.assertFalse(report["target_validator_matches_executed"])
        expected_messages = {
            "VALIDATOR_CHANGED_DURING_RUN": "the executed validator file changed while validation ran",
            "VALIDATOR_TARGET_MISMATCH": "the target validator was not byte-identical to the executed validator for the full run",
        }
        for diagnostic, message in expected_messages.items():
            finding = next(item for item in report["findings"] if item["code"] == diagnostic)
            self.assertEqual(message, finding["message"])
            self.assertEqual("TOOLS/validate.py", finding["path"])
            self.assertIsNone(finding["line"])
        self.assertTrue(all(item["line"] is None or type(item["line"]) is int for item in report["findings"]))
        self.assertEqual(production_bytes, (HERE / "validate.py").read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)
