#!/usr/bin/env python3
"""Read-only reference scheduler for RPG OS's opt-in autosave protocol.

One JSON observation on stdin; one decision on stdout. No campaign reads,
file writes, model calls, timers, randomness, or save execution. A host may
use this helper, or the GM may follow ADMIN/AUTOSAVE.md directly.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields
import json
import math
import sys
from typing import Any

sys.dont_write_bytecode = True


@dataclass(frozen=True)
class Observation:
    # This must come from the accepted agreement, never from a suggested policy.
    enabled: bool = False
    dirty: bool = False
    # Monotonic completed PLAY replies in this conversation; OOC/tool calls do not count.
    turn: int = 0
    turns_since_save: int = 0
    interval: int = 15
    # The turn at whose end the warning was actually delivered; None means no notice.
    warned_at: int | None = None
    deferred: bool = False
    consequential: bool = False
    scene_boundary: bool = False
    # Only actual model-visible telemetry or an explicit operator report is eligible.
    context_percent: float | None = None
    context_source: str = "unavailable"
    context_threshold: float = 65.0
    # Caller latches after verified persistence during a high-context episode;
    # rearm only after an observed drop below threshold or a clean fresh boot.
    context_handled: bool = False
    # Safe means administratively quiescent, not fictionally free of danger.
    safe_boundary: bool = True
    recovery_active: bool = False
    handover_active: bool = False
    write_in_progress: bool = False
    persistence_available: bool = True
    # A manual operation overrides warning/deferral but never recovery/handover.
    manual: str | None = None


@dataclass(frozen=True)
class Decision:
    action: str
    warned_at: int | None
    reason: str


def validate(o: Observation) -> None:
    for field in ("enabled", "dirty", "deferred", "consequential", "scene_boundary",
                  "context_handled", "safe_boundary", "recovery_active", "handover_active",
                  "write_in_progress", "persistence_available"):
        if type(getattr(o, field)) is not bool:
            raise ValueError(f"{field} must be a JSON boolean")
    for field in ("turn", "turns_since_save", "interval"):
        value = getattr(o, field)
        if type(value) is not int or value < (1 if field == "interval" else 0):
            raise ValueError(f"{field} must be a valid nonnegative integer (interval >= 1)")
    if o.warned_at is not None and (type(o.warned_at) is not int or not 0 <= o.warned_at <= o.turn):
        raise ValueError("warned_at must be null or a completed turn no later than turn")
    for field in ("context_percent", "context_threshold"):
        value = getattr(o, field)
        if value is None and field == "context_percent":
            continue
        # Range-check before float conversion so arbitrarily large JSON integers
        # produce a normal validation error instead of overflowing math.isfinite.
        if type(value) not in (int, float) or not 0 <= value <= 100 or not math.isfinite(value):
            raise ValueError(f"{field} must be a finite number in [0, 100]")
    if o.context_threshold == 0:
        raise ValueError("context_threshold must be greater than zero")
    if o.context_source not in ("unavailable", "host", "operator"):
        raise ValueError("context_source must be unavailable, host, or operator; estimates are not telemetry")
    if (o.context_percent is None) != (o.context_source == "unavailable"):
        raise ValueError("context value and its source must agree")
    if o.manual not in (None, "checkpoint", "close"):
        raise ValueError("manual must be null, checkpoint, or close")


def decide(o: Observation) -> Decision:
    """Evaluate once after a reply, preserving a warning until verified persistence.

    A checkpoint/close decision requests ADMIN; it is not a success receipt.
    Reset dirty/count/notice only after actual write/readback verification.
    At verification, latch context_handled if the latest supported reading is high;
    a checkpoint does not empty context. Reasons are diagnostic codes, not spoilers.
    """
    validate(o)
    pending = o.warned_at
    for active, reason in ((o.recovery_active, "recovery"),
                           (o.handover_active, "handover"),
                           (o.write_in_progress, "write-in-progress")):
        if active:
            return Decision("blocked", pending, reason)
    if o.manual is not None:
        if not o.persistence_available:
            return Decision("unavailable", pending, "export-or-recover")
        if not o.safe_boundary:
            return Decision("wait", pending, "finish-current-operation")
        return Decision(o.manual, pending, "explicit-request")
    if not o.enabled:
        return Decision("none", None, "disabled")
    if not o.dirty:
        return Decision("none", None, "no-unsaved-state")
    if o.deferred:
        return Decision("deferred", pending, "operator-deferral")
    if not o.persistence_available:
        return Decision("unavailable", pending, "export-or-recover")
    if not o.safe_boundary:
        return Decision("wait", pending, "finish-current-operation")
    if pending is not None:
        if o.turn <= pending:
            return Decision("wait", pending, "notice-turn-not-completed")
        return Decision("checkpoint", pending, "previously-announced")
    pressure = (not o.context_handled and o.context_percent is not None
                and o.context_percent >= o.context_threshold)
    due = o.consequential or o.scene_boundary or o.turns_since_save >= o.interval or pressure
    if due:
        return Decision("warn", o.turn, "autosave-due")
    return Decision("none", None, "not-due")


def from_mapping(data: Any) -> Observation:
    if not isinstance(data, dict):
        raise ValueError("input must be one JSON object")
    extra = set(data) - {field.name for field in fields(Observation)}
    if extra:
        raise ValueError("unknown input fields: " + ", ".join(sorted(extra)))
    observation = Observation(**data)
    validate(observation)
    return observation


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def main() -> int:
    try:
        data = json.load(sys.stdin, object_pairs_hook=unique_object)
        print(json.dumps(asdict(decide(from_mapping(data))), allow_nan=False))
        return 0
    except (ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
