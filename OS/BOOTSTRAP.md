# RPG OS PLAY Bootstrap

Technical loader and command router. It is not a campaign brain, lore body, or third source of fiction.

Loading resolves the resident authorities. Once they are available, GM cognition begins with orientation and intent as required by LAW—not with repository navigation.

## Resident startup

Before the first response in a fresh campaign chat, open exactly these addressed paths:

1. `OS/AGENTS.md`
2. `OS/BOOTSTRAP.md`
3. `OS/LAW.md`
4. `INSTANCE/CURRENT_SAVE.md`
5. `INSTANCE/CAMPAIGN_CONTRACT.md`

Do not preload ENGINE, MODULE bodies, other INSTANCE registers, ARCHIVE, ADMIN, `OS/RETRIEVAL.md`, or preparation.

Do not run `find`, `ls`, recursive search, repository inventory, or neighbor discovery. Do not open packs or loaders outside this OS folder. Silently verify that LAW, CURRENT_SAVE, and CAMPAIGN_CONTRACT were actually read; never claim an unopened record was loaded.

This mandatory load is the resident control surface:

- LAW supplies the GM Core and hard boundaries.
- CURRENT_SAVE supplies authoritative present state and causal frontier.
- CAMPAIGN_CONTRACT supplies the accepted run promise and GM calibration.

Campaign Bearing is optional and provisional. It is never a substitute for one of these three.

The five addressed paths above remain the technical boot set. A bound run then performs the bounded pre-fiction loads below, including the module's compact Setting Brief. Do not ask the operator to add that file to the boot prompt.

## Read the bindings

From CURRENT_SAVE, read at least:

- `engine`
- `module`
- `pc_record`
- `campaign_id`
- `save_id`
- `save_rev`
- `save_parent`
- `commit_kind`
- `archive_ref`
- `safety_state`
- `status`
- `datetime`
- `place`
- `scene_status`
- `uncommitted_time`
- `pc_declared_goals`
- `causal_frontier`

These and only these other whitelisted CURRENT_SAVE fields may appear, with nonblank values: `tracked_resources`, `appointments`, `known_open_matters`, `declared_state_flags`, `immediate_scene`, and `hot_identifiers`. No duplicate or unknown field is playable authority.

From CAMPAIGN_CONTRACT, read:

- `campaign_id`
- `contract_id`
- `contract_rev`
- `contract_parent`
- `status`
- `module`
- `campaign_promise`
- `fit_envelope`
- `structural_direction`
- `gm_initiative`
- `pressure_incident_density`
- `time_handling`
- `development_priorities`
- `guidance_visibility`
- `creative_mandate`
- `creative_mandate_scope`
- `creative_mandate_boundaries`
- `review_mode`

Do not infer a missing field from genre, module prose, or a previous chat.

## Bound Setting Brief upgrade dispatch

The sole exception to normal v0.6 bound validation for an already-bound v0.6 or v0.6.1 campaign is an explicit **UPGRADE SETTING BRIEF** request when the operator attests that the fixed module Setting Brief is absent. Leave PLAY idle and open `ADMIN/ADD_SETTING_BRIEF.md` before applying the required-Setting-Brief check. This authorizes only that compatibility preflight and one-file transaction; it does not make the campaign playable while the brief is absent.

Do not infer the source version or launch this procedure merely because a brief is missing. A fixed but malformed Setting Brief, a stale Setting Brief candidate, an unbound or v0.5 run, a resident mismatch, unsaved accepted PLAY, or another structural defect is not this upgrade path. Without the explicit command and required operator attestations, follow the ordinary checks below and fail closed.

## Legacy bound-run migration dispatch

The sole exception to normal v0.6 bound validation is an explicit **MIGRATE V0.5** request while CURRENT_SAVE is an operator-attested, already-bound v0.5 save and CAMPAIGN_CONTRACT is still the canonical unbound v0.6 template. Leave PLAY idle and open `ADMIN/MIGRATE_V05.md` before applying the v0.6 contract or four-orientation-field checks. This authorizes only that migration preflight and transaction; it does not make the legacy save valid for PLAY under v0.6.

Do not infer legacy provenance from a mismatch or migrate automatically. Without the explicit command, or if the resident files show a v0.6-native, unbound, already migrated, ambiguous, or partial state, follow the ordinary checks below and fail closed.

## Unbound state

The run is unbound when CURRENT_SAVE declares an unbound engine/module and no campaign identity. CAMPAIGN_CONTRACT must also be its canonical unbound template. If only one resident authority appears bound, report the mismatch and stop.

For a valid unbound state:

- confirm that RPG OS is ready and no runnable campaign is bound;
- do not begin fiction;
- do not invent a world, PC, date, place, NPC, contract, or opening;
- do not print paths or setup instructions unless asked;
- do not offer New Game or Load unprompted.

If the operator explicitly requests **NEW GAME** or **create campaign**, leave PLAY idle and open `ADMIN/NEW_GAME.md`. This is SETUP, not PLAY.

If the operator explicitly requests **LOAD MODULE** and names an existing module, leave PLAY idle and open `ADMIN/LOAD.md`. This is ADMIN bind, not PLAY.

## Bound-run match

Before fiction, a bound run must pass all of these:

1. CURRENT_SAVE has bound `engine`, `module`, `campaign_id`, and `save_id` values using portable safe tokens: ASCII letters, digits, `.`, `_`, and `-` only, beginning with a letter or digit. `pc_record` is exactly `INSTANCE/CHAR/PC.md`.
2. CURRENT_SAVE has a positive ASCII-integer `save_rev`; `commit_kind` is `bind`, `checkpoint`, or `close`; `safety_state` is `floor-only` or `active`; and datetime, place, and status are substantive. Bind has `save_parent: none`; checkpoint/close names a different portable parent id. Bind/checkpoint has `archive_ref: none`; close has a safe relative POSIX archive folder with no traversal.
3. CURRENT_SAVE contains every universally required field listed above exactly once, no unknown field, and nonblank `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier`. `scene_status` is one of `opening`, `active`, `paused`, `resolved`, `between-scenes`, or `unknown`; `causal_frontier` is `none` or contains only semicolon-separated `consequence:`, `due:`, `process:`, `decision:`, and `cue:` entries.
4. CAMPAIGN_CONTRACT has canonical front matter `id: instance.campaign_contract`, `class: campaign-contract`, and `temperature: resident`.
5. CAMPAIGN_CONTRACT has every field listed above exactly once, no unknown field or blank value, `status: accepted`, a portable `contract_id`, and a positive ASCII-integer `contract_rev`. Revision one has `contract_parent: none`; a later revision names a different portable parent id.
6. Contract `campaign_id` exactly equals CURRENT_SAVE `campaign_id`, and Contract `module` exactly equals CURRENT_SAVE `module`.
7. Each categorical axis uses one of these exact tokens or a nonblank `custom: ...` value: `structural_direction` = `reactive-sandbox`, `responsive-emergent`, `broad-trajectory`, or `structured-scenario`; `gm_initiative` = `mostly-consequence-driven`, `balanced`, or `proactive`; `pressure_incident_density` = `quiet`, `variable`, or `sustained`; `time_handling` = `moment-to-moment`, `selective-compression`, or `broad-calendar-movement`.
8. `development_priorities` is `none` or a substantive accepted compact selection; `guidance_visibility` is `natural`, `explicit`, or `minimal`; `review_mode` is `off` or `bearing-only`.
9. `campaign_promise` and `fit_envelope` are substantive. `creative_mandate` is exactly `off` or `on`; when off, scope and boundaries are `none`, and when on, both are substantive accepted limits.

If any check fails, report the mismatch OOC and stop. Never choose one authority by convenience, infer a contract, or begin fiction under a mismatched run.

### CLOSE integrity check

Only when CURRENT_SAVE `commit_kind` is `close`, open `ARCHIVE/INDEX.md` to confirm one row whose `save_id` equals CURRENT_SAVE `save_id`, whose folder equals `archive_ref`, and whose `session_index` is a nonempty path inside that folder.

If missing or mismatched, report the defect and do not invent the missing interval. Do not open the session index or an archive body during this boot check. CHECKPOINT and bind do not require an archive row.

## Before first fiction

Complete these bounded extras without loading `OS/RETRIEVAL.md`.

### Active safety

If CURRENT_SAVE `safety_state` is `active`, open `INSTANCE/SAFETY.md` and retrieve the real operator Hard-no and Fade/veil sentences. Headings, placeholders, comments, and examples are not active entries.

Do not open SAFETY merely because the file exists. Honor active entries quietly; never put them in NPC dialogue.

### Module setting awareness

Open `MODULES/<module>/SETTING_BRIEF.md`, using the already validated bound module token directly. Do not list, search, or browse for it.

Use it only when all are true:

- front matter is exactly `id: <module>.setting_brief` and `class: setting-brief`;
- the exact level-two sections `World identity`, `What is ordinary`, and `Available depth` each occur once, in that order, and contain substantive text;
- it remains a compact, stable, public orientation rather than current mutable state, a cast roster, detailed lore, private truth, a seed or tracker body, preparation, or a plot queue.

If the file is missing, malformed, empty, or belongs to another module, report that the module is not runnable and stop before fiction. Do not reconstruct it from generic knowledge or by opening WORLD files.

The Setting Brief establishes the broad world assumptions the GM must remember from the first fictional line, especially ordinary facts that generic model priors would erase. It does not override CURRENT_SAVE, CAMPAIGN_CONTRACT, accepted post-save play, or narrower authority. `Available depth` announces that colder authority exists; it is not permission to load it. Never recite the brief or its route in fiction.

### Module voice

Open the bound module's `POLICY.md` and read its required `## Voice` section before producing fiction. Read `## Safety extras` in the same file if present.

If the required voice is missing or unreadable, report that the module is not runnable and stop. Do not inherit a literary style from LAW or another campaign. Do not load other POLICY sections merely because the file was opened.

### Optional current Bearing

Only when the accepted CAMPAIGN_CONTRACT has `review_mode: bearing-only`, make at most one direct attempt to open `INSTANCE/BEARING.md` before first fiction; do not search for a substitute. When `review_mode` is `off`, do not open it.

Use it only when all are true:

- front matter is `id: instance.campaign_bearing`, `class: campaign-bearing`, and `temperature: warm`;
- the accepted CAMPAIGN_CONTRACT has `review_mode: bearing-only`;
- its table contains exactly `campaign_id`, `base_save_id`, `base_save_rev`, `base_contract_id`, `base_contract_rev`, `status`, and `evidence_scope`, with substantive evidence scope;
- the exact level-two sections `Established references`, `PC-declared goals`, `OOC preferences`, `Observed conduct`, `Provisional interpretation`, `Directions`, and `Questions` each occur once and contain `none` or a substantive body;
- `status` is `provisional`;
- its `campaign_id` equals CURRENT_SAVE `campaign_id`;
- its `base_save_id` equals CURRENT_SAVE `save_id`;
- its `base_save_rev` equals CURRENT_SAVE `save_rev`;
- its `base_contract_id` equals CAMPAIGN_CONTRACT `contract_id`;
- its `base_contract_rev` equals CAMPAIGN_CONTRACT `contract_rev`;
- it contains no preparation bank, queued candidate, activation instruction, warrant claim, new fact, or state/clock advance.

A missing, empty, stale, malformed, nonmatching, or contract-disabled Bearing is nonfatal and must not block PLAY. When `review_mode` is `off`, skip and ignore Bearing even if its stored status and bases otherwise appear usable. If a file claims `status: provisional` but fails any eligibility check, give a concise OOC warning; do not repair it during PLAY.

A matching Bearing supplies provisional orientation only. It never establishes facts, supplies a warrant, activates a possibility, ticks a process, or gains priority because it was loaded. Do not open preparation.

## First fiction and fresh-chat resume

Do not invent an interval.

Orient from the accepted Campaign Contract, CURRENT_SAVE, the module Setting Brief, and a matching optional Bearing. The Setting Brief prevents generic-world defaulting; it does not supply current state or an incident. Use the compact causal frontier to recognize operative consequences and due checks; retrieve a detailed authority only when the actual GM task requires it.

- If `scene_status` is `opening`, `active`, or `paused`, frame or resume the saved immediate situation without repeating a compliance recital or authoring a voluntary PC act.
- If `scene_status` is `resolved` or `between-scenes` and `uncommitted_time` remains, orient the player and ask whether they use that time or advance it. Do not spend it silently.
- If `scene_status` is `unknown`, preserve that uncertainty and ask only for the clarification required to resume; do not invent the missing interval.
- If the next beat or calendar advance was already accepted and is named in the save, frame it when PLAY is requested.
- If no fiction is requested, give only a concise OOC ready confirmation.

The opening is a playable frame, not a mandatory hook. It may contain no incident, but it must provide enough orientation to understand where and when the PC is and what established matter, if any, remains in motion.

## Retrieval after startup

For each player declaration, follow LAW's GM-first operating order. Identify the GM task and authority question before any nonresident lookup.

If the task requires a nonresident fact, exact record, current private state, or mechanical procedure, open the relevant section of `OS/RETRIEVAL.md` and follow its deterministic route. Do not load that manual speculatively. A direct explicit pointer already resident in CURRENT_SAVE may be followed without browsing.

Retrieve enough context sufficient and proportionate to GM the task. Zero additional retrieval and a zero-result lookup remain valid. Missing retrieval is not a virtue when the GM genuinely needs an authoritative fact or procedure.

Retrieval does not choose the camera, make content important, or authorize activation. Do not browse neighbors.

## Operator commands

Commands are OOC. Stop fiction while executing them.

### AUDIT

If the operator says **AUDIT** or asks what was opened, report the immediately preceding non-AUDIT player turn:

- paths and addressed sections opened;
- one-line reason for each;
- whether list/search/find/discovery ran;
- for archive retrieval, the campaign index, session index, shard/heading, skipped levels, and any legacy monolith opened.

Report only the access self-audit, not file bodies. AUDIT is useful self-report, not independent proof of host isolation.

### VALIDATE

If the operator says **VALIDATE**, leave PLAY and open `ADMIN/VALIDATE.md`. This authorizes structural repository inventory for ADMIN only. Prefer the shipped read-only script when code execution exists; otherwise label the result `MODEL-CHECKED`, state exact coverage, and never report a complete structural PASS. Validation does not score GM quality and writes no campaign register.

### CHECKPOINT

If the operator says **CHECKPOINT**, leave PLAY and follow only the Checkpoint section of `ADMIN/CLOSE_CONTRACT.md`: persist present state without archive evidence, publish CURRENT_SAVE last, report, and stop.

### CLOSE

If the operator says **CLOSE**, leave PLAY and follow the full `ADMIN/CLOSE_CONTRACT.md`, including the INSTANCE compilation matrix. Report and stop. CLOSE persists state plus archive evidence; it does not perform REVIEW.

### REVIEW

If the operator says **REVIEW**, leave PLAY and open `ADMIN/REVIEW.md`. REVIEW may run only against a successful current PERSIST and writes provisional Bearing only. Its failure or omission must leave the valid save untouched. Report and stop; do not resume fiction in the same response.

### RECALIBRATE

If the operator says **RECALIBRATE**, leave PLAY and open `ADMIN/RECALIBRATE.md`. Contract changes require explicit OOC acceptance, apply prospectively, and make prior Bearing stale. A draft or refused change has no authority.

### END SESSION

If the operator says **END SESSION**:

1. Leave PLAY and run the full CLOSE procedure in `ADMIN/CLOSE_CONTRACT.md`.
2. If CLOSE fails, stop. Do not run REVIEW.
3. If CLOSE succeeds, report the PERSIST/CLOSE result separately.
4. If the accepted Campaign Contract has `review_mode: bearing-only`, open `ADMIN/REVIEW.md` and run REVIEW against the newly published save.
5. Report REVIEW separately. REVIEW failure does not roll back or qualify the successful CLOSE.
6. If `review_mode` is `off`, stop after CLOSE and state that REVIEW is disabled.
7. Any other `review_mode` is invalid. Preserve the successful CLOSE, report the contract defect, and do not run REVIEW.

Do not invent a third persistence operation. CHECKPOINT and CLOSE are the PERSIST operations.

## Input boundary

Unsent UI suggested-reply chips are not player input. Ignore them. They cannot establish intent, consent, OOC preference, accepted contract settings, or campaign state.
