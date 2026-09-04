# INSTANCE schema

An instance is one campaign run. It is not the module. Its accepted campaign contract, authoritative present, and optional provisional bearing are separate records with separate mutation rights.

ADMIN creates a new instance by accepting a run-scoped campaign contract, copying the bound module’s `T0_SAVE.md` into a **candidate** save, assigning a new campaign identity, copying the accepted PC bundle into `INSTANCE/CHAR/` with its entrypoint at `PC.md`, initializing empty registers, validating the completed candidates, publishing the accepted contract, then replacing `CURRENT_SAVE.md` last. Bind requires an unbound save and an empty run archive; prior archive evidence is never cleared or inherited into a new campaign. An interrupted multi-file bind is incomplete and fail-closed until ADMIN repairs or resumes it; it is never PLAY authority.

## CURRENT_SAVE whitelist

```
engine
module
pc_record
campaign_id
save_id
save_rev
save_parent
commit_kind
archive_ref
safety_state
status
datetime
place
tracked_resources
appointments
known_open_matters
declared_state_flags
immediate_scene
hot_identifiers
scene_status
uncommitted_time
pc_declared_goals
causal_frontier
```

`tracked_resources` exists only when the bound engine/module/T0 template defines it. `declared_state_flags` normally exists only when the bound module/T0 defines it; however, at an explicit CHECKPOINT/CLOSE, ADMIN may introduce this already-whitelisted optional field when an accepted emergent durable private subsystem first requires cross-boot discovery and no other resident fact supplies it. If a selected private mutable subsystem is known during SETUP to need that possibility, T0 defines `declared_state_flags: none` even when no cue is initially live. Neither reservation nor later introduction activates a system. The universal schema does not assume a phone, messages, or carried weapons.

CURRENT_SAVE carries only the compact authoritative present needed to orient a GM and resume: current time/place, materially hot conditions, clean scene/beat state, uncommitted PC time, explicitly declared PC goals, the causal frontier, and selected public resource totals. It contains no provisional campaign interpretation, inferred player preference, preparation, rejected candidate, or plot forecast.

The four v0.6 orientation fields are:

- `scene_status`: exact lowercase `none` for the unbound skeleton; otherwise `opening`, `active`, `paused`, `resolved`, `between-scenes`, or `unknown`. `resolved` means the immediate situation ended but does not claim that remaining PC time was committed. `between-scenes` means the prior beat was closed and no next fictional frame is committed. `unknown` preserves an honestly unresolved legacy state; new native binds should not use it when the accepted opening establishes the answer.
- `uncommitted_time`: `none`, `unknown`, or one compact literal interval still belonging to the player before a proposed time advance. It is not permission to skip that time. Use `none` only when no such interval is recorded, not as a claim about what the PC would choose to do.
- `pc_declared_goals`: `none` or only goals the player explicitly declared and that remain causally relevant. Preserve the declaration exactly or as an unambiguous compact quotation; observed conduct and OOC preferences never enter this field. `none` means no currently recorded goal, not that the PC has no desires.
- `causal_frontier`: `none` or a compact semicolon-separated set of established entries prefixed `consequence:`, `due:`, `process:`, `decision:`, or `cue:`. It carries only operative established consequences, specific due conditions/obligations, established live processes needing a later check, pending decisions, and narrow non-revelatory current-state cues/routes. It never carries broad open lore, provisional interpretation, a prepared candidate, or a possibility merely because it fits the campaign.

Do not duplicate a fact merely to populate `causal_frontier`. When `appointments`, `immediate_scene`, `declared_state_flags`, or another selected authority already owns the detail, the frontier may use a compact typed reference to that field/route. `known_open_matters` holds durable public unresolved matters that are not currently operative; once one becomes operative, put its current cue in the frontier and keep at most a nonduplicating background reference in `known_open_matters`.

For each detailed inventory, account, calendar, faction, clock, or logistics value, choose one current authority. If its authoritative total is in CURRENT_SAVE, another body may hold nonduplicating components or a pointer but not a competing total. If a PC overlay or explicit INSTANCE state shard owns the detailed total, CURRENT_SAVE keeps only a nonconflicting resume cue or pointer when needed. Exact values and estimates remain distinguishable.

Unbound OS skeleton: `engine: unbound` / `module: unbound` / `commit_kind: unbound` / `save_rev: 0` / `safety_state: floor-only` / `status: OS ready; no instance` / `scene_status: none` / `uncommitted_time: none` / `pc_declared_goals: none` / `causal_frontier: none`. Every other present, identity, pointer, roster, appointment, matter, and optional-resource field is absent when schema-optional or exactly `none`. `CAMPAIGN_CONTRACT.md` is the distributed unbound template and `BEARING.md` has `status: none`. Unbound state contains no campaign residue or unexpected INSTANCE path. Until bind completes, KNOWN, NOW, CAST_STATUS, and CORRECTIONS retain the distributed structurally empty templates (blank-line, line-ending, paragraph-wrap, and table-spacing changes do not alter emptiness); extra prose, comments, fenced blocks, or other content do. CHAR and PEOPLE contain only their README files. Bind revision one retains those empty registers, adds only the exact accepted PC route closure under `INSTANCE/CHAR/` (plus the shipped README), and may add accepted SAFETY sentences.
PLAY confirms ready and does not begin a scene. No filenames in that confirmation.

Machine-readable whitelist tables use outer `|` delimiters and one contiguous row block; a blank line ends the table, and no field row may appear later in the file. Present fields are never blank: use the exact `none` sentinel where the schema allows no current value.

Canonical roster field is CURRENT_SAVE `hot_identifiers` only. Do not keep a second list on NOW.md.

## Commit metadata

- `campaign_id` — new unique portable token for this run, using the same grammar as `save_id`; never reuse an id inherited from T0 or another run
- `save_id` — new unique portable token on every CHECKPOINT, CLOSE, and bind; v0.4-and-later writes use only ASCII letters, digits, `.`, `_`, and `-`, beginning with a letter or digit, because this id is embedded in stable headings
- `save_rev` — canonical nonnegative ASCII integer (`0` or a nonzero digit followed by digits), increments; no sign, leading zero, underscore, or non-ASCII digit
- `save_parent` — previous save_id, using the same portable-token grammar, or `none` for bind
- `commit_kind`: `checkpoint` | `close` | `bind` | `unbound`
- `archive_ref`: POSIX path relative to `ARCHIVE/` for the session/slice folder containing its routing index and evidence after CLOSE; `none` after CHECKPOINT or bind. New writes use no absolute path, backslash, `.`/`..` traversal, or symlink route.
- `safety_state`: `floor-only` | `active`

Enum and sentinel tokens are exact lowercase strings. `CLOSE`, `ACTIVE`, `null`, and `n/a` are not substitutes for `close`, `active`, `unbound`, or `none`; BOOT and VALIDATE must not silently normalize them.

`active` only if INSTANCE/SAFETY.md contains at least one real operator sentence under the literal `Hard no:`/`Hard-no:` or `Fade / veil:` label. Canonical entries are bullets beneath a label; a sentence may instead follow the label on the same line. Headings, comments, fenced examples, placeholders, and unrelated prose do not count.

Boot check lives in BOOTSTRAP, not here. Detection is boot-time only. A CHECKPOINT does not require an archive row. A CLOSE must have campaign INDEX `save_id` = CURRENT_SAVE `save_id`, folder = `archive_ref`, and a session-index pointer. Archive layout follows `ARCHIVE/_SCHEMA.md`.

VALIDATE output is an ephemeral ADMIN diagnostic, not an INSTANCE field or register. Never add validator, host, model, probe, or PASS state to CURRENT_SAVE.

## CAMPAIGN_CONTRACT schema

`INSTANCE/CAMPAIGN_CONTRACT.md` is the one accepted, run-scoped campaign contract. A MODULE may propose defaults; only the explicitly accepted INSTANCE record authorizes the bound run. It is compact and resident because it answers what kind of GMing was accepted, not what is true in the world.

The fixed record declares scalar front matter `id: instance.campaign_contract`, `class: campaign-contract`, and `temperature: resident`.

Its machine-readable table has the exact header `| Field | Value |` and these fields exactly once:

```
campaign_id
contract_id
contract_rev
contract_parent
status
module
campaign_promise
fit_envelope
structural_direction
gm_initiative
pressure_incident_density
time_handling
development_priorities
guidance_visibility
creative_mandate
creative_mandate_scope
creative_mandate_boundaries
review_mode
```

- `campaign_id` matches CURRENT_SAVE.
- `contract_id` is a new unique portable token on bind and every accepted RECALIBRATE, using the `save_id` grammar.
- `contract_rev` uses the `save_rev` integer grammar: `0` unbound, `1` at bind, then increments.
- `contract_parent` is the prior `contract_id`, or `none` for unbound/bind.
- `status` is `unbound`, `candidate`, or `accepted`. `candidate` is valid only in `INSTANCE/CAMPAIGN_CONTRACT.candidate.md`; the fixed path is never playable while marked candidate.
- `module` matches CURRENT_SAVE.
- `campaign_promise` is a compact statement of the accepted play experience, including its material tone and cadence, not a destination or plot summary.
- `fit_envelope` states compatible kinds, material exclusions, and the accepted anti-attractors needed for routine GM judgment. Fit is not warrant.
- `structural_direction`: `reactive-sandbox`, `responsive-emergent`, `broad-trajectory`, `structured-scenario`, or `custom: ...`.
- `gm_initiative`: `mostly-consequence-driven`, `balanced`, `proactive`, or `custom: ...`. This label alone never grants a creative mandate.
- `pressure_incident_density`: `quiet`, `variable`, `sustained`, or `custom: ...`.
- `time_handling`: `moment-to-moment`, `selective-compression`, `broad-calendar-movement`, or `custom: ...`.
- `development_priorities`: `none` or an operator-accepted compact ordered selection from `relationships`, `profession-status`, `exploration`, `mystery`, `external-conflict`, `domestic-life`, `survival`, and `custom: ...`.
- `guidance_visibility`: `natural`, `explicit`, or `minimal`; `natural` is the offered default but must still be accepted.
- `creative_mandate`: `off` or `on`, accepted explicitly. When `on`, `creative_mandate_scope` states kinds, never a queued scene/person/object, and `creative_mandate_boundaries` names eligible scene/session/calendar boundaries. When `off`, both are `none`. A boundary is an opportunity, not a warrant or quota.
- `review_mode`: `off` or `bearing-only`. v0.6 has no durable preparation mode.

In the distributed unbound template, identity/promise/envelope/axis fields are `none`, `creative_mandate: off` with scope and boundaries `none`, and `review_mode: off`. These safe template defaults grant no campaign authority before bind.

Every accepted-contract value is nonblank. A `custom: ...` value must contain the accepted text after the colon. The contract contains no current facts, inferred preferences, campaign bearing, prepared possibility, secret plot, or promised outcome. Its promise, envelope, axes, and mandate authorize kinds and cadence only; they do not make any specific content true or entitled to appear.

## BEARING schema

`INSTANCE/BEARING.md` is an optional, compact, provisional review record. The distributed file has `status: none`; that file's existence does not make a bearing active. A usable bearing is never factual authority and never a warrant.

The fixed record declares scalar front matter `id: instance.campaign_bearing`, `class: campaign-bearing`, and `temperature: warm`.

Its machine-readable table has the exact header `| Field | Value |` and these fields exactly once:

```
campaign_id
base_save_id
base_save_rev
base_contract_id
base_contract_rev
status
evidence_scope
```

`status` is `none`, `candidate`, or `provisional`. `candidate` is valid only in `INSTANCE/BEARING.candidate.md`. The distributed unbound template has `campaign_id: none`; at bind, ADMIN resets the empty record to the new run's `campaign_id` while leaving every base id/revision and `evidence_scope` at `none`/`0`, every section at `none`, and `status: none`. This identity-only reset is not REVIEW content and supplies no orientation. A fixed-path `provisional` bearing is usable only when its `campaign_id`, base save id/revision, and base contract id/revision exactly match the currently accepted records. Any mismatch makes it stale by definition even if the stored status still says `provisional`; omit it from PLAY orientation and do not mutate it merely to relabel staleness. `evidence_scope` is `none` in the empty template and otherwise lists only the exact files/headings REVIEW actually consulted. Scope is provenance, not an authority upgrade.

After the table, these exact level-two sections occur once and stay distinct:

```
## Established references
## PC-declared goals
## OOC preferences
## Observed conduct
## Provisional interpretation
## Directions
## Questions
```

Use `none` for an empty section. Established references point to current or historical authority rather than retelling canon. PC goals preserve explicit in-fiction declarations; OOC preferences contain only explicit operator calibration; observed conduct records only what the PC did without inferring appetite, desire, consent, or preferred plot. Interpretation, directions, and questions remain explicitly provisional and may say `no stable pattern yet`. Directions are abstract trajectories to attend to, weaken, retire, or reconsider—not queued scenes or content that should appear. Questions preserve uncertainty; they are not invitations to answer it.

BEARING contains no preparation, candidate scenes, candidate people, encounter list, hidden plot, clock advance, new fact, activation cue, or instruction to make a direction happen. Retrieval, presence, fit, a boundary, or an entry in this record never activates anything.

## Mutation boundaries

| Operation | May write | Must not write |
|---|---|---|
| Bind | accepted CAMPAIGN_CONTRACT; identity-only empty BEARING reset; PC route closure and initialized INSTANCE registers; revision-one CURRENT_SAVE last | campaign history; bearing interpretation/review content; unaccepted contract values; invented T0 facts |
| MIGRATE V0.5 | identity-only bound-empty BEARING; explicitly accepted revision-one CAMPAIGN_CONTRACT; legacy CURRENT_SAVE preserved and upgraded as a new checkpoint, published last | unsaved PLAY; inferred goals/mandate/bearing; MODULE, ENGINE, ARCHIVE, PC/person/system history; legacy fact loss or reinterpretation |
| PERSIST (`CHECKPOINT` / `CLOSE`) | established current authorities; CURRENT_SAVE candidate last; archive evidence on CLOSE only | CAMPAIGN_CONTRACT; BEARING; inferred meaning/preference; preparation or rejected material |
| REVIEW | BEARING candidate, published separately after a successful PERSIST | CURRENT_SAVE; CAMPAIGN_CONTRACT; ENGINE/MODULE; history; clocks/people/state; activation cues; preparation |
| RECALIBRATE | CAMPAIGN_CONTRACT candidate after explicit OOC acceptance, then fixed contract path last | CURRENT_SAVE; MODULE defaults; history; safety rulings; BEARING; retrospective facts |

Bind gives the accepted contract `contract_rev: 1`, `contract_parent: none`, and the same new `campaign_id` as the candidate save. It publishes CAMPAIGN_CONTRACT immediately before CURRENT_SAVE; CURRENT_SAVE remains the bind commit point. If interrupted between them, BOOT fails closed on the mismatch and ADMIN resumes or repairs the bind.

PERSIST never interprets campaign direction. REVIEW runs only after a successful PERSIST and bases its candidate on that accepted save and contract. It may conclude `no stable pattern yet`. Publishing BEARING is its own replacement operation; a failed or skipped REVIEW leaves the accepted save and contract untouched and the campaign playable. `END SESSION` may sequence PERSIST first and REVIEW second, but reports their results separately.

RECALIBRATE is prospective. It creates a new unique `contract_id`, increments `contract_rev`, names the prior id in `contract_parent`, and requires explicit OOC acceptance of the complete resulting contract. Replacing the contract automatically makes any prior bearing stale by base mismatch; RECALIBRATE does not rewrite BEARING merely to mark that fact. It does not revise established evidence, current facts, the PC, or safety. A candidate file is never authority.

Before a contract or bearing candidate replaces its fixed path, ADMIN changes its temporary `candidate` status to the fixed-path status (`accepted` or `provisional`) and validates the finalized file again. The sole additional fixed Bearing status produced by migration is the identity-only bound-empty `none` shape described below. Renaming a still-`candidate` record never publishes authority.

## Compilation matrix (ADMIN CLOSE and CHECKPOINT)

ADMIN must open this matrix and write each fact once:

| Fact class | Destination |
|---|---|
| present essentials | CURRENT_SAVE |
| scene/beat lifecycle and remaining player-owned time | CURRENT_SAVE `scene_status` / `uncommitted_time` |
| explicitly declared live PC goals | CURRENT_SAVE `pc_declared_goals` |
| operative established consequences, due conditions, live processes, pending decisions, and compact current-state cues | CURRENT_SAVE `causal_frontier`, using nonduplicating references where another current field/route owns the detail |
| accepted run promise, axes, and creative mandate | CAMPAIGN_CONTRACT (bind/RECALIBRATE only) |
| provisional campaign interpretation after PERSIST | BEARING (REVIEW only; never factual authority) |
| learned durable public facts | KNOWN |
| live private consequences | NOW |
| mutable campaign/world-system state | NOW or an explicit shard routed from NOW |
| emergent durable subsystem definition + current state | one explicit `INSTANCE/NOW/<system_id>.md` shard routed from NOW only |
| promotion and stable person-id mapping | CAST_STATUS |
| rulings | CORRECTIONS |
| selected tracked public current total | CURRENT_SAVE only; PC may retain a maximum/derivation but not a duplicate live total |
| other mutable sheet/build values | INSTANCE PC entrypoint or its explicit shards only |
| person NOW/PC progression | INSTANCE/PEOPLE/<person_id>.md only |
| emergent promoted person identity | minimal established CANON in INSTANCE/PEOPLE/<person_id>.md only |
| accepted historical evidence | one semantic ARCHIVE scene shard (CLOSE only) |
| exact message | stable heading in its scene shard + MESSAGES_LEDGER pointer (CLOSE only) |
| embodied recall | stable scene-shard heading + RELATION_LEDGER + pointer on instance person overlay (CLOSE only) |

MODULE baseline files stay stable. Never patch MODULE CHAR or MODULE PEOPLE after bind.

At bind, NOW and the other registers remain canonical empty even when MODULE contains accepted immutable as-of-T0 snapshots. For a current-status question, accepted post-save transitions already established in the current chat come first, then the selected explicit current authority. Only when neither exists and no declared causal transition has occurred or is due may one specifically named T0 snapshot support a current answer by established continuity. PLAY writes nothing. At the next explicit CHECKPOINT or CLOSE after the first causal change, ADMIN applies all accepted post-save transitions exactly once in the selected destination: materialize complete as-of-now status in NOW only for a NOW-owned system; update only the candidate for a CURRENT_SAVE-owned value; update only the INSTANCE PC bundle for a PC-owned value. The MODULE snapshot thereafter still answers T0 and stable-definition questions, while the selected INSTANCE route answers current status; do not treat them as competing current claims. Do not copy the full lore body, preactivate seeds, or initialize every tracker merely because it exists.

For a MODULE person with as-of-T0 `## NOW` or `## PC`, absence of an INSTANCE person overlay, an accepted post-save transition, and any declared causal transition that has occurred or is due permits continuity from that named snapshot. PLAY keeps later unsaved change in chat RAM. At the next explicit CHECKPOINT or CLOSE, ADMIN materializes the complete as-of-now mutable surface (`NOW`, `PC`, and only affected current PRIVATE state), applying accepted changes once; stable CANON and unrelated PRIVATE lore remain in MODULE. After that, do not merge a current overlay with the historical T0 snapshot.

An emergent person with durable causal state has no MODULE source to copy. At the next explicit CHECKPOINT/CLOSE, assign a stable portable `person_id`, write only established minimal CANON plus the complete current mutable surface to `INSTANCE/PEOPLE/<person_id>.md`, and add the exact id/record mapping to CAST_STATUS. `hot_identifiers` uses the same id only while the person is actually hot. Do not invent missing fields, mutate MODULE, or promote a transient appearance.

An emergent non-person subsystem with durable causal state likewise has no MODULE definition. At the first explicit CHECKPOINT/CLOSE that promotes it, assign one stable portable `system_id` using the save-id safe-token grammar and create one shard at `INSTANCE/NOW/<system_id>.md`, explicitly routed from `INSTANCE/NOW.md`. That shard is the single authority for both its complete current state and the smallest established operational definition needed after fresh boot: triggers and non-triggers, its current-state route, cue lifecycle when applicable, and dependency/update order when applicable. Preserve unknowns as unknown; do not invent rules for completeness, promote a transient condition merely because it appeared, or retrofit MODULE. Later saves update that same current authority. If a private emergent system needs independent cross-boot discovery, use the ordinary compact non-revelatory cue rule below.

`declared_state_flags`, when present, may contain only compact resume conditions or nonsecret routing cues accepted during module construction or later accepted for an emergent durable subsystem. For a private subsystem that cannot otherwise be recognized, a cue names a stable system id, causal/due-check condition, and its exact authority route—declared MODULE capability/section for a preauthored T0 system, or the selected `INSTANCE/NOW/<system_id>.md` shard after emergent state materializes. It never contains the hidden value, outcome, or lore body. The id, route, and filename must also be non-revelatory; use an opaque stable id where needed. Absence of a cue does not authorize discovery. Retrieval of a cue does not activate or advance its target.

The cue lifecycle continues after T0. CHECKPOINT/CLOSE adds or updates a cue when a private subsystem remains causally live across fresh boot and no other resident present fact makes its check discoverable; once state materializes, the route follows the selected current INSTANCE authority rather than the older MODULE snapshot. Remove/demote it when the system retires or another resident fact or route supersedes it. Cue metadata never becomes the current value itself.

Clock, phase, front, faction, institution, economy, and similar state changes require an established cause. Elapsed time advances a record only when the record explicitly declares elapsed time as a cause. Retrieval and session/CLOSE boundaries never move it by themselves.

## v0.5 module and run migration

A v0.5 MODULE does not need to be rewritten merely to bind under v0.6. During bind, ADMIN creates the accepted run-scoped CAMPAIGN_CONTRACT from explicit operator choices; MODULE defaults are proposals, never inferred acceptance. If the legacy `T0_SAVE.md` lacks the four v0.6 orientation fields, add them only to the candidate INSTANCE save: use `scene_status: opening` only for an explicitly accepted, not-yet-played opening; otherwise ask or use `unknown`. Use `none` for uncommitted time, PC goals, and causal frontier only when no corresponding item is recorded; copy only explicit accepted T0 facts and never manufacture a process or opportunity to fill the fields. New v0.6-native T0 templates include all four fields.

An already-bound v0.5 run is not migrated by ordinary boot, LOAD, or silent normalization. Only an explicit **MIGRATE V0.5** request may route to `ADMIN/MIGRATE_V05.md`, before normal v0.6 bound validation. The operator must attest the source version, provide a restorable byte-for-byte backup outside the active folder, and confirm that no accepted PLAY remains unsaved. Otherwise write nothing.

The migration leaves the legacy CURRENT_SAVE authoritative while it stages a complete explicitly accepted revision-one Campaign Contract, an identity-only bound-empty Bearing, and a complete candidate save. The Contract and candidate save retain the existing `campaign_id` and `module`. The save preserves every legacy fact and allowed field, adds the four orientation fields from accepted records/operator clarification, assigns a new unique `save_id`, increments `save_rev` by one, names the old id as `save_parent`, uses `commit_kind: checkpoint`, and sets `archive_ref: none`. Never infer goals from conduct, bearing from repetition, a mandate from old POLICY tone, or a causal item from compatibility.

After all staged bodies validate, publish the bound-empty Bearing, publish CAMPAIGN_CONTRACT immediately before CURRENT_SAVE, and publish CURRENT_SAVE last as the commit point. Any partial write is fail-stop and requires restoration or exact completion from the external backup; it never authorizes PLAY. Migration does not rewrite or migrate MODULE, ENGINE, ARCHIVE, the PC/person/system records, safety, or old seeds. A later optional REVIEW may create provisional Bearing only after the migrated checkpoint succeeds.

## Retrieval locality for growing INSTANCE records

CURRENT_SAVE remains a compact present, never a routing dump or chronicle. INSTANCE registers and person overlays begin as single files.

If materially different parts of a growing register or overlay are routinely needed independently, preserve its canonical route file (`KNOWN.md`, `NOW.md`, `PEOPLE/<person_id>.md`, or another declared entrypoint) as a compact index and move only the independently authoritative bodies into explicit subordinate files. Update all pointers together during ADMIN; v0.6 does not claim filesystem-atomic multi-file writes.

Do not split by file size alone and do not create empty shard trees in advance. Indexes route; they do not duplicate bodies. PLAY follows only the explicit branch justified by the immediate declaration and does not browse siblings.
