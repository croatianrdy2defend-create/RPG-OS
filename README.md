# RPG OS
### Boundless imagination. Negotiable details. One enduring core.

**Persistent solo role-playing with an AI game master.** Build a world, choose your character, play through conversation, and return to a campaign whose history lives in readable files.

## Start your first campaign

**New to GitHub or AI agents? Start here. No programming is required.** RPG OS is a folder of instructions and campaign records. You talk to an AI game master; it uses those files to run the game and save your progress. There is no separate RPG OS application to launch.

**[Full beginner guide: download, setup, play, save and return](DOCS/BEGINNER_GUIDE.md)** — includes an example setup conversation and help with common problems.

### [Download the latest files — ZIP](https://github.com/croatianrdy2defend-create/RPG-OS/archive/refs/heads/main.zip)

The current **RPG OS v0.9.7** files include the 13 September continuity and saving fixes. Extract this repository ZIP and use its **GAME** subfolder as your campaign folder. It includes a simple Freeform rules engine and blank campaign records, ready for your own world and character. RPG OS is free to download; your AI application's access requirements and usage costs are separate.

### 1. Download and extract

Download the ZIP above. On Windows, right-click it and choose **Extract All**; on macOS, double-click it. Put the extracted folder somewhere you can find again, such as Documents. Open the extracted **RPG-OS-main → GAME** folder, where **OS**, **ADMIN**, **INSTANCE** and **MODULES** appear together. That is your campaign folder. Keep the whole folder together and use a separate copy for each campaign.

### 2. Open that folder in an AI application

Use an AI application that can **read and update local files**. One concrete route is **Codex on desktop**. OpenAI's current documentation calls this Codex in the ChatGPT desktop app; older app versions may be labelled Codex. Install through the [official desktop setup guide](https://learn.chatgpt.com/docs/quickstart), sign in with an account that has Codex access, and select Codex if the app shows a product selector.

Add your extracted campaign folder as a **local project** and start a chat in that project. In the current interface, **Edit project → Add folder** attaches a folder; make the campaign folder primary if several are attached. A project is simply the app's way of giving chats access to your files. [Official folder instructions](https://learn.chatgpt.com/docs/projects#use-local-projects-for-folders-and-codebases).

Use that same folder for play and saving. Uploading a ZIP to an ordinary chat may provide reading access without the ability to update your campaign; [the beginner guide explains the alternatives](DOCS/BEGINNER_GUIDE.md#can-i-use-another-ai-app-or-a-browser-chat).

### 3. Paste this starting message

```text
Open OS/AGENTS.md in this campaign folder. Help me start a new RPG campaign.
Follow ADMIN/NEW_GAME.md, including Neutrality before worldbuilding and
Campaign spirit, and use Quick start. Ask only what you need next.
Check the available file access and tell me if you cannot save changes here.
```

The AI should help you choose the world, character, rules, tone and what you want from play. Describe what interests you; you can also ask it to propose options. If you have no preferred rules, ask for the included **Freeform** engine. Review its setup summary, request changes or say you accept it, and let it finish and verify the initial save. Then say **“Begin the campaign.”**

### 4. Play by talking

Describe what your character says or tries: “I ask what happened,” “I look around,” or “I get ready and head to work.” The GM describes the world and resolves the response. You can ask for more detail, faster pacing, a rules explanation or a correction in ordinary language. You do not need to edit the files yourself.

### 5. Save, stop and come back

To save while continuing, say **“Save the campaign.”** To finish playing, say **“End the session, take my feedback, and save the campaign.”** Wait for confirmation that the files were written and checked before closing the chat. Autosave and brief write-only PLAY notes are separate optional setup choices. A note does not replace a verified save.

Next time, open the **same updated campaign folder**, start a new chat in its project and paste:

```text
Open OS/AGENTS.md and continue my saved campaign. Resume from the saved point.
```

Keep only one chat actively playing a campaign. After a verified save, copy the entire campaign folder to a separate backup location. Your progress lives in the updated folder; extracting another fresh kit starts with blank records.

**Stuck? [Read the step-by-step guide and troubleshooting](DOCS/BEGINNER_GUIDE.md).** If asking for help, mention your AI app, model, the step you reached and the exact error or response.

[Browse game files](GAME/README.md) · [Quick start](GAME/QUICKSTART.md) · [Installation](GAME/INSTALLATION.md) · [Game-only release and checksums](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/game-v0.9.7)

> GitHub's green **Code → Download ZIP** downloads the whole repository. For the latest same-version fixes, open **GAME** inside that extraction. The older [frozen game-only ZIP](https://github.com/croatianrdy2defend-create/RPG-OS/releases/download/game-v0.9.7/RPG_OS_v0.9.7_Game.zip) remains available for its original build. After extraction, use the folder containing `OS/AGENTS.md` as the campaign workspace.

## Three separate places

| What you want | Where to go |
|---|---|
| **Play RPG OS** | [GAME/](GAME/README.md) — self-contained playable files and essential instructions. |
| **Understand how it works** | [DOCS/](DOCS/README.md) — architecture, mechanics, design explanations, host notes and release history. |
| **Inspect the playtests** | [TEST_REPORTS/](TEST_REPORTS/README.md) — campaign transcripts, findings, evidence and limitations. |
| **Develop or test the software** | [DEV/](DEV/README.md) — regression tests, package-building tools and distribution checks. Not needed for play. |

## Published playtest: 30 sessions, findings, and transcripts

**The Ninth Sluice / Afterwater** follows one campaign through ten initial sessions and twenty additional sessions: **30 condensed sessions and 260 recorded player/GM exchanges**, using RPG OS **v0.9.5** and Freeform.

**[Read the findings](TEST_REPORTS/2026-09-11-synthetic-campaign/REPORT.md)** · **[Read all 30 sessions](TEST_REPORTS/2026-09-11-synthetic-campaign/transcripts/README.md)** · **[Browse the evidence](TEST_REPORTS/2026-09-11-synthetic-campaign/evidence/README.md)**

The report covers successes, failures, deliberately corrupted saves, conversation-backed review, missed errors and recommendations. These were AI-authored, instrumented, non-blind tests—not human sessions or an independent-model study. They informed v0.9.6; they are not new campaign tests of v0.9.6. The publication contains all thirty play bodies and selected evidence, not every working save or audit bundle.

## Learn more

[Why I built RPG OS](DOCS/OVERVIEW.md) · [Architecture](DOCS/ARCHITECTURE.md) · [How the mechanics work](DOCS/MECHANICS.md) · [Host compatibility](DOCS/HOST_CONTRACT.md) · [Verification](DOCS/VERIFICATION.md)

**Current software: v0.9.7.** This release improves routine pacing, save operation, current-record maintenance and evidence tooling. [Release changes](DOCS/releases/V0.9.7_CHANGES.md). The earlier `game-v0.9.7` release contains the original playable build; current `main` includes the same-version fixes. Earlier release tags and downloads remain unchanged. [What moved and how the smaller package is checked](DOCS/DISTRIBUTION.md).

For an existing campaign, keep a complete backup and use the [protected upgrade procedure](GAME/ADMIN/UPGRADE_V08.md). Never overwrite live campaign records with blank installation templates.

RPG OS by [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). [Contributing](CONTRIBUTING.md). Original protocol/documentation: [CC BY 4.0](LICENSE); code and automation: MIT, with licenses included alongside the code. No rights in third-party game settings or content are granted.
