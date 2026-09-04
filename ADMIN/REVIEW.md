# ADMIN — Campaign Review

ADMIN maintenance. No fiction. No canon compilation.

REVIEW is the optional stewardship pass after a successful PERSIST. It asks what the campaign may be becoming and writes only `INSTANCE/BEARING.md`. It never changes what is true.

Open this file only after an explicit **REVIEW** command, or as the second, separately reported step of **END SESSION** after CLOSE succeeds.

## Preconditions

1. CURRENT_SAVE is bound and valid, and its latest commit is a successful `checkpoint` or `close`.
2. No accepted PLAY remains unsaved after that commit. If play continued, stop and request CHECKPOINT or CLOSE first.
3. `INSTANCE/CAMPAIGN_CONTRACT.md` is valid, accepted, and matches CURRENT_SAVE by `campaign_id` and `module`.
4. The accepted contract says `review_mode: bearing-only`. If it says `off`, report that REVIEW is disabled. Do not change the contract here.

If a precondition fails, write nothing. A skipped or failed REVIEW never blocks PLAY and never weakens a valid save.

## Authority boundary

Bearing is provisional GM orientation, not campaign fact.

REVIEW may:

- identify accumulation, recurring choices, consequences, weak or emerging patterns, contradictions, and retired directions;
- preserve PC-declared goals and explicit OOC preferences in separate lanes;
- describe observed PC conduct without inferring desire, consent, attraction, or a wish for more of the offered material;
- identify questions worth watching;
- conclude **no stable pattern yet** or **no preparation warranted**.

REVIEW may not:

- change CURRENT_SAVE, Campaign Contract, MODULE, ARCHIVE, NOW, KNOWN, CAST_STATUS, CORRECTIONS, SAFETY, a PC/person record, a clock, phase, faction, institution, resource, cue, or any other current authority;
- advance time, tick a system, resolve an unknown, establish an off-screen event, or manufacture historical cause;
- turn a rumor, inference, possibility, or observed response into fact or player preference;
- supply an external warrant, activate a seed/person/process, or grant a prepared idea priority;
- write a durable preparation bank. v0.6 supports only `off` and `bearing-only`; preparation remains cold and disabled by default.

## Bounded inputs

Open:

1. the accepted Campaign Contract;
2. CURRENT_SAVE and only the exact current INSTANCE routes needed to understand its causal frontier;
3. the prior Bearing, if any, as supersedable interpretation rather than evidence;
4. only the archive indexes, evidence headings, and accepted records needed to review developments not already clear from current state.

Follow routing indexes. Do not dump the archive, scan the repository for inspiration, or open inactive seeds/preparation. `evidence_scope` must name the bounded files/headings actually used, with non-revelatory routes where required. Absence from the reviewed scope means **not reviewed**, not **did not happen**.

## Review pass

1. Fix the bases: CURRENT_SAVE `save_id` and `save_rev`, Campaign Contract `contract_id` and `contract_rev`, and the evidence scope.
2. List compact references to established developments. Do not duplicate canon as a second authority.
3. Separate player input:
   - **PC-declared goals** — only goals actually declared in fiction;
   - **explicit OOC preferences** — campaign-attention calibration, never fictional facts.
4. Record observed conduct literally enough to avoid attributing motive. Player response to GM-offered material does not prove interest.
5. State provisional interpretations, each visibly revisable and supported by cited established developments.
6. Mark apparent directions as active, weak, contradicted, or retired—or say no stable pattern exists. Do not invent a destination or convert compatibility into warrant.
7. Add only compact questions worth watching. Do not answer them to make the review feel complete.

Novelty may be zero. A short honest Bearing is better than a synthetic arc.

## Bearing transaction

Build `INSTANCE/BEARING.candidate.md` using INSTANCE/_SCHEMA.md with `status: candidate`. Copy the matching `campaign_id`; set `base_save_id` and `base_save_rev` to the reviewed CURRENT_SAVE values, set `base_contract_id` and `base_contract_rev` to the accepted Campaign Contract values, and include the bounded `evidence_scope`.

Validate the candidate's identity, bases, exact sections, and noncanonical labels. Confirm it contains no current-state replacement, activation instruction, warrant claim, or preparation list. Set the publishable record to `status: provisional`, recheck it against the current bases, replace `INSTANCE/BEARING.md` only after that check, then remove the candidate.

If generation, validation, or replacement fails, leave CURRENT_SAVE, Campaign Contract, ARCHIVE, and every current authority untouched. Preserve the prior Bearing unless restoration is required for a partial replacement. Report REVIEW failure separately; PLAY remains available without Bearing.

## Result

Report OOC:

- REVIEW succeeded or failed;
- the `base_save_id`/`base_save_rev` and `base_contract_id`/`base_contract_rev` on success;
- whether the honest result was **no stable pattern yet**;
- that no canon or current state changed.

Do not print private analysis or candidate material unless the operator explicitly asks for it.
