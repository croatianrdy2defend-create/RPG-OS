# RPG OS v0.8.0 — experimental playtest release

RPG OS helps an LLM run a persistent solo RPG campaign using ordinary Markdown files as its memory. You play in chat; the GM retrieves references, follows your accepted campaign agreement, and saves the campaign into the workspace.

**Experimental, unbound fresh install.** This release includes the Freeform engine and blank campaign records. It includes no setting module, character, campaign history, or artwork. No paid API, custom application, database, or required script is part of the design.

<table>
<tr><td>
<h3><a href="MECHANICS.md">How RPG OS works</a></h3>
<p>See how the GM uses the world, your agreement, and saved records to continue a campaign. Includes eight diagrams, a workspace tree, and a worked example of an NPC relationship changing and surviving a fresh chat.</p>
<p><a href="MECHANICS.md"><strong>Explore how RPG OS works →</strong></a> · <a href="MECHANICS.md#independent-people-and-other-agents"><strong>Independent agent state →</strong></a></p>
</td></tr>
</table>

[Get v0.8.0](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.8.0) · [Quick start](QUICKSTART.md) · [Installation](INSTALLATION.md) · [Everyday commands](COMMANDS.md) · [Release notes](V0.8.0_CHANGES.md) · [Verification](VERIFICATION.md)

## Start playing

Extract the release into its own folder and give your model read/write access. Then say:

> Open OS/AGENTS.md. Help me start a new RPG campaign. Use Quick start and ask only what you need next.

Provide any premise, character, rules, preferences, and references you already have. The interview reuses them and presents one compact proposal for your acceptance. Quick start develops only what the opening needs; Guided and Detailed setup provide more preparation.

To resume in a fresh chat:

> Open OS/AGENTS.md and continue my saved campaign.

To stop:

> Save the campaign and end the session.

Wait for confirmation that the save completed before discarding the conversation. A fresh chat can access only records actually saved and made available. Attachment-only hosts use the manual export procedure in [INSTALLATION](INSTALLATION.md).

## What v0.8 adds

Independent agent state is integrated through setup, worldbuilding, play, saving, resumption, and scene handover. The GM uses each relevant person's established circumstances, knowledge and aims, determines eligible unknowns through the accepted method, and changes their state for actual causes. Cooperation, initiative, resistance and indifference can all follow from those circumstances. Conversation length and the player's hoped-for outcome do not automatically create agreement.

Here, an **agent** is a fictional person, creature, machine or collective whose decisions matter. One GM portrays these agents; the feature requires no additional running AI processes.

For example, a coworker can remain personally distant while developing professional trust after a difficult shared job. A successful save should preserve both aspects and the available evidence of what changed, so the next GM can continue the same relationship. Existing friendships and accepted starting relationships remain valid. [Follow the worked example from encounter to fresh GM](MECHANICS.md#example-a-coworker-a-mistaken-belief-and-a-fresh-gm).

The procedure uses the existing person and system records. There is no required personality spreadsheet, new startup file, cast-wide simulation or automatic save. New unsaved state remains in conversation until an authorized save installs it. A checkpoint preserves the whole present while retaining the previous archive evidence boundary.

This is a complete experimental build for ordinary campaign playtesting. Start playing, switch models at completed saves or through the existing handover, and note meaningful problems when they occur. No scripted trial schedule is required before playing. [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md) explains a lightweight way to preserve useful evidence; narrative quality and cross-model reliability remain to be evaluated in actual play.

Valid v0.7.3 campaigns retain their record format. Use the [v0.8 upgrade procedure](ADMIN/UPGRADE_V08.md) in a separate protected copy. Adoption preserves established characters and histories; different generation methods or permissions require their own accepted prospective change.

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
| ADMIN | Setup, save, correction, recovery, and handover procedures |
| TOOLS | Optional read-only checkers, tests, and public-release packaging |

Only a small startup packet is routinely loaded. SAVE, CLOSE, and END SESSION perform a complete save. CHECKPOINT preserves the present while retaining the preceding archive evidence boundary. Handover adds a live transfer package without turning that package into a historical save.

File-changing procedures retain verified prior copies and publish the main save last. Pending recovery blocks ordinary play until reconciled. These are model-operated procedures, not atomic filesystem guarantees. Keep complete campaign backups.

## Evidence and credits

The [verification report](VERIFICATION.md) separates structural tests from live-play evidence. Scripts check specified file relationships; they cannot prove enjoyable GMing, complete memory, private-file concealment, or universal host compatibility.

Project author and maintainer: [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). RPG OS developed through iterative campaign work and LLM-assisted design and review.

Design reference for the v0.7.2 optional preparation discussion: [Claude Corpus Engine by galliard5](https://github.com/galliard5/claude-corpus-engine/tree/7be53247635d41dad80b8dfb74dc96ae44852998). RPG OS's guidance and examples use original wording and its existing authority model.

Original documentation/protocol material: [CC BY 4.0](LICENSE). Code and repository automation/configuration: [MIT](TOOLS/LICENSE). Attribute “RPG OS” to croatianrdy2defend-create, link to this repository, and indicate modifications. These licenses grant no rights in third-party games, rules, trademarks, settings, artwork, or campaign content.
