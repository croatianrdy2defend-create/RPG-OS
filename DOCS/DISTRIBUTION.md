# Game-only distribution and repository layout

**11 September 2026. Software version remains 0.9.6.** This is an organization and distribution change, not a new rules version or a new campaign playtest.

## Choose what to download

[Download the game-only ZIP](https://github.com/croatianrdy2defend-create/RPG-OS/releases/download/game-v0.9.6/RPG_OS_v0.9.6_Game.zip). The [separate distribution release](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/game-v0.9.6) also includes SHA-256 checksums and a file manifest. Earlier `v0.9.6` release assets and tags are not replaced.

GitHub's **Code → Download ZIP** remains a complete repository download. GitHub's automatically generated source-code archives also contain the repository. The explicitly named `_Game.zip` asset is the smaller playable download.

| Repository location | Included in playable ZIP? | Purpose |
|---|---|---|
| `GAME/` | Yes, its contents form the installation root | All actual operating procedures, rules, engine, unbound templates, essential user instructions, runtime helpers and licenses. |
| `DOCS/` | No | Architecture, mechanics explanation, project overview, host explanations, verification history, supplemental examples and historical changes. |
| `TEST_REPORTS/` | No | Published campaign transcripts, analyses and selected evidence. |
| `DEV/` | No | Regression suites, test runner, packaging tools and explicit package inventory. |
| `.github/` | No | Repository automation and issue templates. |

Markdown is also the format of the game itself: `GAME/OS/LAW.md` and the saving procedures are operating rules, not optional explanatory essays. Removing those would remove gameplay functionality. They remain included, together with the short installation, quick-start and command guides. Supplemental examples and test protocols are available through explicit online links rather than unresolved local dependencies.

## Workspaces and existing campaigns

The folder containing `OS/AGENTS.md` is the campaign workspace. Inside a full checkout that folder is GAME; in the playable download it is the extracted `RPG_OS_v0.9.6` folder. Saved routes retain their existing names such as `INSTANCE/NOW.md`. Do not add a `GAME/` prefix inside a save or point the loader at the parent repository.

Existing campaigns are not automatically moved, reset or upgraded. Never extract blank `INSTANCE`, `ARCHIVE` or module templates over live files. Use the [protected upgrade procedure](../GAME/ADMIN/UPGRADE_V08.md) on a separate copy when applying program changes. Old optional documentation can remain in an existing campaign; absence of those optional documents is no longer a structural failure.

## Compatibility and safety changes

The runtime validator now checks actual playable dependencies instead of requiring architecture essays, historical release notes and developer test scripts. Its existing campaign structure, path, identity, recovery, handover, agreement and archive checks remain. The validator's own diagnostic identifier is `VALIDATE-v3.2.1`; the game version is unchanged.

The new developer packager reads the committed GAME subtree, verifies it against the explicitly reviewed `DEV/game_files.json` inventory, checks exact extracted bytes and runs the extracted game's own validator. New unreviewed paths, missing operating files, links, duplicate inventory entries, tracked working changes, nonempty campaign templates and existing output collisions are rejected. Untracked files never enter the committed export. Runtime helpers are included; developer test and release scripts are not.

Package output is reproducible for identical GAME bytes. A documentation-only commit changes the manifest's source-commit attribution but does not change the playable ZIP. The `game-v<version>` distribution uses its own tag and never overwrites the historical `v<version>` release. Publishing a different playable tree under an existing distribution tag is refused.

## Verification performed during preparation

The standalone game folder passed its own structural validation with no documentation or developer folder present. The retained regression suites completed **318 cases: 314 passed, four platform-specific cases skipped, zero failures**. A separate **15-case distribution suite passed**, exercising actual standalone validation, local game links, exact contents, reproducibility, missing files, bound-state rejection, unsafe path modes, dirty sources, untracked-file exclusion and non-overwriting output. These are software and packaging tests, not new AI gameplay or proof of flawless memory.

The older suites expect a flat development tree. [DEV/run_tests.py](../DEV/run_tests.py) assembles their actual current sources in a disposable fixture from GAME, DOCS and DEV. It does not ship this fixture or modify the game's rules to pass tests. [DEV/test_distribution.py](../DEV/test_distribution.py) separately verifies the real standalone layout, avoiding reliance on the assembled fixture as evidence of player-download completeness.

Published session evidence and its hash manifest remain unchanged. The test index's link to the moved verification document is updated. The original project introduction is retained as [the overview](OVERVIEW.md), and the playtest remains prominently linked on the [repository homepage](../README.md).

Current maintenance commands and release behavior are documented in [DEV/README.md](../DEV/README.md). CI repeats the distribution and regression checks before publishing the game-only asset.
