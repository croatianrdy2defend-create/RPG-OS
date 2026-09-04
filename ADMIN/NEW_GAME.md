# SETUP — New Game

Operator-side construction. Not PLAY. Not fiction. Not canon until ADMIN commit.

Open this file only after an explicit **NEW GAME** / **create campaign** request. Never on unbound boot.
If CURRENT_SAVE is already bound, stop. Do not overwrite a live run. New Game in this folder is for unbound kits only.
If the save is unbound but ARCHIVE has any campaign row, ledger row, session folder, or other prior-run evidence, or INSTANCE contains non-template registers/overlays or an unexpected path, stop. Use a clean separate kit copy. Never clear or inherit prior-run state to make New Game proceed.
This guard authorizes one bounded ADMIN inventory of `ARCHIVE/` and `INSTANCE/` only; it does not authorize PLAY discovery or a repository-wide lore scan.

## Mode

SETUP may: ask design questions; summarize; flag missing required fields; draft proposed module text; draft a compact engine file; challenge contradictions; show a proposed manifest.

SETUP may not: narrate a play scene; roleplay NPCs in-character; advance instance time; make PC decisions; roll; treat drafts as canon; write persistent files while questions are still open.
The proposed starting frame is draft until the operator accepts or revises it. Unaccepted alternatives have no later authority.

## Transaction

```
unbound READY
→ explicit NEW GAME
→ SETUP interview (draft only)
→ proposed configuration
→ operator accept
→ validation checklist
→ ADMIN writes files
→ bind INSTANCE from T0
→ fresh PLAY chat
```

Nothing is campaign canon because the wizard proposed it.
During the interview say **recorded in the draft**, never **locked**. The only lock is operator ACCEPT → ADMIN commit.

## Stage A — runnable core only

Draft, then on accept write:

- `ENGINE/<id>.md` if this run chose a ruleset that was not already installed
- `MODULES/<id>/MODULE.md` (v0.4 descriptor: scalar front matter + exact `## Capabilities` section)
- `MODULES/<id>/SETTING_BRIEF.md` (required compact public session-start orientation; exact setting-brief front matter and headings)
- `MODULES/<id>/POLICY.md` (must declare voice under exact heading `## Voice` and complete proposed run settings under exact heading `## Campaign defaults`)
- `MODULES/<id>/CHAR/PC.md` (substantive operator-approved entrypoint; one body or a compact index with its exact routed PC bundle; a completed mechanical sheet is optional)
- `MODULES/<id>/T0_SAVE.md`
- `INSTANCE/CAMPAIGN_CONTRACT.md` (the compact, run-scoped promise and accepted GM calibration; write from the accepted draft, not inferred module defaults)
- optional capabilities **only if** a declared target entrypoint and at least one real authoritative body will exist at commit; sparse setup omits them
- accepted extra safety sentences into `INSTANCE/SAFETY.md`; set CURRENT_SAVE `safety_state`

At bind, reset `INSTANCE/BEARING.md` to the schema's bound-empty shape: the new run's `campaign_id`, `status: none`, empty base/evidence values, and all sections `none`. This identity-only reset is not REVIEW content. A contract with `review_mode: bearing-only` permits a later REVIEW; it does not create an opening interpretation or preparation.

If voice or a valid substantive Setting Brief is missing after accept, the module is not runnable. Do not bind.

## Stage B — optional authoring

Only if the operator chooses more than sparse campaign construction or asks to build a declared capability. Open `ADMIN/CAMPAIGN_BUILD.md` only for that branch.
Do not auto-create NPC stubs, seed banks, or encyclopedias because a capability exists.
Follow MODULES/_CONTRACT.md retrieval locality: keep cohesive material together; when parts are independently useful, create a compact declared index with real authoritative bodies and explicit pointers. Do not prebuild empty directory trees or split by an arbitrary size threshold.

## Interview (minimum)

Ask one cluster at a time.

1. Rules engine — first question.
   List installed engines by reading `ENGINE/*.md` and `ENGINE/*/ENGINE.md`. Exclude `_CONTRACT.md`, README/pointers, any candidate without exact scalar `class: engine`, any root file whose stem does not equal its front-matter `id`, and any directory engine whose directory name does not equal its front-matter `id` (skip aliases).
   Also accept a system the operator names.
   Before resolving or drafting any engine path, confirm its proposed id uses only ASCII letters, digits, `.`, `_`, and `-`, begins with a letter or digit, and contains no separator or traversal segment.
   - If that id already exists, record it as the draft engine.
   - If it does not exist, SETUP drafts a new `ENGINE/<id>.md`: resolution procedure + required/deferred/optional sheet field groups + compact character-build order only. Do **not** paste a copyrighted rulebook. If uncertain, ask; do not reconstruct chapters or bulk tables.
   - Show the engine summary before moving on: resolution method, required/deferred/optional field groups, and character-build support (`self-contained`, `operator-values-required`, or `no-mechanical-sheet`). Do not imply the adapter supplies rules or values it does not contain.
2. Title, one-line premise, and a proposed portable module id. New engine/module ids use only ASCII letters, digits, `.`, `_`, and `-`, begin with a letter or digit, and contain no separators or traversal. Confirm the id before any path is drafted. Then address only the exact proposed `MODULES/<id>` path: if any file or directory already exists there, stop that id and offer a new id or LOAD of the existing module in a clean instance. Do not list MODULES and never overwrite an installed module through NEW GAME.
3. Narrative voice — required.
4. Tone and cadence.
5. Genre policy / anti-attractors.
5b. **Only if the premise is real-world historical:** source policy. Record it in POLICY.
6. **Safety extras beyond the OS floor — ask before detailed world, character, or starting-frame drafting.** Record accepted operator/run-specific sentences under the exact INSTANCE/SAFETY.md `Hard no:` or `Fade / veil:` labels, as bullets or inline label text. If any real sentence is accepted, draft `safety_state: active`. A MODULE may separately impose stronger genre/content restrictions in POLICY. If safety changes later, recheck every affected draft before ACCEPT.
7. **Run campaign contract — always ask and explicitly accept.** A MODULE may propose defaults; it cannot accept them for this run. Draft the compact `INSTANCE/CAMPAIGN_CONTRACT.md` with:
   - a one-to-three-sentence `campaign_promise` describing the kind of play being offered and its material tone/cadence, without a plot destination;
   - a compact `fit_envelope` saying what kinds of material belong, what does not, and the accepted anti-attractors needed during routine play;
   - six independent axes: `structural_direction`, `gm_initiative`, `pressure_incident_density`, `time_handling`, `development_priorities`, and `guidance_visibility`;
   - `creative_mandate`, separately accepted as `off` or `on`; when on, separately accept `creative_mandate_scope` and eligible scene/session/calendar `creative_mandate_boundaries`;
   - `review_mode`: `off` or `bearing-only`.

   Use the axis meanings in INSTANCE/_SCHEMA.md. Ask one compact cluster and let the operator revise individual axes. Do not infer one axis from another: high pressure does not imply proactive initiative; proactive initiative does not itself grant a creative mandate; broad direction does not specify a plot. A boundary is an opportunity, never a warrant by itself. `bearing-only` permits an optional later REVIEW and no durable preparation body.
8. **World and campaign construction depth — always ask.** This choice is independent of character detail.
   - **Sparse** (default): premise, opening place, required policy, T0, and starting situation only.
   - **Focused:** develop only selected facts or systems likely to matter near the opening.
   - **Detailed:** develop selected domains step by step, including their causal operation and retrieval routes.
   - **Custom:** operator chooses depth separately for world detail, campaign dynamics, bookkeeping, and rule calibration.
   Focused, Detailed, or Custom opens `ADMIN/CAMPAIGN_BUILD.md`. Detailed never means “generate everything.” Omitted areas stay absent or unfixed; do not create filler, mass rosters, or empty trees.
   At every depth, derive one concise `SETTING_BRIEF.md` from the world facts the operator has already accepted. It must identify the world, state the few public ordinary facts generic model priors would erase, and name the broad cold depth available. Do not turn this into another lore interview: ask one small clarification only if the accepted premise cannot supply a required section. Do not put named cast, current state, private truth, seeds, clocks/phases, preparation, plot summary, or detailed lore into the brief.
9. **PC concept, agency split, character/profile depth, and mechanical-sheet path — always ask.** Open `ADMIN/CHARACTER_BUILD.md`.
   - Profile depth: Quick / Standard / Detailed / Custom.
   - Mechanical sheet: No full sheet now / Minimum required / Guided full sheet / Import and review.
   These are independent choices. A full sheet is optional; the baseline PC record is not. Missing optional facts remain unspecified. An ENGINE-required field may be deferred only when that ENGINE permits it; otherwise resolve it or delay bind rather than guess.
10. T0 frame: era/datetime, place, body/state, obligations, intentionally unfixed facts, `scene_status`, `uncommitted_time`, exact `pc_declared_goals` if the player supplied any, and the compact established `causal_frontier`. If optional campaign systems were drafted, run the starting-state dependency and interaction audits in `ADMIN/CAMPAIGN_BUILD.md` before finalizing T0. Do not infer a PC goal from persona, background, campaign promise, or OOC preference. Do not put interpretations or prepared possibilities in the causal frontier.
11. **Starting frame (required and operator-accepted).** Propose one playable opening frame that fits the accepted contract, premise, voice, safety, T0, and anti-attractors. Offer alternatives only if the operator asks for them or rejects the first frame.
   - Orient the player: where and when the PC is, what is relevantly perceivable, what established matter is already moving (if anything), and whether uncommitted PC time remains.
   - A live incident is optional. A quiet ordinary frame or genuine solitude is valid; the frame may be empty of incident but not empty of orientation.
   - Hand back before the first voluntary PC act. Do not supply the PC's feelings, goal, decision, prior conduct, or consent.
   - Do not manufacture a hook, stranger, threat, clue, or problem merely to make the opening look active. If the accepted creative mandate permits proactive authorship, that is permission, not a quota.
   Forbidden: violating anti-attractors; choosing the PC's feelings or first move; a three-act quest; unprovided prior PC promises, crimes, intimacy, purchases, or risk acceptance. If a frame depends on a prior PC fact, list that fact separately for explicit acceptance.
   Record the accepted frame into T0 `immediate_scene` and compile its actual open/closed state and remaining player-owned time into the new T0 fields.
12. Optional capabilities: declare only those that will have a real authoritative body at commit. The declared target may be that body or a compact routing index pointing to it. Write the exact MODULES/_CONTRACT.md capability table; sparse setup writes `none` under `## Capabilities`.
13. Proposed manifest including the complete draft run contract, the exact required `SETTING_BRIEF.md`, construction depth, character/profile depth, mechanical-sheet path and state (`not built/deferred`, `minimum`, `complete`, `imported`, or `partial`), PC storage shape and exact routed bundle if any, separately labeled omitted and intentionally unfixed domains, private-truth disclosure mode/routes if used, mutable-system T0 classifications and cue lifecycle, cross-system update order where applicable, retrieval-route rehearsal for every complex capability, and the single accepted starting frame. Explicit accept or revise.

If the operator asks to start a scene before accept, refuse.

## Accept / validation checklist

Before any write, open MODULES/_CONTRACT.md, ENGINE/_CONTRACT.md, and INSTANCE/_SCHEMA.md. Confirm:

- exact `## Voice` heading declared
- `SETTING_BRIEF.md` has exact scalar `id: <module>.setting_brief` and `class: setting-brief`; exact once-only `## World identity`, `## What is ordinary`, and `## Available depth` headings in that order; concise substantive public orientation; and none of the prohibited roster, current-state, private, seed/clock/phase, preparation, plot-summary, or detailed-lore material
- exact `## Campaign defaults` heading declared in the newly authored POLICY, with a compact nonblank proposal for `campaign_promise`, `fit_envelope`, all six independent axes, `creative_mandate` plus its scope/boundaries, and `review_mode` using the canonical INSTANCE/_SCHEMA.md values; these remain MODULE proposals and are not substituted for the separately accepted run contract
- the run contract has a compact campaign promise and fit envelope; all six axes are present and independently accepted; `creative_mandate` is separately explicit; `review_mode` is exactly `off` or `bearing-only`; it contains no plot destination, current-state claim, inferred player desire, or prepared scene
- MODULE scalar front matter and exact `## Capabilities` section present
- the exact proposed `MODULES/<id>` path is still absent immediately before writes; if it appeared during SETUP, stop rather than merge or overwrite it
- engine id = either exactly one installed engine with scalar `class: engine` whose scalar front-matter `id` matches its flat filename stem or, for `<id>/ENGINE.md`, its containing directory name; or the one operator-accepted in-memory draft destined for `ENGINE/<id>.md`, with exact `class: engine`, a matching safe scalar id, valid support class, and no installed-path/id collision
- no undeclared alias engines
- every listed capability has a declared target entrypoint and at least one real authoritative body, or `## Capabilities` contains exactly `none`
- every PC fact/value was supplied or explicitly accepted; deferred and intentionally unspecified fields remain labeled rather than inferred
- any unresolved ENGINE-required character field is explicitly deferrable **and not required by the accepted starting frame's expected mechanics**, or bind stops
- the ENGINE declares an exact supported `character_build_support` value; setup has not claimed a procedure or sheet capability beyond it
- persona/background text grants no standing permission to author the PC; PC current status agrees with T0
- `CHAR/PC.md` is either one body or a machine-marked index whose exact transitive targets stay under `CHAR/`; no unrelated sibling is included
- detailed construction covers only selected domains, and each complex capability passes a representative need → entrypoint → exact target → stop route rehearsal without discovery
- phase/clock/faction/seed/resource/rule material, if selected, has the authority and lifecycle required by `ADMIN/CAMPAIGN_BUILD.md`; every private system that may need a later cross-boot cue has the optional field reserved, every initially implicated system that cannot otherwise be recognized has one compact nonsecret T0 cue, and every interaction plan applies each cause once
- every accepted mutable-system authority stores its own triggers/non-triggers, selected current-state route, cue lifecycle, and interaction edges/order; the proposed manifest only mirrors these declarations and is not persistence
- private truth, if selected, is reviewed, operator-constrained sealed, or deliberately unfixed; the accepted envelope cannot manufacture PC agency, safety, or mechanics
- starting frame is playable and oriented, does not require an incident, has no authored PC first act, and has only one accepted version in the committed T0
- `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier` agree with the accepted opening; the frontier contains only schema-authorized `consequence:`, `due:`, `process:`, pending `decision:`, and compact non-revelatory current-state `cue:` entries/routes, never interpretation or preparation
- SAFETY sentences vs safety_state match

Then write files. If an accepted engine exists only as the in-memory draft, write and validate that exact compact engine before writing the module or binding; do not substitute or expand it after acceptance. Initialize the canonical empty NOW, KNOWN, CAST_STATUS, and CORRECTIONS templates. Stable subsystem definitions and accepted as-of-T0 snapshots stay in declared MODULE bodies; do not bulk-activate them in INSTANCE. Copy the exact accepted PC route closure to matching paths under `INSTANCE/CHAR/` at bind. Point `pc_record` to `INSTANCE/CHAR/PC.md`.
Assign a new unique portable `campaign_id` for this run, a new safe `contract_id`, and a new safe `save_id`. Build `INSTANCE/CAMPAIGN_CONTRACT.candidate.md` with that same `campaign_id`, `contract_rev: 1`, `contract_parent: none`, `status: candidate`, and the other identity fields required by INSTANCE/_SCHEMA.md. Reset BEARING to the bound-empty identity-only shape defined by INSTANCE/_SCHEMA.md. Build the complete candidate CURRENT_SAVE with `save_rev: 1`, `save_parent: none`, `commit_kind: bind`, `archive_ref: none`, the accepted safety flag, and every required present/orientation field compiled from T0. Validate both candidates and the empty Bearing against INSTANCE/_SCHEMA.md; if any fails, keep the prior unbound save authoritative. Set the publishable contract to `status: accepted` and recheck it, publish it immediately before replacing CURRENT_SAVE, then replace CURRENT_SAVE last, remove both candidate files, and confirm the campaign, contract, and save ids.

If any file write, provider response, or generation is interrupted before CURRENT_SAVE replacement, the unbound save remains authoritative but the folder may contain a published-but-unbound Campaign Contract or partial ENGINE/MODULE/SAFETY/INSTANCE/candidate artifacts. Do not call them committed and do not start PLAY. Either complete only the already accepted manifest and validate the entire bind, or inspect and restore the clean pre-bind copy required by P19 before retrying. Do not improvise missing sealed/private content, silently delete evidence, or claim automatic rollback.

## After commit

Start PLAY in a **fresh** chat.
Resident orientation: LAW/GM Core + accepted CAMPAIGN_CONTRACT + new CURRENT_SAVE; a matching BEARING may join only after a later successful REVIEW. Before first fiction, load applicable safety, the required SETTING_BRIEF once, and POLICY voice; use them silently rather than reciting them.
First fiction: the single accepted T0 `immediate_scene`, with its established causal frontier and uncommitted-time state. Do not add a second situation because SETUP discussed or rejected an alternative. Unaccepted proposals die with the interview chat and never enter BEARING or canon.

This clean kit has no pre-authored world. New Game is how a campaign is born.
