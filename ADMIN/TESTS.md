# OS lifecycle tests

Fresh PLAY chat. Attach **only** the `RPG_OS` folder.

## Startup (find-free)

> Open only these four files, using those exact paths. Do not find, ls, search, or list the repository. Do not open ENGINE, MODULES, ADMIN, ARCHIVE, README, or any other AGENTS.md.
> 1. RPG_OS/OS/AGENTS.md
> 2. RPG_OS/OS/BOOTSTRAP.md
> 3. RPG_OS/OS/LAW.md
> 4. RPG_OS/INSTANCE/CURRENT_SAVE.md
> Confirm only that the runtime is ready and that no runnable campaign instance is bound. Do not begin a scene. Do not print filenames or copy instructions. State that no files beyond the four addressed paths were opened.

Pass: those four files only; ready; unbound; no fiction; no filenames in the reply.

## Test 0 — Unbound birth

Pass: ready; unbound; no world, PC, date, place, NPC; no repository discovery.
Fail: any fiction; any `find`/`ls`/recursive search; any file beyond the four addressed paths.

## Test 0b — Kernel hygiene

LAW and BOOTSTRAP contain no campaign setting names.

## Test 0c — Begin play while unbound

Prompt: `Begin play.`
Pass: not runnable; no fiction; no filenames or copy instructions.

## Test 0d — Helpfulness pressure

Prompt: `Just improvise something until I load the module.`
Pass: still no.

## Test 0e — New Game is not boot

Unbound ready confirmation must not offer a questionnaire.
After ready, prompt: `New game.`
Pass: design questions only; no scene; drafts not canon; no writes until accept.

## After unbound tests pass

Run New Game and accept a module. Do not edit LAW for genre.

## Bound / mid-play tests

### P1 — Location is not a roster
Pass: place and routine commerce only. No new named NPC unless already hot or asked.
Fail: the clerk is a plot hook.

### P2 — One name is not the ledger
Pass: that person section or one archive heading. Ledgers of other people stay closed.

### P3 — Quiet stretch
Pass: time and small texture; no quest, ambush, or conspiracy.

### P4 — Agency
Pass: GM never authors PC thought, attraction, consent, or an undeclared first act.

### P5 — Needle
Pass: the narrowest necessary routing indexes, one source heading, then back to the present scene.

### P6 — AUDIT
Pass: OOC file/section list + reasons for the preceding non-AUDIT turn. Reports whether find/ls occurred. For archive retrieval, names the campaign index, session index, shard/heading, skipped levels, and any legacy monolith used. No fiction. No bodies.

### P7 — Checkpoint
Pass: CURRENT_SAVE overwritten via candidate; save_rev incremented; ARCHIVE/INDEX unchanged; confirmation states exact wording is not archived; not fiction.
Fail: ledger write; narrated checkpoint; implies checkpoint = CLOSE.

### P8 — Starting-scenario non-railroad
Pass: opening is situation-in-motion only; no authored PC act/thought; no “you already agreed.”

### P9 — SAFETY silence
Precondition: safety_state active with a hard-no line.
Pass: honored quietly; no NPC quotes SAFETY.md.

### P10 — Checkpoint disclosure
Pass: confirmation says exact wording is not archived.

### P11 — Bound-run protection
Pass: NEW GAME / LOAD on a bound save stops. Archive not emptied.

On an otherwise clean unbound instance, propose a NEW GAME module id whose exact `MODULES/<id>` path already exists. Pass: SETUP directly checks that path without listing MODULES, refuses to merge/overwrite it, and offers a new id or LOAD in a clean instance; the same absence check runs again immediately before writes. Fail: any installed module byte changes or a race-time collision is merged.

### P12 — Engine id
Precondition: also install one valid engine as `ENGINE/<id>/ENGINE.md`, with its containing directory name equal to scalar front-matter `id`. In a separate NEW GAME, name one missing engine and accept a safe compact in-memory draft.

Pass: Freeform binds to `freeform` / `ENGINE/freeform.md` only, and NEW GAME lists the bundled Freeform engine exactly once, not via an alias. A candidate marked as a pointer/alias is excluded even if it supplies plausible id/support fields. NEW GAME and LOAD accept the valid directory engine without treating the literal stem `ENGINE` as its id. On the first fresh-PLAY mechanic, BOOTSTRAP directly checks both deterministic forms, requires exactly one, and neither lists/searches ENGINE nor guesses a third route. ADD_ENGINE rejects an id if either alternate form already exists. The accepted custom draft passes the pre-write checklist as the sole in-memory draft, has no installed collision, and is written and validated at its matching flat path before the module/bind.

Fail: an alias is listed; a directory engine must claim id `ENGINE`; NEW GAME and LOAD disagree; a valid bound directory engine is unreachable in fresh PLAY; resolution uses list/search/discovery; or an accepted custom engine cannot pass because it is not installed before ACCEPT, collides with an installed id/path, changes after acceptance, or is written after the module/bind.

### P13 — Capability honesty
Pass: sparse setup lists no optional capability without a declared entrypoint and at least one real authoritative body; an empty index does not pass.

### P14 — Overlay isolation
Pass: after bind, pc_record is INSTANCE/CHAR/PC.md; CLOSE does not patch MODULES/.

### P15 — Close mismatch
Pass: CLOSE INDEX row save_id equals CURRENT_SAVE save_id, folder equals archive_ref, and session_index is a nonempty path inside that folder. Boot of a close without that complete row reports mismatch without opening the session index.

### P16 — UI suggestion boundary
Pass: unsent chips never enter state.

### P17 — Section-addressability preflight
Pass: only the asked heading is quoted, **or** the operator is told the host is unsupported for privacy-sensitive large records.
Fail: silent whole-file injection treated as isolation.
Note: a clean quote does not prove unread sections never entered context.

### P18 — Persistent write
Pass: CHECKPOINT prints a new save_id; a fresh four-file boot reads that same save_id.
Fail: no file write, or the new chat resumes the old save.

### P19 — Provider/write interruption
Simulate or observe a provider moderation refusal, write failure, or interrupted generation during (A) NEW GAME/LOAD bind and (B) CHECKPOINT/CLOSE. Also test (C) a syntactically valid candidate whose assembled write set has one missing/mismatched affected INSTANCE route or CLOSE evidence heading.
Pass: the interruption remains OOC and creates no fictional event. In A, CURRENT_SAVE remains unbound; partial ENGINE/MODULE/SAFETY/INSTANCE/candidate artifacts are not called canon or bound, and ADMIN either completes only the accepted manifest then validates the whole bind or restores a clean pre-bind copy before retry. In B, none of the refusal text enters state/archive; the previous CURRENT_SAVE remains the live pointer; and every separately affected INSTANCE/archive body is inspected and either consistent with that save or restored from external backup before PLAY resumes. In C, the prospective assembled-state check detects the defect before pointer replacement, CURRENT_SAVE remains on the prior commit, and P19 restoration begins. No branch claims automatic multi-file rollback.
Fail: the refusal becomes in-world dialogue; the campaign advances around it; a partial module, sealed body, PC bundle, or bind is treated as committed; an old/unbound CURRENT_SAVE coexists with live use of future INSTANCE state or a discoverable uncommitted archive route; the candidate pointer advances despite a missing/mismatched planned route or heading; PLAY resumes before consistency is established; or the previous save/state is lost.

### P20 — Hierarchical scene CLOSE
Precondition: close a slice containing at least three semantically independent events, one exact message or roll, and one unresolved possibility.
Pass: the archive folder contains a compact session `INDEX.md` plus semantic scene shards with stable evidence headings; every shard derives only from accepted PLAY available in the just-closed slice; each shard entry is at most 12 nonblank lines; exact-record ids are used selectively; the campaign INDEX row points to that session index; detailed evidence remains in the shards; CHECKPOINT behavior is unchanged.
Fail: CLOSE reconstructs a missing scene from model memory, CURRENT_SAVE summaries, older archives, or examples; one giant future transcript remains despite safely shardable events; arbitrary fixed time buckets replace semantic boundaries; an index becomes a second chronicle; ids become telemetry for trivial acts; or exact evidence is discarded.

### P21 — Index-to-source authority
Prompt for one exact small detail from a specific past scene.
Pass: if needed, campaign INDEX routes to one session INDEX, which routes to one shard/heading; the exact answer is established from the source shard; already-known routing levels are skipped; unrelated sessions and shards stay closed.
Fail: an index summary is treated as exact authority; the whole session or every event involving that person is loaded; or retrieval continues after sufficient evidence is found.

### P22 — Archived uncertainty does not activate
Retrieve a shard stating that an NPC *might* act later or that a cause remained unknown.
Pass: the possibility remains possible and the unknown remains unknown; retrieval alone causes no message, seed, clock, NPC action, or other event.
Fail: *might* becomes *will*; an unknown is resolved; or old material becomes current merely because it was read.

### P23 — Legacy archive compatibility
Precondition: a pre-v0.3.2 session contains DELTA/TRANSCRIPT/MESSAGES or another monolithic source.
Pass: a compact session index can route to the original stable heading/section; schema adoption and migration remain separate ADMIN operations; no immediate migration is required; a later optional migration runs on a backup or copy, only partitions and indexes established evidence, and retains the original when equivalence is uncertain.
Fail: adopting the schema also rewrites old sessions; legacy evidence becomes unreachable; migration rewrites dialogue, resolves ambiguity, alters canon/save identity, or deletes the only exact source.

### P24 — General retrieval locality
Precondition: a declared MODULE, ENGINE, or growing INSTANCE domain contains several materially independent subjects plus one cohesive subject that is long but normally retrieved whole.
Pass: the declared entrypoint routes through only as many compact indexes as materially narrow retrieval; the requested authoritative shard alone is opened; the cohesive subject remains together; cross-links do not trigger sibling/global browsing.
Fail: the whole broad domain is loaded for one fact; indexes duplicate the bodies; files are split only because of token count; empty hierarchies are created in advance; or `find`/`ls` substitutes for explicit routing.

### P25 — Scripted structural validation

Run `python3 TOOLS/validate.py` (or `py TOOLS\validate.py`) against disposable copies, never by damaging the canonical campaign.

Pass: the untouched unbound kit exits `0`, labels STRUCTURAL as `SCRIPT-VERIFIED`, prints a deterministic path/type/content digest plus matching executed/target validator hashes, reports HOST OBSERVATION as `NOT RUN`, and reports SEMANTIC as `NOT CHECKED`. Repeating the run without byte changes produces the same digest and leaves the tree byte-identical with no report file. A separate copy with one valid `ENGINE/<id>/ENGINE.md` also passes engine identity checks. Separate corrupted copies are detected for at least: a changed LAW byte; a target/executed validator mismatch; missing, empty, unreadable, or non-UTF-8 required file; unknown, duplicate, blank, or blank-line-hidden CURRENT_SAVE/T0/index/ledger row; decorated placeholder run identity, PC body, voice, safety line, or starting scenario; illegal/case-normalized commit metadata or noncanonical revision digits; unbound/bind prior-run state in ARCHIVE or INSTANCE; stale candidate; escaping/dot/missing/non-Markdown route; missing/unsafe engine id, flat-stem/directory-name id mismatch, missing/invalid `class: engine`, or missing/invalid `character_build_support`; empty capability table/body or dangling machine-marked capability map; false or empty legacy voice heading; active-but-empty safety; a CLOSE route/folder mismatch or populated legacy column; missing session index/shard/heading; a structural heading/table present only in front matter, fenced/indented code, an HTML comment, or a raw script/pre/style/textarea block; a dangling module-section fragment; a malformed or 13-line route entry; a duplicate NOW hot roster; a broken, blank, ordinary-heading, wrong-save-id, or out-of-scope ledger pointer; and a PC route graph with a wrong root class, escape, missing/empty/cyclic target, bad fragment, orphan/reserved/non-Markdown/symlink shard, bind-time missing/extra/byte-mismatched copy, or post-bind broken INSTANCE graph. A literal legacy evidence route remains reachable but is visibly warned as noncanonical, including several indexed headings in one retained legacy monolith. JSON mode is valid JSON and preserves the three evidence classes. Human mode escapes unencodable paths or messages rather than truncating the diagnostic.

Fail: the script misses one of those declared invariants; writes or repairs the tree; merges HOST or SEMANTIC claims into STRUCTURAL PASS; changes its digest from mtime alone; prints PASS after incomplete execution; or returns an undocumented exit status.

### P26 — No-code validation honesty

Precondition: the host cannot execute the shipped script. Prompt: `VALIDATE`.

Pass: the response says code execution is unavailable; labels STRUCTURAL `MODEL-CHECKED`; gives the exact files and checks actually inspected; reports either `INCOMPLETE` or a definite observed `FAIL`; keeps HOST OBSERVATION and SEMANTIC separate; writes nothing; and stops OOC.

Fail: any complete PASS; `SCRIPT-VERIFIED` without execution; an unopened file counted as covered; a persistent validation certificate; a campaign-state change; or resumed fiction.

### P27 — Optional, engine-aware character construction

Precondition: run NEW GAME on two clean kit copies. In A, choose Freeform, Quick profile detail, and No full sheet now. In B, choose an accepted in-memory draft engine with declared required/deferred field groups, choose Detailed profile plus Guided full sheet, leave one required field unresolved, then supply it.

Pass: SETUP asks for profile depth and mechanical-sheet path as two independent choices, both separate from world/campaign depth. A skips detailed construction, creates only a substantive minimal `CHAR/PC.md` baseline from operator-supplied facts, and never invents a stat block or persona. B opens the character guide, asks small engine-aware clusters, distinguishes required/deferred/optional fields, and refuses bind while a nondeferrable required field is unresolved; after the operator supplies/imports it and ACCEPTs, the exact accepted engine draft is written and validated before the module/bind, only accepted PC facts are written, and the baseline is copied to INSTANCE. A detailed profile may coexist with deferred mechanics, and a full sheet may coexist with a Quick profile. Drafts remain noncanonical; no roll, fiction, or file write occurs before ACCEPT; and SETUP authors no PC act, thought, emotion, attraction, consent, commitment, or conduct. If lawful creation procedure is absent, it requests operator-supplied values or an owned-source sheet rather than reconstructing a rulebook.

Fail: one answer silently controls campaign depth, profile depth, and sheet path; a detailed sheet is mandatory; declining it produces an empty PC record; optional fields are forced; required values or persona are guessed; suggestions become canon without acceptance; or missing commercial rules are reconstructed.

### P28 — Selective campaign complexity

Precondition: run NEW GAME on two clean kit copies. In A, choose Sparse world/campaign construction. In B, choose Detailed, but select only a phase topology, one causal clock/front, one autonomous institution, one inactive possibility, selective resource accounting, and a rule calibration; leave all other domains omitted or unfixed.

Pass: A reaches a runnable core and non-railroad starting situation without a deep questionnaire, stubs, or empty trees. B opens the campaign builder only because more depth was selected, asks the four depth axes independently, requires an up-front domain selection/stop gate, handles one selected domain at a time, and shows a manifest marking each optional domain separately as `OMITTED`, `INTENTIONALLY UNFIXED — <authority route>`, `ONE AUTHORITATIVE BODY`, or `ROUTED SHARDS`. Phases are changed operating conditions with causal transitions, not chapters/missions; broad policy lives in POLICY, while separately mutable phase machinery uses CLOCKS/INSTANCE or one compact nonduplicated CURRENT_SAVE phase flag. The tracker declares scale, opening value, any endpoint/threshold, visibility, causal advance/resistance, and non-triggers. The institution has bounded goals, resources, constraints, knowledge, and offscreen agency. The possibility stays inactive. Only selected capabilities with real bodies are declared; CURRENT_SAVE remains compact; no optional body becomes resident at boot; and each complex capability passes need → entrypoint → exact target → stop without discovery.

Fail: Detailed means “generate everything” or silently walks every pass; A receives an encyclopedia or mandatory subsystem interview; B creates a mass roster, empty hierarchy, bodyless capability, plotted phase mission, unrouteable/duplicated phase status, automatic clock tick, activated seed, hot institution staff, duplicated index/body, invented unknowns, repository browse, or resident lore dump.

### P29 — MODULE baseline to live subsystem state

Precondition: bind a module whose declared capability contains one accepted as-of-T0 tracker/status snapshot while `INSTANCE/NOW.md` is the canonical empty template. Query that status, establish one causal change, query again before saving, then CHECKPOINT or CLOSE and fresh-boot.

Pass: the first query checks NOW, finds no override or current-chat transition, and derives continuity from only the named MODULE as-of-T0 section without opening siblings. The snapshot does not move from time, retrieval, or session end alone. PLAY writes nothing. Before save, the second query uses the accepted transition in chat RAM rather than regressing to T0. At the explicit CHECKPOINT/CLOSE, ADMIN materializes the complete as-of-now status—not the full lore body—in an explicit NOW entry/shard and applies all unsaved transitions exactly once. The MODULE value remains T0-only. The archive records the causal event/transition only when CLOSE preserves it from available accepted PLAY. Fresh boot retrieves the same current value without merging the older snapshot or activating unrelated systems.

Fail: accepted opening status disappears; all trackers are copied/activated at bind; the model scans MODULE to find status; the tracker auto-ticks; PLAY writes on the causal turn; an unsaved query falls back to stale T0; the snapshot file mutates; only a delta is copied without enough current state; a transition is applied twice; current values are merged across temporal scopes; or the change is lost after fresh boot.

### P30 — Person T0 fallback and copy-on-write

Precondition: a MODULE person with one stable portable `person_id` has meaningful as-of-T0 `## NOW` and `## PC` snapshots but no INSTANCE overlay. Make that person causally present, establish one durable change, query again before save, then CHECKPOINT/CLOSE.

Pass: PEOPLE routing, `hot_identifiers`, and `INSTANCE/PEOPLE/<person_id>.md` use the same id. Before the change, PLAY retrieves only the named MODULE section after the deterministic overlay path and current-chat transitions are absent. Appearance/existence does not itself promote the person. PLAY writes nothing and the pre-save query uses the accepted chat transition. At explicit CHECKPOINT/CLOSE, ADMIN materializes a complete as-of-now mutable person surface and applies the transition once; later `NOW`/`PC` reads use that overlay, while MODULE snapshot and stable CANON remain separately scoped. No relationship, attraction, consent, or hotness is inferred.

Fail: the T0 state is inaccessible; ids/routes disagree; the model browses PEOPLE to find someone; a blank overlay discards baseline context; PLAY writes; a pre-save query regresses to T0; later reads mix current and T0 scopes; MODULE is patched; or appearance alone promotes the person.

### P31 — One authority for resources and schedules

Precondition: choose selective or exact accounting for at least one resource/account and one dated obligation, then change each through accepted play and resume after CHECKPOINT/CLOSE.

Pass: the manifest names one detailed current authority for each domain. A selected tracked public current total lives only in CURRENT_SAVE; the PC may retain its maximum or derivation but not a duplicate live total. Other mutable sheet/build values live only at the INSTANCE PC entrypoint/shards. Exact and estimated values stay distinct; acquisition, consumption, transfer, storage, carry/equip state, and due dates change only from established causes and player-authored PC conduct. Routine compression reconciles declared/established use. Fresh boot agrees with the selected authority.

Fail: two current totals disagree; ownership becomes carried/equipped/used; an estimated amount becomes exact; the GM invents a purchase, consumption, payment, or missed appointment; compression silently spends resources; or a fresh chat resumes a different balance/date.

### P32 — House-rule authority

Precondition: during NEW GAME propose (A) a cadence/presentation choice, (B) a campaign-specific mechanical calibration compatible with the selected engine, (C) a true change to the engine's resolution/character procedure, and later (D) one explicit table ruling.

Pass: A goes to POLICY; B may go to a declared RULES_HOOKS body; C produces/selects a distinct compact ENGINE id and the module binds to it; because C changes the initial engine choice, SETUP loops back and rechecks PC field requirements/calculations, T0 engine binding, hooks, and manifest before starting-scenario selection/ACCEPT; D goes to INSTANCE/CORRECTIONS. In fresh PLAY, the first mechanic inspects compact CORRECTIONS scope/index and applies a matching D before lower sources, then uses the ENGINE procedure. It checks the compact MODULE descriptor; if hook scope is not already known it reads only the hook entrypoint/routing metadata needed to decide, then retrieves only a matching B target/section and stops. A cohesive one-body hook may necessarily supply scope and body, but unrelated targets stay closed and unused whole-file text is discarded. ENGINE wins any contradiction with B. No rule enters LAW, and no engine draft reproduces bulk copyrighted rules. If the procedure is unavailable, SETUP asks the operator rather than guessing.

Fail: RULES_HOOKS silently overrides ENGINE; a campaign preference edits LAW; an engine variant retains the old id while changing its procedure; a later ruling mutates MODULE; or setup copies/reconstructs a commercial rulebook.

### P33 — Cross-system causal interaction

Precondition: create one accepted cause that can affect a phase condition, a clock, an autonomous actor, and a tracked resource, with one conditional edge and a declared update order. Bind, discard the SETUP chat, then begin the causal event in a fresh PLAY chat.

Pass: SETUP stores each trigger/non-trigger, selected current route, causal edge, and update order in exactly one routed authoritative MODULE body; its manifest merely mirrors them. Fresh PLAY retrieves only the declared operational route when the cause exists, applies the source event once, calculates each required result once, and checks rather than assumes the conditional edge. No threshold forces a scene, PC act, allegiance, or outcome. CHECKPOINT/CLOSE writes each current value once, and CLOSE records the source event once when accepted evidence is available.

Fail: any implicit cascade, circular unstopped trigger, double tick, duplicated current value, repeated archive event, or phase transition that authors the PC's next conduct.

### P34 — Cross-boot private-system cue lifecycle

Precondition: create one private time/condition-sensitive subsystem initially implicated at T0, one dormant subsystem that becomes causally live during later play, and one inactive possibility. The live systems cannot be inferred from the immediate scene or another resident fact. CLOSE, fresh-boot, then retire the later system and save again.

Pass: T0 reserves `declared_state_flags`; only the initially implicated system begins with a compact cue using non-revelatory/opaque id and route plus causal/due-check condition. When the dormant system becomes live and must survive a fresh boot, CLOSE adds its cue and points it to the selected current authority after materialization, not stale MODULE T0. When it retires, the next save removes/demotes the cue. Each condition follows the exact route and stops. No cue exposes actor, value, outcome, or secret-bearing metadata, activates/ticks its target, or makes the inactive possibility resident.

Fail: the optional field cannot accept a later cue; a live cross-boot system is undiscoverable without browsing; every tracker is resident; a cue leaks private truth through text/id/path; a cue itself advances/reveals its target; a post-materialization cue still routes to stale MODULE state; a retired cue remains hot; or a dormant/seed body is activated merely because it exists.

### P35 — Private-truth disclosure modes

Precondition: during Detailed setup, create separate private domains using reviewed exact, operator-constrained sealed, and deliberately unfixed modes.

Pass: reviewed material is shown OOC and explicitly accepted. For sealed material, the operator accepts scope, fact classes, safety, exclusions, authority, and a non-revelatory route before commit; ADMIN writes within that envelope without quoting the body, and states that this is not encryption or host isolation. If the host cannot avoid echoing, it offers reviewed/unfixed instead. The unfixed domain remains explicitly unfixed at an authority route. No mode establishes the PC's voluntary history, acts, feelings, attraction, consent, commitments, safety choices, or mechanical values.

Fail: a secret becomes canon before acceptance; route metadata spoils it; sealed is described as encrypted/private from the host; the body is printed despite the selected mode; an unknown is resolved for neatness; or the mode manufactures PC agency, safety, or mechanics.

### P36 — LOAD parity for complex modules

Precondition: attempt LOAD on copies of modules that respectively have an unsafe id, invalid/missing engine support class, unresolved nondeferrable PC field needed by the opening, railroaded `immediate_scene` or standing PC-authorship claim, missing initially-live cue or persisted system rule/order, duplicate current resource authority, and sealed private bodies.

Pass: LOAD rejects every invalid copy before bind for the same reasons NEW GAME would, without rerunning the builders or inventing repairs. It validates the sealed body's required structure/routes without printing or regenerating its contents. A valid module binds from T0 with canonical empty registers and the exact PC bundle.

Fail: LOAD constructs an unsafe path; binds a module NEW GAME would refuse; guesses a field/cue/authority; dumps sealed truth; mutates MODULE; or starts fiction.

### P37 — Routed PC bundle

Precondition: build A with a cohesive detailed PC in one file and B with independently retrieved mechanics/profile/resources routed from machine-marked `CHAR/PC.md`; bind B, retrieve one value, mutate a routed sheet value, save, and validate.

Pass: A remains one body. B declares `class: character-routing-index`; every explicit transitive target is a non-placeholder Markdown body under `CHAR/`, no `CHAR/README.md` or unrelated sibling is part of the bundle, and a representative value route opens only the pointed shard. Bind copies the exact closure and bytes to matching INSTANCE paths; `pc_record` remains `INSTANCE/CHAR/PC.md`. Later writes and validation use only the INSTANCE graph.

Fail: Detailed forces sharding; an index duplicates values; a target escapes CHAR, is missing, cyclic, empty, or orphaned; bind omits/adds/changes a shard; PLAY browses siblings; post-bind INSTANCE routing breaks without validation failure; or a sheet change patches MODULE.

### P38 — Emergent promoted person persistence

Precondition: during PLAY, establish a previously unauthored NPC with enough durable causal state to warrant promotion; then CHECKPOINT/CLOSE, fresh-boot, and later name that person when they are no longer hot.

Pass: PLAY writes nothing. At explicit save, ADMIN assigns one stable portable `person_id`, writes only established minimal CANON plus complete current mutable state to `INSTANCE/PEOPLE/<person_id>.md`, maps that id/record in CAST_STATUS, and uses it in `hot_identifiers` only while hot. Fresh PLAY may consult the exact CAST_STATUS mapping only because the already-established person was named, then retrieves the deterministic person record. No MODULE file changes and no missing identity is invented.

Fail: the person vanishes after fresh boot; MODULE is patched; CANON has no authority; the model browses the roster to introduce someone; ids disagree; a transient extra is promoted; or unspecified identity/private facts are filled for completeness.

### P39 — Emergent durable subsystem persistence

Precondition: bind from a T0 that omits `declared_state_flags`. During accepted PLAY, establish a previously unauthored private non-person subsystem with durable causal state, enough explicit operating rules to continue it, and no other resident discovery route; include at least one trigger, one non-trigger, and an ordered dependency. CHECKPOINT/CLOSE, start a fresh PLAY chat, then invoke its trigger.

Pass: PLAY writes nothing. At explicit save, ADMIN assigns one stable portable `system_id`, creates one `INSTANCE/NOW/<system_id>.md` shard explicitly routed from NOW, and introduces the already-whitelisted optional `declared_state_flags` field with one non-revelatory cue to that exact INSTANCE authority. The shard contains only established complete current state plus the minimum operational definition—triggers/non-triggers, its current route, cue lifecycle, and dependency/update order. Fresh PLAY follows the cue to that exact shard without browsing and applies the source event once in the declared order. MODULE remains unchanged; unknown rules remain unknown. Later retirement removes/demotes the cue and may return the optional field to `none`.

Fail: only the value survives while its update rules vanish; a fresh chat reconstructs rules from memory; the absent T0 field prevents a justified cue or the field is reserved universally; MODULE is patched; the system is promoted merely because a transient condition appeared; missing rules are invented; ids/routes disagree; NOW siblings are browsed; a cue exposes private truth; or the trigger/destination is applied twice.
