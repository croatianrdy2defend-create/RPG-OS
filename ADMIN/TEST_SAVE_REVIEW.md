# Tiered save-review acceptance cases — v0.9.6

Behavioral status: **NOT RUN** for this release. These cases require observed GM/reviewer behavior, not text-presence tests or passing Python checks. Use disposable original fixtures and independent reviewer contexts where genuinely available. Preserve an answer key outside the reviewer's supplied material; same-context authorship must be disclosed rather than labeled blind.

## Deterministic support

Run `python -B TOOLS/test_save_audit.py` with the existing suites, sequentially. It checks tier selection, selected diff/save metadata, frozen boundary binding, exact selected-file readback, stale reports, capture gaps, explicit removal versus prior-only evidence, source-conflict declarations and CLI compatibility. It supplies synthetic report judgments; it neither discovers errors in prose nor scores a model's semantic accuracy. Existing recovery, archive, session and autosave suites remain separate evidence.

## Behavioral cases

| Case | Required observation |
|---|---|
| SR01 Missing obligation | Source-first extraction detects a new promise omitted everywhere in the proposed save, not merely a wrong value in a selected changed file. |
| SR02 Legitimate change | Actual repayment, renegotiation and retirement of a temporary mood are accepted; historical values are not automatically restored. |
| SR03 Completed-action checkpoint | Departure updates location and participation before checkpoint; payment settles both money and obligation; a completed job leaves current goals. An unanswered choice remains unanswered. |
| SR04 Overlap and repeated events | One payment appearing in active chat and its export is applied once. Two distinct payments with identical wording are not collapsed. Edited-source conflicts stay explicit. |
| SR05 Checkpoint/archive boundary | Several checkpoints followed by full save archive all available accepted evidence from evidence_through without repeating already-applied effects. State, archive and review endpoints remain distinct. |
| SR06 Unknown versus wrong | Missing export, missing earlier agreement or missing private determination produces incomplete coverage, not fabricated dialogue or a clean result. Progress is preserved without a review retry loop. |
| SR07 Self-contradictory source | Conflicting prose/numerical chronology is flagged as source conflict when noticed, not silently reconciled by save copying. Measure misses separately from source/save mismatch detection. |
| SR08 Knowledge and authority | Attempts, testimony, private facts, authorized OOC corrections and superseded/rewound material retain their distinct meanings; the reviewer does not become a second GM. |
| SR09 Reviewed candidate changes | Change a candidate after review or the live parent before publication. Its prior report is not reused. Final bytes match the new reviewed candidate or the review remains incomplete. |
| SR10 Failure and repair | Interrupted publication follows actual recovery. A known corrupt candidate stays separate. A clear recording repair follows existing authority; a correction changing an already-played outcome is not silently applied. |
| SR11 Cost and pacing | Compare tiered and every-save modes with normal autosave cadence. Record actual source size, model usage/time where supplied, extra prompts, incomplete reviews and player interruption. Do not infer cost from Python helper timings. |
| SR12 Long-gap/fresh-context | Resume with only supplied saved records and retrievable evidence, without player coaching. Bring an older obligation back after unrelated play; include a source spot-check for something missing from the current open-matters list. |

Report true/false findings, missed errors, false alarms on legitimate controls, exact-source relevance, coverage and reviewer independence separately. Completed-session counts and passing hash checks are not semantic detection rates. Do not report these cases passed until actually executed.
