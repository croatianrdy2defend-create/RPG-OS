# ADMIN — Legacy prepared/confirmed journal

Historical compatibility procedure retained for migration and recovery. Current write-only-log play and saving use [PLAY_PERSISTENCE](PLAY_PERSISTENCE.md) and [INCREMENTAL_SAVE](INCREMENTAL_SAVE.md). Do not run this former turn protocol merely because old journal files remain in the campaign.


The remaining sections describe the earlier prepared/confirmed journal for an explicitly selected legacy administrative operation or migration. They do not apply to ordinary PLAY in write-only-log mode and do not override the selected workflow above. Retain old history; do not silently discard or reinterpret it.

Optional local experiment on v0.9.7. Installation alone enables nothing. The accepted campaign agreement must select this procedure and its actual host completion mode; existing campaigns retain ordinary conversation-held state and protected saves otherwise. This is a durability mechanism, not additional fictional authority or a promise of lower cost before measurement.

This file preserves the old prepared/confirmed journal protocol for an identified legacy ADMIN task only. The current ordinary PLAY guide describes a different selected method; do not import these turn instructions into write-only-log play.

## Three boundaries

1. **Exchange recording:** prepare one small protected batch containing the exact proposed response, available original input, actual roll results and established changes. Confirm only against the actual completed delivered response. No inference, generated event, new NPC cause or reconstructed dialogue is introduced while storing it.
2. **CHECKPOINT:** consolidate committed batches into their existing current owners and verify publication. Preserve the accepted autosave cadence and earlier triggers; recording a batch does not reset that cadence. Checkpoint deferral postpones consolidation, not recording. A checkpoint preserves the current present without advancing the accepted archive boundary.
3. **SAVE / CLOSE:** consolidate pending accepted changes, archive remaining accepted evidence and perform the selected bounded review. **END SESSION SAVE** also uses [SESSION](SESSION.md) for actual feedback and genuinely due boundary mechanics. Saving alone never ends a scene or session.

The effective persisted present is **the consolidated baseline plus later committed batches**. Pending prepared responses are recoverable proposals, not automatically accepted history. Accepted delivered play still governs fiction; if it cannot be matched to a durable batch, preserve and reconcile that source rather than pretending either that it was saved or that it did not happen.

## Adoption and storage

Use a verified compatible runtime and complete backup. Reconcile any `RECOVERY/ACTIVE.md` or `HANDOVER/ACTIVE.md` first. Identify the actual campaign, accepted agreement, consolidated save and exact starting evidence coverage. Do not fabricate transactions for past play, reroll old encounters or alter the stopping point to initialize the feature.

Record the accepted opt-in prospectively within the existing agreement sections through [RECALIBRATE](RECALIBRATE.md), including the literal clause **Incremental persistence: enabled**, the host completion mode and existing checkpoint cadence. Already explicit acceptance of this concrete experiment need not be requested again. Initialize the optional `INSTANCE/JOURNAL/` store through `TOOLS/persistence.py`, bound to those verified identities. The store is required recovery material while enabled, not a disposable cache. Its presence must not silently enable a missing agreement grant; an enabled agreement with a missing or incompatible store requires repair before dependent PLAY.

`INSTANCE/JOURNAL/HEAD.json` owns the configuration, accepted-contract hash, committed head and digest-bound pending-delivery reference. Immutable batches live under `batches/`; finalized receipts under `receipts/`. The helper's versioned format binds predecessor batches and delivery receipts and verifies their contents. `PREPARE_INTENT.json` retains an interrupted preparation's exact batch and prior/target heads; use `recover-prepare` before another operation to finish that preparation, then confirm actual delivery separately. Neither that intent nor pending delivery is `RECOVERY/ACTIVE.md` or automatic fictional rollback. Do not hand-edit markers, hashes or receipts, copy an unrelated journal into a campaign, or reconstruct a missing head from whichever file is newest. Keep exactly one writer. A conflicting base requires inspection; deleting a lock is not reconciliation.

Run from the campaign root with its available Python interpreter; inspect the helper's actual input schema/help before writing a plan. The operation surface is:

```text
python TOOLS/persistence.py --root . init --conversation-id <actual-conversation-id>
python TOOLS/persistence.py --root . status
python TOOLS/persistence.py --root . resume
python TOOLS/persistence.py --root . resume --full --path <needed-owner> --path <another-needed-owner>
python TOOLS/persistence.py --root . resume
python TOOLS/persistence.py --root . pending
python TOOLS/persistence.py --root . read --path INSTANCE/CURRENT_SAVE.md
python TOOLS/persistence.py --root . prepare --input <batch-plan.json>
python TOOLS/persistence.py --root . recover-prepare
python TOOLS/persistence.py --root . confirm --receipt <actual-delivery-receipt.json>
python TOOLS/persistence.py --root . abandon --transaction-id <pending-id> --reason <actual-disposition>
python TOOLS/persistence.py --root . checkpoint --save-id <new-save-id>
python TOOLS/persistence.py --root . close --plan <full-save-plan.json>
python TOOLS/persistence.py --root . recover --action finish
python TOOLS/persistence.py --root . recover --action restore
python TOOLS/persistence.py --root . rebind --conversation-id <actual-conversation-id> --expected-base <prior-journal-base-save-id>
python TOOLS/persistence.py --root . disable
```

These are alternatives selected for the actual task, not a script to run indiscriminately. Retrying uses the original operation identity and retained exact target. A receipt identifies real completed source and its coverage; naming a file `receipt` does not prove delivery. If a required operation/schema is unsupported, stop that path and report the limitation instead of hand-editing the journal to imitate it.

For the normal Codex foreground trial, use `resume` at the next actual tool boundary. In one call it checks the prior pending response against completed selected-conversation source, confirms it if exact and unambiguous, and returns compact journal status, identities and effective owner hashes. Request CURRENT_SAVE's body with `--full` or identified full records with repeated `--path`. Optional `--source <exact-rollout.jsonl>` narrows discovery. It does not resolve an interrupted or mismatched reply by guessing, create a checkpoint or play a new action. Then perform the actual declaration and use `prepare` once before sending that exact planned response. Separate `pending`/adapter/`confirm` commands remain useful for diagnosed source ambiguity.

Identical repeated replies may require the adapter's explicit observed `--turn-id` before confirmation. `resume` does not select tool outputs: when exact roll/tool-output receipt evidence is needed, use the adapter with the actual `--tool-item-id` and confirm first. Obtained results must still be preserved in the prepared batch; a stored result and a verified original tool-output receipt are distinct evidence.

Adopt at the initial bind or a completed full SAVE, so an earlier unarchived span is not skipped. For a played campaign with an available original completed save boundary, pass `init --source-floor <verified-boundary-receipt.json>` in addition to its conversation ID. The helper verifies that original completed source and rejects admission of the same or earlier response as new progress. Across a later rollout of the same conversation it requires a verifiably later host completion timestamp. This establishes the recording start, not a fabricated transaction or a retrospective semantic audit. Keep the actual baseline/source coverage; an unavailable floor is a disclosed limitation, never an invented message identity.

`abandon` is only for a reconciled uncommitted response that actually did not survive or was explicitly cancelled; it preserves the batch and obtained results. It is not an undo command for committed history or a shortcut around unavailable delivery evidence. Retain the pending item when its disposition is unknown.

## Foreground completion mode

This experiment supplies foreground tools, not a host callback or background service. Before the final reply, preserve one prepared batch with the exact intended response and its established changes. At the next actual tool boundary, obtain the original completed delivered assistant message and confirm its identity and exact content against that batch **before resolving another action**. An original host message/export may supply this evidence; the draft itself, model recollection or a statement that a reply was sent does not. Preserve any known unavailable source span honestly.

For routine Codex PLAY, `resume` uses the supplied `TOOLS/codex_exchange.py` adapter to verify actual previous delivery and returns compact metadata/hashes; `--full` and repeated `--path` select required full bodies. Do not separately export a receipt and confirm again after a successful resume. The lower-level adapter/confirmation commands below remain for an identified source/recovery task. Write the prepared response text exactly to the selected local input file, then run after completion:

```text
python TOOLS/codex_exchange.py --thread-id <actual-thread-id> --expected-response <exact-response.txt> --transaction-id <pending-id> --output <delivery-receipt.json>
python TOOLS/persistence.py --root . confirm --receipt <delivery-receipt.json>
```

The adapter can narrow an observed ambiguous source with `--source <actual-rollout.jsonl>` and `--turn-id <actual-turn-id>`; select recorded tool outputs only when needed with `--tool-item-id <actual-item-id>`. It does not invent identifiers or turn a draft into completed delivery. Confirmation reopens the claimed source instead of trusting a handwritten Codex receipt. New source admission needs accessible host records; later receipt-chain verification remains portable. A manual/operator observer is a separate accepted fallback requiring **Incremental delivery observer: operator** in the agreement and actual supplied completed source. Missing adapter access never silently selects that fallback.

If delivery was interrupted, edited, regenerated, abandoned or cannot be established, keep the prepared batch pending until reconciled. Do not commit its proposed outcome merely because the file exists. Preserve already obtained random inputs with their procedure and scope; retrying persistence or recovering an interrupted reply never authorizes another draw. If only part of the response was delivered, retain that actual source and resolve the narrow discrepancy without completing a reserved player choice.

A host with a reliable completed-message callback may confirm against the actual delivered event. Such integration requires its own demonstrated capability; this local foreground helper does not supply it. Report the actual boundary as **prepared**, **delivery confirmed**, **checkpoint verified** or **full save verified**. Never claim universal immediate post-delivery persistence. A crash after delivery can leave a prepared batch requiring source reconciliation on restart.

At an ordinary turn boundary, batch mechanical work and keep notices out of fiction. Follow the accepted presentation preference; do not print private changes, a maintenance worksheet or a save announcement every exchange. Report a material persistence failure promptly and pause further state advancement until it is resolved or an explicit safe fallback is selected. Silent failure is not an accepted fallback.

## Supply established changes

Each batch identifies its actual exchange, expected predecessor, source provenance and targeted changes to existing state owners. Preserve unaffected text and scope. New required people/system records include their established current contents and discoverable routes in the same batch. A first mutable override follows the existing complete-current-surface rule; no combining a new partial override with superseded module values.

The prepare input contains `transaction_id`, `conversation_id`, `expected_head` from resume/status, actual `user_text`, exact planned `response`, and `changes`. Optional `source_notes` and `actual_results` retain factual coverage/input. Each existing-record change uses `path`, verified `expected_sha256`, and minimal `edits`: exact unique `before`/`after` spans or the compact unique field, line-suffix and section-append selectors in PLAY_PERSISTENCE. Broad section replacement is not the routine update method. A newly created record uses null `expected_sha256` and full established `content`. An empty `changes` list is allowed. Never manufacture a prior hash, source reference or original utterance.

Store each established fact once at its canonical owner, with only a necessary short resume pointer elsewhere. Do not recap an exchange in CURRENT_SAVE, NOW and KNOWN or rewrite unchanged baselines. Preserve every consequential changed value, qualification and unresolved choice; there is no hard edit-size cap. Original dialogue retains scene texture and exact available wording, while operative facts remain discoverable through current owners. Defer prose cleanup to checkpoint without losing meaning. `prepare` returns `resulting_hashes`; retain them with known resulting bodies. After actual delivery confirmation, matching `effective_hashes` from resume allow reuse without another full read.

The confirmation receipt uses `schema: rpg-delivery-v1`, `transaction_id`, `conversation_id`, `complete: true`, an actual selected `observer`, exact delivered `assistant_text`, and factual `source_ref` with stable actual message identity. Preserve the adapter's complete receipt, including its original `user_messages` and selected tool sources; do not trim it into a manually asserted substitute. Prepared `user_text` must match the observed original input. `codex-rollout` requires the source-verifying adapter; `operator` requires the separately accepted fallback above. The immutable receipt and predecessor digests attest retained bytes and bindings, not the GM's interpretation.

For that user-input comparison only, terminal CR/LF differences are ignored because the host commonly appends a final line break absent from the displayed input. Spaces, tabs, internal line breaks and substantive text remain significant; assistant-response matching remains exact. Original receipt input is preserved unchanged and supplies the archived user text. Partial correction offsets refer to that original observed text, not a transport-normalized copy.

Preserve PC values, time and unresolved declarations, actual knowledge with qualifications, commitments, private/system effects, complete changed active encounter fields, genuine deactivation and retained consequences, session continuity and once-only mechanical application references where affected. Record actual outcome values, not an instruction to roll again, re-evaluate a seed or perform a future subtraction. An intended action is not a completed event. Store factual provenance, never private reasoning.

An exchange with no current-state change can have an empty change set while preserving useful original dialogue and the completed PLAY count. Do not invent a no-change fact for every bystander or force a durable NPC profile. Original source capture and state deltas have separate roles: a concise commitment summary cannot replace its exact available wording, and stored raw source does not establish that every sentence belongs to surviving fiction.

Expected prior values/bytes and unique identities prevent detectable stale writes and duplicate application. The same transaction retried is the same operation; identical text in two actual exchanges is not a deduplication key. These checks cannot prove that the GM selected every affected fact or interpreted a promise correctly.

## Read the effective present

At boot and before later current-state retrieval, use the helper's effective view for affected records and routes, following PLAY_PERSISTENCE's compact resume/hash reuse rather than repetitive status/full reads. `resume --full` returns CURRENT_SAVE; repeated `--path` selects other required full owners in `records`. This applies to CHAR, NOW, KNOWN, PEOPLE, CAST_STATUS and other supported owners, including records existing only in committed batches. A direct baseline read/search alone cannot settle a changed current fact or prove that a new person/route does not exist. A hash is useful only with its known exact corresponding body.

The initial helper scopes exchange changes to CURRENT_SAVE, NOW, KNOWN, CAST_STATUS, optional PREP and Markdown descendants of CHAR, PEOPLE, NOW and KNOWN. It does not authorize arbitrary campaign writes. Agreement, safety, correction-register, engine, module and archive changes require their owning supported operation; do not smuggle them into an allowed file to bypass the boundary. Read unaffected owners through their normal exact-source path where the helper does not serve them.

Reuse an already loaded effective body when its hash matches the newly verified effective hash at the current boundary. A body retained after applying the exact own prepared edits may be reused after actual delivery is confirmed and its returned resulting hash matches; unknown bodies or mismatches require retrieval. Distinguish that effective view from exact original file/source bytes. MODULE rules/lore and historical evidence keep their normal routes. Prepared changes remain excluded from committed authority until delivery confirmation; reconcile pending delivery before another action.

## Consolidate and review

CHECKPOINT resolves pending delivery, selects the exact committed transaction boundary and obtains the effective present. Perform the existing lightweight affected-record, route, ownership and once-only checks; preserve complete current state and unchanged archive metadata. Use the persistence helper's protected consolidation operation so baseline files and the incorporated transaction boundary remain recoverable together. Do not update current files by an independent save and leave the journal claiming an older baseline. A failed or interrupted consolidation blocks PLAY until the recorded operation is reconciled.

Only completed PLAY replies since the last verified consolidation count toward cadence. Prepared replies, OOC discussion, tools and maintenance do not count as completed PLAY. Confirming each exchange must not continually reset the autosave counter. Use the observed committed boundary/count, preserve an accepted custom cadence, and never infer a count from filenames or generated prose. Manual checkpoint/full save supersedes the scheduled consolidation as before.

Full SAVE retains [CLOSE_CONTRACT](CLOSE_CONTRACT.md)'s archive and review duties. Reuse preserved original sources mechanically where possible and label their accepted scope, revisions and gaps. Archive only remaining accepted evidence; incorporation into a checkpoint is not evidence deletion or a reason to apply the same effects again. Keep journal/source material until its recovery and evidence duties are demonstrably preserved. This experiment introduces no journal-pruning or archive-purge permission.

The close plan supplies a new `save_id`, `expected_head`, compact `title`, `route_terms`, `span`, `place`, `session_id` and `review` with actual `status` (`complete`, `incomplete` or `not-selected`), `scope` and `limitations`. Optional `current_updates` use the same expected-hash/exact-edit grammar for existing supported owners, or null expected hash plus full `content` for a genuinely new authorized record such as useful preparation, to preserve already authorized session/correction work; they do not create its authority. Actual feedback/lifecycle source uses `operational_evidence: [{session_id, text, source_ref}]`, labelled separately from fictional events. Never insert inferred feedback or private reasoning.

For an accepted supersession affecting a whole captured exchange, `source_dispositions` maps its transaction ID to `{status: "superseded", reason, correction_ref}`. The helper excludes that whole exchange from the new accepted-fiction body while retaining raw journal source and the disposition. For a partial correction, use `status: "partly-superseded"` with `spans: [{role: "user" or "assistant", start: 0, end: 10}]`: offsets are zero-based Python Unicode-character positions, end-exclusive, in the exact original message. Only explicitly superseded spans are excluded; surviving text is copied in order and the omission and accepted correction route are labelled. The helper checks bounds/overlap, not whether the correction is authorized or semantically complete. Do not discard a whole exchange just to avoid reviewing its valid parts, or call an unaccepted correction supersession. Previously archived source retains its existing immutable history and correction routes.

For source review, inspect the declared new accepted source span independently of the journal's selected changes, then compare affected current owners and prior authorities. A promise omitted from the journal must remain discoverable from source. Perform one defined review pass; repeat only the checks invalidated by a concrete discrepancy/correction, extending source scope for an identified dependency or conflict. Do not repeatedly rebuild the same capture, preimages, archive or already verified candidate without a changed input. If coverage cannot be completed, preserve valid progress and report the exact incomplete review scope under the existing policy. Receipt generation is not another unlimited semantic review.

## Corrections, transfer and portability

Use [CORRECT](CORRECT.md) for error repair or an accepted rewind. Supersede committed effects explicitly with the corrected effective values and scope; never erase original committed provenance or apply compensation twice. A chat edit alone does not revoke a committed transaction. Reconcile its actual source and dependent consequences. Agreement, safety, engine and historical repairs retain their owning authorization/procedure; the journal is not permission to write any campaign path.

Before a full save, session end, handover, protocol-changing upgrade or GM/runtime switch, reconcile prepared delivery and identify the exact committed/consolidated boundary. For this experiment, full-save remaining journal evidence before freezing a scene handover; that prevents a later external return archive and the next journal close from both archiving the same unaccounted source. The receiving GM must not append to the frozen source journal. Import uses one protected source operation and preserves the exact journal source/base boundaries. Do not bypass a handover or recovery barrier through a per-turn write.

Routine code-compatible maintenance can replace only its reviewed program/docs through a protected runtime operation while preserving campaign state, agreement, journal, preparation intent, pending batch and source bytes exactly. Verify backup/preimages, single-writer pause, unchanged schema/semantics and the resulting runtime's ability to read those bindings before resuming. Such maintenance need not confirm a pending response, consolidate fictional state, archive evidence or rebind an unchanged campaign merely to install equivalent code. Do not clear a pre-existing recovery/handover barrier to perform it. A schema, authority, contract, state or persistence-semantics change is a substantive migration and retains the reconciliation/consolidation process below.

For an already authorized substantive state/contract/protocol maintenance or transfer outside the helper's current write scope, first reconcile and consolidate all committed state. Use that operation's existing protected procedure while preserving journal cursors/anchors and retained source; complete its recovery/transfer disposition. Then use `rebind --conversation-id <actual-id> --expected-base <old-journal-base>` to bind the verified resulting save/agreement and selected conversation. Rebind checks campaign and incorporated boundaries, preserves source history and never absorbs unconsolidated changes. It does not authorize the preceding maintenance or transfer. Stop on a mismatch instead of rewriting the head to make it pass.

Backups and compatible exports include the complete journal and required baseline, source and recovery material. An older loader that ignores an enabled journal cannot reliably resume an unconsolidated campaign. Before disabling or moving to an incompatible runtime, reconcile and consolidate all accepted changes, full-save available evidence, verify a self-contained compatible export and preserve the original recovery copy.

To disable, first complete that full save; then publish the explicitly accepted agreement clause **Incremental persistence: disabled**, removing its enabled literal through protected RECALIBRATE. Run `disable`. It requires no pending batch/preparation intent and equal consolidated, archived and committed boundaries. The helper atomically renames HEAD to retained `INSTANCE/JOURNAL/DISABLED-<stream_id>.json`; it does not delete batches, receipts or history. Verify completion and ordinary baseline readiness before play. An interrupted or failed disable remains an administrative task; do not merely remove HEAD yourself. Automatic re-enabling over retained nonzero journal history is unsupported and requires a separately designed verified stream-epoch migration, not a fresh `init` over old records.

The helper validates mechanical bindings; source fidelity, semantic completeness and acceptable latency still require actual checks.
