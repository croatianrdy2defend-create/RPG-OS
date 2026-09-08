#!/usr/bin/env python3
"""Autosave scheduler unit tests; repository instruction/route checks.

These tests do not run an LLM or certify complete saves/host context retention.
Run from an installed kit: python -B TOOLS/test_autosave.py
"""
from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from autosave import Observation, decide, from_mapping, unique_object

ROOT = Path(__file__).resolve().parent.parent


class SchedulerTests(unittest.TestCase):
    def sample(self, **changes):
        return replace(Observation(enabled=True, dirty=True, turn=15, turns_since_save=15), **changes)

    def test_default_off(self):
        self.assertEqual(decide(Observation(dirty=True, consequential=True)).reason, "disabled")

    def test_clean_state_never_creates_empty_autosaves(self):
        self.assertEqual(decide(self.sample(dirty=False, context_percent=99, context_source="host")).action, "none")

    def test_interval_warns_before_saving(self):
        warning = decide(self.sample())
        self.assertEqual((warning.action, warning.warned_at), ("warn", 15))
        self.assertEqual(decide(self.sample(warned_at=15)).action, "wait")
        self.assertEqual(decide(self.sample(turn=16, warned_at=15)).action, "checkpoint")

    def test_each_event_trigger_warns(self):
        for changes in ({"consequential": True}, {"scene_boundary": True}):
            with self.subTest(changes=changes):
                self.assertEqual(decide(self.sample(turns_since_save=1, **changes)).action, "warn")

    def test_pressure_only_uses_sourced_values(self):
        for source in ("host", "operator"):
            self.assertEqual(decide(self.sample(turns_since_save=1, context_percent=65, context_source=source)).action, "warn")
        self.assertEqual(decide(self.sample(turns_since_save=1, context_percent=64, context_source="host")).action, "none")
        self.assertEqual(decide(self.sample(turns_since_save=1)).action, "none")

    def test_high_pressure_does_not_bypass_warning(self):
        self.assertEqual(decide(self.sample(context_percent=99, context_source="operator")).action, "warn")

    def test_handled_pressure_does_not_loop_after_checkpoint(self):
        o = self.sample(turns_since_save=1, context_percent=70, context_source="host", context_handled=True)
        self.assertEqual(decide(o).action, "none")
        self.assertEqual(decide(replace(o, consequential=True)).action, "warn")
        self.assertEqual(decide(replace(o, turns_since_save=15)).action, "warn")

    def test_context_episode_rearms_only_when_caller_observes_reset(self):
        low = self.sample(turns_since_save=1, context_percent=60, context_source="operator", context_handled=False)
        self.assertEqual(decide(low).action, "none")
        self.assertEqual(decide(replace(low, context_percent=66)).action, "warn")
        fresh = Observation(enabled=True, dirty=True, context_percent=66, context_source="host")
        self.assertEqual(decide(fresh).action, "warn")

    def test_triggers_coalesce_and_do_not_repeat_notice(self):
        decision = decide(self.sample(turn=16, warned_at=15, consequential=True, scene_boundary=True))
        self.assertEqual(decision.action, "checkpoint")
        self.assertEqual(decision.warned_at, 15)

    def test_ooc_and_tool_calls_do_not_advance_notice_turn(self):
        for _ in range(4):
            self.assertEqual(decide(self.sample(warned_at=15)).action, "wait")

    def test_operator_deferral_always_wins_over_auto_pressure(self):
        self.assertEqual(decide(self.sample(deferred=True, context_percent=100, context_source="host")).action, "deferred")

    def test_disable_cancels_pending_automatic_operation(self):
        decision = decide(self.sample(enabled=False, warned_at=14))
        self.assertEqual((decision.action, decision.warned_at), ("none", None))

    def test_explicit_manual_save_supersedes_warning_and_deferral(self):
        for kind in ("checkpoint", "close"):
            self.assertEqual(decide(self.sample(enabled=False, deferred=True, manual=kind)).action, kind)

    def test_manual_close_is_never_downgraded_to_checkpoint(self):
        self.assertEqual(decide(self.sample(manual="close", warned_at=14)).action, "close")

    def test_recovery_and_handover_block_even_manual_save(self):
        for flag in ("recovery_active", "handover_active", "write_in_progress"):
            for kind in (None, "checkpoint", "close"):
                with self.subTest(flag=flag, kind=kind):
                    self.assertEqual(decide(self.sample(manual=kind, **{flag: True})).action, "blocked")

    def test_recovery_has_precedence_over_handover(self):
        self.assertEqual(decide(self.sample(recovery_active=True, handover_active=True)).reason, "recovery")

    def test_unavailable_persistence_is_not_success(self):
        for kind in (None, "checkpoint", "close"):
            self.assertEqual(decide(self.sample(persistence_available=False, manual=kind)).action, "unavailable")

    def test_unfinished_operation_defers_but_keeps_notice(self):
        result = decide(self.sample(safe_boundary=False, warned_at=14))
        self.assertEqual((result.action, result.warned_at), ("wait", 14))

    def test_eligible_checkpoint_is_not_a_verified_save(self):
        o = self.sample(turn=16, warned_at=15)
        result = decide(o)
        self.assertEqual(result.action, "checkpoint")
        self.assertEqual(result.warned_at, 15)
        self.assertTrue(o.dirty)
        self.assertEqual(o.turns_since_save, 15)

    def test_failure_blocks_and_preserves_pending_notice(self):
        result = decide(self.sample(turn=16, warned_at=15, recovery_active=True))
        self.assertEqual((result.action, result.warned_at), ("blocked", 15))

    def test_verified_save_reset_avoids_duplicate_checkpoint(self):
        result = decide(self.sample(turns_since_save=0, dirty=False, warned_at=None))
        self.assertEqual(result.action, "none")

    def test_bad_values_are_rejected(self):
        cases = [dict(enabled="false"), dict(turn=-1), dict(turn=True), dict(interval=0),
                 dict(warned_at=16), dict(warned_at=True), dict(context_percent=float("nan"), context_source="host"),
                 dict(context_percent=101, context_source="host"), dict(context_percent=70),
                 dict(context_source="host"), dict(context_source="estimate", context_percent=70),
                 dict(context_threshold=0), dict(manual="save"), dict(safe_boundary=1),
                 dict(context_handled=1), dict(context_percent=10**400, context_source="host")]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                decide(self.sample(**changes))

    def test_unknown_fields_and_duplicate_fields_are_rejected(self):
        for data in ([], {"enable": True}, {"context_percent": 70}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                from_mapping(data)
        with self.assertRaises(ValueError):
            json.loads('{"enabled":false,"enabled":true}', object_pairs_hook=unique_object)

    def test_roundtrip_and_custom_interval(self):
        o = self.sample(interval=20)
        self.assertEqual(from_mapping(asdict(o)), o)
        self.assertEqual(decide(o).action, "none")

    def test_cli_has_no_filesystem_side_effects(self):
        script = ROOT / "TOOLS/autosave.py"
        with tempfile.TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, "-B", str(script)], input=json.dumps(asdict(self.sample())),
                                    text=True, capture_output=True, cwd=folder)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["action"], "warn")
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_cli_errors_are_not_decisions(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "TOOLS/autosave.py")],
                                input='{"enabled": "yes"}', text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error", json.loads(result.stderr))


class ProtocolTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_protocol_safeguards(self):
        body = self.read("ADMIN/AUTOSAVE.md")
        for phrase in ("off unless explicitly accepted", "one response before", "15 completed PLAY replies",
                       "65%", "operator-reported", "not fictional safety", "No background",
                       "complete present", "archive_ref", "evidence_through", "CURRENT_SAVE last",
                       "full CLOSE", "not a guarantee", "do not reconstruct", "READ-ONLY",
                       "RECOVERY/ACTIVE.md", "HANDOVER/ACTIVE.md", "delay autosave", "context_handled"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), body.casefold())

    def test_runtime_routes_are_integrated(self):
        for path in ("OS/LAW.md", "OS/BOOTSTRAP.md", "ADMIN/CLOSE_CONTRACT.md", "ADMIN/NEW_GAME.md",
                     "ADMIN/RECALIBRATE.md", "README.md", "COMMANDS.md"):
            with self.subTest(path=path):
                self.assertIn("ADMIN/AUTOSAVE.md", self.read(path))

    def test_both_workflows_execute_new_suite(self):
        for path in (".github/workflows/validate.yml", ".github/workflows/release.yml"):
            self.assertIn("TOOLS/test_autosave.py", self.read(path))

    def test_behavioral_cases_honestly_unrun(self):
        body = self.read("ADMIN/TEST_AUTOSAVE.md")
        self.assertIn("Behavioral status: **NOT RUN**", body)
        for number in range(1, 11):
            self.assertIn(f"### A{number:02d} —", body)

    def test_current_release_has_notes_and_prior_notes_survive(self):
        version = self.read("VERSION").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (0, 9, 2))
        self.assertTrue((ROOT / f"V{version}_CHANGES.md").is_file())
        self.assertTrue((ROOT / "V0.9.1_CHANGES.md").is_file())


class PersistenceIntegrationTests(unittest.TestCase):
    """Synthetic metadata fixtures, not a model-operated checkpoint implementation."""
    def fixture(self):
        from test_validate import StructuralValidationTests
        fixture = StructuralValidationTests(methodName="test_clean_unbound")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture

    def test_old_agreement_stays_valid_without_autosave(self):
        fixture = self.fixture()
        fixture.bind()
        fixture.assert_valid()
        self.assertNotIn("Autosave:", fixture.read("INSTANCE/CAMPAIGN_CONTRACT.md"))

    def test_opt_in_uses_existing_agreement_without_new_schema(self):
        fixture = self.fixture()
        fixture.bind()
        fixture.contract_sections["GM initiative"] += "\n\nAutosave: Enabled under ADMIN/AUTOSAVE.md; announce one response before a protected complete-present checkpoint."
        fixture.flush()
        fixture.assert_valid()

    def test_auto_checkpoint_keeps_evidence_and_pending_choice(self):
        fixture = self.fixture()
        fixture.bind()
        fixture.archive_close()
        archive_before = {p.relative_to(fixture.root): p.read_bytes() for p in (fixture.root / "ARCHIVE").rglob("*") if p.is_file()}
        prior_evidence = (fixture.save["archive_ref"], fixture.save["evidence_through"])
        prior_time = fixture.save["datetime"]
        pending = "The player has not decided which outlet to inspect. No time passes at this checkpoint."
        fixture.save_sections["Situation"] = pending
        decision = decide(Observation(enabled=True, dirty=True, turn=16, turns_since_save=16, warned_at=15))
        self.assertEqual(decision.action, "checkpoint")
        fixture.save.update(save_id="save-03", save_rev="3", save_parent="save-02", commit_kind="checkpoint")
        fixture.flush()
        fixture.assert_valid()
        self.assertEqual(prior_evidence, (fixture.save["archive_ref"], fixture.save["evidence_through"]))
        self.assertEqual(prior_time, fixture.save["datetime"])
        self.assertIn(pending, fixture.read("INSTANCE/CURRENT_SAVE.md"))
        self.assertEqual(archive_before, {p.relative_to(fixture.root): p.read_bytes() for p in (fixture.root / "ARCHIVE").rglob("*") if p.is_file()})


if __name__ == "__main__":
    unittest.main(verbosity=2)
