# Developer tools — not required to play

GAME is the standalone campaign workspace. DOCS and TEST_REPORTS are separate reading material. This directory contains tests and packaging code, not another memory system.

From the repository root, with Python 3.10+ and Git:

```sh
python -B GAME/TOOLS/validate.py --root GAME
python -B DEV/run_tests.py
python -B DEV/test_distribution.py
python -B TEST_REPORTS/2026-09-11-synthetic-campaign/verify_published.py
# Commit the intended tree before packaging:
python -B DEV/package_game.py
```

`package_game.py` reads only the committed GAME subtree and the explicit `game_files.json` inventory. It rejects missing/extra game paths, links, tracked working changes and nonempty campaign templates; verifies exact extracted bytes; then runs the extracted game's own validator. Existing output is never overwritten: choose another `--output-dir` when needed. Untracked private material cannot enter a Git-based package.

The outputs are a game-only ZIP, a SHA-256 file and an exact-file manifest in `.release/`. The source version is `GAME/VERSION`. Only the game folder's contents enter the ZIP. Both licenses remain included.

## Why the test runner assembles a temporary fixture

The existing regression suites predate the repository split and use paths such as `TOOLS/test_validate.py` and root-level explanatory documents. `run_tests.py` copies the actual GAME, DOCS and DEV sources to a disposable flat-layout fixture, following `legacy_map.json`, and runs those suites sequentially. It does not reword game rules, supply model answers or modify a campaign. This avoids maintaining duplicate runtime code or shipping test files to players.

`test_distribution.py` separately tests the real new layout, standalone GAME validation and the actual game-only packager. That separate check is necessary: success in an assembled developer fixture alone would not prove that the smaller download works. `TOOLS/package_release.py` is retained here for the historical packaging regressions and shared safety routines; the current publishing entry point is `DEV/package_game.py`.

`game_files.json` is a reviewed allowlist, not an automatically expanding selection. When adding a genuine operating file, update it deliberately and review why it belongs in the playable package. Never add a live PC, setting module, archive body, capture or audit result to that list.

## Releases

The distribution workflow reads GAME/VERSION, runs tests, builds the standalone kit and publishes a separate `game-v<version>` tag with versioned `_Game.zip`, checksum and manifest assets. Existing tags and assets are not replaced. The original v0.9.6 full-kit release remains available as historical material; the homepage points to the game-only distribution.

This reorganization does not change game rules or the software version. The next actual game-version release must update GAME/VERSION and its matching documentation. Source commits, byte integrity, simulated regression coverage and real play observations remain separate claims.

Code and automation are [MIT licensed](LICENSE). See the [contribution guide](../DOCS/CONTRIBUTING.md) for evidence standards.
