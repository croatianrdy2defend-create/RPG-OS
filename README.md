# RPG OS v0.7.1

RPG OS helps one commercial LLM run a persistent solo RPG campaign using ordinary Markdown files as its memory. You play in chat; the model retrieves references and saves the campaign into the workspace.

**Experimental release.** This kit contains no campaign world and bundles only the Freeform engine. Other systems need an appropriate local rules adapter and character values. No API subscription, custom application, database, or required script is part of the design.

Start with [QUICKSTART](QUICKSTART.md). See [INSTALLATION](INSTALLATION.md) for workspace requirements and older campaigns, [COMMANDS](COMMANDS.md) for everyday requests, [v0.7.1 changes](V0.7.1_CHANGES.md) for this repair release, [v0.7 changes](V0.7_CHANGES.md) for the redesign, and [VERIFICATION](VERIFICATION.md) for checks actually run.

## What changed

v0.7.1 repairs agreement omissions, recovery directory cleanup, and validator diagnostics in the v0.7 redesign. It adds explicit form-selection/disclosure, hard-cut, and retcon clauses while retaining five readable sections. Setup proposes the defaults in its existing compact review; it does not require five extra interview rounds.

- A shorter GM core and startup path.
- A concrete five-part campaign agreement instead of mandatory calibration axes.
- A readable present situation with separate pointers to detailed state and historical evidence.
- "Save" and "End session" both perform the complete ordinary save.
- Recovery copies and a pending-operation marker before multi-file changes.
- An adaptive universal NEW GAME with Quick start, Guided, and Detailed paths.
- Targeted search when an exact needed reference cannot be found through its pointers.
- Optional review notes stay outside normal startup.
- Ordinary language works for starting, continuing, saving, correcting, and changing the game.

The model still supplies judgment, prose, and file operations. These changes reduce repeated procedural decisions; they do not make the model infallible.

## Start playing

Give the model access to the extracted folder in a workspace where it can read and write files. Then say:

> Open OS/AGENTS.md. Help me start a new RPG campaign. Use Quick start and ask only what you need next.

You can provide your premise, character, rules, preferences, and reference files immediately. The interview reuses them. It presents a compact proposal before binding the campaign; your explicit acceptance can be ordinary language.

To resume in a fresh chat:

> Open OS/AGENTS.md and continue my saved campaign.

At a stopping point:

> Save the campaign and end the session.

Wait for confirmation that the save completed before discarding the conversation. A fresh chat can read only what was actually saved and made accessible.

## A universal setup

NEW GAME separates choices that do not imply each other:

- The world and its source fidelity.
- The rules for resolution.
- Character/profile depth and required mechanical values.
- What the GM may initiate and what you control.
- Pacing, routine transitions, voice, and useful state display.
- Optional detailed systems and private preparation.

A quick freeform campaign can begin with a short profile and opening. A mechanical game still needs whatever values its opening actually uses. Detailed setup develops selected domains; it does not automatically build every world system.

The questions adapt to fantasy, historical, contemporary, science-fiction, domestic, investigative, military, surreal, nonhuman, or custom premises. They do not require human anatomy, Earth dates, money, romance, combat, a central plot, or a conventional adventuring party. A novel perspective still needs a clear statement of what the player controls.

## Where memory lives

| Area | Purpose |
|---|---|
| OS | Core instructions, startup, and targeted retrieval |
| ENGINE | Resolution procedures and required character values |
| MODULES | Stable setting, world brief, starting baselines, and optional authored material |
| INSTANCE | Accepted agreement, current situation, character, relationships, knowledge, systems, limits, and corrections |
| ARCHIVE | Historical evidence and compact routes to it |
| ADMIN | Setup, saving, recovery, correction, upgrade, and optional review |
| TOOLS | Optional read-only structural validation and regression tests |

Only the small startup packet is routinely loaded. Detailed records remain available when a particular question needs them. A relationship summary does not replace its consequential history; a world fact does not automatically become PC knowledge.

## Saving and repair

SAVE, CLOSE, and END SESSION use the same complete save procedure. CHECKPOINT is an explicitly reduced option: it preserves the present while leaving the previous archive evidence boundary intact.

The model preserves prior versions of affected files, records new files and directories, writes the changes, checks them, and publishes the main save last. Restoration removes only verified operation-created empty directories after the affected files are reconciled. A pending recovery marker prevents ordinary resumption after interruption. Recovery is a procedure the model follows, not an atomic filesystem guarantee.

Say "That contradicts our earlier scene" or "I never agreed to that" for a narrow correction. The GM preserves unaffected play and repairs consequences. Ordinary play changes remain in chat until saved; file-changing maintenance follows its recovery procedure.

Valid outcomes follow the agreement's Retcon clause: rewind is available by default, or ironman/no-retcon may be accepted. Genuine errors, stopping play, and changing depiction are separate. General play structure is known by default; permission to choose it and permission to withhold it are distinct optional grants. Hard cuts likewise require an explicit scope.

## Evidence and limits

The optional validator checks structures, paths, identities, references, and the presence of required agreement clauses. It cannot prove their meaning or acceptance. Regression tests exercise synthetic files. Neither proves enjoyable GMing, semantic memory accuracy, or compatibility with every commercial host. See [ADMIN/TESTS](ADMIN/TESTS.md) for playtesting scenarios.

Attachment-only hosts need the manual export workflow in INSTALLATION. Hidden preparation requires actual host support; ordinary private files are spoiler separation, not encryption. Random rolls require an available randomizer or player-supplied result. Model judgment must be labeled honestly.

The startup packet is a collection of authoritative records, not a compiled snapshot pinning every engine, module, agreement, and mutable body revision. Identity/route checks cannot detect every plausible file-version swap. Preserve campaign copies and use explicit maintenance rather than mixing records from different versions.

## Credits and rights

Project author and maintainer: [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). RPG OS developed through iterative campaign work and LLM-assisted design and review; the files must remain usable without the original design conversation.

Original documentation and protocol material are licensed under [CC BY 4.0](LICENSE); code and repository automation/configuration under [MIT](TOOLS/LICENSE). Preferred attribution: "RPG OS" by croatianrdy2defend-create, with a link to [this repository](https://github.com/croatianrdy2defend-create/RPG-OS). Indicate modifications.

These licenses cover only material the project is entitled to license. They do not grant rights in third-party games, rules, trademarks, settings, artwork, or user-created campaign content. The public kit includes only the Freeform engine and no third-party ruleset adapter. Keep bound campaigns, personal limits, and owned source material out of a public kit.
