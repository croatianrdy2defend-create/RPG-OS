# OS lifecycle tests

Fresh PLAY chat. Attach **only** the `RPG_OS` folder.

## Startup (find-free)

> Open only these five files, using those exact paths. Do not find, ls, search, or list the repository. Do not open ENGINE, MODULES, ADMIN, ARCHIVE, README, `OS/RETRIEVAL.md`, `INSTANCE/BEARING.md`, or any other AGENTS.md.
> 1. RPG_OS/OS/AGENTS.md
> 2. RPG_OS/OS/BOOTSTRAP.md
> 3. RPG_OS/OS/LAW.md
> 4. RPG_OS/INSTANCE/CURRENT_SAVE.md
> 5. RPG_OS/INSTANCE/CAMPAIGN_CONTRACT.md
> Confirm only that the runtime is ready and that no runnable campaign instance is bound. Do not begin a scene. Do not print filenames, a load-compliance recital, or copy instructions.

Pass: those five addressed files only; LAW, CURRENT_SAVE, and CAMPAIGN_CONTRACT are read as the resident authorities; ready; unbound; no fiction, repository discovery, filenames, or load-compliance recital in the reply.

## Test 0 — Unbound birth

Pass: ready; unbound; CAMPAIGN_CONTRACT is the canonical unbound template; no world, PC, date, place, NPC, or repository discovery.
Fail: any fiction; any `find`/`ls`/recursive search; any file beyond the five addressed paths.

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
Pass: concise locally appropriate function/texture, including honest solitude. Location or retrieval alone introduces no person. A fresh consequential person may be authored only as responsive realization or under an independent warrant/accepted creative mandate; ordinary function need not mint a durable identity.
Fail: the clerk/service worker becomes a hook merely because the location exists; or the GM refuses lawful fresh portrayal only because no NPC was prewritten.

### P2 — One name is not the ledger
Pass: that person section or one archive heading. Ledgers of other people stay closed.

### P3 — Quiet stretch
Pass: clear time/place/orientation and concise relevant texture; genuine solitude and zero novelty remain valid. If the beat is finished, say so once and ask whether the player uses any recorded uncommitted time or advances it. No quest, ambush, conspiracy, planted stranger, repeated void, or incident quota.
Fail: empty parser-style replies make the player supply the world; or liveness is used to manufacture a problem.

### P4 — Agency
Pass: GM never authors PC thought, attraction, consent, or an undeclared first act.

### P5 — Needle
Pass: after identifying the GM task, only routing indexes and source material sufficient and proportionate to that task are opened, then play returns to the present. Zero-result and zero-additional retrieval remain valid.
Fail: default starvation prevents GMing; retrieval precedes the task/authority question; or unrelated archive, roster, lore, Bearing, or preparation is dumped.

### P6 — AUDIT
Pass: OOC file/section list + reasons for the preceding non-AUDIT turn. Reports whether find/ls occurred. For archive retrieval, names the campaign index, session index, shard/heading, skipped levels, and any legacy monolith used. No fiction. No bodies.

### P7 — Checkpoint
Pass: CURRENT_SAVE overwritten via candidate; save_rev incremented; ARCHIVE/INDEX unchanged; confirmation states exact wording is not archived; not fiction.
Fail: ledger write; narrated checkpoint; implies checkpoint = CLOSE.

### P8 — Starting-scenario non-railroad
Pass: opening is a contract-appropriate playable frame with time, place, and enough orientation to act. An incident is optional. No authored PC act/thought/feeling/commitment and no “you already agreed.”
Fail: mandatory hook or dilemma; empty location with no orientation; or accepted premise is strengthened into prior PC conduct.

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
Pass: CHECKPOINT prints a new save_id; a fresh resident boot reads that same save_id and the matching accepted Campaign Contract.
Fail: no file write, or the new chat resumes the old save.

### P19 — Provider/write interruption
Simulate or observe a provider moderation refusal, write failure, or interrupted generation during (A) NEW GAME/LOAD bind and (B) CHECKPOINT/CLOSE. Also test (C) a syntactically valid candidate whose assembled write set has one missing/mismatched affected INSTANCE route or CLOSE evidence heading.
Pass: the interruption remains OOC and creates no fictional event. In A, CURRENT_SAVE remains unbound; partial ENGINE/MODULE/SAFETY/INSTANCE/candidate artifacts are not called canon or bound, and ADMIN either completes only the accepted manifest then validates the whole bind or restores a clean pre-bind copy before retry. In B, none of the refusal text enters state/archive; the previous CURRENT_SAVE remains the live pointer; and every separately affected INSTANCE/archive body is inspected and either consistent with that save or restored from external backup before PLAY resumes. In C, the prospective assembled-state check detects the defect before pointer replacement, CURRENT_SAVE remains on the prior commit, and P19 restoration begins. No branch claims automatic multi-file rollback.
Fail: the refusal becomes in-world dialogue; the campaign advances around it; a partial module, sealed body, PC bundle, or bind is treated as committed; an old/unbound CURRENT_SAVE coexists with live use of future INSTANCE state or a discoverable uncommitted archive route; the candidate pointer advances despite a missing/mismatched planned route or heading; PLAY resumes before consistency is established; or the previous save/state is lost.

v0.6 bind addition: CAMPAIGN_CONTRACT is published immediately before CURRENT_SAVE. If interruption leaves an accepted contract beside an unbound/mismatched save, boot fails closed and ADMIN repairs or resumes; the contract alone does not bind the run. BEARING remains the empty `status: none` record at bind. Unfinished CURRENT_SAVE, contract, or Bearing candidates are residue, never authority.

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

Pass: the untouched unbound kit exits `0`, labels STRUCTURAL as `SCRIPT-VERIFIED`, prints a deterministic path/type/content digest plus matching executed/target validator hashes, reports HOST OBSERVATION as `NOT RUN`, and reports SEMANTIC as `NOT CHECKED`. Repeating the run without byte changes produces the same digest and leaves the tree byte-identical with no report file. A separate copy with one valid `ENGINE/<id>/ENGINE.md` also passes engine identity checks.

Separate corrupted copies are detected for at least: a changed release LAW byte; target/executed validator mismatch; missing, empty, unreadable, or non-UTF-8 required file; a bound module with a missing/empty Setting Brief, wrong copied-module id/class, an unexpected front-matter field, missing/duplicate/out-of-order exact section, placeholder-only required section, or stale `SETTING_BRIEF.candidate.md`; unknown, duplicate, blank, or blank-line-hidden CURRENT_SAVE/T0/contract/bearing/index/ledger row; invalid v0.6 scene status or causal-frontier type; malformed, mismatched, unaccepted, self-parented, or noncanonical Campaign Contract identity/revision/axis/mandate; mandate `off` with scope or mandate `on` without scope/boundaries; invalid Bearing front matter/status/section set/id/revision/evidence scope; unbound or `status: none` Bearing residue; unfinished save/contract/Bearing candidate; decorated placeholder run identity, PC body, voice, safety line, or starting frame; illegal/case-normalized commit metadata or noncanonical revision digits; unbound/bind prior-run state in ARCHIVE or INSTANCE; escaping/dot/missing/non-Markdown route; missing/unsafe engine id, flat-stem/directory-name id mismatch, missing/invalid `class: engine`, or missing/invalid `character_build_support`; empty capability table/body or dangling machine-marked capability map; false or empty legacy voice heading; active-but-empty safety; a CLOSE route/folder mismatch or populated legacy column; missing session index/shard/heading; a structural heading/table present only in front matter, fenced/indented code, an HTML comment, or a raw script/pre/style/textarea block; a dangling module-section fragment; a malformed or 13-line route entry; a duplicate NOW hot roster; a broken, blank, ordinary-heading, wrong-save-id, or out-of-scope ledger pointer; and a PC route graph with a wrong root class, escape, missing/empty/cyclic target, bad fragment, orphan/reserved/non-Markdown/symlink shard, bind-time missing/extra/byte-mismatched copy, or post-bind broken INSTANCE graph.

A structurally valid provisional Bearing whose campaign/save/contract base no longer matches is reported as stale with a nonfatal warning and is not called current. A literal legacy evidence route remains reachable but is visibly warned as noncanonical, including several indexed headings in one retained legacy monolith. JSON mode is valid JSON and preserves the three evidence classes. Human mode escapes unencodable paths or messages rather than truncating the diagnostic.

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

Pass: A reaches a runnable core and non-railroad playable starting frame without a deep questionnaire, stubs, empty trees, or mandatory incident. B opens the campaign builder only because more depth was selected, asks the depth axes independently, requires an up-front domain selection/stop gate, handles one selected domain at a time, and shows a manifest marking each optional domain separately as `OMITTED`, `INTENTIONALLY UNFIXED — <authority route>`, `ONE AUTHORITATIVE BODY`, or `ROUTED SHARDS`. Phases are changed operating conditions with causal transitions, not chapters/missions; broad policy lives in POLICY, while separately mutable phase machinery uses CLOCKS/INSTANCE or one compact nonduplicated CURRENT_SAVE phase flag. The tracker declares scale, opening value, any endpoint/threshold, visibility, causal advance/resistance, and non-triggers. The institution has bounded goals, resources, constraints, knowledge, and offscreen agency. The possibility stays inactive. Only selected capabilities with real bodies are declared; CURRENT_SAVE remains compact; no optional body becomes resident at boot; and each complex capability passes need → entrypoint → exact target → stop without discovery.

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

Pass: LOAD rejects every invalid copy before bind for the same reasons NEW GAME would, without rerunning the builders or inventing repairs. It validates the sealed body's required structure/routes without printing or regenerating its contents. A valid module binds from T0 with canonical empty registers and the exact PC bundle. Before bind, MODULE defaults are offered only as proposals and the operator explicitly accepts a complete run-scoped Campaign Contract; LOAD never infers a mandate from tone, engine, complexity, or the existence of a module. It publishes the accepted contract immediately before CURRENT_SAVE.

Fail: LOAD constructs an unsafe path; binds a module NEW GAME would refuse; guesses a field/cue/authority or contract choice; silently accepts a creative mandate; dumps sealed truth; mutates MODULE; or starts fiction.

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

## v0.6 GM acceptance lane

P40–P50 are semantic, human/player-evaluated fixtures. The structural validator reports them as `SEMANTIC: NOT CHECKED`; they are never folded into SCRIPT-VERIFIED PASS. Run the lane through at least a quiet or slice-of-life campaign, a directed slow-burn, an open sandbox, and a protected-truth adventure/mystery. Score player experience separately from structural integrity.

### P40 — GM-first turn, invisible services

Precondition: in a bound scene, give a declaration whose intent and immediate GM task are clear; one authoritative nonresident fact is useful and several unrelated records exist.

Pass: the response visibly orients to the campaign and scene, answers the player's actual intent, retrieves only context sufficient and proportionate to that task, judges or portrays the world, and returns agency or closes. File routes, fact-class labels, warrant analysis, Bearing analysis, and rejected candidates do not leak into fiction. The player does not have to supply NPC initiative, ordinary world response, or the next verb merely to make the GM function.

Fail: navigation or a noun lookup becomes the apparent task; the response is a compliance recital, empty parser handback, repository dump, or invented quota event; or internal file/authority vocabulary appears in fiction.

#### P40a — Silent GM-work rendering

Precondition: a routine established activity includes a valid conditional player declaration. Its honest resolution requires no roll, new incident, complication, activation, or additional retrieval.

Pass: the response portrays the resulting world activity and its natural continuation, shows only mechanics that actually occur, and supplies the required public footer. It does not announce absent mechanics or events, justify compliance, or describe the internal selection procedure.

Fail: it says or paraphrases “no roll is required,” “nothing triggered,” “I checked only,” “the instruction authorizes,” “without expanding what the player said,” or otherwise certifies its own restraint without an explicit OOC request. Putting that compliance explanation into NPC dialogue also fails.

#### P40b — Fresh-chat setting awareness

Precondition: fresh-boot a bound module whose ordinary public reality visibly differs from generic model priors. The technical boot files do not contain its detailed lore. Begin PLAY, then ask a generic public-perception question such as “What do the commuters look like?” without naming the setting-specific difference or supplying a keyword for it.

Pass: before first fiction the GM loads the module's compact Setting Brief once and silently; the ordinary portrayal respects that baseline without requiring the player to remind it what world this is. It does not load or summarize the full WORLD capability, turn the foundational difference into a showcase, hook, clue, encounter, or representation quota, or recite the brief. It retrieves narrower authority only if the actual task needs exact, local, quantitative, disputed, private, or causally material detail.

Fail: the portrayal silently reverts to a generic-world default; the setting appears only after the player supplies its special keyword; the GM opens a lore dump for routine orientation; the brief is narrated as exposition or compliance; or setting awareness manufactures an incident or conspicuous showcase.

### P41 — Quiet orientation and clean closure

Precondition: an established situation has resolved during a quiet evening. The PC is genuinely alone, no incident is due, and a recorded interval of `uncommitted_time` remains.

Pass: the GM gives concise time/place/body orientation, permits true solitude and zero novelty, states once that the beat is finished, and asks whether the player uses the remaining interval or advances to the next accepted/due calendar beat. If the player advances, the GM does not invent conduct inside the skipped interval.

Fail: repeated “nothing happens” voids; a planted stranger, clue, rumor, or problem to prove liveness; exhaustive room inventory; a numbered action menu not requested by the player; or silent consumption of uncommitted PC time.

### P42 — Paired fresh creation / no activation (F5a + F13)

Precondition: use one campaign state with `creative_mandate: off` and one cold inactive candidate whose content fits the campaign. First, the player explicitly and knowingly asks the GM to author **new** campaign-consistent material inside the accepted envelope. Immediately afterward, at a separate boundary with no responsive trigger, external warrant, or mandate, expose or retrieve the old cold candidate for the probe only.

Pass: in the first half, the GM supplies a fresh lawful realization; it does not refuse because no file prewrote it, answer only with the stored candidate, or use “none” to evade the accepted authorship request. A hard-boundary impossibility is explained OOC. In the second half, the retrieved candidate remains inactive and absent from fiction; fit, retrieval, liveness, and the boundary do not become warrants. Passing one half does not cause overcorrection in the other.

Fail: clerk refusal or candidate substitution in the first half; candidate activation, post-hoc self-warrant, or invented supporting condition in the second; or treating either permission as an incident quota.

### P43 — Contract axes and mandate independence

Precondition: create four accepted contracts: A has proactive initiative/variable pressure but mandate off; B has quieter axes and an explicitly accepted bounded mandate on; C has mandate on but the current moment is outside its accepted scope or boundary; D receives an explicit player request or other external warrant for prospective material outside the accepted fit envelope.

Pass: A's labels calibrate judgment but do not authorize a specific proactive situation. B permits, but never requires, a fresh in-scope introduction at an eligible boundary. C does not use the mandate outside scope/boundary. D does not treat warrant as permission to waive the envelope: already-established facts and consequences remain real, while a request to change accepted campaign kinds is handled OOC through explicit recalibration. In all four, an independent external warrant may authorize only a development that also remains within the accepted prospective-authorship envelope, and Bearing never supplies the warrant or mandate.

Fail: proactive, pressure, structural direction, fit, a scene boundary, or a Bearing direction silently becomes a creative mandate; warrant/request is treated as overriding fit or hard boundaries; established facts are erased to preserve fit; mandate becomes a quota; or mandate wording queues a named scene/person/object.

### P44 — Causal frontier and world motion

Precondition: CURRENT_SAVE carries one operative consequence, one specific due condition, one established live process, one pending decision, one exact PC-declared goal, and one unrelated durable open matter outside `causal_frontier`. Advance to a point where only some declared causes fire.

Pass: the GM orients from the compact frontier, follows detailed authority only for the actual task, advances each fired process once in its declared order, leaves non-triggered entries unchanged, and never treats a due check as a predetermined outcome. The PC goal is used only as declared fictional causality, not desire or consent. The unrelated open matter remains real but inactive; absence from the frontier is not asserted as nonexistence. PERSIST compiles the new frontier without forecast, Bearing, preparation, or duplicate current authority.

Fail: retrieval/session end ticks a process; an entry applies twice; a cue reveals private content or activates its target; a due condition forces PC conduct; an absent entry is declared nonexistent; or the frontier becomes a plot outline/routing dump.

### P45 — REVIEW isolation, bases, and staleness

Precondition: after a successful CHECKPOINT/CLOSE with `review_mode: bearing-only`, run REVIEW and publish a valid provisional Bearing. Then change the save through PERSIST and, separately, change the accepted contract through RECALIBRATE without rewriting that Bearing.

Pass: REVIEW reads proportionate evidence, keeps its seven lanes distinct, may conclude `no stable pattern yet`, and writes only BEARING through a candidate replacement. It does not mutate CURRENT_SAVE, CAMPAIGN_CONTRACT, MODULE, ARCHIVE, safety, people, clocks, or activation cues. After either base changes, the old Bearing is stale by comparison and omitted from PLAY without blocking the campaign or being rewritten merely to label it stale. With `review_mode: off`, a stored provisional Bearing is ignored.

Fail: REVIEW runs before a successful PERSIST, writes canon or preparation, infers OOC preference/PC goal from conduct, advances a system, makes a direction happen, corrupts a valid save on failure, or stale/disabled Bearing is used as orientation or authority.

### P46 — Refusal and course change

Precondition: the player clearly refuses an apparent direction, then declares a materially different course. Some prior established consequences remain independently operative; other prepared or provisional material depended only on the refused direction.

Pass: refusal stands with no punishment plot or disguised repetition. Independently established consequences may still resolve on their own terms. The new course receives normal GM framing and consequence. At the next REVIEW, interpretation revises and incompatible directions lose even provisional relevance; merely compatible material remains inactive and unentitled.

Fail: the refused content returns under a renamed hook, refusal is treated as consent/disinterest/character belief, all world consequence freezes, or REVIEW preserves a destination by rewriting the player's conduct.

### P47 — Protected-truth mystery, no retrofit

Precondition: fixed private truth says a searched place has no clue; an earlier ordinary detail was established without clue status; a rumor and an unresolved question also exist. The campaign prioritizes mystery and a provisional Bearing expects progress.

Pass: the search may honestly find no clue. The ordinary detail is not retrospectively converted into evidence; the rumor remains only heard; the unresolved matter remains unresolved. A new clue may arise only prospectively through an authorized situation that does not contradict the fixed truth. Bearing and pressure settings do not override evidence.

Fail: absence is treated as GM failure and patched with a clue; old texture is retconned; rumor becomes truth; mystery priority becomes a warrant; or REVIEW changes historical evidence to preserve a trajectory.

### P48 — Consent and PC interior

Precondition: the player makes an ambiguous or offhand remark that another character could read flirtatiously, then an NPC action would require the PC's attraction, consent, or continuing willingness.

Pass: only the spoken words and any objective delivery the player supplied are established. The NPC may interpret and respond within their own knowledge, but the GM does not establish the PC's attraction, desire, meaning, consent, or commitment. The next voluntary PC decision is returned to the player. No die result, Bearing inference, observed conduct, or campaign priority fills it.

Fail: ambiguity is upgraded to consent; prior participation becomes continuing consent; a roll creates willingness; or the GM narrates the PC's internal reaction or voluntary follow-through.

### P49 — END SESSION transaction and failure isolation

Precondition: run END SESSION on three disposable copies: A succeeds; B fails during CLOSE/PERSIST; C completes CLOSE but REVIEW then fails or is interrupted.

Pass: A runs CLOSE first, publishes CURRENT_SAVE last, then runs REVIEW only when the accepted contract says `bearing-only`, reporting PERSIST and REVIEW separately. B stops before REVIEW and retains/restores the prior valid current pointer under the existing recovery rules. C keeps the successful save and archive authoritative and resumable; failed REVIEW publishes no fixed Bearing and does not roll back, qualify, or contaminate CLOSE. With review off, END SESSION stops after CLOSE.

Fail: REVIEW runs before/after a failed PERSIST; failure text enters fiction/state/archive; a partial Bearing becomes authority; successful CLOSE is rolled back because REVIEW failed; or END SESSION is treated as a third persistence kind.

### P50 — Fresh-chat resume with, without, and despite Bearing

Precondition: boot disposable copies of the same valid bound campaign with A a matching provisional Bearing and `review_mode: bearing-only`; B `status: none`; C a stale or malformed Bearing; D a provisional Bearing while `review_mode: off`.

Pass: every copy loads the same GM Core, accepted Campaign Contract, authoritative CURRENT_SAVE, and required compact module Setting Brief without inventing an interval or loading detailed lore. A may use Bearing only as provisional orientation and gives it no warrant or factual authority. B resumes as a living GM from Contract plus Save and Setting Brief rather than becoming passive or generic-world. C ignores stale content, reports a concise OOC warning when required, and remains playable; a structurally unsafe bound authority still fails closed rather than being guessed. D does not open/use Bearing. Scene status, causal frontier, and uncommitted time produce the correct frame or clarification.

Fail: missing Bearing blocks play or creates clerk vacuum; current Bearing activates a direction; stale/disabled Bearing affects fiction; a new chat invents an off-screen chapter; or campaign continuity depends on reopening the full archive.

### P51 — Bound v0.5 migration transaction

Precondition: make disposable copies of one valid bound v0.5 campaign whose last accepted play was PERSISTed and whose MODULE, ENGINE adapter, INSTANCE facts, archive indexes/ledgers, and scene evidence are known byte-for-byte; the legacy module has no Setting Brief. Install the v0.6.2 runtime/generic contracts and canonical unbound Campaign Contract plus empty Bearing templates without replacing those campaign authorities. Keep a byte-for-byte external backup. Run `MIGRATE V0.5` on A and ACCEPT an exact compact Setting Brief, explicit Contract values, and explicit `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier`. On B interrupt before publication; on C introduce mismatched identity, candidate residue, missing backup attestation, a malformed pre-existing brief, or unsaved-post-save play.

Pass: A preserves all legacy campaign facts, allowed Current Save fields, campaign-owned MODULE content, compatible engine authority, and ARCHIVE indexes, ledgers, and evidence; it neither reshards nor reinterprets history. Its only MODULE addition is the explicitly accepted required Setting Brief, which contains no current/private/queued material or detailed-lore copy. The accepted Contract has the same `campaign_id` and module, revision 1, and only operator-accepted axes/mandate. The new Current Save adds exactly the four v0.6 orientation fields, uses a fresh `save_id`, increments `save_rev`, names the old id as `save_parent`, sets `commit_kind: checkpoint` and `archive_ref: none`, and retains every other established value. A bound identity-only Bearing is `status: none`. Candidates validate before publication; the brief publishes when required, Bearing publishes next, then the accepted Contract immediately before CURRENT_SAVE publishes last. A fresh five-file boot, bounded pre-fiction Setting Brief load, and VALIDATE succeed. B retains or restores the complete prior authoritative v0.5 tree. C fails closed before authoritative publication and directs the operator to save under v0.5 or restore/inspect rather than guessing.

Fail: migration uses LOAD or ordinary CHECKPOINT as implicit Contract authority; overwrites module material beyond the accepted missing Setting Brief, overwrites engine/archive/legacy facts, or guesses the brief from genre; infers a PC goal, causal item, mandate, or Bearing direction; gives old archive text new authority; loses save lineage; publishes CURRENT_SAVE before the accepted Contract; leaves a partial/candidate record authoritative; proceeds without a backup or across unsaved play; or claims an automatic merge it did not verify.

### P52 — Bound v0.6/v0.6.1 missing-brief upgrade

Precondition: install the v0.6.2 generic runtime over disposable copies of an otherwise valid already-bound v0.6 or v0.6.1 campaign whose module has no fixed or candidate Setting Brief. Ensure all accepted PLAY is PERSISTed and keep a restorable byte-for-byte backup outside each active folder. On A explicitly run `UPGRADE SETTING BRIEF`, review a complete draft supported only by already-authoritative stable public module facts, and answer `ACCEPT SETTING BRIEF`. On B omit a required attestation or leave accepted PLAY unsaved. On C provide a malformed fixed brief, candidate residue, resident mismatch, unrelated structural defect, unbound/v0.5 source, or unaccepted/revised draft.

Pass: A's explicit command dispatches to ADMIN before normal boot rejects the missing brief and never starts fiction. Existing bound authorities validate apart from that one absence. The complete draft has the exact module-scoped id, class, headings/order, concise substantive public bodies, and no inferred, current, private, roster, detailed-lore, tracker/phase/seed, preparation, or plot material. Nothing is written before exact acceptance; afterward the identical body is staged, focused-validated, published at the fixed path, byte-compared, and the candidate is removed before full-tree validation. The Setting Brief is the only changed path: save, contract, Bearing, every other MODULE file, ENGINE, INSTANCE, ARCHIVE, safety, and ledgers remain byte-identical and no revision is minted. A fresh normal boot succeeds. B and C write nothing and fail closed with the specific repair/restore path; a malformed existing brief is never overwritten by this command.

Fail: missing-brief detection auto-runs the upgrade; PLAY occurs; backup or persistence is assumed; an unbound, v0.5, mismatched, partial, or otherwise invalid run is normalized; a malformed fixed brief or stale candidate is overwritten; genre, prior-chat memory, archive events, private truth, or completeness pressure supplies new facts; a lore summary is copied; draft acceptance is inferred; publication changes another path or revision; candidate/fixed bytes differ; candidate residue remains; final validation is skipped or overstated; or the old runtime is resumed after an uncertain partial write.
