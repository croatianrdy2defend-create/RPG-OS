# INSTANCE schema

An instance is one campaign run. It is not the module.

ADMIN creates a new instance by copying the bound module’s `T0_SAVE.md` into a **candidate** save, assigning a new campaign identity, copying the accepted PC bundle into `INSTANCE/CHAR/` with its entrypoint at `PC.md`, initializing empty registers, validating the completed candidate, then replacing `CURRENT_SAVE.md` last. Bind requires an unbound save and an empty run archive; prior archive evidence is never cleared or inherited into a new campaign.

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
```

`tracked_resources` exists only when the bound engine/module/T0 template defines it. `declared_state_flags` normally exists only when the bound module/T0 defines it; however, at an explicit CHECKPOINT/CLOSE, ADMIN may introduce this already-whitelisted optional field when an accepted emergent durable private subsystem first requires cross-boot discovery and no other resident fact supplies it. If a selected private mutable subsystem is known during SETUP to need that possibility, T0 defines `declared_state_flags: none` even when no cue is initially live. Neither reservation nor later introduction activates a system. The universal schema does not assume a phone, messages, or carried weapons.

CURRENT_SAVE carries only the compact immediate summary needed to resume: current time/place, materially hot conditions, due obligations, pending action, and selected public resource totals. For each detailed inventory, account, calendar, faction, clock, or logistics value, choose one current authority. If its authoritative total is in CURRENT_SAVE, another body may hold nonduplicating components or a pointer but not a competing total. If a PC overlay or explicit INSTANCE state shard owns the detailed total, CURRENT_SAVE keeps only a nonconflicting resume cue or pointer when needed. Exact values and estimates remain distinguishable.

Unbound OS skeleton: `engine: unbound` / `module: unbound` / `commit_kind: unbound` / `save_rev: 0` / `safety_state: floor-only` / `status: OS ready; no instance`. Every other present, identity, pointer, roster, appointment, matter, and optional-resource field is absent when schema-optional or exactly `none`. Unbound state contains no campaign residue or unexpected INSTANCE path. Until bind completes, KNOWN, NOW, CAST_STATUS, and CORRECTIONS retain the distributed structurally empty templates (blank-line, line-ending, paragraph-wrap, and table-spacing changes do not alter emptiness); extra prose, comments, fenced blocks, or other content do. CHAR and PEOPLE contain only their README files. Bind revision one retains those empty registers, adds only the exact accepted PC route closure under `INSTANCE/CHAR/` (plus the shipped README), and may add accepted SAFETY sentences.
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

## Compilation matrix (ADMIN CLOSE and CHECKPOINT)

ADMIN must open this matrix and write each fact once:

| Fact class | Destination |
|---|---|
| present essentials | CURRENT_SAVE |
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

## Retrieval locality for growing INSTANCE records

CURRENT_SAVE remains a compact present, never a routing dump or chronicle. INSTANCE registers and person overlays begin as single files.

If materially different parts of a growing register or overlay are routinely needed independently, preserve its canonical route file (`KNOWN.md`, `NOW.md`, `PEOPLE/<person_id>.md`, or another declared entrypoint) as a compact index and move only the independently authoritative bodies into explicit subordinate files. Update all pointers together during ADMIN; v0.5 does not claim filesystem-atomic multi-file writes.

Do not split by file size alone and do not create empty shard trees in advance. Indexes route; they do not duplicate bodies. PLAY follows only the explicit branch justified by the immediate declaration and does not browse siblings.
