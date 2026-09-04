# ADMIN — Recalibrate Campaign Contract

ADMIN maintenance. No fiction. Prospective campaign calibration only.

Open this file only after an explicit **RECALIBRATE** request. RECALIBRATE edits only `INSTANCE/CAMPAIGN_CONTRACT.md`, and only after the operator sees and accepts an exact OOC diff.

## Preconditions

1. CURRENT_SAVE is bound and valid.
2. The current Campaign Contract is valid, accepted, and matches CURRENT_SAVE by `campaign_id` and `module`.
3. The requested change concerns the campaign promise, fit envelope, one or more calibration axes, creative mandate, or REVIEW mode.

Changing engine, module, campaign identity, current facts, PC sheet, safety, or archive history is not recalibration. Route those tasks to their own explicit procedures. A new safety ruling applies immediately through the safety procedure and is not delayed behind this transaction.

## Editable contract surface

The operator may revise:

- `campaign_promise`;
- `fit_envelope`;
- `structural_direction`;
- `gm_initiative`;
- `pressure_incident_density`;
- `time_handling`;
- `development_priorities`;
- `guidance_visibility`;
- `creative_mandate`;
- `creative_mandate_scope`;
- `creative_mandate_boundaries`;
- `review_mode` (`off` or `bearing-only`).

Treat all six axes independently. Never infer a creative mandate from proactive initiative, sustained pressure, structural direction, or genre. Turning a mandate on requires explicit scope and eligible scene/session/calendar boundaries. Turning it off sets both mandate-detail fields to `none` and removes discretionary authorization prospectively; it does not erase events already established. A boundary remains an opportunity, not a warrant or quota.

The contract cannot contain a plot destination, queued scene, inferred player desire, current-state claim, or prepared candidate.

## Acceptance transaction

1. Quote the current value and proposed value for every changed field. Label unchanged fields as unchanged without redrafting them.
2. Explain compactly what the change permits or constrains prospectively. Do not narrate an example into canon.
3. Ask for explicit **ACCEPT RECALIBRATION** or revision. Silence, continuing PLAY, or a vague acknowledgment is not acceptance.
4. If accepted, build `INSTANCE/CAMPAIGN_CONTRACT.candidate.md` under INSTANCE/_SCHEMA.md:
   - preserve `campaign_id` and `module`;
   - assign a new portable `contract_id`;
   - increment `contract_rev`;
   - set `contract_parent` to the prior `contract_id`;
   - preserve every unchanged accepted field exactly and apply only the accepted diff;
   - use `status: candidate` while building.
5. Validate the candidate, including identity, revision lineage, axis values, creative-mandate separation, and review mode. If valid, set the publishable record to `status: accepted`, recheck it, replace Campaign Contract with the candidate, and remove the candidate. Do not edit CURRENT_SAVE or Bearing.

If there is no accepted semantic change, write nothing and do not mint a new revision.

## Effects and failure isolation

Recalibration applies from acceptance forward. It never rewrites prior play, archive evidence, CURRENT_SAVE, clocks, causal frontier, or PC decisions.

Any existing Bearing becomes stale automatically because its `base_contract_id`/`base_contract_rev` no longer match. Do not rewrite or delete it merely to mark staleness. If `review_mode` is now `bearing-only`, a later successful PERSIST may be followed by REVIEW. If it is `off`, PLAY simply proceeds without Bearing.

If generation, validation, or replacement fails, the previous Campaign Contract remains authoritative unless a partial replacement requires restoration from the operator's backup. Stop and report the failure. Do not resume under a half-written contract, claim automatic rollback, or modify current state to match the failed proposal.

## Result

On success, report the new `contract_id`, `contract_rev`, and the accepted fields that changed. State plainly that the change is prospective, no canon changed, and any older Bearing is stale. Start or resume PLAY only after the new contract can be read and validated.
