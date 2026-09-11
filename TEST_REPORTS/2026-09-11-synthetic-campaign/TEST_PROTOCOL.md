# Test protocol and reproduction guide

This describes the experiment that produced the published records. It is not a claim that the publication itself runs a new twenty-session campaign. Read the [report](REPORT.md) for interpretation and the [coverage matrix](COVERAGE.md) for boundaries.

## 1. Inputs and authority

The starting software was the uploaded RPG OS v0.9.5 source, byte-tree-identical to commit `211242384046afabe2135e9fee10b11ba4c19901`. The continuation started from the actual session-ten save of *The Ninth Sluice*, not a reconstructed synopsis. SHA-256 identities of the original software and two experiment archives are in [publication verification](evidence/publication-verification.json).

The accepted engine was the bundled Freeform adapter. Its absence of automatic numerical XP, class levels, and compulsory combat statistics was respected. The framework, engine, generated campaign, experimental writer, and semantic reviewer are separate attribution layers.

The generated dialogue was the original synthetic play evidence for this experiment. It was not a real-user chat-platform export. Accepted outcomes and authorized directives must be distinguished from attempts, questions, testimony, private determinations, and superseded wording. The authoritative audit instructions are [ADMIN/EVIDENCE_AUDIT.md](../../ADMIN/EVIDENCE_AUDIT.md), with [raw-source provenance](../../EVIDENCE/README.md) and [contribution evidence requirements](../../CONTRIBUTING.md).

## 2. Continuing campaign procedure

1. Preserve the original source package, session-ten campaign, original archives, and prior save snapshots. Keep destructive fixtures outside the accepted campaign.
2. Resume the preserved state and check the relevant startup markers, agreement, selected engine, current situation, unfinished decisions, and needed source records.
3. Author a continuing player path with coherent goals and imperfect choices. For this run, the same assistant supplied the player, GM, and later semantic judgments. Do not call the roles independent.
4. Emit each generated player/GM pair before serializing the corresponding state. Record actual elapsed time, money changes, custody, obligations, participation, and unresolved choices. Declare random stakes and mappings before using recorded seeded draws.
5. Apply the selected autosave policy with notice, delay/resume, and explicit disable behavior. Distinguish a complete-present checkpoint from archive publication and session ending. Checkpoints must not add ending receipts.
6. End each condensed session explicitly, persist one full session save, retain prior/current state and generated source, and freeze the selected audit evidence. Twenty additional sessions contained eight pairs each.
7. Review the source for consequential developments before comparing destination fields. Check omissions, unsupported additions, authority, and legitimate supersession. Preserve scope gaps and contradictions as unresolved rather than inventing an answer.
8. Record findings and authorized narrow repairs separately. Do not rewrite source to make a prior save look correct. Review reports were completed between five-session segments, not by an independent reviewer before every subsequent turn.

Actual shortcomings are part of the result: intermediate checkpoints sometimes captured incomplete updates, stale fields survived until batch review, and two selected-field problems escaped their first-pass reviews.

## 3. Deliberate semantic cases

The mutation experiment used twenty isolated corrupted save copies, six legitimate-change controls, and two source-scope probes. The [dossier](evidence/semantic-cases.json) retains the original authored assessment, summary, citation identities, and quoted passages for each case.

For each mutation, start from the specified legitimate boundary in a disposable copy; change the selected semantic fact while preserving runnable package structure; run structural validation; freeze the original synthetic source and selected prior/current evidence; author the semantic judgment; and use the evidence helper to check report structure, source hashes, and exact citations.

The first fixture roots were incomplete scoped selections and failed required-file checks. Full unchanged runtime dependencies were then supplied, and final structural results were recorded. Those setup failures are not semantic detections. Likewise, a tamper rejection is not a semantic detector discovering a campaign error.

The author knew the expected mutation. These are non-blind contrast demonstrations, not a held-out benchmark. Do not compute a sensitivity, specificity, precision, or accuracy percentage from twenty deliberately authored findings.

### Valid controls

C01–C06 preserve, respectively, a conditional deposit, a passed assay followed by negotiated cancellation, actual debt payment, supported healing, a settled obligation's retirement, and a departed active controller's retirement. Their purpose is to prevent the mistaken rule that any change or deletion is corruption.

### Historical scope controls

S01 supplies two late saves repeating a false historical fare quotation but omits the original booking. The selected evidence is insufficient, so the authored result is undetermined. S02 creates a new bundle with the original session-nine booking, supporting inconsistency. The auditor must not silently use outside context to fill S01's declared gap or treat agreement between saves as independent evidence.

### Integrity probes

B01 modifies captured bytes; B02 fabricates exact report text. The shipped helper rejects those integrity violations. Exact quotation and relevant interpretation are different dimensions: a correct quote can still be insufficient or misapplied.

## 4. Disposable operating-mechanism branches

Run recovery, handover, source-index, adapter, setting-brief, review/preparation, and repeated-boundary probes in separate copies. Preserve exact preimages and operation-owned material. Do not merge intentional damage into the accepted campaign.

The [branch results](evidence/mechanism-branches.json) cover interrupted protected writes, stale-source rejection, same-context handover/import-once, cancellation, cold review, actual preparation revalidation, adapter identity, and public-brief operations. The [raw lifecycle probe](evidence/session-boundary-probe.json) exposes duplicate ending receipts, duplicated archive evidence, and declined-feedback metadata in the experimental writer. It is not evidence that RPG OS's shipped rules instruct those behaviors.

These branches are file-protocol observations under the same supervising assistant. They do not establish fresh-context transfer, autonomous recovery, operating-system transaction guarantees, or a full campaign on the new adapter.

## 5. Recheck this GitHub publication

From this report directory, run:

```sh
python -B verify_published.py
```

The script is standard-library-only and read-only. It checks the published-file manifest, thirty session bodies and their pair counts, the recorded audit and case totals, regression arithmetic, and exact citations when the full cited source is one of the published transcripts. It reports citations whose complete source is not included instead of pretending to verify them from a fragment.

These are checks of the published record. The script neither plays a campaign nor detects new semantic errors. A successful result must not erase the documented stale final goal or first-pass review misses.

## 6. Recheck the original full continuation archive

The separately supplied file is `RPG_OS_Twenty_Additional_Sessions_Playtest.zip`, SHA-256 `239f31c6073d9a00d98681a2ec9a1f5a1ddf4bedeb4d6bc5d19e6dd4744f70cb`. It is not mirrored in this repository. After obtaining that exact file, extract it into a fresh directory and run:

```sh
cd rpg-os-twenty-additional-sessions
python -B verify_deliverable.py
```

That original verifier checks immutable-core hashes, captured-source identity, selected report citations, recorded money/time arithmetic, checkpoint/ending counts, original archive bodies, and RNG reproduction. It does not perform a new semantic judgment. Its output was rerun and matched the supplied result before publication.

Original delivery receipts are bound to their original absolute bundle paths. Relocation does not make that identity check silently valid. The verifier preserves those receipts and creates temporary fresh byte-delivery receipts for the same frozen sources where needed. This establishes relocated byte delivery, not independent review.

The full archive contains original writer and fixture scripts, snapshots, and frozen bundles. They are experiment infrastructure, not shipped RPG OS features or a safe one-command replay into the final campaign. Never run destructive or authoring scripts over the preserved final save; restore a separate starting snapshot and inspect the scripts' overwrite guards and path assumptions first.

## 7. Recheck bundled regression suites

From a checkout of the tested source commit, run sequentially:

```sh
python -B TOOLS/test_validate.py
python -B TOOLS/test_handover.py
python -B TOOLS/test_package_release.py
python -B TOOLS/test_read_source.py
python -B TOOLS/test_search_index.py
python -B TOOLS/test_evidence.py
python -B TOOLS/test_agent_state.py
python -B TOOLS/test_autosave.py
python -B TOOLS/test_encounter_generation.py
```

The archived run discovered 277 cases, passed 273, and skipped four. Platform-dependent skip behavior can differ on another system. Passing instruction/schema/helper tests is not proof of observed model behavior; keep those evidence classes separate. Do not modify `VERSION` or publish a software release as part of reproducing this report.

## 8. Stronger next experiment

A stronger follow-up would use a fresh reviewer context, hide mutation labels and expected answers, randomize legitimate controls, and measure source retrieval, citation relevance, semantic decisions, repair correctness, and repair burden independently. Long-gap obligations should return after unrelated arcs. Human usability, full-length sessions, and other engines require their own tests.

That work is proposed, not claimed in the published results. Thirty condensed sessions and checked report citations are not a substitute for it.
