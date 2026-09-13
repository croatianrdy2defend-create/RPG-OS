#!/usr/bin/env python3
"""Focused handover checks using isolated OS-temp fixtures; no live campaign writes.

Run: python -B TOOLS/test_handover.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("rpg_handover", Path(__file__).with_name("handover.py"))
assert SPEC and SPEC.loader
handover = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handover)


def document(title, manifest, sections):
    parts = [f"# {title}", "## Manifest", "```json\n" + json.dumps(manifest, indent=2) + "\n```"]
    for name in sections:
        if name != "Manifest":
            parts.extend((f"## {name}", "Synthetic established state; no unrecorded action resolved."))
    return "\n\n".join(parts) + "\n"


class HandoverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rpg-handover-tests-")
        self.root = Path(self.temp.name)
        self.temp_boundary = Path(tempfile.gettempdir()).resolve()
        self.addCleanup(self.cleanup_fixture)
        for name in handover.TREES:
            self.write(f"{name}/README.md", f"# Synthetic {name}\n")
        self.write("README.md", "# Synthetic root\n")
        self.write("MODULES/synthetic/VISUAL/reference.bin", "synthetic bytes")
        self.write("INSTANCE/CURRENT_SAVE.md", "| campaign_id | campaign-1 |\n| save_id | save-1 |\n")
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", "| campaign_id | campaign-1 |\n| contract_id | contract-1 |\n| status | accepted |\n")
        self.package = "HANDOVER/handover-1"
        self.lineage = dict(handover_id="handover-1", campaign_id="campaign-1",
                            base_save_id="save-1", base_contract_id="contract-1")
        self.write(f"{self.package}/CONVERSATION.md", "# Conversation\n\n## Coverage\n\nComplete synthetic fixture.\n\n## Messages\n\nPlayer: Wait here.\nGM: The room remains quiet.\n")
        self.outgoing = dict(schema="scene-handover-v1", **self.lineage,
                             conversation_sha256=handover.digest(self.root / self.package / "CONVERSATION.md"),
                             snapshot_files=handover.snapshot(self.root), source_coverage="complete", source_gaps=[])
        self.flush_outgoing()
        self.incoming = dict(schema="scene-return-v1", **self.lineage,
                             gm_state_sha256=handover.digest(self.root / self.package / "GM_STATE.md"),
                             event_ids=["event-1"])
        self.flush_return()

    def cleanup_fixture(self):
        resolved = self.root.resolve()
        if resolved.parent != self.temp_boundary or not resolved.name.startswith("rpg-handover-tests-"):
            raise RuntimeError("refusing cleanup outside the isolated OS-temp fixture boundary")
        self.temp.cleanup()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def flush_outgoing(self, seal_active=True):
        self.write(f"{self.package}/GM_STATE.md", document("GM State", self.outgoing, handover.GM_SECTIONS))
        if seal_active:
            values = dict(self.lineage, package=self.package,
                          gm_state_sha256=handover.digest(self.root / self.package / "GM_STATE.md"))
            self.write("HANDOVER/ACTIVE.md", "\n".join(f"{key}: {value}" for key, value in values.items()) + "\n")

    def flush_return(self):
        self.write(f"{self.package}/SCENE_RETURN.md", document("Scene Return", self.incoming, handover.RETURN_SECTIONS))

    def receipt(self, status="imported", **changes):
        fields = dict(self.lineage, status=status, resulting_save_id="save-2")
        if status == "imported":
            fields.update(return_sha256=handover.digest(self.root / self.package / "SCENE_RETURN.md"),
                          accepted_event_ids='["event-1"]')
        else:
            fields["reason"] = "The player cancelled the proposed continuation."
        fields.update(changes)
        self.write(f"{self.package}/RECEIPT.md", "\n".join(f"{key}: {value}" for key, value in fields.items()) + "\n")

    def run_cli(self, *arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = handover.main(["check", "--root", str(self.root), "--package", self.package, *arguments])
        return code, json.loads(output.getvalue())

    def assert_invalid(self, fragment, *arguments):
        code, result = self.run_cli(*arguments)
        self.assertEqual(code, 1, result)
        self.assertIn(fragment, result["errors"][0])

    def test_happy_outgoing_and_return_are_read_only(self):
        before = {path.relative_to(self.root).as_posix(): handover.digest(path)
                  for path in self.root.rglob("*") if path.is_file()}
        for args in ((), ("--return",)):
            code, result = self.run_cli(*args)
            self.assertEqual(code, 0, result)
            self.assertEqual(result["status"], "pass")
        after = {path.relative_to(self.root).as_posix(): handover.digest(path)
                 for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_snapshot_recipe_excludes_non_campaign_trees(self):
        for name in ("RECOVERY", "HANDOVER", ".release", ".work", "output", "TOOLS", "EVIDENCE"):
            self.write(f"{name}/not-in-closure.md", "excluded")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = handover.main(["snapshot", "--root", str(self.root)])
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["snapshot_files"], self.outgoing["snapshot_files"])

    def log_fixture(self, reviewed=False):
        self.write("INSTANCE/JOURNAL/HEAD.json", json.dumps({
            "schema": "rpg-journal-v2", "recording": "write-only-log",
            "published_save_ids": ["save-1"],
            "public_source_anchor": {"path": "ARCHIVE/sessions/save-1/01_record.md"},
            "public_source_floor": {"source_ref": {"path": "Z:/unavailable/host.jsonl"}}}))
        self.write("INSTANCE/PLAY_LOG.jsonl", "")
        self.write("ARCHIVE/sessions/save-1/01_record.md", "Retained original public source.")
        for name in handover.LOG_RUNTIME:
            self.write("TOOLS/" + name, "# synthetic runtime dependency\n")
        self.write("TOOLS/test_unrelated.py", "excluded test")
        self.write("EVIDENCE/unrelated/private.txt", "excluded unrelated evidence")
        review = {"status": "incomplete"}
        if reviewed:
            review = {"status": "complete", "receipt": {
                "bundle": "EVIDENCE/reviews/save-1",
                "report": "EVIDENCE/reviews/save-1/report.json",
                "report_sha256": "a" * 64,
                "delivery_receipt": "EVIDENCE/delivery/save-1.jsonl"}}
            self.write("EVIDENCE/reviews/save-1/bundle.json", "{}")
            self.write("EVIDENCE/reviews/save-1/capture/source.txt", "Exact retained source.")
            self.write("EVIDENCE/reviews/save-1/report.json", "{}")
            self.write("EVIDENCE/delivery/save-1.jsonl", "{}\n")
        self.write("EVIDENCE/incremental-reviews/save-1.json", json.dumps({"review": review}))

    def test_log_snapshot_carries_runtime_and_exact_retained_review_dependencies(self):
        self.log_fixture(reviewed=True)
        files = handover.snapshot(self.root)
        for name in handover.LOG_RUNTIME:
            self.assertIn("TOOLS/" + name, files)
        for path in ("EVIDENCE/incremental-reviews/save-1.json",
                     "EVIDENCE/reviews/save-1/bundle.json",
                     "EVIDENCE/reviews/save-1/capture/source.txt",
                     "EVIDENCE/reviews/save-1/report.json",
                     "EVIDENCE/delivery/save-1.jsonl",
                     "ARCHIVE/sessions/save-1/01_record.md"):
            self.assertIn(path, files)
        self.assertNotIn("TOOLS/test_unrelated.py", files)
        self.assertNotIn("EVIDENCE/unrelated/private.txt", files)
        self.outgoing["snapshot_files"] = files
        self.flush_outgoing()
        code, result = self.run_cli()
        self.assertEqual(code, 0, result)
        self.write("EVIDENCE/reviews/save-1/capture/source.txt", "Changed after freeze.")
        self.assert_invalid("snapshot hash mismatch")

    def test_log_snapshot_requires_runtime_even_without_complete_review(self):
        self.log_fixture()
        self.assertIn("EVIDENCE/incremental-reviews/save-1.json", handover.snapshot(self.root))
        with mock.patch.object(handover, "safe_path", wraps=handover.safe_path) as access:
            handover.snapshot(self.root)
        self.assertFalse(any("unavailable" in str(call) for call in access.call_args_list))
        (self.root / "TOOLS/play_log.py").unlink()
        with self.assertRaisesRegex(handover.Invalid, "missing path"):
            handover.snapshot(self.root)

    def test_log_snapshot_refuses_missing_referenced_review_dependency(self):
        self.log_fixture(reviewed=True)
        (self.root / "EVIDENCE/reviews/save-1/report.json").unlink()
        with self.assertRaisesRegex(handover.Invalid, "missing path"):
            handover.snapshot(self.root)

    def test_log_snapshot_refuses_unsafe_or_nonretained_review_dependency(self):
        self.log_fixture(reviewed=True)
        receipt_path = "EVIDENCE/incremental-reviews/save-1.json"
        original = json.loads((self.root / receipt_path).read_text(encoding="utf-8"))
        for path in ("../outside", "Z:/host/source", "RECOVERY/private", "EVIDENCE"):
            with self.subTest(path=path):
                changed = json.loads(json.dumps(original))
                changed["review"]["receipt"]["bundle"] = path
                self.write(receipt_path, json.dumps(changed))
                with self.assertRaises(handover.Invalid):
                    handover.snapshot(self.root)

    def test_log_snapshot_requires_explicit_current_review_route(self):
        self.log_fixture()
        self.write("INSTANCE/CURRENT_SAVE.md", "| save_id | save-2 |\n"
                   "Review: `EVIDENCE/incremental-reviews/missing.json`.\n")
        with self.assertRaisesRegex(handover.Invalid, "missing path"):
            handover.snapshot(self.root)

    def test_legacy_journal_keeps_original_snapshot_recipe(self):
        self.write("INSTANCE/JOURNAL/HEAD.json", json.dumps({"schema": "rpg-journal-v1"}))
        self.write("TOOLS/persistence.py", "not selected")
        self.write("EVIDENCE/incremental-reviews/save-1.json", "not selected")
        files = handover.snapshot(self.root)
        self.assertIn("INSTANCE/JOURNAL/HEAD.json", files)
        self.assertNotIn("TOOLS/persistence.py", files)
        self.assertNotIn("EVIDENCE/incremental-reviews/save-1.json", files)

    def test_stale_base_save(self):
        self.write("INSTANCE/CURRENT_SAVE.md", "| campaign_id | campaign-1 |\n| save_id | save-2 |\n")
        self.assert_invalid("base save identity mismatch")

    def test_stale_base_contract(self):
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", "| campaign_id | campaign-1 |\n| contract_id | contract-2 |\n| status | accepted |\n")
        self.assert_invalid("base contract identity mismatch")

    def test_changed_snapshot_file(self):
        self.write("MODULES/README.md", "changed established lore")
        self.assert_invalid("snapshot hash mismatch")

    def test_saved_agent_and_session_owners_are_covered_without_new_transport_schema(self):
        # These are ordinary existing owners; the checker protects their bytes,
        # not the receiving GM's interpretation or portrayal of these facts.
        owners = {
            "OS/AGENT_STATE.md": "# Agent state\n\nCold procedure in the matching source workspace.\n",
            "INSTANCE/PEOPLE/tavi.md": "# Tavi\n\nDislikes Iri's criticism but trusts its work. Promised access until fourth tide. Mistakenly believes the west channel is closed. Personal interests remain unfixed.\n",
            "INSTANCE/NOW.md": "# NOW\n\n## Sluice watch\n\nAccess expires at fourth tide. No earlier inspection is due.\n",
            "INSTANCE/KNOWN.md": "# KNOWN\n\nIri heard the claim that the west channel is closed; it is unverified.\n",
            "ADMIN/SESSION.md": "# Session procedure\n\nTransfer preserves the actual play-session identity.\n",
            "INSTANCE/CURRENT_SAVE.md": "| campaign_id | campaign-1 |\n| save_id | save-1 |\n\n## Session continuity\n\n| Session item | Value |\n|---|---|\n| session_id | play-session-1 |\n| phase | active |\n| opening_save | save-0 |\n| feedback | not-due |\n\nEarlier feedback for play-session-0 is pending; preserve its actual source.\n",
            "INSTANCE/PREP.md": "# PREP\n\nDerivative notes only. Recheck changed conditions before using a conditional opportunity; previous completion remains settled.\n",
        }
        for relative, content in owners.items():
            self.write(relative, content)
        self.outgoing["snapshot_files"] = handover.snapshot(self.root)
        self.flush_outgoing()
        self.incoming["gm_state_sha256"] = handover.digest(self.root / self.package / "GM_STATE.md")
        self.flush_return()
        before = {relative: (self.root / relative).read_bytes() for relative in owners}
        for relative in owners:
            self.assertEqual(self.outgoing["snapshot_files"][relative], handover.digest(self.root / relative))
        for args in ((), ("--return",)):
            code, result = self.run_cli(*args)
            self.assertEqual(code, 0, result)
        self.assertEqual(before, {relative: (self.root / relative).read_bytes() for relative in owners})
        for relative, content in owners.items():
            with self.subTest(path=relative):
                self.write(relative, content + "\nChanged after source freeze.\n")
                self.assert_invalid("snapshot hash mismatch", "--return")
                self.write(relative, content)
        self.outgoing["snapshot_files"].pop("INSTANCE/PREP.md")
        self.flush_outgoing()
        self.incoming["gm_state_sha256"] = handover.digest(self.root / self.package / "GM_STATE.md")
        self.flush_return()
        self.assert_invalid("snapshot coverage mismatch", "--return")

    def test_omitted_snapshot_file(self):
        self.outgoing["snapshot_files"].pop("MODULES/README.md")
        self.flush_outgoing()
        self.assert_invalid("snapshot coverage mismatch")

    def test_added_snapshot_file(self):
        self.write("MODULES/new.md", "new fact")
        self.assert_invalid("snapshot coverage mismatch")

    def test_missing_coverage_declaration(self):
        del self.outgoing["source_coverage"]
        self.flush_outgoing()
        self.assert_invalid("source_coverage must declare")

    def test_partial_coverage_reports_warning(self):
        self.outgoing.update(source_coverage="partial", source_gaps=["Earlier messages unavailable after compaction."])
        self.flush_outgoing()
        code, result = self.run_cli()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["status"], "pass_with_warnings")
        self.assertIn("WARNING", result["warnings"][0])

    def test_partial_coverage_requires_gap_description(self):
        self.outgoing["source_coverage"] = "partial"
        self.flush_outgoing()
        self.assert_invalid("partial/summary coverage must describe gaps")

    def test_edited_conversation(self):
        path = self.root / self.package / "CONVERSATION.md"
        self.write(f"{self.package}/CONVERSATION.md", path.read_text(encoding="utf-8") + "changed dialogue\n")
        self.assert_invalid("conversation hash mismatch")

    def test_missing_required_heading(self):
        path = self.root / self.package / "GM_STATE.md"
        self.write(f"{self.package}/GM_STATE.md", path.read_text(encoding="utf-8").replace("## Stop point", "## Different heading"))
        self.assert_invalid("missing or empty ## Stop point")

    def test_duplicate_manifest(self):
        path = self.root / self.package / "GM_STATE.md"
        self.write(f"{self.package}/GM_STATE.md", path.read_text(encoding="utf-8") + "\n## Manifest\n\n```json\n{}\n```\n")
        self.assert_invalid("duplicate heading Manifest")

    def test_duplicate_json_key(self):
        path = self.root / self.package / "GM_STATE.md"
        original = path.read_text(encoding="utf-8")
        changed = original.replace('"source_coverage": "complete",', '"source_coverage": "complete", "source_coverage": "complete",')
        self.write(f"{self.package}/GM_STATE.md", changed)
        self.assert_invalid("duplicate JSON key")

    def test_duplicate_events(self):
        self.incoming["event_ids"] = ["event-1", "event-1"]
        self.flush_return()
        self.assert_invalid("duplicate event_ids", "--return")

    def test_no_change_return(self):
        self.incoming["event_ids"] = []
        self.flush_return()
        code, result = self.run_cli("--return")
        self.assertEqual(code, 0, result)
        self.assertEqual(result["event_count"], 0)

    def test_wrong_return_parent(self):
        self.incoming["base_save_id"] = "save-2"
        self.flush_return()
        self.assert_invalid("return base_save_id mismatch", "--return")

    def test_wrong_return_gm_hash(self):
        self.incoming["gm_state_sha256"] = "0" * 64
        self.flush_return()
        self.assert_invalid("return GM_STATE hash mismatch", "--return")

    def test_imported_and_cancelled_receipts_block_replay(self):
        for status in ("imported", "cancelled"):
            self.receipt(status)
            self.assert_invalid(f"handover already resolved: {status}", "--return")

    def test_malformed_receipt_fails(self):
        self.receipt("maybe")
        self.assert_invalid("malformed RECEIPT status")

    def test_incomplete_receipt_fails(self):
        self.write(f"{self.package}/RECEIPT.md", "handover_id: handover-1\nstatus: imported\n")
        self.assert_invalid("RECEIPT: missing field campaign_id")

    def test_cross_campaign_receipt_fails(self):
        self.receipt(campaign_id="different-campaign")
        self.assert_invalid("RECEIPT campaign_id mismatch")

    def test_resolved_receipt_uses_frozen_lineage_not_current_save(self):
        self.receipt()
        self.write("INSTANCE/CURRENT_SAVE.md", "| campaign_id | campaign-1 |\n| save_id | save-9 |\n")
        (self.root / "HANDOVER/ACTIVE.md").unlink()
        self.assert_invalid("handover already resolved: imported", "--return")

    def test_receipt_requires_safe_identifiers_hash_and_unique_event_list(self):
        cases = (
            ({"resulting_save_id": "../save"}, "RECEIPT resulting_save_id"),
            ({"return_sha256": "invalid"}, "RECEIPT return_sha256"),
            ({"accepted_event_ids": "not JSON"}, "must be a JSON list"),
            ({"accepted_event_ids": '{}'}, "must be a list"),
            ({"accepted_event_ids": '["event-1", "event-1"]'}, "duplicate RECEIPT accepted_event_ids"),
            ({"accepted_event_ids": '["../event"]'}, "RECEIPT accepted_event_ids entry"),
        )
        for changes, fragment in cases:
            with self.subTest(changes=changes):
                self.receipt(**changes)
                self.assert_invalid(fragment)

    def test_receipt_allows_empty_event_list(self):
        self.receipt(accepted_event_ids="[]")
        self.assert_invalid("handover already resolved: imported")

    def test_cancelled_receipt_requires_reason(self):
        self.receipt("cancelled", reason="")
        self.assert_invalid("cancelled status requires reason")

    def test_active_marker_required_and_bound(self):
        active = self.root / "HANDOVER/ACTIVE.md"
        self.write("HANDOVER/ACTIVE.md", active.read_text(encoding="utf-8").replace("handover_id: handover-1", "handover_id: different"))
        self.assert_invalid("ACTIVE handover_id mismatch")
        (self.root / "HANDOVER/ACTIVE.md").unlink()
        self.assert_invalid("missing path")

    def test_active_requires_gm_seal(self):
        active = self.root / "HANDOVER/ACTIVE.md"
        self.write("HANDOVER/ACTIVE.md", "\n".join(line for line in active.read_text(encoding="utf-8").splitlines()
                                                  if not line.startswith("gm_state_sha256:")))
        self.assert_invalid("ACTIVE: missing field gm_state_sha256")

    def test_changed_briefing_cannot_be_resealed_by_return_alone(self):
        gm = self.root / self.package / "GM_STATE.md"
        self.write(f"{self.package}/GM_STATE.md", gm.read_text(encoding="utf-8") + "\nInvented later development.\n")
        self.incoming["gm_state_sha256"] = handover.digest(gm)
        self.flush_return()
        self.assert_invalid("ACTIVE GM_STATE hash mismatch", "--return")

    def test_unsafe_snapshot_routes(self):
        for route in ("../escape.md", "/absolute.md", "C:/outside.md", "OS/../outside.md", "OS\\outside.md", "OS/NUL.md"):
            with self.subTest(route=route):
                self.outgoing["snapshot_files"][route] = "0" * 64
                self.flush_outgoing()
                code, result = self.run_cli()
                self.assertEqual(code, 1, result)
                del self.outgoing["snapshot_files"][route]

    def test_unsafe_package_route(self):
        self.package = "HANDOVER/../handover-1"
        self.assert_invalid("unsafe route")

    def test_symlink_refused_where_supported(self):
        link = self.root / "MODULES/link.md"
        try:
            link.symlink_to(self.root / "OS/README.md")
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are not permitted on this host")
        self.assert_invalid("symlink or reparse point refused")

    def test_windows_reparse_point_refused(self):
        original = Path.lstat
        blocked = self.root / "MODULES/README.md"
        def reparse_info(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == blocked:
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with mock.patch.object(Path, "lstat", reparse_info):
            self.assert_invalid("symlink or reparse point refused")

    def test_case_colliding_package_routes_refused(self):
        original = handover.children
        package_path = self.root / self.package
        def duplicate_case(path):
            entries = original(path)
            if path == package_path:
                entries.append(package_path / "gm_state.md")
            return entries
        with mock.patch.object(handover, "children", duplicate_case):
            self.assert_invalid("case-colliding package route")

    def test_unreadable_file_is_incomplete(self):
        original = Path.read_bytes
        def blocked(path):
            if path.name == "GM_STATE.md":
                raise PermissionError("synthetic read denial")
            return original(path)
        with mock.patch.object(Path, "read_bytes", blocked):
            code, result = self.run_cli()
        self.assertEqual(code, 2, result)
        self.assertEqual(result["status"], "incomplete")


if __name__ == "__main__":
    unittest.main(verbosity=2)
