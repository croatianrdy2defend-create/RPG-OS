# RPG OS experimental verification

## Game-only distribution separation — 11 September 2026

Version remains 0.9.6. The standalone GAME directory passes its own structural validator without DOCS, DEV or TEST_REPORTS. All 318 retained regression cases completed (314 passed, four platform-specific skips, zero failures); the separate 15-case distribution suite passed. Existing regressions run in an explicitly assembled developer fixture; distribution tests separately inspect the actual game-only layout and ZIP builder. Published-record verification preserves 30 sessions, 260 exchanges, 48 hashed files and the original review limitations. This is packaging/integrity evidence, not new gameplay or semantic-review performance.

See [distribution details](DISTRIBUTION.md) and [current commands](../DEV/README.md). Earlier entries below retain their historical scope and results.

## v0.9.6 tiered, source-bound save review — 2026-09-11

Local Linux verification of the prepared public kit completed **318 tests: 314 passed, 4 platform/privilege skips, zero remaining failures** across ten sequential suites. Whole-tree structural validation passed with no findings and a stable tree. The unchanged core matched the supplied v0.9.5 archive and the live repository's core tree before editing; the previously published TEST_REPORTS folder is preserved on GitHub and deliberately excluded from fresh-install distribution.

| Suite | Discovered | Passed | Skipped |
|---|---:|---:|---:|
| test_validate.py | 68 | 68 | 0 |
| test_handover.py | 36 | 36 | 0 |
| test_package_release.py | 24 | 24 | 0 |
| test_read_source.py | 31 | 30 | 1 |
| test_search_index.py | 33 | 31 | 2 |
| test_evidence.py | 33 | 32 | 1 |
| test_save_audit.py | 39 | 39 | 0 |
| test_agent_state.py | 14 | 14 | 0 |
| test_autosave.py | 34 | 34 | 0 |
| test_encounter_generation.py | 6 | 6 | 0 |

The 39 new save-review tests check tier selection, read-only selected diff, save identity/revision/parent and archive boundaries, exact capture stopping points, frozen write/removal scope, changed-candidate/readback rejection, pending/missing-source handling, explicit source-conflict declarations, duplicate text retention, safe paths and CLI compatibility. Their reports contain deliberately supplied synthetic judgments. They do not run an AI reviewer, discover a prose contradiction or measure semantic error detection. Two additional packaging tests verify repository-only report exclusion without allowing unrelated tracked campaign content into the kit.

Two development regressions were caught and fixed before this final run: the generic report-template exit status was accidentally changed while adding pending save-review handling; a packaging error-message change broke an existing assertion. The original CLI behavior was restored and the diagnostic retained compatibility. No old failure was relabeled a pass or removed from the suite.

The semantic acceptance cases in [ADMIN/TEST_SAVE_REVIEW.md](ADMIN/TEST_SAVE_REVIEW.md) are **NOT RUN** for v0.9.6. No blind reviewer trial, fresh-context campaign, human enjoyment study, measured model latency/token cost or 100-session trial was performed for this patch. Lightweight checkpoint checks offer less assurance than a source review; they are not equivalent validation at lower cost. Source-first methodology already existed, and uniform routing does not remove same-model review blind spots. Source coherence remains a separate human/model assessment.

No Mermaid diagram was changed. Public engine/world rules, accepted campaign facts, empty live templates and original playtest report remain unchanged. Release CI reruns the checks and committed-blob packaging; its actual outcome belongs to the publication commit and is not inferred from these local results.

## v0.9.5 session preparation, closure and feedback — 2026-09-10

Local Windows verification of the assembled public source discovered **277 tests: 269 passed, 8 platform skips, zero remaining failures** across the nine release suites. The final structural suite includes the session control, derivative preparation and compatibility checks; packaging and handover cover the new surfaces through their existing mechanisms.

| Suite | Discovered | Passed | Platform skips |
|---|---:|---:|---:|
| test_validate.py | 68 | 67 | 1 |
| test_handover.py | 36 | 35 | 1 |
| test_package_release.py | 22 | 22 | 0 |
| test_read_source.py | 31 | 28 | 3 |
| test_search_index.py | 33 | 32 | 1 |
| test_evidence.py | 33 | 31 | 2 |
| test_agent_state.py | 14 | 14 | 0 |
| test_autosave.py | 34 | 34 | 0 |
| test_encounter_generation.py | 6 | 6 | 0 |

Adversarial parser checks exposed two initial shadow-control misses: an outer-pipeless table outside the administrative section and control rows preceding the canonical table. Both were fixed with regressions before delivery. A final cross-field check rejects closing/ended sessions still claiming feedback is not due, while retaining valid early feedback and unfinished ended-session feedback. The final validator suite and three relevant packaging cases passed after that change; previously passing unaffected suites were reused. Platform skips include Windows symlink-creation limitations. No skip is counted as a pass.

Whole-tree structural validation passed with zero findings for the public unbound source and the separately assembled bound upgrade candidate. The latter also passed its six campaign-specific encounter checks, which remain outside the public package. The package continues to exclude runtime PREP, live session control and private campaign content. The release workflow independently tests and verifies the committed fresh-install archive before publishing; its actual run belongs to the triggering commit, not to these local suite counts.

One guided model rehearsal recorded 17 concrete transitions using supplied synthetic source facts and feedback: actual-play permission after bind, a pending choice through ordinary Save and a new-chat-style resume, explicit ending and feedback, a sourced synthetic zero award, repeated End, a second session, late feedback after PREP loss, finite completion, immediate stop followed by decline, and readiness without play. The recorded responses retained the tested choices, session identities, feedback, completion and settled zero. Repeated End on already saved unchanged closure reported the existing receipt rather than claiming a fresh save; a separately requested new full save was not exercised in that turn.

This was a single-context guided rehearsal with simulated persistence receipts, not independent fresh-context recovery, actual file publication, unscripted award judgment or long-campaign evidence. Missing-rule choices, real save failure/recovery, arbitrary engine beginning effects and the complete connected [S01–S19 cases](ADMIN/TEST_SESSION.md) were not exercised end to end. Structural tests do not prove feedback quality, causal reasoning or once-only GM judgment. Synthetic people, raw rehearsal content and private campaign records are not distributed.

All eleven MECHANICS Mermaid blocks parsed with Mermaid 11.12.0. The changed setup diagram rendered in a local headless browser and was visually inspected: verified bind waits for an actual PLAY request before SESSION preparation and the accepted opening. Other diagrams were unchanged.

## v0.9.4 universal encounter generation — 2026-09-09

Local Windows verification of the clean unbound release candidate discovered **253 tests: 246 passed, 7 platform skips, zero failures** across nine sequential suites. The prior eight suites remain, with one additional packaging test and six encounter-generation checks. All nine suites passed on their first execution against this prepared public candidate. Whole-tree structural validation passed with zero findings and a stable measured tree.

| Suite | Discovered | Passed | Platform skips |
|---|---:|---:|---:|
| test_validate.py | 48 | 48 | 0 |
| test_handover.py | 36 | 35 | 1 |
| test_package_release.py | 18 | 18 | 0 |
| test_read_source.py | 31 | 28 | 3 |
| test_search_index.py | 33 | 32 | 1 |
| test_evidence.py | 33 | 31 | 2 |
| test_agent_state.py | 14 | 14 | 0 |
| test_autosave.py | 34 | 34 | 0 |
| test_encounter_generation.py | 6 | 6 | 0 |

The new suite verifies optional selection, source routing, concrete-state ordering, three determinations/six faces maximum, five bands covering totals 2–12, and all 36 independent dice-pair combinations with counts 3/7/16/7/3. These are checks of documented rules, not random samples or model behavior. Packaging exercises exact helper inclusion while preserving an unbound save and rejecting nearby setting/campaign paths. Both GitHub workflows now include the encounter suite and verify the committed package; their actual run status belongs to the triggering commit, not this local test result.

Five small two-stage developer rehearsals covered a task-bound adult, a sourced territorial animal, controlled credential gates, a bacterium and an entity with a missing required source. The three rolled fixtures were reset and repeated after final selection of 2d6. Observed responses retained task/relationship limits despite strong attraction, gave the middle band concrete ordinary energy, respected sensory and controller communication limits, followed a fixed chemical response, and left missing capacities unresolved. The first animal fixture omitted explicit unobstructed sight; the agent correctly withheld detection. That input was clarified prospectively and supplied at establishment in the final repeat.

The rehearsals used visible establishment, deterministic supplied inputs and explicit case resets in one agent context. They did not establish independent fresh-context isolation, unprompted play, population distributions, save/handover fidelity or crowded long-context reliability. Formal U01–U26 remain separately NOT RUN. No private actor, campaign binding or raw audit transcript is distributed.

All eleven MECHANICS Mermaid blocks are unchanged from v0.9.3, so no diagram rerender was required. The existing README introduction is preserved. The public instance and archive remain blank and unbound; Freeform remains the only selectable engine. The new helper requires explicit selection and does not impose dice or change existing campaign agreements.


## v0.9.3 temporary encounter state — 2026-09-09

Local Windows verification of the clean unbound release candidate discovered **246 tests: 239 passed, 7 platform skips, zero remaining failures** across the eight release suites. Structural validation passed with zero findings for both the unbound kit and the installed bound workspace. The companion campaign-specific suite is kept outside the public distribution; the bound workspace total was 251 tests, 244 passed and the same seven platform skips.

| Suite | Discovered | Passed | Platform skips |
|---|---:|---:|---:|
| test_validate.py | 48 | 48 | 0 |
| test_handover.py | 36 | 35 | 1 |
| test_package_release.py | 17 | 17 | 0 |
| test_read_source.py | 31 | 28 | 3 |
| test_search_index.py | 33 | 32 | 1 |
| test_evidence.py | 33 | 31 | 2 |
| test_agent_state.py | 14 | 14 | 0 |
| test_autosave.py | 34 | 34 | 0 |

The first public evidence-suite attempt completed its test assertions but failed in Windows temporary-directory cleanup with `WinError 145`; an unchanged rerun passed. The first bound autosave check ran while the new release-notes file was still being written; its release-note existence check passed when rerun after preparation. These initial failures are not counted as successful executions.

All eleven MECHANICS Mermaid diagrams rendered successfully with Mermaid 11.12.0 in a local headless browser. The changed lifecycle diagram was visually inspected. The public README introduction was preserved from the existing repository; generic instructions and version guidance were updated below it.

Two bounded paired crowded-scene pilots compared the prior rules with the two Resolve additions, including full saves and fresh-context continuations. The explicit High repeat retained the tested observations, unheard-speech boundaries and pending-action dependencies in both variants. Both witnesses spoke publicly in that repeat. The trials did not demonstrate an advantage from the added paragraphs, silent-witness reliability under long context, or complete private reactivation on return. A small hidden-device-detail disclosure remained an observed portrayal defect. These results are limited behavioral observations, not a full execution of the cold U01–U26 cases, which retain their NOT RUN status.

Five-field activation and release are model-operated instructions, not an independent simulation or guaranteed hidden memory. The public kit contains no private campaign module, actor, saved encounter, raw session transcript or campaign-specific test suite. Packaging verifies the committed unbound inventory and archive integrity separately; it does not establish model compliance or long-campaign quality.

## v0.9.2 announced autosave — 2026-09-08

The implementation candidate is commit `480174e37f1ee299441b73cda5961f897f60c538`, based on published v0.9.1 commit `7c1499c084c96595a13f73582176332413749b8f`. [Structural validation run 34205017056](https://github.com/croatianrdy2defend-create/RPG-OS/actions/runs/34205017056), job `101992375832`, completed successfully on GitHub's Ubuntu 24.04.4 runner. The logs were read after completion. A local full checkout was unavailable in this authoring environment; these are remote CI observations, not claimed local test runs.

| Check | Observed candidate result |
|---|---|
| Whole-tree structural validator | PASS, zero findings; stable measured tree and matching executed/target validator |
| Structural regression suite | 48 passed |
| Handover regression suite | 36 passed |
| Packaging regression suite | 15 passed |
| Exact source reader | 30 passed, 1 platform skip |
| Scoped lexical search | 31 passed, 2 platform skips |
| Evidence capture/report checks | 32 passed, 1 platform skip |
| Agent-instruction regressions | 18 passed |
| Autosave scheduler, routes and synthetic metadata | 34 passed |
| Total | 248 discovered: 244 passed, 4 platform skips |
| Actual committed fresh-install package | Exporter completed; RPG_OS_v0.9.2.zip checksum check OK |
| Live autosave/model-switch cases A01–A10 | NOT RUN |
| Native Windows repetition for v0.9.2 | NOT RUN |
| Hidden-state completeness, long-campaign and host context-transfer reliability | NOT ESTABLISHED |

The new suite tests default-off permission, one-response notice ordering, coalescing, operator overrides, supported context sources, pressure-episode debounce, failure/blocking decisions, absence of scheduler filesystem writes and compatible checkpoint metadata. The synthetic save fixtures manually assemble expected records under the existing validator; they do not execute a model-operated protected checkpoint. They therefore do not establish that a model notices every trigger, preserves every private fact, or follows the procedure in live play.

The actual scheduling helper is read-only and optional. The accepted model-operated protocol invokes ADMIN/CLOSE_CONTRACT.md for persistence. Recovery markers remain conventions rather than OS locks, readback is fallible, and a checkpoint does not preserve new exact archive evidence. See [Autosave](../GAME/ADMIN/AUTOSAVE.md) and [the separate behavioral cases](ADMIN/TEST_AUTOSAVE.md).

A successful checkpoint during a high-context episode must not create a repeated pressure-only save loop: the episode stays handled until a supported below-threshold reading or fresh boot. The outgoing context saves before a planned model/reasoning switch. No empirical claim about the host's internal context transfer follows from that conservative rule.

The final documentation commit reruns the same branch checks before promotion. Final publication must independently pass the release workflow on its exact triggering commit; consult [the release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) and [v0.9.2 assets](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.9.2) for that final commit and result. This recorded candidate result is not a claim that an unobserved later run succeeded. No live campaign was modified or given autosave permission by publishing this kit.

The following sections retain earlier observations at their original scope.

## v0.9.0 source and evidence tools — 2026-09-08

The source-access implementation was initially published as v9.0.0 at commit `3d6ad58c920691929295fdc19ba185029a38dbbe`. v0.9.0 corrects that release number and adds a narrow Windows Python 3.12 source-reader compatibility fix. Path/handle identity metadata is compared across APIs, while each API's full before/after signature retains its own ctime check. Four added regressions cover different API timestamp representations, same-API timestamp mutation and actual same-size/same-mtime file replacement before opening or after reading. The corrected release workflow repeats the regression and committed-package checks, then retires only the mistaken release/tag after verifying the corrected publication.

This experimental release starts from public v0.8.2, commit `e297c3f29debfda2bc610ccf08acbddd48f66242`. It adds optional source reading, scoped lexical search and evidence capture/report checks. Existing save/record formats and the direct-attention NPC procedure remain compatible. Verification below concerns this implementation; it does not establish long-campaign reliability.

| Check | Observed local result |
|---|---|
| Structural regression suite | 48 passed |
| Handover regression suite | 35 passed, 1 platform skip |
| Packaging regression suite | 15 passed, including new raw-capture exclusion and required-tool inventory checks |
| Exact source reader | 28 passed, 3 platform skips, including the four compatibility/mutation regressions |
| Scoped lexical search | 32 passed, 1 platform skip |
| Evidence capture and report checker | 31 passed, 2 platform skips |
| Total | 196 discovered: 189 passed, 7 platform skips on Windows; suites repeated on Python 3.11.9 and 3.12.14 |
| Capability probe | Exact local UTF-8/CRLF read and an actual SQLite FTS5 query demonstrated; host chat export explicitly unobserved |
| Whole-tree structural check | PASS, zero findings, stable measured tree and matching executed/target validator bytes |
| Mechanics diagrams | All eleven parsed and rendered using Mermaid 10.9.3; the two new source/audit diagrams visually inspected |
| Independent code review | Reproduced and fixed Windows short-path containment, changed nested-campaign eligibility, invalid cached passage ranges and empty-source delivery; focused suites rerun |
| Documented capture workflow | Import, integrity check, selected prior/current bundle, pending template, authored report and checker exercised through actual subprocess commands |
| Played-campaign upgrade, forty-session continuity, cross-model audit reliability | NOT RUN |
| Proposed E01 retirement and E02 repeatability diagnostics | NOT RUN as those named complete exercises |

The platform skips concern unavailable unprivileged symlink creation, FIFO support and a receipt alias case dependent on symlink creation. Actual Windows junction and 8.3 short-path tests ran successfully. Native platform checks are kept separate from simulated link/reparse rejection. The repository workflows run all six suites and package the exact triggering commit; their Linux observations are available in the release's Actions runs, not presumed here.

The version-correction cleanup step also passed twelve isolated mocked-API execution cases. These cover its exact old release/tag target, corrected-publication and asset gates, safe repetition after complete or partial retirement, refusal of changed identities and HTTP errors, and preservation of a tag retargeted during cleanup. These local cases do not claim GitHub deletion has occurred; consult the corrected release's workflow run for the actual result.

One fresh reviewer context also used the production tools on six selected synthetic cases. The fixture author did not pass expected verdicts to that reviewer. All 34 selected source bodies were delivered with tool-generated receipts, and all six authored reports passed hash, original-line quotation and schema checks on their first attempt: 100 citation occurrences verified exactly. The reviewer found the omitted appointment, ignored authorized correction and inherited licence error; preserved an ambiguous suggestion and a legitimate appearance change; and identified the unambiguous HP error as requiring a player decision because a narrow repair would invalidate the played escape. No campaign repair was executed.

A second fresh reviewer checked citation relevance against the 34 frozen bodies and found all 12 material findings supported, with no unsupported material claim found. This second review inspected sources directly and claimed no reader receipts.

That was one semantic integration pass by the same model family in a fresh context, not a cross-model or unattended long-run benchmark. Delivery receipts do not prove comprehension. The prior exploratory twelve-case repeated trial used a different diagnostic harness; its results are not counted as passes for this implementation. Source fixtures, raw captures and private audit artifacts are kept outside this unbound distribution.

The integration run exposed a usability gap: reviewers needed clearer report-field and citation instructions. The [audit guide](../GAME/ADMIN/EVIDENCE_AUDIT.md#complete-the-report-template) now includes the supported values, exact original-line quoting and delivery-receipt workflow. Candidate reports explicitly keep source coverage, unresolved questions, consistency and repair eligibility separate.

Before publication the final committed exporter must verify its public inventory, exact committed bytes, ZIP paths/CRCs, frozen unbound state and SHA-256. See [v0.9.0 release assets](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.9.0) and [release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) for actual publication evidence. The sections below retain earlier results at their original scope.

## v0.8.2 direct-attention baseline — 2026-09-07

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
| Issue form | YAML parses; unique field IDs and correctly nested v0.8.2 placeholder |
| Mechanics diagrams | All nine parsed and rendered with Mermaid 10.9.3; revised individual-state diagram visually inspected |
| Independent static behavior review | Direct-attention trigger, routine contact, undeclared intent, perception, reuse, bounded depth and existing resolution/persistence rules reviewed; no actionable issue found |
| B16 first-contact and fresh-chat diagnostics | Six optional manual cases documented, NOT RUN |
| Model-operated update of a played campaign | NOT RUN |
| NPC-capacity or long-campaign behavioral benchmark | NOT RUN |

The final committed exporter must verify the public inventory, exact committed bytes, ZIP paths/CRCs, frozen unbound state and written SHA-256 before publication. The [release workflow](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/release.yml) repeats regression and packaging checks on the published commit; consult it and the [v0.8.2 assets](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.8.2) for publication evidence. This source report does not claim a completed external run in advance.

These engineering results do not prove that a GM establishes its baseline before responding, retains unsaved private state, or portrays a large cast consistently. B16 asks for available factual state and operation evidence while leaving unavailable ordering unverified; private model reasoning is not required. New baselines remain best-effort conversation state until an authorized save succeeds. The release creates no running AI worker per NPC, full-cast scan, new schema or automatic write.

The sections below retain the scope and observations of earlier versions.

This report distinguishes engineering checks from human campaign observations and identifies the build each result describes. The v0.8.1 release tree starts from canonical public main, commit `40f8c021059b3f5a3f0f761441da117591871ae6`, with the reviewed simple fallback changes. The checks below were observed on the versioned release candidate. Historical [v0.7.2 trials](releases/V0.7.2_TRIALS.md) retain their original scope; they are not evidence of new agent-state behavior.

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
| Packaging regression suite | 15 tests passed |
| Total automated regression cases | 99 discovered: 98 passed, 1 platform skip |
| Mechanics diagrams | All eight parsed and rendered using Mermaid 10.9.3 in headless Chrome; the new agent-state diagram was visually inspected |
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
python -B TOOLS/test_read_source.py
python -B TOOLS/test_search_index.py
python -B TOOLS/test_evidence.py
python -B TOOLS/test_agent_state.py
python -B TOOLS/test_autosave.py
python -B TOOLS/validate.py --root .
```

On a clean committed public checkout, `python -B TOOLS/package_release.py` exports that commit, rejects non-public or populated campaign paths, validates its frozen unbound tree and compares every archived file to the committed blob. It verifies ZIP CRCs and the written SHA-256 checksum. A downloaded play folder does not require these development tools or Git.

## Runtime scope and remaining observations

Ordinary PLAY remains read-only and creates no private scratch file. In v0.9.2 a separately accepted announced-autosave policy may enter the protected ADMIN checkpoint procedure; without that grant, no automatic checkpoint occurs. Newly established unsaved state has best-effort retention in available conversation. Authorized saving preserves the complete accepted present; a checkpoint retains the previous archive evidence boundary. The receiving GM leaves frozen source authorities unchanged.

Setup records a pending generated determination before obtaining its input. After an interrupted bind, physical restoration alone does not cancel the accepted setup: its active recovery route remains until completion or explicit setup cancellation/replacement. A genuinely lost result is reported as a gap. Optional diagnostic M07 in [ADMIN/TESTS](ADMIN/TESTS.md) describes this model-operated recovery edge and remains NOT RUN; the automated active-marker checks do not validate its semantic execution.

The [v0.8 upgrade procedure](../GAME/ADMIN/UPGRADE_V08.md) has been reviewed for program/data ownership, backup preservation and compatibility routing. A complete model-operated upgrade of a played campaign was not executed during this build. Existing synthetic compatibility and recovery checks do not establish that broader result.

In the published v0.8.0 build, the core grew by 123 whitespace-delimited words from v0.7.3 and the cold agent-state procedure was 952 words. The loader adds no unconditional read of that procedure. These are static measurements; actual retrieval, latency, setup burden and adherence require observation.

Use [real-campaign playtesting](ADMIN/PLAYTEST_V08.md) to assess recognizability, initiative, cause-driven change, pacing, saving and continuation with different models. Notes are optional and outside fictional authority. A rejection is not by itself evidence of independence, and an enjoyable session is not proof of lossless memory.

Recovery remains a model-operated procedure, handover markers are not operating-system locks, and private files are not encrypted. No new empirical claim of universal host compatibility, unbiased initialization or fully lossless transfer is made.
