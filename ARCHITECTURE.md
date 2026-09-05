# RPG OS v0.7 architecture

## Operating environment

One LLM acts as GM and file operator in an ordinary workspace. Conversation is temporary working memory. Markdown files preserve accepted records. Scripts are optional development tools, never required runtime components.

The architecture optimizes the amount of relevant material the GM must reconcile during play. Disk size alone is not the target.

## Startup and play

OS/AGENTS -> OS/BOOTSTRAP -> LAW + CURRENT_SAVE + CAMPAIGN_CONTRACT.

A bound run also reads its compact SETTING_BRIEF and active SAFETY. It checks RECOVERY/ACTIVE directly before play. POLICY, full schemas, retrieval instructions, reference bodies, and optional Bearing are cold. The agreement contains the accepted presentation, so ordinary startup does not open a large policy file for one voice section.

During a turn the GM understands the situation and intent, retrieves materially relevant authority, resolves consequences, and presents the result. A direct pointer needs no preliminary route traversal. A bounded subject search can recover a missing route.

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

Current values replace corresponding mutable starting values; stable background remains reusable. Known-to-PC, private, unfixed, and provisional states remain distinct. A summary cannot silently supersede evidence outside its scope.

## Saving

SAVE/CLOSE/END SESSION performs one complete save. Current-save metadata carries the latest present identity separately from the latest archived evidence boundary. CHECKPOINT changes the former while retaining the latter.

The operator/model preserves preimages, records the affected set and new paths, marks the operation active, writes the selected records and evidence, checks them, and publishes CURRENT_SAVE last. Recovery reconciles an interrupted set before resumption. This is a recoverability convention, not an atomic transaction or an independent consistency engine.

A coherent episode can occupy one evidence body. Split scenes or records when they will be retrieved independently. Preserve consequential wording and missing-source qualifications. Optional indexes locate evidence; they do not replace it.

## Setup and maintenance

Quick start, Guided, and Detailed are interview-depth choices. They share one acceptance and binding procedure. World, rules, PC perspective, player control, source fidelity, and construction depth are independently considered only as needed.

An accepted agreement has five prose sections: Campaign promise, Player control, GM initiative, Time and transitions, Presentation. It states concrete grants rather than requiring the GM to infer them from multiple enum labels.

New Game never clears an existing run. Upgrade preserves old material and maps it explicitly. Correction distinguishes a mistake from a newly requested revision and repairs only dependent consequences. Review is explicit, optional, and cannot alter facts or authorize a plot.

## Validation boundary

The read-only validator observes structure and references. Model readback checks selected semantic consistency fallibly. Player-rated sessions assess agency, pacing, coherence, and correction burden. Evidence from these activities is reported separately.
