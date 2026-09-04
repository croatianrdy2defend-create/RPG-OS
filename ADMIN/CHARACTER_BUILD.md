# SETUP — Character Build

Operator-side character construction. Not PLAY. Not fiction. Nothing here is canon until explicit ACCEPT and ADMIN commit.

Open this file only when NEW GAME reaches the character-building choice. A complete mechanical sheet is optional. A substantive, operator-approved `CHAR/PC.md` baseline is required so the bound `pc_record` is never an empty placeholder.

## Choose profile depth and sheet path separately

Ask both questions even when the operator has already supplied a character concept.

**Character/profile detail:**

1. **Quick** — concept, agency boundary, starting facts, and intentionally unspecified facts.
2. **Standard** — add only the most useful identity, background, capability, persona, obligation, resource, and status cues.
3. **Detailed** — work through operator-selected profile sections one small cluster at a time.
4. **Custom** — operator names the sections and depth independently.

**Mechanical sheet:**

1. **No full sheet now** — keep mechanics deferred except any nondeferrable ENGINE minimum.
2. **Minimum required** — complete only fields the selected or in-memory draft ENGINE requires for bind or the opening's intended mechanics.
3. **Guided full sheet** — follow the selected or in-memory draft ENGINE's declared field groups step by step.
4. **Import and review** — preserve an existing sheet, check it against the selected or in-memory draft ENGINE, and ask about conflicts or missing required fields.

The choices are independent: a detailed persona can use deferred mechanics, and a complete mechanical sheet can use a quick profile. Any optional section may be skipped. Missing facts remain unspecified; SETUP does not fill a template by inference.

They are also independent of the Campaign Contract. Its initiative, pressure, development priorities, guidance setting, or creative mandate cannot choose character depth, complete a sheet, supply persona, or authorize PC conduct. Character choices do not silently recalibrate those campaign settings.

Before optional profile work, show the profile-pass headings below and ask which to build now, add as custom, or leave unspecified. Do not walk unselected passes. After each selected pass, offer revise / next selected pass / stop.

## Always establish

Every path establishes only operator-supplied or explicitly accepted material:

- a concise character concept and role;
- facts required to understand the T0 body/state and immediate situation;
- the authorship boundary: the player owns voluntary PC acts, words, thoughts, emotions, attraction, consent, commitments, purchases, risks, messages, and conduct;
- any ENGINE-required fields needed before the chosen kind of play can begin, or an explicit statement that those fields are deferred;
- intentionally unspecified facts where omission matters.

Quick profile detail stops here unless the operator asks for more.

## Optional profile passes

For Standard, Detailed, Custom, or a requested review, offer only relevant passes and ask one small cluster at a time:

1. **Identity and presentation** — name, pronouns, age where relevant, body/appearance, culture, languages, and public presentation.
2. **Background and role** — origin, training, work, social position, affiliations, important history, and limits on what that history grants.
3. **Capabilities** — competencies, weaknesses, powers, equipment access, and areas deliberately left unknown.
4. **Persona cues** — player-authored values, goals, habits, tastes, fears, flaws, boundaries, and portrayal cues.
5. **Connections and obligations** — only relationships, dependents, duties, debts, appointments, or commitments the operator establishes.
6. **Resources and possessions** — only at the campaign's chosen accounting precision; distinguish owned, stored, carried, equipped, available, owed, and estimated.
7. **T0 status handoff** — health/condition, location, schedule, active effects, exact player-declared goals, and other facts actually needed for the opening. Put immediate location, appointments, `pc_declared_goals`, and other mutable present facts in `T0_SAVE.md`/CURRENT_SAVE, not redundantly in the stable PC baseline. Only sheet-owned mechanical condition belongs in `CHAR/PC.md`, and its current value must not compete with another authoritative total.
8. **Intentionally unspecified** — facts that should remain open rather than being completed for neatness.

Persona is descriptive input from the player, not standing permission for the GM to author the PC. A listed goal does not choose the next action. A preference does not create attraction or consent. A possession is not automatically carried, equipped, consumed, or used.
A PC-declared goal and an OOC campaign preference are different claims: preserve the former exactly in the PC/current-state lane and the latter only in the accepted Campaign Contract or provisional REVIEW lane. Never infer either from observed conduct.
A behavioral disadvantage, compulsion, self-control value, alignment, drive, or similar mechanic may establish a trigger or involuntary mechanical consequence only as the ENGINE permits. Accepting it never delegates the PC's voluntary conduct, interpretation, dialogue, attraction, consent, or decision.

## Engine-aware sheet procedure

For Minimum required, Guided full sheet, or a mechanically complete import:

1. Open only the selected ENGINE's character-creation/field-group section, or use the accepted in-memory draft if the engine file has not yet been written.
2. State the build method or budget only if the ENGINE or operator supplies it.
3. Distinguish **required before bind**, **required only when that subsystem enters play**, and **optional** fields.
4. Show the declared field groups and their required/deferred/optional status, then work through one selected or required group at a time. After each group offer revise / next / skip if permitted / stop as partial. Offer choices as proposals, never silent selections.
5. Derive a value only when both the procedure and its inputs are present. Show the derivation compactly when it matters.
6. Do not reconstruct missing commercial rules, costs, tables, lists, or chapters. Ask the operator to provide the value, consult an owned source, import a sheet, choose another engine, or defer the field.
7. Finish with an audit: supplied facts, accepted proposals, derived values, required unresolved fields, optional deferred fields, and intentionally unspecified facts.

No campaign promise, fit judgment, initiative setting, or creative mandate can supply a missing ENGINE value or substitute for the engine's character procedure.

An incomplete sheet may bind only if the ENGINE permits those missing fields to be deferred. If later adjudication requires a missing value, pause and ask; never guess it.

## Import rules

- Preserve supplied values and wording unless the operator accepts a change.
- Flag contradictions, duplicate totals, unclear editions, and missing ENGINE-required fields.
- Do not silently rebalance, optimize, normalize, or complete the character.
- Treat external sheets and rule text as operator-provided reference, not permission to copy a rulebook into ENGINE or MODULE.

## Draft output

Before returning to NEW GAME, show:

- character/profile depth and mechanical-sheet path;
- sheet state: `not built/deferred`, `minimum`, `complete`, `imported`, or `partial`;
- required unresolved fields, if any;
- intentionally unspecified areas;
- proposed `CHAR/PC.md` section outline and storage shape: `ONE AUTHORITATIVE BODY` or `ROUTED SHARDS`;
- if routed, the exact transitive bundle beginning at `CHAR/PC.md`, with every target under `CHAR/`, no unrelated siblings, and one representative listed-value route rehearsal;
- mutable T0 facts handed back to NEW GAME for `T0_SAVE.md` rather than duplicated in the baseline.
- exact player-declared goals handed to `T0_SAVE.md` as `pc_declared_goals`; OOC development preferences remain outside the PC record.

Use one cohesive `CHAR/PC.md` while its material is normally retrieved together. If sheet mechanics, persona/background, or resource records are materially independent retrieval units—or a whole-file test shows leakage—`CHAR/PC.md` may instead be a compact routing index with scalar front matter exactly `class: character-routing-index`, pointing to narrow Markdown bodies under the same `CHAR/` tree. Do not shard merely because Detailed was selected. Indexes locate values and do not duplicate them.

Do not write the file here. NEW GAME includes it in the proposed manifest, and only explicit ACCEPT authorizes the ADMIN commit.
