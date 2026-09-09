# RPG OS
### Boundless imagination. Negotiable details. One enduring core.

I built RPG OS because I wanted to play in the worlds I imagined without having to write every outcome myself.

I wanted to sit down at home, become someone within a setting I had designed, and discover what happened next. Not wait for a studio to turn that particular world into a videogame. Not program every possible interaction. And when I returned the following evening, I wanted yesterday’s decisions to still matter.

**RPG OS is a framework for persistent solo role-playing with an AI game master.** You play through conversation. The AI portrays the world and its inhabitants, resolves your attempts through the chosen rules, and maintains the campaign in ordinary, readable files.

The intended setup is simple: a PC, an internet connection, a capable AI subscription with an environment that can read, update, and preserve files, and a campaign folder. No separate paid API integration, custom server, or programming project is required.

I originally made it for myself. I shared it because other people might want the same experience—but have entirely different adventures in mind.

## Choose the experience

Perhaps you want a tightly guided adventure: a clear mission, prepared turning points, and a few sessions packed with action. Perhaps you want an open sandbox where you can explore, settle somewhere, pursue an ambition, or abandon yesterday’s plan for something more interesting.

Both are legitimate. A guided campaign should not have to pretend it is a sandbox, and a sandbox should not secretly force you toward a predetermined ending. The agreement between you and the GM defines the experience.

You also choose the scope of detail.

You can arrive with extensive lore and insist on close adherence to its geography, history, physics, and inhabitants. You can request meticulous records of possessions, resources, exact promises, and the small details that make a place recognizable.

Or you can begin with a premise and a character, keep bookkeeping light, and give the GM broad permission to develop the unknown as you encounter it.

These approaches can coexist. Carefully defined biology can sit alongside improvised settlements. Detailed combat can coexist with abstract travel. A short adventure can have deep lore; a sprawling campaign can use simple rules.

Tone, difficulty, pacing, narrative structure, world depth, and recordkeeping are separate choices—not a single package you must accept.

**You decide what needs precision, what can remain abstract, and where the GM has room to surprise you.** Permission to invent expands what remains open; it does not silently erase what has already been established. Deliberate revisions are possible, but they remain deliberate.

## Human is not the default

Universality matters because the next campaign might require a completely different reality.

Star Wars, Warhammer 40,000, and Star Trek should not become interchangeable scenery. Neither should a Second World War spy campaign, a gladiator’s life in ancient Rome, or a Viking raider’s journey along an unfamiliar coast.

And why stop at people?

Play a dinosaur in the Late Cretaceous. Navigate hunger, injury, unfamiliar terrain, and encounters that never involve a single spoken word.

**Play as a bloody ant in an ant nest.**

A food trail vanishes. Water enters the lower tunnels. Beyond the entrance, a fallen branch becomes a formidable obstacle. Getting something home could be an entire expedition.

An adventure does not become less meaningful because its protagonist has six legs.

These are campaign possibilities, not bundled settings or promises of complete scientific simulation. You establish the kind of world being played. A naturalistic ant colony and a kingdom of talking ants are both valid—but they are not the same premise.

That distinction extends to every encounter. A machine need not have human emotions. A creature may learn without understanding speech. A controlled organism may have limited discretion. The GM should use each entity’s actual senses, information, circumstances, and source of control rather than put a human personality behind every unfamiliar body.

Nor should an entity’s nature be determined by what you hope it will do. Cooperation and opposition should arise from the fiction, not from automatic agreement or compulsory resistance.

The setting defines what exists. The chosen rules govern resolution. RPG OS provides the shared operating discipline without requiring every universe to contain the same concepts.

## A growing history, a focused present

The campaign’s memory lives in files so that it does not depend entirely on one increasingly long conversation.

The GM works with the immediate situation and retrieves relevant records when necessary. Earlier scenes and detailed lore remain available without crowding every exchange. An extensive archive can serve as a reference library rather than a manuscript the model must reread from beginning to end.

When you ask about a promise made several sessions ago, recognizing that the earlier conversation matters—and finding it—is part of the GM’s job. You should not have to operate a database to speak to a character.

Checkpoints preserve the current situation. Full saves also preserve the available history of play. After saving, a fresh conversation can resume from those records with a focused working set.

**The aim is to let the campaign grow in history without making the GM carry all of that history at once.**

Because those records are ordinary files, you can inspect them, back them up, and provide them to another compatible model. Changing GMs need not mean abandoning the adventure. Better-suited models and tools can become useful to an existing campaign, not just its replacement.

## Built to be played, not to be perfect

The goal is a good game master, not an infallible machine.

An awkward description, a forgotten minor detail, or a debatable ruling need not ruin an evening. Human GMs make mistakes too, and legitimate differences of judgment are part of role-playing.

What matters is distinguishing manageable imperfections from failures that undermine the campaign: lost relationships, rewritten history, invented player decisions, or mistakes that spread through later records. RPG OS’s procedures are designed to prevent or contain those failures without making the player a full-time auditor.

It remains experimental and depends on the model and environment running it. The practical standard is nevertheless straightforward: **Was the adventure enjoyable? Did it honor the game you chose? Can you return and continue it?**

“One enduring core” does not mean frozen software. It means preserving the commitments underneath all that freedom: an understood agreement, respected player control, coherent consequences, and a history worth returning to.

You might bring years of worldbuilding or only a strange idea. You might want a few evenings of action, a life among the stars, or an expedition beneath a fallen leaf.

**Build the world. Choose the experience. Take your place in it.**

---

## Documentation and release information

**RPG OS v0.9.3 — experimental playtest release**

RPG OS helps an LLM run a persistent solo RPG campaign using ordinary Markdown files as its memory. You play in chat; the GM retrieves references, follows your accepted campaign agreement, and saves the campaign into the workspace.

**New in v0.9.3:** temporary five-field encounter baselines give active individuals a current basis before their behavior, including applicable attraction or aversion. Genuine deactivation releases inconsequential private values while retaining observations, commitments and unresolved consequences. Focused physical portrayal retrieves its required source independently of activation. Resolve carries actual event changes forward and checks the means and conditions of pending actions. These duties use existing records and add no background simulation or per-turn file writes. See [release notes](V0.9.3_CHANGES.md).

[Host compatibility contract](HOST_CONTRACT.md) describes the existing host/GM boundary, two capability levels and nine compatibility examples. [East Three creature test](V0.9.1_TRIALS.md) records the earlier guided scene, retrospective-cause defect and evidence limits. These retained documents are neither a gameplay mechanism nor a startup dependency.

**Retained from v0.9.2:** optional [announced autosave](ADMIN/AUTOSAVE.md) invokes the existing protected complete-present CHECKPOINT after a one-response-ahead notice. It coalesces meaningful-state, scene-boundary, turn-count and actually available context-pressure triggers. The outgoing model saves before a model/reasoning change; a checkpoint does not replace a full evidence-preserving CLOSE. Autosave stays off until explicitly selected. No campaign format, background service or private scratch layer is added.

**Retained from v0.9.1:** independent-agent establishment starts with an entity-appropriate behavioral basis and its actual source of control, not a human personality template or the PC's interpretation. Control and information remain separate, inapplicable behavioral dimensions stay inapplicable, and later deepening cannot backfill an earlier hidden cause merely to explain or contradict the player's interpretation. The [procedure](OS/AGENT_STATE.md), core, Freeform adapter and existing state owners remain aligned; [targeted regression cases](ADMIN/TEST_AGENT_STATE.md) separate automated instruction checks from behavioral evidence. No campaign schema or existing character is reset.

**Experimental, unbound fresh install.** This release includes the Freeform engine and blank campaign records. It includes no setting module, character, campaign history, or artwork. No paid API, custom application, database or script is required for play. Optional Python tools provide exact source reads, a disposable search cache, evidence-audit support and a read-only autosave scheduling helper.

<table>
<tr><td>
<h3><a href="MECHANICS.md">How RPG OS works</a></h3>
<p>See how the GM uses the world, your agreement, and saved records to continue a campaign. Includes diagrams, a workspace tree, and worked examples of NPC continuity, random fallback, exact retrieval and checking a save against session evidence.</p>
<p><a href="MECHANICS.md"><strong>Explore how RPG OS works →</strong></a> · <a href="OS/AGENT_STATE.md"><strong>Independent agent state →</strong></a></p>
</td></tr>
</table>

[Get v0.9.3](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.9.3) · [Quick start](QUICKSTART.md) · [Installation](INSTALLATION.md) · [Everyday commands](COMMANDS.md) · [Release notes](V0.9.3_CHANGES.md) · [Verification](VERIFICATION.md)

**v0.9.0 added:** optional tools for exact source passages, scoped full-text search, immutable transcript capture, selected before/after save snapshots and citation checks. A separate model or human can reconcile prior canon, session evidence and the resulting save. The code verifies bytes and report evidence; semantic judgments remain fallible. Later releases preserve those tools and refine independent-agent establishment and persistence. See [the illustrated workflow](MECHANICS.md#exact-retrieval-and-evidence-audits) and [v0.9.0 release notes](V0.9.0_CHANGES.md).

The standing random fallback from v0.8.1 remains available for eligible unauthored outcomes that lack enough basis for grounded judgment. Existing facts, applicable rules and other selected methods come first. Its supplied convention is one actual d6, **1–3 No and 4–6 Yes**, applied to a bounded question. See the [worked examples](MECHANICS.md#random-fallback-for-unresolved-outcomes).

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

**Save first, switch second.** Do not change model/reasoning strength before the outgoing context saves. A checkpoint protects current state only: use full CLOSE or the actual scene handover before discarding dialogue/source access, and have the next GM reload the authoritative files. Neither readback nor a context percentage guarantees hidden-memory completeness or host switching behavior. The [autosave procedure](ADMIN/AUTOSAVE.md) and [behavioral cases](ADMIN/TEST_AUTOSAVE.md) state the limits. Installing v0.9.3 does not enable autosave in a separately stored campaign.

## Independent agent state

Independent agent state is integrated through setup, worldbuilding, play, saving, resumption, and scene handover. The GM first recovers or establishes what actually governs the relevant entity: its supported nature, source of control, applicable drives or directives, available information and present circumstances. Those governing facts constrain five required current determinations: condition and mode, priorities and constraints, perception and appraisal, applicable overall attraction or aversion, and engagement stance. Each has a concrete value, supported inapplicability, or a precise perception/source limitation before dependent behavior. They describe this active encounter rather than a compulsory permanent personality. The same GM portrays the entities; no additional running AI processes are needed.

**Independence from the player's wishes is not individual autonomy.** An individual, creature, machine or collective may operate through discretion, instinct, programming, orders or shared control. A controlled body need not have human emotions or an independent personal project. An ordinary organization need not erase its members' discretion. Shared control does not grant unlimited shared knowledge. The module supplies these setting-specific facts; the engine governs applicable resolution.

An individual's participation, appraisal, initiative or separately resolved personal decision activates that temporary basis. “I approach her” can begin participation without choosing the PC's purpose; an NPC's own individual look can also activate it. Merely observing an unaware actor does not generate private state, while first focused physical portrayal still retrieves any module-prescribed guide before description. Active participation survives a pause or shift of attention. Supported events update the affected values; repeated contact does not reroll them.

Applicable attraction can be positive, absent or aversive without deciding trust, availability, willingness or a relationship. Physical, aesthetic, sexual and romantic meaning can be resolved later where relevant, preserving already known limits. Being busy or partnered does not make applicable attraction inapplicable. A bacterium's chemical response or a predator's hunger uses its actual mechanism instead of interpersonal attraction by analogy. World creation binds usable, source-compatible methods for its actors; the OS imposes no universal dice table.

**Establish the entity, not the player's impression.** Accepted world and individual facts, actual prior history and pre-encounter circumstances can constrain generation. Unverified interpretations, unperceived player wishes and desired scene endings cannot establish private nature. Preserve what an entity actually said or did without automatically treating its perceived meaning as its motive. A short reply need not mean dislike; non-attack need not mean benevolence. Private state, outward presentation and each viewpoint's supported interpretation remain distinct where applicable. Not applicable is not unknown or zero.

**Deepen prospectively.** Once an earlier portrayal exists, an unexplained private cause behind it stays unresolved unless an existing authority or an accepted generation procedure independently establishes that earlier cause from admissible inputs. The GM may not choose the player's interpretation—or its opposite—as hidden backstory merely to fit or resist the player. New evidence can change current state from that point forward without rewriting that change backward.

For example, a synthetic raider can value a challenging opponent and therefore become more interested in a contest, not automatically friendlier. A linked defender can guard its assigned approach rather than chase every target, using only its actual control and information. A credential device need not acquire friendship because the player asks nicely. A tired appearance need not acquire a retrospective long-shift explanation. These examples require their facts in their own setting; the OS does not impose them on a species, device category or human personality. The [targeted cases](ADMIN/TEST_AGENT_STATE.md) include human social controls, nonhuman drives, collective control, limited communication, capability changes and late-deepening controls.

Existing entities retain their established facts. Actual causes can change the relevant state; repeated attention does not create a different individual. A successful demonstration can improve professional trust without automatically creating personal affection. Cooperation, initiative, resistance, obedience and indifference are all possible when supported. Neither a favorable nor an unfavorable outcome proves independence. [Follow the coworker example across a save](MECHANICS.md#example-a-coworker-a-mistaken-belief-and-a-fresh-gm).

Background crowds need no individual preparation. Coordinated conduct can use shared operational facts: ten soldiers following patrol orders need not acquire ten personalities. A spokesperson making a personal response receives an individual basis; three independent drink decisions require three. Routine individual contact can use five concise clauses; deeper detail follows actual causal significance. A later eligible opportunity can still use the accepted fallback without replacing fixed state or rerolling an earlier reaction. A roll cannot create an unsupported capacity or an inapplicable relationship dimension. There is no mandatory personality spreadsheet, new agent startup file or cast-wide simulation. Agent establishment alone grants no automatic save; the optional whole-present autosave needs its separate accepted policy.

When participation reasonably ends, discard inconsequential temporary values. Keep material observations, promises, injuries, relationships and unresolved matters at their proper owners; a witness can cease being active without losing what they saw. Later incidental contact may receive fresh eligible temporary values within surviving facts. Physical absence does not end an ongoing pursuit or negotiation, and losing a still-required value is a source gap rather than expiry. Historical evidence remains evidence of its time.

New unsaved state has best-effort retention in the available conversation, not an independently recoverable private commitment. At authorized saving, the active temporary set belongs in NOW; consequential individual facts belong in PEOPLE and shared state keeps one system owner. Retain needed facts and method provenance, not internal reasoning. A checkpoint preserves the whole present while retaining the previous archive evidence boundary. Temporary-state release does not erase chat tokens or authorize private scratch writes. Adoption preserves established characters, controllers and history rather than regenerating them or silently relabeling fixed facts as impressions.

This is a complete experimental build for ordinary campaign playtesting. Start playing, switch models at completed saves or through the existing handover, and note meaningful problems when they occur. No scripted trial schedule is required before playing. [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md) explains a lightweight way to preserve useful evidence; narrative quality and cross-model reliability remain to be evaluated in actual play. The automated instruction checks are not evidence that a model follows the procedure.

Valid v0.7.3, v0.8.0, v0.8.1, v8.1.1, v0.9.0, v0.9.1 and v0.9.2 campaigns retain their record format. Use the [compatible-campaign upgrade procedure](ADMIN/UPGRADE_V08.md) in a separate protected copy. Adoption preserves established characters and histories; different generation methods or permissions require their own accepted prospective change. Updating this public repository does not itself modify a separately stored campaign.

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

The [East Three case report](V0.9.1_TRIALS.md) preserves the creature test's reported outcomes and audit defects, selected player declarations, tested candidate and missing-source qualifications. It is not a full transcript, a post-fix rerun or evidence of cross-model persistence. The [host contract](HOST_CONTRACT.md) is for implementation review, not a certification earned by passing text checks.

Project author and maintainer: [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). RPG OS developed through iterative campaign work and LLM-assisted design and review.

Design reference for the v0.7.2 optional preparation discussion: [Claude Corpus Engine by galliard5](https://github.com/galliard5/claude-corpus-engine/tree/7be53247635d41dad80b8dfb74dc96ae44852998). RPG OS's guidance and examples use original wording and its existing authority model.

Original documentation/protocol material: [CC BY 4.0](LICENSE). Code and repository automation/configuration: [MIT](TOOLS/LICENSE). Attribute “RPG OS” to croatianrdy2defend-create, link to this repository, and indicate modifications. These licenses grant no rights in third-party games, rules, trademarks, settings, artwork, or campaign content.

## Optional evidence review

Ask: “Preserve this actual session export and audit the save against it and the prior records.” The GM follows [Evidence audit](ADMIN/EVIDENCE_AUDIT.md), states the captured and inspected scope, and separates contradictions, unresolved questions and missing evidence. An authorized correction is not ignored merely because the GM failed to acknowledge it. Clear bookkeeping and changes that would alter played outcomes have different repair eligibility.

You can adopt that bounded review after each full save through the existing agreement. It is optional; unavailable exports or reviewers produce an explicit incomplete audit. No tool can promise a complete chat export on every host. Raw captures and private findings stay in your campaign or selected audit location; the public kit contains only empty guidance. [Source access](ADMIN/SOURCE_ACCESS.md) explains optional exact reads and the rebuildable search cache.

The v0.9.0 source-access and audit design also draws lessons from [Claude Corpus Engine](https://github.com/galliard5/claude-corpus-engine/tree/0ab149e8699440acf2715a16df4604ea268e2315). The tools and procedures here are independently implemented for RPG OS's existing file authorities.
