# RPG OS — playable game files

Current `main` includes the **13 September 2026 v0.9.7** saving and continuity fixes. Older tagged game ZIPs retain their original bytes.

**Version 0.9.7.** This folder is a standalone, unbound game kit. It contains the GM's operating rules, the Freeform engine, blank campaign records, saving/recovery procedures and optional runtime tools. Explanatory articles, playtest campaigns, developer tests and build automation are deliberately elsewhere.

## Start a new campaign

Copy this entire folder to a new campaign workspace, or extract the game-only ZIP. Give the AI access to the extracted folder containing `OS`, `ADMIN`, `ENGINE` and `INSTANCE`, then say:

> Open OS/AGENTS.md. Help me start a new RPG campaign.

Use this folder as the workspace root. In a full repository checkout that root is `GAME/`, **not its parent repository**. Do not insert `GAME/` into saved campaign routes: inside the workspace they still start with `OS/`, `INSTANCE/`, and so on.

[Quick start](QUICKSTART.md) · [Installation and host setup](INSTALLATION.md) · [Everyday commands](COMMANDS.md)

## Resume or stop

> Open OS/AGENTS.md and continue my saved campaign.

> Save the campaign and end the session.

Verify saving before discarding the conversation. No setting or character is preinstalled. Python tools are optional; no custom server or developer checkout is required for ordinary play.

**Do not extract a blank installation over an existing campaign.** Back up the whole campaign and follow [the protected upgrade procedure](ADMIN/UPGRADE_V08.md). This repository reorganization does not migrate or reset your saves.

## Optional reading — online, not required to play

[Architecture and mechanics](https://github.com/croatianrdy2defend-create/RPG-OS/tree/main/DOCS) · [Published playtest](https://github.com/croatianrdy2defend-create/RPG-OS/tree/main/TEST_REPORTS) · [Developer tooling](https://github.com/croatianrdy2defend-create/RPG-OS/tree/main/DEV)

RPG OS by [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create/RPG-OS). Protocol material: [CC BY 4.0](LICENSE). Runtime Python code: [MIT](TOOLS/LICENSE).
