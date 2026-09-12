# RPG OS v0.9.7 architecture

## Operating environment

One LLM acts as GM and file operator in an ordinary workspace. Conversation is temporary working memory. Markdown files preserve accepted records. Scripts are optional development tools, never required runtime components.

The architecture optimizes the amount of relevant material the GM must reconcile during play. Disk size alone is not the target.

## Host boundary — developer reference

[HOST_CONTRACT.md](HOST_CONTRACT.md) describes the existing 0.9.x boundary against the v0.9.2 baseline. It separates the host's storage, tools and execution from the selected GM's fictional authorship and authorized file-operation role. Basic plain-file and Enhanced native implementations preserve the same meanings; alternate storage requires a mapping/export before claiming compatibility with the existing tools. The document and its nine compatibility examples add no gameplay mechanism, automatic startup read or certification.

Infrastructure may accelerate source access, recovery and transfer without acquiring authority to invent private causes, convert search results into canon or advance fiction during persistence. The file encoding can change in a future implementation; state ownership, knowledge distinctions and evidence boundaries cannot silently disappear. No external harness, adapter or alternate storage implementation is added here.

The [East Three creature-test report](releases/V0.9.1_TRIALS.md) explains one guided pre-v0.9.1 scene and its audit, including the retrospective-cause defect that informed prospective deepening. Selected player messages and recovered play/audit summaries have different evidence weight. The report is not a complete transcript, post-fix rerun or save/resume test.

## Startup and play

OS/AGENTS -> OS/BOOTSTRAP -> LAW + CURRENT_SAVE + CAMPAIGN_CONTRACT.

A bound run also reads its compact SETTING_BRIEF and active SAFETY. It checks RECOVERY/ACTIVE directly before play, followed by the existing HANDOVER/ACTIVE check. POLICY, full schemas, retrieval instructions, the agent-state procedure, reference bodies, and optional Bearing are cold. The agreement contains the accepted presentation, so ordinary startup does not open a large policy file for one voice section.

Every PLAY response follows LAW's [prime directive](../GAME/OS/LAW.md#prime-directive--every-play-response) in order:

| Stage | Responsibility |
|---|---|
| [Understand](../GAME/OS/LAW.md#understand) | Identify the actual declaration or request, the present situation and the accepted scope. |
| [Establish](../GAME/OS/LAW.md#establish) | Recover relevant facts, obtain sufficient governing sources and establish only eligible necessary gaps before they affect the response. |
| [Resolve](../GAME/OS/LAW.md#resolve) | Adjudicate the attempt and operative consequences from that basis under the accepted rules. |
| [Portray](../GAME/OS/LAW.md#portray) | Present the perceptible result in the accepted voice, preserving the player's reserved choices. |

The order applies to routine observation and dialogue as well as consequential attempts; a stage can be brief when existing state suffices. Source selection belongs to Establish. Loaded material may be reused within its coverage; a canon-governed fact beyond it needs the narrow governing source before authorship. A module-prescribed first-focused-portrayal guide must be available before focused physical description, even when the brief covers broad anatomy; sufficient loaded guide coverage is reusable. A direct pointer needs no preliminary route traversal, and a bounded subject search can recover a missing route. [OS/RETRIEVAL.md](../GAME/OS/RETRIEVAL.md) locates authority without imposing a reading schedule.

Resolve carries established event changes into current working state before continuing, including what affected entities actually perceived within the event's reach. Observation and interpretation stay distinct; an unchanged bystander needs no no-change entry. Before a pending intention or prepared development executes, check its current conditions, information, means and resources. A failed channel or missing resource needs an actual supported development to change; the intention alone is not completion. Both duties use the existing state owners and authorize no PLAY file write.

LAW owns this mandatory operating order. The model performs it; Markdown does not independently enforce stage completion or verify private reasoning. A draft cannot establish its own warrant, and a claimed check or source read does not prove that the resulting authorship complied. This change adds no external gate, background process or per-turn file write.

## Authority and storage

| Material | Owner |
|---|---|
| Universal GM duties and limits | OS/LAW |
| Accepted play experience, delegation, pacing, presentation | INSTANCE/CAMPAIGN_CONTRACT |
| Stable world facts, source bindings and starting baselines | MODULES |
| Selected generation and resolution procedures | ENGINE, with scoped accepted INSTANCE corrections |
| Compact operative present | INSTANCE/CURRENT_SAVE |
| Detailed character, people, system state, PC knowledge | Their selected INSTANCE records |
| Historical evidence | ARCHIVE |
| Optional untouched exports, including OOC and rewinds | EVIDENCE captures; evidence of what was said, not current canon |
| Optional search cache and audit bundle/report | External selected location; no live-state authority |
| Optional provisional interpretation | Cold BEARING |
| Recoverable changes | ADMIN procedures and operation-specific RECOVERY records |
| Pending GM transfer and retained transport/return provenance | HANDOVER active marker and named package; SCENE_HANDOVER procedure |

Current values replace corresponding mutable starting values; stable background remains reusable. Known-to-PC, private, unfixed, and provisional states remain distinct. A summary cannot silently supersede evidence outside its scope.

For a concrete example, suppose an invented Freeform campaign starts with courier Neri at a landing, the north bridge broken, and keeper Iven incorrectly believing it intact based on an old report. Those facts and his encounter basis are established before this illustrative exchange; it is not bundled canon or observed test evidence.

> **GM:** Iven points upstream. “Try the north bridge. It was clear at noon; I haven't been back.”
>
> **Player:** I keep the dispatch under my coat. “I'll inspect it before risking the letter.”
>
> **GM:** “Mind the current,” he says, leaving the gate open. Beyond it, the road disappears into rain. What do you do?

The bridge's starting condition belongs to MODULE; Iven's consequential current belief belongs to his PEOPLE record. KNOWN preserves what Neri heard, qualified as Iven's claim, without granting Neri the unseen truth. The saved present keeps Neri at the landing with the dispatch and an announced inspection still pending. ARCHIVE preserves the available exchange, including “I haven't been back.”

A later question about Iven's exact directions retrieves that wording. A summary such as “Iven recommended the bridge” cannot establish a guarantee that it was safe now. Neither the old report nor Neri's announced plan repairs the bridge or performs the inspection.

## Independent agent state

An agent here is a fictional decision-maker: a person, creature, machine or collective. One GM portrays the relevant agents; the architecture adds no parallel AI workers or background actor scheduler. The [optional encounter-to-resume example](ADMIN/PORTRAYAL_EXAMPLES.md#example-a-coworker-a-mistaken-belief-and-a-fresh-gm) shows the current-state and evidence owners in use.

LAW's Establish stage governs every turn. [OS/AGENT_STATE.md](../GAME/OS/AGENT_STATE.md#initial-encounter-baseline) supplies five mandatory current fields before individual participation, appraisal or initiative: condition/mode, priorities/constraints, perception/appraisal, overall attraction and engagement stance. Supported nature, control and identity constrain them. Overall attraction permits attraction, absence of attraction or aversion within its applicable domain; it is distinct from approval, trust, availability and participation. Inapplicability and precise perception/source limitations remain distinct from zero. Each applicable field is concrete or precisely limited before dependent behavior. Visual-only focus retains the portrayal-source trigger without generating private state. Coordinated groups use genuinely shared operations; independently resolved individual decisions still require separate bases.

The basis uses existing facts and eligible prospective authorship, rather than the result being sought. It is current state, not a complete biography or a preselected outcome. During continuing participation, repeated attention reuses it and brings its activities forward through actual elapsed time and developments. Group treatment establishes no identical personalities, shared mind or private attraction; an individual entering separately resolved participation or appraisal receives a current basis without retrospective private causes. World truth, private state, outward presentation and each participant's supported interpretation retain distinct scopes. Control, available information and applicable capacities govern the entity; neither human psychology nor individual autonomy is universal.

World creation binds usable source-compatible generation methods and real routes for its ordinary actors and needed opening exceptions. Resolve uses the resulting basis under the bound ENGINE and accepted exceptions. An accepted initial-fact generator is distinct from resolving acceptance, reciprocity or consent. The accepted fallback handles eligible remaining uncertainty through its own permitted scope; the [fallback procedure](MECHANICS.md#random-fallback-for-unresolved-outcomes) keeps already settled facts and genuinely open outcomes distinct. Worked cases remain in the separate optional reference. Source gaps, already resolved opportunities and deliberately open facts retain their separate treatment. These are model-operated judgments and procedures, not an independently running event processor.

The optional universal [ENGINE/_shared/ENCOUNTER_GENERATION.md](../GAME/ENGINE/_shared/ENCOUNTER_GENERATION.md) is a procedure a compatible bound engine and accepted agreement can select. It is not an engine identity; Freeform remains the only bundled selectable engine. MODULE supplies setting facts, capacities, limits and source routes; ENGINE supplies the selected mechanics. Existing diceless agreements and other selected methods survive installation unchanged.

For each eligible condition facet, initial interpersonal appraisal and overall attraction, an independent pair of actual d6 supplies direction/intensity: 2–3 strongly negative, 4–5 negative, 6–8 neutral/mixed, 9–10 positive, 11–12 strongly positive. The GM then establishes a concrete value before dependent behavior, within a facet fixed before input. At most three determinations use six independent faces; no extra intensity or engagement draw is added. The bands are not a catalogue of moods or venue-specific states. Strong values stay within supported capacities and boundaries; the middle band still needs a concrete absence of directional pull or supported countervailing considerations.

Priorities and constraints establish the entity's own current aim, drive, directive or process and practical limits from sources and permitted authorship. Factual perception is not rolled; nonsocial appraisal follows sourced sensing, classification, control and response mechanisms. Engagement is derived from the complete basis and situation, and the bound engine resolves the pending decision once. None of the generated directions grants new capacities, trust, availability or compelled participation.

Fixed opening state belongs to its selected MODULE T0 authority. Current temporary encounter state uses one optional `Active encounter state` block in NOW; entry membership means active. PEOPLE retains durable individual and relationship facts; shared controllers retain one actual system owner. Reuse state through attention gaps and update affected values on relevant events. Genuine deactivation releases inconsequential temporary state, with fresh incidental return allowed within surviving facts. Preserve consequences and unresolved matters; missing required active state remains a gap. Expiry changes current authority at its actual time, never deletes historical evidence or invents old causes. This is a logical working-context policy, not erasure of earlier chat tokens; no private scratch writes, new runtime, roster or automatic per-contact save is introduced.

New state in ordinary PLAY is conversational and best-effort until saved. Authorized persistence compiles the complete accepted present through existing recovery; it does not provide an invisible write on each NPC decision. An authorized setup can establish a small recorded private opening. A result unavailable after interruption is an explicit gap; recovery provenance is not an alternative live-state layer. The earlier automatic protected-establishment experiment is not implemented; the separately accepted whole-present announced-autosave policy introduced in v0.9.2 remains available below.

## Session preparation and feedback

ADMIN/SESSION.md connects relevant historical causes, current commitments and explicit feedback to useful conditional preparation at begin/resume, and consolidates them at an explicit ending. Genuine engine beginning/end hooks use their actual triggers and owners once per session/boundary/rule. Fresh chats, saves and handovers retain the logical session.

CURRENT_SAVE's optional administrative Session continuity owns identity and pending wrap-up; missing legacy coverage stays unknown and a clean bind uses `none`. On-demand INSTANCE/PREP.md is derivative working synthesis, created only by useful authorized post-bind persistence. Current owners and actual evidence survive its absence. Explicit feedback and boundary adjudication may be preserved as labelled OOC session operational evidence; private preparation and other administrative chatter remain outside fictional history. Feedback is a required GM duty, with a player decline permitted, and its applicable treatment informs subsequent preparation.

## Saving

SAVE/bare CLOSE performs a complete save. An explicit END SESSION invokes ADMIN/SESSION.md for consolidation, feedback and genuinely due engine procedures, then that full save; immediate stopping can preserve unfinished closure. No second save type is added. Current-save metadata carries the latest present identity separately from the latest archived evidence boundary. CHECKPOINT changes the former while retaining the latter.

The operator/model preserves preimages, records affected files and newly created directories with their prior existence, marks the operation active, writes the selected records and evidence, checks them, and publishes CURRENT_SAVE last. Restoration removes only verified operation-created empty directories after file reconciliation, using exact nonrecursive removal. Recovery reconciles an interrupted set before resumption. This is a recoverability convention, not an atomic transaction or an independent consistency engine.

The optional [announced-autosave policy](../GAME/ADMIN/AUTOSAVE.md) invokes that existing CHECKPOINT after accepted permission and advance notice. It does not add a save format, background service or private-state owner. Recovery, active handover and an in-progress write block concurrent execution. Installation alone leaves it off, and a checkpoint still does not archive new dialogue or replace full CLOSE before source access is discarded.

A coherent episode can occupy one evidence body. Split scenes or records when they will be retrieved independently. Preserve consequential wording and missing-source qualifications. Optional indexes locate evidence; they do not replace it.

## Scene handover

The optional scene-handover-v1 extension wraps CHECKPOINT with two transport files: ordered available CONVERSATION and a GM_STATE briefing containing the exact stop point, established public/private state, source map and frozen workspace hashes. It does not change save commit kinds or archive semantics. Normal startup checks HANDOVER/ACTIVE once after recovery; a present marker pauses source play and routes to the cold handover procedure. No marker or package is created merely by installing the feature.

The receiving GM is explicitly selected, continues with the player from the pending decision, and returns a factual non-graphic account plus state changes. A matching-base check and retained imported/cancelled receipt prevent stale or repeated application. Source authorities have one writer; imports use protected full save and retain honest evidence gaps. This is procedural coordination with an optional read-only integrity checker, not a filesystem lock or transfer of model-internal context. Full engine/module/current-state hashes are pinned for this temporary transfer only; ordinary startup remains as described below.

## Setup and maintenance

Quick start, Guided, and Detailed are interview-depth choices. They share one acceptance and binding procedure. World, rules, PC perspective, player control, source fidelity, and construction depth are independently considered only as needed.

An accepted agreement has five prose sections: Campaign promise, Player control, GM initiative, Time and transitions, Presentation. They include five named free-text clauses: Play form, Form selection, Structure disclosure, Cuts, Retcon. These make material omissions structurally detectable; their actual meaning, informed acceptance, and compatibility still need review. Form selection and disclosure are separate grants; fixed structure and bounded cuts operate only within the agreement. A–E presets remain optional descriptions, not required enums.

New Game never clears an existing run. Upgrade preserves old material and maps it explicitly. Correction distinguishes a mistake from a newly requested revision and repairs only dependent consequences. Review is explicit, optional, and cannot alter facts or authorize a plot.

Optional recurring-person and hidden-fact notes are cold authoring aids inside existing records. They add neither an authority layer nor a resident file. Stable anchors and current beliefs keep their existing owners; testimony, private truth, and what an audience learned remain distinct across saves and corrections.

Setup selects only materially necessary authorship, generation and retention choices within the same proposal. Newly generated fixed opening values become the module's reusable T0 baseline; later LOAD preserves them. Existing imported baselines stay unchanged. The [compatible-campaign upgrade procedure](../GAME/ADMIN/UPGRADE_V08.md) updates the generic program in a protected copy without regenerating established people or rewriting campaign evidence.

## Validation boundary

The read-only validator observes structure and references. Model readback checks selected semantic consistency fallibly. Player-rated sessions assess agency, pacing, coherence, and correction burden. Evidence from these activities is reported separately.

This experimental build prioritizes [real campaign playtesting](ADMIN/PLAYTEST_V08.md) for practical quality. Structural, recovery and packaging checks remain engineering requirements. Optional focused fixtures can diagnose an observed problem; a scripted behavioral schedule is not an entry or release gate for this playtest build.

The startup packet is not a revision-bound compiled capsule. Save/contract lineage and paths are checked at their documented scope, but the system does not pin every engine/module/body to exact immutable content. A plausible replacement may escape detection. Recovery protects a recorded change set; it does not establish global version coherence or semantic correctness across arbitrary manual swaps.

## Optional source access and audit layer

The exact reader returns current UTF-8 source passages with original line boundaries, file identity and explicit completeness. The scoped SQLite FTS5 cache holds retrieval candidates only. Requested-scope source-set and hash checks prevent quietly using an old cache as current authority; verified fetching reopens the actual file. Missing FTS5 or an unusable cache leaves ordinary file retrieval available. Neither indexing nor reading changes campaign state.

`EVIDENCE/` holds optional original exports and capture manifests, distinct from accepted ARCHIVE evidence. A cold audit freezes explicitly selected prior and resulting records outside its input roots and compares them with captured session source. A model or human extracts changes, identifies applicable authority and checks meaning. Code checks integrity, report structure and exact quotations; it does not perform semantic adjudication. Selection limits and unresolved authority remain explicit even when compared values agree.

The shared CLOSE_CONTRACT route supports an explicitly selected tiered review policy: lightweight checkpoints and bounded source review at full saves, with every-save source review as the higher-cost opt-in. Keep the exact state stopping point, existing archived-evidence boundary and actual reviewed scope separate. Frozen save-bound evidence and readback checks are operational provenance, not a second current authority. Source-first interpretation already existed and remains fallible; neither repeated self-review nor structural matching proves source coherence. No new universal campaign facts, engine mechanics or hidden memory service are introduced.

An optional standing agreement can select bounded review after a full save. Prior evidence must be preserved before its authorities are replaced. Review reports cannot silently repair current state; authorized repairs follow CORRECT and RECOVERY. Reviewed baselines are fallible, versioned review records with actual inspection depth, not truth earned through repetition. Normal boot, CHECKPOINT and ownership of current state remain unchanged.
