# ADMIN — Recoverable file changes

Cold procedure for any operation that changes campaign files: bind, Save/CHECKPOINT, correction, agreement change, review, upgrade, or repair. One model and readable/writable files are sufficient. No script, database, background service, filesystem transaction, or automatic rollback is assumed.

## Before changes

1. Check the exact path `RECOVERY/ACTIVE.md`. If present, resolve that operation below before starting another. Never choose whichever campaign file looks newest.
2. Identify the already authorized change, the accepted input/evidence, the current save/agreement ids, every existing file that will be overwritten, and every new file/candidate and parent directory that will be created. Use exact safe workspace-relative paths; resolve them within the known workspace and check existing ancestors for symlinks before writing. Never follow a symlink or a route outside the workspace. Record which affected directories already exist and verify the absence of each proposed new directory before creation. Exclude unrelated files. Module baseline changes require their separately authorized scope.
3. Choose a new portable operation id. Create `RECOVERY/<operation-id>/OPERATION.md` and `RECOVERY/ACTIVE.md` before changing any campaign path. These recovery files are operational records, not fictional evidence or runtime state. Use non-revelatory names for private material.
4. Copy every affected existing file into `RECOVERY/<operation-id>/before/<original-relative-path>`. Prefer an exact file copy and verify the copy against its original using the host's available file operations. Record the verification method honestly. Preserve complete contents; a paraphrase, diff, checksum alone, or model recollection is not a restorable preimage. If the host cannot preserve and inspect a complete affected file, stop before modifying it.
5. Confirm every intended overwritten file has a verified preimage, every intended new file is listed, and every required new parent directory has recorded and verified pre-existence information. Record that preparation is complete. Only then create campaign directories, write candidates, or publish changes. Record each directory actually created by this operation. If a supposedly absent directory now exists unexpectedly, inspect and reconcile it rather than claiming ownership. If the write set grows, protect and record the additional files/directories before touching them.

The active marker is deliberately small:

```text
operation_id: <operation-id>
record: RECOVERY/<operation-id>/OPERATION.md
```

Any existing marker means ordinary PLAY is blocked, regardless of text claiming completion. Normal startup checks this one exact path; it does not scan recovery history.

The operation record contains:

- operation id, kind, `status: started`, base save/agreement ids, and authorized purpose;
- a write-set table: original path, `existing` or `new`, preimage path for existing files, and verification result;
- a directory-set table: exact path, whether it existed before the operation, how that was checked, whether this operation actually created it, and whether it belongs in the completed result or is temporary;
- enough accepted intended content or exact staged paths to resume the authorized operation without inventing missing material;
- progress and any failure, including which files were actually changed;
- on completion/restoration, the checked result and final `status: complete` or `status: restored`.

Keep private source material private to the available host access level. Opaque paths reduce spoilers; they do not create hidden storage or concealment from the operator. Recovery records and preimage directories are retained recovery material, never rollback cleanup targets.

## During an operation

Stage complete candidates where the owning procedure requires them. Check substantive consistency and all affected exact routes before replacing CURRENT_SAVE or the accepted agreement. Record progress after writes. A last-file replacement orders publication; it does not make prior file writes atomic or prove their semantic completeness.

An interrupted generation, refusal, missing source/preimage required to determine or restore the accepted write target, failed copy/write, or mismatched route is a failed step. A historical source gap already disclosed and handled under the save procedure's evidence-coverage rules is not itself a write failure. Keep failures OOC. Stop publishing; retain the marker, candidates, preimages, and diagnostics. Never turn a failure into fiction or claim a new save succeeded because some files were written.

## Finish

Read the changed files and verify the intended accepted result, identity/evidence pointers, affected routes, and recorded directory set. Check that no required part was skipped and no unrelated file was changed within the recorded write set. An optional validator may check its declared structural scope; do not claim it proves faithful evidence or GM behavior. While the marker/candidates remain, their pending-operation findings are expected and do not by themselves prevent completion. Resolve other material findings, then finish the operation; a clean whole-tree validation, if requested, follows marker/candidate cleanup.

Before clearing the marker, preserve any useful candidate diagnostics inside this operation's retained RECOVERY folder. Remove all resolved live staging candidates by their exact recorded paths and verify their absence. Remove recorded temporary directories only under the same verified-empty, operation-owned, nonrecursive rules used below; keep directories belonging to the completed campaign result. If any staging cleanup fails or leaves unexpected content, retain the active marker and resolve it before PLAY.

After result and staging-cleanup verification, set the operation record to `status: complete`, recording the resulting save/agreement id when relevant. Remove `RECOVERY/ACTIVE.md` last. Retain the operation record, diagnostics, and preimages. If marker removal fails, report that cleanup/recovery remains pending; ordinary boot stays blocked until it is resolved. Diagnostic value never justifies leaving an unfinished candidate in a live INSTANCE or MODULE path after removing the marker.

## Recover or resume

Open only the operation named by the marker and its listed current, candidate, preimage, and directory paths. First establish which writes and directory creations occurred and whether the preimages are complete. A missing or ambiguous operation record is a recovery defect, not permission to infer a clean state.

When the complete accepted target remains available, the model may finish only that already authorized operation after comparing its stages and current files with the record. Do not redraft missing private content, broaden the task, or mint a compensating fictional event. If content or authorization is genuinely missing, preserve the material and request only the missing input.

Otherwise restore every overwritten file from its verified preimage. Before removing a newly created file, verify that its resolved path is inside the intended workspace, no path component is a symlink, and it is explicitly listed as new for this operation. Preserve useful failed evidence/candidates under this operation's recovery folder before any removal. Remove only those individually identified new files needed to restore consistency; never erase pre-existing archive evidence.

Then inspect the recorded operation-created directories, deepest first. Remove a directory only when its record proves it was absent before this operation, this operation actually created it, its resolved path remains inside the intended workspace with no symlink component, and a fresh inspection shows it is empty. Use an exact-path, nonrecursive empty-directory removal; no wildcard, glob, recursive delete, or inferred ownership. Never remove a pre-existing directory, RECOVERY or its retained operation/preimage folders. In particular, an empty new archive session, MODULE, ENGINE, or INSTANCE shard directory is still residue until safely removed when restoring the old tree.

If a directory contains unexpected content, preserve that content and the directory. Do not remove an unlisted file merely to make cleanup succeed. Retain the active marker while its ownership or the restored tree's consistency remains unresolved; report the exact discrepancy for inspection. The same applies when directory pre-existence or creation ownership was not recorded reliably. Do not suppress an orphan-directory finding or call restoration complete after restoring only file bytes.

Compare the restored write set to its recorded preimages and verify the prior save/agreement, routes, and directory structure agree: protected pre-existing directories remain, operation-created residue is resolved, and no unexpected content was discarded. Only then record `status: restored` and the result and remove the active marker. If an interrupted completion already marked the operation complete but left the marker, verify that completion before removing it. Do not merely trust the status word.

If complete inspection/restoration cannot be established, keep the marker and stop PLAY. Explain the concrete missing file or ambiguity. Prior backups help recovery; they do not guarantee it. No branch claims automatic rollback, atomic multi-file writes, or successful restoration without checking the files.
