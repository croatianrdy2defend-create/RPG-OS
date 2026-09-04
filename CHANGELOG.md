# Changelog

All notable RPG OS prototype releases and design milestones are recorded here. The project is in public testing; version labels describe protocol releases, not proof of long-campaign reliability.

## Unreleased

- No unreleased changes.

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
