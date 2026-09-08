# RPG OS v0.9.2 — experimental playtest release

RPG OS helps an LLM run a persistent solo RPG campaign using ordinary Markdown files as its memory. You play in chat; the GM retrieves references, follows your accepted campaign agreement, and saves the campaign into the workspace.

**New in v0.9.2:** optional [announced autosave](ADMIN/AUTOSAVE.md) invokes the existing protected complete-present CHECKPOINT after a one-response-ahead notice. It coalesces meaningful-state, scene-boundary, turn-count and actually available context-pressure triggers. The outgoing model saves before a model/reasoning change; a checkpoint does not replace a full evidence-preserving CLOSE. Autosave stays off until explicitly selected. No campaign format, background service or private scratch layer is added.

**Retained from v0.9.1:** independent-agent establishment starts with an entity-appropriate behavioral basis and its actual source of control, not a human personality template or the PC's interpretation. Control and information remain separate, inapplicable behavioral dimensions stay inapplicable, and later deepening cannot backfill an earlier hidden cause merely to explain or contradict the player's interpretation. The [procedure](OS/AGENT_STATE.md), core, Freeform adapter and existing state owners remain aligned; [targeted regression cases](ADMIN/TEST_AGENT_STATE.md) separate automated instruction checks from behavioral evidence. No campaign schema or existing character is reset.

**Experimental, unbound fresh install.** This release includes the Freeform engine and blank campaign records. It includes no setting module, character, campaign history, or artwork. No paid API, custom application, database or script is required for play. Optional Python tools provide exact source reads, a disposable search cache, evidence-audit support and a read-only autosave scheduling helper.

<table>
<tr><td>
<h3><a href="MECHANICS.md">How RPG OS works</a></h3>
<p>See how the GM uses the world, your agreement, and saved records to continue a campaign. Includes diagrams, a workspace tree, and worked examples of NPC continuity, random fallback, exact retrieval and checking a save against session evidence.</p>
<p><a href="MECHANICS.md"><strong>Explore how RPG OS works →</strong></a> · <a href="OS/AGENT_STATE.md"><strong>Independent agent state →</strong></a></p>
</td></tr>
</table>

[Get v0.9.2](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.9.2) · [Quick start](QUICKSTART.md) · [Installation](INSTALLATION.md) · [Everyday commands](COMMANDS.md) · [Release notes](V0.9.2_CHANGES.md) · [Verification](VERIFICATION.md)

**v0.9.0 added:** optional tools for exact source passages, scoped full-text search, immutable transcript capture, selected before/after save snapshots and citation checks. A separate model or human can reconcile prior canon, session evidence and the resulting save. The code verifies bytes and report evidence; semantic judgments remain fallible. Later releases preserve those tools and refine independent-agent establishment and persistence. See [the illustrated workflow](MECHANICS.md#exact-retrieval-and-evidence-audits) and [v0.9.0 release notes](V0.9.0_CHANGES.md).

The standing random fallback from v0.8.1 remains available for eligible unauthored outcomes that lack enough basis for grounded judgment. Existing facts, applicable rules and other selected methods come first. Its supplied convention is one actual d6, **1–3 No and 4–6 Yes**, applied to a bounded question. See the [worked fallback examples](MECHANICS.md#random-fallback-for-unresolved-outcomes).

To select it once, say: “Use the simple d6 fallback as our standing method for eligible unresolved outcomes when grounded judgment is insufficient.” Include it in a new campaign's accepted proposal, or adopt it prospectively through [Recalibrate](ADMIN/RECALIBRATE.md) for an existing campaign. After selection, no per-roll permission is needed. Installing the update alone does not change an existing diceless agreement or another selected oracle.

## Start playing

Extract the release into its own folder and give your model read/write access. Then say:

> Open OS/AGENTS.md. Help me start a new RPG campaign. Use Quick start and ask only what you need next.

Provide any premise, character, rules, preferences, and references you already have. The interview reuses them and presents one compact proposal for your acceptance. Quick start develops only what the opening needs; Guided and Detailed setup provide more preparation.

To resume in a fresh chat:

> Open OS/AGENTS.md and continue my saved campaign.

To stop:

> Save the campaign and end the session.

Wait for confirmation that the save completed before discarding the conversation. A fresh chat can access only records actually saved and made available. Attachment-only hosts use the manual export procedure in [INSTALLATION](INSTALLATION.md).

## Optional announced autosave

To select the standard policy for a campaign, say:

> Enable the standard announced autosave policy in ADMIN/AUTOSAVE.md for this campaign.

The GM records that accepted permission through normal setup or recalibration. With unsaved state, it warns after a consequential change or substantial scene boundary, after 15 completed PLAY replies since verified persistence, or at a supported context reading of at least 65%. The meter must actually be available to the model or reported by the operator; it is never guessed. Several triggers create one notice, not several saves.

> OOC — Checkpoint due after the next completed play turn. Keep the current model/reasoning setting until the save is verified. You may say “checkpoint now” or “delay autosave.”

After the next completed play response, the GM briefly enters the existing protected CHECKPOINT procedure and reports the result. No fictional time passes, no unanswered PC choice is resolved, and no new archive evidence is created. Recovery or active handover blocks execution. Delay, resume, disable and manual save are ordinary requests; full SAVE always remains a full save. Nothing runs while the chat is idle.

**Save first, switch second.** Do not change model/reasoning strength before the outgoing context saves. A checkpoint protects current state only: use full CLOSE or the actual scene handover before discarding dialogue/source access, and have the next GM reload the authoritative files. Neither readback nor a context percentage guarantees hidden-memory completeness or host switching behavior. The [autosave procedure](ADMIN/AUTOSAVE.md) and [behavioral cases](ADMIN/TEST_AUTOSAVE.md) state the limits. Installing v0.9.2 does not enable autosave in a separately stored campaign.

## Independent agent state

Independent agent state is integrated through setup, worldbuilding, play, saving, resumption, and scene handover. The GM first recovers or establishes what actually governs the relevant entity: its supported nature, source of control, applicable drives or directives, available information and present circumstances. These are optional questions for finding the smallest useful basis, not required character fields. The same GM portrays the entities; no additional running AI processes are needed.

**Independence from the player's wishes is not individual autonomy.** An individual, creature, machine or collective may operate through discretion, instinct, programming, orders or shared control. A controlled body need not have human emotions or an independent personal project. An ordinary organization need not erase its members' discretion. Shared control does not grant unlimited shared knowledge. The module supplies these setting-specific facts; the engine governs applicable resolution.

When you single out an individual for attention or interaction, or an NPC directly engages your character, the GM recovers or establishes its minimal basis before the first focused portrayal or resolution that depends on it. “I approach her” is enough: the GM need not ask your character's motive or assume flirtation, company or a request for directions. An entity's own relevant perception, an established order, a due process or authorized initiative can also make its basis material; player attention is not the fictional cause of its existence or activity.

**Establish the entity, not the player's impression.** Accepted world and individual facts, actual prior history and pre-encounter circumstances can constrain generation. Unverified interpretations, unperceived player wishes and desired scene endings cannot establish private nature. Preserve what an entity actually said or did without automatically treating its perceived meaning as its motive. A short reply need not mean dislike; non-attack need not mean benevolence. Private state, outward presentation and each viewpoint's supported interpretation remain distinct where applicable. Not applicable is not unknown or zero.

**Deepen prospectively.** Once an earlier portrayal exists, an unexplained private cause behind it stays unresolved unless an existing authority or an accepted generation procedure independently establishes that earlier cause from admissible inputs. The GM may not choose the player's interpretation—or its opposite—as hidden backstory merely to fit or resist the player. New evidence can change current state from that point forward without rewriting that change backward.

For example, a synthetic raider can value a challenging opponent and therefore become more interested in a contest, not automatically friendlier. A linked defender can guard its assigned approach rather than chase every target, using only its actual control and information. A credential device need not acquire friendship because the player asks nicely. A tired appearance need not acquire a retrospective long-shift explanation. These examples require their facts in their own setting; the OS does not impose them on a species, device category or human personality. The [targeted cases](ADMIN/TEST_AGENT_STATE.md) include human social controls, nonhuman drives, collective control, limited communication, capability changes and late-deepening controls.

Existing entities retain their established facts. Actual causes can change the relevant state; repeated attention does not create a different individual. A successful demonstration can improve professional trust without automatically creating personal affection. Cooperation, initiative, resistance, obedience and indifference are all possible when supported. Neither a favorable nor an unfavorable outcome proves independence. [Follow the coworker example across a save](MECHANICS.md#example-a-coworker-a-mistaken-belief-and-a-fresh-gm).

Background crowds need no individual preparation. Routine contact can use a tiny basis; deeper detail follows actual causal significance. A later eligible opportunity can still use the accepted fallback without replacing fixed state or rerolling an earlier reaction. A roll cannot create an unsupported capacity or an inapplicable relationship dimension. There is no mandatory personality spreadsheet, new agent startup file or cast-wide simulation. Agent establishment alone grants no automatic save; the optional whole-present autosave needs its separate accepted policy.

New unsaved state has best-effort retention in the available conversation, not an independently recoverable private commitment. Authorized saving preserves the factual basis and actual method provenance in existing PEOPLE or system owners, not internal reasoning. Shared state has one owner; a checkpoint preserves the whole present while retaining the previous archive evidence boundary. Adoption preserves established characters, controllers and history rather than regenerating them or silently relabeling fixed facts as impressions.

This is a complete experimental build for ordinary campaign playtesting. Start playing, switch models at completed saves or through the existing handover, and note meaningful problems when they occur. No scripted trial schedule is required before playing. [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md) explains a lightweight way to preserve useful evidence; narrative quality and cross-model reliability remain to be evaluated in actual play. The automated instruction checks are not evidence that a model follows the procedure.

Valid v0.7.3, v0.8.0, v0.8.1, v8.1.1, v0.9.0 and v0.9.1 campaigns retain their record format. Use the [compatible-campaign upgrade procedure](ADMIN/UPGRADE_V08.md) in a separate protected copy. Adoption preserves established characters and histories; different generation methods or permissions require their own accepted prospective change. Updating this public repository does not itself modify a separately stored campaign.

## Continue a scene with another GM

Live scene handover lets you pause at the current unresolved choice, continue with another GM, and reconcile the outcome into the same campaign. It exports the accessible session conversation separately from established GM state, including hidden facts, NPC knowledge and motives, mechanical values, and pending events. Missing history is marked honestly.

The receiving GM explicitly takes over. The source stays paused until a checked return is imported or the transfer is cancelled. The return preserves factual outcomes and state changes in a non-graphic format. Export hashes, snapshots, and receipts help detect stale packages and duplicate imports; they do not transfer model-internal reasoning or prove semantic completeness.

Ask:

> Prepare a scene handover at this point.

Use the same accessible workspace copy with the receiving GM and ask it to open `OS/AGENTS.md` and receive the active handover. See [the procedure](ADMIN/SCENE_HANDOVER.md) for export, return, import, cancellation, and partial-history handling. No external model is contacted automatically.

The v0.7.3 handover, packaging checks and release tooling remain available. The runtime uses provider-neutral wording without a bundled provider-specific depiction policy. The host's actual capabilities determine what it can execute. Newly created receiver-side state remains in the receiving conversation until captured in the permitted return; the frozen source is not a live autosave target.

## Your agreement controls play

Setup separates world fidelity, resolution rules, character depth, GM initiative, player control, time, and presentation. None automatically grants the others. Five short clauses make the play form, form selection, structure disclosure, cuts, and retcon terms explicit.

The player controls the PC's reserved choices and inner experience. The GM portrays the world within accepted authority. Private preparation is optional; invented world truth, NPC belief, testimony, and PC knowledge stay distinct. Recurring NPC portrayal and investigations can use compact preparation notes without imposing a mandatory dossier or plot.

The kit accommodates different genres and kinds of player character. Other rules systems need appropriate local adapters and character values; only Freeform is bundled.

## Where memory lives

| Area | Purpose |
|---|---|
| OS | Startup, GM instructions, targeted retrieval |
| ENGINE / MODULES | Resolution rules and stable setting authorities |
| INSTANCE | Accepted agreement and current campaign state |
| ARCHIVE | Historical evidence and routes to it |
| ADMIN | Setup, save, correction, recovery, autosave and handover procedures |
| EVIDENCE | Optional untouched session captures, including OOC and rewinds; separate from accepted canon |
| TOOLS | Optional readers, search, audit and scheduling helpers, tests, and public-release packaging |

Only a small startup packet is routinely loaded. SAVE, CLOSE, and END SESSION perform a complete save. CHECKPOINT preserves the present while retaining the preceding archive evidence boundary. Handover adds a live transfer package without turning that package into a historical save.

File-changing procedures retain verified prior copies and publish the main save last. Pending recovery blocks ordinary play until reconciled. These are model-operated procedures, not atomic filesystem guarantees. Keep complete campaign backups.

## Evidence and credits

The [verification report](VERIFICATION.md) separates structural tests from live-play evidence. Scripts check specified file relationships; they cannot prove enjoyable GMing, complete memory, private-file concealment, or universal host compatibility.

Project author and maintainer: [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). RPG OS developed through iterative campaign work and LLM-assisted design and review.

Design reference for the v0.7.2 optional preparation discussion: [Claude Corpus Engine by galliard5](https://github.com/galliard5/claude-corpus-engine/tree/7be53247635d41dad80b8dfb74dc96ae44852998). RPG OS's guidance and examples use original wording and its existing authority model.

Original documentation/protocol material: [CC BY 4.0](LICENSE). Code and repository automation/configuration: [MIT](TOOLS/LICENSE). Attribute “RPG OS” to croatianrdy2defend-create, link to this repository, and indicate modifications. These licenses grant no rights in third-party games, rules, trademarks, settings, artwork, or campaign content.

## Optional evidence review

Ask: “Preserve this actual session export and audit the save against it and the prior records.” The GM follows [Evidence audit](ADMIN/EVIDENCE_AUDIT.md), states the captured and inspected scope, and separates contradictions, unresolved questions and missing evidence. An authorized correction is not ignored merely because the GM failed to acknowledge it. Clear bookkeeping and changes that would alter played outcomes have different repair eligibility.

You can adopt that bounded review after each full save through the existing agreement. It is optional; unavailable exports or reviewers produce an explicit incomplete audit. No tool can promise a complete chat export on every host. Raw captures and private findings stay in your campaign or selected audit location; the public kit contains only empty guidance. [Source access](ADMIN/SOURCE_ACCESS.md) explains optional exact reads and the rebuildable search cache.

The v0.9.0 source-access and audit design also draws lessons from [Claude Corpus Engine](https://github.com/galliard5/claude-corpus-engine/tree/0ab149e8699440acf2715a16df4604ea268e2315). The tools and procedures here are independently implemented for RPG OS's existing file authorities.
