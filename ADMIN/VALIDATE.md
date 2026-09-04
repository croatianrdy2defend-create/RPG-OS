# ADMIN Validate Contract

ADMIN maintenance. No fiction.
Open only after an explicit **VALIDATE** request. VALIDATE inspects structure; it never repairs, rewrites, deletes, migrates, binds, checkpoints, closes, or advances the campaign.

## Preferred execution

If code execution is available, run the dependency-free validator against this `RPG_OS` root:

```text
python3 TOOLS/validate.py
```

On Windows, `py TOOLS\validate.py` is equivalent. Invoke the file that exists in this folder; do not recreate its logic from memory. Return its report and exit status without upgrading or softening any result.

The script is read-only. It emits an ephemeral point-in-time diagnostic and writes no report file. Do not put validation fields in CURRENT_SAVE or any campaign register.

Exit status:

- `0` — the complete declared v2 structural surface was scanned and no structural violation was found;
- `1` — the scan completed and found one or more structural violations;
- `2` — declared coverage is incomplete because of invocation/access failure, validator failure, a tree change during the scan, an unsupported legacy descriptor, or another declared machine-readable surface that could not be completely parsed or scanned. Never report PASS.

Warnings and metrics do not change exit status. A warning is not proof that the warned condition is safe.

## Required evidence classes

Keep these blocks separate:

```text
STRUCTURAL
Result: PASS / PASS WITH WARNINGS / FAIL / INCOMPLETE
Provenance: SCRIPT-VERIFIED / MODEL-CHECKED
Coverage: explicit scope

HOST OBSERVATION
Result: NOT RUN

SEMANTIC
Result: NOT CHECKED
```

`SCRIPT-VERIFIED` means the shipped script actually executed. The report hashes the executed validator and the target tree's validator separately; if they differ, coverage is `INCOMPLETE`. Do not use that label for an LLM checklist, an asserted command, or reconstructed output.

The tree digest identifies the scanned path/type/content snapshot for that run, including directory paths and symlink targets as well as file bytes. It is not a persistent certification and becomes historical as soon as the tree changes.

## No-code fallback

If the script cannot execute, a model may perform a read-only structural inspection only after saying that code execution is unavailable.

Label it:

```text
STRUCTURAL
Result: INCOMPLETE or FAIL
Provenance: MODEL-CHECKED
Coverage: exact files and checks actually inspected
```

A model may report a definite defect it observed. Absence of an observed defect is never a complete PASS unless the script ran successfully. Do not imply that a sample covered unopened files.

## Structural scope

The script checks only deterministic file invariants declared by its output, including required release and ADMIN-contract files (including the v0.5 migration contract), executed/target-validator identity, release-LAW bytes, CURRENT_SAVE fields, scene status, causal-frontier syntax and commit metadata, the accepted Campaign Contract's identity/binding/revision/axis/mandate shape, the Bearing's identity/required lanes/base references and stale-base observation, clean unbound/bind INSTANCE registers, canonical hot-roster placement, safe engine identity and character-build support, the bound module descriptor where machine-parseable, closed MODULE/INSTANCE PC route graphs and bind-copy bytes, safety flag consistency, archive routes, session-index budgets, stable literal headings, ledger pointers, path containment, unfinished candidate residue, initial archive contamination, and routed orphan sessions. A well-formed but stale Bearing is reported as a warning and must be omitted from PLAY; it does not invalidate the accepted save or contract. The script cannot identify every interrupted transaction after all intermediate files happen to be structurally valid.

It may report archive size and routing metrics. Metrics are evidence, not automatic split thresholds.

## Explicitly not checked

VALIDATE does not establish:

- semantic coherence or completeness of scene shards;
- whether the GM oriented before retrieving, supplied a playable frame, or closed a quiet beat well;
- whether a particular external warrant, responsive duty, or accepted creative mandate existed;
- whether contract language, Bearing interpretation, or fresh creation stayed within its semantic authority;
- whether a causal-frontier entry duplicates another authority or captures the right established cause;
- whether REVIEW inferred preference, prepared a railroad, or correctly identified a campaign pattern;
- whether `MIGRATE V0.5` preserved every source fact, used a complete backup, or received truthful operator-supplied orientation and Contract values;
- whether archived text came only from accepted PLAY;
- whether an exact id was narratively warranted;
- whether an index became a plot summary in meaning;
- agency, salience, quiet-day, consent, refusal, no-retrofit, or nonactivation compliance;
- truth, quality, or copyright status of a capability body;
- host section isolation, persistent-write behavior, moderation behavior, or model identity;
- future correctness after the reported tree digest changes.

Those remain tests, observations, or judgment. Never merge them into STRUCTURAL PASS.

The GM-quality fixtures in `ADMIN/TESTS.md`, including P40–P50, are a separate semantic/player-evaluated lane. Passing this script does not run or score them.

## Stop condition

Report the categorized result OOC and stop. Do not resume fiction. Any repair requires a separate, explicit ADMIN instruction and must preserve the existing authority and write-order rules.
