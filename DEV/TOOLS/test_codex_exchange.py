"""Bounded synthetic delivery fixtures; no access to real conversation logs."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import codex_exchange as adapter

THREAD = "11111111-1111-4111-8111-111111111111"
TURN = "22222222-2222-4222-8222-222222222222"
NEXT = "33333333-3333-4333-8333-333333333333"
TEXT = "The purchase completes. Cash: €288.\n"


def event(kind, **kw):
    return {"type": "event_msg", "payload": {"type": kind, **kw}}


def item(kind, identity, turn=TURN, **kw):
    return event("item_completed", thread_id=THREAD, turn_id=turn,
                 item={"type": kind, "id": identity, **kw})


def exchange(turn=TURN, text=TEXT):
    return [event("task_started", turn_id=turn),
            item("UserMessage", "user1", turn, content=[{"type": "text", "text": "I buy lunch."}]),
            item("Reasoning", "secret", turn, summary_text=["PRIVATE_REASONING_SENTINEL"]),
            item("CommandExecution", "roll1", turn, status="completed", exit_code=0,
                 stdout="3d6: [2,3,4] = 9\n", stderr="", command=["SECRET_ARGS"]),
            item("AgentMessage", "assistant1", turn, phase="final_answer", content=[{"type": "Text", "text": text}]),
            event("task_complete", turn_id=turn)]


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.jsonl"
        self.rows = [{"type": "session_meta", "payload": {"id": THREAD, "cli_version": "0.153.4"}}, *exchange()]
        self.write()

    def write(self, suffix=b""):
        self.source.write_bytes(b"".join((json.dumps(r) + "\r\n").encode() for r in self.rows) + suffix)

    def capture(self, **kw):
        return adapter.capture(THREAD, TEXT, "tx-1", sources=[self.source], **kw)

    def test_completed_exact_text_and_minimal_public_evidence(self):
        receipt = self.capture(tool_item_ids=["roll1"])
        self.assertEqual(receipt["assistant_text"], TEXT)
        self.assertTrue(receipt["complete"])
        self.assertEqual(receipt["user_messages"][0]["text"], "I buy lunch.")
        self.assertEqual(receipt["tool_outputs"][0]["result"]["stdout"], "3d6: [2,3,4] = 9\n")
        self.assertNotIn("PRIVATE_REASONING_SENTINEL", json.dumps(receipt))
        self.assertNotIn("SECRET_ARGS", json.dumps(receipt))
        self.assertTrue(adapter.verify_receipt(receipt))

    def test_tools_are_explicit_opt_in(self):
        self.assertEqual(self.capture()["tool_outputs"], [])
        with self.assertRaises(adapter.DeliveryError):
            self.capture(tool_item_ids=["absent"])

    def test_abort_is_not_completion(self):
        self.rows[-1] = event("turn_aborted", turn_id=TURN, reason="interrupted")
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_abort_even_after_completion_rejected(self):
        self.rows.append(event("turn_aborted", turn_id=TURN))
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_final_record_alone_remains_pending(self):
        self.rows.pop()
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_partial_stream_rejected(self):
        self.write(b'{"type":')
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_exact_whitespace_required(self):
        with self.assertRaises(adapter.DeliveryError):
            adapter.capture(THREAD, TEXT.rstrip(), "tx-1", sources=[self.source])

    def test_multiple_matching_turns_need_explicit_identity(self):
        self.rows.extend(exchange(NEXT))
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()
        self.assertEqual(self.capture(turn_id=TURN)["source_ref"]["turn_id"], TURN)

    def test_multiple_finals_same_turn_rejected(self):
        self.rows.insert(-1, item("AgentMessage", "assistant2", phase="final_answer", content=[{"type": "Text", "text": "different"}]))
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_completion_with_wrong_turn_rejected(self):
        self.rows[-1]["payload"]["turn_id"] = NEXT
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_item_after_turn_boundary_rejected(self):
        self.rows.append(item("UserMessage", "late", content=[{"type": "text", "text": "late"}]))
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_failed_tool_not_presented_as_roll_evidence(self):
        self.rows[4]["payload"]["item"]["exit_code"] = 1
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture(tool_item_ids=["roll1"])

    def test_successful_selected_mcp_output(self):
        self.rows[4] = item("McpToolCall", "roll1", status="completed", result={
            "content": [{"type": "text", "text": "Rolled 9"}], "isError": False},
            arguments={"private": "SECRET_ARGS"})
        self.write()
        receipt = self.capture(tool_item_ids=["roll1"])
        self.assertEqual(receipt["tool_outputs"][0]["result"], {"text": "Rolled 9"})
        self.assertNotIn("SECRET_ARGS", json.dumps(receipt))

    def test_source_thread_mismatch_rejected(self):
        self.rows[0]["payload"]["id"] = NEXT
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_fork_and_edit_rejected(self):
        self.rows[0]["payload"]["forked_from_id"] = NEXT
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()
        self.rows[0]["payload"].pop("forked_from_id")
        self.rows.append(event("thread_rolled_back", num_turns=1))
        self.write()
        with self.assertRaises(adapter.DeliveryError):
            self.capture()

    def test_retry_stable_when_later_turns_append(self):
        before = self.capture()
        self.rows.extend(exchange(NEXT, "Later reply."))
        self.write()
        self.assertEqual(self.capture(), before)
        self.assertTrue(adapter.verify_receipt(before))

    def test_receipt_tampering_rejected(self):
        receipt = self.capture()
        receipt["user_messages"][0]["text"] = "Invented consent"
        with self.assertRaises(adapter.DeliveryError):
            adapter.verify_receipt(receipt)

    def test_targeted_discovery_only(self):
        folder = self.root / "sessions/2026/09/13"
        folder.mkdir(parents=True)
        selected = folder / ("rollout-now-" + THREAD + "_suffix.jsonl")
        selected.write_bytes(self.source.read_bytes())
        (folder / ("rollout-now-" + NEXT + "_suffix.jsonl")).write_bytes(b"PRIVATE_UNRELATED")
        receipt = adapter.capture(THREAD, TEXT, "tx-1", codex_home=self.root)
        self.assertEqual(Path(receipt["source_ref"]["path"]), selected)

    def test_cli_exact_utf8_and_idempotent_output(self):
        expected, output = self.root / "expected.txt", self.root / "receipt.json"
        expected.write_bytes(TEXT.encode("utf-8"))
        argv = ["--thread-id", THREAD, "--transaction-id", "tx-1", "--source", str(self.source),
                "--expected-response", str(expected), "--output", str(output)]
        self.assertEqual(adapter.main(argv), 0)
        self.assertEqual(adapter.main(argv), 0)
        original = output.read_bytes()
        self.assertEqual(json.loads(original)["assistant_text"], TEXT)
        output.write_bytes(b"existing")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(adapter.main(argv), 2)
        self.assertEqual(output.read_bytes(), b"existing")


if __name__ == "__main__":
    unittest.main()
