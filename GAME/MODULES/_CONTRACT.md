# Module contract — v0.8.2

A module supplies a reusable world, opening baseline, character baseline, and any selected reference depth. It does not accept a run agreement or activate its own prepared material.

## Required new-module files

| Record | Purpose |
|---|---|
| MODULE.md | identity, engine binding, declared capability routes |
| SETTING_BRIEF.md | compact stable public orientation |
| POLICY.md | setup-only voice, campaign defaults, source expectations, proposed extra limits |
| CHAR/PC.md | substantive accepted character baseline or exact routed bundle |
| T0_SAVE.md | accepted opening template for a new run |

A complete mechanical sheet is required only where the selected engine/opening needs it. A PC may be nonhuman, collective, or another playable viewpoint. Its profile does not grant GM control.

CHAR/PC.md is one body or an index with scalar `class: character-routing-index`. Its exact transitive Markdown targets stay under the same CHAR tree. Do not include unrelated siblings; `CHAR/README.md` is reserved for the INSTANCE guide. At bind copy this exact bundle to INSTANCE/CHAR; there is no later fallback from the current PC record to the module baseline.

## Setting Brief

Use exactly this scalar front matter, substituting the module id:

```yaml
---
id: <module>.setting_brief
class: setting-brief
---
```

No other front-matter fields. Use these exact once-only headings in this order:

```markdown
## World identity
## What is ordinary
## Available depth
```

**World identity** gives the public premise, original/historical/source-bound/hybrid basis, relevant reality or era, and opening operating scope. Do not force a chronology or a whole world survey where neither matters.

**What is ordinary** gives useful public priors, meaningful distribution/variation, and the few generic model assumptions that would distort portrayal. Qualitative prevalence is sufficient. Local scenes need not display every category. Category membership alone is not an individual biography; explicitly established physical, social, or collective facts may constrain behavior without importing generic stereotypes.

**Available depth** states what the brief supports inventing and which concrete facts/procedures require existing cold authority. For each cold domain name its trigger and matching declared capability token. Do not include body filenames, detailed payload, or a compulsory reading list; do not promise absent sources.

When a module prescribes a guide for focused physical portrayal, its trigger includes the first focused description covered by that guide. Advertise this through the matching capability and retain the exact guide route in the descriptor/entrypoint. Compatible anatomical facts in the brief do not replace the guide's applicable portrayal instructions. Verify the route at setup; during PLAY reuse loaded guidance within its sufficient coverage.

Keep the brief concise and stable across scenes. No named cast roster, current mutable state, private truth, prepared possibilities, clock/phase bodies, plot summary, or future schedule. Specific exact, local, disputed, quantitative, private, or causally material facts remain in narrow reference bodies. Open areas remain open to accepted invention. A later current record outranks a stale mutable claim accidentally left in the brief. Reading it creates no event.

## POLICY is setup-only

New POLICY files retain `## Voice` and `## Campaign defaults`. Voice proposes portrayal; Campaign defaults proposes the five run-agreement areas:

- Campaign promise, fit, exclusions, source/fidelity expectations, and `Play form:`.
- Player control, proposed routine grants, and `Retcon:`.
- GM initiative: permitted kinds, conditions, obligations, limits, and `Form selection:`.
- Time and transitions: declared-sequence continuation, stopping points, and `Cuts:`.
- Presentation: voice, dialogue/narration balance, guidance, status display, and `Structure disclosure:`.

These are plain-language proposals, not axis enums or a second rule engine. New/bound v0.7.1-and-later agreements require each named clause once, with substantive free text, in its assigned section. NEW_GAME supplies their proposed defaults; acceptance remains run-specific and requires no additional questionnaire or mandatory A-E label. No retired creative-mandate scalar or review-mode field is required. Detailed machinery belongs in capabilities.

Form selection and permission to withhold structural selection are separate grants. Default general form is known while plot remains hidden; optional opacity records its true selection/disclosure envelope without forcing a concealed choice into the review, metadata, or a false form claim. Defaults preserve lived continuity with declared/delegated routine compression; hardcuts need bounded permission. Retcon defaults to OOC rewind, with optional ironman for valid outcomes and distinct error/depiction/stop handling. Existing v0.7 agreements missing clauses use focused accepted RECALIBRATE supplementation, not implicit defaults or state migration.

Accepted fixed destinations/outcomes are allowed within scope, without fake open rolls or overwritten reserved PC decisions. Optional seeds remain candidates; a specifically accepted structural obligation has its own governing authority. Off-premise choices require an OOC return, recalibration, or ending rather than invented physical impossibility or compulsory NPC authority.

At NEW GAME/LOAD, copy accepted operational clauses and voice into CAMPAIGN_CONTRACT. Every fidelity/source constraint affecting PLAY belongs in that agreement/brief or a real source-authority body reached by an exact contract/descriptor route, never solely in POLICY. The brief still uses domain/trigger/capability wording rather than body filenames. Copy accepted stronger module limits into SAFETY under canonical labels, with their origin labeled. Actual acceptance is required; defaults never become active by loading. Ordinary PLAY does not load POLICY. A legacy module's missing POLICY/defaults can be supplied in the reviewed run proposal without modifying its source; new authored modules still include POLICY. If no voice was supplied, offer the concrete-prose default in NEW_GAME for acceptance.

## Descriptor and route grammar

Preserve the v0.4 descriptor grammar. MODULE.md begins with simple scalar front matter: `id`, `title`, `engine`. Module id matches its directory. Safe ids contain ASCII letters, digits, `.`, `_`, `-`, begin with a letter or digit, and contain no separators/traversal.

Use exactly one `## Capabilities` section. With no optional bodies, its body is exactly `none`. Otherwise:

```markdown
| capability | entrypoint |
|---|---|
| WORLD | `WORLD/INDEX.md` |
```

Use outer pipes and one contiguous row block. Allowed capabilities are `WORLD`, `PEOPLE`, `INST`, `SEEDS`, `CLOCKS`, `TRUTH`, `VISUAL`, `RULES_HOOKS`. Entrypoints are POSIX-style paths relative to the module: no absolute path, backslash, dot/traversal segment, or symlink route.

An entrypoint is a real authoritative body or routing index leading to real bodies. Empty indexes do not establish a capability. Use `INDEX.md` for an index, or scalar `class: routing-index` (including namespaced classes ending in `-routing-index`) for another filename. Explicit targets are backticked relative Markdown paths outside fenced examples, relative to the index directory. Internal `..` may cross-link only within the same module; no escape, absolute path, backslash, `.` segment, empty segment, or symlink. A fragment names literal heading text and resolves exactly once.

Legacy prose descriptors remain readable but structurally INCOMPLETE until explicitly mapped/converted; manual checks do not turn script omissions into script PASS.

## Locality and optional depth

Keep related material together. Split independently retrieved subjects when useful, using a compact index with exact targets and just enough selection metadata. Do not split to hit a word quota, build empty hierarchies, duplicate body content in indexes, or require broad discovery at play time.

Typical homes: public world in WORLD; actors/institutions in PEOPLE/INST; candidates in SEEDS; public conditions/tracks in CLOCKS; hidden facts in TRUTH; compatible mechanical clarifications in RULES_HOOKS. A real engine override requires a distinct engine id. Later table rulings live in INSTANCE/CORRECTIONS.md.

Independent-agent establishment uses the [Initial Encounter Baseline](../OS/AGENT_STATE.md#initial-encounter-baseline) and its active-participation lifecycle. The five mandatory current fields are **Condition and mode; Priorities and constraints; Perception and appraisal; Attraction; Engagement stance**. MODULE supplies capacities, senses, drives/directives, control and meaningful variation; OS requires the basis before individual participation, appraisal or initiative; ENGINE governs generation and resolution. Visual focus alone triggers relevant portrayal sources without a private baseline. Hard limits, group tendencies and individual facts keep their separate scopes. These fields impose no universal human psychology.

Bind one compatible default generation procedure and necessary opening exceptions through NEW_GAME/LOAD. Put its usable sources, mappings and scope behind existing engine/module routes. Cover all five current fields and lifecycle, not merely a baseline enable flag. Nature, control and known identity constrain temporary generation; no enduring trait draw is compulsory. Overall attraction can be negative, absent or positive, with meaningful subtypes resolved later as needed. Existing subtype-specific facts remain binding. Actual absence, supported inapplicability, insufficient perception, protected unknowns and missing required sources remain distinct; duty or partnership alone does not erase applicable attraction.

Where material, identify the actual decision owner, local discretion, communication scope/delay and supported control transitions. Shared control does not imply unlimited knowledge. Keep its governing state once with relevant local differences. Independently minded groups may share orders and coordinated conduct without sharing a personality or attraction. Shared conduct needs its applicable common basis; an individual appraisal or discretionary decision triggers individual establishment. Independently deciding entities require separate baselines even when they share a place or task. Inherit applicable established shared facts without manufacturing a common mind, and establish eligible individual gaps before their dependent response rather than backdating them to a group sighting.

A compatible generation hook identifies its admissible inputs, context, eligible dimensions, hard exclusions, dependencies, outcome meanings, actual random-input method and result scope before use. Existing facts constrain draws, and derived dimensions account for their established inputs instead of independently contradicting them. Select subjects from actual world facts and circumstances before selecting their portrayal references. Example frequency, reference availability and document order are not population weights; established demographics and local variation remain effective without equal quotas. Cultural guidance retains its community and individual scope. Prior causal history involving the PC may constrain generation; unverified impressions, unperceived wishes, preferred partner traits and desired scene outcomes do not supply population or private state. The engine owns resolution; POLICY alone cannot install operative rules. Retain actual inputs/results and accepted generated facts in their proper owners, not an unexecuted seed as though it were a person. No module promises concealed durable state without the host's actual retention and visibility support.

Private filenames, headings, ids, index gists, and watch cues must be non-revelatory when secrecy matters. Separate unrelated private subjects when whole-file reads would expose them. This is spoiler hygiene, not encryption or guaranteed host secrecy.

Rehearse one representative need → declared entrypoint → smallest sufficient body → stop lookup for every complex capability before bind. A pointer is a route, not an instruction to read everything linked.

The shared bind verification also exercises the selected encounter method once with a synthetic individual and an applicable coordinated group. Check the individual's five current fields before its response and the group's shared-state/individual-decision boundary using the actual methods and source routes. Reuse a matching rehearsal from the same setup; this contract adds no separate round. Keep test actors and events out of module T0 and campaign history, retain actual observations and coverage limits in the bind verification, and distinguish an executed rehearsal from an unrun case or static route check. A successful example is evidence for that example, not proof of general model reliability.

### Optional portrayal and investigation notes

The optional preparation principles in `ADMIN/CAMPAIGN_BUILD.md` apply at selected depth. Worked examples are retrieved separately from `https://github.com/croatianrdy2defend-create/RPG-OS/blob/main/DOCS/ADMIN/PORTRAYAL_EXAMPLES.md` only when an example is needed. These notes are optional prose inside existing authority, not new capabilities, required headings, tables, or files. They add no automatic startup load or requirement to complete an existing campaign retrospectively.

A recurring person's stable portrayal anchor belongs with their PEOPLE baseline during setup or, for an emergent person, their established INSTANCE record. It may give a useful priority, expression sample, constraint, or pressure response without a mannerism quota. For nonhuman or controlled entities, use only applicable expression and decision mechanisms, not a human personality template. An expression sample does not reverse-establish its private cause. Current motives, relationships, and resources retain their selected current owner; the anchor links rather than duplicating them. Samples are illustrative unless they quote an actual sourced exchange. They grant no new actions, knowledge, or PC authority. A bound MODULE remains immutable: derive a temporary reminder from existing content or persist an accepted change through its selected INSTANCE authority, rather than rewriting the baseline to add this aid.

A consequential hidden-fact note belongs with its existing TRUTH/WORLD/person authority. Distinguish fixed content, deliberate uncertainty, beliefs, and lies; identify relevant evidence paths when the accepted experience needs them. Later changes follow the selected INSTANCE authority, preserving what was said separately from what is established. Do not duplicate complete knowledge records or require every mystery to have a fixed answer or clue quota. Writing a proposal does not establish its truth, and REVIEW cannot turn an interpretation into canon. Private headings and routes remain non-revelatory where needed, within the host's actual disclosure capabilities.

## Opening template

New T0_SAVE uses the CURRENT_SAVE metadata table and five readable sections in `INSTANCE/_SCHEMA.md`. Set actual engine/module and canonical future `pc_record: INSTANCE/CHAR/PC.md`. Use `none` for campaign_id, save_id, save_parent, archive_ref, evidence_through; `save_rev: 0`; `commit_kind: unbound`; actual accepted safety_state, datetime, and place.

Its sections are **Situation; Character state; Open matters; Active processes; Relevant records**. They hold the accepted opening, relevant condition/resources, actual declared goals/obligations, due processes/non-revelatory private watch routes, and useful exact records. The PC's future INSTANCE route is created at bind. For systems and people not yet materialized in INSTANCE, save pointers target their existing MODULE T0 bodies; store the planned later INSTANCE destination inside the governing definition, not as an already existing save authority. Redirect the save pointer when the first persistent change creates that current record. Do not infer goals or PC participation. Legacy templates are mapped into an accepted bind draft without silently changing their source.

T0 may omit administrative Session continuity for legacy compatibility or contain `## Session continuity` with body `none`. It must carry no live session identity, feedback, adjudication receipts or runtime PREP from another run. Reusable opening facts are not a previous campaign notebook.

LOAD assigns unique runtime ids and bind lineage, preserves accepted opening bodies, and begins with `archive_ref: none` and `evidence_through: none`. It initializes CURRENT_SAVE's Session continuity independently to `none` and creates no PREP at bind.

Fixed opening agent state stays in its named MODULE T0 owner. Current PEOPLE/NOW/CAST_STATUS registers retain their empty bind convention; no new stance overlay is copied into INSTANCE merely by loading. Preserve existing-module bytes and fixed relationships. A genuinely unresolved dimension remains eligible only under its accepted future establishment path; no implicit run-specific randomized T0 override or nested bind/checkpoint is introduced.

## Mutable systems and people

MODULE definitions and mutable baselines are immutable as-of-T0 after bind. Authorized migration or Setting Brief upgrade/refinement may change only their explicitly approved surface; they do not silently rewrite world facts or history.

For each selected mutable system, store its id, accepted T0 status (definition-only/dormant/live), actual triggers/non-triggers, one later current-authority route, needed watch-cue lifecycle, and dependency/update order where relevant. Retain minimal source/acceptance provenance. A real session-boundary trigger identifies its selected engine/module procedure and resulting current owner; the generic session routine supplies no implicit tick, award or reset. POLICY can propose cadence defaults, but accepted runtime terms belong in the agreement. Static lore needs no lifecycle bureaucracy.

Current answers use accepted unsaved changes, then the selected INSTANCE record. A specifically identified T0 snapshot may support unchanged continuity only when no later transition is established or due; do not initialize everything. When due, resolve the relevant process from its governing state before answering its consequences. Reading a definition or ending a session does not change a system unless that is its declared trigger.

At SAVE/CLOSE or optional CHECKPOINT, carry accepted changes once to their selected authority: NOW entry/shard, CURRENT_SAVE section, person overlay, or PC record. The save's Active processes holds compact conditions and useful non-revelatory routes, not duplicate secret values. Retire or redirect stale cues. Optional REVIEW notes cannot activate a system or establish current facts.

Authored people may use `## CANON`, `## NOW`, `## PC`, `## PRIVATE`. CANON is stable baseline; NOW/PC and mutable PRIVATE are T0 snapshots. Use one safe stable person id in PEOPLE routing, relevant save references, and `INSTANCE/PEOPLE/<person_id>.md`. Keep a mature record together or narrowly routed according to retrieval needs.

On the first persistent change, a preauthored person's INSTANCE overlay owns the complete relevant enduring/consequential personal state and links to stable MODULE material. Temporary active fields belong to NOW's Active encounter state block, with exact references to any values already owned by the person/system record. Do not copy stable CANON or unrelated private lore, or mix older T0 values into a newer current answer. An emergent agent with continuing causal significance may have minimal established CANON and current state in INSTANCE with its route in CAST_STATUS, including a nonhuman individual. Shared controller state remains with its selected system owner. Do not promote every transient extra, infer a missing biography, or modify MODULE to store relationship progression.

Retain complete current encounter bases in NOW's optional `Active encounter state` block throughout active participation, with compact actual generation provenance, limitations and material changes. Entry presence means active; store no inactive registry. Durable personal/relationship facts stay in PEOPLE, shared control/system facts with their actual owner, and entries use precise references instead of duplicating those values. Update affected state through relevant events and time. Genuine deactivation releases inconsequential temporary values while retaining consequences and unresolved matters; later incidental contact may generate new temporary values constrained by surviving facts. Missing required active state is not expiry. Fixed MODULE T0 facts are not resampled by LOAD. PLAY remains read-only; authorized saves/handover preserve the complete current active state and surviving consequences, not expired trivia.
Reusable encounter mechanics belong to the selected ENGINE procedure; the module binds its applicable populations, sources and accepted settings. Keep local venues, role facts and current activities out of universal generation rules. A direction mapping is not a catalogue of world-specific states: the GM concretely fills eligible values at the stage the selected mechanic requires.
