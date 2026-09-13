#!/usr/bin/env python3
"""Read selected local Codex rollout files and attest a completed public reply.

Experimental adapter tested against local Codex Desktop 0.153.4 records. This is
not a supported post-final callback, proof of UI display, or a branch resolver.
Use at the next foreground tool boundary. Unknown/ambiguous delivery remains
pending. The adapter never writes a rollout and never exports reasoning records.

The SHA-256 in a source reference covers the exact inclusive selected line span,
including original line endings. It is NOT the hash of the entire mutable log.
Tool evidence is opt-in by exact completed tool item ID; do not select tools that
read private reasoning or unrelated records. No tool arguments are exported.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid


class DeliveryError(ValueError):
    """Delivery could not be established; preserve the prepared transaction."""


def _uuid(value, label):
    try:
        if str(uuid.UUID(value)) != value.lower():
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise DeliveryError(label + " must be a UUID") from None
    return value.lower()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _text(content, accepted):
    if not isinstance(content, list):
        raise DeliveryError("Unsupported public message content shape")
    chunks, other = [], []
    for part in content:
        if not isinstance(part, dict):
            raise DeliveryError("Unsupported public message part")
        typ = part.get("type")
        if typ in accepted and isinstance(part.get("text"), str):
            chunks.append(part["text"])
        else:
            other.append(str(typ))
    return "".join(chunks), other


def discover(thread_id, codex_home=None):
    """List only conventional rollout filenames naming this exact thread UUID."""
    thread_id = _uuid(thread_id, "thread_id")
    home = Path(codex_home or os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    sessions = home / "sessions"
    found = sorted(sessions.glob("*/*/*/rollout-*" + thread_id + "*.jsonl"))
    if not found:
        raise DeliveryError("No selected-thread rollout found; supply --source explicitly")
    return found


def _snapshot(path, thread_id):
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise DeliveryError("Rollout source is not a regular file")
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    rows = []
    for number, line in enumerate(lines, 1):
        try:
            row = json.loads(line)
        except (ValueError, UnicodeDecodeError):
            raise DeliveryError("Incomplete or malformed source JSON at line " + str(number)) from None
        if not isinstance(row, dict) or not isinstance(row.get("payload"), dict):
            raise DeliveryError("Unsupported rollout record at line " + str(number))
        rows.append(row)
    metadata = [r["payload"] for r in rows if r.get("type") == "session_meta"]
    if len(metadata) != 1 or metadata[0].get("id") != thread_id:
        raise DeliveryError("Source does not identify exactly the selected conversation")
    if any(metadata[0].get(k) for k in ("forked_from_id", "forked_from", "parent_thread_id")):
        raise DeliveryError("Forked source requires explicit branch reconciliation")
    if path.read_bytes() != data:
        raise DeliveryError("Source changed while read; retry at a stable boundary")
    return path, lines, rows


def _ref(path, lines, start, end, **extra):
    return {"path": str(path), "sha256": _sha(b"".join(lines[start - 1:end])),
            "sha256_scope": "selected_span", "start_line": start, "end_line": end, **extra}


def _scan(path, lines, rows, thread_id):
    turns = {}
    active = None
    for number, row in enumerate(rows, 1):
        data = row["payload"]
        typ = data.get("type", "")
        if row.get("type") == "event_msg" and not isinstance(typ, str):
            raise DeliveryError("Unsupported event type")
        if row.get("type") == "event_msg" and any(
                token in typ.lower() for token in ("rollback", "rolled_back", "message_edited", "message_deleted", "branch", "fork")):
            raise DeliveryError("Source contains edit/branch/rollback history; reconcile explicitly")
        if row.get("type") != "event_msg":
            continue
        if typ == "task_started":
            tid = data.get("turn_id")
            if not isinstance(tid, str) or tid in turns:
                raise DeliveryError("Missing or repeated turn identity")
            if active is not None:
                turns[active]["ambiguous"] = True
            turns[tid] = {"start": number, "complete": [], "aborted": False,
                          "finals": [], "users": [], "tools": {}, "ambiguous": False}
            active = tid
        elif typ in ("task_complete", "turn_aborted", "task_failed"):
            tid = data.get("turn_id")
            if tid not in turns:
                raise DeliveryError("Terminal event lacks a selected start boundary")
            turn = turns[tid]
            if typ == "task_complete":
                turn["complete"].append(number)
                if data.get("status") not in (None, "completed", "complete", "success"):
                    turn["ambiguous"] = True
                if data.get("error"):
                    turn["ambiguous"] = True
            else:
                turn["aborted"] = True
            if active == tid:
                active = None
        elif typ == "item_completed":
            tid = data.get("turn_id")
            if data.get("thread_id") != thread_id or tid not in turns:
                raise DeliveryError("Completed item has a mismatched thread/turn boundary")
            item = data.get("item")
            if not isinstance(item, dict):
                raise DeliveryError("Malformed completed item")
            turn = turns[tid]
            if active != tid:
                turn["ambiguous"] = True
            kind = item.get("type")
            if kind == "AgentMessage" and item.get("phase") == "final_answer":
                text, other = _text(item.get("content"), {"Text"})
                if other or not isinstance(item.get("id"), str):
                    turn["ambiguous"] = True
                turn["finals"].append((number, item.get("id"), text))
            elif kind == "UserMessage":
                text, other = _text(item.get("content"), {"text", "input_text"})
                turn["users"].append({"text": text, "non_text_types": other,
                    "source_ref": _ref(path, lines, number, number,
                                       message_id=item.get("id"), turn_id=tid)})
            elif kind in ("CommandExecution", "McpToolCall"):
                identity = item.get("id")
                if identity in turn["tools"]:
                    turn["ambiguous"] = True
                turn["tools"][identity] = (number, item)
    return turns


def observe(thread_id, sources):
    """One stable read and parse per selected file for a bounded SAVE operation."""
    observed = []
    seen = set()
    for source in sources:
        key = Path(source).resolve(strict=True)
        if key not in seen:
            path, lines, rows = _snapshot(key, thread_id)
            observed.append((path, lines, rows, _scan(path, lines, rows, thread_id)))
            seen.add(key)
    return observed


def capture(thread_id, expected_response, transaction_id, sources=None,
            codex_home=None, turn_id=None, tool_item_ids=(), _observed=None):
    """Return a deterministic receipt for one unambiguously completed reply."""
    thread_id = _uuid(thread_id, "thread_id")
    if not isinstance(transaction_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,199}", transaction_id):
        raise DeliveryError("Unsafe transaction identity")
    if not isinstance(expected_response, str) or not expected_response:
        raise DeliveryError("Expected response must be nonempty exact UTF-8 text")
    if turn_id is not None:
        turn_id = _uuid(turn_id, "turn_id")
    sources = list(sources) if sources is not None else discover(thread_id, codex_home)
    if not sources:
        raise DeliveryError("No selected source")
    candidates = []
    selected_paths = {Path(source).resolve(strict=True) for source in sources}
    for path, lines, rows, turns in (_observed if _observed is not None else observe(thread_id, sources)):
        if path not in selected_paths:
            continue
        selected_turns = [(turn_id, turns[turn_id])] if turn_id in turns else ([] if turn_id else turns.items())
        for tid, turn in selected_turns:
            if turn_id is not None and turn_id != tid:
                continue
            if any(f[2] == expected_response for f in turn["finals"]):
                candidates.append((path, lines, tid, turn))
    if len(candidates) != 1:
        raise DeliveryError("Expected response has no unique selected turn; use exact source and --turn-id")
    path, lines, tid, turn = candidates[0]
    if turn["aborted"] or turn["ambiguous"] or len(turn["complete"]) != 1 or len(turn["finals"]) != 1:
        raise DeliveryError("Selected reply is interrupted, incomplete, or ambiguous; keep it pending")
    final_line, message_id, actual = turn["finals"][0]
    end = turn["complete"][0]
    if not turn["start"] < final_line < end:
        raise DeliveryError("Final reply does not precede its explicit completion boundary")
    outputs = []
    for identity in dict.fromkeys(tool_item_ids):
        if identity not in turn["tools"]:
            raise DeliveryError("Selected tool result is absent from the completed turn")
        number, item = turn["tools"][identity]
        if not turn["start"] < number < end or item.get("status") != "completed":
            raise DeliveryError("Selected tool result is not completed within this turn")
        if item["type"] == "CommandExecution":
            if item.get("exit_code") != 0:
                raise DeliveryError("Selected command did not complete successfully")
            result = {"stdout": item.get("stdout", ""), "stderr": item.get("stderr", "")}
            if not all(isinstance(v, str) for v in result.values()):
                raise DeliveryError("Unsupported command output format")
        else:
            raw = item.get("result")
            if not isinstance(raw, dict) or raw.get("isError"):
                raise DeliveryError("Selected MCP tool did not return successful output")
            value, other = _text(raw.get("content"), {"text"})
            if other:
                raise DeliveryError("Selected MCP result has unsupported non-text evidence")
            result = {"text": value}
        outputs.append({"item_id": identity, "kind": item["type"], "result": result,
            "source_ref": _ref(path, lines, number, number, turn_id=tid, message_id=identity)})
    return {"schema": "rpg-delivery-v1", "conversation_id": thread_id,
            "transaction_id": transaction_id, "assistant_text": actual,
            "source_ref": _ref(path, lines, final_line, end, message_id=message_id, turn_id=tid,
                               completed_at=json.loads(lines[end - 1]).get('timestamp')),
            "complete": True, "observer": "codex-rollout",
            "user_messages": turn["users"], "tool_outputs": outputs}


def verify_receipt(receipt):
    """Re-read the selected source instead of trusting a hand-written receipt."""
    try:
        ref = receipt["source_ref"]
        actual = capture(receipt["conversation_id"], receipt["assistant_text"],
            receipt["transaction_id"], sources=[ref["path"]], turn_id=ref["turn_id"],
            tool_item_ids=[x["item_id"] for x in receipt.get("tool_outputs", [])])
    except (KeyError, TypeError):
        raise DeliveryError("Malformed delivery receipt") from None
    if actual != receipt:
        raise DeliveryError("Receipt differs from its selected original source")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--expected-response", required=True, type=Path)
    parser.add_argument("--transaction-id", required=True)
    parser.add_argument("--source", action="append", type=Path)
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument("--turn-id")
    parser.add_argument("--tool-item-id", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        expected = args.expected_response.read_bytes().decode("utf-8")
        receipt = capture(args.thread_id, expected, args.transaction_id, sources=args.source,
                          codex_home=args.codex_home, turn_id=args.turn_id,
                          tool_item_ids=args.tool_item_id)
        encoded = (json.dumps(receipt, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode("utf-8")
        if args.output:
            if args.output.exists():
                if args.output.read_bytes() != encoded:
                    raise DeliveryError("Output already exists with different contents")
            else:
                with args.output.open("xb") as stream:
                    stream.write(encoded)
                    stream.flush()
                    os.fsync(stream.fileno())
        else:
            sys.stdout.write(encoded.decode("ascii"))
        return 0
    except (DeliveryError, OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"status": "pending", "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
