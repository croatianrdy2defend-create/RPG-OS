#!/usr/bin/env python3
"""Synthetic save-review plumbing checks. No LLM calls or semantic detection score."""
from __future__ import annotations
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.dont_write_bytecode = True
import evidence

ROOT = Path(__file__).resolve().parent.parent


def save_text(save_id="s1", parent="s0", rev=1, kind="close", archived="s1", folder="sessions/s1", campaign="trial"):
    values = {"campaign_id": campaign, "save_id": save_id, "save_rev": str(rev), "save_parent": parent,
              "commit_kind": kind, "archive_ref": folder, "evidence_through": archived}
    return ("---\nid: instance.current_save\n---\n\n# CURRENT_SAVE\n\n| Field | Value |\n|---|---|\n"
            + "".join(f"| {key} | {value} |\n" for key, value in values.items())
            + "\n## Situation\nUnanswered choice retained.\n").encode()


class SaveReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rpg-save-review-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prior, self.current = self.root / "prior", self.root / "current"
        for folder in (self.prior, self.current):
            (folder / "INSTANCE").mkdir(parents=True)
            (folder / "INSTANCE/PC.md").write_bytes(b"---\nid: pc\n---\n\nCash: 10\nDebt: 3\n")
            (folder / evidence.SAVE_PATH).write_bytes(save_text())
        (self.current / evidence.SAVE_PATH).write_bytes(save_text("s2", "s1", 2, "checkpoint"))
        (self.current / "INSTANCE/PC.md").write_bytes(b"---\nid: pc\n---\n\nCash: 7\nDebt: settled\n")
        self.raw, self.capture = self.root / "chat.txt", self.root / "capture"
        self.raw.write_bytes(b"Player: I pay three crowns.\nGM: The debt is settled; seven remain.\nPlayer: Next choice not yet saved.\n")
        evidence.import_capture(self.raw, self.capture)
        self.bundle, self.report_file = self.root / "bundle", self.root / "report.json"
        self.boundary_file = self.root / "boundary.json"
        self.request = {"schema": evidence.SAVE_BOUNDARY_SCHEMA,
                        "state_saved_through": {"basis": "capture_lines", "capture_sha256": evidence.sha(self.raw.read_bytes()),
                                                "start_line": 1, "end_line": 2, "description": "through accepted payment; later choice excluded"},
                        "write_paths": [evidence.SAVE_PATH, "INSTANCE/PC.md"], "removed_paths": [],
                        "limitations": ["Synthetic selected evidence; not a whole-campaign or semantic trial."]}
        self.write(self.boundary_file, self.request)

    def write(self, path, value):
        path.write_bytes(evidence.json_bytes(value))

    def prepare(self, **changes):
        if changes:
            self.request.update(changes)
            self.write(self.boundary_file, self.request)
        return evidence.prepare_save_audit(self.prior, self.current, self.capture, self.bundle,
                                            self.boundary_file, ["INSTANCE/PC.md"])

    def cite(self, ref, first=1, last=1):
        prefix = "capture" if ref["source"] == "capture" else "sources/" + ref["source"]
        lines = (self.bundle / prefix / ref["path"]).read_bytes().decode().splitlines(keepends=True)
        return {**ref, "start_line": first, "end_line": last, "quote": "".join(lines[first - 1:last])}

    def completed(self, consistency="consistent"):
        report = evidence.report_template(self.bundle)
        report["review_status"] = "completed"
        report["reviewer"] = {"kind": "model", "identifier": "synthetic-declaration-not-a-real-review", "independence": "same_context"}
        refs = report["source_coverage"]["indexed_sources"]
        report["source_coverage"].update(status="scoped", reviewed_sources=copy.deepcopy(refs))
        report["record_consistency"] = {"status": consistency, "summary": "Synthetic declared judgment, not measured detection.",
                                         "citations": [self.cite(ref) for ref in refs]}
        report["save_review"]["review_covered_through"] = self.request["state_saved_through"]
        return report

    def checked(self, report):
        self.write(self.report_file, report)
        return evidence.check_save_audit(self.bundle, self.report_file, self.current)

    def cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = evidence.main([str(arg) for arg in args])
        return code, json.loads(out.getvalue())

    def test_tiered_checkpoint_is_lightweight(self):
        plan = evidence.save_review_plan("tiered", "checkpoint")
        self.assertEqual(plan["review_level"], "lightweight")
        self.assertFalse(plan["capture_required_for_source_review"])

    def test_tiered_close_is_source_review(self):
        self.assertEqual(evidence.save_review_plan("tiered", "close")["review_level"], "source")

    def test_every_save_explicitly_includes_checkpoint(self):
        for kind in ("checkpoint", "close"):
            self.assertEqual(evidence.save_review_plan("every-save", kind)["review_level"], "source")

    def test_absence_does_not_enable_source_review(self):
        for kind in ("checkpoint", "close"):
            self.assertEqual(evidence.save_review_plan(kind=kind)["review_level"], "lightweight")

    def test_one_off_source_review_does_not_change_policy(self):
        plan = evidence.save_review_plan("off", "checkpoint", True)
        self.assertEqual((plan["policy"], plan["review_level"]), ("off", "source"))
        self.assertEqual(evidence.save_review_plan()["review_level"], "lightweight")

    def test_invalid_policy_inputs_refused(self):
        for args in (("automatic", "checkpoint"), ("tiered", "end"), ("tiered", "close", 1)):
            with self.subTest(args=args), self.assertRaises(evidence.EvidenceError):
                evidence.save_review_plan(*args)

    def test_diff_reports_selected_bytes_and_no_semantic_review(self):
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        diff = evidence.save_diff(self.prior, self.current, ["INSTANCE/PC.md"])
        self.assertEqual(len(diff["files"]), 2)
        self.assertIsNone(diff["review_covered_through"])
        self.assertEqual(diff["semantic_review"], "not_performed")
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_diff_add_remove_and_unchanged(self):
        (self.prior / "INSTANCE/old.md").write_bytes(b"old\n")
        (self.current / "INSTANCE/new.md").write_bytes(b"new\n")
        for folder in (self.prior, self.current):
            (folder / "INSTANCE/unchanged.md").write_bytes(b"same\n")
        files = evidence.save_diff(self.prior, self.current, ["INSTANCE/old.md", "INSTANCE/new.md", "INSTANCE/unchanged.md"])["files"]
        self.assertEqual({v["change"] for v in files}, {"added", "removed", "changed", "unchanged"})

    def test_diff_rejects_unsafe_path(self):
        with self.assertRaises(evidence.EvidenceError):
            evidence.save_diff(self.prior, self.current, ["../outside.md"])

    def test_duplicate_save_metadata_refused(self):
        path = self.current / evidence.SAVE_PATH
        path.write_bytes(path.read_bytes().replace(b"| save_id | s2 |", b"| save_id | s2 |\n| save_id | s3 |"))
        with self.assertRaisesRegex(evidence.EvidenceError, "duplicate"):
            self.prepare()

    def test_wrong_parent_revision_and_campaign_refused(self):
        for kwargs in ({"parent": "other"}, {"rev": 3}, {"campaign": "other"}, {"save_id": "s1"}):
            args = dict(save_id="s2", parent="s1", rev=2, kind="checkpoint"); args.update(kwargs)
            (self.current / evidence.SAVE_PATH).write_bytes(save_text(**args))
            with self.subTest(kwargs=kwargs), self.assertRaises(evidence.EvidenceError):
                self.prepare()
            self.assertFalse(self.bundle.exists())

    def test_checkpoint_cannot_advance_or_clear_archive(self):
        for archived, folder in (("s2", "sessions/s2"), ("none", "none")):
            (self.current / evidence.SAVE_PATH).write_bytes(save_text("s2", "s1", 2, "checkpoint", archived, folder))
            with self.subTest(archived=archived), self.assertRaisesRegex(evidence.EvidenceError, "checkpoint changed"):
                self.prepare()

    def test_close_binds_own_archive_boundary(self):
        (self.current / evidence.SAVE_PATH).write_bytes(save_text("s2", "s1", 2, "close", "s2", "sessions/s2"))
        bound = self.prepare()["manifest"]["save_binding"]
        self.assertEqual(bound["history_archived_through"]["evidence_through"], "s2")
        self.assertEqual(bound["state_saved_through"]["end_line"], 2)

    def test_close_reusing_archive_refused(self):
        (self.current / evidence.SAVE_PATH).write_bytes(save_text("s2", "s1", 2, "close"))
        with self.assertRaisesRegex(evidence.EvidenceError, "full save needs"):
            self.prepare()

    def test_preparation_retains_original_and_separate_boundaries(self):
        bound = self.prepare()["manifest"]["save_binding"]
        self.assertEqual((self.bundle / "capture/source.txt").read_bytes(), self.raw.read_bytes())
        self.assertEqual(bound["history_archived_through"]["evidence_through"], "s1")
        report = evidence.report_template(self.bundle)
        self.assertIsNone(report["save_review"]["review_covered_through"])
        self.assertEqual(report["save_review"]["source_coherence"]["status"], "not_assessed")

    def test_unselected_write_refused_before_output(self):
        with self.assertRaisesRegex(evidence.EvidenceError, "outside frozen"):
            self.prepare(write_paths=[evidence.SAVE_PATH, "INSTANCE/PC.md", "INSTANCE/missing.md"])
        self.assertFalse(self.bundle.exists())

    def test_changed_selected_file_must_be_in_write_set(self):
        with self.assertRaisesRegex(evidence.EvidenceError, "omitted from write_paths"):
            self.prepare(write_paths=[evidence.SAVE_PATH])

    def test_boundary_rejects_bad_hash_line_or_boolean(self):
        for changes in ({"capture_sha256": "0" * 64}, {"end_line": 99}, {"start_line": True}, {"basis": "invented_host_id"}):
            request = copy.deepcopy(self.request)
            request["state_saved_through"].update(changes)
            self.write(self.boundary_file, request)
            with self.subTest(changes=changes), self.assertRaises(evidence.EvidenceError):
                evidence.prepare_save_audit(self.prior, self.current, self.capture, self.bundle, self.boundary_file, ["INSTANCE/PC.md"])

    def test_completed_review_and_exact_readback(self):
        self.prepare()
        result = self.checked(self.completed())
        self.assertEqual(result["status"], "selected_saved_bytes_verified")
        self.assertEqual(result["save_id"], "s2")
        self.assertEqual(result["semantic_review"], "not_performed_by_tool")
        self.assertFalse(result["repair_authorized"])

    def test_changed_candidate_invalidates_readback(self):
        self.prepare()
        (self.current / "INSTANCE/PC.md").write_bytes(b"Cash: 999\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from reviewed version"):
            self.checked(self.completed())

    def test_changed_save_pointer_invalidates_readback(self):
        self.prepare()
        path = self.current / evidence.SAVE_PATH
        path.write_bytes(path.read_bytes() + b"\nAudit passed!\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from reviewed"):
            self.checked(self.completed())

    def test_stale_binding_report_rejected(self):
        self.prepare(); report = self.completed()
        report["save_review"]["binding_sha256"] = "0" * 64
        with self.assertRaisesRegex(evidence.EvidenceError, "stale save binding"):
            self.checked(report)

    def test_wrong_review_boundary_rejected(self):
        self.prepare(); report = self.completed()
        report["save_review"]["review_covered_through"] = {**self.request["state_saved_through"], "end_line": 3}
        with self.assertRaisesRegex(evidence.EvidenceError, "boundary differs"):
            self.checked(report)

    def test_citation_after_saved_stop_rejected(self):
        self.prepare(); report = self.completed()
        ref = next(v for v in report["source_coverage"]["indexed_sources"] if v["source"] == "capture")
        report["record_consistency"]["citations"].append(self.cite(ref, 3, 3))
        with self.assertRaisesRegex(evidence.EvidenceError, "after selected save boundary"):
            self.checked(report)

    def test_partial_review_cannot_claim_whole_selected_span(self):
        self.prepare(); report = self.completed("undetermined")
        report["source_coverage"]["status"] = "partial"
        with self.assertRaisesRegex(evidence.EvidenceError, "all selected"):
            self.checked(report)

    def test_pending_template_remains_pending_not_verified_semantics(self):
        self.prepare(); report = evidence.report_template(self.bundle)
        self.write(self.report_file, report)
        code, result = self.cli("check-save-audit", "--bundle", self.bundle, "--report", self.report_file, "--saved", self.current)
        self.assertEqual(code, 2)
        self.assertEqual(result["record_consistency"], "not_reviewed")
        self.assertIsNone(result["review_covered_through"])
        self.assertEqual(self.cli("report-template", "--bundle", self.bundle)[0], 0)

    def test_missing_capture_cannot_claim_reviewed_through(self):
        pending = self.root / "pending"
        evidence.pending_capture(pending, {"gaps": ["Host cannot export the current chat."]})
        self.capture = pending
        self.prepare(state_saved_through={"basis": "unavailable", "description": "No actual transcript supplied"})
        report = self.completed("undetermined")
        with self.assertRaisesRegex(evidence.EvidenceError, "unavailable capture"):
            self.checked(report)
        report["save_review"]["review_covered_through"] = None
        result = self.checked(report)
        self.assertIn("Host cannot export the current chat.", result["limitations"])

    def test_explicit_source_conflict_is_not_a_consistent_save_badge(self):
        self.prepare(); report = self.completed()
        ref = next(v for v in report["source_coverage"]["indexed_sources"] if v["source"] == "capture")
        report["save_review"]["source_coherence"] = {"status": "conflict_observed", "summary": "Synthetic conflict declaration; not a model-discovered contradiction.", "citations": [self.cite(ref, 1, 2)]}
        with self.assertRaisesRegex(evidence.EvidenceError, "source conflict"):
            self.checked(report)
        report["record_consistency"]["status"] = "undetermined"
        self.assertEqual(self.checked(report)["source_coherence"]["status"], "conflict_observed")

    def test_selected_old_evidence_is_not_automatically_deleted(self):
        path = "INSTANCE/older.md"
        for folder in (self.prior, self.current):
            (folder / path).write_bytes(b"---\nid: older\n---\nOriginal promise.\n")
        evidence.prepare_save_audit(self.prior, self.current, self.capture, self.bundle, self.boundary_file,
                                    ["INSTANCE/PC.md"], prior_selected=[path])
        self.assertEqual(self.checked(self.completed())["removed_paths_verified"], [])
        self.assertTrue((self.current / path).exists())

    def test_explicit_removal_is_checked_after_publication(self):
        path = "INSTANCE/expired.md"
        (self.prior / path).write_bytes(b"---\nid: expired\n---\nTemporary entry.\n")
        self.request["removed_paths"] = [path]; self.write(self.boundary_file, self.request)
        evidence.prepare_save_audit(self.prior, self.current, self.capture, self.bundle, self.boundary_file,
                                    ["INSTANCE/PC.md"], prior_selected=[path])
        self.assertEqual(self.checked(self.completed())["removed_paths_verified"], [path])
        (self.current / path).write_bytes(b"reappeared\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "removal not applied"):
            self.checked(self.completed())

    def test_still_existing_declared_removal_refused(self):
        path = "INSTANCE/old.md"
        for folder in (self.prior, self.current):
            (folder / path).write_bytes(b"---\nid: old\n---\nStill present.\n")
        self.request["removed_paths"] = [path]; self.write(self.boundary_file, self.request)
        with self.assertRaisesRegex(evidence.EvidenceError, "still exists"):
            evidence.prepare_save_audit(self.prior, self.current, self.capture, self.bundle, self.boundary_file,
                                        ["INSTANCE/PC.md"], prior_selected=[path])

    def test_byte_exact_capture_does_not_deduplicate_identical_words(self):
        source = self.root / "repeated.txt"; source.write_bytes(b"I pay three.\nI pay three.\n")
        captured = evidence.import_capture(source, self.root / "repeated")
        self.assertEqual(captured["manifest"]["byte_coverage"]["source_line_count"], 2)
        self.assertEqual(captured["exact_bytes_verified"], len(source.read_bytes()))

    def test_output_cannot_overlap_boundary_file(self):
        with self.assertRaises(evidence.EvidenceError):
            evidence.prepare_save_audit(self.prior, self.current, self.capture, self.boundary_file,
                                        self.boundary_file, ["INSTANCE/PC.md"])

    def test_symlinked_readback_refused(self):
        self.prepare()
        path = self.current / "INSTANCE/PC.md"; original = path.read_bytes(); path.unlink()
        other = self.root / "outside.md"; other.write_bytes(original)
        try:
            path.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest("symlink unavailable")
        with self.assertRaisesRegex(evidence.EvidenceError, "symlink"):
            self.checked(self.completed())

    def test_new_commands_cli_workflow(self):
        self.assertEqual(self.cli("save-review-plan", "--policy", "tiered", "--kind", "close")[1]["review_level"], "source")
        self.assertEqual(self.cli("save-diff", "--prior", self.prior, "--current", self.current, "--select", "INSTANCE/PC.md")[0], 0)
        self.assertEqual(self.cli("prepare-save-audit", "--prior", self.prior, "--current", self.current,
                                  "--capture", self.capture, "--boundary", self.boundary_file,
                                  "--output", self.bundle, "--select", "INSTANCE/PC.md")[0], 0)
        self.write(self.report_file, self.completed())
        self.assertEqual(self.cli("check-save-audit", "--bundle", self.bundle, "--report", self.report_file, "--saved", self.current)[0], 0)

    def test_generated_citation_honors_selected_save_boundary(self):
        self.prepare()
        quote = evidence.citation(self.bundle, "capture", "source.txt", 1, 2)
        self.assertEqual(quote["quote"], "".join(self.raw.read_bytes().decode().splitlines(keepends=True)[:2]))
        with self.assertRaisesRegex(evidence.EvidenceError, "after selected save boundary"):
            evidence.citation(self.bundle, "capture", "source.txt", 2, 3)




class ProtocolTests(unittest.TestCase):
    def test_every_saving_route_names_shared_policy(self):
        for path in ("ADMIN/CLOSE_CONTRACT.md", "ADMIN/AUTOSAVE.md", "ADMIN/SESSION.md", "ADMIN/SCENE_HANDOVER.md"):
            with self.subTest(path=path):
                text = (ROOT / path).read_text()
                self.assertIn("tiered", text)
                self.assertIn("source", text)

    def test_autosave_capture_exception_is_explicit(self):
        text = (ROOT / "ADMIN/AUTOSAVE.md").read_text()
        self.assertNotIn("create no archive bodies, indexes, ledgers or raw transcript through autosave", text)
        self.assertIn("ADMIN/CLOSE_CONTRACT.md", text)
        owner = (ROOT / "ADMIN/CLOSE_CONTRACT.md").read_text()
        self.assertIn("CHECKPOINT", owner)
        self.assertIn("Lightweight", owner)
        self.assertIn("every-save", owner)
        self.assertIn("source review", owner)

    def test_review_quality_and_cost_are_explicit(self):
        text = (ROOT / "ADMIN/EVIDENCE_AUDIT.md").read_text()
        for phrase in ("blind spots", "cost", "does not establish a semantic detection rate", "source_coherence"):
            self.assertIn(phrase, text)
        self.assertIn("Lightweight means no transcript-grounded review boundary",
                      (ROOT / "ADMIN/CLOSE_CONTRACT.md").read_text())

    def test_workflows_run_new_suite(self):
        for path in (".github/workflows/validate.yml", ".github/workflows/release.yml"):
            runner = ROOT / "DEV/run_tests.py"
            if runner.exists():
                self.assertIn("DEV/run_tests.py", (ROOT / path).read_text())
                self.assertIn("test_save_audit", runner.read_text())
            else:
                self.assertIn("TOOLS/test_save_audit.py", (ROOT / path).read_text())


if __name__ == "__main__":
    unittest.main()
