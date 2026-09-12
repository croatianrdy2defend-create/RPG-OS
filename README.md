# RPG OS
### Boundless imagination. Negotiable details. One enduring core.

**Persistent solo role-playing with an AI game master.** Build a world, choose your character, play through conversation, and return to a campaign whose history lives in readable files.

## Just want to play?

### [Download the playable game files only — ZIP](https://github.com/croatianrdy2defend-create/RPG-OS/releases/download/game-v0.9.7/RPG_OS_v0.9.7_Game.zip)

This is the standalone **RPG OS v0.9.7** game kit: the operating rules, Freeform engine, blank campaign records, essential setup/save procedures and optional runtime tools. **No architecture essay, mechanics explainer, playtest transcripts, release-history collection, developer tests or GitHub automation is included.**

[Browse game files](GAME/README.md) · [Quick start](GAME/QUICKSTART.md) · [Installation](GAME/INSTALLATION.md) · [Game-only release and checksums](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/game-v0.9.7)

> GitHub's green **Code → Download ZIP** downloads the whole repository. Use the game-only download above when you only want to play. After extraction, use the folder containing `OS/AGENTS.md` as the campaign workspace.

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

**Current software: v0.9.7.** This release improves routine pacing, save operation, current-record maintenance and evidence tooling. [Release changes](DOCS/releases/V0.9.7_CHANGES.md). The `game-v0.9.7` release contains only the playable files. Earlier release tags and downloads remain unchanged. [What moved and how the smaller package is checked](DOCS/DISTRIBUTION.md).

For an existing campaign, keep a complete backup and use the [protected upgrade procedure](GAME/ADMIN/UPGRADE_V08.md). Never overwrite live campaign records with blank installation templates.

RPG OS by [croatianrdy2defend-create](https://github.com/croatianrdy2defend-create). [Contributing](CONTRIBUTING.md). Original protocol/documentation: [CC BY 4.0](LICENSE); code and automation: MIT, with licenses included alongside the code. No rights in third-party game settings or content are granted.
