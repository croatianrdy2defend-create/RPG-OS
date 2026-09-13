#!/usr/bin/env python3
"""Focused incremental persistence tests in isolated synthetic temp campaigns.

Run: python -X utf8 -B TOOLS/test_persistence.py
No live campaign records or actual play are created or changed by these tests.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("rpg_persistence", Path(__file__).with_name("persistence.py"))
assert SPEC and SPEC.loader
persistence = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = persistence
SPEC.loader.exec_module(persistence)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def values(value):
    """Yield nested stored values without assuming a journal directory layout."""
    if isinstance(value, dict):
        for child in value.values():
            yield from values(child)
    elif isinstance(value, list):
        for child in value:
            yield from values(child)
    else:
        yield value


class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rpg-persistence-tests-")
        self.root = Path(self.temp.name)
        self.temp_boundary = Path(tempfile.gettempdir()).resolve()
        self.addCleanup(self.cleanup_fixture)
        self.make_fixture(self.root)
        persistence.initialize(self.root, "test-thread")

    def cleanup_fixture(self):
        target = self.root.resolve()
        if target.parent != self.temp_boundary or not target.name.startswith("rpg-persistence-tests-"):
            raise RuntimeError("refusing cleanup outside isolated OS-temp fixture boundary")
        self.temp.cleanup()

    def write(self, relative, content, root=None):
        path = (root or self.root) / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def make_fixture(self, root, enabled=True):
        self.write("INSTANCE/CURRENT_SAVE.md", (
            "# Synthetic CURRENT_SAVE\n\n| Field | Value |\n|---|---|\n"
            "| campaign_id | fixture-campaign |\n| save_id | fixture-s0001 |\n"
            "| save_rev | 1 |\n| save_parent | none |\n| commit_kind | close |\n"
            "| archive_ref | sessions/fixture-s0001 |\n| evidence_through | fixture-s0001 |\n"
            "\n## Situation\n\nSynthetic fixture; no new action is resolved.\n"
        ), root)
        self.write("INSTANCE/CAMPAIGN_CONTRACT.md", (
            "# Synthetic contract\n\n| campaign_id | fixture-campaign |\n"
            "| contract_id | fixture-c0001 |\n| status | accepted |\n\n"
            + ("Incremental persistence: enabled\n" if enabled else "Incremental persistence: disabled\n")
            + "Incremental delivery observer: operator\n"
        ), root)
        self.write("INSTANCE/CHAR/PC.md", "# Synthetic PC\n\nCash: 100\nUnchanged qualifier: exact.\n", root)
        self.write("INSTANCE/NOW.md", "# Synthetic NOW\n\nNo active encounter.\n", root)
        self.write("INSTANCE/KNOWN.md", b"# Known\r\n\r\nUnchanged CRLF record.\r\n", root)
        self.write("OS/GM_RULES.md", "# Synthetic protected rules\n", root)
        self.write("ARCHIVE/sessions/fixture-s0001.md", "# Previous immutable evidence\n", root)
        self.write("ARCHIVE/INDEX.md", (
            "# Synthetic archive index\n\n"
            "| Save | Kind | Session | Span | Place | Terms | Notes | Folder | Index | Extra |\n"
            "|---|---|---|---|---|---|---|---|---|---|\n"
            "| fixture-s0001 | close | fixture-session | fixture start | fixture | baseline | previous | sessions/fixture-s0001 | sessions/fixture-s0001.md | |\n"
        ), root)

    def inventory(self):
        return {p.relative_to(self.root).as_posix(): digest(p.read_bytes())
                for p in self.root.rglob("*") if p.is_file()}

    def request(self, transaction_id="tx-1", before="Cash: 100", after="Cash: 88", **overrides):
        current = persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")
        result = {
            "transaction_id": transaction_id,
            "conversation_id": "test-thread",
            "expected_head": persistence.status(self.root)["head"],
            "user_text": "Synthetic established input.",
            "response": "Synthetic established result.",
            "changes": [{"path": "INSTANCE/CHAR/PC.md", "expected_sha256": current["sha256"],
                         "edits": [{"before": before, "after": after}]}],
        }
        result.update(overrides)
        return result

    def receipt(self, request, **overrides):
        result = {
            "schema": "rpg-delivery-v1",
            "conversation_id": request["conversation_id"],
            "transaction_id": request["transaction_id"],
            "assistant_text": request["response"],
            "user_text": request["user_text"],
            "source_ref": {"kind": "synthetic-fixture", "message_id": request["transaction_id"]},
            "complete": True,
            "observer": "operator",
        }
        result.update(overrides)
        return result

    def commit(self, request=None):
        request = request or self.request()
        persistence.prepare(self.root, request)
        persistence.confirm(self.root, self.receipt(request))
        return request

    def close_plan(self, save_id="fixture-s0003", **overrides):
        plan = {
            "save_id": save_id,
            "expected_head": persistence.status(self.root)["head"],
            "title": "Synthetic persisted exchange",
            "route_terms": "synthetic fixture; established resource change",
            "span": "fixture interval",
            "place": "fixture location",
            "session_id": "fixture-session",
            "review": {"status": "complete", "scope": "Synthetic fixture source and changed resource.",
                       "limitations": "No actual human play or semantic quality assessment."},
        }
        plan.update(overrides)
        return plan

    def test_partial_correction_preserves_surviving_source(self):
        response = 'Keep this. Wrong detail. Keep that.'
        request = self.request(response=response)
        self.commit(request)
        first = response.index('Wrong detail.')
        plan = self.close_plan(source_dispositions={request['transaction_id']: {
            'status': 'partly-superseded', 'reason': 'Explicit synthetic correction',
            'correction_ref': 'fixture-correction',
            'spans': [{'role': 'assistant', 'start': first, 'end': first + len('Wrong detail.')}],
        }})
        persistence.close(self.root, plan)
        body = (self.root / 'ARCHIVE/sessions/fixture-s0003/01_record.md').read_text(encoding='utf-8')
        self.assertIn('Keep this.', body)
        self.assertIn('Keep that.', body)
        self.assertNotIn('Wrong detail.', body)

    def test_partial_correction_rejects_out_of_bounds_without_publication(self):
        request = self.commit()
        plan = self.close_plan(source_dispositions={request['transaction_id']: {
            'status': 'partly-superseded', 'reason': 'Synthetic invalid span', 'correction_ref': 'fixture',
            'spans': [{'role': 'assistant', 'start': 0, 'end': 100000}],
        }})
        self.assert_rejected_without_mutation(persistence.close, self.root, plan)

    def test_review_boundary_updates_after_checkpoint_and_close(self):
        self.commit()
        persistence.checkpoint(self.root, 'fixture-s0002')
        current = persistence.read_current(self.root, 'INSTANCE/CURRENT_SAVE.md')['content']
        self.assertIn('no new semantic source-review claim', current)
        persistence.close(self.root, self.close_plan())
        current = persistence.read_current(self.root, 'INSTANCE/CURRENT_SAVE.md')['content']
        self.assertIn('EVIDENCE/incremental-reviews/fixture-s0003.json', current)
        self.assertNotIn('no new semantic source-review claim', current)

    def test_new_authorized_preparation_can_be_published_at_closure(self):
        self.commit()
        plan = self.close_plan(current_updates=[{'path': 'INSTANCE/PREP.md', 'expected_sha256': None,
                            'content': '# Preparation\n\nEstablished synthetic follow-up only.\n'}])
        persistence.close(self.root, plan)
        self.assertIn('Established synthetic', persistence.read_current(self.root, 'INSTANCE/PREP.md')['content'])

    def test_published_checkpoint_id_cannot_be_reused(self):
        self.commit()
        persistence.checkpoint(self.root, 'fixture-s0002')
        persistence.checkpoint(self.root, 'fixture-s0003')
        self.assert_rejected_without_mutation(persistence.checkpoint, self.root, 'fixture-s0002')

    def assert_rejected_without_mutation(self, function, *arguments):
        before = self.inventory()
        with self.assertRaises(persistence.PersistenceError):
            function(*arguments)
        self.assertEqual(before, self.inventory())

    def test_disabled_policy_does_not_initialize(self):
        other = self.root / "disabled-fixture"
        self.make_fixture(other, enabled=False)
        with self.assertRaises(persistence.PersistenceError):
            persistence.initialize(other, "test-thread")
        self.assertFalse((other / "INSTANCE/JOURNAL/HEAD.json").exists())

    def test_active_recovery_prevents_initialization(self):
        other = self.root / "recovering-fixture"
        self.make_fixture(other)
        self.write("RECOVERY/ACTIVE.md", "Existing interrupted operation.\n", other)
        with self.assertRaises(persistence.PersistenceError):
            persistence.initialize(other, "test-thread")
        self.assertFalse((other / "INSTANCE/JOURNAL/HEAD.json").exists())

    def test_initialize_does_not_change_existing_campaign_bytes(self):
        self.assertEqual((self.root / "INSTANCE/KNOWN.md").read_bytes(), b"# Known\r\n\r\nUnchanged CRLF record.\r\n")
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        self.assertIsNone(persistence.status(self.root)["head"])
        self.assert_rejected_without_mutation(persistence.initialize, self.root, "test-thread")

    def test_prepared_changes_are_recoverable_but_not_current(self):
        request = self.request()
        persistence.prepare(self.root, request)
        self.assertIn("Cash: 100", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        self.assertTrue(persistence.status(self.root)["pending"])
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        persistence.confirm(self.root, self.receipt(request))
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        self.assertIn("Cash: 100", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))

    def test_retry_prepare_and_confirm_applies_effect_exactly_once(self):
        request = self.request()
        persistence.prepare(self.root, request)
        persistence.prepare(self.root, request)
        persistence.confirm(self.root, self.receipt(request))
        persistence.confirm(self.root, self.receipt(request))
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)
        self.assertEqual(persistence.status(self.root)["head"], "tx-1")
        self.assertEqual(persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"].count("Cash: 88"), 1)

    def test_conflicting_same_transaction_identity_is_rejected(self):
        request = self.request()
        persistence.prepare(self.root, request)
        changed = copy.deepcopy(request)
        changed["response"] = "Different proposed outcome."
        self.assert_rejected_without_mutation(persistence.prepare, self.root, changed)

    def test_stale_predecessor_cannot_advance_campaign(self):
        self.commit()
        request = self.request("tx-2", "Cash: 88", "Cash: 76", expected_head=None)
        self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_another_conversation_cannot_silently_become_writer(self):
        request = self.request(conversation_id="another-thread")
        self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_completed_message_cannot_be_reused_under_different_transaction(self):
        first = self.commit()
        second = self.request("tx-2", "Cash: 88", "Cash: 76")
        persistence.prepare(self.root, second)
        duplicate_source = self.receipt(second, source_ref=self.receipt(first)["source_ref"])
        self.assert_rejected_without_mutation(persistence.confirm, self.root, duplicate_source)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])

    def test_operator_receipt_requires_explicit_accepted_observer_policy(self):
        other = self.root / "foreground-fixture"
        self.make_fixture(other)
        contract = other / "INSTANCE/CAMPAIGN_CONTRACT.md"
        contract.write_bytes(contract.read_bytes().replace(b"Incremental delivery observer: operator\n", b""))
        persistence.initialize(other, "test-thread")
        request = self.request()
        persistence.prepare(other, request)
        self.assert_rejected_without_mutation(persistence.confirm, other, self.receipt(request))
        self.assertEqual(persistence.status(other)["committed_seq"], 0)

    def test_changed_campaign_identity_is_detected(self):
        path = self.root / "INSTANCE/CURRENT_SAVE.md"
        path.write_text(path.read_text(encoding="utf-8").replace("fixture-campaign", "different-campaign"), encoding="utf-8")
        self.assert_rejected_without_mutation(persistence.status, self.root)

    def test_changed_expected_value_cannot_overwrite_other_work(self):
        request = self.request()
        request["changes"][0]["expected_sha256"] = "0" * 64
        self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_external_owner_change_cannot_be_silently_overlaid(self):
        self.commit()
        self.write("INSTANCE/CHAR/PC.md", "# Synthetic PC\n\nCash: 500\nExternal incompatible edit.\n")
        self.assert_rejected_without_mutation(persistence.read_current, self.root, "INSTANCE/CHAR/PC.md")

    def test_existing_record_cannot_be_replaced_wholesale(self):
        request = self.request()
        change = request["changes"][0]
        change.pop("edits")
        change["content"] = "Whole-body replacement would lose unchanged qualifications."
        self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_ambiguous_or_missing_exact_edit_is_rejected(self):
        for before in ("not present", "\n"):
            with self.subTest(before=before):
                request = self.request(before=before)
                self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_protected_and_escaping_paths_are_rejected(self):
        for path in ("../outside.md", "INSTANCE/../OS/GM_RULES.md", "OS/GM_RULES.md", "INSTANCE/CAMPAIGN_CONTRACT.md"):
            with self.subTest(path=path):
                request = self.request(changes=[{"path": path, "expected_sha256": None, "content": "unauthorized"}])
                self.assert_rejected_without_mutation(persistence.prepare, self.root, request)

    def test_symlink_does_not_turn_protected_file_into_allowed_owner(self):
        link = self.root / "INSTANCE/CHAR/linked.md"
        try:
            link.symlink_to(self.root / "OS/GM_RULES.md")
        except (OSError, NotImplementedError):
            self.skipTest("platform does not permit unprivileged symlink creation")
        original = (self.root / "OS/GM_RULES.md").read_bytes()
        request = self.request(changes=[{
            "path": "INSTANCE/CHAR/linked.md", "expected_sha256": digest(original),
            "edits": [{"before": "Synthetic protected rules", "after": "Changed rules"}],
        }])
        self.assert_rejected_without_mutation(persistence.prepare, self.root, request)
        self.assertEqual((self.root / "OS/GM_RULES.md").read_bytes(), original)

    def test_failed_delivery_receipts_do_not_commit(self):
        request = self.request()
        persistence.prepare(self.root, request)
        cases = ({"complete": False}, {"assistant_text": "abandoned alternative"},
                 {"user_text": "different input"}, {"conversation_id": "other-thread"},
                 {"source_ref": {}}, {"observer": "invented-observer"})
        for changes in cases:
            with self.subTest(changes=changes):
                self.assert_rejected_without_mutation(persistence.confirm, self.root, self.receipt(request, **changes))
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        self.assertIn("Cash: 100", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])

    def test_source_only_exchange_preserves_exact_text_without_state_fabrication(self):
        response = "Synthetic exact source — café.\r\nSecond line with  two spaces.\n"
        user = "Synthetic user input\r\nwith exact line endings."
        request = self.request(changes=[], response=response, user_text=user)
        before_pc = (self.root / "INSTANCE/CHAR/PC.md").read_bytes()
        self.commit(request)
        stored = []
        for path in (self.root / "INSTANCE/JOURNAL").rglob("*.json"):
            stored.extend(values(json.loads(path.read_text(encoding="utf-8"))))
        self.assertIn(response, stored)
        self.assertIn(user, stored)
        self.assertEqual(before_pc, (self.root / "INSTANCE/CHAR/PC.md").read_bytes())
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)

    def test_successive_real_changes_use_effective_preimage(self):
        self.commit()
        second = self.request("tx-2", "Cash: 88", "Cash: 76")
        self.commit(second)
        self.assertIn("Cash: 76", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        self.assertEqual(persistence.status(self.root)["committed_seq"], 2)

    def test_explicit_correction_supersedes_current_value_without_replaying_effect(self):
        self.commit()
        correction = self.request("tx-correction", "Cash: 88", "Cash: 90", user_text="Explicit fixture correction: amount was ten.")
        self.commit(correction)
        self.assertIn("Cash: 90", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        persistence.confirm(self.root, self.receipt(correction))
        self.assertEqual(persistence.status(self.root)["committed_seq"], 2)

    def test_new_record_is_readable_before_consolidation(self):
        path = "INSTANCE/PEOPLE/synthetic-person.md"
        body = "# Synthetic person\n\nEstablished fixture knowledge only.\n"
        request = self.request(changes=[{"path": path, "expected_sha256": None, "content": body}])
        self.commit(request)
        self.assertFalse((self.root / path).exists())
        self.assertEqual(persistence.read_current(self.root, path)["content"], body)
        persistence.checkpoint(self.root, "fixture-s0002")
        self.assertEqual((self.root / path).read_bytes(), body.encode("utf-8"))

    def test_checkpoint_consolidates_without_claiming_new_archive_coverage(self):
        self.commit()
        untouched = {relative: (self.root / relative).read_bytes() for relative in (
            "INSTANCE/KNOWN.md", "INSTANCE/NOW.md", "OS/GM_RULES.md", "ARCHIVE/sessions/fixture-s0001.md")}
        persistence.checkpoint(self.root, "fixture-s0002")
        self.assertIn("Cash: 88", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))
        save = (self.root / "INSTANCE/CURRENT_SAVE.md").read_text(encoding="utf-8")
        self.assertIn("| save_id | fixture-s0002 |", save)
        self.assertIn("| save_parent | fixture-s0001 |", save)
        self.assertIn("| save_rev | 2 |", save)
        self.assertIn("| archive_ref | sessions/fixture-s0001 |", save)
        self.assertIn("| evidence_through | fixture-s0001 |", save)
        self.assertIn("| journal_through | 1 |", save)
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 1)
        for relative, original in untouched.items():
            self.assertEqual((self.root / relative).read_bytes(), original, relative)

    def test_checkpoint_does_not_delete_unarchived_original_messages(self):
        request = self.commit()
        persistence.checkpoint(self.root, "fixture-s0002")
        stored = []
        for path in (self.root / "INSTANCE/JOURNAL").rglob("*.json"):
            stored.extend(values(json.loads(path.read_text(encoding="utf-8"))))
        self.assertIn(request["response"], stored)
        self.assertIn(request["user_text"], stored)

    def test_checkpoint_cannot_consolidate_unconfirmed_response(self):
        persistence.prepare(self.root, self.request())
        self.assert_rejected_without_mutation(persistence.checkpoint, self.root, "fixture-s0002")

    def interrupted_checkpoint(self):
        original = persistence._publish_write
        hits = []

        def fail_at_save(path, data):
            if Path(path).name == "CURRENT_SAVE.md":
                hits.append(str(path))
                raise OSError("Deliberate synthetic interrupted publication")
            return original(path, data)

        with mock.patch.object(persistence, "_publish_write", side_effect=fail_at_save):
            with self.assertRaises((OSError, persistence.PersistenceError)):
                persistence.checkpoint(self.root, "fixture-s0002")
        self.assertEqual(len(hits), 1, "fault injection must reach the save publication boundary")

    def test_interrupted_checkpoint_blocks_reads_and_finish_preserves_effect_once(self):
        self.commit()
        self.interrupted_checkpoint()
        with self.assertRaises(persistence.PersistenceError):
            persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")
        persistence.recover(self.root, "finish")
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 1)
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        self.assertIn("Cash: 88", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))
        self.assertIn("fixture-s0002", (self.root / "INSTANCE/CURRENT_SAVE.md").read_text(encoding="utf-8"))

    def test_restore_interrupted_checkpoint_retains_committed_journal_for_retry(self):
        self.commit()
        self.interrupted_checkpoint()
        persistence.recover(self.root, "restore")
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 0)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)
        self.assertIn("Cash: 100", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        persistence.checkpoint(self.root, "fixture-s0003")
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 1)
        self.assertIn("Cash: 88", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))

    def test_new_transactions_after_checkpoint_do_not_replay_old_effects(self):
        self.commit()
        persistence.checkpoint(self.root, "fixture-s0002")
        self.commit(self.request("tx-2", "Cash: 88", "Cash: 76"))
        self.assertIn("Cash: 88", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))
        self.assertIn("Cash: 76", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        persistence.checkpoint(self.root, "fixture-s0003")
        self.assertIn("Cash: 76", (self.root / "INSTANCE/CHAR/PC.md").read_text(encoding="utf-8"))
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 2)

    def test_rebind_after_consolidated_external_maintenance_preserves_metadata(self):
        self.commit()
        persistence.checkpoint(self.root, "fixture-s0002")
        save_path = self.root / "INSTANCE/CURRENT_SAVE.md"
        maintained_save = (save_path.read_bytes()
                           .replace(b"| save_id | fixture-s0002 |", b"| save_id | fixture-maintenance |")
                           .replace(b"| save_parent | fixture-s0001 |", b"| save_parent | fixture-s0002 |")
                           .replace(b"| save_rev | 2 |", b"| save_rev | 3 |"))
        save_path.write_bytes(maintained_save)
        contract_path = self.root / "INSTANCE/CAMPAIGN_CONTRACT.md"
        maintained_contract = contract_path.read_bytes().replace(b"fixture-c0001", b"fixture-c0002")
        contract_path.write_bytes(maintained_contract)
        self.assert_rejected_without_mutation(persistence.status, self.root)
        persistence.rebind(self.root, "new-thread", "fixture-s0002")
        self.assertEqual(save_path.read_bytes(), maintained_save)
        self.assertEqual(contract_path.read_bytes(), maintained_contract)
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 1)
        second = self.request("tx-2", "Cash: 88", "Cash: 76", conversation_id="new-thread")
        self.commit(second)
        self.assertIn("Cash: 76", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])

    def test_rebind_cannot_absorb_unconsolidated_changes(self):
        self.commit()
        self.assert_rejected_without_mutation(persistence.rebind, self.root, "new-thread", "fixture-s0001")

    def test_rebind_cannot_absorb_pending_response(self):
        persistence.prepare(self.root, self.request())
        self.assert_rejected_without_mutation(persistence.rebind, self.root, "new-thread", "fixture-s0001")

    def test_full_save_after_checkpoint_archives_without_reapplying_effect(self):
        request = self.commit()
        persistence.checkpoint(self.root, "fixture-s0002")
        pc_before = (self.root / "INSTANCE/CHAR/PC.md").read_bytes()
        plan = self.close_plan()
        result = persistence.close(self.root, plan)
        self.assertEqual(result["archived_exchanges"], 1)
        self.assertEqual((self.root / "INSTANCE/CHAR/PC.md").read_bytes(), pc_before)
        source = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_text(encoding="utf-8")
        self.assertIn(request["response"], source)
        self.assertIn(request["user_text"], source)
        save = (self.root / "INSTANCE/CURRENT_SAVE.md").read_text(encoding="utf-8")
        self.assertIn("| evidence_through | fixture-s0003 |", save)
        self.assertIn("| journal_archive_through | 1 |", save)
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 1)
        before = self.inventory()
        persistence.close(self.root, plan)
        self.assertEqual(before, self.inventory(), "retrying an already published close must not append archive rows")

    def test_full_save_archive_excludes_private_change_payload(self):
        request = self.request(changes=[{
            "path": "INSTANCE/PEOPLE/synthetic-private.md", "expected_sha256": None,
            "content": "# Private fixture state\nSecret fixture determination: withheld-marker-319.\n",
        }])
        self.commit(request)
        persistence.close(self.root, self.close_plan())
        public_archive = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_text(encoding="utf-8")
        self.assertNotIn("withheld-marker-319", public_archive)
        self.assertIn("withheld-marker-319", (self.root / "INSTANCE/PEOPLE/synthetic-private.md").read_text(encoding="utf-8"))

    def test_superseded_source_is_excluded_from_accepted_archive_but_retained_raw(self):
        original_text = "Original superseded fixture-only text."
        self.commit(self.request(response=original_text))
        correction = self.request("tx-correction", "Cash: 88", "Cash: 90", response="Accepted corrected fixture result.")
        self.commit(correction)
        disposition = {"tx-1": {"status": "superseded", "reason": "Explicit fixture correction accepted.",
                                  "correction_ref": {"transaction_id": "tx-correction"}}}
        persistence.close(self.root, self.close_plan(source_dispositions=disposition))
        archive = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_text(encoding="utf-8")
        self.assertNotIn(original_text, archive)
        self.assertIn("Accepted corrected fixture result.", archive)
        self.assertIn("Excluded from accepted fiction", archive)
        stored = json.loads((self.root / "INSTANCE/JOURNAL/batches/tx-1.json").read_text(encoding="utf-8"))
        self.assertIn(original_text, list(values(stored)))
        self.assertIn("Cash: 90", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])

    def test_superseded_source_requires_explicit_correction_reference(self):
        self.commit()
        plan = self.close_plan(source_dispositions={"tx-1": {"status": "superseded", "reason": "Unsupported omission."}})
        self.assert_rejected_without_mutation(persistence.close, self.root, plan)

    def test_session_feedback_evidence_preserves_actual_fixture_text_and_source(self):
        self.commit()
        feedback = "Synthetic feedback: preserve this exact wording.\r\n```quoted boundary```\n"
        source = {"kind": "synthetic-fixture", "message_id": "feedback-1"}
        plan = self.close_plan(operational_evidence=[{"session_id": "fixture-session", "text": feedback,
                                                      "source_ref": source}])
        persistence.close(self.root, plan)
        archive = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_bytes()
        self.assertIn(feedback.encode("utf-8"), archive)
        self.assertIn(b"OOC session operational evidence", archive)
        self.assertIn(b"feedback-1", archive)
        self.assertIn(b"fixture-session", archive)

    def test_later_full_save_archives_only_unarchived_source(self):
        self.commit(self.request(response="First exact fixture response."))
        persistence.close(self.root, self.close_plan())
        original_archive = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_bytes()
        self.commit(self.request("tx-2", "Cash: 88", "Cash: 76", response="Second exact fixture response."))
        result = persistence.close(self.root, self.close_plan("fixture-s0004"))
        self.assertEqual(result["archived_exchanges"], 1)
        new_archive = (self.root / "ARCHIVE/sessions/fixture-s0004/01_record.md").read_text(encoding="utf-8")
        self.assertIn("Second exact fixture response.", new_archive)
        self.assertNotIn("First exact fixture response.", new_archive)
        self.assertEqual((self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_bytes(), original_archive)
        self.assertIn("Cash: 76", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])

    def test_incomplete_review_is_published_as_incomplete(self):
        self.commit()
        review = {"status": "incomplete", "scope": "One bounded fixture check.",
                  "limitations": "Independent source review remains unfinished."}
        result = persistence.close(self.root, self.close_plan(review=review))
        self.assertEqual(result["review_status"], "incomplete")
        receipt = json.loads((self.root / "EVIDENCE/incremental-reviews/fixture-s0003.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["review"], review)

    def test_interrupted_full_save_restore_removes_new_archive_but_preserves_journal(self):
        self.commit()
        archive_index = (self.root / "ARCHIVE/INDEX.md").read_bytes()
        original = persistence._publish_write

        def fail_at_save(path, data):
            if Path(path).name == "CURRENT_SAVE.md":
                raise OSError("Deliberate interrupted full save")
            return original(path, data)

        with mock.patch.object(persistence, "_publish_write", side_effect=fail_at_save):
            with self.assertRaises((OSError, persistence.PersistenceError)):
                persistence.close(self.root, self.close_plan())
        persistence.recover(self.root, "restore")
        self.assertEqual((self.root / "ARCHIVE/INDEX.md").read_bytes(), archive_index)
        self.assertFalse((self.root / "ARCHIVE/sessions/fixture-s0003").exists())
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)
        self.assertEqual(persistence.status(self.root)["consolidated_through"], 0)
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
