"""Independent crash and observed-delivery regressions; isolated fixtures only."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import uuid

import codex_exchange
import test_persistence as support

persistence = support.persistence
THREAD = "11111111-1111-4111-8111-111111111111"


class DeliveryPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rpg-delivery-regression-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fx = support.PersistenceTests()
        self.fx.root = self.root
        self.fx.make_fixture(self.root)
        contract = self.root / persistence.CONTRACT
        contract.write_bytes(contract.read_bytes().replace(b"Incremental delivery observer: operator\n", b""))
        persistence.initialize(self.root, THREAD)

    def request(self, *args, **kw):
        return self.fx.request(*args, conversation_id=THREAD, **kw)

    def receipt(self, request, completed_at=None):
        tid = str(uuid.uuid5(uuid.NAMESPACE_DNS, request["transaction_id"]))
        def event(typ, **values):
            return {"type": "event_msg", "payload": {"type": typ, "turn_id": tid, **values}}
        def item(typ, identity, **values):
            return event("item_completed", thread_id=THREAD,
                         item={"type": typ, "id": identity, **values})
        rows = [{"type": "session_meta", "payload": {"id": THREAD}},
                event("task_started"),
                item("UserMessage", "user-" + tid,
                     content=[{"type": "text", "text": request["user_text"]}]),
                item("Reasoning", "secret", summary_text=["PRIVATE_REASONING_SENTINEL"]),
                item("AgentMessage", "message-" + tid, phase="final_answer",
                     content=[{"type": "Text", "text": request["response"]}]),
                event("task_complete")]
        if completed_at:
            rows[-1]["timestamp"] = completed_at
        source = self.root / (request["transaction_id"] + ".jsonl")
        source.write_bytes(b"".join((json.dumps(row) + "\n").encode() for row in rows))
        return codex_exchange.capture(THREAD, request["response"], request["transaction_id"],
                                      sources=[source], turn_id=tid)

    def commit(self, request=None):
        request = request or self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(request)
        persistence.confirm(self.root, receipt)
        return request, receipt

    def fail_head_write(self):
        original = persistence._atomic_write
        def fail(path, data):
            if Path(path) == self.root / persistence.HEAD:
                raise OSError("Synthetic crash before publishing HEAD")
            return original(path, data)
        return mock.patch.object(persistence, "_atomic_write", side_effect=fail)

    def test_prepare_crash_cannot_look_ready_and_forget_durable_proposal(self):
        request = self.request(actual_results=[{"source": "synthetic", "roll": 9}])
        with self.fail_head_write():
            with self.assertRaises(OSError):
                persistence.prepare(self.root, request)
        try:
            state = persistence.status(self.root)
        except persistence.PersistenceError:
            pass  # A declared recovery barrier is safe.
        else:
            self.assertNotEqual(state["status"], "ready", "unlinked prepared work must be surfaced")

    def test_resume_without_pending_preserves_current_state(self):
        before = self.fx.inventory()
        result = persistence.resume(self.root)
        self.assertIsNone(result["confirmation"])
        self.assertEqual(result["journal"]["committed_seq"], 0)
        self.assertEqual(self.fx.inventory(), before)

    def test_resume_confirms_actual_completed_reply_once(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(request)
        result = persistence.resume(self.root, receipt["source_ref"]["path"])
        self.assertEqual(result["confirmation"]["status"], "committed")
        self.assertEqual(result["journal"]["committed_seq"], 1)
        self.assertIn("Cash: 88", persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"])
        again = persistence.resume(self.root)
        self.assertIsNone(again["confirmation"])
        self.assertEqual(again["journal"]["committed_seq"], 1)

    def test_resume_cannot_commit_unfinished_reply(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(request)
        source = Path(receipt["source_ref"]["path"])
        source.write_bytes(b"\n".join(source.read_bytes().splitlines()[:-1]) + b"\n")
        with self.assertRaises(persistence.PersistenceError):
            persistence.resume(self.root, source)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        self.assertIsNotNone(persistence.status(self.root)["pending"])

    def test_transport_newline_does_not_block_input_and_original_is_archived(self):
        request = self.request(user_text="I leave.")
        persistence.prepare(self.root, request)
        actual = dict(request, user_text="I leave.\n")
        receipt = self.receipt(actual)
        persistence.confirm(self.root, receipt)
        persistence.close(self.root, self.fx.close_plan())
        archive = (self.root / "ARCHIVE/sessions/fixture-s0003/01_record.md").read_text(encoding="utf-8")
        self.assertIn("```text\nI leave.\n\n```", archive)
        retained = json.loads((self.root / "INSTANCE/JOURNAL/receipts/tx-1.json").read_bytes())
        self.assertEqual(retained["user_messages"][0]["text"], "I leave.\n")

    def test_transport_normalization_keeps_spaces_and_substantive_input_strict(self):
        request = self.request(user_text="I leave.")
        persistence.prepare(self.root, request)
        for text in ("I stay.\n", "I leave. \n", "I\nleave.\n", " I leave.\n"):
            with self.subTest(text=text):
                receipt = self.receipt(dict(request, user_text=text))
                with self.assertRaises(persistence.PersistenceError):
                    persistence.confirm(self.root, receipt)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)

    def test_assistant_trailing_newline_mismatch_remains_pending(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(dict(request, response=request["response"] + "\n"))
        with self.assertRaises(persistence.PersistenceError):
            persistence.confirm(self.root, receipt)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)

    def test_resumed_rollout_must_be_newer_than_adopted_save(self):
        floor = self.receipt(self.request("floor"), "2026-09-12T23:12:45.612Z")
        head_path = self.root / persistence.HEAD
        head = json.loads(head_path.read_bytes())
        head["source_floor"] = floor
        head_path.write_bytes(persistence._json(head))
        request = self.request()
        persistence.prepare(self.root, request)
        stale = self.receipt(request, "2026-09-12T23:00:00.000Z")
        with self.assertRaises(persistence.PersistenceError):
            persistence.confirm(self.root, stale)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        current = self.receipt(request, "2026-09-13T01:00:00.000Z")
        persistence.confirm(self.root, current)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)

    def test_same_request_recovers_prepare_head_write_crash(self):
        request = self.request()
        with self.fail_head_write():
            with self.assertRaises(OSError):
                persistence.prepare(self.root, request)
        persistence.recover_prepare(self.root)
        persistence.prepare(self.root, request)
        self.assertEqual(persistence.pending(self.root)["transaction_id"], request["transaction_id"])
        persistence.confirm(self.root, self.receipt(request))
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)

    def test_rebind_cannot_change_head_during_preparation_recovery(self):
        request = self.request()
        with self.fail_head_write():
            with self.assertRaises(OSError):
                persistence.prepare(self.root, request)
        before = (self.root / persistence.HEAD).read_bytes()
        with self.assertRaises(persistence.PersistenceError):
            persistence.rebind(self.root, "another-thread", "fixture-s0001")
        self.assertEqual((self.root / persistence.HEAD).read_bytes(), before)
        persistence.recover_prepare(self.root)
        self.assertEqual(persistence.pending(self.root)["transaction_id"], request["transaction_id"])

    def test_current_read_obeys_publication_lock(self):
        with persistence._lock(self.root):
            with self.assertRaises(persistence.PersistenceError):
                persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")

    @unittest.skipUnless(os.name == "nt", "Case alias regression requires case-insensitive Windows filesystem")
    def test_case_alias_cannot_return_stale_pre_checkpoint_owner(self):
        self.commit()
        try:
            view = persistence.read_current(self.root, "INSTANCE/CHAR/pc.md")
        except persistence.PersistenceError:
            pass  # Rejecting a noncanonical alias is safe.
        else:
            self.assertIn("Cash: 88", view["content"])

    @unittest.skipUnless(os.name == "nt", "Case alias regression requires case-insensitive Windows filesystem")
    def test_case_alias_cannot_commit_against_stale_physical_preimage(self):
        self.commit()
        path = "INSTANCE/CHAR/pc.md"
        physical = (self.root / path).read_bytes()
        request = self.request("tx-2", changes=[{
            "path": path, "expected_sha256": support.digest(physical),
            "edits": [{"before": "Cash: 100", "after": "Cash: 77"}]}])
        with self.assertRaises(persistence.PersistenceError):
            persistence.prepare(self.root, request)

    def test_confirm_head_write_crash_can_retry_once(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(request)
        with self.fail_head_write():
            with self.assertRaises(OSError):
                persistence.confirm(self.root, receipt)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)
        persistence.confirm(self.root, receipt)
        persistence.confirm(self.root, receipt)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)

    def test_committed_receipt_evidence_is_hash_bound(self):
        request, receipt = self.commit()
        path = self.root / "INSTANCE/JOURNAL/receipts/tx-1.json"
        stored = json.loads(path.read_bytes())
        stored["user_messages"][0]["text"] = "Altered original user evidence"
        path.write_bytes(persistence._json(stored))
        with self.assertRaises(persistence.PersistenceError):
            persistence.status(self.root)

    def test_close_duplicate_owner_updates_never_silently_drop_first_update(self):
        self.commit()
        view = persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")
        updates = [
            {"path": view["path"], "expected_sha256": view["sha256"],
             "edits": [{"before": "Cash: 88", "after": "Cash: 86"}]},
            {"path": view["path"], "expected_sha256": view["sha256"],
             "edits": [{"before": "Unchanged qualifier: exact.", "after": "Unchanged qualifier: updated."}]},
        ]
        plan = self.fx.close_plan(current_updates=updates)
        try:
            persistence.close(self.root, plan)
        except persistence.PersistenceError:
            return  # Rejecting duplicate paths is safe.
        current = persistence.read_current(self.root, "INSTANCE/CHAR/PC.md")["content"]
        self.assertIn("Cash: 86", current)
        self.assertIn("Unchanged qualifier: updated.", current)

    def test_actual_source_mismatch_cannot_confirm(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.receipt(request)
        receipt["assistant_text"] += " invented"
        with self.assertRaises(persistence.PersistenceError):
            persistence.confirm(self.root, receipt)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 0)

    def test_same_observed_message_cannot_confirm_two_transaction_ids(self):
        request, receipt = self.commit()
        other = self.request("tx-2", "Cash: 88", "Cash: 76")
        persistence.prepare(self.root, other)
        replay = copy.deepcopy(receipt)
        replay["transaction_id"] = "tx-2"
        with self.assertRaises(persistence.PersistenceError):
            persistence.confirm(self.root, replay)
        self.assertEqual(persistence.status(self.root)["committed_seq"], 1)

    def test_unaccepted_operator_observer_cannot_bypass_foreground_verification(self):
        request = self.request()
        persistence.prepare(self.root, request)
        receipt = self.fx.receipt(request)
        with self.assertRaises(persistence.PersistenceError):
            persistence.confirm(self.root, receipt)

    def test_corrupt_recovery_preimage_mapping_is_rejected_before_writes(self):
        self.commit()
        self.fx.interrupted_checkpoint()
        manifest = self.root / "RECOVERY/journal-fixture-s0002/operation.json"
        record = json.loads(manifest.read_bytes())
        owner = next(row for row in record["write_set"] if row["path"] == "INSTANCE/CHAR/PC.md")
        self.assertIsNotNone(owner["before_sha256"])
        owner["before"] = None
        manifest.write_bytes(persistence._json(record))
        before = self.fx.inventory()
        with self.assertRaises(persistence.PersistenceError):
            persistence.recover(self.root, "restore")
        self.assertEqual(self.fx.inventory(), before, "corrupt mapping must not delete or replace current owners")

    def test_missing_head_cannot_initialize_over_retained_committed_progress(self):
        self.commit()
        head = self.root / persistence.HEAD
        head.unlink()
        before = self.fx.inventory()
        with self.assertRaises(persistence.PersistenceError):
            persistence.initialize(self.root, THREAD)
        self.assertEqual(self.fx.inventory(), before)


if __name__ == "__main__":
    unittest.main()
