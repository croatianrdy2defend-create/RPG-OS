# ADMIN — Save the campaign

Cold persistence procedure. PLAY narrates and adjudicates; this operation writes the accepted record. Read INSTANCE/_SCHEMA.md for record placement and ADMIN/RECOVERY.md before changing files.

## Commands and promise

**Save**, **CLOSE**, and **END SESSION** mean the same normal full save: preserve the complete current state and the available accepted evidence since the previous evidence boundary. No automatic REVIEW follows. Report the save result separately from any later explicit review.

**CHECKPOINT** is an optional present-only save. It preserves all current authorities, retains the prior archive_ref AND evidence_through, and writes no new archive bodies, indexes, or ledgers. Say plainly that new exact evidence was not archived. Do not offer a checkpoint as equivalent to a full save before discarding chat.

**Scene handover** is a separate operation in `ADMIN/SCENE_HANDOVER.md`. It may checkpoint the complete present, then export the available conversation and GM briefing without claiming a new archive boundary. Check `HANDOVER/ACTIVE.md` before ordinary save/play: an active transfer is returned, cancelled or reconciled through that procedure, not advanced by a second GM. Importing an accepted return uses this full-save procedure and a retained receipt so later evidence preservation cannot apply the same changes again.

Saving never advances fiction, resolves an unanswered choice, activates preparation, or interprets campaign direction. Preserve accepted post-save changes already in chat; do not infer goals, preferences, hidden events, or missing rules.

## Compile what changed

Identify accepted transitions since CURRENT_SAVE and the single current authority for each affected value. Begin from its current INSTANCE record; for a first change with no override, use only the specifically named MODULE as-of-T0 snapshot. Apply every still-unsaved change once, preserving the complete current mutable surface. MODULE files remain unchanged.

Carry forward unaffected accepted facts and detailed record sections. Do not shorten, silently omit, or reinterpret them merely because this is a new save. For each accepted change, identify its selected current destination and, on a full save, its surviving evidence source. Compare the proposed changes with the prior records and available accepted play before publication. A same-model compilation and reread remain fallible; a structural check cannot prove semantic completeness or losslessness. Report an actual source/verification limitation when one remains rather than claiming stronger coverage.

Prepare the five readable resume sections. Preserve actual ongoing action, meaningful unresolved decisions, remaining time where relevant, selected public conditions/resources, explicit live goals/obligations, operative processes, and exact useful routes. Follow the accepted agreement's continuation rules; a save boundary does not impose a new PC choice or erase one.

Preserve full PC details under CHAR, what the PC learned under KNOWN, private/system state under NOW, person/relationship progression under PEOPLE, id mappings under CAST_STATUS, and accepted rulings under CORRECTIONS. Do not replace detailed authority with a vague resume summary or duplicate a live total. If an emergent durable person/system first needs persistence, follow the schema's established-only record rules. Keep a non-revelatory process cue only when needed for fresh-chat discovery.

For historical evidence, the boundary is the prior **evidence_through**, not necessarily the prior checkpoint. Gather only accepted source actually available from that boundary forward. A checkpoint may already have applied its state transitions; archiving those transitions now must not apply them to state again. Identify source gaps explicitly; a summary is not the missing dialogue or roll record.

## Full save evidence

Use ARCHIVE/_SCHEMA.md and preserve existing history. Create one new `ARCHIVE/sessions/<close-folder>/` with an INDEX and one or more coherent accepted-evidence bodies. One episode may use one detailed body. Split when independently useful for retrieval, not to meet a quota. Keep exact consequential wording, declarations, outcomes, quantities, chronology, learned facts and uncertainties that are actually available. Exclude rejected/rewound fiction, provider/OOC ADMIN responses, unsent suggestions, and internal preparation.

If a full source is unavailable, archive only what the authoritative available record supports. Mark the missing span/detail and its limits explicitly in the evidence body; do not reconstruct it from model memory, current summaries, old hints, or expected continuity. A current private value may be defensible while its historical cause is unavailable; preserve that distinction. The public save report discloses a material source gap without leaking private content.

Indexes locate, source bodies establish detail. The campaign INDEX row carries the new save_id, close kind, folder, and session-index path. Keep routing terms compact and non-revelatory. A ledger entry is optional when it provides a useful direct route to exact wording or relationship evidence; ordinary relationships and intimacy do not require a special ledger entry. Never duplicate a complete exchange in a ledger or create a duplicate full-session transcript after faithful sharding. If safe partition is uncertain, retain a detailed coherent source and route to it.

## Protected write order

1. Build the intended complete save and affected record changes in working context. Assign a unique save_id, increment save_rev, and set save_parent to the accepted prior id. Full save uses commit_kind `close`, new archive_ref, and evidence_through equal to the new save_id. CHECKPOINT uses `checkpoint` and copies both prior evidence metadata values unchanged.
2. Follow ADMIN/RECOVERY.md: record the entire file and directory sets, preserve and verify all existing-file preimages, list new archive/candidate/body paths and every required new parent directory with verified pre-existence, and create the active marker before campaign writes or directory creation. Protect safety/PC/index files too if affected. Record directories actually created by this operation. If this fails, leave campaign files untouched.
3. Write `INSTANCE/CURRENT_SAVE.candidate.md` and the selected complete current bodies. Do not write the agreement or Bearing. Only an explicitly requested safety/correction change may add its separately authorized affected files to this operation.
4. Full save only: write evidence bodies, session INDEX, campaign INDEX row, then any useful ledger pointers. CHECKPOINT writes none of these.
5. Inspect the candidate and actual assembled write set. Confirm each changed fact has one current destination, accepted transitions were applied once, required sections and metadata are complete, every affected path resolves, and archive/evidence identity agrees. Confirm gaps/uncertainty were preserved. The current pointer still names the earlier save, so do not report a whole-tree structural PASS at this intermediate stage.
6. Replace CURRENT_SAVE last. Read it and the affected routes again. Verify new id/revision, parent, evidence boundary, the intended state, and the recorded directory set. Finish the recovery record and remove its active marker only after successful checking. Preserve preimages and recovery history. Restoring a failed save also resolves operation-created empty directories through the exact nonrecursive cleanup in ADMIN/RECOVERY.md; file restoration alone is insufficient.
7. Confirm OOC: full save or checkpoint, new save_id, where exact evidence now reaches, and any material source limitation. No fictional time passes. An explicit REVIEW request is separate.

If anything fails before or after pointer replacement, keep the active marker and follow ADMIN/RECOVERY.md. An older CURRENT_SAVE alongside separately overwritten newer bodies is not a playable old save. A new CURRENT_SAVE beside missing bodies is not a successful new save. Neither the candidate nor CURRENT_SAVE-last provides atomicity or automatic rollback.

## Historical corrections and later maintenance

Never silently rewrite immutable accepted history to make a later correction look as though no error occurred. Use ADMIN/CORRECT.md to preserve a narrow superseding correction and repair the affected present. A request to undo a valid accepted outcome follows the agreement's Retcon clause; saving itself grants no rewind or ironman exception. Rejected fictional material is not reintroduced as an event. Optional archive reindexing or lossless partition is a separate protected maintenance operation; retain original source whenever equivalence is uncertain.

A full save requires no campaign interpretation, new plot, general repository audit, or exhaustive lore rereading. Use the available accepted source and exact changed authorities, and preserve what is unknown.
