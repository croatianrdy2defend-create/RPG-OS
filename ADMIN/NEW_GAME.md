# SETUP — New Game

Operator-side construction. Not PLAY. Not fiction. Not canon until ADMIN commit.

Open this file only after an explicit **NEW GAME** / **create campaign** request. Never on unbound boot.
If CURRENT_SAVE is already bound, stop. Do not overwrite a live run. New Game in this folder is for unbound kits only.
If the save is unbound but ARCHIVE has any campaign row, ledger row, session folder, or other prior-run evidence, or INSTANCE contains non-template registers/overlays or an unexpected path, stop. Use a clean separate kit copy. Never clear or inherit prior-run state to make New Game proceed.
This guard authorizes one bounded ADMIN inventory of `ARCHIVE/` and `INSTANCE/` only; it does not authorize PLAY discovery or a repository-wide lore scan.

## Mode

SETUP may: ask design questions; summarize; flag missing required fields; draft proposed module text; draft a compact engine file; challenge contradictions; show a proposed manifest.

SETUP may not: narrate a play scene; roleplay NPCs in-character; advance instance time; make PC decisions; roll; treat drafts as canon; write persistent files while questions are still open.
Starting-scenario names and hooks are draft until the operator picks or revises them.

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
- `MODULES/<id>/POLICY.md` (must declare voice under exact heading `## Voice`)
- `MODULES/<id>/CHAR/PC.md` (substantive operator-approved entrypoint; one body or a compact index with its exact routed PC bundle; a completed mechanical sheet is optional)
- `MODULES/<id>/T0_SAVE.md`
- optional capabilities **only if** a declared target entrypoint and at least one real authoritative body will exist at commit; sparse setup omits them
- accepted extra safety sentences into `INSTANCE/SAFETY.md`; set CURRENT_SAVE `safety_state`

If voice is missing after accept, the module is not runnable. Do not bind.

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
6. **Safety extras beyond the OS floor — ask before detailed world, character, or starting-scenario drafting.** Record accepted operator/run-specific sentences under the exact INSTANCE/SAFETY.md `Hard no:` or `Fade / veil:` labels, as bullets or inline label text. If any real sentence is accepted, draft `safety_state: active`. A MODULE may separately impose stronger genre/content restrictions in POLICY. If safety changes later, recheck every affected draft before ACCEPT.
7. **World and campaign construction depth — always ask.** This choice is independent of character detail.
   - **Sparse** (default): premise, opening place, required policy, T0, and starting situation only.
   - **Focused:** develop only selected facts or systems likely to matter near the opening.
   - **Detailed:** develop selected domains step by step, including their causal operation and retrieval routes.
   - **Custom:** operator chooses depth separately for world detail, campaign dynamics, bookkeeping, and rule calibration.
   Focused, Detailed, or Custom opens `ADMIN/CAMPAIGN_BUILD.md`. Detailed never means “generate everything.” Omitted areas stay absent or unfixed; do not create filler, mass rosters, or empty trees.
8. **PC concept, agency split, character/profile depth, and mechanical-sheet path — always ask.** Open `ADMIN/CHARACTER_BUILD.md`.
   - Profile depth: Quick / Standard / Detailed / Custom.
   - Mechanical sheet: No full sheet now / Minimum required / Guided full sheet / Import and review.
   These are independent choices. A full sheet is optional; the baseline PC record is not. Missing optional facts remain unspecified. An ENGINE-required field may be deferred only when that ENGINE permits it; otherwise resolve it or delay bind rather than guess.
9. T0 frame: era/datetime, place, body/state, obligations, intentionally unfixed facts. If optional campaign systems were drafted, run the starting-state dependency and interaction audits in `ADMIN/CAMPAIGN_BUILD.md` before finalizing T0.
10. **Starting scenario (required).** The campaign must not open on a passive idle pose.
   SETUP proposes 2–3 jump-starts that fit premise, tone, cadence, and anti-attractors. Each is a *live situation already happening*, not a plotted adventure and not the PC's first act.
   Forbidden: violating anti-attractors; choosing the PC's feelings or first move; a three-act quest; unprovided prior PC promises, crimes, intimacy, purchases, or risk acceptance. If a hook needs a prior PC fact, list it separately for explicit acceptance.
   Operator picks one. Record it into T0 `immediate_scene` with handback before the first voluntary PC act.
11. Optional capabilities: declare only those that will have a real authoritative body at commit. The declared target may be that body or a compact routing index pointing to it. Write the exact MODULES/_CONTRACT.md capability table; sparse setup writes `none` under `## Capabilities`.
12. Proposed manifest including construction depth, character/profile depth, mechanical-sheet path and state (`not built/deferred`, `minimum`, `complete`, `imported`, or `partial`), PC storage shape and exact routed bundle if any, separately labeled omitted and intentionally unfixed domains, private-truth disclosure mode/routes if used, mutable-system T0 classifications and cue lifecycle, cross-system update order where applicable, retrieval-route rehearsal for every complex capability, and the chosen starting scenario. Explicit accept or revise.

If the operator asks to start a scene before accept, refuse.

## Accept / validation checklist

Before any write, open MODULES/_CONTRACT.md, ENGINE/_CONTRACT.md, and INSTANCE/_SCHEMA.md. Confirm:

- exact `## Voice` heading declared
- MODULE scalar front matter and exact `## Capabilities` section present
- the exact proposed `MODULES/<id>` path is still absent immediately before writes; if it appeared during SETUP, stop rather than merge or overwrite it
- engine id = either exactly one installed engine with scalar `class: engine` whose scalar front-matter `id` matches its flat filename stem or, for `<id>/ENGINE.md`, its containing directory name; or the one operator-accepted in-memory draft destined for `ENGINE/<id>.md`, with exact `class: engine`, a matching safe scalar id, valid support class, and no installed-path/id collision
- no undeclared alias engines
- every listed capability has a declared target entrypoint and at least one real authoritative body, or `## Capabilities` contains exactly `none`
- every PC fact/value was supplied or explicitly accepted; deferred and intentionally unspecified fields remain labeled rather than inferred
- any unresolved ENGINE-required character field is explicitly deferrable **and not required by the accepted starting scenario's intended mechanics**, or bind stops
- the ENGINE declares an exact supported `character_build_support` value; setup has not claimed a procedure or sheet capability beyond it
- persona/background text grants no standing permission to author the PC; PC current status agrees with T0
- `CHAR/PC.md` is either one body or a machine-marked index whose exact transitive targets stay under `CHAR/`; no unrelated sibling is included
- detailed construction covers only selected domains, and each complex capability passes a representative need → entrypoint → exact target → stop route rehearsal without discovery
- phase/clock/faction/seed/resource/rule material, if selected, has the authority and lifecycle required by `ADMIN/CAMPAIGN_BUILD.md`; every private system that may need a later cross-boot cue has the optional field reserved, every initially implicated system that cannot otherwise be recognized has one compact nonsecret T0 cue, and every interaction plan applies each cause once
- every accepted mutable-system authority stores its own triggers/non-triggers, selected current-state route, cue lifecycle, and interaction edges/order; the proposed manifest only mirrors these declarations and is not persistence
- private truth, if selected, is reviewed, operator-constrained sealed, or deliberately unfixed; the accepted envelope cannot manufacture PC agency, safety, or mechanics
- starting scenario has no authored PC first act
- SAFETY sentences vs safety_state match

Then write files. If an accepted engine exists only as the in-memory draft, write and validate that exact compact engine before writing the module or binding; do not substitute or expand it after acceptance. Initialize the canonical empty NOW, KNOWN, CAST_STATUS, and CORRECTIONS templates. Stable subsystem definitions and accepted as-of-T0 snapshots stay in declared MODULE bodies; do not bulk-activate them in INSTANCE. Copy the exact accepted PC route closure to matching paths under `INSTANCE/CHAR/` at bind. Point `pc_record` to `INSTANCE/CHAR/PC.md`.
Assign a new unique portable `campaign_id` for this run and a new safe `save_id`. Write the complete candidate CURRENT_SAVE with `save_rev: 1`, `save_parent: none`, `commit_kind: bind`, `archive_ref: none`, the accepted safety flag, and every required present field compiled from T0. Validate the completed candidate against INSTANCE/_SCHEMA.md; if it fails, keep the prior unbound save authoritative. Replace CURRENT_SAVE last and confirm both ids.

If any file write, provider response, or generation is interrupted before CURRENT_SAVE replacement, the unbound save remains authoritative but the folder may contain partial ENGINE/MODULE/SAFETY/INSTANCE/candidate artifacts. Do not call them committed and do not start PLAY. Either complete only the already accepted manifest and validate the entire bind, or inspect and restore the clean pre-bind copy required by P19 before retrying. Do not improvise missing sealed/private content, silently delete evidence, or claim automatic rollback.

## After commit

Start PLAY in a **fresh** chat.
Resident payload: LAW + new CURRENT_SAVE.
First fiction: T0 immediate_scene only (the accepted jump-start), plus POLICY voice and POLICY safety extras.
Do not add a second hook because SETUP drafted unused alternatives. Unused proposals die with the interview chat.

This clean kit has no pre-authored world. New Game is how a campaign is born.
