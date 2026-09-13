#!/usr/bin/env python3
"""Isolated lexical-index regressions; no live campaign writes or external services.

Run: python -B TOOLS/test_search_index.py
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import read_source
import search_index as index


class LexicalIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_parent = HERE.parent / ".work" / "test_search_index"
        self.fixture_parent.mkdir(parents=True, exist_ok=True)
        self.case = Path(tempfile.mkdtemp(prefix="case-", dir=self.fixture_parent))
        self.root = self.case / "campaign"
        self.root.mkdir()
        self.db = self.case / "candidate-cache.sqlite3"
        self.addCleanup(self.remove_fixture)
        self.write("INSTANCE/CURRENT_SAVE.md", "# Current save\n\nThe observatory capacity is 20.\n")
        self.write("INSTANCE/CORRECTIONS.md", "# Corrections\n\nObservatory rulings apply only to the east dome.\n")
        self.write("MODULES/brine/CANON.md", "# Brine canon\n\nThe observatory stands beside the grey estuary.\n")
        self.write("ARCHIVE/INDEX.md", "# Archive index\n\n| route_terms | folder |\n|---|---|\n| observatory | ARCHIVE/s01/EVENTS.md |\n")
        self.write("ARCHIVE/s01/EVENTS.md", "# Earlier scene\n\nThe observatory capacity was 5 before repairs.\n")
        self.write("EVIDENCE/captures/c01/source.txt", "The operator said: observatory notes remain unverified.\n")
        self.write("ENGINE/freeform.md", "# Freeform\n\nAn observatory challenge uses accepted stakes.\n")
        self.write("OS/RETRIEVAL.md", "# Retrieval\n\nAn observatory lookup needs the original source.\n")

    def remove_fixture(self) -> None:
        # Check the final resolved target before recursive deletion on Windows.
        resolved = self.case.resolve()
        if resolved.parent != self.fixture_parent.resolve() or not resolved.name.startswith("case-"):
            raise RuntimeError("Refusing cleanup outside isolated test fixture")
        shutil.rmtree(resolved)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="")
        return path

    def build(self) -> dict:
        if not index.fts5_available():
            self.skipTest("SQLite was compiled without FTS5; optional fallback tested separately")
        return index.build_index(self.root, self.db)

    def candidate(self, query: str, scope: str = "current") -> dict:
        result = index.search(self.root, self.db, query, scope)
        self.assertTrue(result["candidates"], result)
        return result["candidates"][0]

    def snapshot(self) -> dict:
        return {path.relative_to(self.root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in self.root.rglob("*") if path.is_file()}

    def test_late_file_term_routes_to_its_child_and_fetch_is_exact(self) -> None:
        self.write("INSTANCE/PEOPLE/agent.md", "---\nid: person.maren\n---\n\n# Maren\n\n"
                   + "Ordinary early material.\n" * 12000
                   + "\n## Under the eastern dome\n\nHer private password is tidalquartz.\n")
        self.build()
        result = index.search(self.root, self.db, "tidalquartz")
        self.assertEqual(1, len(result["candidates"]))
        candidate = result["candidates"][0]
        self.assertEqual("Under the eastern dome", candidate["heading"])
        self.assertEqual(["Maren", "Under the eastern dome"], candidate["heading_path"])
        self.assertGreater(candidate["start_line"], 12000)
        self.assertNotIn("text", candidate)
        fetched = index.fetch_candidate(self.root, self.db, candidate)
        self.assertEqual("## Under the eastern dome\n\nHer private password is tidalquartz.\n", fetched["passage"]["text"])
        self.assertTrue(fetched["source_revision_verified"])

    def test_existing_ids_frontmatter_aliases_and_field_table_names(self) -> None:
        self.write("INSTANCE/PEOPLE/agent.md", "---\nid: person.maren\nname: Maren Vale\naliases:\n"
                   "  - Harbor Lantern\n  - 'Blue Courier'\n---\n\n# Local agent\n\n"
                   "| Field | Value |\n|---|---|\n| aliases | Tide Listener; Quiet Bell |\n\n"
                   "## Condition\n\nWaiting near the quay.\n")
        self.build()
        for query in ("person.maren", "Harbor Lantern", "Blue Courier", "Maren Vale", "Quiet Bell"):
            with self.subTest(query=query):
                candidate = self.candidate(query)
                self.assertEqual("INSTANCE/PEOPLE/agent.md", candidate["path"])
        self.assertIn("Harbor Lantern", self.candidate("Harbor Lantern")["identities"])

    def test_default_current_never_combines_prior_and_current_values(self) -> None:
        self.build()
        current = index.search(self.root, self.db, "capacity")
        self.assertEqual({"current"}, {item["scope"] for item in current["candidates"]})
        self.assertEqual(1, len(current["candidates"]))
        actual = index.fetch_candidate(self.root, self.db, current["candidates"][0])["passage"]["text"]
        self.assertIn("20", actual)
        self.assertNotIn("was 5", actual)
        old = self.candidate("capacity", "history")
        with self.assertRaises(index.SearchError) as denied:
            index.fetch_candidate(self.root, self.db, old)
        self.assertEqual("scope_denied", denied.exception.code)
        self.assertIn("was 5", index.fetch_candidate(self.root, self.db, old, "history")["passage"]["text"])

    def test_every_scope_filters_and_fetch_rechecks_scope(self) -> None:
        self.build()
        expected = {"current", "world", "history", "raw", "rules"}
        for scope in expected:
            with self.subTest(scope=scope):
                result = index.search(self.root, self.db, "observatory", scope)
                self.assertTrue(result["candidates"])
                self.assertEqual({scope}, {candidate["scope"] for candidate in result["candidates"]})
                for candidate in result["candidates"]:
                    self.assertEqual("verified", index.fetch_candidate(self.root, self.db, candidate, scope)["status"])
                    wrong_scope = "world" if scope != "world" else "current"
                    with self.assertRaises(index.SearchError):
                        index.fetch_candidate(self.root, self.db, candidate, wrong_scope)
        result = index.search(self.root, self.db, "observatory", "all", 100)
        self.assertEqual(expected, {candidate["scope"] for candidate in result["candidates"]})
        self.assertFalse(result["ranking_is_authority"])

    def test_corrections_rules_and_archive_indexes_are_route_hints(self) -> None:
        self.build()
        correction = self.candidate("rulings", "rules")
        self.assertEqual("correction-register", correction["source_class"])
        self.assertEqual([], index.search(self.root, self.db, "rulings")["candidates"])
        route = next(item for item in index.search(self.root, self.db, "observatory", "history")["candidates"]
                     if item["path"] == "ARCHIVE/INDEX.md")
        self.assertEqual("route-hint", route["source_class"])
        self.assertEqual("route-hint", index.fetch_candidate(self.root, self.db, route, "history")["source_class"])

    def test_preamble_plain_text_and_parent_routes_are_searchable(self) -> None:
        self.write("INSTANCE/notes.md", "Preamble says copperkin.\n\n# Shared family\n\nIntro.\n\n"
                   "## Child\n\nThe token is eastglass.\n")
        self.build()
        preamble = self.candidate("copperkin")
        self.assertEqual(1, preamble["start_line"])
        self.assertEqual("Preamble says copperkin.\n\n", index.fetch_candidate(self.root, self.db, preamble)["passage"]["text"])
        child = self.candidate("family eastglass")
        self.assertEqual("Child", child["heading"])
        raw = self.candidate("unverified", "raw")
        self.assertIn("operator said", index.fetch_candidate(self.root, self.db, raw, "raw")["passage"]["text"])

    def test_disallowed_trees_raw_manifests_private_artifacts_and_binary_are_excluded(self) -> None:
        for relative in (
            "ADMIN/plan.md", "UNKNOWN/notes.md", "RECOVERY/old.md", "HANDOVER/notes.md",
            ".git/secret.md", ".work/secret.md", ".release/secret.md",
            "INSTANCE/RECOVERY/old.md", "MODULES/othercampaigns/current.md",
            "MODULES/private-campaigns/current.md", "EVIDENCE/other/source.txt",
            "EVIDENCE/captures/c01/manifest.md", "EVIDENCE/captures/c01/private-notes.txt",
            "EVIDENCE/captures/c01/private_artifacts/transcript.txt",
            "EVIDENCE/captures/c01/artifacts/export.txt", "CORRECTIONS.md",
        ):
            self.write(relative, "forbiddenneedle\n")
        self.write("MODULES/nested-campaign/OS/AGENTS.md", "forbiddenneedle\n")
        self.write("MODULES/nested-campaign/INSTANCE/CURRENT_SAVE.md", "forbiddenneedle\n")
        self.write("EVIDENCE/captures/c01/manifest.json", '{"text":"forbiddenneedle"}')
        self.write("EVIDENCE/captures/c01/photo.png", "forbiddenneedle")
        binary = self.write("EVIDENCE/captures/c01/binary.md", "")
        binary.write_bytes(b"forbiddenneedle\x00data")
        invalid = self.write("EVIDENCE/captures/c01/invalid.txt", "")
        invalid.write_bytes(b"forbiddenneedle\xff")
        self.write("EVIDENCE/captures/c02/source.jsonl", '{"role":"user","text":"capturequartz"}\n')
        built = self.build()
        self.assertEqual([], index.search(self.root, self.db, "forbiddenneedle", "all")["candidates"])
        self.assertEqual("raw", self.candidate("capturequartz", "raw")["scope"])
        self.assertEqual({"binary_source", "invalid_utf8", "nested-campaign-root"}, {item["reason"] for item in built["skipped"]})

    def test_reparse_directory_and_special_file_are_skipped_before_reading(self) -> None:
        self.write("INSTANCE/junction/stolen.md", "reparseneedle\n")
        special = self.write("INSTANCE/special.md", "specialneedle\n")
        link = self.root / "INSTANCE" / "junction"
        original = Path.lstat

        def lstat(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == link or path == special:
                fields = {name: getattr(info, name) for name in dir(info) if name.startswith("st_")}
                if path == link:
                    fields["st_file_attributes"] = 0x400
                else:
                    fields["st_mode"] = 0o010600  # FIFO: never open it as text.
                return SimpleNamespace(**fields)
            return info

        with patch.object(Path, "lstat", lstat):
            built = self.build()
            self.assertEqual([], index.search(self.root, self.db, "reparseneedle", "all")["candidates"])
            self.assertEqual([], index.search(self.root, self.db, "specialneedle", "all")["candidates"])
        self.assertEqual({"link-or-reparse-point", "special-file"}, {item["reason"] for item in built["skipped"]})

    def test_real_symlink_source_is_excluded_when_supported(self) -> None:
        external = self.case / "outside.txt"
        external.write_text("externalneedle", encoding="utf-8")
        link = self.root / "INSTANCE" / "linked.txt"
        try:
            link.symlink_to(external)
        except (OSError, NotImplementedError):
            self.skipTest("Host does not permit unprivileged symlink creation")
        built = self.build()
        self.assertIn({"path": "INSTANCE/linked.txt", "reason": "link-or-reparse-point"}, built["skipped"])
        self.assertEqual([], index.search(self.root, self.db, "externalneedle", "all")["candidates"])

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_actual_windows_junction_source_and_database_parent_are_refused(self) -> None:
        outside = self.case / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("junctionneedle", encoding="utf-8")
        junction = self.root / "INSTANCE" / "junction"
        escaped_path = str(junction).replace("'", "''")
        escaped_target = str(outside).replace("'", "''")
        result = subprocess.run([
            "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
            f"New-Item -ItemType Junction -Path '{escaped_path}' -Target '{escaped_target}' -ErrorAction Stop | Out-Null",
        ], capture_output=True, text=True)
        if result.returncode:
            self.skipTest("Host does not permit a temporary Windows junction")
        self.addCleanup(junction.rmdir)
        built = self.build()
        self.assertIn({"path": "INSTANCE/junction", "reason": "link-or-reparse-point"}, built["skipped"])
        self.assertEqual([], index.search(self.root, self.db, "junctionneedle", "all")["candidates"])
        with self.assertRaises(index.SearchError):
            index.build_index(self.root, junction / "cache.sqlite3")
        self.assertFalse((outside / "cache.sqlite3").exists())
        self.assertEqual("junctionneedle", (outside / "secret.txt").read_text(encoding="utf-8"))

    @unittest.skipUnless(os.name == "nt", "Windows short-path regression")
    def test_short_root_alias_cannot_place_database_inside_source_root(self) -> None:
        import ctypes
        buffer = ctypes.create_unicode_buffer(32768)
        length = ctypes.windll.kernel32.GetShortPathNameW(str(self.root), buffer, len(buffer))
        if not length or buffer.value.casefold() == str(self.root).casefold():
            self.skipTest("Host has no alternate short-path alias for this fixture")
        inside = self.root / "inside.sqlite3"
        with self.assertRaises(index.SearchError) as rejected:
            index.build_index(Path(buffer.value), inside)
        self.assertEqual("unsafe_database", rejected.exception.code)
        self.assertFalse(inside.exists())

    def test_status_detects_same_size_edit_even_with_restored_mtime(self) -> None:
        self.build()
        source = self.root / "INSTANCE/CURRENT_SAVE.md"
        before = source.stat()
        self.write("INSTANCE/CURRENT_SAVE.md", source.read_text(encoding="utf-8").replace("20", "99"))
        os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
        os.utime(self.db, None)
        status = index.index_status(self.root, self.db)
        self.assertEqual("stale", status["status"])
        self.assertEqual(["INSTANCE/CURRENT_SAVE.md"], status["changed"])

    def test_status_detects_additions_and_deletions(self) -> None:
        self.build()
        self.write("INSTANCE/new.md", "newonlyterm\n")
        (self.root / "MODULES/brine/CANON.md").unlink()
        status = index.index_status(self.root, self.db)
        self.assertEqual("stale", status["status"])
        self.assertEqual(["INSTANCE/new.md"], status["added"])
        self.assertEqual(["MODULES/brine/CANON.md"], status["deleted"])
        search = index.search(self.root, self.db, "newonlyterm")
        self.assertEqual("stale", search["status"])
        self.assertEqual([], search["candidates"])
        self.assertIn("fact is absent", search["retrieval_notice"])

    def test_mtime_only_change_does_not_make_cache_stale(self) -> None:
        self.build()
        source = self.root / "INSTANCE/CURRENT_SAVE.md"
        before = source.stat()
        os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns + 1000000000))
        os.utime(self.db, ns=(before.st_atime_ns, 1000000000))
        self.assertEqual("ready", index.index_status(self.root, self.db)["status"])

    def test_search_freshness_and_source_reads_stay_in_selected_scope(self) -> None:
        self.build()
        self.write("ARCHIVE/new.md", "Another observatory event.\n")
        self.write("ARCHIVE/s01/EVENTS.md", "An edited old event.\n")
        (self.root / "ARCHIVE/INDEX.md").unlink()
        original = read_source.load_document
        loaded = []

        def observe(root, relative, *args, **kwargs):
            loaded.append(relative)
            return original(root, relative, *args, **kwargs)

        with patch.object(index.read_source, "load_document", side_effect=observe):
            result = index.search(self.root, self.db, "capacity")
            candidate = result["candidates"][0]
            fetched = index.fetch_candidate(self.root, self.db, candidate)
        self.assertEqual("ready", result["status"])
        self.assertEqual("current", result["freshness_scope"])
        self.assertEqual([], result["added"] + result["deleted"] + result["changed"])
        self.assertTrue(loaded)
        self.assertTrue(all(index.classify_source(relative)[0] == "current" for relative in loaded))
        self.assertEqual("not_rechecked", fetched["cache_freshness"]["status"])
        history = index.search(self.root, self.db, "observatory", "history")
        self.assertEqual("stale", history["status"])
        self.assertEqual("history", history["freshness_scope"])
        self.assertEqual(["ARCHIVE/new.md"], history["added"])
        self.assertEqual(["ARCHIVE/INDEX.md"], history["deleted"])
        self.assertEqual(["ARCHIVE/s01/EVENTS.md"], history["changed"])
        self.assertEqual("stale", index.index_status(self.root, self.db)["status"])
        self.assertEqual("stale", index.search(self.root, self.db, "capacity", "all")["status"])

    def test_stale_search_is_flagged_and_fetch_refuses_changed_source(self) -> None:
        self.build()
        before = self.candidate("capacity")
        self.write("INSTANCE/CURRENT_SAVE.md", "# Replacement\n\nNo old observatory content.\n")
        result = index.search(self.root, self.db, "capacity")
        self.assertEqual("stale", result["status"])
        self.assertTrue(result["candidates"][0]["cache_stale"])
        with self.assertRaises(read_source.SourceError) as rejected:
            index.fetch_candidate(self.root, self.db, before)
        self.assertEqual("stale_revision", rejected.exception.code)

    def test_unchanged_candidate_can_be_verified_when_another_source_was_added(self) -> None:
        self.build()
        candidate = self.candidate("capacity")
        self.write("INSTANCE/new.md", "A new unrelated record.\n")
        self.assertEqual("stale", index.index_status(self.root, self.db)["status"])
        self.assertEqual("verified", index.fetch_candidate(self.root, self.db, candidate)["status"])

    def test_fetch_never_scans_unrelated_collection(self) -> None:
        self.build()
        candidate = self.candidate("capacity")
        with patch.object(index, "collect_sources", side_effect=AssertionError("collection read")), \
             patch.object(index, "_walk_sources", side_effect=AssertionError("collection walk")):
            fetched = index.fetch_candidate(self.root, self.db, candidate)
        self.assertEqual("verified", fetched["status"])
        self.assertIsNone(fetched["cache_freshness"]["fresh"])
        self.assertTrue(fetched["source_revision_verified"])

    def test_search_walks_collection_once(self) -> None:
        self.build()
        with patch.object(index, "_walk_sources", wraps=index._walk_sources) as walk:
            result = index.search(self.root, self.db, "capacity")
        self.assertEqual("ready", result["status"])
        self.assertEqual(1, walk.call_count)

    def test_fetch_refuses_deleted_sources_and_obsolete_generations(self) -> None:
        self.build()
        candidate = self.candidate("capacity")
        self.build()
        with self.assertRaises(index.SearchError) as obsolete:
            index.fetch_candidate(self.root, self.db, candidate)
        self.assertEqual("stale_candidate", obsolete.exception.code)
        candidate = self.candidate("capacity")
        (self.root / candidate["path"]).unlink()
        with self.assertRaises((read_source.SourceError, index.SearchError)):
            index.fetch_candidate(self.root, self.db, candidate)

    def test_new_nested_campaign_is_excluded_from_stale_search_and_fetch(self) -> None:
        self.write("MODULES/side/notes.md", "# Sidebar\n\nNestedcampneedle.\n")
        self.build()
        candidate = self.candidate("Nestedcampneedle", "world")
        self.write("MODULES/side/INSTANCE/CURRENT_SAVE.md", "# Separate campaign\n")
        self.write("MODULES/side/OS/AGENTS.md", "# Separate rules\n")
        result = index.search(self.root, self.db, "Nestedcampneedle", "world")
        self.assertEqual("stale", result["status"])
        self.assertEqual([], result["candidates"])
        with self.assertRaises(index.SearchError) as rejected:
            index.fetch_candidate(self.root, self.db, candidate, "world")
        self.assertEqual("scope_denied", rejected.exception.code)

    def test_corrupt_synthetic_ranges_cannot_expand_to_whole_source(self) -> None:
        self.write("EVIDENCE/captures/c03/source.txt", "prefix\nrangequartz\nprotected suffix\n")
        self.build()
        candidate = self.candidate("rangequartz", "raw")
        with contextlib.closing(sqlite3.connect(self.db)) as connection, connection:
            connection.execute("UPDATE sections SET start_line=2, end_line=2 WHERE id=?", (candidate["candidate_id"],))
        candidate = self.candidate("rangequartz", "raw")
        with self.assertRaises(index.SearchError) as rejected:
            index.fetch_candidate(self.root, self.db, candidate, "raw")
        self.assertEqual("corrupt", rejected.exception.code)
        with contextlib.closing(sqlite3.connect(self.db)) as connection, connection:
            connection.execute("UPDATE sections SET start_line=500, end_line=1 WHERE id=?", (candidate["candidate_id"],))
        self.assertEqual("corrupt", index.index_status(self.root, self.db)["status"])
        self.assertEqual("corrupt", index.search(self.root, self.db, "rangequartz", "raw")["status"])

    def test_wrong_campaign_database_and_candidate_are_refused(self) -> None:
        self.build()
        candidate = self.candidate("capacity")
        other = self.case / "other-campaign"
        other.mkdir()
        self.assertEqual("wrong_root", index.index_status(other, self.db)["status"])
        result = index.search(other, self.db, "capacity", "all")
        self.assertEqual("wrong_root", result["status"])
        self.assertEqual([], result["candidates"])
        candidate["root_id"] = "root-other"
        with self.assertRaises(index.SearchError) as rejected:
            index.fetch_candidate(self.root, self.db, candidate)
        self.assertEqual("stale_candidate", rejected.exception.code)

    def test_candidate_path_hash_scope_and_range_cannot_be_forged(self) -> None:
        self.build()
        base = self.candidate("capacity")
        for field, value in (("path", "../outside.txt"), ("source_sha256", "0" * 64),
                             ("scope", "raw"), ("start_line", 400), ("end_line", 900),
                             ("heading", "Invented heading")):
            with self.subTest(field=field):
                candidate = {**base, field: value}
                with self.assertRaises(index.SearchError) as rejected:
                    index.fetch_candidate(self.root, self.db, candidate, "all")
                self.assertEqual("invalid_candidate", rejected.exception.code)

    def test_missing_and_corrupt_cache_report_fallback_and_direct_pointer_still_works(self) -> None:
        self.assertEqual("missing", index.index_status(self.root, self.db)["status"])
        result = index.search(self.root, self.db, "observatory")
        self.assertEqual("missing", result["status"])
        self.assertIn("known source pointer", result["message"])
        self.db.write_bytes(b"This is not a SQLite database.")
        self.assertEqual("corrupt", index.index_status(self.root, self.db)["status"])
        self.assertEqual("corrupt", index.search(self.root, self.db, "observatory")["status"])
        document = read_source.load_document(self.root, "INSTANCE/CURRENT_SAVE.md")
        self.assertIn("capacity is 20", read_source.select_passage(document)["text"])
        self.build()
        self.assertEqual("ready", index.index_status(self.root, self.db)["status"])

    def test_no_fts5_is_explicit_and_never_prevents_direct_source_reads(self) -> None:
        self.db.write_bytes(b"placeholder")
        with patch.object(index, "fts5_available", return_value=False):
            self.assertEqual("fts_unavailable", index.index_status(self.root, self.db)["status"])
            self.assertEqual("fts_unavailable", index.search(self.root, self.db, "observatory")["status"])
            with self.assertRaises(index.SearchError) as rejected:
                index.build_index(self.root, self.db)
            self.assertEqual("fts_unavailable", rejected.exception.code)
        self.assertEqual(b"placeholder", self.db.read_bytes())
        self.assertIn("observatory", read_source.load_document(self.root, "INSTANCE/CURRENT_SAVE.md")["text"])

    def test_failed_rebuild_preserves_old_database_and_cleans_only_temporary_files(self) -> None:
        self.build()
        before = self.db.read_bytes()
        witness = self.case / "untouched.txt"
        witness.write_text("keep", encoding="utf-8")
        with patch.object(index, "_verify_database", side_effect=index.SearchError("injected verification failure")):
            with self.assertRaises(index.SearchError):
                index.build_index(self.root, self.db)
        self.assertEqual(before, self.db.read_bytes())
        self.assertEqual("keep", witness.read_text(encoding="utf-8"))
        self.assertEqual([], list(self.case.glob(".candidate-cache.sqlite3.build-*")))
        self.assertEqual("ready", index.index_status(self.root, self.db)["status"])

    def test_publish_failure_preserves_old_database(self) -> None:
        self.build()
        before = self.db.read_bytes()
        with patch.object(index.os, "replace", side_effect=PermissionError("injected file lock")):
            with self.assertRaises(PermissionError):
                index.build_index(self.root, self.db)
        self.assertEqual(before, self.db.read_bytes())
        self.assertEqual([], list(self.case.glob(".candidate-cache.sqlite3.build-*")))

    def test_source_change_during_rebuild_prevents_publication(self) -> None:
        self.build()
        before = self.db.read_bytes()
        original = index._verify_database

        def verify_and_change(connection):
            original(connection)
            self.write("INSTANCE/appeared.md", "Changed during construction.\n")

        with patch.object(index, "_verify_database", side_effect=verify_and_change):
            with self.assertRaises(index.SearchError) as rejected:
                index.build_index(self.root, self.db)
        self.assertEqual("source_changed", rejected.exception.code)
        self.assertEqual(before, self.db.read_bytes())

    def test_unreadable_source_makes_freshness_unknown_and_rebuild_preserves_cache(self) -> None:
        self.build()
        before = self.db.read_bytes()
        with patch.object(index.read_source, "load_document", side_effect=read_source.SourceError("denied", "unreadable_source")):
            status = index.index_status(self.root, self.db)
            self.assertEqual("unknown", status["status"])
            self.assertFalse(status["fresh"])
            result = index.search(self.root, self.db, "capacity")
            self.assertEqual("unknown", result["status"])
            self.assertTrue(result["candidates"][0]["cache_stale"])
            with self.assertRaises(read_source.SourceError):
                index.build_index(self.root, self.db)
        self.assertEqual(before, self.db.read_bytes())

    def test_cache_deletion_and_queries_do_not_change_any_sources(self) -> None:
        before = self.snapshot()
        root_mtime = self.root.stat().st_mtime_ns
        self.build()
        self.candidate("capacity")
        index.index_status(self.root, self.db)
        self.db.unlink()
        self.assertEqual(before, self.snapshot())
        self.assertEqual(root_mtime, self.root.stat().st_mtime_ns)
        self.assertEqual("missing", index.index_status(self.root, self.db)["status"])

    def test_database_inside_read_root_is_rejected_before_writing(self) -> None:
        inside = self.root / "INSTANCE" / "cache.sqlite3"
        with self.assertRaises(index.SearchError) as rejected:
            index.build_index(self.root, inside)
        self.assertEqual("unsafe_database", rejected.exception.code)
        self.assertFalse(inside.exists())

    def test_literal_query_and_no_match_have_bounded_honest_results(self) -> None:
        self.build()
        result = index.search(self.root, self.db, '" OR (imaginaryneedle) --')
        self.assertEqual([], result["candidates"])
        self.assertEqual("ready", result["status"])
        self.assertIn("fact is absent", result["retrieval_notice"])
        for query in ("", "***", "word " * 100):
            with self.assertRaises(index.SearchError):
                index.search(self.root, self.db, query)

    def test_fetch_character_cap_keeps_shared_reader_truncation_receipt(self) -> None:
        self.build()
        candidate = self.candidate("capacity")
        result = index.fetch_candidate(self.root, self.db, candidate, max_chars=12)
        self.assertEqual(12, len(result["passage"]["text"]))
        self.assertTrue(result["passage"]["truncated"])
        self.assertFalse(result["passage"]["complete"])

    def test_cli_build_status_search_and_fetch_json(self) -> None:
        self.build()
        common = ["--root", str(self.root), "--db", str(self.db)]
        for command in ("build", "status"):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = index.main([command, *common])
            self.assertEqual(0, code)
            self.assertEqual("ready", json.loads(output.getvalue())["status"])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = index.main(["search", *common, "capacity"])
        self.assertEqual(0, code)
        candidate = json.loads(output.getvalue())["candidates"][0]
        with patch.object(sys, "stdin", io.StringIO(json.dumps(candidate))):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = index.main(["fetch", *common, "--candidate", "-"])
        self.assertEqual(0, code)
        self.assertEqual("verified", json.loads(output.getvalue())["status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
