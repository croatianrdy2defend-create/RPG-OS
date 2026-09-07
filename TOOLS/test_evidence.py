#!/usr/bin/env python3
"""Synthetic evidence fixtures; no campaign writes, model calls, or semantic verdicts.

Run: python -B TOOLS/test_evidence.py
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import evidence


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rpg-evidence-tests-")
        self.root = Path(self.temp.name)
        self.temp_boundary = Path(tempfile.gettempdir()).resolve()
        self.addCleanup(self.cleanup_fixture)
        self.prior = self.root / "prior"
        self.current = self.root / "current"
        self.capture = self.root / "capture"
        self.bundle = self.root / "bundle"
        self.raw = self.root / "provided.txt"
        self.report_file = self.root / "report.json"
        self.raw.write_bytes("Player: Čekaj.\r\nOOC: Do not resolve the scene.\r\nGM: Waiting.\r\n".encode("utf-8"))
        for side in (self.prior, self.current):
            (side / "OS").mkdir(parents=True)
            (side / "OS" / "RULE.md").write_bytes(b"# Rules\r\n\r\nCorrection requires authority.\r\nKeep consequences contained.\r\n")
            (side / "WORLD").mkdir()
            (side / "WORLD" / "visual.bin").write_bytes(b"\x00" * 1024)

    def cleanup_fixture(self):
        resolved = self.root.resolve()
        if resolved.parent != self.temp_boundary or not resolved.name.startswith("rpg-evidence-tests-"):
            raise RuntimeError("refusing cleanup outside isolated OS-temp fixture")
        self.temp.cleanup()

    def write_json(self, path, value):
        path.write_bytes(evidence.json_bytes(value))

    def imported(self, claims=None):
        return evidence.import_capture(self.raw, self.capture, metadata=claims)

    def frozen(self, claims=None):
        self.imported(claims)
        return evidence.prepare_audit(self.prior, self.current, self.capture, self.bundle, selected=["OS/RULE.md"])

    def citation(self, ref, start=1, end=1):
        if ref["source"] == "capture":
            path = self.bundle / "capture" / ref["path"]
        else:
            path = self.bundle / "sources" / ref["source"] / ref["path"]
        lines = path.read_bytes().decode("utf-8").splitlines(keepends=True)
        return {**ref, "start_line": start, "end_line": end, "quote": "".join(lines[start - 1:end])}

    def completed_report(self):
        report = evidence.report_template(self.bundle)
        report["review_status"] = "completed"
        report["reviewer"] = {"kind": "model", "identifier": "synthetic-test-reviewer", "independence": "unknown"}
        refs = report["source_coverage"]["indexed_sources"]
        report["source_coverage"].update(status="scoped", reviewed_sources=copy.deepcopy(refs))
        report["record_consistency"] = {"status": "consistent", "summary": "Synthetic scoped record assessment.",
                                        "citations": [self.citation(ref) for ref in refs]}
        return report

    def check_written(self, report):
        self.write_json(self.report_file, report)
        return evidence.check_report(self.bundle, self.report_file)

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = evidence.main([str(item) for item in args])
        return code, json.loads(output.getvalue())

    def test_raw_import_preserves_exact_crlf_unicode_ooc_and_order(self):
        result = self.imported({"campaign_id": "synthetic", "save_id": "save-1",
                                "message_boundary": {"first": "Player: Čekaj.", "last": "GM: Waiting."},
                                "conversation_complete": True, "gaps": []})
        source = self.raw.read_bytes()
        self.assertEqual((self.capture / "source.txt").read_bytes(), source)
        self.assertEqual(result["exact_bytes_verified"], len(source))
        self.assertEqual(result["source_sha256"], evidence.sha(source))
        self.assertEqual(result["conversation_completeness"], "unverified_caller_claim")
        self.assertEqual(result["manifest"]["byte_coverage"]["source_line_count"], 3)
        self.assertIn(b"OOC: Do not resolve the scene.\r\nGM: Waiting.", source)

    def test_partial_gaps_are_claims_not_byte_loss(self):
        result = self.imported({"conversation_complete": False, "gaps": ["Earlier messages unavailable."]})
        self.assertEqual(result["exact_bytes_verified"], self.raw.stat().st_size)
        self.assertEqual(result["declared_gaps"], ["Earlier messages unavailable."])
        self.assertEqual(result["manifest"]["caller_claims"]["conversation_complete"], False)

    def test_unicode_paragraph_separator_does_not_invent_original_lines(self):
        self.raw.write_bytes("OOC: first\u2028still first\r\nsecond\r\n".encode("utf-8"))
        result = self.imported()
        self.assertEqual(result["manifest"]["byte_coverage"]["source_line_count"], 2)

    def test_jsonl_records_and_extensions_preserved_without_normalization(self):
        records = [{"role": "user", "content": "Čekaj\nOOC: pause", "kind": "ooc", "id": "a"},
                   {"role": "assistant", "content": "Waiting.", "custom": {"kept": True}}]
        raw = b"\r\n".join(json.dumps(item, ensure_ascii=False).encode("utf-8") for item in records) + b"\r\n"
        self.raw.write_bytes(raw)
        result = evidence.import_capture(self.raw, self.capture, "jsonl")
        self.assertEqual((self.capture / "source.jsonl").read_bytes(), raw)
        ranges = result["manifest"]["byte_coverage"]["message_records"]
        self.assertEqual([value["role"] for value in ranges], ["user", "assistant"])
        self.assertEqual(ranges[-1]["end_byte_exclusive"], len(raw))
        self.assertEqual(ranges[1]["start_byte"], ranges[0]["end_byte_exclusive"])

    def test_invalid_utf8_jsonl_or_metadata_leaves_no_capture(self):
        for raw, fmt, metadata in ((b"\xff", "raw", None),
                                   (b'{"role":"user","content":42}\n', "jsonl", None),
                                   (b'{"role":"user","role":"assistant","content":"x"}', "jsonl", None),
                                   (b"text", "raw", {"conversation_complete": "yes"}),
                                   (b"text", "raw", {"invented_platform_export": True})):
            with self.subTest(raw=raw, metadata=metadata):
                self.raw.write_bytes(raw)
                with self.assertRaises(evidence.EvidenceError):
                    evidence.import_capture(self.raw, self.capture, fmt, metadata)
                self.assertFalse(self.capture.exists())

    def test_pending_has_no_invented_source(self):
        result = evidence.pending_capture(self.capture, {"notes": "Awaiting actual export."})
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["exact_bytes_verified"], 0)
        self.assertEqual(sorted(path.name for path in self.capture.iterdir()), ["manifest.json"])
        self.assertIsNone(result["manifest"]["source"])

    def test_import_never_overwrites(self):
        self.imported()
        original = (self.capture / "source.txt").read_bytes()
        with self.assertRaisesRegex(evidence.EvidenceError, "already exists"):
            evidence.import_capture(self.raw, self.capture)
        self.assertEqual((self.capture / "source.txt").read_bytes(), original)
        with self.assertRaises(evidence.EvidenceError):
            evidence.import_capture(self.raw, self.raw)

    def test_capture_tamper_extra_file_and_coverage_rejected(self):
        self.imported()
        source = self.capture / "source.txt"
        original = source.read_bytes()
        source.write_bytes(original + b"Invented after capture.\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "hash/size"):
            evidence.check_capture(self.capture)
        source.write_bytes(original)
        extra = self.capture / "undeclared.txt"
        extra.write_bytes(b"unexpected")
        with self.assertRaisesRegex(evidence.EvidenceError, "unexpected"):
            evidence.check_capture(self.capture)
        extra.unlink()
        manifest = evidence.read_json(self.capture / "manifest.json")
        manifest["byte_coverage"]["verified_bytes"] -= 1
        self.write_json(self.capture / "manifest.json", manifest)
        with self.assertRaisesRegex(evidence.EvidenceError, "coverage"):
            evidence.check_capture(self.capture)

    def test_source_path_escape_and_special_names_refused(self):
        self.imported()
        for relative in ("../provided.txt", "/OS/RULE.md", "OS/../OS/RULE.md", "OS\\RULE.md", "OS/NUL.md", "C:/outside.md"):
            with self.subTest(relative=relative), self.assertRaises(evidence.EvidenceError):
                evidence.prepare_audit(self.prior, self.current, self.capture, self.bundle, selected=[relative])
        self.assertFalse(self.bundle.exists())

    def test_symlink_input_refused_when_supported(self):
        linked = self.root / "linked.txt"
        try:
            linked.symlink_to(self.raw)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation unavailable to this test account")
        with self.assertRaisesRegex(evidence.EvidenceError, "symlink or reparse"):
            evidence.import_capture(linked, self.capture)

    def test_special_input_refused_when_supported(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO unavailable on this platform")
        fifo = self.root / "pipe"
        os.mkfifo(fifo)
        with self.assertRaisesRegex(evidence.EvidenceError, "special file"):
            evidence.import_capture(fifo, self.capture)

    def test_scoped_frozen_sources_exact_and_inputs_immutable(self):
        before = {str(path): path.read_bytes() for root in (self.prior, self.current)
                  for path in root.rglob("*") if path.is_file()}
        result = self.frozen()
        self.assertEqual(result["source_count"], 2)
        self.assertEqual(result["source_coverage"], "scoped")
        for side, root in (("prior", self.prior), ("current", self.current)):
            self.assertEqual((self.bundle / "sources" / side / "OS/RULE.md").read_bytes(), (root / "OS/RULE.md").read_bytes())
            self.assertFalse((self.bundle / "sources" / side / "WORLD/visual.bin").exists())
            self.assertTrue(result["manifest"]["roots"][side]["omitted_scope"])
        self.assertEqual(before, {str(path): path.read_bytes() for root in (self.prior, self.current)
                                 for path in root.rglob("*") if path.is_file()})

    def test_bundle_output_must_be_outside_all_input_roots(self):
        self.imported()
        for output in (self.prior / "audit", self.current / "audit", self.capture / "audit", self.root):
            with self.subTest(output=output), self.assertRaises(evidence.EvidenceError):
                evidence.prepare_audit(self.prior, self.current, self.capture, output, selected=["OS/RULE.md"])
        self.assertFalse((self.current / "audit").exists())

    def test_windows_short_path_cannot_bypass_protected_root(self):
        if os.name != "nt":
            self.skipTest("Windows 8.3 aliases are specific to Windows")
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.GetShortPathNameW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
        kernel.GetShortPathNameW.restype = wintypes.DWORD
        buffer = ctypes.create_unicode_buffer(32768)
        self.assertTrue(kernel.GetShortPathNameW(str(self.prior), buffer, len(buffer)))
        short_root = Path(buffer.value)
        canonical = evidence.checked_absolute(short_root, directory=True)
        self.assertEqual(canonical, self.prior.resolve())
        with self.assertRaisesRegex(evidence.EvidenceError, "protected input"):
            evidence.output_path(self.prior / "inside-bundle", [canonical])
        with self.assertRaisesRegex(evidence.EvidenceError, "protected input"):
            evidence.output_path(short_root / "inside-bundle", [self.prior])

    def test_windows_dot_space_device_and_stream_aliases_rejected_lexically(self):
        for name in ("provided.txt.", "provided.txt ", "CONIN$", "COM0", "LPT¹", "provided.txt:stream"):
            with self.subTest(name=name), self.assertRaises(evidence.EvidenceError):
                evidence.checked_absolute(self.root / name)
            with self.subTest(output=name), self.assertRaises(evidence.EvidenceError):
                evidence.output_path(self.root / name, [])

    def test_explicit_prior_only_current_only_selection_honest(self):
        self.imported()
        (self.prior / "OLD.md").write_bytes(b"# Prior-only selected file\n")
        (self.current / "NEW.md").write_bytes(b"# Current-only selected file\n")
        result = evidence.prepare_audit(self.prior, self.current, self.capture, self.bundle,
                                         prior_selected=["OLD.md"], current_selected=["NEW.md"])
        difference = result["manifest"]["selection_difference"]
        self.assertEqual(difference["prior_only"], ["OLD.md"])
        self.assertEqual(difference["current_only"], ["NEW.md"])
        self.assertIn("do not establish", difference["meaning"])
        self.assertEqual(result["manifest"]["roots"]["prior"]["selected_paths"], ["OLD.md"])

    def test_selection_manifests_use_actual_source_hashes(self):
        self.imported()
        paths = []
        for side in ("prior", "current"):
            path = self.root / f"{side}-selection.json"
            self.write_json(path, {"schema": evidence.SELECTION_SCHEMA, "root": side,
                                   "selected_paths": ["OS/RULE.md"], "omitted_scope": ["World visuals and all other files omitted."]})
            paths.append(path)
        result = evidence.prepare_audit(None, None, self.capture, self.bundle,
                                         prior_manifest=paths[0], current_manifest=paths[1])
        self.assertEqual(result["manifest"]["roots"]["prior"]["selection_manifest_sha256"], evidence.sha(paths[0].read_bytes()))
        self.assertEqual(result["manifest"]["sources"][0]["sha256"], evidence.sha((self.prior / "OS/RULE.md").read_bytes()))

    def test_bundle_never_overwritten(self):
        self.frozen()
        manifest = (self.bundle / "bundle.json").read_bytes()
        with self.assertRaisesRegex(evidence.EvidenceError, "already exists"):
            evidence.prepare_audit(self.prior, self.current, self.capture, self.bundle, selected=["OS/RULE.md"])
        self.assertEqual((self.bundle / "bundle.json").read_bytes(), manifest)

    def test_actual_external_report_exact_citations_and_limited_result(self):
        self.frozen()
        result = self.check_written(self.completed_report())
        self.assertEqual(result["status"], "report_structure_verified")
        self.assertEqual(result["verified_operations"]["exact_original_line_quotes"], 3)
        self.assertEqual(result["semantic_review"], "not_performed")
        self.assertFalse(result["repair_authorized"])
        self.assertTrue(result["source_coverage"]["review_not_verified"])

    def test_correct_original_multiline_crlf_citation(self):
        self.frozen()
        report = self.completed_report()
        report["record_consistency"]["citations"][0] = self.citation(report["source_coverage"]["indexed_sources"][0], 2, 4)
        self.assertEqual(self.check_written(report)["status"], "report_structure_verified")

    def test_wrong_quote_wrong_line_stale_hash_and_stale_bundle_rejected(self):
        self.frozen()
        original = self.completed_report()
        for kind in ("quote", "line", "source_hash", "bundle_hash", "capture_hash"):
            report = copy.deepcopy(original)
            if kind == "quote":
                report["record_consistency"]["citations"][0]["quote"] = "Invented quote.\n"
            elif kind == "line":
                report["record_consistency"]["citations"][0]["start_line"] = 99
            elif kind == "source_hash":
                report["record_consistency"]["citations"][0]["sha256"] = "0" * 64
            elif kind == "bundle_hash":
                report["bundle_sha256"] = "0" * 64
            else:
                report["capture"]["manifest_sha256"] = "0" * 64
            with self.subTest(kind=kind), self.assertRaises(evidence.EvidenceError):
                self.check_written(report)

    def test_frozen_tamper_invalidates_report_and_live_changes_do_not(self):
        self.frozen()
        report = self.completed_report()
        (self.current / "OS/RULE.md").write_bytes(b"# Later live change\n")
        self.assertEqual(self.check_written(report)["status"], "report_structure_verified")
        (self.bundle / "sources/current/OS/RULE.md").write_bytes(b"# Tampered snapshot\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "hash mismatch"):
            self.check_written(report)

    def test_unobserved_coverage_cannot_support_consistent_or_pass(self):
        self.frozen()
        for status in ("consistent", "PASS"):
            report = self.completed_report()
            report["source_coverage"].update(status="unobserved", reviewed_sources=[])
            report["record_consistency"]["status"] = status
            with self.subTest(status=status), self.assertRaises(evidence.EvidenceError):
                self.check_written(report)

    def test_pending_template_remains_pending_and_cli_exit_two(self):
        self.frozen()
        template = evidence.report_template(self.bundle)
        self.assertEqual(template["record_consistency"]["status"], "not_reviewed")
        self.write_json(self.report_file, template)
        code, result = self.run_cli("check-report", "--bundle", self.bundle, "--report", self.report_file)
        self.assertEqual(code, 2)
        self.assertEqual(result["status"], "pending_review")
        self.assertFalse(result["repair_authorized"])

    def test_pending_capture_never_supports_consistent_report(self):
        evidence.pending_capture(self.capture)
        evidence.prepare_audit(self.prior, self.current, self.capture, self.bundle, selected=["OS/RULE.md"])
        report = self.completed_report()
        with self.assertRaisesRegex(evidence.EvidenceError, "pending capture"):
            self.check_written(report)
        report["record_consistency"]["status"] = "undetermined"
        report["unresolved_facts"] = [{"summary": "Actual conversation source is unavailable.",
                                       "basis": "pending_capture", "citations": []}]
        self.assertEqual(self.check_written(report)["status"], "report_structure_verified")

    def test_partial_undetermined_review_with_unresolved_categories(self):
        self.frozen({"conversation_complete": False, "gaps": ["Missing older messages."]})
        report = self.completed_report()
        ref = report["source_coverage"]["indexed_sources"][0]
        citation = self.citation(ref)
        report["source_coverage"].update(status="partial", reviewed_sources=[ref])
        report["record_consistency"].update(status="undetermined", citations=[citation])
        report["unresolved_facts"] = [{"summary": "Synthetic unresolved fact.", "citations": [citation]}]
        report["unresolved_instructions"] = [{"summary": "Synthetic unresolved instruction.", "citations": [citation]}]
        report["unresolved_instructions"].append({"summary": "Older instructions are not observed.",
                                                   "basis": "caller_declared_gap", "citations": []})
        self.assertEqual(self.check_written(report)["status"], "report_structure_verified")

    def test_clear_but_consequential_repair_rejected(self):
        self.frozen()
        report = self.completed_report()
        authority = self.citation(report["source_coverage"]["indexed_sources"][1], 3, 4)
        report["repair_eligibility"].update(status="eligible", evidentiary_clarity=True,
                                           consequence_containment=False, summary="A clear record would require a consequential rewind.",
                                           authority_citations=[authority])
        with self.assertRaisesRegex(evidence.EvidenceError, "clarity AND consequence"):
            self.check_written(report)
        report["repair_eligibility"]["status"] = "ineligible"
        self.assertEqual(self.check_written(report)["status"], "report_structure_verified")

    def test_repair_and_rewind_findings_require_authority_citations(self):
        self.frozen()
        report = self.completed_report()
        citation = self.citation(report["source_coverage"]["indexed_sources"][0], 3, 4)
        report["findings"] = [{"id": "synthetic-1", "category": "record_consistency",
                               "summary": "Synthetic rewind finding.", "decision": "rewind", "citations": [citation],
                               "authority_citations": []}]
        with self.assertRaisesRegex(evidence.EvidenceError, "authority"):
            self.check_written(report)
        report["findings"][0]["authority_citations"] = [citation]
        report["repair_eligibility"].update(status="eligible", evidentiary_clarity=True,
                                           consequence_containment=True, summary="Declared eligibility in synthetic fixture.",
                                           authority_citations=[citation])
        result = self.check_written(report)
        self.assertFalse(result["repair_authorized"])
        self.assertEqual(result["semantic_review"], "not_performed")

    def test_delivery_receipt_validates_text_without_proving_reading(self):
        self.frozen()
        report = self.completed_report()
        passage = report["record_consistency"]["citations"].pop()
        receipt_file = self.root / "receipt.json"
        self.write_json(receipt_file, {"schema": evidence.RECEIPT_SCHEMA, "bundle_id": report["bundle_id"],
                                       "bundle_sha256": report["bundle_sha256"], "passages": [passage]})
        self.write_json(self.report_file, report)
        with self.assertRaisesRegex(evidence.EvidenceError, "no matching citation"):
            evidence.check_report(self.bundle, self.report_file)
        result = evidence.check_report(self.bundle, self.report_file, receipt_file)
        self.assertEqual(result["source_coverage"]["receipt_delivered"], 1)
        self.assertEqual(result["source_coverage"]["declared_reviewed"], 3)
        self.assertTrue(result["source_coverage"]["review_not_verified"])
        receipt = evidence.read_json(receipt_file)
        receipt["passages"][0]["quote"] = "wrong\n"
        self.write_json(receipt_file, receipt)
        with self.assertRaisesRegex(evidence.EvidenceError, "quote"):
            evidence.check_report(self.bundle, self.report_file, receipt_file)

    def test_actual_reader_jsonl_receipts_accept_exact_and_reject_stale_passages(self):
        self.frozen()
        report = self.completed_report()
        report["record_consistency"]["citations"] = report["record_consistency"]["citations"][:1]
        receipt_file = self.root / "reader-receipts.jsonl"
        for relative in ("sources/current/OS/RULE.md", "capture/source.txt"):
            doc = evidence.read_source.load_document(self.bundle, relative)
            passage = evidence.read_source.select_passage(doc)
            evidence.read_source.write_receipt(self.bundle, relative, passage, receipt_file)
        self.write_json(self.report_file, report)
        result = evidence.check_report(self.bundle, self.report_file, receipt_file)
        self.assertEqual(result["source_coverage"]["receipt_delivered"], 2)
        self.assertEqual(result["source_coverage"]["receipt_fully_delivered"], 2)
        self.assertTrue(result["source_coverage"]["review_not_verified"])
        records = [json.loads(line) for line in receipt_file.read_text(encoding="utf-8").splitlines()]
        records[0]["passage"]["text"] = "Invented delivery."
        receipt_file.write_bytes(b"".join(evidence.json_bytes(record).replace(b"\n", b"") + b"\n" for record in records))
        with self.assertRaisesRegex(evidence.EvidenceError, "receipt passage/hash/coverage"):
            evidence.check_report(self.bundle, self.report_file, receipt_file)

    def test_complete_empty_source_receipt_counts_as_delivery(self):
        (self.current / "OS/RULE.md").write_bytes(b"")
        self.frozen()
        report = self.completed_report()
        report["record_consistency"]["citations"] = [citation for citation in report["record_consistency"]["citations"]
                                                       if citation["source"] != "current"]
        receipt_file = self.root / "empty-receipt.jsonl"
        doc = evidence.read_source.load_document(self.bundle, "sources/current/OS/RULE.md")
        passage = evidence.read_source.select_passage(doc)
        evidence.read_source.write_receipt(self.bundle, doc["path"], passage, receipt_file)
        self.write_json(self.report_file, report)
        result = evidence.check_report(self.bundle, self.report_file, receipt_file)
        self.assertEqual(result["source_coverage"]["receipt_delivered"], 1)
        self.assertEqual(result["source_coverage"]["receipt_fully_delivered"], 1)
        self.assertEqual(result["semantic_review"], "not_performed")

    def test_documented_cli_workflow_end_to_end(self):
        for root in (self.prior, self.current):
            (root / "INSTANCE").mkdir()
            (root / "INSTANCE/CURRENT_SAVE.md").write_bytes(b"# Synthetic current save\n")
            (root / "INSTANCE/CAMPAIGN_CONTRACT.md").write_bytes(b"# Synthetic accepted agreement\n")

        def command(*args):
            result = subprocess.run([sys.executable, "-B", str(Path(evidence.__file__).resolve()), *map(str, args)],
                                    cwd=self.current, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return json.loads(result.stdout)

        # These are the ADMIN/EVIDENCE_AUDIT.md commands with disposable roots.
        capture_route = "EVIDENCE/captures/session-001"
        command("import", "--input", self.raw, "--output", capture_route, "--format", "raw")
        self.assertEqual(command("check", capture_route)["status"], "captured")
        command("prepare-audit", "--prior", self.prior, "--current", ".", "--capture", capture_route,
                "--output", self.bundle, "--select", "INSTANCE/CURRENT_SAVE.md", "--select", "INSTANCE/CAMPAIGN_CONTRACT.md")
        template = command("report-template", "--bundle", self.bundle)
        self.assertEqual(template["review_status"], "pending")
        self.assertEqual(len(template["source_coverage"]["indexed_sources"]), 5)
        self.write_json(self.report_file, self.completed_report())
        result = command("check-report", "--bundle", self.bundle, "--report", self.report_file)
        self.assertEqual(result["status"], "report_structure_verified")
        self.assertEqual(result["semantic_review"], "not_performed")

    def test_cli_import_check_and_failure_are_json(self):
        code, result = self.run_cli("import", "--input", self.raw, "--output", self.capture)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "captured")
        code, result = self.run_cli("check", self.capture)
        self.assertEqual(code, 0)
        self.assertEqual(result["semantic_review"], "not_performed")
        code, result = self.run_cli("import", "--input", self.raw, "--output", self.capture)
        self.assertEqual(code, 1)
        self.assertEqual(result["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
