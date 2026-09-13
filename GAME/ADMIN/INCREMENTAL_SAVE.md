# ADMIN — Working-log saving and retained legacy journal

## Selected write-only play log

The accepted clause **Incremental recording: write-only-log** selects [PLAY_PERSISTENCE](PLAY_PERSISTENCE.md): one short append per exchange. Notes are working material, not a transcript or proof of delivery. Installation selects no policy. Ongoing PLAY performs no persistence reads, source matching, confirmation or record edits.

At fresh boot or actual CHECKPOINT/SAVE, run `python -X utf8 -B TOOLS/play_log.py --root . read` once. At ADMIN compilation reconcile uncompiled notes against prior state and available conversation, including interrupted/revised replies. Preserve established changes, qualifications, operative private facts and actual results; do not infer acceptance solely from a note.

Compile only changed canonical owners in one bounded pass. Reuse unrelated content, add useful routes and apply each effect once. Ordinary disengagement preserves its actual transition and consequences without a dossier rewrite. Follow the accepted checkpoint cadence and deferral; an append resets no count.

## Checkpoint

Use `python -X utf8 -B TOOLS/persistence.py --root . checkpoint --save-id <new-id> --plan <plan.json>` with actual ADMIN-observed values:

```json
{
  "expected_base_save_id": "<current compiled save id>",
  "log_snapshot": {"after": 0, "through": 123, "prefix_sha256": "<actual prefix hash>"},
  "log_compilation": "reviewed",
  "current_updates": [
    {"path": "INSTANCE/NOW.md", "expected_sha256": "<actual current file hash>",
     "edits": [{"before": "<unique existing span>", "after": "<established replacement>"}]}
  ]
}
```

Copy the whole returned snapshot; `after` is its compiled starting offset. Existing records use their actual hash and unique targeted edits, grouped once per path. A genuinely new established record uses `expected_sha256: null` and complete `content`. Omit unchanged files. Save identity and cursor metadata remain helper-owned. The helper protects publication and incorporation together; do not run CLOSE_CONTRACT’s manual write sequence afterward. Lightweight compilation is not a formal semantic audit.

## Full save and bounded review

The full plan adds `save_id`, `title`, `route_terms`, `span`, `place`, `session_id` and `review: {status, scope, limitations}`. Status is `complete`, `incomplete` or `not-selected`, according to the selected policy and actual work. Retain the same snapshot/current updates. Actual feedback may use `operational_evidence` with `session_id`, exact `text` and real `source_ref`.

For selected source review, run `close --plan <plan.json> --preview <new-isolated-directory>`. This stages the exact proposed affected files without publishing. Import its returned `source` body for ADMIN/EVIDENCE_AUDIT’s existing save-bound workflow. Select affected owners on the current side and their existing prior versions; select relevant unchanged authorities with `--prior-select`. The preview is partial: absence is not deletion; only declared `removed_paths` are removals.

Perform the source-first comparison once, looking for omitted developments as well as unsupported edits. Retain the actual reviewer arrangement, scope and gaps. A completed consistent review supplies `review.receipt` with `bundle`, `report`, actual `report_sha256` and optional `delivery_receipt`. Before final close, retain byte-identical review material at portable campaign-local EVIDENCE paths and use matching relative references. Then run `close --plan <plan.json>`: it verifies the existing receipt against the proposed source/owners and publishes those bytes. It does not perform another semantic audit. Concrete corrections require a refreshed preview/report only for invalidated coverage; missing evidence or unavailable review remains explicitly incomplete.

The compatible Codex helper obtains remaining original public source at SAVE. Its archive body labels actual conversation, including OOC, rather than asserting every statement is accepted fiction. For a superseded public message, `source_dispositions` maps its actual message id to `status` (`superseded` or `partly-superseded`), `reason` and `correction_ref` to the actual CORRECTIONS entry; retain original text. Other hosts use actual supported source access or disclose `source_gap`, never reconstruct originals from notes. END SESSION also preserves actual feedback and due mechanics through SESSION.

Keep original logs/source and recovery material in backups. Report append failures without a turn-level retry loop. Compatible program maintenance may preserve pending bytes; a protocol migration must reconcile outstanding state/source first.

At a new PLAY task, initialize only a never-initialized bound campaign through LOAD. For an existing binding, use ADMIN `rebind --conversation-id <actual-new-task-UUID> --expected-base <current-save-id>` after old progress/source is saved. It establishes the new conversation-start boundary; no per-turn rebinding occurs. An unplayed fresh bind needs no invented SAVE. If a restored campaign’s old host source is unavailable, rebind requires a verified local full-save boundary and no pending notes; retain its returned `source_limit` about unavailable later messages.

## Retained legacy procedure

[LEGACY_INCREMENTAL_SAVE](LEGACY_INCREMENTAL_SAVE.md) is only for an actual unmigrated journal or identified legacy ADMIN recovery. Preserve its source/results and disposition during migration; never restart its old turn protocol merely because its files remain.
