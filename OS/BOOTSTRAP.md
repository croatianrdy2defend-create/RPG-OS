# RPG OS PLAY Bootstrap

Loader only. Not a third body of campaign lore.

## Startup

Before the first PLAY response in a fresh chat, load exactly:

1. `OS/AGENTS.md`
2. this file
3. `OS/LAW.md`
4. `INSTANCE/CURRENT_SAVE.md`

Do not preload ENGINE, MODULES, other INSTANCE registers, ARCHIVE, or ADMIN.
Do not `find`, `ls`, recursively search, or otherwise discover the repository.
Do not open packs or loaders outside this OS folder.

Silently verify those two resident records (LAW + CURRENT_SAVE) were actually read. Do not claim unopened records were loaded.

If unbound, the ready line must include: no files beyond the four addressed paths were opened.

Do not open ARCHIVE/INDEX.md during the four-file boot. The close-mismatch check below runs only after CURRENT_SAVE has been read and only when `commit_kind` is `close`.

## Bindings

Read from CURRENT_SAVE:

- `engine` — ruleset id (example: `freeform`)
- `module` — campaign-module id
- `pc_record` — path to the bound player character, if any
- `commit_kind` — `unbound` / `bind` / `checkpoint` / `close`
- `save_id`
- `archive_ref`
- `safety_state`

If `engine` or `module` is empty or `unbound`:

- Confirm the OS is ready and that no runnable campaign instance is bound.
- State that no files beyond the four addressed paths were opened.
- Do not begin a scene.
- Do not invent a world, PC, or opening.
- Do not print filenames, paths, or copy instructions.
- Do not offer New Game or Load unprompted.

If the operator then explicitly requests **NEW GAME** or **create campaign**, leave PLAY idle and open `ADMIN/NEW_GAME.md`. That is SETUP, not PLAY.

If the operator then explicitly requests **LOAD MODULE** and names an existing module, leave PLAY idle and open `ADMIN/LOAD.md`. That is ADMIN bind, not PLAY.

## Bound boot extras (after the four files)

If bound and `commit_kind` is `close`: open `ARCHIVE/INDEX.md` only to confirm a row whose `save_id` equals CURRENT_SAVE `save_id`, whose folder equals `archive_ref`, and whose `session_index` field is a nonempty path inside that folder. If missing or mismatched, report the defect and do not invent the missing interval. Do not open the session index or other archive bodies during this check.

If `safety_state` is `active`, retrieve `INSTANCE/SAFETY.md` entries (real Hard-no / Fade sentences, not headings) before first fiction. Honor quietly. Never put those lines in NPC mouths.
Do **not** retrieve SAFETY merely because the file exists or contains headings.

If bound, open no module or engine file until the immediate declaration requires it.

The first request that requires fiction also requires:

- the bound module’s declared **voice** section in `POLICY.md`
- that module’s **Safety extras** section in the same POLICY file, if present

Voice is not permanently resident in LAW. If the voice section is missing, fail closed: the module is not runnable; do not begin the scene.

## Retrieval

Resident LAW + CURRENT_SAVE first.
Open the smallest sufficient set. Default is zero extra files. Every extra section needs its own immediate causal reason.
A routing index plus one target counts as one bounded lookup.
A tool may return a whole file; treat only the addressed section as retrieved and discard the rest immediately. This mitigates leakage; it does not isolate tokens. If a test shows PRIVATE/CANON leakage from whole-file reads, split that record physically.
Zero additional retrieval is valid.
A retrieved fact gains no narrative weight.
Do not browse neighbors.

A declared capability or canonical route file may be either the authoritative body or a compact index pointing to narrower bodies. Follow only explicit file/section pointers. Recurse through another index only when it materially narrows the target; skip known levels and stop at the smallest sufficient authoritative unit. An index or cross-link does not authorize global search, sibling browsing, or retrieval without immediate causal need.

If a fact is unknown or unfixed, leave it so.
If a capability is not listed in the bound `MODULE.md`, it is absent.

Archive indexes are maps, not fine-detail authority. A compact index may answer a simple unambiguous routing/existence question. Exact wording, rolls, quantities, sequence, subtle relationship context, or disputed history require the pointed source shard or legacy source heading.

For historical retrieval, open `ARCHIVE/INDEX.md` only when the relevant session/slice is not already known; then its session `INDEX.md`; then one or a few addressed scene shards. Skip a higher index when a trusted current pointer or the operator already identifies the target. Stop as soon as sufficient authoritative evidence is found. Question breadth governs retrieval breadth.

Reading an archived possibility, intention, seed, or unresolved condition does not activate it or make it current. Preserve *might*, *suspected*, *conditional*, *unknown*, and *not decided* exactly.

## Route table

Paths are relative to the bound ENGINE / MODULE / INSTANCE. Do not hard-code a campaign name.

| Required fact | Open |
|---|---|
| Listed PC value | bound `pc_record` (INSTANCE overlay), smallest named section or explicitly pointed shard under `INSTANCE/CHAR/`; never browse sibling shards |
| Mechanic beyond LAW | On the first mechanic in a fresh chat, inspect compact `INSTANCE/CORRECTIONS.md` scope/index first and retrieve a matching ruling if any; then check the two deterministic candidates `ENGINE/<id>.md` and `ENGINE/<id>/ENGINE.md` without listing/searching, require exactly one to exist, and open that entrypoint for the bound ENGINE procedure. If neither or both exist, fail closed. Inspect bound `MODULE.md` for RULES_HOOKS and, if hook scope is not known, only its compact entrypoint/routing metadata; retrieve only a matching target/section (a cohesive one-body entrypoint may necessarily supply both scope and body). A current correction outranks lower sources; ENGINE wins any contradiction with a MODULE hook. |
| Saved ruling or correction | `INSTANCE/CORRECTIONS.md`, then only its explicit pointed shard if it has become an index; consult ENGINE only if the present ruling does not settle the question |
| Module cadence, tone, voice, anti-attractors, relationship extras, module safety extras | bound `POLICY.md`, named section |
| Module identity / capability list | bound `MODULE.md` |
| Learned instance fact | `INSTANCE/KNOWN.md`, then one explicitly pointed shard if it has become an index |
| Exact past event | `ARCHIVE/INDEX.md` if session unknown → that session `INDEX.md` → one scene shard/heading; follow a legacy pointer as written |
| Exact message wording | `ARCHIVE/MESSAGES_LEDGER.md` → one scene-shard exact-message heading; follow a legacy `MESSAGES.md` pointer as written |
| Embodied / intimacy recall | `ARCHIVE/RELATION_LEDGER.md` → one scene-shard heading; follow a legacy `TRANSCRIPT.md` pointer as written |
| Cross-session historical development | current relation/state first, then only the selected archive indexes and shards proportionate to the question |
| Public setting / place / institution function | declared module WORLD or INST entrypoint → one explicit authoritative section/file, if that capability exists |
| Private now of a person already present, scheduled, or implicated | Use accepted post-save change already established in this chat; otherwise try the deterministic INSTANCE person entrypoint → `## NOW` or its explicit shard; only if neither exists derive continuity from that person's named MODULE as-of-T0 `## NOW`; never browse for a person |
| Relation/current state with the PC | Use accepted post-save change already established in this chat; otherwise try the deterministic INSTANCE person entrypoint → `## PC` or its explicit shard; only if neither exists derive continuity from that person's named MODULE as-of-T0 `## PC`; use ARCHIVE separately only for exact history |
| Stable established person identity | Deterministic INSTANCE person entrypoint → `## CANON` only for an emergent promoted person; otherwise MODULE person entrypoint → `## CANON` or its explicit shard |
| Hidden private life | INSTANCE or MODULE person entrypoint → `## PRIVATE` or its explicit shard, only if causally required |
| Phase, clock/front, seed, faction/institution, or other mutable subsystem *status* | Accepted post-save transition in this chat first → selected explicit current authority (resident CURRENT_SAVE value/flag when selected, otherwise `INSTANCE/NOW.md`/shard) → only if none exists and no declared transition is due, one specifically named MODULE as-of-T0 snapshot named by an immediate fact or compact cue; never browse siblings or load all trackers |
| Preauthored subsystem operational definition | its explicitly named declared MODULE authority/section only, reached from the immediate fact or compact cue; never scan the capability or load all systems |
| Emergent durable subsystem definition/current state | exact `INSTANCE/NOW/<system_id>.md` shard reached through its explicit NOW route, immediate fact, or compact cue; never browse NOW siblings |
| Seed or truth *body* | that one module file, only if capability present and already active/implicated or ADMIN explicitly browses |
| Visual interpretation | module VISUAL, then one image if the image itself is required |
| Current private registers | `INSTANCE/NOW.md`, then one explicitly pointed shard if it has become an index |
| `person_id` for an already named established emergent person | exact `INSTANCE/CAST_STATUS.md` mapping only; never browse it or use the roster to introduce someone |
| Promotion roster / discovery | `INSTANCE/CAST_STATUS.md` — ADMIN; PLAY never opens it to find someone to introduce |
| Operator safety list | `INSTANCE/SAFETY.md` only when `safety_state` is `active` |

Missing files: say the record is not in this skeleton. Do not invent. Do not substitute another campaign pack.

For a mutable subsystem or person, MODULE status is an immutable as-of-T0 snapshot, not a permanent current claim. Use it for current continuity only while neither an INSTANCE override nor an accepted post-save transition in this chat exists **and no declared causal transition has occurred or is due**. If a cue/known condition says a transition may be due, retrieve and resolve only its declared route; do not assume the T0 value persisted. PLAY keeps unsaved changes in chat RAM and never writes. Once an explicit INSTANCE route exists, it answers current status; the older MODULE value answers T0 only. MODULE may still supply stable definitions and CANON when separately required. A subsystem first established after bind has no MODULE authority: after its first explicit save, its one routed INSTANCE/NOW shard supplies both the established operational definition and current state.

## Opening

If CURRENT_SAVE has an immediate-scene block, establish only that, then return control before any voluntary PC act.
If CURRENT_SAVE is unbound, stop after the ready confirmation.

## Operator commands (not fiction)

If the operator says **AUDIT** (or "what did you open?"):
do not narrate. Report the immediately preceding **non-AUDIT** player turn: paths/sections opened, one-line reasons, and whether any list/search/find/discovery ran. No bodies. For archive retrieval, identify which campaign index, session index, and shard/heading were used, which levels were skipped, and whether a legacy monolithic source was opened.

If the operator says **VALIDATE**:
leave PLAY. Open `ADMIN/VALIDATE.md` and follow it. This explicitly authorizes a structural repository inventory for ADMIN only. Prefer the shipped read-only script when code execution exists; otherwise label the inspection `MODEL-CHECKED` with exact coverage and never report complete PASS. Report OOC and stop. Do not write a validation result into any campaign file.

If the operator says **CHECKPOINT**:
leave PLAY. Follow ADMIN/CLOSE_CONTRACT.md section Checkpoint only (save overwrite, no archive). Then stop.

If the operator says **CLOSE**:
leave PLAY. Follow the full close contract, including the compilation matrix in INSTANCE/_SCHEMA.md.

Unsent UI suggested-reply chips are not player input. Ignore them.
