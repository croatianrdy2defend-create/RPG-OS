# ADMIN — Migrate a bound v0.5 run

ADMIN maintenance. No fiction. This is a one-time compatibility transaction, not LOAD, bind, REVIEW, or archive migration.

Open this file only after the operator explicitly says **MIGRATE V0.5** and the resident CURRENT_SAVE is an operator-attested, already-bound v0.5 save. Do not run this procedure merely because a file is old-looking or normal v0.6 boot validation failed.

## Preconditions

Before any write, require all of these:

1. The operator confirms that the active folder is an upgraded copy of a bound v0.5 campaign, not a clean kit, v0.6-native run, or partially hand-converted tree.
2. The operator confirms a byte-for-byte backup of the complete campaign folder exists **outside** the active OS folder and can be restored without relying on this transaction.
3. The operator confirms CURRENT_SAVE includes all accepted PLAY. If any accepted play occurred after that save, stop: restore/use the v0.5 environment and CHECKPOINT or CLOSE there first. A chat transcript, recollection, or platform log is not a substitute for persistence.
4. CURRENT_SAVE is a coherent bound v0.5 authority: bound engine/module, portable campaign/save identities, positive revision, valid parent/commit/archive/safety metadata for that version, and a substantive present. It contains no field outside the current schema's CURRENT_SAVE whitelist and none of the four v0.6 orientation fields; a partially hand-converted save is ambiguous and must stop. Its engine, module, PC route, INSTANCE records, and any archive pointers resolve without contradiction.
5. `INSTANCE/CAMPAIGN_CONTRACT.md` is still the canonical unbound v0.6 template. No accepted/candidate contract, migration candidate, or partial migration artifact exists. `INSTANCE/BEARING.md` is the canonical empty template or an untouched identity-free empty equivalent.

This preflight may inspect only the exact bound records and routes needed to establish those claims. It does not apply the v0.6 contract or four new orientation-field requirements to the legacy save. If provenance, identity, lineage, or completeness is uncertain, stop and restore/inspect the external backup; do not guess.

## Explicit acceptance

Collect and show one complete proposed run contract under `INSTANCE/_SCHEMA.md`, then require explicit acceptance. MODULE/POLICY material may inform the proposal but is not acceptance.

The operator must explicitly accept every contract value, including the campaign promise, fit envelope, six calibration axes, guidance visibility, creative mandate, and review mode. Do not infer a creative mandate from genre, initiative, pressure, old POLICY wording, prior GM behavior, or campaign events. If the mandate is off, its scope and boundaries are `none`.

Separately show and require explicit acceptance of the four v0.6 CURRENT_SAVE orientation fields:

- `scene_status`
- `uncommitted_time`
- `pc_declared_goals`
- `causal_frontier`

Use accepted records plus operator clarification. Preserve uncertainty. Never infer a PC goal from conduct, turn a possibility into a causal item, manufacture an outstanding decision, or derive Bearing from repeated events. `scene_status: unknown` and `none` in the other fields are valid when honest.

Also require a valid v0.6.2 module `SETTING_BRIEF.md`. If the legacy module already has one, validate it against `MODULES/_CONTRACT.md` and do not alter it. If it has none, draft the three compact public sections only from stable public module facts plus operator clarification, show the complete draft, and require explicit acceptance. This one compatibility addition is not permission to rewrite the module, summarize its lore, or infer ordinary facts from genre. If a fixed but malformed brief already exists, stop and repair that module defect separately rather than overwriting it inside migration.

No draft is authoritative. Refusal or revision writes nothing.

## Staged transaction

After acceptance:

1. Re-read the legacy CURRENT_SAVE and confirm its `save_id` and `save_rev` still match the accepted migration base. If they changed, stop and restart from preflight. When an accepted Setting Brief must be added, stage it as `MODULES/<id>/SETTING_BRIEF.candidate.md`, validate its exact module-scoped id, class, section order, and substantive bodies, and confirm no other MODULE path will change.
2. Build `INSTANCE/CAMPAIGN_CONTRACT.candidate.md`:
   - preserve the existing `campaign_id` and `module` exactly;
   - assign a new portable `contract_id`;
   - set `contract_rev: 1`, `contract_parent: none`, and `status: candidate`;
   - include the complete explicitly accepted contract and nothing inferred.
3. Build `INSTANCE/CURRENT_SAVE.candidate.md` from the legacy save:
   - preserve every legacy campaign, present, resource, appointment, matter, cue, scene, and roster value exactly; if a legacy contradiction requires correction, stop and resolve it in the backed-up v0.5 run rather than combining correction with migration;
   - preserve `engine`, `module`, `pc_record`, `campaign_id`, `safety_state`, `status`, `datetime`, and `place`;
   - add the four explicitly accepted v0.6 orientation fields;
   - assign a new unique portable `save_id`, set `save_rev` to exactly the legacy revision plus one, set `save_parent` to the legacy `save_id`, set `commit_kind: checkpoint`, and set `archive_ref: none`;
   - contain only the v0.6 CURRENT_SAVE whitelist.
4. Build `INSTANCE/BEARING.candidate.md` as an identity-only bound-empty record: canonical Bearing front matter, the existing `campaign_id`, base ids and evidence scope `none`, base revisions `0`, every required section `none`, and no interpretation, direction, question, preparation, activation, or inferred preference. It may use `status: candidate` while staged.
5. Validate all three staged records against `INSTANCE/_SCHEMA.md`, their shared campaign/module identity, exact field sets, revision lineage, contract enums, PC route, safety state, and the unchanged INSTANCE/archive authorities. Confirm the migration writes no ARCHIVE file, loses no legacy fact, and changes no MODULE path except the explicitly accepted new Setting Brief when required.
6. Finalize the staged Bearing to `status: none` and the staged Contract to `status: accepted`; validate both finalized candidate bodies again. The Current Save candidate remains the new checkpoint.

If any validation fails, publish nothing. Remove no accepted record and report the exact defect.

## Publish order and interruption

After all final candidate bodies pass:

1. when required, publish the accepted `MODULES/<id>/SETTING_BRIEF.md` from its candidate; otherwise leave the existing valid brief byte-identical;
2. replace `INSTANCE/BEARING.md` with the finalized identity-only bound-empty Bearing;
3. replace `INSTANCE/CAMPAIGN_CONTRACT.md` with the finalized accepted Contract;
4. immediately replace `INSTANCE/CURRENT_SAVE.md` **last** with the checkpoint candidate;
5. remove the candidate files only after the fixed records re-open and validate together.

Run the full read-only v0.6 structural validator only after the three fixed records are published; candidate-only checks before publication do not claim that the still-legacy fixed tree already passes v0.6.

CAMPAIGN_CONTRACT is therefore the write immediately before CURRENT_SAVE, and CURRENT_SAVE is the migration commit point. Do not write any unrelated file between them.

Any interruption or partial replacement is fail-stop. Do not enter PLAY, improvise completion, call the run migrated, or choose whichever fixed file looks newest. Restore the complete external backup, or complete only the already accepted transaction after comparing every staged/fixed record to that backup and validating the whole result. Never claim automatic rollback.

## What migration does not do

- It does not rewrite, repartition, re-index, or add to ARCHIVE.
- It does not rewrite MODULE, ENGINE, the PC bundle, people, clocks, ledgers, safety sentences, or other INSTANCE facts. The sole MODULE exception is adding an explicitly accepted required Setting Brief when the legacy module has none.
- It does not create Bearing interpretation or durable preparation.
- It does not infer PC goals, consent, preferences, trajectory, mandate, causes, or pending opportunities.
- It does not convert unsaved chat into evidence.

After success, report the preserved `campaign_id`, new `contract_id`/revision, old and new `save_id`/revision, and that Bearing is empty. State that the operation produced a checkpoint and migrated no archive. Start PLAY only in a fresh chat after normal v0.6 bound validation succeeds.
