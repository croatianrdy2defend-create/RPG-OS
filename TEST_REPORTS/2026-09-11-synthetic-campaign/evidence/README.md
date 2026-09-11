# Published evidence index

This is a curated selection, not a mirror of every frozen bundle or save snapshot. Original archive-relative paths inside copied JSON are preserved as provenance. They are not automatically paths in this GitHub directory.

| File | Provenance and scope |
|---|---|
| [verification.json](verification.json) | Exact copy of the original twenty-session read-only verification output. Integrity/arithmetic/citation checks, not semantic certification. |
| [baseline-verification.json](baseline-verification.json) | Exact original first-phase structured verification. |
| [baseline-fault-probes.json](baseline-fault-probes.json) | Exact results for the five first-phase disposable fault probes. |
| [baseline-host-01.json](baseline-host-01.json) | Exact first-phase duplicate-baseline finding, attributed to the experimental host. |
| [regressions.json](regressions.json) | Exact continuation per-suite result records, including skips. |
| [mechanism-branches.json](mechanism-branches.json) | Exact disposable recovery, retrieval, handover, review/preparation, adapter, and brief results. |
| [session-boundary-probe.json](session-boundary-probe.json) | Exact raw experimental-writer lifecycle failures; not shipped-core behavior. |
| [review-misses.json](review-misses.json) | Exact supplemental findings: two primary-review misses and a separate intermediate checkpoint issue. |
| [primary-audit-statuses.json](primary-audit-statuses.json) | Derived index of all twenty original first-pass semantic reports; original report hashes identify the full archive records. Not a new semantic review. |
| [semantic-cases.json](semantic-cases.json) | Derived dossier retaining original summaries and exact citations for twenty non-blind mutations, six valid controls, and two scope probes, plus integrity-probe results and fixture failures. |
| [publication-verification.json](publication-verification.json) | Newly recorded publication-time source-tree comparison, full-archive hash verification, original archive identities, and publication scope. |

The semantic dossier includes deliberately corrupted state fragments. They are not accepted campaign canon. Its quotation excerpts identify full original sources by SHA-256 and line range; they do not reproduce every source file. A fragment alone cannot establish a whole-file omission or substitute for the original frozen bundle. The [published verifier](../verify_published.py) explicitly distinguishes transcript quotations it can recheck from state-source citations requiring the separate full archive.

The thirty original synthetic dialogue bodies are in the [transcript index](../transcripts/README.md). Protocol owners remain the unchanged [evidence-audit procedure](../../../ADMIN/EVIDENCE_AUDIT.md) and [raw-source contract](../../../EVIDENCE/README.md). A source-delivery receipt or exact quotation is not a guarantee of relevant interpretation or complete source selection.
