# ADMIN — Add a missing Setting Brief

ADMIN maintenance. No fiction. This is a one-time compatibility transaction for an already-bound v0.6 or v0.6.1 campaign; it is not PLAY, LOAD, bind, module redesign, lore migration, CHECKPOINT, CLOSE, or REVIEW.

Open this file only after the operator explicitly says **UPGRADE SETTING BRIEF**. Do not run it merely because normal boot reports that `MODULES/<id>/SETTING_BRIEF.md` is missing or malformed.

## Preconditions

Before drafting or writing, require all of these:

1. The operator attests that the active folder is an upgraded copy of an already-bound v0.6 or v0.6.1 campaign, not an unbound kit, v0.5 run, new bind, partially migrated tree, or module under ordinary authoring.
2. The operator attests that a restorable byte-for-byte backup of the complete campaign folder exists **outside** the active OS folder.
3. The operator attests that CURRENT_SAVE includes all accepted PLAY. If any accepted play occurred after that save, stop and persist it under the campaign's prior compatible runtime first. A chat transcript, recollection, or platform log is not a substitute.
4. CURRENT_SAVE and CAMPAIGN_CONTRACT are otherwise valid, accepted, bound v0.6 authorities with matching campaign and module identities. Their engine, PC, safety, INSTANCE, and archive routes resolve without contradiction; when `commit_kind: close`, the ordinary close/index match also passes. The only compatibility failure is the absent required Setting Brief.
5. `MODULES/<module>/SETTING_BRIEF.md` does not exist, and no `SETTING_BRIEF.candidate.md` or other unfinished upgrade artifact exists. A fixed but malformed or wrong-module brief is an existing module defect and must be repaired separately; this procedure may not overwrite it. Candidate residue is ambiguous and must be resolved against the external backup before restarting.

Use only directly addressed records needed for this preflight. Do not list, search, or browse for a version, substitute brief, lore source, or campaign clue. If provenance, persistence, identity, or structural health is uncertain, write nothing and stop.

## Bounded source material

The Setting Brief may restate only stable, public module facts that already have authority. It establishes no new canon.

- Read the bound `MODULE.md` descriptor for identity and broad declared capability kinds.
- For `World identity` and `What is ordinary`, use operator-supplied exact facts or the smallest directly named stable public MODULE passages needed to verify them. Ask a compact clarification when needed.
- Treat every proposed sentence as unfixed unless the operator identifies its existing public authority and accepts the restatement.
- Use `Available depth` only to name broad kinds of colder authority that actually exist through declared capabilities. Do not open those bodies merely to make the list richer.

Do not infer setting facts from genre, title, engine, generic model knowledge, prior-chat memory, archive events, private truth, or campaign patterns. Do not copy detailed lore into the brief. Do not include named cast, current mutable state, PC history, private material, seeds, clock or phase bodies, preparation, queued situations, plot summary, or campaign forecast.

## Candidate and acceptance

1. Prepare one complete candidate body in OOC without writing it to the tree. It must contain only:

   ```markdown
   ---
   id: <module>.setting_brief
   class: setting-brief
   ---

   ## World identity
   <concise substantive public orientation>

   ## What is ordinary
   <concise substantive everyday baseline>

   ## Available depth
   <broad kinds of declared cold authority>
   ```

2. Show the complete candidate verbatim, identify the existing public authority or operator attestation supporting each substantive statement, and state that it is not yet authority.
3. Ask for exact **ACCEPT SETTING BRIEF** or revision. Silence, continued PLAY, a vague acknowledgment, or acceptance of only a summary is not acceptance. Refusal or revision writes nothing.
4. Immediately before any write, re-read CURRENT_SAVE and CAMPAIGN_CONTRACT and confirm their ids/revisions and the module identity still match the accepted preflight; confirm the fixed and candidate Setting Brief paths remain absent. If anything changed, stop and restart.
5. After acceptance, write the exact accepted body to `MODULES/<module>/SETTING_BRIEF.candidate.md`. Do not change its wording while writing.
6. Validate the candidate against `MODULES/_CONTRACT.md`: exact scalar id and class, exact once-only required level-two headings in order, substantive concise bodies, and no prohibited material. Confirm that this candidate is the only proposed tree change.

If candidate validation fails, publish nothing. Do not repair it silently; show the defect and return to a complete revised draft and fresh acceptance.

## Publish and verify

After the accepted candidate passes its focused checks:

1. publish it unchanged as `MODULES/<module>/SETTING_BRIEF.md`;
2. re-open the fixed file and verify it is byte-for-byte identical to the accepted candidate;
3. remove the candidate only after that comparison succeeds;
4. run the shipped read-only structural validator against the complete tree;
5. confirm CURRENT_SAVE, CAMPAIGN_CONTRACT, BEARING, every other MODULE file, ENGINE, INSTANCE, ARCHIVE, safety, and all ledgers remain byte-identical to the preflight tree.

The operation does not mint a save, contract, archive, or Bearing revision. The new fixed Setting Brief is the sole allowed change.

If publication or final validation fails, do not enter PLAY or claim automatic rollback. If the accepted fixed file and candidate can be compared unambiguously, complete only this already-accepted one-file transaction and validate it; otherwise restore the complete external backup and restart.

## Result

On success, report the bound module id, the published Setting Brief path, the validator result, and that no other campaign authority changed. Stop. Begin PLAY only in a fresh chat after the normal five-file technical boot and bounded pre-fiction loads succeed.
