# ADMIN — Recoverable file changes

Cold procedure for any operation that changes campaign files: bind, Save/CHECKPOINT, correction, agreement change, review, upgrade, or repair. One model and readable/writable files are sufficient. No script, database, background service, filesystem transaction, or automatic rollback is assumed.

## Before changes

1. Check the exact path `RECOVERY/ACTIVE.md`. If present, resolve that operation below before starting another. Never choose whichever campaign file looks newest.
2. Identify the already authorized change, the accepted input/evidence, the current save/agreement ids, every existing file that will be overwritten, and every new file/candidate that will be created. Use exact safe workspace-relative paths; exclude unrelated files. Module baseline changes require their separately authorized scope.
3. Choose a new portable operation id. Create `RECOVERY/<operation-id>/OPERATION.md` and `RECOVERY/ACTIVE.md` before changing any campaign path. These recovery files are operational records, not fictional evidence or runtime state. Use non-revelatory names for private material.
4. Copy every affected existing file into `RECOVERY/<operation-id>/before/<original-relative-path>`. Prefer an exact file copy and verify the copy against its original using the host's available file operations. Record the verification method honestly. Preserve complete contents; a paraphrase, diff, checksum alone, or model recollection is not a restorable preimage. If the host cannot preserve and inspect a complete affected file, stop before modifying it.
5. Confirm every intended overwritten file has a verified preimage and every intended new path is listed. Record that preparation is complete. Only then write candidates or publish changes. If the write set grows, protect and record the additional path before touching it.

The active marker is deliberately small:

```text
operation_id: <operation-id>
record: RECOVERY/<operation-id>/OPERATION.md
```

Any existing marker means ordinary PLAY is blocked, regardless of text claiming completion. Normal startup checks this one exact path; it does not scan recovery history.

The operation record contains:

- operation id, kind, `status: started`, base save/agreement ids, and authorized purpose;
- a write-set table: original path, `existing` or `new`, preimage path for existing files, and verification result;
- enough accepted intended content or exact staged paths to resume the authorized operation without inventing missing material;
- progress and any failure, including which files were actually changed;
- on completion/restoration, the checked result and final `status: complete` or `status: restored`.

Keep private source material private to the available host access level. Opaque paths reduce spoilers; they do not create hidden storage or concealment from the operator.

## During an operation

Stage complete candidates where the owning procedure requires them. Check substantive consistency and all affected exact routes before replacing CURRENT_SAVE or the accepted agreement. Record progress after writes. A last-file replacement orders publication; it does not make prior file writes atomic or prove their semantic completeness.

An interrupted generation, refusal, missing source/preimage required to determine or restore the accepted write target, failed copy/write, or mismatched route is a failed step. A historical source gap already disclosed and handled under the save procedure's evidence-coverage rules is not itself a write failure. Keep failures OOC. Stop publishing; retain the marker, candidates, preimages, and diagnostics. Never turn a failure into fiction or claim a new save succeeded because some files were written.

## Finish

Read the changed files and verify the intended accepted result, identity/evidence pointers, and affected routes. Check that no required part was skipped and no unrelated file was changed within the recorded write set. An optional validator may check its declared structural scope; do not claim it proves faithful evidence or GM behavior.

Set the operation record to `status: complete`, recording the resulting save/agreement id when relevant. Remove only the now-resolved `RECOVERY/ACTIVE.md` marker and staged candidate files whose diagnostic value is no longer needed, using exact listed paths. Retain the operation record and preimages. If marker removal fails, report that cleanup/recovery remains pending; ordinary boot stays blocked until it is resolved.

## Recover or resume

Open only the operation named by the marker and its listed current, candidate, and preimage paths. First establish which writes occurred and whether the preimages are complete. A missing or ambiguous operation record is a recovery defect, not permission to infer a clean state.

When the complete accepted target remains available, the model may finish only that already authorized operation after comparing its stages and current files with the record. Do not redraft missing private content, broaden the task, or mint a compensating fictional event. If content or authorization is genuinely missing, preserve the material and request only the missing input.

Otherwise restore every overwritten file from its verified preimage. Before removing a newly created file, verify that its resolved path is inside the intended workspace and is explicitly listed as new for this operation. Preserve useful failed evidence/candidates under this operation's recovery folder before any removal. Remove only those individually identified new files needed to restore consistency; never recursively delete a directory or erase pre-existing archive evidence.

Compare the restored write set to its recorded preimages and verify the prior save/agreement and routes agree. Record `status: restored` and the result, then remove the active marker. If an interrupted completion already marked the operation complete but left the marker, verify that completion before removing it. Do not merely trust the status word.

If complete inspection/restoration cannot be established, keep the marker and stop PLAY. Explain the concrete missing file or ambiguity. Prior backups help recovery; they do not guarantee it. No branch claims automatic rollback, atomic multi-file writes, or successful restoration without checking the files.
