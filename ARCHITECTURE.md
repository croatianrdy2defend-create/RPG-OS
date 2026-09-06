# RPG OS v0.7.3 architecture

## Operating environment

One LLM acts as GM and file operator in an ordinary workspace. Conversation is temporary working memory. Markdown files preserve accepted records. Scripts are optional development tools, never required runtime components.

The architecture optimizes the amount of relevant material the GM must reconcile during play. Disk size alone is not the target.

## Startup and play

OS/AGENTS -> OS/BOOTSTRAP -> LAW + CURRENT_SAVE + CAMPAIGN_CONTRACT.

A bound run also reads its compact SETTING_BRIEF and active SAFETY. It checks RECOVERY/ACTIVE directly before play. POLICY, full schemas, retrieval instructions, reference bodies, and optional Bearing are cold. The agreement contains the accepted presentation, so ordinary startup does not open a large policy file for one voice section.

During a turn the GM understands the situation and intent, retrieves materially relevant authority, resolves consequences, and presents the result. A direct pointer needs no preliminary route traversal. A bounded subject search can recover a missing route.

Authority for a new consequential development is identified before drafting it. A candidate cannot create its own warrant. This is an operating instruction, not an independently enforced boundary around model reasoning.

## Authority and storage

| Material | Owner |
|---|---|
| Universal GM duties and limits | OS/LAW |
| Accepted play experience, delegation, pacing, presentation | INSTANCE/CAMPAIGN_CONTRACT |
| Stable world and starting baselines | MODULES |
| Resolution procedures | ENGINE, with scoped accepted INSTANCE corrections |
| Compact operative present | INSTANCE/CURRENT_SAVE |
| Detailed character, people, system state, PC knowledge | Their selected INSTANCE records |
| Historical evidence | ARCHIVE |
| Optional provisional interpretation | Cold BEARING |
| Recoverable changes | ADMIN procedures and operation-specific RECOVERY records |
| Pending GM transfer and retained transport/return provenance | HANDOVER active marker and named package; SCENE_HANDOVER procedure |

Current values replace corresponding mutable starting values; stable background remains reusable. Known-to-PC, private, unfixed, and provisional states remain distinct. A summary cannot silently supersede evidence outside its scope.

## Saving

SAVE/CLOSE/END SESSION performs one complete save. Current-save metadata carries the latest present identity separately from the latest archived evidence boundary. CHECKPOINT changes the former while retaining the latter.

The operator/model preserves preimages, records affected files and newly created directories with their prior existence, marks the operation active, writes the selected records and evidence, checks them, and publishes CURRENT_SAVE last. Restoration removes only verified operation-created empty directories after file reconciliation, using exact nonrecursive removal. Recovery reconciles an interrupted set before resumption. This is a recoverability convention, not an atomic transaction or an independent consistency engine.

A coherent episode can occupy one evidence body. Split scenes or records when they will be retrieved independently. Preserve consequential wording and missing-source qualifications. Optional indexes locate evidence; they do not replace it.

## Scene handover

The optional scene-handover-v1 extension wraps CHECKPOINT with two transport files: ordered available CONVERSATION and a GM_STATE briefing containing the exact stop point, established public/private state, source map and frozen workspace hashes. It does not change save commit kinds or archive semantics. Normal startup checks HANDOVER/ACTIVE once after recovery; a present marker pauses source play and routes to the cold handover procedure. No marker or package is created merely by installing the feature.

The receiving GM is explicitly selected, continues with the player from the pending decision, and returns a factual non-graphic account plus state changes. A matching-base check and retained imported/cancelled receipt prevent stale or repeated application. Source authorities have one writer; imports use protected full save and retain honest evidence gaps. This is procedural coordination with an optional read-only integrity checker, not a filesystem lock or transfer of model-internal context. Full engine/module/current-state hashes are pinned for this temporary transfer only; ordinary startup remains as described below.

## Setup and maintenance

Quick start, Guided, and Detailed are interview-depth choices. They share one acceptance and binding procedure. World, rules, PC perspective, player control, source fidelity, and construction depth are independently considered only as needed.

An accepted agreement has five prose sections: Campaign promise, Player control, GM initiative, Time and transitions, Presentation. They include five named free-text clauses: Play form, Form selection, Structure disclosure, Cuts, Retcon. These make material omissions structurally detectable; their actual meaning, informed acceptance, and compatibility still need review. Form selection and disclosure are separate grants; fixed structure and bounded cuts operate only within the agreement. A–E presets remain optional descriptions, not required enums.

New Game never clears an existing run. Upgrade preserves old material and maps it explicitly. Correction distinguishes a mistake from a newly requested revision and repairs only dependent consequences. Review is explicit, optional, and cannot alter facts or authorize a plot.

Optional recurring-person and hidden-fact notes are cold authoring aids inside existing records. They add neither an authority layer nor a resident file. Stable anchors and current beliefs keep their existing owners; testimony, private truth, and what an audience learned remain distinct across saves and corrections.

## Validation boundary

The read-only validator observes structure and references. Model readback checks selected semantic consistency fallibly. Player-rated sessions assess agency, pacing, coherence, and correction burden. Evidence from these activities is reported separately.

The startup packet is not a revision-bound compiled capsule. Save/contract lineage and paths are checked at their documented scope, but the system does not pin every engine/module/body to exact immutable content. A plausible replacement may escape detection. Recovery protects a recorded change set; it does not establish global version coherence or semantic correctness across arbitrary manual swaps.
