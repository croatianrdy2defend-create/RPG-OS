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
            "Campaign promise": "Quiet exploration in an original tidal world; no imported franchise lore.",
            "Player control": "Player chooses Iri's voluntary conduct and commitments. No routine authorship delegated.",
            "GM initiative": "GM portrays the world and NPCs, resolves live processes, and may invent ordinary compatible texture.",
            "Time and transitions": "Carry declared sequences until a meaningful new choice; no undeclared hard cuts.",
            "Presentation": "Clear sensory prose with brief public status. Optional guidance in ordinary prose.",
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

    def test_retained_completed_recovery_does_not_block(self) -> None:
        self.bind()
        self.write("RECOVERY/operation-01/RECORD.md", "# Recovery\n\nstatus: complete\n")
        self.assert_valid()

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
