# SETUP — Campaign Build

Operator-side world and campaign-system construction. Not PLAY. Not fiction. Nothing here is canon until explicit ACCEPT and ADMIN commit.

Open this file only when NEW GAME's world/campaign-depth choice requests more than the sparse runnable core. It is a menu, not a questionnaire quota. Ask one selected domain at a time and omit the rest.

## Depth means selection, not volume

- **Sparse** — premise, opening place, required policy, PC baseline, T0, and starting situation only. Do not open this guide.
- **Focused** — build only selected facts and systems likely to matter near the opening.
- **Detailed** — develop selected domains step by step, including their causal operation and retrieval routes.
- **Custom** — the operator names domains and desired granularity independently.

Detailed does not mean encyclopedic. It does not authorize filler, mass NPC rosters, empty directory trees, or a larger resident PLAY payload. A domain not selected remains absent, provisional, or intentionally unfixed.

## Ask four independent calibration questions

Do not let one answer silently control all four:

1. **World detail** — sparse / focused / detailed / custom.
2. **Campaign dynamics** — none beyond ordinary causality / selected systems / detailed interacting systems / custom.
3. **Bookkeeping** — abstract / selective / exact in named areas / custom.
4. **Rule calibration** — engine as written / selected clarifications / explicit variant / custom.

## Common design record

For each selected domain or subsystem, establish only what is useful:

- purpose and scope;
- stable public baseline, private truth, provisional elements, and intentionally unfixed areas;
- what can change and which causal events change it;
- whether it is definition-only, dormant at T0, or initially implicated;
- current-state authority after the first causal change;
- visibility to the PC/player;
- what does **not** activate, advance, or imply it;
- retirement or resolution condition, if any;
- the smallest useful retrieval route.

Do not force every field onto every domain. Unknown remains unknown.

The accepted authoritative MODULE body for each mutable system stores the operational declarations needed after the SETUP chat is gone: stable id, as-of-T0 classification/snapshot where present, causal triggers and non-triggers, selected post-change current-authority route, cue lifecycle when applicable, and any cross-system edges/order it owns. Put public and private declarations in the appropriate declared capability and use explicit routes between them; do not duplicate the same operational rule in several bodies. The proposed manifest mirrors these declarations for operator review only. It is not runtime authority and disappears with the disposable setup chat.

## Domain-selection gate

Before any optional pass, show a compact menu of the pass headings below and ask the operator to select the domains to build now, add a custom domain, or stop with the focused material already chosen. Record the selection in the draft. Do not walk an unselected pass. After each selected pass, allow revise / next selected domain / stop. “Detailed” increases depth inside the selection; it never selects all domains automatically.

## Optional authoring passes

### Campaign topology and time

Choose, if useful: episodic, sandbox, arc/phase, or hybrid; mostly emergent or with a fixed broad trajectory; expected time scale; routine-compression preference; incident density; quiet-day permission; and how ordinary life relates to the main premise.

A broad trajectory may be fixed while timing, particular events, responsible actors, PC involvement, and outcome remain unfixed. OOC intent frames possibilities; it does not guarantee scenes.

### World model

Select only relevant areas: geography, history, cultures, bodies/material accommodations, technology or magic, law/civil status, households/kinship, economy, institutions, politics, ordinary life, public knowledge, private truth, and deliberate unknowns.

Separate tradition, stereotype, public belief, private truth, and individual fact. World categories never dictate a person's morality, politics, sexuality, relationship structure, or conduct unless the operator explicitly establishes a narrower fact for that individual.

When private authoring is selected, choose one disclosure mode for each private domain:

1. **Reviewed exact draft** — show the proposed exact private facts OOC and require explicit acceptance.
2. **Operator-constrained sealed generation** — before ACCEPT, agree the domain, permitted fact classes, safety boundaries, exclusions, and the exact authority being delegated. After ACCEPT, ADMIN may write a bounded private body without quoting its contents into chat. This is not encryption or isolation from the host or filesystem operator. If the host cannot write without echoing the body, use reviewed or unfixed instead. Sealed generation may not establish the PC's voluntary history, acts, thoughts, feelings, attraction, consent, commitments, safety choices, or mechanical values.
3. **Deliberately unfixed** — leave the truth open until an authorized causal process establishes it.

The manifest records the mode and route, never a sealed secret's contents. For sealed material, filenames, directory names, heading ids, index labels, routing gists, and other metadata must also be non-revelatory; use opaque stable identifiers where necessary because AUDIT and VALIDATE may report paths. Material outside an accepted envelope stays unfixed. A sealed body becomes canon only after the operator accepts the envelope and the ADMIN commit succeeds.

### Phases, arcs, and changing conditions

A phase is an operating condition, not a chapter or mission list. For each phase used, define:

- the condition of the world or affected area;
- the kinds of situations that condition enables;
- causal transition conditions, plus what signs (if any) are observable;
- what persists from earlier life;
- whether different places, institutions, or factions may occupy different conditions at once.

Never assign the PC's allegiance, response, or required task. Never advance a phase merely because a planned scene or session was completed.

POLICY contains only present-facing cadence, tone, genre boundaries, and any broad trajectory disclosure that genuinely must shape every scene. Do not put detailed future phase definitions or private transition logic there: POLICY is opened for first fiction and would make them permanently hot. Put public phase machinery behind the declared CLOCKS capability or private causal phase truth behind TRUTH, and move changed state through its selected current authority (normally NOW for detailed state). A single current phase needed on every resume may instead be a compact `declared_state_flags` value in CURRENT_SAVE; do not duplicate that same current value elsewhere.

### Clocks, fronts, pressures, and tracks

For each selected tracker, define:

- scale and initial value;
- scope and visibility;
- what any endpoint or threshold means, if one exists;
- causal advances;
- causal resistance, reduction, or reversal where applicable;
- what does not move it;
- resolution/retirement behavior.

Elapsed time may move a tracker only when elapsed time is itself an explicitly declared cause. Session endings, retrieval, dramatic convenience, and PC inattention do not tick it automatically. A tracker is not a morality meter unless explicitly designed as one.

### Autonomous people, factions, and institutions

Develop only actors whose independent existence matters. Useful dimensions include role/scope, goals, resources/capacity, constraints, pressures, knowledge and wrong suspicions, values/boundaries, ordinary schedule, internal disagreement, vulnerabilities, and how matters can progress or resolve without the PC.

Also record what an institution or actor is **not** when genre assumptions would otherwise inflate it. Existence does not make an actor hot, scheduled, allied, hostile, or romantically relevant.

For each authored person who may be named in CURRENT_SAVE or receive an overlay, assign one stable portable `person_id`. The PEOPLE route, `hot_identifiers`, and future `INSTANCE/PEOPLE/<person_id>.md` must use the same id. Use an opaque non-revelatory id when necessary, and do not create mass ids or person stubs.

### Seeds and possibilities

A possibility body may define contact conditions, fixed or deliberately unfixed truth, stakes, useful capabilities, independent resolution, dependencies, constraints, and possible tracker effects.

Seeds are inactive by default. They are not quests, promises, a required sequence, or PC knowledge. Drafting, indexing, or retrieving one never activates it. Do not choose the most dramatic explanation merely because it exists.

### Relationships and social structures

Track only established dimensions relevant to the relation. General dimensions may include relation kind, power or authority, trust, obligation or debt, affiliation or allegiance, reputation, dependence or care, rivalry, kinship or mentorship, access, boundaries, and public/private presentation. For intimate or domestic relations, attraction, orientation, availability, sexual exclusivity, romantic exclusivity, disclosure, residence, finances, parenting, and legal status remain separate facts. Do not collapse them into a single relationship score.

No subsystem may automate the PC's attraction, consent, attachment, jealousy, commitment, or response. NPC choices remain individual and causal; dice do not manufacture relationships.

### Resources, economy, logistics, and calendar

Choose the precision by domain:

- **abstract** — only materially limiting categories;
- **selective** — exact for named consequential resources, abstract elsewhere;
- **exact** — explicit accounts, quantities, locations, due obligations, acquisition, consumption, loss, and transfer in selected areas.

Exact values remain exact; estimates remain estimates. Choose one current authority for each detailed total. If CURRENT_SAVE owns a selected hot total, another body may store nonduplicating components or a pointer but not a second total. If the PC overlay or an explicitly routed INSTANCE body owns the total, CURRENT_SAVE carries only a nonconflicting resume cue or pointer when needed. Do not keep competing totals.

Ownership never implies carried, equipped, consumed, transferred, or used. Routine compression reconciles only conduct the player declared or previously established.

### House rules and campaign calibration

Classify every proposed rule before writing it:

| Kind | Authority/home |
|---|---|
| voice, cadence, genre boundary, module-imposed stronger content restriction | `POLICY.md` |
| operator/run-specific Hard-no or Fade/veil sentence | `INSTANCE/SAFETY.md` + `safety_state` |
| campaign-specific interpretation or hook that does not contradict ENGINE | `RULES_HOOKS` capability |
| changed resolution procedure, character rule, or other real ENGINE override | a distinct compact ENGINE id selected by the module |
| later explicit table ruling or correction | `INSTANCE/CORRECTIONS.md` |

Do not hide an ENGINE contradiction in lower-authority MODULE text. A derived engine stays procedure + field groups only; it does not copy a commercial rulebook. If the needed rule is unavailable, ask the operator for the procedure or value.

If this classification creates a distinct ENGINE after the initial engine question, pause campaign authoring and return to engine/character setup. Recheck character field requirements, calculations, T0 engine binding, RULES_HOOKS compatibility, and the manifest against the new id before proposing the starting scenario or ACCEPT. Never change the engine id as a silent late patch.

Useful optional calibration areas include when to resolve, task scope and retests, consequences, complementary actions, perception/evidence limits, social-result bounds, self-control triggers, exertion, advancement, combat clarity and aftermath, and resource handling. Add only actual campaign choices, not a generic rules catalogue.

### Visual authority

If VISUAL exists, state what each reference establishes. Images may establish appearance, layout, object, costume, or atmosphere. They do not silently establish personality, politics, orientation, mechanics, relationship, attraction, consent, or narrative importance.

## Starting-state dependency audit

Before the starting scenario is proposed, trace material T0 changes through their dependencies. A change in date, place, body, job, affiliation, resources, or campaign condition may require reviewing appointments, pay, travel, contacts, inventory, known facts, clocks, institutions, and the opening situation. Do not patch one field and leave contradicted dependents behind.

Stable definitions and immutable **as-of-T0 snapshots** live in declared MODULE bodies. They do not assert that their mutable values remain current forever. INSTANCE registers remain canonical empty at bind. A current value may follow from established continuity with one specifically named T0 snapshot only when no selected current authority or accepted current-chat transition supplies a later value and no declared causal transition has occurred or is due. PLAY keeps accepted changes in chat RAM and writes nothing. At the next explicit CHECKPOINT/CLOSE, a system whose selected authority is NOW materializes complete as-of-now status in an explicit `INSTANCE/NOW.md` route/shard and applies unsaved transitions once; a CURRENT_SAVE-owned value changes only in the candidate, and a PC-owned value changes only in its INSTANCE PC bundle. From that point the MODULE snapshot answers only “at T0”; the selected route answers “now,” so they are never competing current authorities. Do not initialize every seed, clock, faction, or person merely because its body exists.

For every mutable subsystem, label the T0 state as **definition-only**, **dormant**, or **initially implicated**. An inactive possibility remains inactive. If an initially implicated private system could not be recognized later from the immediate scene, open matters, appointments, or another already-resident fact, add one compact nonsecret routing cue to T0 `declared_state_flags`: stable system id, the causal/due-check condition, and the declared capability/section route. The id and route are themselves non-revelatory; use an opaque stable id and neutral filename when a descriptive name would expose the secret. Do not put the hidden value, outcome, actor, or other lore in the cue. A cue permits a bounded check when its condition exists; it does not make the system hot, reveal it, activate it, or tick it. Dormant and definition-only systems receive no resident cue merely because they exist.

If the selected campaign contains a private mutable system that may later become independently live, include `declared_state_flags` in T0 even when its opening value is `none`; this reserves the existing optional field without making a watcher active. At each CHECKPOINT/CLOSE, add or update a cue only when such a system remains causally live across fresh boot and no immediate scene, open matter, appointment, or other resident fact makes its bounded check discoverable. An initial cue may route to its declared MODULE snapshot; after current state materializes, update the cue to the selected current INSTANCE authority. Remove/demote the cue when the system retires or another resident fact supersedes it. Never retain a stale MODULE route to answer later current status.

## Cross-system interaction audit

For detailed interacting systems, trace each accepted initiating cause through a bounded update plan:

1. name the one established source event or condition;
2. list only the records and selected current authorities it can affect;
3. distinguish required effects from conditional checks;
4. declare update order where one result is an input to another;
5. apply the source event once, then write each resulting current value once;
6. record the causal event once in the archive when CLOSE preserves it.

No implicit cascade, circular trigger, or double tick is allowed. A phase or threshold may enable new conditions, but it does not force a scene, mission, PC act, allegiance, or outcome. If two rules would apply the same cause twice, or a cycle has no explicit stopping rule, revise the design before ACCEPT.

## Retrieval-locality preflight

For every selected capability:

1. Keep one cohesive body if its contents are normally retrieved together.
2. If materially independent subjects will be queried separately, create a compact declared `INDEX.md` and narrow authoritative bodies or sections.
3. Use a heading fragment only when the surrounding file is safe and cohesive enough for the host's retrieval behavior; physically split unrelated PRIVATE subjects.
4. Keep cross-links sparse and need-driven.
5. Rehearse at least one representative question as: need → declared entrypoint → exact file/heading → stop. Do not use `find`, `ls`, or sibling browsing to make the route work.

A broad-category index that merely points to another multi-subject monolith has not improved retrieval locality.

## Draft output

Return to NEW GAME with a proposed manifest that labels each optional domain:

- `OMITTED` — no capability/body exists and PLAY treats it as absent
- `INTENTIONALLY UNFIXED — <authority route>` — the authoritative body preserves that a named fact is unfixed
- `ONE AUTHORITATIVE BODY`
- `ROUTED SHARDS`

For mutable systems, also identify the immutable as-of-T0 MODULE snapshot and intended INSTANCE current-state route. Record reviewed/sealed/unfixed private-truth mode without disclosing a sealed body, any compact T0 watch cue, and the explicit interaction/update order. Confirm that each accepted operational declaration will live in exactly one routed MODULE authority; the manifest only mirrors it and is not persistence. List unresolved contradictions and dependencies. Do not write files here; explicit ACCEPT in NEW GAME authorizes the ADMIN commit.
