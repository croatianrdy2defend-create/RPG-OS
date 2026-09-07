"""Regression tests for exact source reads, bounded context, and safe receipts."""

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import read_source as reader


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.sandbox = tempfile.TemporaryDirectory(prefix="rpg-reader-tests-")
        self.addCleanup(self.sandbox.cleanup)
        self.base = Path(self.sandbox.name)
        self.root = self.base / "sources"
        self.root.mkdir()

    def write(self, text, name="rules.md"):
        destination = self.root / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(text.encode("utf-8"))
        return reader.load_document(self.root, name)

    def assert_code(self, code, function, *args, **kwargs):
        with self.assertRaises(reader.SourceError) as caught:
            function(*args, **kwargs)
        self.assertEqual(code, caught.exception.code)
        return caught.exception

    def test_exact_crlf_unicode_bom_and_no_final_newline(self):
        source = "\ufeff# Rules\r\nčarobni izbor\r\nOnly if alive."
        document = self.write(source)
        self.assertEqual(source, document["text"])
        self.assertEqual(["\ufeff# Rules\r\n", "čarobni izbor\r\n", "Only if alive."], document["lines"])
        self.assertEqual(hashlib.sha256(source.encode("utf-8")).hexdigest(), document["sha256"])
        self.assertEqual(len(source.encode("utf-8")), document["source_size_bytes"])
        passage = reader.select_passage(document)
        self.assertEqual(source, passage["text"])
        self.assertTrue(passage["source_complete"])
        self.assertEqual(3, passage["returned_end_line"])
        self.assertEqual("Rules", reader.list_sections(document)[0]["heading"])

    def test_original_line_offsets_and_partial_character_offsets(self):
        document = self.write("first\r\nčćž\r\nlast")
        passage = reader.select_passage(document, start_line=2, end_line=3, max_chars=2)
        self.assertEqual("čć", passage["text"])
        self.assertEqual((2, 3), (passage["start_line"], passage["end_line"]))
        self.assertEqual((2, 2), (passage["returned_start_line"], passage["returned_end_line"]))
        self.assertEqual(7, passage["start_char_offset"])
        self.assertEqual(9, passage["returned_end_char_offset"])
        self.assertEqual(11, passage["returned_end_byte_offset"])
        self.assertFalse(passage["returned_end_line_complete"])
        self.assertTrue(passage["truncated"])
        self.assertEqual(7, passage["omitted_selection_chars"])
        self.assertIn("qualifiers", passage["completeness_note"])

    def test_lone_cr_and_unicode_separator_keep_original_coordinates(self):
        document = self.write("one\rtwo\u2028still two\nthree")
        self.assertEqual(["one\r", "two\u2028still two\n", "three"], document["lines"])
        self.assertEqual("two\u2028still two\n", reader.select_passage(document, start_line=2, end_line=2)["text"])

    def test_hierarchy_ends_at_equal_or_shallower_heading(self):
        document = self.write("intro\n# Combat\nbase\n## Attack\nattack\n### Condition\nOnly if ready.\n## Defense\ndefense\n# Travel\ntravel")
        sections = reader.list_sections(document)
        self.assertEqual([("Combat", 2, 9), ("Attack", 4, 7), ("Condition", 6, 7), ("Defense", 8, 9), ("Travel", 10, 11)], [(s["heading"], s["start_line"], s["end_line"]) for s in sections])
        self.assertEqual(["Combat", "Attack", "Condition"], sections[2]["heading_path"])
        attack = reader.select_passage(document, heading="Combat > Attack")
        self.assertEqual("## Attack\nattack\n### Condition\nOnly if ready.\n", attack["text"])
        self.assertTrue(attack["complete"])
        self.assertFalse(attack["source_complete"])
        self.assertEqual(attack, reader.select_passage(document, heading=["Combat", "Attack"]))

    def test_fences_frontmatter_and_indented_code_are_not_headings(self):
        source = "---\n# frontmatter heading\nkey: value\n---\n# Real\n```markdown\n# hidden\n~~~\n## still hidden\n````\n~~~ lang\n# hidden again\n~~~~\n    # indented\n## Child\nbody\n"
        document = self.write(source)
        sections = reader.list_sections(document)
        self.assertEqual(["Real", "Child"], [s["heading"] for s in sections])
        self.assertEqual([5, 15], [s["start_line"] for s in sections])
        self.assertEqual(source.split("# Real", 1)[1], reader.select_passage(document, heading="Real")["text"][len("# Real"):])

    def test_setext_and_yaml_end_marker(self):
        document = self.write("---\nname: value\n...\nTitle\n=====\nbody\nSubtitle\n---\ncondition\n# Next\nend")
        sections = reader.list_sections(document)
        self.assertEqual([("Title", 1, 4, 9), ("Subtitle", 2, 7, 9), ("Next", 1, 10, 11)], [(s["heading"], s["level"], s["start_line"], s["end_line"]) for s in sections])
        self.assertEqual("Subtitle\n---\ncondition\n", reader.select_passage(document, heading="Subtitle")["text"])

    def test_duplicate_headings_return_candidates_without_guessing(self):
        document = self.write("# First\n## Rule\na\n# Second\n## Rule\nb")
        error = self.assert_code("ambiguous_heading", reader.select_passage, document, heading="Rule")
        self.assertEqual(2, len(error.details["candidates"]))
        self.assertEqual(["Second", "Rule"], error.details["candidates"][1]["heading_path"])
        chosen = reader.select_passage(document, heading="Second > Rule")
        self.assertEqual("## Rule\nb", chosen["text"])
        self.assertEqual(chosen, reader.select_passage(document, section_id=error.details["candidates"][1]["section_id"]))

    def test_duplicate_full_paths_still_require_section_id(self):
        document = self.write("# Same\n## Rule\na\n## Rule\nb")
        self.assert_code("ambiguous_heading", reader.select_passage, document, heading="Same > Rule")

    def test_ids_are_revision_specific_and_stale_hash_is_rejected(self):
        first = self.write("# Rule\nold")
        section_id = reader.list_sections(first)[0]["section_id"]
        self.assertEqual(section_id, reader.list_sections(reader.load_document(self.root, "rules.md"))[0]["section_id"])
        second = self.write("# Rule\nnew")
        self.assertNotEqual(section_id, reader.list_sections(second)[0]["section_id"])
        self.assert_code("stale_revision", reader.load_document, self.root, "rules.md", first["sha256"])
        self.assert_code("section_not_found", reader.select_passage, second, section_id=section_id)
        self.assert_code("invalid_revision", reader.load_document, self.root, "rules.md", "bogus")

    def test_qualifier_remains_in_section_or_truncation_is_explicit(self):
        document = self.write("# Flight\nYou can fly.\n\nThis works only while wearing the amulet.\n# Swimming\nYou can swim.")
        full = reader.select_passage(document, heading="Flight")
        self.assertIn("only while wearing the amulet", full["text"])
        cut = reader.select_passage(document, heading="Flight", max_chars=22)
        self.assertTrue(cut["truncated"])
        self.assertFalse(cut["selection_complete"])
        self.assertGreater(cut["omitted_selection_chars"], 0)
        self.assertIn("conditions", cut["completeness_note"])

    def test_whole_empty_plain_text_and_zero_cap(self):
        empty = self.write("")
        self.assertEqual([], empty["lines"])
        self.assertEqual([], reader.list_sections(empty))
        passage = reader.select_passage(empty)
        self.assertEqual((1, 0), (passage["start_line"], passage["end_line"]))
        self.assertIsNone(passage["returned_start_line"])
        self.assertTrue(passage["source_complete"])
        document = self.write("ordinary text with no headings")
        self.assertEqual([], reader.list_sections(document))
        cut = reader.select_passage(document, max_chars=0)
        self.assertEqual("", cut["text"])
        self.assertTrue(cut["truncated"])
        self.assertIsNone(cut["returned_end_line"])

    def test_invalid_selection_fails_without_silent_clamping(self):
        document = self.write("# Rule\nbody\n")
        for kwargs in ({"start_line": 1}, {"end_line": 1}, {"start_line": 0, "end_line": 2}, {"start_line": 1, "end_line": 3}, {"heading": "Rule", "start_line": 1, "end_line": 2}, {"max_chars": -1}, {"max_chars": True}):
            with self.subTest(kwargs=kwargs):
                self.assert_code("invalid_selection", reader.select_passage, document, **kwargs)

    def test_traversal_absolute_device_and_stream_paths_rejected(self):
        self.write("safe")
        for relative in ("../outside.md", "dir/../../outside.md", "dir\\..\\rules.md", str(self.root / "rules.md"), "C:\\rules.md", "C:rules.md", "//host/share/rules.md", "./rules.md", "dir//rules.md", "rules.md:stream", "NUL", "CON.txt", "rules.md.", "rules.md "):
            with self.subTest(relative=relative):
                self.assert_code("unsafe_path", reader.resolve_source, self.root, relative)
        directory = self.root / "directory"
        directory.mkdir()
        self.assert_code("not_regular_file", reader.resolve_source, self.root, "directory")

    def test_source_symlink_and_symlink_parent_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.md").write_text("outside", encoding="utf-8")
        try:
            (self.root / "linked.md").symlink_to(outside / "secret.md")
            (self.root / "linked-directory").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        self.assert_code("unsafe_path", reader.load_document, self.root, "linked.md")
        self.assert_code("unsafe_path", reader.load_document, self.root, "linked-directory/secret.md")
        self.assert_code("unsafe_path", reader.load_document, self.root / "linked-directory", "secret.md")

    def test_special_file_rejected_without_opening(self):
        if not hasattr(os, "mkfifo"):
            self.skipTest("Named FIFO creation unavailable on this platform")
        os.mkfifo(self.root / "pipe.md")
        self.assert_code("not_regular_file", reader.load_document, self.root, "pipe.md")

    def test_reparse_attribute_is_rejected(self):
        ordinary = mock.Mock(st_mode=stat.S_IFREG, st_file_attributes=0x400)
        self.assertTrue(reader._is_link(ordinary))

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_source_and_receipt_parent_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.md").write_text("outside", encoding="utf-8")
        junction = self.root / "junction"
        escaped_path = str(junction).replace("'", "''")
        escaped_target = str(outside).replace("'", "''")
        result = subprocess.run([
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            f"New-Item -ItemType Junction -Path '{escaped_path}' -Target '{escaped_target}' -ErrorAction Stop | Out-Null",
        ], capture_output=True, text=True)
        if result.returncode:
            self.skipTest("This Windows host cannot create a temporary junction")
        self.addCleanup(junction.rmdir)
        self.assert_code("unsafe_path", reader.load_document, self.root, "junction/secret.md")
        self.assert_code("unsafe_path", reader.load_document, junction, "secret.md")
        document = self.write("safe")
        passage = reader.select_passage(document)
        self.assert_code("unsafe_path", reader.write_receipt, self.root, "rules.md", passage, junction / "receipt.jsonl")
        self.assertFalse((outside / "receipt.jsonl").exists())

    def test_invalid_utf8_and_binary_sources_classified(self):
        (self.root / "invalid.md").write_bytes(b"\xff")
        self.assert_code("invalid_utf8", reader.load_document, self.root, "invalid.md")
        (self.root / "binary.md").write_bytes(b"valid\x00but binary")
        self.assert_code("binary_source", reader.load_document, self.root, "binary.md")

    def test_changed_during_read_fails(self):
        self.write("original")
        original_resolver = reader.resolve_source
        calls = 0

        def mutating_resolver(root, relative):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.root / "rules.md").write_bytes(b"changed-size")
            return original_resolver(root, relative)

        with mock.patch.object(reader, "resolve_source", side_effect=mutating_resolver):
            self.assert_code("source_changed", reader.load_document, self.root, "rules.md")

    def test_same_file_with_different_stat_and_fstat_ctimes_is_read(self):
        source = self.root / "rules.md"
        source.write_bytes(b"original")
        info = source.stat()
        handle_info = SimpleNamespace(**{name: getattr(info, name) for name in
            ("st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")})
        handle_info.st_ctime_ns += 100
        with mock.patch.object(reader.os, "fstat", return_value=handle_info):
            document = reader.load_document(self.root, "rules.md")
        self.assertEqual("original", document["text"])
        self.assertEqual(hashlib.sha256(b"original").hexdigest(), document["sha256"])

    def test_ctime_change_within_each_stat_api_is_still_rejected(self):
        source = self.root / "rules.md"
        source.write_bytes(b"original")
        info = source.stat()
        fields = {name: getattr(info, name) for name in
            ("st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")}
        changed = SimpleNamespace(**{**fields, "st_ctime_ns": info.st_ctime_ns + 1})
        handle = SimpleNamespace(**{**fields, "st_ctime_ns": info.st_ctime_ns + 100})
        changed_handle = SimpleNamespace(**{**fields, "st_ctime_ns": info.st_ctime_ns + 101})
        original_stat = Path.stat
        for api in ("path", "handle"):
            with self.subTest(api=api):
                path_values = iter([info, changed if api == "path" else info])
                def path_stat(path, *args, **kwargs):
                    return next(path_values) if path == source else original_stat(path, *args, **kwargs)
                with mock.patch.object(reader, "resolve_source", return_value=source), \
                        mock.patch.object(Path, "stat", path_stat), \
                        mock.patch.object(reader.os, "fstat", side_effect=[handle, changed_handle if api == "handle" else handle]):
                    self.assert_code("source_changed", reader.load_document, self.root, "rules.md")

    def test_same_size_same_mtime_path_replacement_before_open_is_rejected(self):
        source = self.root / "rules.md"
        replacement = self.root / "replacement.md"
        source.write_bytes(b"original")
        replacement.write_bytes(b"replaced")
        info = source.stat()
        os.utime(replacement, ns=(info.st_atime_ns, info.st_mtime_ns))
        self.assertNotEqual(info.st_ino, replacement.stat().st_ino)
        original_open = os.open
        def replacing_open(path, flags, *args, **kwargs):
            replacement.replace(source)
            return original_open(path, flags, *args, **kwargs)
        with mock.patch.object(reader.os, "open", side_effect=replacing_open):
            self.assert_code("source_changed", reader.load_document, self.root, "rules.md")

    def test_same_size_same_mtime_path_replacement_after_read_is_rejected(self):
        source = self.root / "rules.md"
        replacement = self.root / "replacement.md"
        source.write_bytes(b"original")
        replacement.write_bytes(b"replaced")
        info = source.stat()
        os.utime(replacement, ns=(info.st_atime_ns, info.st_mtime_ns))
        self.assertNotEqual(info.st_ino, replacement.stat().st_ino)
        original_resolver = reader.resolve_source
        calls = 0
        def replacing_resolver(root, relative):
            nonlocal calls
            calls += 1
            if calls == 2:
                replacement.replace(source)
            return original_resolver(root, relative)
        with mock.patch.object(reader, "resolve_source", side_effect=replacing_resolver):
            self.assert_code("source_changed", reader.load_document, self.root, "rules.md")

    def test_receipt_explicit_external_and_no_source_mutation(self):
        document = self.write("# Rule\r\nOnly if ready.")
        source = self.root / "rules.md"
        before = (source.read_bytes(), source.stat().st_mtime_ns)
        passage = reader.select_passage(document)
        target = self.base / "receipts.jsonl"
        self.assertFalse(target.exists())
        receipt_meta = reader.write_receipt(self.root, "rules.md", passage, target)
        self.assertEqual(before, (source.read_bytes(), source.stat().st_mtime_ns))
        record = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual(passage, record["passage"])
        self.assertIn("not proof of comprehension", record["claim"])
        self.assertIn("transcript completeness", record["claim"])
        self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), receipt_meta["receipt_sha256"])
        reader.write_receipt(self.root, "rules.md", passage, target)
        self.assertEqual(2, len(target.read_text(encoding="utf-8").splitlines()))

    def test_receipt_inside_root_and_hardlinked_source_rejected(self):
        document = self.write("safe source")
        passage = reader.select_passage(document)
        self.assert_code("unsafe_receipt", reader.write_receipt, self.root, "rules.md", passage, self.root / "receipt.jsonl")
        self.assertFalse((self.root / "receipt.jsonl").exists())
        linked = self.base / "hardlink.jsonl"
        try:
            os.link(self.root / "rules.md", linked)
        except OSError as exc:
            self.skipTest(f"Hardlinks unavailable: {exc}")
        self.assert_code("unsafe_receipt", reader.write_receipt, self.root, "rules.md", passage, linked)
        self.assertEqual("safe source", (self.root / "rules.md").read_text())

    def test_receipt_symlink_and_parent_rejected(self):
        document = self.write("safe")
        passage = reader.select_passage(document)
        try:
            (self.base / "receipt-link").symlink_to(self.root / "rules.md")
            (self.base / "directory-link").symlink_to(self.root, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        self.assert_code("unsafe_path", reader.write_receipt, self.root, "rules.md", passage, self.base / "receipt-link")
        self.assert_code("unsafe_path", reader.write_receipt, self.root, "rules.md", passage, self.base / "directory-link" / "receipt.jsonl")

    def test_stale_receipt_request_fails_without_writing(self):
        document = self.write("original")
        passage = reader.select_passage(document)
        self.write("changed")
        target = self.base / "receipt.jsonl"
        self.assert_code("stale_revision", reader.write_receipt, self.root, "rules.md", passage, target)
        self.assertFalse(target.exists())

    def test_receipt_alias_forgery_and_unrelated_file_rejected(self):
        document = self.write("exact source")
        passage = reader.select_passage(document)
        self.assert_code("unsafe_receipt", reader.write_receipt, self.root, "rules.md", passage, self.base / "receipt.jsonl.")
        self.assert_code("unsafe_receipt", reader.write_receipt, self.root, "rules.md", passage, self.base / "receipt.jsonl:stream")
        target = self.base / "receipt.jsonl"
        forged = {**passage, "text": "made-up source"}
        self.assert_code("invalid_receipt", reader.write_receipt, self.root, "rules.md", forged, target)
        self.assertFalse(target.exists())
        unrelated = b'{"user":"unrelated data"}\n'
        target.write_bytes(unrelated)
        self.assert_code("invalid_receipt", reader.write_receipt, self.root, "rules.md", passage, target)
        self.assertEqual(unrelated, target.read_bytes())

    def test_cli_invalid_arguments_are_json(self):
        result = subprocess.run([sys.executable, str(Path(reader.__file__).resolve()), "read", "--max-chars", "wrong"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertEqual("invalid_arguments", json.loads(result.stdout)["error"]["code"])
        self.assertEqual("", result.stderr)

    def test_cli_json_read_list_stale_and_duplicate(self):
        document = self.write("# Same\nfirst\n# Same\nsecond")
        command = [sys.executable, str(Path(reader.__file__).resolve())]
        result = subprocess.run(command + ["list", "--root", str(self.root), "--path", "rules.md"], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, len(json.loads(result.stdout)["sections"]))
        result = subprocess.run(command + ["read", "--root", str(self.root), "--path", "rules.md", "--heading", "Same"], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertEqual("ambiguous_heading", json.loads(result.stdout)["error"]["code"])
        self.write("changed")
        target = self.base / "stale-cli.jsonl"
        result = subprocess.run(command + ["read", "--root", str(self.root), "--path", "rules.md", "--expected-sha256", document["sha256"], "--receipt", str(target)], capture_output=True, text=True)
        self.assertEqual(2, result.returncode)
        self.assertEqual("stale_revision", json.loads(result.stdout)["error"]["code"])
        self.assertFalse(target.exists())

    def test_probe_reports_actual_local_capability_without_host_claim(self):
        result = reader.probe()
        self.assertTrue(result["source_reader"]["performed"])
        self.assertTrue(result["source_reader"]["exact_utf8_and_crlf"])
        self.assertTrue(result["sqlite_fts5"]["performed"])
        if result["sqlite_fts5"]["available"]:
            self.assertEqual(1, result["sqlite_fts5"]["matching_rows"])
        self.assertFalse(result["host_chat_export"]["observed"])
        self.assertFalse(result["comprehension_proven"])
        self.assertEqual([], list(self.root.iterdir()))


if __name__ == "__main__":
    unittest.main()
