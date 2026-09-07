# VALIDATE — v0.8.0 experimental structural inspection

VALIDATE is read-only ADMIN work. It inspects an explicitly selected RPG_OS tree, reports what it observed, and stops. It does not repair, save, recover, accept an agreement, or start PLAY. Normal PLAY does not preload this file or the validator.

## Run

When Python is available, run the validator supplied with the target kit:

```text
python -B TOOLS/validate.py --root .
python -B TOOLS/validate.py --root . --json
```

`VALIDATE-v3.1.0` writes no report or repair. JSON and readable results go to standard output. If an operator wants a saved report, save it outside the tree being measured after the run; creating a report inside that tree during validation changes the measurement.

Scene handovers have an optional separate integrity checker: `python -B TOOLS/handover.py check --root . --package HANDOVER/<id>`; add `--return` when checking SCENE_RETURN.md. `python -B TOOLS/handover.py snapshot --root .` emits the outgoing snapshot recipe. These commands are read-only. Normal VALIDATE does not certify a handover's identities, source coverage, matching snapshot or return; consult the separate report and `ADMIN/SCENE_HANDOVER.md`. Its synthetic tests run with `python -B TOOLS/test_handover.py`.

Exit 0 means structural PASS or PASS WITH WARNINGS; exit 1 means a definite structural failure; exit 2 means incomplete execution or coverage. If errors and incomplete coverage coexist, the result remains INCOMPLETE and the definite errors remain listed. Warnings do not change the exit status.

## Evidence classes

Keep the report's classes separate:

```text
STRUCTURAL
Result: PASS / PASS WITH WARNINGS / FAIL / INCOMPLETE
Provenance: SCRIPT-VERIFIED
Coverage: checks actually executed

HOST OBSERVATION
Result: NOT RUN

SEMANTIC
Result: NOT CHECKED
```

SCRIPT-VERIFIED means this script actually ran. Its output identifies the executed and target validator bytes, observed LAW digest, initial and final tree digests, and findings. Different executed/target validator bytes or a tree changed during the run make coverage incomplete. An observed LAW digest is provenance, not an immutable required prompt hash. A validator upgrade may legitimately accompany a core rewrite.

The tree digest includes scanned paths, file bytes, directory entries and link targets. It is a point-in-time observation, not certification of future correctness. A warning is not proof that the warned condition is harmless.

## Structural coverage

The script checks:

- Required kit files, including RECOVERY, CORRECT, UPGRADE_V07, UPGRADE_V08, the cold AGENT_STATE protocol, PLAYTEST_V08 and current release notes; portable path containment, symlink routes, case collisions, UTF-8 and unfinished fixed-path candidates. Required presence is a distribution check, not a normal startup read requirement.
- CURRENT_SAVE required metadata, readable section presence, portable identity, commit lineage shape, bound PC route, and archive_ref/evidence_through agreement. Extension metadata warns; duplicate identity/control fields remain errors.
- Accepted CAMPAIGN_CONTRACT identity, revision, binding and five substantive agreement sections. Each bound agreement also requires exactly one named prose clause in its designated section: `Play form:` in Campaign promise, `Form selection:` in GM initiative, `Structure disclosure:` in Presentation, `Cuts:` in Time and transitions, and `Retcon:` in Player control. A clause is a plain or bullet line with substantive free text, not an enum. Blank/placeholder values, duplicates, wrong sections and clauses hidden in code/comments do not satisfy the check. The unbound template keeps sections `none` and needs no clauses. An older v0.7 agreement receives focused accepted supplementation through RECALIBRATE, not inferred defaults or a campaign reset. Retired calibration axes and a magic acceptance phrase are not required.
- Explicit backticked Markdown record routes in the save, including non-revelatory private watch pointers and exact literal target headings. Ordinary prose and whether a cue has the correct trigger are semantic checks.
- Unbound/bind instance/archive contamination, installed engine identity and declared character-build support, bound module/brief structure, capability routes, character routing closure, and accepted v0.7 T0/bind consistency where parseable. Supported legacy T0 tables remain unchanged; their identity/opening shape is checked and the unverified semantic mapping into new sections is reported as a warning.
- Optional POLICY source voice structure. POLICY is setup material; the accepted agreement owns the runtime presentation choice. Structural inspection is broader than the normal boot read set.
- Active safety flag and entry presence. This verifies shape, not the truth or sufficiency of limits.
- Archive index/session/source reachability, literal evidence identifiers, duplicate routes and stable heading scope. Existing hierarchical-scene-v1 routes remain supported. One coherent episode body is valid; there is no shard-count quota. Optional ledgers are checked only when present.
- Optional cold BEARING provenance/staleness as warnings. There is no mandatory seven-section layout or normal boot dependency.
- Any existing RECOVERY/ACTIVE.md as a pending recovery error, even if its text says complete. Successful recovery/completion removes the active marker only after verification and retains the operation record/preimages. Empty unindexed session directories remain orphan errors. Restoring an interrupted operation includes exact nonrecursive removal of its recorded, verified operation-created directories only when empty; see ADMIN/RECOVERY.md. The validator does not perform recovery.
- Initial/final tree and executed-validator stability.
- Active handover marker presence: a bound campaign receives `HANDOVER_PAUSED` as a warning requiring the dedicated handover check; an unbound kit receives `HANDOVER_UNBOUND` as an error. This presence check does not validate the package or authorize resumption.

v0.8 adds no mandatory NPC fields, stance vector or new current-state owner. Existing PEOPLE prose, NOW processes and KNOWN knowledge records remain valid without conversion into a new schema. Their explicit routes and applicable existing structural rules are checked; the meaning, initialization and causal changes of agent state are not.

A CHECKPOINT may point to an older archived save. It must not claim its own new evidence, mismatch an archived id/folder, or clear an existing evidence boundary. Static inspection cannot prove the values were retained unchanged from a previous current save unless that prior state is supplied and compared separately.

## Not established by PASS

The validator cannot establish that an agreement was actually accepted; that its grants are clear or faithfully performed; that its named clauses truthfully describe form selection, structural disclosure, cut scope or retcon policy; that ordinary world authorship, reserved choices, due processes, compression, scene cuts or operator limits were handled correctly; or that any output was enjoyable. Presence of five clauses is not semantic approval. It cannot prove lore accuracy, appropriate retrieval, narrator/NPC knowledge separation, preservation of player wording, or whether a private cue is sufficient and non-revelatory in meaning.

It does not prove that archived prose came from accepted available play, that an exact transcript was available, that summaries preserve all consequential qualifications, or that SAVE/CORRECT/UPGRADE used complete preimages and the accepted scope. No active marker is not proof that no interrupted write happened. Current file shape cannot certify a past transaction or multi-file atomicity.

It does not execute a GM, test fresh-chat behavior, or observe the host's read/write isolation. AUDIT self-report does not establish those results. Use the separate behavioral and maintenance fixtures in ADMIN/TESTS.md.

An agent-state file's presence does not establish independent NPC decisions, unbiased generation, genuine causal change, privacy or enjoyable play. Those are experimental claims to observe in actual campaigns using ADMIN/PLAYTEST_V08.md. The handover checker protects recorded source bytes and package identity; it cannot prove that the receiving model interpreted or portrayed them faithfully.

## Without Python

One capable model with readable/writable files can still operate RPG OS. If code execution is unavailable, inspect the relevant files manually and label the result MODEL-CHECKED with exact observed coverage. Report a definite defect as FAIL; otherwise report INCOMPLETE, not SCRIPT-VERIFIED PASS. Do not imply unopened paths were checked or pretend to have executed code.

Report OOC and stop. Authorized repair uses the relevant ADMIN procedure and preserves evidence. Pending recovery is resolved through ADMIN/RECOVERY.md before ordinary PLAY.
