# Evidence capture and campaign consistency audit — v0.9.7

Cold maintenance procedure for a requested source capture, consistency check or selected audit-on-save option. Ordinary `AUDIT` of tool activity remains an observed-actions report; a request to compare campaign state against evidence selects this procedure. Do not begin fiction, resolve an open outcome, or change current records while auditing.

The Python helper imports actual supplied source, freezes explicitly selected inputs, and checks package/report identity and citations. A capable model or human performs the semantic comparison. No helper silently calls another provider, generates semantic findings, or grants itself repair authority. A fresh reviewer context is preferable when available; report the actual reviewer arrangement and limits when it is not. Uniform routing is not a cure for review-quality failures: the same model can repeat the same blind spots. Source coherence is a separate question from faithful copying; the helper detects neither automatically. A semantic reviewer may flag explicit contradictions within inspected source, but cannot silently reconcile them or guarantee all such contradictions were found.

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

Use `python -X utf8 -B TOOLS/evidence.py metadata-template` for editable capture claims. `notes` and `source_description` are strings; `gaps` is a list of strings; completeness starts `null` (unknown). Fill only actual claims and save the JSON as UTF-8 before passing it to `import --metadata`. An empty template is neither an export nor proof that no gaps exist. Avoid rebuilding a valid metadata structure from memory at every save.

Use the read-only `citation` command for exact original-line references from a verified frozen bundle:

```sh
python -X utf8 -B TOOLS/evidence.py citation --bundle C:/RPG_SUPPORT/audit-session-001 --source capture --path source.txt --start-line 1 --end-line 2
```

Select an actual indexed source/path and inclusive range. Output is the citation object expected by the report: source, path, hash, line range and exact quote. It preserves original line endings and Unicode; it rejects unavailable or altered bundle sources, invalid ranges and capture lines beyond a bound save's endpoint. It does not select relevant evidence, write a report, certify reading/comprehension or perform semantic review. CLI JSON uses ASCII escapes so legacy Windows stdout also preserves the values; input/capture bytes remain UTF-8 and unmodified. Parse/save JSON with explicit encoding instead of silently normalizing source text.

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

## Shared policy and bounded cost

CLOSE_CONTRACT owns the common save route. An explicit request selects review once; retain a standing choice prospectively through the existing agreement/recalibration procedure. `tiered` is the recommended opt-in: lightweight checkpoints and bounded source-first review on full saves/session ends/accepted returns. `every-save` explicitly adds that review to checkpoints. `off`/absence disables only the additional formal review; ordinary faithful compilation and write checks remain. Legacy full-save grants retain their original scope. Capture, review and repair permission remain distinct. No mandatory new agreement clause, automatic enablement or new campaign truth store is introduced.

Lightweight checking does not prepare a capture/bundle or ask a model to independently extract the transcript. It checks the completed action and affected records with available working evidence, plus selected diff/metadata/readback. Its record says no transcript-grounded review performed. Source review uses the existing source-first steps above; widening the routes does not improve the reviewer's judgment by itself.

Prioritize source-grounded comparison of changed identity, attribution, chronology, location/possession, knowledge, assent and once-only effects. Inspect apparently unrelated rewrites for accidental drift. Keep the source-first extraction of consequential developments independent of the proposed edit list so a wholly omitted change can still be found. Reuse sufficient verified source and existing captures; neither a larger bundle nor repeated same-context review is a substitute for this comparison. Record actual omissions or limits in the existing report, without an extra universal checklist.

Bound source reviews to the selected save, relevant earlier evidence and actual available context. Do not repeatedly reread the entire campaign. Reuse exact captures/prior reviewed facts with their limits; expand to original evidence when a claim depends on it. At accepted periodic full-save/end-session maintenance, sample some older evidence including obligations no longer visible in current open-matters lists. This is a selected spot-check, not a claim to review all history. Host/token/time budgets and actual pacing need measurement in independent live play. When budget, source or reviewer is unavailable, record incomplete/deferred scope and preserve progress rather than pretending the review ran, looping retries or forcing more play.

Active chat and exported transcript can overlap. Use actual source identity, message/revision identifiers or exact capture spans to reconcile that overlap. Same wording is not a unique event identifier. An edited conflict needs source/authority inspection; never choose the convenient copy or apply the shared event twice. A host must supply actual accessible text: the player's visible window is not proof of model access. Include recorded private facts under their access rules, but never reconstruct missing private determinations.

## Save-bound helper workflow

All existing capture/report commands remain compatible. The new commands add selected save identity, separate boundaries and readback checks; none executes a semantic review, calls a provider, writes the campaign, or grants repair permission.

```text
python -B TOOLS/evidence.py save-review-plan --policy tiered --kind checkpoint
python -B TOOLS/evidence.py save-diff --prior C:/RPG_SUPPORT/prior --current C:/RPG_SUPPORT/candidate --select INSTANCE/CHAR/PC.md --select INSTANCE/NOW.md
```

`save-diff` performs no capture or writes. It reads CURRENT_SAVE automatically plus explicitly selected Markdown, reports additions/changes/removals and checks campaign/parent/revision/commit/evidence metadata. It is not the whole structural validator, does not inspect chat, and cannot prove action completion or selection completeness. Use complete stable roots, not a mixed in-progress tree.

For a source review, import the real available source with `import`, or use `pending` for a genuinely missing capture. Create a caller-authored boundary JSON outside the input roots. Example shape (replace all illustrative values using actual source reads):

```json
{
  "schema": "rpg-save-review-boundary-v1",
  "state_saved_through": {
    "basis": "capture_lines",
    "capture_sha256": "<actual SHA256 from the verified capture>",
    "start_line": 1,
    "end_line": 8,
    "description": "Accepted source since the chosen prior boundary through this exact stopping point; any overlap already applied to state is identified in review."
  },
  "write_paths": ["INSTANCE/CURRENT_SAVE.md", "INSTANCE/CHAR/PC.md"],
  "removed_paths": [],
  "limitations": ["Only the explicitly selected sources are in scope."]
}
```

For inaccessible source, use `{"basis":"unavailable","description":"Actual missing source and stopping-point limitation"}` rather than fake lines/hashes. The line-span endpoint binds the selected save; it does not prove that all host messages were exported, that all listed play is accepted, or that the selected stop is the true last accepted action. That still needs review. Older relevant lines may support history; later unsaved lines cannot support a finding about this save. Record source-scope gaps separately from factual uncertainty.

`write_paths` lists every affected Markdown file, including the current pointer and new archive files for a full save. Freeze each written file as a current selection. Select actual prior versions where they exist, and prior-only removed records separately. `removed_paths` explicitly distinguishes real deletions from a prior-only evidence selection; absence from a selection alone is not a deletion. Include governing agreement, corrections and relevant historical/private sources even when unchanged. The helper cannot infer an omitted write or omitted source from the caller's list.

```text
python -B TOOLS/evidence.py prepare-save-audit --prior C:/RPG_SUPPORT/prior --current C:/RPG_SUPPORT/candidate --capture EVIDENCE/captures/session-001 --boundary C:/RPG_SUPPORT/boundary.json --output C:/RPG_SUPPORT/save-review-001 --select INSTANCE/CHAR/PC.md --select INSTANCE/CAMPAIGN_CONTRACT.md
python -B TOOLS/evidence.py report-template --bundle C:/RPG_SUPPORT/save-review-001
python -B TOOLS/evidence.py check-save-audit --bundle C:/RPG_SUPPORT/save-review-001 --report C:/RPG_SUPPORT/save-review-001.report.json --saved .
```

The preparation command automatically selects prior/current CURRENT_SAVE, verifies their campaign/parent/revision relationship, binds `state_saved_through`, derives **history archived through** from actual archive_ref/evidence_through and freezes the explicit write/removal scope. CHECKPOINT must preserve both archive fields; CLOSE must use its new save_id and archive folder. Existing prepare-audit bundles without save binding remain valid for general audits.

A save-bound report adds `save_review`: preserve `binding_sha256`; leave `review_covered_through` null until the selected span and all selected inputs were actually reviewed, then copy the exact `state_saved_through` object. With missing capture, a pending report or only partial review, retain null. This is a reviewer declaration, not proof of comprehension. `source_coherence` has `status` (`not_assessed`, `no_conflict_observed`, `conflict_observed`, `undetermined`), `summary` and exact `citations`. Explicit conflict requires cited source, remains unresolved under the existing correction rules, and cannot be reported as a consistent-save result. No conflict observed is not proof of coherent source. A source-versus-source chronology contradiction is not repaired by making the save match one side.

Complete the ordinary report fields and source-first comparison as above. `check-report` also binds the new fields and refuses capture citations after the selected stopping point. `check-save-audit` additionally compares every selected current file with the actual saved/proposed bytes and verifies explicit removals. A changed file, different save identity or changed review binding invalidates reuse of the earlier review. The output separates selected-byte matching, declared record consistency, source coherence, coverage/gaps and all three boundaries. Exit 0 means those mechanical checks completed, even when a completed report declares inconsistency; exit 2 means review pending; exit 1 means invalid input or mismatched bytes/references. A generated report-template still exits 0 and is not a performed review.

Report/receipt outputs stay outside the frozen candidate and bundle; no self-referential hash or after-review success stamp is written into reviewed files. Optional CURRENT_SAVE Save review prose can point to an intended external receipt without claiming its existence or result. A fresh context must read the actual receipt before treating it as evidence of review. Missing legacy fields mean unrecorded coverage, never a fabricated baseline.

## Publication, failures and review quality

Where a host can assemble a stable complete candidate, review before publication and read back afterward under CLOSE_CONTRACT/RECOVERY. Recheck the live prior identity/preimages before publishing. Otherwise preserve prior authorities and perform a bounded post-save audit; disclose that ordering. Never label an in-progress mixed tree frozen or reuse an old approval for a revised candidate. A known corrupt candidate does not replace the usable save: preserve new progress separately while resolving the discrepancy. An otherwise valid save can complete with missing evidence/unavailable reviewer, explicitly unverified. Post-publication recording repairs require existing CORRECT authority; a source disagreement or already-played consequence is not a copying fix.

Source-first review, two-way omission checking, testimony/truth distinctions and repair gates predate v0.9.6. This release connects them to the selected save routes and binds their evidence; it does not establish a semantic detection rate. Test them with hidden fault keys and legitimate-change controls in a genuinely separate reviewer context when available. Record misses and false positives, correct-source relevance, source gaps, actual cost and player interruption separately from hash/quote checks. The new deterministic regression suite does not call a model or demonstrate human enjoyment or session-100 reliability.

Examples use a separate existing `C:/RPG_SUPPORT` directory. Substitute actual absolute paths for external inputs and outputs (or ordinary relative paths without `..`). Parent traversal is rejected; output locations must be outside the protected input roots.
