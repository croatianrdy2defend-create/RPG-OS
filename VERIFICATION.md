# RPG OS experimental verification

## v9.0.0 source and evidence tools — 2026-09-08

This experimental release starts from public v8.1.1, commit `e297c3f29debfda2bc610ccf08acbddd48f66242`. It adds optional source reading, scoped lexical search and evidence capture/report checks. Existing save/record formats and the direct-attention NPC procedure remain compatible. Verification below concerns this implementation; it does not establish long-campaign reliability.

| Check | Observed local result |
|---|---|
| Structural regression suite | 48 passed |
| Handover regression suite | 35 passed, 1 platform skip |
| Packaging regression suite | 15 passed, including new raw-capture exclusion and required-tool inventory checks |
| Exact source reader | 24 passed, 3 platform skips |
| Scoped lexical search | 32 passed, 1 platform skip |
| Evidence capture and report checker | 31 passed, 2 platform skips |
| Total | 192 discovered: 185 passed, 7 platform skips on Windows / Python 3.11.9 |
| Capability probe | Exact local UTF-8/CRLF read and an actual SQLite FTS5 query demonstrated; host chat export explicitly unobserved |
| Whole-tree structural check | PASS, zero findings, stable measured tree and matching executed/target validator bytes |
| Mechanics diagrams | All eleven parsed and rendered using Mermaid 10.9.3; the two new source/audit diagrams visually inspected |
| Independent code review | Reproduced and fixed Windows short-path containment, changed nested-campaign eligibility, invalid cached passage ranges and empty-source delivery; focused suites rerun |
| Documented capture workflow | Import, integrity check, selected prior/current bundle, pending template, authored report and checker exercised through actual subprocess commands |
| Played-campaign upgrade, forty-session continuity, cross-model audit reliability | NOT RUN |
| Proposed E01 retirement and E02 repeatability diagnostics | NOT RUN as those named complete exercises |

The platform skips concern unavailable unprivileged symlink creation, FIFO support and a receipt alias case dependent on symlink creation. Actual Windows junction and 8.3 short-path tests ran successfully. Native platform checks are kept separate from simulated link/reparse rejection. The repository workflows run all six suites and package the exact triggering commit; their Linux observations are available in the release's Actions runs, not presumed here.

One fresh reviewer context also used the production tools on six selected synthetic cases. The fixture author did not pass expected verdicts to that reviewer. All 34 selected source bodies were delivered with tool-generated receipts, and all six authored reports passed hash, original-line quotation and schema checks on their first attempt: 100 citation occurrences verified exactly. The reviewer found the omitted appointment, ignored authorized correction and inherited licence error; preserved an ambiguous suggestion and a legitimate appearance change; and identified the unambiguous HP error as requiring a player decision because a narrow repair would invalidate the played escape. No campaign repair was executed.

A second fresh reviewer checked citation relevance against the 34 frozen bodies and found all 12 material findings supported, with no unsupported material claim found. This second review inspected sources directly and claimed no reader receipts.

That was one semantic integration pass by the same model family in a fresh context, not a cross-model or unattended long-run benchmark. Delivery receipts do not prove comprehension. The prior exploratory twelve-case repeated trial used a different diagnostic harness; its results are not counted as passes for this implementation. Source fixtures, raw captures and private audit artifacts are kept outside this unbound distribution.

The integration run exposed a usability gap: reviewers needed clearer report-field and citation instructions. The [audit guide](ADMIN/EVIDENCE_AUDIT.md#complete-the-report-template) now includes the supported values, exact original-line quoting and delivery-receipt workflow. Candidate reports explicitly keep source coverage, unresolved questions, consistency and repair eligibility separate.

Before publication the final committed exporter must verify its public inventory, exact committed bytes, ZIP paths/CRCs, frozen unbound state and SHA-256. See [v9.0.0 release assets](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v9.0.0) and [release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) for actual publication evidence. The sections below retain earlier results at their original scope.

## v8.1.1 direct-attention baseline — 2026-09-07

This incremental release starts from canonical public v0.8.1, commit `6177772108c8c0b61350670e71a7c97cb491e667`. Direct attention or interaction now requires a minimal current individual basis before focused portrayal or reception. Existing state, engine authority, private/public distinctions and requested-save boundaries remain intact. The observation that motivated the change was a supplied campaign audit; it does not independently authenticate that conversation's tool history.

All three regression suites ran sequentially on the versioned candidate after the instruction and documentation changes. Whole-tree validation ran separately after fixture mutation stopped. No tool code, record format or release-version parser changed.

| Check | Observed result |
|---|---|
| Structural regression suite | 48 passed on Windows / Python 3.11 |
| Handover regression suite | 35 passed; one native-symlink case skipped because this host does not permit symlink creation; separate Windows reparse-point case passed |
| Packaging regression suite | 15 passed |
| Total automated regression cases | 99 discovered: 98 passed, 1 platform skip |
| Whole-tree structural validator | PASS; zero findings, stable measured tree and matching executed/target validator bytes |
| Documentation links | 101 relative destinations/anchors checked; zero failures |
| Issue form | YAML parses; unique field IDs and correctly nested v8.1.1 placeholder |
| Mechanics diagrams | All nine parsed and rendered with Mermaid 10.9.3; revised individual-state diagram visually inspected |
| Independent static behavior review | Direct-attention trigger, routine contact, undeclared intent, perception, reuse, bounded depth and existing resolution/persistence rules reviewed; no actionable issue found |
| B16 first-contact and fresh-chat diagnostics | Six optional manual cases documented, NOT RUN |
| Model-operated update of a played campaign | NOT RUN |
| NPC-capacity or long-campaign behavioral benchmark | NOT RUN |

The final committed exporter must verify the public inventory, exact committed bytes, ZIP paths/CRCs, frozen unbound state and written SHA-256 before publication. The [release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) repeats regression and packaging checks on the published commit; consult it and the [v8.1.1 assets](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v8.1.1) for publication evidence. This source report does not claim a completed external run in advance.

These engineering results do not prove that a GM establishes its baseline before responding, retains unsaved private state, or portrays a large cast consistently. B16 asks for available factual state and operation evidence while leaving unavailable ordering unverified; private model reasoning is not required. New baselines remain best-effort conversation state until an authorized save succeeds. The release creates no running AI worker per NPC, full-cast scan, new schema or automatic write.

The sections below retain the scope and observations of earlier versions.

This report distinguishes engineering checks from human campaign observations and identifies the build each result describes. The v0.8.1 release tree starts from canonical public main, commit `40f8c021059b3f5a3f0f761441da117591871ae6`, with the reviewed simple fallback changes. The checks below were observed on the versioned release candidate. Historical [v0.7.2 trials](V0.7.2_TRIALS.md) retain their original scope; they are not evidence of new agent-state behavior.

## v0.8.1 release checks — 2026-09-07

All three suites were rerun sequentially after the v0.8.1 runtime and release-documentation edits. The whole-tree validator ran separately after fixture mutation stopped. The final committed export must pass its own frozen validation, byte comparison, inventory and checksum checks before publication. Release automation repeats the suites and exporter on the published commit; its result and assets are available with the [release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) and [v0.8.1 release](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.8.1).

| Final v0.8.1 check | Status |
|---|---|
| Structural regression suite | 48 passed on Windows / Python 3.11 |
| Handover regression suite | 35 passed; one native-symlink test skipped because this host does not permit symlink creation; separate Windows reparse-point test passed |
| Packaging regression suite | 15 passed |
| Total automated regression cases | 99 discovered: 98 passed, 1 platform skip |
| Whole-tree structural validator | PASS; zero findings, stable measured tree and matching executed/target validator bytes |
| Current documentation links | 97 relative destinations/anchors checked; zero failures |
| Public issue form | YAML parses; unique field IDs and correctly nested v0.8.1 version placeholder |
| Mechanics diagrams | All nine parsed and rendered with Mermaid 10.9.3; the new fallback diagram visually inspected |
| Independent static review | No scope, standing-selection or release-inventory issue found; generic Freeform kit and blank campaign/archive bodies retained |
| Committed ZIP and GitHub assets | Checked after commit by the exporter and release workflow; consult the release assets and workflow for the published artifact result |
| B15 human diagnostics and fresh-chat replay | NOT RUN |
| Complete model-operated upgrade of a played campaign to v0.8.1 | NOT RUN |

## Reviewed random-fallback candidate — prior observations (2026-09-07)

A supplied campaign audit reported successful retrieval of an unresolved contact record, followed by a quiet interval whose later opportunity had never been assessed. This is reported play evidence motivating the change; it does not prove every quiet outcome is erroneous or independently authenticate the other conversation's tool history.

The reviewed candidate supplied a simple optional standing oracle for eligible outcomes too sparse for grounded judgment: frame a bounded question and obtain actual random input. Its default convention is one d6, 1–3 No and 4–6 Yes; existing facts, applicable engine procedures and other accepted methods retain priority. It replaced the longer local assessment draft. Its save schema, installed engine adapters, startup file set and write permissions were unchanged. LAW grew from 1,609 to 1,690 whitespace-delimited words; AGENT_STATE grew from 952 to 1,223. These are measurements of that reviewed candidate. The detailed method remains cold and is enabled by the player's request or standing selection, without per-roll reconfirmation. Installation alone does not change an existing diceless agreement or another selected method.

| Reviewed fallback-candidate check | Previously observed result |
|---|---|
| Structural regression suite | 48 passed |
| Handover regression suite | 35 passed; one native-symlink test skipped on this Windows host; Windows reparse-point test passed |
| Packaging regression suite | 15 passed |
| Total automated regression cases | 99 discovered: 98 passed, 1 platform skip |
| Final structural validator | PASS, zero findings; stable tree and matching executed/target validator bytes |
| Documentation links | 91 relative destinations/anchors checked; no failures |
| Mechanics diagrams | All nine parsed and rendered with Mermaid 10.9.3; the simplified fallback diagram visually inspected |
| Independent static instruction review | Reviewed direct sparse-outcome fallback, existing facts/methods, standing acceptance, real input, causal scope and missing-source protection; updated the diagnostic link after its heading changed |
| New B15 diagnostic variants | Nine optional variants documented, NOT RUN |
| Fresh-chat campaign replay with revised instructions | NOT RUN |

All three regression suites were rerun on the reviewed fallback candidate after simplifying the protocol. These engineering and static checks do not establish that a GM will apply it reliably, and they predate the final v0.8.1 version and documentation changes. At that observation point the patch was local and unpublished; the published v0.8.0 artifact and live campaign history were unchanged. No retrospective contact decision or replacement roll was made. No v0.8.1 publication, completed campaign upgrade or human behavioral result is inferred from those checks.

The following engineering section describes the original v0.8.0 release build, whose baseline was public v0.7.3, commit `a92d658530a7fd30f958c1af3814a604803368d0`.

## Published v0.8.0 engineering checks — 2026-09-07

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

In the published v0.8.0 build, the core grew by 123 whitespace-delimited words from v0.7.3 and the cold agent-state procedure was 952 words. The loader adds no unconditional read of that procedure. These are static measurements; actual retrieval, latency, setup burden and adherence require observation.

Use [real-campaign playtesting](ADMIN/PLAYTEST_V08.md) to assess recognizability, initiative, cause-driven change, pacing, saving and continuation with different models. Notes are optional and outside fictional authority. A rejection is not by itself evidence of independence, and an enjoyable session is not proof of lossless memory.

Recovery remains a model-operated procedure, handover markers are not operating-system locks, and private files are not encrypted. No new empirical claim of universal host compatibility, unbiased initialization or fully lossless transfer is made.
