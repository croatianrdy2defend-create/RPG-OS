# RPG OS v0.9.5: longitudinal synthetic playtest and save-consistency audit

**Publication date:** 11 September 2026  
**Tested source:** `211242384046afabe2135e9fee10b11ba4c19901`  
**Engine:** bundled Freeform  
**Campaign:** *The Ninth Sluice*, followed by *Afterwater*  
**Scope:** an initial ten-session run and twenty additional sessions, reaching session 30  
**Publication type:** test documentation and evidence, not a software release

> This is an AI-authored, instrumented, non-blind synthetic playtest. It is not a human usability study, an independent-model evaluation, or proof that every RPG OS mechanism works. The experimental campaign writer is not the supplied RPG OS core. Findings attributable to that writer are identified accordingly.

## 1. Executive assessment

The campaign maintained several consequential facts through thirty condensed sessions, including conditional debt, restricted funds, NPC knowledge boundaries, unfinished paid work, disputed ownership, and a major fictional failure. The continuation advanced to Day 65, including a substantial period away from the original crisis. A later successful pump repair did not erase the earlier flood.

The central audit finding is that structural validity and faithful recording are different properties. Twenty deliberately corrupted saves passed structural validation, but source-grounded semantic reviews produced evidence-supported findings for the seeded defects. Six legitimate-change controls were not flagged for their tested changes. These reviews were non-blind: the same author knew the mutations and wrote the semantic findings. The results demonstrate workable comparisons, not a measured 100% detection rate.

Original play evidence also exposed a historical claim inherited by successive saves. The important qualification is source selection. Without the original receipt, the correct result was undetermined; with the original receipt included, the discrepancy became demonstrable. Agreement between later summaries did not authenticate their shared claim.

The process was not infallible. Two issues escaped their first-pass semantic reviews and were found in later inspection. Several errors also arose in the experimental writer, especially stale state projections, checkpoint timing, repeated session-ending publication, and feedback disposition. The known final stale goal remains part of the evidence rather than being silently removed.

The resulting assessment is cautiously favorable for supervised long campaigns with preserved original evidence, disciplined state maintenance, and recurring semantic audits. It does not establish reliable unaided chat memory or readiness for 100 sessions without further independent testing.

## 2. Evidence and publication provenance

The tested source is the immutable [v0.9.5 source commit](https://github.com/croatianrdy2defend-create/RPG-OS/tree/211242384046afabe2135e9fee10b11ba4c19901). The source package was compared with that commit during publication preparation. This document does not change `VERSION`, core rules, engines, runtime state, or release tags.

The prepared report, transcript, and evidence objects were uploaded as Git trees before this index document. Their combined snapshot is identified by tree SHA `8e4ddcfe273fc69e0d9b299c5fcd26cef023b2cb`. The [recursive GitHub evidence-tree listing](https://api.github.com/repos/croatianrdy2defend-create/RPG-OS/git/trees/8e4ddcfe273fc69e0d9b299c5fcd26cef023b2cb?recursive=1) provides paths, object types, and blob identifiers. This is an uploaded Git-object snapshot; this document does not assert that the entire snapshot has been merged into the default branch.

The underlying run materials are named `RPG_OS_Ten_Session_Audit.md`, `The_Ninth_Sluice_Play_Log.md`, `RPG_OS_Twenty_Session_Audit.md`, `Afterwater_Sessions_11_to_30.md`, `RPG_OS_Twenty_Session_Coverage.md`, and `RPG_OS_Twenty_Session_Verification.json`. Supporting evidence includes mutation-benchmark results, session-boundary probes, mechanism branches, regression summaries, and supplemental review findings. The prepared publication preserves original dialogue, first-pass findings, corrections, and known unresolved defects separately.

Evidence should be read at its actual level. A transcript records the authored play. A save records the writer's projection of that play. A semantic report records a reviewer's judgment. Hashes and quotation checks establish integrity and correspondence; they do not establish that the judgment is complete or correct.

## 3. Questions and test design

The initial run asked whether the framework could support a coherent original campaign under sustained play. The follow-up specifically tested whether validation against actual accepted play could identify corrupted saves, including omissions and mistakes inherited by later saves.

The campaign was deliberately built around interacting obligations and constraints rather than a sequence of isolated demonstrations. Mara Venn, a former lock surveyor, returned to a flood-threatened port. Family priorities, vulnerable patients, a disabled pump, missing equipment, contractor misconduct, disputed ownership, and limited resources created opportunities for both ordinary play and long-term continuity checks.

The simulated player was not perfectly cooperative. Mara made an unsupported public accusation, negotiated narrow commitments, retreated from danger, changed objectives when equipment was unavailable, and accepted an outcome in which the original repair objective failed. Those choices were authored within the same evaluation process, not independently supplied by a human participant.

The second run continued the actual session-ten campaign instead of restarting it. Recovery, procurement, repair, debt settlement, ownership issues, and a month away created later occasions to revisit old facts. Deliberately destructive mechanism tests used disposable copies or branches so that a probe did not silently alter the main campaign.

### Recorded scope

| Measure | Initial run | Continuation | Combined interpretation |
|---|---:|---:|---|
| Condensed sessions | 10 | 20 | 30 authored sessions |
| Player/GM exchanges | 100 | 160 | 260 recorded exchanges |
| Full session saves | 10 | 20 | 30 session saves |
| Mid-session checkpoints | 1 | 5 | 6 checkpoints |
| Transcript-grounded continuation audit reports | Not the same audit schedule | 20 | Do not relabel as 30 equivalent reports |
| Fictional time | First 76 hours | Through Day 65 | Includes recovery and a longer absence |

Session count must not be confused with tabletop hours. The continuation used eight recorded exchanges per session. All sessions were condensed synthetic units, not full-length human sessions.

## 4. Authority model: accepted play, not arbitrary transcript text

A save should not override accepted play merely because it is newer. An obligation established in play remains operative until a supported event or authorized correction changes it. A save that omits it is not made accurate by later saves copying the omission.

However, raw chat statements do not all have the same authority. A declared attempt is not automatically a completed action. An NPC accusation is evidence that the accusation was made, not proof of its subject. A proposal is not acceptance. Private GM information does not automatically become NPC or public knowledge. Authorized corrections can supersede earlier narration, but that authority must be preserved rather than inferred.

A useful semantic audit therefore compares in both directions. It independently identifies consequential developments in the source and checks whether the save preserves them. It also checks whether the save introduces facts without adequate support. Reviewing only assertions already present in the save is insufficient to detect facts that disappeared entirely or were never recorded.

Historical review must include relevant intervening developments. Restoring an old debt amount without checking for later repayment would itself corrupt the campaign. Continuity means preserving justified change, not freezing every historical value.

## 5. Campaign findings: what survived sustained play

### 5.1 Conditional debt and an actual trigger

The original loan separated two conditions: three crowns when the western pump ran, and five more only after survey wages cleared. It did not purchase Mara's testimony. The wages arrived in session nine and the corresponding five crowns were paid. Because the pump remained inoperable, the other three were still conditional at session ten.

During the continuation, Mara and Sera explicitly clarified that disconnected motor rotation was insufficient; actual water delivery would count. A dry diagnostic consequently did not make the remaining payment due. Outlet flow in session 23 did. Mara informed Sera and paid in session 24. The debt remained settled after Mara's month away.

This was more informative than merely retaining an unchanged number. The system had to distinguish an obligation's existence, its trigger, actual payment, the creditor's knowledge, and later historical status.

### 5.2 Restricted procurement funds versus personal money

Mara received a restricted 24-crown procurement purse, spent twenty on the completed procurement and transport, and returned four. The purse did not become personal income. Her separate personal transactions ended at twelve crowns. A nine-crown refund awarded to Nessa belonged to Nessa rather than the player character.

The initial run's separate ledger reconciled to zero: eighteen starting crowns plus twenty received, minus thirty-eight spent. These arithmetic checks are useful but narrower than a complete semantic audit. Correct totals alone would not establish correct ownership, authorization, or transaction meaning.

### 5.3 A changed agreement did not falsify an earlier result

A component passed its actual material test. Mara nevertheless declined the purchase and negotiated a new cancellation agreement. The deposit was returned under that agreement, not by rewriting the successful test as a failure.

An auditor that enforced the original refund condition while ignoring the subsequent renegotiation would produce a false positive. This case illustrates why semantic review must preserve both the original result and the legitimate later change.

### 5.4 NPC knowledge, appraisal, and cooperation

NPC cooperation remained bounded by circumstances and agreements. Distrust did not make all paid cooperation impossible, and competence did not automatically create friendship. Catching a courier created an opportunity to speak, not an obligation to obey. Mechanical authorization did not replace physical prerequisites for operating the gate or pump.

The audit also examined knowledge propagation. Sera did not remotely learn that the pump was operating; Mara actually communicated the event. Public accusations, corrections, private information, and established world facts remained distinct categories to review.

### 5.5 Failure remained part of history

At the end of the initial arc, the temporary barrier failed, the crew withdrew under its agreement, and Lower Quay flooded. The patients and evidence survived, but the western pump was not restored in time. The continuation's eventual repair did not retroactively turn that outcome into victory.

This is an important positive observation, although it remains a property of the authored run. It does not prove that all future GMs will resist convenient rescues, forced heroics, or retrospective rewrites.

## 6. Three different validation layers

### Structural validation

Structural checks verify such properties as expected files, required document structure, record links, and permitted operating states. They do not, by themselves, determine whether every consequential fact was faithfully retained from play.

All twenty seeded semantic corruptions in the continuation benchmark passed structural validation. Earlier probes similarly showed that removing a live conditional debt or a required active-state field could evade the structural checks exercised. These results are consistent with the tools' declared semantic limits; they are not proof that a structural checker malfunctioned.

### Evidence integrity and citation verification

The evidence helper actually rejected altered captured bytes and a fabricated exact quotation. These are automated integrity results. They support confidence that a report is referring to the preserved material it claims to quote.

They do not show that the selected evidence is sufficient, that the interpretation is sound, or that every omission has been found. A correctly quoted passage can still be irrelevant or incomplete for the proposition under review.

### Semantic comparison

The semantic comparison was performed by the authoring reviewer. It could identify missing obligations, invented acceptance, reversed results, duplicated money, revived paid debts, unsupported knowledge, unauthorized elapsed time, and other discrepancies when the relevant evidence was available.

This layer depends on both source selection and judgment. The two later-discovered first-pass misses demonstrate that a completed audit report is not a guarantee of exhaustive correctness.

## 7. Deliberate corruption benchmark

The continuation included twenty deliberately corrupted save copies, six valid-change controls, and two historical-source-scope cases. The mutation classes covered omissions, unsupported additions, changed conditions, stale or absent current state, false historical claims, duplicated economic effects, knowledge leakage, and unauthorized chronology changes.

| Benchmark result | Interpretation |
|---|---|
| Twenty mutated copies accepted structurally | Structural success did not establish faithful memory. |
| Twenty source-supported semantic findings | The comparisons were feasible with the supplied evidence and an informed reviewer. |
| Six tested legitimate changes not flagged | These controls demonstrated the importance of recognizing supported change. |
| Historical claim without original source: undetermined | The reviewer did not treat repeated summaries as independent authentication. |
| Historical claim with original source: inconsistent | Expanded evidence made the discrepancy demonstrable. |

**These numbers are not a detection-rate estimate.** The reviewer authored the mutations and knew what to look for. The cases were selected rather than randomly sampled. They are not independent trials of an unknown production error distribution. There was no blinded held-out evaluation, independently measured sensitivity, or generalizable false-positive rate.

### The inherited receipt discrepancy

Two later saves repeated a claim that Nessa's original trip cost six crowns per leg. When the original booking was outside the evidence selection, the reviewer could not establish whether that repeated historical claim was true. The appropriate conclusion was undetermined, not consistent by repetition and not inconsistent by intuition.

A new expanded evidence bundle included the original booking exchange. It established six crowns total for the round trip. The contradiction was then supported by the original play record.

This directly answers the central design question: preserved original play can expose a mistake inherited by successive saves. It also identifies a critical operational requirement: the audit must retrieve the source needed for the claim under review.

## 8. Defects and execution failures observed outside seeded mutations

Severity below describes the potential campaign consequence, not a statistically measured frequency. Attribution matters: the player experiences the framework, GM, and host together, but that does not make every host mistake a core-rule defect.

### F-01: conflicting NPC baseline records

In the initial run, the experimental writer copied opening NPC baseline fields into durable person records while retaining generated and updated encounter state in `NOW`. Jory consequently had potentially conflicting descriptions: fields still awaiting generation in one place and concrete active state in another.

The issue was found after session six. Faulty snapshots were preserved, the writer was corrected, and current person records were repaired. No changed fictional outcome was demonstrated in that run. The risk was nevertheless material: a later reader could choose the wrong source or regenerate state that should have persisted.

**Attribution:** experimental host writer. **Lesson:** maintain clear ownership between durable identity, current encounter state, and historical evidence.

### F-02: stale projections after accepted events

In the continuation, completed work remained labeled incomplete, accepted offers retained unaccepted labels, and a delivered document remained in inventory. Source-grounded comparisons found these disagreements and narrow corrections were recorded separately from the original saves.

**Attribution:** writer execution and incomplete state synchronization. **Lesson:** accepting an event requires updating every operative projection it legitimately changes, not merely appending a narrative note.

### F-03: checkpoint timing and synchronization

One automatic checkpoint retained Voss as an active participant after Mara left because the writer saved before processing departure. Another checkpoint preserved the correct money but an outdated situation summary saying no personal cash had been earned.

**Attribution:** experimental writer sequencing. **Lesson:** checkpoint validation must examine the fully applied event state. Auditing only session-end snapshots can miss a defective intermediate resume point.

### F-04: ambiguous chronology in the source itself

The phrase “next morning” conflicted with the recorded numerical timeline. The audit did not invent a reconciliation. An explicit simulated-operator correction selected the intended timeline.

**Attribution:** authored source ambiguity, requiring authorized resolution. **Lesson:** a canonical transcript can contain a contradiction. An auditor should identify the conflict and its consequences rather than manufacture missing authority.

### F-05: repeated session ending and archive publication

In a disposable branch, repeated raw writer calls duplicated ending receipts and archived the same exchanges again without new play. Freeform supplied no automatic numerical session XP, so this did not demonstrate duplicated XP. It did demonstrate failure of the required once-only behavior in that implementation.

**Attribution:** experimental writer lifecycle implementation. **Lesson:** use explicit session-boundary identity and an archive cursor rather than treating every close request as a new ending.

### F-06: declined feedback recorded as received

The raw writer labeled explicitly declined feedback as received.

**Attribution:** writer status mapping. **Lesson:** distinguish requested, received, declined, and unavailable feedback. A structurally acceptable label can misrepresent the interaction.

### F-07: first-pass semantic review misses

Later inspection found stale or ambiguous controller appraisal wording and a completed prepaid-hour task still listed among current PC goals. Both had escaped their first-pass reviews.

The tested final save retains the stale goal, with a proposed narrow repair documented separately. Correct payment and obligation records elsewhere do not make a misleading current goal acceptable.

**Attribution:** incomplete first-pass semantic review, together with stale writer output. **Lesson:** audit current goals and active-state wording explicitly. Passing quotation checks does not establish coverage of all consequential assertions.

### Other bounded authoring issues

An initial opening/save character-state mismatch was caught structurally before play, and optional preparation records initially lacked prescribed metadata. These were authoring or formatting errors, not demonstrated core defects. A stale preparation-base advisory was retained where provenance genuinely differed rather than being falsely refreshed merely to make the warning disappear.

## 9. Recovery, retrieval, handover, and administrative coverage

Disposable branches exercised interrupted-write recovery, exact historical retrieval, stale-source rejection, outgoing handover, return-only writing, import-once behavior, cancellation, cold campaign review, preparation revalidation, adding a distinct engine without rebinding the campaign, and adding or refining a public setting brief.

The recovery branch restored exact prior bytes and removed operation-created material. Handover preserved the unresolved choice and rejected replay. These were actual branch operations in the instrumented environment, but the handover remained within the same context. It was not an independent-model or genuinely fresh-conversation trial.

A missing original archive source was treated as missing rather than replaced with a reconstructed quotation. An indexed candidate from a changed source was rejected as stale. These are useful safeguards against presenting unavailable or outdated material as original evidence.

The publication must not turn broad coverage into “all mechanisms proved.” Authentic legacy migration, genuine fresh-context resumption, cross-model transfer, actual context-capacity telemetry, a second complete new-game bind, and some optional administrative variants remain unverified by this run. Combat and advancement balance in other engines were not established by playing the Freeform campaign.

## 10. Automated results and their limits

All nine supplied regression suites ran: **277 cases discovered, 273 passed, four skipped, zero failures**. Passing suite results do not cancel the writer failures or review misses above. Skipped cases are not passing cases.

The initial run also recorded 290 narrow assertions, many of which repeated arithmetic or time checks. They must not be represented as 290 independent gameplay scenarios. A corrected replay established reproducibility of the recorded choices, not a second independent playtest.

Publication preparation recorded verification of the archive manifest and exact source-tree correspondence. Those integrity checks help readers identify the artifacts examined. They do not create an independent semantic reviewer or validate human enjoyment.

## 11. What this means for session 100

The results support the plausibility of long-lived campaigns whose current state is compact and whose original evidence remains retrievable. The strongest positive example is not a value that stayed unchanged; it is an old obligation whose condition was later clarified, fulfilled, communicated, paid, and kept settled.

The leading long-horizon risk is quiet continuity drift: an operative fact disappears or becomes misleading, later saves inherit that state, and subsequent play treats the omission as settled history. Transcript-grounded auditing directly addresses that failure mechanism, provided the relevant source is selected and interpreted correctly.

There is no defensible per-session failure probability from this authored path. Thirty condensed sessions cannot establish a 100-session survival rate. Reaching session 100 while requiring frequent manual rescue would also be different from dependable routine operation. Future evaluation should measure correction burden, consequence severity, and detection before errors affect play, not merely completed session count.

## 12. Recommendations arising from the evidence

These recommendations are findings, not changes applied by this publication.

1. **Complete accepted-event state before autosave.** Update active participants, inventory, money, obligations, and operative summaries before publishing a resume point. Preserve failed intermediate states as regression fixtures.
2. **Make session closure and archive publication idempotent.** Track the identity of an ending and the last archived exchange. Repeating a request without new play must not create another ending receipt or duplicate archive material.
3. **Run semantic review in both directions.** Derive consequential source developments independently, check their preservation, and check save assertions for unsupported additions. Include current goals and active-state wording.
4. **Make historical source selection explicit.** Identify claims that require earlier evidence. Expand the evidence bundle or return undetermined; do not authenticate a claim because several summaries repeat it.
5. **Preserve legitimate change and correction authority.** Distinguish settlement from deletion, renegotiation from falsified history, and source ambiguity from a writer defect. Repair consequential downstream effects explicitly rather than silently rewriting resolved play.
6. **Test independently next.** Use held-out corruptions, valid-change controls, genuine fresh-context resumption, and an independently acting reviewer. Record misses, false positives, repair burden, and the amount of evidence required.

## 13. Reproduction and review guidance

Review original dialogue alongside both the prior and resulting save. Keep seeded mutations separate from organically occurring defects and keep repairs separate from the original failure. Read the coverage matrix before interpreting a successful mechanism branch as an end-to-end capability claim.

For the uploaded Git-object snapshot, retrieve the recursive tree listing linked in Section 2. GitHub's blob endpoint for each returned blob SHA provides its content. Preserve paths and verify blob or manifest hashes before reviewing the materials. Do not replace the live campaign or runtime files with an experimental save merely to inspect the evidence.

Re-running integrity or regression scripts can establish whether the same stored artifacts and mechanical checks reproduce. It cannot reproduce an independent judgment merely by replaying an already-authored semantic report. A new semantic evaluation needs a reviewer who actually reads the evidence, with blinding where detection reliability is being measured.

## 14. Final conclusion

RPG OS provided a workable foundation for this supervised synthetic campaign. The original play record was useful as an authority outside the save and exposed semantic corruption that structural validation accepted. Historical evidence could also correct a claim repeated by successive summaries.

The execution remained fallible. The experimental writer produced stale and duplicated state, and semantic review missed two issues on its first pass. The appropriate conclusion is therefore neither “everything passed” nor “the architecture cannot support long campaigns.” It is that evidence-grounded persistence is promising and demonstrably useful, while reliable source selection, event synchronization, lifecycle handling, and independent review remain important validation targets.

**This publication reports the test and its findings. RPG OS remains version 0.9.5; no core fixes, version bump, or software release are included.**
