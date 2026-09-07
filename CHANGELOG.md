# Changelog

## v0.9.0 — 2026-09-08

- Added optional exact-source reader with original lines, revision hashes, scoped section selection and delivery receipts.
- Added optional disposable SQLite FTS5 search with scoped candidates, current-source verification and safe rebuilds.
- Added untouched text/JSONL capture, selected prior/current audit bundles, pending report templates and mechanical citation/report checks; semantic review remains a separate model/human task.
- Integrated optional evidence review after full saves without changing CHECKPOINT, current record formats or ordinary startup. Added compact NPC portrayal and omission/retirement review examples.
- Expanded the mechanics guide, installation and compatible-upgrade instructions, public-package exclusions and regression checks.
- Corrected the initially published v9.0.0 label to the intended v0.9.0; the workflow verifies the corrected publication before retiring only that mistaken release and tag. Earlier release labels below remain historical.
- Fixed false source-change reports from differing Windows Python 3.12 path/handle timestamp representations, retaining identity and before/after mutation checks. Added four focused reader regressions. Features and record formats are unchanged. See [release notes](V0.9.0_CHANGES.md) and [verification](VERIFICATION.md).

All notable RPG OS prototype releases and design milestones are recorded here. The project is in public testing; version labels describe protocol releases, not proof of long-campaign reliability.

## Unreleased

No changes currently listed.

## v8.1.1 — individual baselines on direct attention (2026-09-07)

- Establish or retrieve a minimal current individual baseline when the player singles out an NPC for direct attention or interaction, or an NPC directly engages the PC, before focused portrayal or reaction resolution. A bare approach requires no inferred or declared PC purpose.
- Separate pre-existing individual circumstances from what the NPC perceives and the first impression or response formed now. Attention creates no additional PC conduct or automatic NPC awareness; private state remains distinct from PC knowledge.
- Reuse existing individuals and deepen only as actual developments require. Tiny service encounters require no full profile, mandatory field inventory, crowd initialization or automatic durable record.
- Preserve ENGINE authority and the selected fallback. Descriptive traits supply no invented numerical modifiers; one reaction is not resolved twice, and motives are not invented after a result to explain it.
- Update the nine-diagram mechanics guide, setup/upgrade guidance and optional B16 human diagnostics. This is an incremental instruction update from v0.8.1; save, agreement, archive, handover and person/system formats remain unchanged. See V8.1.1_CHANGES.md and VERIFICATION.md for scope and evidence.

## v0.8.1 — simple standing random fallback (2026-09-07)

- Add a simple standing fallback oracle for eligible unauthored outcomes with too little basis for grounded judgment: frame a bounded question and use actual random input. The supplied convention is one d6, 1–3 No and 4–6 Yes; facts, applicable rules and other accepted methods retain priority.
- Resolve relevant open matters before settling elapsed-time outcomes, including inaction. Preserve the question, actual input and scoped result through existing owners, without NPC dossiers, a scheduler, per-roll permission or automatic saving.
- Document examples for contact, promises and secrets, first-interruption behavior and honest audit gaps. Add optional regression scenarios; human replay of the revised behavior remains untested.
- Explain one-time selection in setup or a prospective agreement change. Installing this patch does not silently change a diceless campaign, another selected oracle, established facts or saved history.
- Update current release guidance and the nine-diagram mechanics guide. Existing record formats, Freeform-only distribution and public unbound campaign templates remain unchanged. See V0.8.1_CHANGES.md and VERIFICATION.md for scope and evidence.

## v0.8.0 — integrated agent state, experimental playtest release (2026-09-07)

- Added a compact core rule and cold agent-state procedure using existing person/system authorities, without new required fields or startup reads.
- Connected independent portrayal, causal change, actual randomness and eligible initialization through setup, worldbuilding, character construction, binding, saving, resumption and handover.
- Preserved accepted relationships, individual variation, real initiative and meaningful influence. Repeated equivalent attempts and unperceived OOC hopes do not create automatic progress or resistance.
- Added a protected v0.8 upgrade path preserving previous campaign/runtime copies and existing record formats; no retrospective cast generation or baseline rewriting.
- Kept interrupted setup determinations reachable through the active recovery operation until the bind completes or the setup is explicitly cancelled/replaced, including after physical restoration of the starting files.
- Reworked Quick start and installation guidance, added a real-campaign playtest guide, and expanded the illustrated mechanics guide to eight diagrams.
- Fixed Windows release-archive line-ending conversion while retaining exact committed-blob checks, and repaired the public issue form's version field while accommodating brief play incidents.
- Kept structural, recovery and packaging checks while making ordinary human campaign play the primary next evaluation of quality. Optional diagnostics remain available; no scripted behavioral pilot schedule is required before playing.
- Retained ordinary requested-save/checkpoint semantics. New unsaved private state remains best-effort; no automatic protected-establishment experiment, new live-state layer or receiver writes to frozen source are included.
- Preserved the unbound fresh-install package, Freeform-only engine inventory and provider-neutral campaign wording. See V0.8.0_CHANGES.md and VERIFICATION.md for scope and observed evidence.

## v0.7.3 — live scene handover and illustrated mechanics (2026-09-06)

- Added optional live scene export, explicit receiving-GM activation, factual return, protected import, and cancellation. The source pauses at the pending choice; ordinary CHECKPOINT and archive evidence boundaries retain their meaning.
- Separated accessible conversation from established GM state, including hidden facts, NPC knowledge and motives, mechanical values, unresolved events, and source gaps. Transfers never claim to capture unavailable history or model-internal reasoning.
- Added snapshot manifests, hashes, export seals, return identity checks, and import receipts to detect mismatched or stale transfers and prevent applying the same return twice.
- Added a read-only handover checker and regression fixtures. The main validator now reports active handovers and identifies itself as VALIDATE-v3.0.2.
- Published a detailed mechanics guide with seven Mermaid diagrams, a workspace tree, and a prominent README card.
- Carried the current provider-neutral runtime wording into the generic kit; accepted operator limits and player authorship remain campaign choices, without a bundled provider-specific depiction policy.
- Added VERSION, fresh-install packaging checks, a release ZIP/checksum workflow, and CI coverage for all three Python test suites.
- Distributed only a blank, unbound campaign and the Freeform engine. No campaign module, character, session history, private preparation, or campaign artwork is included. Valid v0.7.1/v0.7.2 campaigns need no state-format migration.

## v0.7.2 — optional portrayal and hidden-information preparation (2026-09-05)

- Added two optional cold preparation aids with original examples: recurring-person portrayal anchors and consequential hidden-fact/investigation notes.
- Integrated them selectively into NEW GAME without new required fields, files, interview rounds, or normal-startup reads.
- Made the consequential-authority check explicit before drafting while preserving ordinary invention and accepted continuation.
- Clarified preservation of misleading utterances, actual audiences, established private truth, and qualified NPC beliefs through saves and corrections.
- Added a reproducible controlled trial protocol; observed results and limitations belong in VERIFICATION, separately from proposed fixtures and structural checks.
- Retained the v0.7.1 save/contract shape and existing optional validator. Existing campaigns need no record-format migration or retrospective preparation.

## v0.7.1 — agreement and recovery repairs (2026-09-05)

- Added five required named prose clauses within the existing agreement sections, preserving plain-language grants and optional A–E presets.
- Separated form selection from structure disclosure; preserved truthful opacity envelopes and operative concealed selections across restarts.
- Clarified accepted fixed structure, lived-continuity defaults, scoped hard cuts, ironman versus genuine error repair, and OOC off-premise handling.
- Separated product/host depiction restrictions, operator limits, PC authorship, and fictional morality/NPC conduct.
- Recorded newly created directories during recoverable operations and added safe empty-directory restoration without recursive deletion or weaker orphan checks.
- Fixed two malformed validator provenance diagnostics and added failure-path, directory-restoration, and agreement-clause regressions.
- Added proposed opacity, ironman, cut, and premise behavioral fixtures; live-play results remain unrun.
- Restored project attribution and third-party-rights scope; documented the absence of complete referenced-record version pinning.
- Kept the v0.7 save layout; existing v0.7 agreements use focused accepted supplementation rather than current-state migration.

## v0.7 — simpler operation and universal progressive setup (2026-09-05)

- Retained rules, world, current-state, knowledge/private-state, and historical-evidence separation.
- Rewrote the GM core, ordinary startup, and targeted retrieval instructions.
- Replaced mandatory calibration axes with a concrete five-section campaign agreement.
- Replaced the current-save state-field cluster with five readable sections and independent present/evidence metadata.
- Made SAVE, CLOSE, and END SESSION the same complete ordinary save; CHECKPOINT retains the preceding evidence boundary.
- Added recovery records, verified prior copies, an active-operation marker, and operational restoration instructions.
- Added natural-language correction and simplified prospective agreement changes.
- Made NEW GAME progressive through Quick start, Guided, or Detailed setup while keeping world, rules, profile depth, mechanical readiness, and authority independent.
- Resolved accepted voice/source expectations and module limits at bind so ordinary PLAY need not load POLICY.
- Made Bearing cold and optional, with no automatic review after saving.
- Allowed bounded subject search when an exact needed route is missing; kept source evidence and current-state precedence.
- Added explicit older-campaign upgrade mapping and preserved legacy archive readability.
- Updated the read-only validator and synthetic regression tests for the changed records and recovery boundary.
- Remains an experimental unbound kit with Freeform only; structural testing does not establish live GM performance.

## v0.6.3 — world calibration and portrayal routing

- Expanded the existing three-heading Setting Brief semantics without adding a resident file or changing its schema
- Made world identity scope-aware: original/homebrew, historical/real-world, source-bound, or hybrid basis; opening operating scope; and foundational differences generic model priors could erase
- Made “what is ordinary” a creative prior with contextual variation and optional qualitative prevalence, not a requirement to display one example of every world category in each scene
- Distinguished incidental background portrayal, which may use the resident brief, from materially concrete module-defined portrayal, which retrieves the smallest governing cold authority
- Required fixed individual traits to survive type-level lore retrieval and prohibited generic genre defaults when relevant module authority is available
- Reworked NEW GAME around one adaptive World Operating Baseline covering reality, scope, personhood, variation, generic-default hazards, and fidelity boundaries across radically different campaign types
- Extended source-policy questions from historical campaigns to externally defined/source-bound settings while keeping copyrighted sourcebooks and unsupported model reconstruction out of the build
- Strengthened campaign construction around what may be improvised, what requires exact authority, what remains unfixed, and the smallest retrieval route
- Added paired semantic fixtures for natural background variety versus checklist portrayal, narrow on-demand lore retrieval, established-person preservation, and lawful homebrew improvisation
- Added optional backup-first `REFINE SETTING BRIEF` for a valid bound campaign; after exact `ACCEPT REFINED SETTING BRIEF`, it may replace only that brief using already-authoritative stable public module facts and cannot create new canon
- Existing valid v0.6.2 Setting Briefs remain structurally compatible; refinement is optional
- Kept LAW, the five-file technical boot, Campaign Contract and Current Save field schemas, engine architecture, archives, clocks, phases, Bearing, and NPC promotion unchanged
- The public package remains unbound, contains no campaign world, and bundles only Freeform

## v0.6.2 — session-start setting awareness

- Added one required compact `MODULES/<module-id>/SETTING_BRIEF.md` for every bound module
- Kept the five-file technical boot unchanged; BOOTSTRAP loads the Setting Brief once before first fiction
- Defined three narrow contents: world identity, foundational facts describing what is ordinary, and available cold depth
- Explicitly excluded current mutable state, named rosters, seeds, clock or phase bodies, private truth, prepared scenes, detailed lore, and plot queues
- Kept detailed world material cold and task-retrieved; loading the brief grants no activation authority
- Updated setup, loading, migration, structural validation, and semantic fixture P40b for keyword-free setting awareness without lore dumping or forced showcase scenes
- Added backup-first `UPGRADE SETTING BRIEF` for existing bound v0.6/v0.6.1 campaigns; it displays the complete brief and, after exact `ACCEPT SETTING BRIEF`, writes only the previously absent module file
- The public package remains unbound, contains no campaign world, and bundles only Freeform

## v0.6.1 — silent GM-work rendering

- Added an explicit render boundary between internal GM work and player-facing PLAY output
- Required PLAY to omit retrieval narration, authority checks, rejected alternatives, absent-mechanics explanations, and self-certifying compliance prose unless OOC clarification is actually needed
- Added semantic fixture P40a for silent resolution of ordinary established activity
- No campaign world, save, archive, or engine content changed

## v0.6 — GM-first runtime and separated campaign stewardship

- Reframed the runtime around a positive GM Core: orient to campaign and intent, identify the GM task and authority, then retrieve enough to imagine, judge, portray, and return agency or close
- Added a separately authoritative, run-scoped `INSTANCE/CAMPAIGN_CONTRACT.md` for the accepted campaign promise, fit envelope, six calibration axes, explicit creative-mandate scope/boundaries, and `review_mode`
- Expanded `INSTANCE/CURRENT_SAVE.md` with `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier` so a fresh chat receives an established causal present rather than only ledger state
- Added optional warm `INSTANCE/BEARING.md` as a provisional, noncanonical reading of campaign direction; it is usable only when its base save and Contract identities/revisions match
- Separated **PERSIST** from **REVIEW**: CHECKPOINT/CLOSE record authoritative state and evidence, while REVIEW may update only Bearing after a successful PERSIST
- Added `RECALIBRATE` for explicitly accepted prospective Campaign Contract changes; recalibration never rewrites history and invalidates older Bearing
- Added explicit `MIGRATE V0.5` ADMIN conversion for backed-up bound v0.5 campaigns; it preserves campaign authorities and archive evidence, accepts the first v0.6 Contract and four orientation fields, and publishes a checkpoint-lineage save rather than pretending normal LOAD or CHECKPOINT can perform the upgrade
- Added `END SESSION` as CLOSE first, then REVIEW only after CLOSE succeeds and only when `review_mode: bearing-only`
- Made retrieval task-first and sufficient/proportionate rather than default-zero as a virtue; retrieval still never activates content
- Distinguished responsive GM duties from discretionary introductions, and compatibility (“fit”) from independent warrant or accepted creative mandate
- Preserved quiet play, solitude, refusal, honest no-change outcomes, and player ownership while requiring playable orientation and an autonomous world
- Retained OS / ENGINE / MODULE / INSTANCE / ARCHIVE storage boundaries, retrieval-local archives, optional campaign machinery, and structural validation as supporting services
- The public package still contains no campaign world and bundles only Freeform; other systems may use lawful compact local adapters but are not shipped
- Durable preparation is deliberately not included in v0.6. Bearing is not a hidden plot queue, and fresh lawful realization remains available
- Known limits remain explicit: single-context prose enforcement, no recovery of unsaved chat, non-atomic multi-file writes, host/provider dependence, and no Session-100 proof
- This entry describes the v0.6 testing design; it is not a claim that final structural, semantic, host, or long-campaign validation has passed

## v0.5 — optional construction and complex-campaign lifecycle

- Added separate optional character and campaign builders: Quick/Standard/Detailed/Custom profile depth, independent deferred/minimum/full/import sheet paths, and Sparse/Focused/Detailed/Custom campaign depth
- Added generic authoring guidance for phase conditions, causal clocks/fronts, autonomous actors, inactive possibilities, relationship dimensions, resource precision, visual authority, and house-rule placement
- Added as-of-T0 snapshot → current-chat transition → next explicit save lifecycle, with one selected current authority and no resident lore dump
- Added P27–P39 for optional construction, routed PC records, complex-campaign lifecycle, causal interactions, private-system cues, spoiler modes, LOAD parity, and emergent person/system persistence
- Documented the remaining multi-file transaction boundary instead of treating CURRENT_SAVE-last as filesystem-wide atomicity
- No host profile, automatic archive threshold, recursive root-index protocol, persistent validation certificate, or PLAY scratch log
- No LAW change
- The public GitHub package ships Freeform only. The earlier compact GURPS adapter is not distributed; users may add lawful local engines through the generic ENGINE contract.
- Added public GitHub documentation, a command cheatsheet, contribution/test-report templates, read-only CI validation, and explicit CC BY 4.0 / MIT licensing.

---

## v0.4 — executable structural validation

- Added ADMIN-only `VALIDATE` and dependency-free `TOOLS/validate.py`
- Script checks deterministic release/validator identity, LAW, save, clean initial INSTANCE state, engine, bound module using v0.4 descriptor grammar, safety, archive-route, heading, ledger, path, and named residue invariants without writing the tree; P19 still tests interrupted ADMIN transactions
- Output separates STRUCTURAL, HOST OBSERVATION, and SEMANTIC evidence; script execution is `SCRIPT-VERIFIED`
- No-code fallback is `MODEL-CHECKED`, states exact coverage, and cannot report a complete PASS
- Added deterministic scanned-tree digest, stable diagnostics, optional JSON output, and exit statuses `0` / `1` / `2`
- Added exact v0.4 MODULE descriptor, archive path, literal-heading, and 12-line route-entry grammar needed for honest mechanical validation
- Bind now requires an empty run archive, assigns fresh portable campaign/save identities, and validates the completed candidate before CURRENT_SAVE replacement
- Clarified that later ADMIN may revise routing or losslessly repartition evidence without rewriting or reinterpreting it
- Added P25–P26 for scripted validation and fallback honesty


## v0.3.2 — hierarchical scene archives

- Added `ARCHIVE/_SCHEMA.md` with archive schema `hierarchical-scene-v1`
- Adapted `ARCHIVE/INDEX.md` as the sparse campaign-level router
- Future CLOSE writes a compact session/slice INDEX plus semantic scene shards
- Promoted retrieval locality into the cross-domain design doctrine in `ARCHITECTURE.md`
- Added indexed-authority rules to MODULE, INSTANCE, ENGINE, New Game, LOAD, and PLAY routing
- Defined stable capability entrypoints, explicit cross-links, recursive routing only when useful, and no arbitrary split threshold
- Exact-detail questions must reach a source shard; indexes remain routing metadata
- Message and relationship ledgers point directly to stable shard headings
- Added legacy DELTA/TRANSCRIPT/MESSAGES compatibility without mandatory migration
- Added P20–P24 for sharding, source authority, nonactivation, legacy compatibility, and general retrieval locality
- CHECKPOINT remains cheap and writes no archive
- No campaign world or active state migrated
- No LAW change
- No new kernel machinery


## v0.3.1 — provider-risk hardening

- Added provider-policy and account-risk warning
- Added offline canonical-copy guidance
- Added P19 provider-interruption test
- Defined moderation/refusal or generation interruption during ADMIN as a failed transaction
- Updated host examples; P17/P18 remain the capability test
- No LAW change
- No new kernel machinery


## v0.3 — design guide and write preflight

- Version stamp v0.3
- This README: definition, origin, purpose, runtime, strengths, weaknesses, history, changelog
- P18 persistent-write preflight: CHECKPOINT save_id must survive a fresh four-file boot
- No LAW change
- No new kernel machinery


## v0.2 — P0/P1 close-out

Auditor of previous zip: STILL BLOCKED on execution contradictions. v0.2 closed:

- Canonical engine id `gurps4e` only; alias enumeration forbidden
- Candidate save; archive-first, CURRENT_SAVE last; INDEX `save_id` + `archive_ref` boot match (v0.3.2 also validates the session-index route; INDEX not opened at four-file boot)
- NEW GAME / LOAD refuse if bound; never empty ARCHIVE
- ACCEPT/LOAD validation checklist; capabilities only with bodies
- SAFETY flag-gated; New Game writes limits; POLICY safety with voice; NPC silence
- PC overlay at bind; no MODULE mutation fallback
- Typed archive routes; stable heading ids; `event_heading`
- CLOSE follows `_SCHEMA` compilation matrix; `hot_identifiers` only on the save
- AUDIT = previous non-AUDIT turn
- Section preflight (honestly weak); physical context isolation remains unproven
- Campaign-specific names and setting residue removed from the clean kit

Auditor: **READY WITH MINOR CHANGES.** LAW byte/semantic freeze requested; kernel not reopened for genre.


## v0.1 — first clean public prototype

- Unbound skeleton, GURPS + Freeform engines, SETUP, CLOSE, TESTS, QUICKSTART.
- Starting-scenario requirement in New Game.
- Claude-driven tester levers: AUDIT, CHECKPOINT, `save_rev`/`save_parent`, `INSTANCE/SAFETY.md`, mid-play tests P1–P7, one-page QUICKSTART.


## Design freeze (no public zip)

- Greenfield V2: preserve lore/principles, not file ancestry.
- Universal OS + GURPS engine + campaign module.
- INSTANCE split out of MODULE.
- Optional capabilities; module-declared voice; no LAW literary fallback.
- Unbound Test 0 / 0b / 0c / adversarial improvise.
- SETUP / New Game wizard.
- First authored campaign used as a contract client, then removed from the public kit.
- Session 1 play, ADMIN close, and fresh-chat resume with one targeted archive recall.
- Archive grain: session deltas, message/relation ledgers.
- Engine-agnostic: any RPG as ENGINE plugin.
- Clean kit: campaign world stripped; testers start New Game.


## Unversioned research (pre-OS)

- Original v1 campaign pack: detailed world, mixed live state, chronicle attractors, legacy loaders.
- Evaluation of that pack as a campaign OS; decision to stop retrofitting.
