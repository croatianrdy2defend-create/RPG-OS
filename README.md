# RPG OS v0.7.3

RPG OS helps an LLM run a persistent solo RPG campaign using ordinary Markdown files as its memory. You play in chat; the GM retrieves references, follows your accepted campaign agreement, and saves the campaign into the workspace.

**Experimental, unbound fresh install.** This release includes the Freeform engine and blank campaign records. It includes no setting module, character, campaign history, or artwork. No paid API, custom application, database, or required script is part of the design.

<table>
<tr><td>
<h3><a href="MECHANICS.md">How RPG OS works</a></h3>
<p>A detailed visual guide to the GM loop, player authorship, memory and evidence, hidden GM state, recoverable saves, and live scene handover. Includes seven diagrams and a workspace tree.</p>
<p><a href="MECHANICS.md"><strong>Explore the internal mechanics →</strong></a></p>
</td></tr>
</table>

[Download v0.7.3](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.7.3) · [Quick start](QUICKSTART.md) · [Installation](INSTALLATION.md) · [Everyday commands](COMMANDS.md) · [Release notes](V0.7.3_CHANGES.md) · [Verification](VERIFICATION.md)

## Start playing

Extract the release into its own folder and give your model read/write access. Then say:

> Open OS/AGENTS.md. Help me start a new RPG campaign. Use Quick start and ask only what you need next.

Provide any premise, character, rules, preferences, and references you already have. The interview reuses them and presents one compact proposal for your acceptance. Quick start develops only what the opening needs; Guided and Detailed setup provide more preparation.

To resume in a fresh chat:

> Open OS/AGENTS.md and continue my saved campaign.

To stop:

> Save the campaign and end the session.

Wait for confirmation that the save completed before discarding the conversation. A fresh chat can access only records actually saved and made available. Attachment-only hosts use the manual export procedure in [INSTALLATION](INSTALLATION.md).

## What v0.7.3 adds

Live scene handover lets you pause at the current unresolved choice, continue with another GM, and reconcile the outcome into the same campaign. It exports the accessible session conversation separately from established GM state, including hidden facts, NPC knowledge and motives, mechanical values, and pending events. Missing history is marked honestly.

The receiving GM explicitly takes over. The source stays paused until a checked return is imported or the transfer is cancelled. The return preserves factual outcomes and state changes in a non-graphic format. Export hashes, snapshots, and receipts help detect stale packages and duplicate imports; they do not transfer model-internal reasoning or prove semantic completeness.

Ask:

> Prepare a scene handover at this point.

Use the same accessible workspace copy with the receiving GM and ask it to open `OS/AGENTS.md` and receive the active handover. See [the procedure](ADMIN/SCENE_HANDOVER.md) for export, return, import, cancellation, and partial-history handling. No external model is contacted automatically.

This release also adds the illustrated mechanics guide, fresh-install packaging checks, and automated release assets. It carries provider-neutral runtime wording without a bundled provider-specific depiction policy. The host's actual capabilities still determine what it can execute. Valid v0.7.1/v0.7.2 campaigns need no state-format migration; preserve their records when updating.

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
