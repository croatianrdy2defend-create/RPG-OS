# Module contract

The OS does not know any campaign’s filenames beyond this contract.

## Required

| Record | Purpose |
|---|---|
| `MODULE.md` | id, title, engine binding, capability list, pointers |
| `POLICY.md` | **Required voice declaration**; v0.6 campaign-default proposals; cadence, tone, genre anti-attractors, relationship extras, stronger safety |
| `CHAR/PC.md` | player character **baseline** |
| `T0_SAVE.md` | template ADMIN copies into a new INSTANCE |

`CHAR/PC.md` is always present as the stable PC entrypoint so the bound run has a stable `pc_record`; this does not require a completed character sheet. It may be one cohesive authoritative body or a compact routing index whose scalar front matter declares exactly `class: character-routing-index`. Every transitive target remains under the same `CHAR/` tree; subordinate indexes use the ordinary routing-index grammar below. `CHAR/README.md` is reserved for the INSTANCE distribution guide and is not a module shard. A minimal baseline may contain only operator-approved concept and starting facts plus clearly marked deferred or intentionally unspecified fields. Missing facts and values are never inferred. Persona entries are established facts or player-facing portrayal cues, not standing permission for the GM to author the PC's thoughts, feelings, words, choices, attraction, consent, or conduct.

The bound ENGINE decides which mechanical fields, if any, are required before bind and which may be deferred. If a later mechanic requires a missing value, PLAY pauses rather than guessing.

For a newly authored v0.6 module, `T0_SAVE.md` also supplies the opening `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier` fields required by the INSTANCE schema. `pc_declared_goals` contains only goals the player actually declared. `causal_frontier` contains only T0-established operative consequences, specific due conditions or obligations, live established processes, pending decisions, and non-revelatory routes to current state; use `none` when there are none. Reserve optional `declared_state_flags: none` separately when a selected private mutable subsystem may later require cross-boot discovery.

## Voice (required)

For v0.4-and-later authoring, `POLICY.md` must contain the exact level-two heading `## Voice`; its body declares the narrative voice. The OS does not supply a fallback. If voice is absent, PLAY must not start fiction. Report: module not runnable.

A pre-v0.4 module whose voice is clearly declared under another heading remains legacy-compatible, but VALIDATE reports that check as `INCOMPLETE` and noncanonical rather than silently pretending it matched the v0.4 grammar. Manual confirmation or descriptor-only conversion is required before claiming complete coverage.

## Campaign defaults (v0.6)

A newly authored v0.6 `POLICY.md` contains one compact exact heading `## Campaign defaults`. Its human-readable body proposes all of the following without turning them into front matter or a second rules engine:

- `campaign_promise` — what kind of play the module is offering, including material tone and cadence;
- `fit_envelope` — what belongs naturally, what would make this a different campaign, and material anti-attractors;
- six independent axes: `structural_direction`, `gm_initiative`, `pressure_incident_density`, `time_handling`, `development_priorities`, and `guidance_visibility`;
- `creative_mandate` — explicitly `off` by default, with `creative_mandate_scope: none` and `creative_mandate_boundaries: none`; or `on` with bounded kind-level scope and eligible scene/session/calendar boundaries in those two companion values;
- `review_mode` — exactly `off` or `bearing-only`; the latter permits an explicit REVIEW after successful PERSIST and an optional separately reported REVIEW after CLOSE.

Use the canonical Campaign Contract tokens defined by the INSTANCE schema so accepted values copy cleanly; a `custom: ...` value includes its short operator-approved text. Do not infer one axis from another. High pressure does not imply proactive initiative; a broad direction does not imply a plot; explicit guidance does not imply menus; and any setting may contain quiet, solitary, or no-change play.

These MODULE values are proposals only. They are never run acceptance, campaign fact, factual authority, external warrant, prepared content, or a scene/incident quota. At NEW GAME or LOAD, the operator accepts or revises a complete run-scoped contract in `INSTANCE/CAMPAIGN_CONTRACT.md`. PLAY uses that accepted contract, not a MODULE proposal, when judging creative authority. A legacy module without `## Campaign defaults` remains loadable when the operator supplies and accepts the complete run contract before PLAY; do not guess the missing settings from tone, genre, archives, or prior model conduct.

## Machine-readable descriptor (v0.4)

For deterministic validation, `MODULE.md` begins with simple front matter containing scalar `id`, `title`, and `engine` values. Its `id` equals the module directory name. New module ids are portable safe tokens: ASCII letters, digits, `.`, `_`, and `-` only, beginning with a letter or digit; no slash, backslash, whitespace, absolute path, or traversal segment.

It also contains one exact `## Capabilities` section. If no optional capability exists, its body is the single word `none`. Otherwise use this table:

```markdown
| capability | entrypoint |
|---|---|
| WORLD | `WORLD/INDEX.md` |
```

Machine-readable descriptor tables use outer `|` delimiters and one contiguous row block; do not hide a later row after a blank line.

Allowed capability names are listed below. Entrypoints are POSIX-style paths relative to the module directory: no absolute paths, backslashes, `.`/`..` traversal, or symlink routes.

When an entrypoint is a routing index, name it `INDEX.md`. A differently named capability map must declare scalar front matter `class: routing-index` (a namespaced value ending in `-routing-index` is also valid). Its explicit target files appear as backticked relative `.md` paths outside fenced examples. Those internal routes are relative to the index file's directory. They may use `..` only to cross-link within the same module; resolution outside the module, absolute paths, backslashes, `.` segments, empty segments, and symlink routes are forbidden. A `#fragment` names the literal target heading text, not a host-generated Markdown slug, and must resolve exactly once in that file. That gives VALIDATE a structural route to check; it does not let the script judge the truth or adequacy of the body.

Existing pre-v0.4 modules without this exact descriptor remain readable, but their module/capability result is `INCOMPLETE` until ADMIN converts only the descriptor. Never infer a SCRIPT-VERIFIED capability map from arbitrary prose.

## Optional capabilities

Declare in `MODULE.md` only what exists as a retrievable target entrypoint:

`WORLD` `PEOPLE` `INST` `SEEDS` `CLOCKS` `TRUTH` `VISUAL` `RULES_HOOKS`

An entrypoint may be one authoritative file or a compact, machine-marked routing index/capability map with explicit pointers to authoritative body files. `MODULE.md` names the entrypoint using the v0.4 table above.

For sealed/private material, filenames, directory names, heading ids, index labels, routing gists, stable ids, and other metadata must be non-revelatory because manifests, AUDIT, and VALIDATE may expose paths. Use opaque stable identifiers where necessary. This is salience/spoiler hygiene, not encryption or protection from the host/filesystem operator.

If omitted, the capability is absent. Do not invent it.
Do not declare a capability without a real body. An empty index does not make a capability present.

Campaign construction may be sparse, focused, detailed, or custom. Those are SETUP choices, not capability names and not permission to create every optional capability. Complex campaigns use the same declared capabilities; they add only selected authoritative bodies and current-state routes.

Typical placement:

| Material | Usual authority |
|---|---|
| voice, campaign-default proposals, cadence, current-facing phase/genre policy, anti-attractors, module-imposed stronger safety | `POLICY.md` |
| public world, geography, culture, economy, law | WORLD |
| institutions and factions | INST, with private causal truth in TRUTH where needed |
| stable people baselines | PEOPLE |
| inactive possibility bodies | SEEDS |
| clock/front definitions, public phase machinery, and accepted as-of-T0 snapshots | CLOCKS |
| hidden causal baseline | TRUTH |
| campaign calibration that does not contradict ENGINE | RULES_HOOKS |

RULES_HOOKS cannot silently override the higher-authority bound ENGINE. A genuine change to resolution or character rules must use a distinct compact ENGINE id selected by the module. Later operator rulings belong in `INSTANCE/CORRECTIONS.md`.

## Retrieval locality

Persistent module material follows this design axiom:

> Large information domain → compact routing/index layer → narrowly scoped authoritative shards.

Keep a domain in one file while it is cohesive and normally retrieved together. If materially different parts are likely to be retrieved independently, keep a stable compact entrypoint and split those parts into independently addressable authoritative files or sections.

Typical candidates include WORLD geography/institutions/culture, lore history/biology/technology, large location records, rules hooks, equipment, and mature person records. This is not a mandatory folder taxonomy.

Do not split by a fixed word/token threshold. Do not create empty hierarchies in advance. Split only when retrieval locality improves.

An index:

- contains only enough metadata to select a target;
- points explicitly to files and, where useful, named sections;
- does not duplicate the authoritative body or become a campaign bible;
- may point to a narrower sub-index when another level materially reduces unrelated retrieval;
- uses sparse cross-links for likely dependencies, never as permission for automatic retrieval.

A broad-category index that points to another unrelated multi-subject monolith is not sufficient merely because the first layer is small. Route to the practical granularity of likely retrieval. A heading fragment is appropriate only when the surrounding file is cohesive and safe enough for the host's observed whole-file behavior; physically separate unrelated PRIVATE subjects when leakage tests require it.

PLAY follows explicit pointers and stops at the smallest sufficient authoritative target. It does not `find`, list, or browse neighboring files to discover the hierarchy.

Before ACCEPT, rehearse at least one representative lookup for every complex capability: immediate need → declared entrypoint → exact file or heading → stop. If the route requires discovery, repair the manifest rather than teaching PLAY to browse.

## Mutable subsystem baselines

Stable definitions and accepted immutable **as-of-T0 snapshots** for phases, clocks/fronts, factions/institutions, inactive possibilities, economy/logistics, or other selected systems live in their declared MODULE bodies. A T0 snapshot asserts what was true at T0; it is not an enduring present-tense claim. MODULE files never mutate after bind.

Each mutable system's one authoritative definition also preserves its stable id, T0 classification, causal triggers/non-triggers, selected post-change current-authority route, cue lifecycle if needed, and any cross-system dependency/order that definition owns. Public/private placement follows the declared capabilities; explicit pointers connect them without duplicating rules. A SETUP manifest may mirror this for acceptance, but the disposable manifest/chat is never runtime authority.

INSTANCE registers remain canonical empty at bind. When a subsystem's current status is actually required, use accepted post-save transitions already established in the current chat first, then an explicit INSTANCE override. Only if neither exists **and no declared causal transition has occurred or is due** may current continuity be derived from one specifically named MODULE T0 snapshot. Do not scan the module or initialize every declared system. Definitions, indexes, REVIEW, Bearing, retrieval, and compatibility with the campaign envelope never make a subsystem operative.

PLAY never writes this transition. The GM may steward an already-operative process when its established cause or declared due condition calls for world action; it does not need to wait for the PC to inspect the process. An accepted creative mandate may separately authorize discretionary consequential material at its eligible boundaries, but no MODULE definition supplies that warrant. At the next explicit CHECKPOINT or CLOSE after the first accepted change, ADMIN follows the selected single current authority: a NOW-owned subsystem materializes complete as-of-now status—not its full lore or history—in an explicit NOW entry/shard; a CURRENT_SAVE-owned value changes only in the candidate; a PC-owned value changes only in the INSTANCE PC bundle. Apply every accepted post-save transition exactly once. Thereafter the MODULE snapshot remains authority only for T0 and stable definitions; the selected INSTANCE route answers current status. A clock, phase, seed, faction, institution, or resource track never changes merely because time passed, a session ended, REVIEW noticed it, or its body was retrieved unless that exact cause was declared in its design.

Each mutable T0 system is marked definition-only, dormant, or initially implicated. If a private initially implicated system can become relevant without being named by another resident fact, T0 supplies one compact nonsecret watch/route cue in `declared_state_flags`. The cue contains only a stable system id, causal or due-check condition, and declared capability/section route. The id, route, filename, and heading are themselves non-revelatory; use opaque stable forms where needed. It does not contain the private value, a prepared scene, or its own warrant, and does not by itself activate or advance the system. While that condition is genuinely operative, `causal_frontier` may carry a compact typed reference to this field rather than duplicate its detail. A private system with no such cue is query-triggered or dormant, not silently autonomous.

CHECKPOINT/CLOSE adds or updates a `declared_state_flags` cue only while the private system remains causally live across fresh boot and no other resident fact makes its check discoverable. An initial cue may name a MODULE snapshot; once current state materializes, its cue follows the selected current INSTANCE authority. Add, update, or retire the corresponding nonduplicating `causal_frontier` reference when the condition becomes operative or ceases to be. Retire the watch cue with the system or when another resident route supersedes it. Never keep a stale MODULE route as if it pointed to current state. REVIEW may interpret what an operative process means for campaign direction, but it cannot add either cue, activate or advance the process, or change its authoritative state.

## Person records (if PEOPLE exists)

The preauthored-person rules in this section require PEOPLE. The emergent-person INSTANCE/CAST_STATUS rule below applies whether or not the MODULE declares a PEOPLE capability.

MODULE files are **baseline CANON** (and initial PRIVATE if authored).
Sections: `## CANON` / `## NOW` / `## PC` / `## PRIVATE`.

Each authored person that may be named in CURRENT_SAVE or receive an overlay has one stable portable `person_id` using the module-id safe-token grammar. The PEOPLE entrypoint maps that id to the record; `hot_identifiers` uses the same id, and the overlay path is always `INSTANCE/PEOPLE/<person_id>.md`. Use a non-revelatory opaque id when a descriptive id would expose private truth. Do not mint mass ids, stubs, or hot entries merely because people may exist.

Keep a person in one file while those sections are small. If a mature person record needs sharding, retain the declared person entry file as a compact index and route to narrower authoritative files; do not split merely because the four headings exist.

MODULE `## NOW` / `## PC` sections are immutable as-of-T0 snapshots. Until an INSTANCE overlay or accepted post-save transition exists, and only while no declared causal transition has occurred or is due, those specifically named sections may support a current answer by established continuity. PLAY keeps later unsaved changes in chat RAM and never writes them. At the next explicit CHECKPOINT or CLOSE after the first durable change, ADMIN materializes the complete as-of-now mutable surface (`NOW`, `PC`, and only affected current PRIVATE state) in `INSTANCE/PEOPLE/<person_id>.md`, preserving an explicit route shape when sharded and applying all accepted transitions once. Do not duplicate stable CANON or unrelated PRIVATE lore. Thereafter MODULE `NOW`/`PC` answers only T0; current mutable person state lives under the INSTANCE overlay.

That no-CANON-copy rule applies to a person already authored in MODULE. For an emergent person created through accepted PLAY who gains durable causal state, the next explicit CHECKPOINT/CLOSE assigns one stable portable `person_id`, writes only their established minimal `## CANON` plus current mutable surface into `INSTANCE/PEOPLE/<person_id>.md`, and maps that id/record in CAST_STATUS. Do not retrofit or patch MODULE, invent missing identity, or promote a transient extra merely to make a roster.
CLOSE must not write relationship progression back into MODULE.

## Instance overlays

At **bind**, ADMIN copies the complete accepted PC bundle rooted at `MODULES/<id>/CHAR/PC.md` to the same relative paths under `INSTANCE/CHAR/`, and sets CURRENT_SAVE `pc_record` to `INSTANCE/CHAR/PC.md`. The bundle is the entrypoint plus its transitive explicit route closure; do not copy unrelated CHAR siblings.
When a preauthored person is promoted or a `## NOW` / `## PC` fact must persist, copy-on-write the complete mutable current-state surface to `INSTANCE/PEOPLE/<person_id>.md` at explicit CHECKPOINT/CLOSE before applying accepted unsaved transitions. Preserve their stable CANON in MODULE and do not duplicate unrelated PRIVATE lore. For an emergent promoted person, the INSTANCE record also owns minimal established CANON. Do not mix a newer overlay section with a current answer derived from the older T0 snapshot.
There is no “use MODULE until overlay exists” fallback after bind for the PC sheet.
