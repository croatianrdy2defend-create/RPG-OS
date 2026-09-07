# v0.8.0 experimental verification — 2026-09-07

This report distinguishes engineering checks on the isolated public candidate from future human campaign observations. The baseline is public v0.7.3, commit `a92d658530a7fd30f958c1af3814a604803368d0`. Historical [v0.7.2 trials](V0.7.2_TRIALS.md) retain their original scope; they are not evidence of new agent-state behavior.

## Observed engineering checks

| Check | Observed result |
|---|---|
| Structural validator on the unbound candidate | PASS; zero findings, stable measured tree and matching executed/target validator bytes |
| Structural regression suite | 48 tests passed on Python 3.11 / Windows |
| Handover regression suite | 36 tests: 35 passed, one native-symlink fixture skipped because this host does not permit symlink creation; the separate Windows reparse-point rejection fixture passed |
| Packaging regression suite | 15 tests passed on Python 3.11 / Windows |
| Total automated regression cases | 99 discovered: 98 passed, 1 platform skip |
| Mechanics diagrams | All eight parsed and rendered with Mermaid 10.9.3 in headless Chrome; the new agent-state diagram was visually inspected |
| Documentation links | Checked relative destinations and heading anchors resolve |
| Public incident form | YAML parses; version placeholder is correctly nested and optional incident context is available |
| Release inventory | 74 intended public files; blank campaign/archive records, generic module contracts and Freeform only |
| Committed ZIP and checksum | PASS; exact committed-file bytes, complete public inventory, frozen unbound validation, ZIP CRCs and written SHA-256 verified by release packaging |
| Scripted behavioral pilot | NOT RUN; not a gate for this experimental playtest release |
| Human v0.8 campaign / model switching | NOT RUN during development; the primary next evaluation |
| Long-campaign fidelity, enjoyment and universal compatibility | NOT ESTABLISHED |

`VALIDATE-v3.1.0` adds required inventory checks for the cold agent-state procedure, v0.8 upgrade/playtest guides and current release notes. Presence checks do not add startup reads or prove instruction compliance. The campaign record formats remain unchanged.

The structural suite includes ordinary existing PEOPLE/NOW/KNOWN prose without new agent fields, protected save/directory recovery fixtures, agreement structure, source routes and present/evidence boundaries. The Windows fixture copier now preserves exact validator bytes instead of normalizing line endings; strict identity checking was not weakened.

The handover suite confirms that current person/system/knowledge records and the cold agent-state procedure are in its frozen snapshot and that changed source bytes invalidate that snapshot. These are file-integrity observations, not proof that a receiving GM will interpret the state faithfully.

The packaging suite covers committed exports, checksums, dirty tracked trees, populated campaign registers, extra modules/private paths, missing extension files, version-derived filenames, omitted Git exports, links, traversal and case collisions. A real CRLF checkout fixture verifies that Windows preferences do not alter the committed bytes in the archive or change Git settings. Final packaging exposed this conversion issue; the exporter now disables checkout line-ending conversion for its archive command while keeping all blob comparisons.

The final whole-tree validator ran separately after fixture mutation stopped. An earlier overlapping scan encountered changing temporary test directories and was discarded as incomplete; the affected structural suite was rerun successfully in isolation. Never validate a measured tree while tests or edits mutate it.

## Reproduce the checks

Run sequentially from a separate development copy:

```text
python -B TOOLS/test_validate.py
python -B TOOLS/test_handover.py
python -B TOOLS/test_package_release.py
python -B TOOLS/validate.py --root .
```

On a clean committed public checkout, `python -B TOOLS/package_release.py` exports that commit, rejects non-public or populated campaign paths, validates its frozen unbound tree and compares every archived file to the committed blob. It verifies ZIP CRCs and the written SHA-256 checksum. A downloaded play folder does not require these development tools or Git.

## Runtime scope and remaining observations

Ordinary PLAY creates no automatic checkpoint or private scratch file. Newly established unsaved state has best-effort retention in available conversation. Requested saving preserves the complete accepted present; a checkpoint retains the previous archive evidence boundary. The receiving GM leaves frozen source authorities unchanged.

Setup records a pending generated determination before obtaining its input. After an interrupted bind, physical restoration alone does not cancel the accepted setup: its active recovery route remains until completion or explicit setup cancellation/replacement. A genuinely lost result is reported as a gap. Optional diagnostic M07 in [ADMIN/TESTS](ADMIN/TESTS.md) describes this model-operated recovery edge and remains NOT RUN; the automated active-marker checks do not validate its semantic execution.

The [v0.8 upgrade procedure](ADMIN/UPGRADE_V08.md) has been reviewed for program/data ownership, backup preservation and compatibility routing. A complete model-operated upgrade of a played campaign was not executed during this build. Existing synthetic compatibility and recovery checks do not establish that broader result.

The core grew by 123 whitespace-delimited words from v0.7.3; the cold agent-state procedure is 952 words. The loader adds no unconditional read of that procedure. These are static measurements; actual retrieval, latency, setup burden and adherence require observation.

Use [real-campaign playtesting](ADMIN/PLAYTEST_V08.md) to assess recognizability, initiative, cause-driven change, pacing, saving and continuation with different models. Notes are optional and outside fictional authority. A rejection is not by itself evidence of independence, and an enjoyable session is not proof of lossless memory.

Recovery remains a model-operated procedure, handover markers are not operating-system locks, and private files are not encrypted. No new empirical claim of universal host compatibility, unbiased initialization or fully lossless transfer is made.
