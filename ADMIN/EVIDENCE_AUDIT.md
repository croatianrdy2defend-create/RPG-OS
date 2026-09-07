# Evidence capture and campaign consistency audit — v9.0.0

Cold maintenance procedure for a requested source capture, consistency check or selected audit-on-save option. Ordinary `AUDIT` of tool activity remains an observed-actions report; a request to compare campaign state against evidence selects this procedure. Do not begin fiction, resolve an open outcome, or change current records while auditing.

The Python helper imports actual supplied source, freezes explicitly selected inputs, and checks package/report identity and citations. A capable model or human performs the semantic comparison. No helper silently calls another provider, generates semantic findings, or grants itself repair authority. A fresh reviewer context is preferable when available; report the actual reviewer arrangement and limits when it is not.

## Capture the available original

Use a real host export or operator-supplied text/JSONL file. Do not reconstruct a conversation from summaries, memory or a model's internal reasoning. A generic manual import is supported; platform-specific automatic export is not implied. Preserve displayed OOC material and available played-then-rewound scenes. Unavailable discarded generations need not block an otherwise useful capture.

```text
python -B TOOLS/evidence.py import --input C:/RPG_SUPPORT/session-export.txt --output EVIDENCE/captures/session-001 --format raw
python -B TOOLS/evidence.py check EVIDENCE/captures/session-001
```

Choose an absent output package and actual input. The import command preserves original bytes and records their hash. Optional metadata identifies declared campaign/save boundary, message IDs, exporter and gaps; inspect `--help` and the package manifest for the supported fields. A verified imported file does not prove that the application exported every message. JSONL validation checks the supplied message representation, not its fidelity to inaccessible host history. A `pending` package can record absent source without creating fake dialogue.

Retain relevant attachments/source versions and actual recorded private GM determinations when they affect a review. A public conversation alone cannot establish an unrecorded motive or when the GM first privately determined it. Report those gaps. Capture receipt is not fictional receipt, knowledge disclosure, ARCHIVE publication or a completed SAVE.

## Select matching boundaries and freeze inputs

Identify the campaign, prior save, current/proposed save and exact session boundary. A checkpoint can include state beyond ARCHIVE's evidence_through. A raw export can include later unsaved play. Compare only the selected boundary, retaining later play for its proper save rather than replaying it into the selected one.

Use stable copies of the relevant prior and current authorities and the actual capture. Include applicable agreement/corrections, governing rules, source lore and recorded private state. Read relevant primary historical evidence when a claim needs it; an index entry only locates it. Do not rely solely on the list of changed files: a wholly omitted appointment would be absent from that list.

`TOOLS/evidence.py prepare-audit` creates a no-overwrite bundle outside all input roots. Select source paths explicitly using the CLI or selection manifests. Include current-only new records and prior-only removed records using the respective selection options. There is no implicit all-campaign selection. Keep omitted scope and inaccessible material explicit. An output copy protects observed input bytes; it does not certify prior history or end-to-end semantic completeness.

```text
python -B TOOLS/evidence.py prepare-audit --prior C:/RPG_SUPPORT/prior-save --current . --capture EVIDENCE/captures/session-001 --output C:/RPG_SUPPORT/audit-session-001 --select INSTANCE/CURRENT_SAVE.md --select INSTANCE/CAMPAIGN_CONTRACT.md
python -B TOOLS/evidence.py report-template --bundle C:/RPG_SUPPORT/audit-session-001
```

The example selects only two records and cannot support a whole-campaign conclusion. Add the actual person/resource/system records, correction authorities and source bodies needed for the session. If a fact requires an unselected source, extend the selection into a new bundle or report the gap; do not guess from a route name. Template output is pending work, not a performed review. Keep the audit's source-delivery receipts and authored report outside frozen inputs.

## Perform the independent comparison

1. Read the selected agreement and authorities. Independently identify consequential accepted developments from the session before checking proposed destinations. Include promises, obligations, custody/transfers, damage, resources, appointments, disclosed information, unresolved conditions and their qualifications. A small fact need not be a dramatic event to matter.
2. Distinguish fictional evidence, authorized OOC directives/corrections, and provisional or superseded material. Record instruction, GM acknowledgment and application separately where relevant. An authorized user correction does not require GM acknowledgment; ignored application is a finding. A genuinely ambiguous suggestion remains uncertain. Valid-outcome rewinds follow the actual accepted Retcon clause.
3. Compare starting authorities/prior state with new play for unexplained contradictions or undelegated PC actions. Compare prior state plus accepted developments against resulting records in both directions: lost consequential facts and unsupported additions. A legitimate development may replace an old value. Mere repetition does not validate an inherited error.
4. Keep world truth, testimony, actual audience, belief, uncertainty and private state distinct. Correcting world truth does not tell an NPC. Do not infer a lie from false testimony without evidence of the speaker's knowledge. Do not infer a message promise from accepting contact details.
5. Check relevant retirements. A fulfilled obligation can leave Open matters while its history, continuing relationships and relevant person state remain in their existing owners. Removing an active cue must not erase the only surviving schedule, identity or pending consequence. Current files do not need a copy of every historical utterance.
6. For each conclusion, cite the actual inspected source revision and original lines. Cite the agreement or directive establishing authority when a correction/rewind or repair depends on it. A correct verdict supported by the wrong passage is a defective finding. Provide a short evidence-backed explanation of material classifications, not private model reasoning.

Report record consistency, unresolved matters, source coverage and repair eligibility separately. A record may correctly preserve an unresolved question. Do not reduce those dimensions to one unexplained PASS/clean badge. State exactly which sources were merely located, actually delivered, and semantically reviewed. A delivery receipt proves supplied bytes, not understanding. Missing evidence requires incomplete coverage even when no contradiction was found in the inspected scope.

Use `check-report` after authoring the report:

```text
python -B TOOLS/evidence.py check-report --bundle C:/RPG_SUPPORT/audit-session-001 --report C:/RPG_SUPPORT/audit-session-001.report.json
```

This validates supported report structure, frozen-source hashes and citation text/line identity. Its mechanical success is not endorsement of the model's interpretation, authority classification, or completeness. Inspect the meaning of cited passages as a separate reviewer duty.

## Complete the report template

Keep the generated identity, bundle/capture references and evidence-boundary fields unchanged. Write the completed JSON report outside the bundle. The supported review fields are:

| Field | Values and meaning |
|---|---|
| `review_status` | `pending` until the selected review is performed; then `completed`. Completion does not mean consistency or full campaign coverage. |
| `reviewer` | `kind`: `model` or `human` for completed work; actual `identifier`; `independence`: `unknown`, `same_context` or `claimed_independent`. A declaration is not externally authenticated. |
| `source_coverage` | Preserve `indexed_sources`. Put actually reviewed reference objects in `reviewed_sources`; status `unobserved`, `partial` or `scoped`. Keep explicit `limitations`; scoped means the selected inputs only. |
| `record_consistency` | Status `not_reviewed`, `consistent`, `inconsistent` or `undetermined`, plus a short `summary` and exact `citations`. Consistent selected records require declared review of every selected input. |
| `unresolved_facts`, `unresolved_instructions` | Separate arrays of objects containing `summary` and `citations`. Optional `basis` is `source_text` (default), `caller_declared_gap`, `outside_selected_scope` or `pending_capture`; the latter three can have empty citations when that limit actually applies. |
| `findings` | Each has unique `id`, `category` (`record_consistency`, `unresolved_fact`, `unresolved_instruction`), `summary`, `decision` (`observation`, `correction`, `rewind`), `citations` and `authority_citations`. Correction/rewind requires cited authority and a repair assessment. |
| `repair_eligibility` | `status`: `not_requested`, `ineligible` or `eligible`; boolean `evidentiary_clarity` and `consequence_containment`; `summary` and `authority_citations`. Eligible requires both gates and cited authority, and still grants no write permission. |

A citation object contains `source` (`prior`, `current` or `capture`), original `path` and `sha256` from the template references, inclusive integer `start_line` and `end_line`, and `quote`. Copy complete original lines, including their line endings. For example, a one-line source containing `Cash: 40` followed by LF has `"quote": "Cash: 40\n"`; CRLF must remain `\r\n`. That is a formatting example, not campaign evidence. Obtain the actual hash, path and wording through the reader; never fill them from this example.

To retain tool-generated delivery evidence, read a frozen source using `--root C:/RPG_SUPPORT/audit-session-001 --path sources/current/INSTANCE/CURRENT_SAVE.md --receipt C:/RPG_SUPPORT/audit-session-001.delivery.jsonl` with `TOOLS/read_source.py read`. Pass that external receipt to `check-report` with `--delivery-receipt`. The checker distinguishes references listed, passages delivered and review declared; it cannot verify model comprehension. A citation can establish exact text without proving that the entire source was delivered.

## Repair and reviewed baselines

| Correct replacement is unambiguous | Applying it leaves played consequences intact | Treatment |
|---|---|---|
| Yes | Yes | Eligible for the existing authorized narrow correction procedure; the report itself grants no permission. |
| Yes | No | Report the known correction and affected outcome for the applicable player decision. |
| No | Yes | Preserve the uncertainty; no supported replacement yet. |
| No | No | Preserve the conflict and consequences for clarification; no automatic repair. |

Inspection and report creation do not authorize campaign edits. A request or retained standing grant can authorize narrow supported recording repairs through `ADMIN/CORRECT.md` and `ADMIN/RECOVERY.md`. Both gates matter: the replacement is unambiguous AND applying it does not change a played consequence. Numeric form alone is not sufficient. If the correct HP value would invalidate a resolved escape, report the conflict for a decision; do not silently reverse the escape or invent a revival. Uncertain replacement values remain unmodified.

Retain original evidence and write a traceable superseding correction. Do not replay already applied transitions, make compensating fictional transactions, or replace a whole save with an inferred reconstruction. Apply only the approved/supported scope and preserve all other unsaved accepted developments when publishing a corrected save.

A reviewed baseline references a specific report, exact source revisions, time boundary and coverage. It is a fallible cached assessment, not new campaign truth. Reuse it for unchanged relevant facts; reopen affected conclusions when evidence, corrections, authority or scope changes. Periodically selected spot-checks can investigate a settled fact without a preexisting contradiction. Record what was actually sampled; never report all baselines reviewed from one sample. An index-only review cannot substitute for inspecting the primary body. There is no automatic truth-by-age or repetition rule.

## Optional audit on full save

An explicit request such as “audit this save” authorizes this review once. To run it after each full save, retain that standing choice and any narrow repair grant in the existing agreement through the appropriate acceptance/recalibration procedure. Installation alone adds neither. Keep checkpoint semantics unchanged unless separately requested.

At an opted-in full save, preserve the prior authorities needed for comparison before replacement. Complete the protected save under CLOSE_CONTRACT, retain its actual available source and snapshots, then run a bounded audit of that save. A host that can safely assemble a complete candidate may review before publication, but cannot claim that a changing mixed working tree is a frozen candidate. Report save success separately from audit status. Missing capture, unavailable reviewer or uncertain evidence yields incomplete audit coverage rather than a fabricated PASS or an indefinite loss of the otherwise authorized save. A defect requiring repair follows CORRECT; unresolved scope is reported honestly.

The audit is selective maintenance, not an additional per-scene dossier, plot director or compulsory full-archive read. Preserve the normal small startup packet and continue to test actual play quality with `ADMIN/PLAYTEST_V08.md`.

Examples use a separate existing `C:/RPG_SUPPORT` directory. Substitute actual absolute paths for external inputs and outputs (or ordinary relative paths without `..`). Parent traversal is rejected; output locations must be outside the protected input roots.
