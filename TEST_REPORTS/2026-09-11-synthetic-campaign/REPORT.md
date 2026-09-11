# RPG OS v0.9.5: longitudinal synthetic playtest and evidence-audit report

**Publication date:** 11 September 2026  
**Tested source:** `211242384046afabe2135e9fee10b11ba4c19901`  
**Campaign:** *The Ninth Sluice*, continued as *Afterwater*  
**Scope:** an initial ten-session experiment followed by twenty additional condensed sessions; thirty campaign sessions in total  
**Publication type:** test documentation and supporting records, not a software release or a patch

> **Bottom line:** RPG OS supported a continuing, consequential campaign under supervised, instrumented operation. Its original-source audit procedure exposed semantic save errors that structural validation accepted, including an error inherited by successive saves. The evidence does not establish autonomous, blind, human, all-mechanism, or 100-session reliability. The experimental writer had real defects, and two first-pass semantic reviews missed issues within their selected sources.

Start with this report, then the [test protocol](TEST_PROTOCOL.md), [coverage matrix](COVERAGE.md), [transcript index](transcripts/README.md), and [evidence index](evidence/README.md). All campaign people, events, and finances below are fictional test material. Some records reveal GM-only scenario information. Deliberately corrupted fixtures are not accepted campaign state.

## 1. Executive assessment

The strongest positive result is not simply that thirty numbered sessions exist. It is that an early, conditional obligation survived new work, procurement, a failed purchase, changed circumstances, later fulfillment of its trigger, actual payment, and a subsequent month away. The continuing campaign preserved a failed flood defense rather than rewriting it into success. It distinguished personal money from restricted public funds, permissions from physical capability, offers from accepted work, and private knowledge from public findings.

The strongest operational warning is that a valid file can still be a misleading save. Both experiments demonstrated that the structural validator can accept missing or incorrect consequential state. This is consistent with its documented scope; it is not evidence that it promises semantic certification and fails to deliver it. The second experiment specifically exercised the existing transcript-grounded audit procedure rather than treating structural validation as its substitute.

That procedure made meaningful corrections possible. It also had fallible execution: the same assistant generated the play, designed the deliberate corruptions, and authored the semantic judgments. Audits were scoped and completed in batches. Two first-pass reports later required supplements for missed selected-field problems. A third late finding concerned an intermediate checkpoint outside the primary full-save comparison. These distinctions must survive publication; an unqualified audit success percentage would obscure them.

**Assessment:** promising architecture for a maintained, supervised long campaign; demonstrated benefits from evidence-grounded review; important host-integration and review-coverage risks; no numerical estimate of session-100 reliability. No defect in the unchanged core was established within the exercised cases, but that is not a claim that the core is defect-free. See [verification](evidence/verification.json), [review misses](evidence/review-misses.json), and [coverage](COVERAGE.md).

## 2. Provenance, version, and publication boundary

The tested upload identifies itself as **v0.9.5**. Before this publication, the Git tree reconstructed from that original upload was compared with the repository's current source tree. Both were `fd8596cc4c98f20362ab1faa5de897dd3e17e2a4`, associated with commit `211242384046afabe2135e9fee10b11ba4c19901`. This identifies the actual tested source, not merely a matching version label.

The continuation's archived verifier was run again for publication. Its output matched the previously delivered verification JSON. All **13,390 entries** in the continuation package's manifest matched their included file bytes. These are integrity and reproducibility checks of recorded artifacts, not another playtest or a fresh semantic assessment. [Publication verification](evidence/publication-verification.json)

Only the `TEST_REPORTS/` documentation subtree is added by this publication. The root `VERSION`, existing core instructions, engines, tools, live campaign registers, release workflow, and existing release assets are not edited. No new version or release tag is requested or created.

This GitHub publication contains the detailed report, test protocol, full original synthetic dialogue bodies for the thirty sessions, coverage, selected original machine-readable results, and derived audit dossiers. It is **not a mirror of the complete original ZIP archives**: thousands of duplicated runtime files, frozen bundles, snapshots, and experimental authoring scripts remain in the separately supplied full archives. Their sizes and SHA-256 identities are recorded in [publication-verification.json](evidence/publication-verification.json). A checksum identifies an archive; it does not make that archive downloadable from this repository. Archive-relative paths in preserved results are provenance references, not links to files necessarily mirrored here.

## 3. Research questions and what counts as evidence

The first experiment asked whether a complex campaign could remain coherent over ten connected sessions. The continuation asked a more specific question: **can original accepted-play evidence validate a save and expose semantic corruption, including omissions that structurally valid files conceal?** It also broadened exercise of the operating mechanisms through actual play and disposable branches.

Five evidence classes are kept separate throughout this report:

| Evidence class | What it establishes here | What it does not establish |
|---|---|---|
| Recorded synthetic play | The particular declared choices, generated responses, and documented consequences on this authored path. | Human enjoyment, representative player behavior, or independent GM performance. |
| Persisted states and differences | What the experimental host actually retained at full saves and checkpoints. | Whether every retained interpretation is faithful to play. |
| Automated checks | File structure, source identity, quotation fidelity, selected arithmetic, and specific helper behavior. | General narrative truth, appropriate adjudication, or complete source selection. |
| Source-grounded semantic judgments | The assistant's cited interpretation of the selected play and state evidence. | Blindness, independence, exhaustive coverage, or infallibility. |
| Deliberate corruption demonstrations | That specified wrong states can be contrasted with their original evidence through the audit workflow. | A measured detection rate on hidden, novel, or naturally occurring errors. |

The exact deployed model build and reasoning configuration were not independently instrumented in the archived test record. The relevant known condition is **same-assistant, same-context generation and judgment**, supported by an experimental Python writer. No separate human player or incoming independent model was used. [Verification limitations](evidence/verification.json)

### 3.1 Canonical evidence is interpreted accepted play

The audit's reference is what accepted play and authorized instructions established, not whatever the latest summary happens to say. However, a raw transcript also contains attempted actions, questions, testimony, operational requests, mistakes, and superseded material. An attempted purchase is not necessarily an accepted purchase; an NPC's accusation is not automatically world truth; an authorized correction can supersede earlier wording without erasing the original source.

The shipped [evidence-audit procedure](../../ADMIN/EVIDENCE_AUDIT.md) already addresses this distinction. It requires actual sources, independently identifying consequential developments, comparison in both directions, authority analysis, and support for repairs. The test did not invent a new audit subsystem and attribute it to RPG OS. The raw-source layer also explicitly distinguishes capture integrity from accepted fiction. [Raw-evidence contract](../../EVIDENCE/README.md)

### 3.2 Why a source reader is not a semantic reviewer

The helper can verify that a passage came from the selected source bytes and that a quoted line is exact. It cannot, by those checks alone, establish that the passage is relevant, unsuperseded, correctly interpreted, or sufficient to resolve the question. Likewise, a delivery receipt proves delivery of selected bytes, not comprehension or reviewer independence.

This distinction matters to the headline counts: “report_structure_verified” is a successful integrity/report check, not an automatic verdict that the campaign is semantically correct. The archived judgments are published as judgments, not relabeled as detector output. [Semantic-case dossier](evidence/semantic-cases.json)

## 4. Experimental design and execution

### 4.1 Initial ten-session phase

The initial campaign used the bundled Freeform engine. Mara Venn, a former lock surveyor, returned to a flood-threatened port. Family obligations, vulnerable patients, a borrowed boat, missing repair equipment, disputed ownership, and contractor misconduct created interacting problems. The player was cautious but imperfect: she refused a job, made an unsupported accusation, negotiated limited commitments, retreated when necessary, and eventually abandoned pump restoration when resources did not support it.

The phase recorded **100 player/GM pairs**, ten full session saves, one manual checkpoint, and five disposable fault probes. A separate bind accounts for another save identity; save revisions are not session counts. The ten condensed sessions covered approximately 76 hours of fictional time. They were not ten full-length human tabletop meetings. [Baseline verification](evidence/baseline-verification.json); [sessions 1–10](transcripts/README.md)

The arc ended with Lower Quay flooded, the patients evacuated, evidence preserved, and unfinished debts and repairs retained. This failure was accepted campaign history. Later repair did not retroactively prevent it.

### 4.2 Twenty-session continuation

The continuation resumed the actual session-ten files rather than creating a replacement starting situation. Each additional session contained eight recorded player/GM exchanges. Its totals were:

| Measure | Recorded result |
|---|---:|
| Additional sessions | 20, numbered 11–30 |
| New player/GM pairs | 160 |
| Total campaign sessions | 30 |
| Total recorded pairs across both phases | 260 |
| Additional full session saves | 20 |
| Additional checkpoints | 5: four announced automatic, one explicit manual |
| Primary continuation audit reports | 20 |
| Extra narrow recording-correction save | 1; not a new session |
| New fictional elapsed time | 87,895 minutes: 61 days and 55 minutes |
| Continuation start / end | Day 4, 12:00 / Day 65, 12:55 |
| New seeded random-input calls | 3 |
| Final save identity | `sluice-save-038` |

The original ten archive bodies remained byte-identical, and all 86 files in the immutable-core manifest matched. The final save was structurally **PASS WITH WARNINGS**, with `PREP_STALE_BASE`. Its retained stale PC-goal wording means it is not declared universally semantically clean. [Continuation verification](evidence/verification.json)

### 4.3 Source capture and review sequence

The experimental host emitted synthetic player/GM output turn by turn before the corresponding save. Those source files are original generated output for this experiment, not prose reconstructed from final state. They are also **not a platform export of real human chat**.

At each full save, the evidence workflow captured the source and froze selected prior/current records. Detailed semantic reports were completed in batches between five-session segments. They were not independent prepublication gates before every later turn. Consequently, an erroneous field could survive into several later snapshots before its recording repair. Those snapshots and original report judgments were retained rather than retrospectively cleaned.

The reviewer first identified consequential developments from the selected play, then compared resulting state for omissions and unsupported additions. Scope remained explicit. Agreement between two saves did not authenticate an inherited claim. When original evidence was missing or contradictory, the proper result could be undetermined rather than an invented resolution. [Primary report index](evidence/primary-audit-statuses.json); [test protocol](TEST_PROTOCOL.md)

### 4.4 Separate destructive experiments

Corruption fixtures, interrupted writes, handover tests, and raw writer lifecycle probes ran on disposable copies. Their deliberately damaged states were not accepted changes to the main campaign. This separation is essential when interpreting an apparent debt resurrection or duplicated ending: some occurred only because the test intentionally constructed them.

## 5. Campaign progression and systems under pressure

| Session | Consequential development | Principal pressure |
|---|---|---|
| 11 | Mara accepts bounded relief work without receiving an advance. | Offer versus earnings; injury limits; conditional debt. |
| 12 | An accepted report earns six crowns once; food costs two. | Payment event, duplicate-copy request, checkpoint synchronization. |
| 13 | A correction physically reaches its recipient; autosave is disabled prospectively. | Information paths; agreement changes. |
| 14 | A later examination supports recovery; a new fare is distinct from old used passage. | Time, injury, completed purchases. |
| 15 | A restricted 24-crown purse is transferred; outbound passage costs four. | Public money versus personal income; unresolved crossing. |
| 16 | A real gust draw informs a crossing; Mara chooses an overnight wait. | Random stakes, unresolved agency, manual checkpoint. |
| 17 | Six crowns are deposited with written conditional return terms, not a completed purchase. | New obligations, acceptance boundaries, safety veil. |
| 18 | The assay passes; a separate cancellation agreement returns the deposit. | Legitimate supersession without falsifying the test. |
| 19 | A six-plus-six manufacturing order has an eight-day lead time. | Logistics; conflicting source chronology. |
| 20 | The ring and document are delivered; 20 spent and four returned close procurement. | Custody, inventory retirement, account closure. |
| 21 | An explicit operator correction resolves chronology; outlet flow is clarified as the loan trigger. | Correction authority; prospective clarification. |
| 22 | The prepaid assembly hour is actually used; a dry rotation is performed. | Service redemption; active-state wording. |
| 23 | Actual outlet flow makes the remaining three crowns due. | Trigger evaluation; no remote knowledge for Sera. |
| 24 | Mara tells Sera and pays three; one crown buys a meal. | Settlement, communication, no duplicate debt. |
| 25 | An accepted operating report earns eight; private wrongdoing remains distinct from a verdict. | Scoped authority and payment. |
| 26 | A fourteen-observation commission begins; autosave is delayed and resumed. | Bounded work; checkpoint after departure. |
| 27 | A panel determines city title; Nessa receives her own nine-crown refund. | Ownership versus custody; beneficiary identity. |
| 28 | Repeated inquiry creates no new dispatch; an old loan passage is retrieved. | No duplicated world event; exact historical retrieval. |
| 29 | Remaining observations are completed; eight are paid and four donated. | Actual completion; bounded learning without a numerical level. |
| 30 | Thirty authorized quiet nights pass; settled accounts remain settled. | Long-gap return; no forced sequel; stale current goal. |

These are summaries of the [original transcripts](transcripts/README.md), not additional scenes or independent observations. Operational exchanges are included in the recorded pair count.

## 6. Positive longitudinal findings

### 6.1 Conditional obligations changed only when their conditions changed

The original loan distinguished three crowns payable when the western pump ran from five payable after survey wages cleared. It also excluded purchasing Mara's testimony. The wage-linked portion was paid in the first arc. The pump-linked portion remained conditional throughout early recovery and procurement.

In session 21, the participants clarified prospectively that disconnected rotation did not satisfy the trigger; actual water through the western outlet did. The dry diagnostic in session 22 therefore did not trigger payment. Outlet flow in session 23 did. Sera did not learn this remotely: Mara informed her and paid in session 24. The account remained settled after the later quiet month. [Sessions 21–24 and 30](transcripts/README.md)

This is a more useful persistence test than freezing an old number. Faithful memory preserves the basis for a fact and the legitimate events that change it. It must neither delete an unresolved debt nor resurrect one that was actually paid.

### 6.2 Restricted funds and personal money remained separate

Mara entered the continuation with zero personal crowns. The recorded personal flows were `+6 -2 -3 -1 +8 +8 -4`, ending at **12**. The verification ledger associates each transition with the generated response establishing it. Nessa's nine-crown refund was never credited to Mara.

The restricted account received 24. Outbound passage cost four; a six-crown reseller deposit was later returned; the manufactured ring cost twelve; return passage cost four. Net expenditure was twenty, and the remaining four were physically returned. The account closed at zero, not as unearned player wages. [Transaction-level verification](evidence/verification.json)

Correct arithmetic alone would not establish correct ownership. The important observed distinctions were who received the funds, what spending was authorized, when a payment actually happened, and which obligation it resolved.

### 6.3 Legitimate change was not mistaken for corruption

The reseller assay passed. Mara nevertheless negotiated a new accepted cancellation because the ring could return to sale. The deposit refund therefore followed the later agreement, not the original rejected-assay condition. A reviewer enforcing only the original clause could falsely flag the refund or incorrectly rewrite the passing result.

The valid control C02 retained both the passing assay and the real refund. It was judged consistent in the selected scope. The mutation M08 falsely attributed the refund to a failed test and was judged inconsistent. These are authored contrast cases, not blind classifier results. [Session 18](transcripts/session-18.txt); [C02 and M08](evidence/semantic-cases.json)

### 6.4 Failure, knowledge, and physical limits remained consequential

The continuation did not erase the flood. Written authorization did not substitute for missing physical prerequisites. A private determination about wrongdoing did not become a public conviction merely because the GM possessed it. Jory could cooperate within a paid, bounded agreement without an invented friendly past. In the first phase, the unavailable seal required a genuine change of objective rather than a convenient rescue of the plot.

These are positive observations on the authored path. They are not evidence that all future GM outputs will respect those distinctions. [Transcript index](transcripts/README.md); [coverage](COVERAGE.md)

## 7. Organic failures and host-integration findings

Severity below is an analytical prioritization, not a measured probability. “High” denotes a defect capable of corrupting a resume or duplicating a consequential operation; “medium” denotes misleading state or an important execution gap; “low” denotes a narrower presentation/metadata issue. A potential consequence is not presented as an outcome that actually happened.

| Finding | Expected versus observed | Attribution, impact, and disposition |
|---|---|---|
| Initial setup mismatch | Opening character wording and bound save should agree; the generated setup did not initially agree. | Experimental setup error; structural validation caught it before play. Repaired. |
| HOST-01: duplicate baseline ownership | Current active state should have an unambiguous owner. The first writer copied opening baseline fields into durable person records while retaining current encounter state elsewhere. | Medium host risk. Found after session six; ten current person records repaired. Original snapshots remain. No resulting altered fictional outcome was demonstrated. |
| Preparation formatting | Optional preparation records should contain prescribed metadata; early writer output did not. | Low writer error. Warnings prompted a formatting correction. Distinct from legitimate stale-provenance warnings. |
| Stale offers and completed work | Current descriptions should follow actual acceptance, completion, and payment. Several fields retained incomplete or unaccepted labels. | Medium writer synchronization issue. Detected in first-pass continuation audits and repaired narrowly; inherited snapshots retained. |
| Malformed correction index | A recording-correction archive should retain required routes; the initial correction writer omitted fields. | Structural errors were detected. The correction was repaired before further play and a later start gate was added. This is not a semantic-only failure. |
| Conflicting chronology | Source statements should support a unique time transition; session 19 combined “next morning” with a numerical timeline landing that evening. | Source-authoring ambiguity. Audit marked it undetermined. A simulated operator explicitly chose the intended numerical timeline in session 21. |
| Stale inventory and pump cause | A delivered document should leave inventory, and a serviceable delivered ring should change the recorded cause of the blockade. | Medium writer issue. Session-20 audit found the stale labels; a subsequent authorized recording correction addressed them. |
| Late agent-state establishment | The active basis should exist before participation requiring it. Bram and Ivo participated before the journal established their active basis. | Medium execution/provenance gap. Recorded as such; no retrospective hidden emotions were invented to disguise it. |
| Departure/checkpoint ordering | An autosave after departure should reflect the completed departure. A session-26 checkpoint still retained Voss as active. | High integration priority. Autosave ran before the host's later departure call. Later correct full save does not validate the faulty earlier checkpoint. |
| Checkpoint summary mismatch | Current-save situation should agree with paid work and coins. Session-12 checkpoint had six coins but retained “report incomplete, no personal cash earned.” | High resume-risk priority. Found during final inspection, outside the primary full-save comparisons. Preserved as LATE-03. |
| Missed K-4 appraisal update | Active appraisal should distinguish completed dry rotation from unperformed pressure/outlet tests. The selected field retained ambiguous compound wording. | Medium state/review issue, LATE-01. First-pass session-22 review missed it; cited supplement retained. |
| Missed stale current PC goal | A used prepaid hour should not remain a current goal to resolve or reschedule. Other work and obligation fields were correctly closed. | Medium state/review issue, LATE-02. First-pass session-30 review missed it despite relevant sources. The tested final save retains the error; proposed repair is separate. |

The first-phase duplicate-state evidence is preserved in [baseline-host-01.json](evidence/baseline-host-01.json). The three late findings are preserved in [review-misses.json](evidence/review-misses.json). Primary report statuses and summaries are in [primary-audit-statuses.json](evidence/primary-audit-statuses.json).

### 7.1 Raw lifecycle probe: duplicate endings and evidence

A disposable branch called the experimental writer's raw full-save and ending methods repeatedly without new play. The first ending added one receipt; the repeat brought the added total to two. The same T01/T02 evidence was archived again in multiple slices. An explicit decline of optional feedback was saved with status `received`.

The main campaign did not acquire those duplicate endings from this branch. Cash and elapsed time did not change, and Freeform supplied no numerical XP reward to duplicate. Nevertheless, the required once-only behavior failed at the experimental integration layer. The shipped rules specify the opposite behavior; this was not evidence of a shipped dispatcher intentionally duplicating awards. [Exact lifecycle results](evidence/session-boundary-probe.json)

The practical lesson is to test the actual host implementation of a protocol. Correct instructions and a passing structural validator do not, by themselves, enforce a once-only command or a last-archived-evidence cursor.

### 7.2 Why the final warning was not suppressed

`PREP_STALE_BASE` indicates that derivative preparation has a different recorded basis from the latest save/agreement. Merely changing its stamp would conceal provenance rather than review relevance. The main warning was retained. A separate branch actually read dependencies and revalidated preparation without changing fictional time or the save identity. [Verification](evidence/verification.json); [COLD branch](evidence/mechanism-branches.json)

## 8. Transcript-grounded audit results

### 8.1 First-pass reports: useful but incomplete

The twenty first-pass reports contained **14 consistent, five inconsistent, and one undetermined** statuses within their selected scopes. These are not independent successes and failures: four inconsistent reports partly trace the same inherited stale-state problem, while two originally consistent reports later received missed-issue supplements.

Do not interpret 14/20 as save reliability, or 20 checked reports as perfect semantic validation. The selected source boundary and the distinction between original judgment and later correction are essential parts of the result. [Primary report index](evidence/primary-audit-statuses.json); [supplemental findings](evidence/review-misses.json)

### 8.2 Twenty deliberately corrupted saves

All twenty completed corruption fixtures passed structural validation, with the ordinary preparation advisory. Each received an authored source-grounded inconsistency finding whose report citations were checked. The same assistant knew and designed the mutations. No automatic semantic detector was invoked and no sensitivity, specificity, precision, or detection percentage is claimed.

| Case | Deliberate semantic corruption | Authored assessment |
|---|---|---|
| M01 | Omit a newly established deposit obligation. | Inconsistent |
| M02 | Inflate the deposit amount. | Inconsistent |
| M03 | Invent purchase acceptance. | Inconsistent |
| M04 | Invent an early refund. | Inconsistent |
| M05 | Remove the refund qualifier. | Inconsistent |
| M06 | Turn restricted funds into personal money. | Inconsistent |
| M07 | Reverse the observed assay result. | Inconsistent |
| M08 | Give a valid refund a false cause. | Inconsistent |
| M09 | Turn custody into personal inventory. | Inconsistent |
| M10 | Revive a redeemed prepaid service. | Inconsistent |
| M11 | Leave a matured debt merely conditional. | Inconsistent |
| M12 | Give an NPC knowledge without a communication path. | Inconsistent |
| M13 | Resurrect a paid debt. | Inconsistent |
| M14 | Make spent money reappear. | Inconsistent |
| M15 | Promote private truth into a public verdict. | Inconsistent |
| M16 | Credit an NPC's refund to the player. | Inconsistent |
| M17 | Duplicate the later wage payment. | Inconsistent |
| M18 | Extend a completed duty. | Inconsistent |
| M19 | Add unchosen elapsed time. | Inconsistent |
| M20 | Delete a required active-state field. | Inconsistent |

The [case dossier](evidence/semantic-cases.json) preserves the selected summaries, source identities, line references, and exact quotations. For omissions, a short quoted fragment is not itself proof that the fact is absent from the entire file; that judgment depended on the full selected record in the original frozen bundle. The full bundle is in the separate archive, not recreated by the dossier.

### 8.3 Six valid-change controls

The controls retained an unchanged conditional deposit, the passed assay plus negotiated cancellation, actual payment closing the debt, healing after a later examination, retirement of a settled obligation object, and retirement of a genuinely departed active controller. Each was judged consistent for its selected question.

These controls matter because consistency is not immobility. An audit that restores every deleted object or insists on every old value can itself corrupt play. Legitimate retirement, supersession, completion, and changed knowledge must remain possible. Six non-blind controls do not establish a general false-positive rate. [C01–C06](evidence/semantic-cases.json)

### 8.4 Historical source scope: the decisive inherited-error test

S01 and S02 used an inherited false claim that Nessa's session-nine passage cost six crowns per leg, twelve total. Both later records repeated it. With the original booking outside the selected evidence, S01 was **undetermined**: repetition could not authenticate the alleged quotation.

S02 created a new, expanded evidence bundle containing the original booking. That passage established six crowns once for the bounded round trip, with the return included. The repeated claim could then be judged **inconsistent**. The original evidence, not agreement between two later summaries, resolved the question. [Original session-nine transcript](transcripts/session-09.md); [S01/S02 citations](evidence/semantic-cases.json)

This directly supports the proposed safeguard: accepted play is an independent reference against which a corrupted save can be challenged. It also locates an important implementation requirement: the reviewer must find and select the necessary original and intervening evidence. A reviewer that never retrieves the booking cannot honestly claim to have verified its price.

### 8.5 Evidence-integrity and fixture failures

Two genuinely mechanical negative tests altered captured source bytes and fabricated exact report text. The helper rejected them with `capture source hash/size mismatch` and `quote does not match original lines in record consistency` respectively.

The initial mutation roots were scoped audit selections, not complete executable packages. Their first structural runs failed missing-core checks; runtime dependencies were then supplied unchanged and validation rerun. One hydration attempt omitted `EVIDENCE/README.md`, and an early exception catcher used the wrong exception class even though the helper had already rejected tampering. These preparation failures were retained, not counted as successful semantic detections. [Mechanical probes and fixture notes](evidence/semantic-cases.json)

## 9. Mechanism branches and automated regression results

The continuation exercised interrupted-write recovery, actual indexed retrieval, original-source reading, stale/missing evidence handling, outgoing handover, same-context receive/return/import, import-once refusal, cancellation, cold review, preparation revalidation, adapter identity, and adding/refining a public setting brief on disposable copies.

Recovery blocked play during interruption, retained the old current-save pointer, restored exact prior bytes, and removed operation-created material. Handover preserved the source freeze and session identity, imported once, and rejected replay. Cancellation left campaign bytes unchanged. The additional adapter did not silently rebind the Freeform campaign, and an identifier collision was refused. These are observed file-protocol cases, not proof of operating-system atomicity, an independent receiver, or a full campaign on the added adapter. [Branch results](evidence/mechanism-branches.json)

### 9.1 Bundled suites

| Suite | Discovered | Passed | Skipped |
|---|---:|---:|---:|
| `test_agent_state.py` | 14 | 14 | 0 |
| `test_autosave.py` | 34 | 34 | 0 |
| `test_encounter_generation.py` | 6 | 6 | 0 |
| `test_evidence.py` | 33 | 32 | 1 |
| `test_handover.py` | 36 | 36 | 0 |
| `test_package_release.py` | 22 | 22 | 0 |
| `test_read_source.py` | 31 | 30 | 1 |
| `test_search_index.py` | 33 | 31 | 2 |
| `test_validate.py` | 68 | 68 | 0 |
| **Total** | **277** | **273** | **4** |

All nine suites completed with zero failures. The four platform-specific skips are not passes. The same suite set was exercised in both phases; repeating it does not create 554 distinct test cases. Several suites check schema, instructions, or helper behavior rather than live model decisions. The initial phase's 290 bounded assertions also contained repeated arithmetic/time checks, not 290 independent behavioral scenarios. [Regression records](evidence/regressions.json); [baseline verification](evidence/baseline-verification.json)

### 9.2 “All available mechanisms” is a coverage request, not a certification

The [coverage matrix](COVERAGE.md) distinguishes main play, disposable branches, regression-only coverage, and untested routes. There was no authentic legacy v0.5/v0.7/v0.8 campaign migration, no second complete new-game bind during the continuation, no complete campaign on the added adapter, no real context-capacity telemetry, no independent cross-model handover, and no comprehensive execution of every feedback or optional ledger variant.

Freeform does not supply the numerical combat/XP/class system of an unrelated engine. This experiment cannot validate those systems by inventing them. Injury was a fictional state variable, not a medical simulation.

## 10. Implications for session 100

The continuation strengthens the case for a long campaign more than another ten scenes inside the same emergency would have. It introduced actual account closure, service redemption, a prospective clarification, ownership adjudication, procurement lead time, commissioned work, and a month away. Old obligations returned and then legitimately stopped being active obligations.

The principal projected failure is still gradual continuity drift rather than a dramatic crash: a fact is omitted, later saves inherit the omission, and new play proceeds fluently without checking the original evidence. The S01/S02 contrast shows a workable route for exposing such drift. The organic review misses show why merely enabling an audit label is not a guarantee.

A dependable session-100 implementation therefore needs correct event-to-save synchronization, once-only lifecycle behavior, explicit evidence coverage, and review that can distinguish a live obligation from a retired one. It should also measure maintenance burden: how often a human or supervising model must intervene, how far an error propagates, and whether a correction prevents recurrence.

No completion probability, per-session failure rate, or numerical reliability score can be estimated responsibly from one same-assistant authored path. Fresh-context retrieval, independent review, longer conversations, broader behavior, and human usability remain separate evidence needs. [Limitations](evidence/verification.json); [coverage](COVERAGE.md)

## 11. Prioritized follow-up work — recommendations, not applied changes

### Priority 1: save only after the complete accepted event is represented

Treat money, inventory, situation summary, active participation, current goals, and unresolved choices as one accepted event update for checkpoint purposes. Run autosave after that update, not between a dialogue event and its later departure/retirement call. Validate intermediate checkpoints as resume points in their own right, not only final session saves.

Acceptance tests should include the actual session-12 contradictory checkpoint and session-26 late-retirement case. A later correct full save must not turn either earlier checkpoint into a pass.

### Priority 2: make endings and evidence publication once-only

Identify a session-ending operation with a stable key and reject a repeat that has no new ending to record. Maintain an explicit last-archived-evidence cursor. A full save during active play must not silently become another end-session operation. Store declined, pending, and received feedback distinctly.

The raw lifecycle branch supplies concrete negative fixtures. A proposed implementation should demonstrate unchanged receipts and archive extent after a repeated command, while permitting a genuinely new session ending later.

### Priority 3: use the existing semantic-audit procedure with explicit coverage

Identify what the conversation establishes before inspecting the destination fields. Check new obligations never written as well as old obligations deleted; unsupported additions as well as missing facts. Include operative current goals and situation summaries, not only numeric ledgers. Recover original and intervening evidence when a historical claim becomes relevant.

A source gap should remain explicit. Correcting an old term requires evidence of a legitimate resolving event or authorized correction; agreement between two summaries is insufficient. Revalidate preparation from its dependencies rather than restamping it. These recommendations operationalize existing contracts instead of introducing a competing master-memory file.

### Priority 4: separate the next evaluator from the author

Use an incoming context with only the intended startup material and access to the authoritative repository. Hide expected answers and mutation labels from the reviewer. Randomize both corruptions and legitimate-change controls. Score source selection, citation relevance, semantic detection, false alarms, and repair correctness separately.

Include old facts dormant across unrelated arcs, later renegotiation, ambiguous testimony, missing originals, and a real human usability trial. Record repair effort and propagation depth as well as completed session count. This is a proposal for stronger evidence, not work claimed by this publication.

## 12. Reproduction and preservation

The [test protocol](TEST_PROTOCOL.md) explains how to inspect the published subset, run the bundled structural/helper suites, and verify the separate full continuation archive. The archive's `verify_deliverable.py` performs integrity, recorded arithmetic, capture, citation, and RNG checks; it does not generate a new semantic review. Original source-delivery receipts are path-bound, so its relocation handling creates a temporary fresh byte-delivery receipt rather than falsifying the original one.

Do not run experimental authoring or destructive branch scripts over the accepted final campaign. Their overwrite guards and known failures are part of the experiment. Restore a separate starting snapshot for a new run. Do not use deliberately mutated case fragments as live state. Do not silently repair preserved snapshots to make the historical test appear cleaner.

**Final conclusion:** the findings support transcript-grounded semantic auditing as a useful protection against corrupted saves. They also show that faithful operation depends on source selection, correct interpretation, and a host that records complete accepted events without duplication. This publication documents both the demonstrated protection and the remaining failures, without changing RPG OS v0.9.5 or presenting the experiment as a certification.
