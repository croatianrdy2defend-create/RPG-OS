# PLAY — One short write-only note

Use only when the agreement selects `Incremental recording: write-only-log`. Continue from working conversation; do not inspect persistence files each turn.

After resolving the declaration, append **one or two concise sentences** describing what actually happened:

```text
python -X utf8 -B TOOLS/play_log.py --root . append --text "<brief factual outcome>"
```

That is the entire routine persistence step. No resume, prepare, confirm, status, owner lookup, hashes, source matching, readback, patch plan, journal compilation or new script. Do not reread the log after appending. Report an actual append failure plainly without starting a retry/audit loop or claiming it succeeded.

The note may be appended immediately before delivering the resolved reply. It is a working note, not proof that the reply reached the player. If delivery is interrupted or revised, reconcile that ambiguity once at the next CHECKPOINT/SAVE against the actual conversation; no per-turn delivery protocol is introduced.

Keep consequential changed circumstances, time/resources, knowledge, commitments, unresolved choices and operative private state concise. Retain actual roll results when needed. Original conversation preserves complete dialogue and scene texture. Do not copy a full NPC baseline, retell prior events, record unchanged-property disclaimers, explain rules or list intended bookkeeping. Existing five-field NPC state is reused; note only substantive changes, including genuine disengagement. Ending an interaction does not require a dossier rewrite, new filename or reorganization.

At a fresh boot, read compiled state and uncompiled notes once with `play_log.py --root . read`, then use context during ongoing play. A specifically missing fact or actual material mechanical question can require its narrow source; ordinary portrayal or an incidental keyword does not trigger rulebook research merely to prove no change. Selected rules still apply at their real triggers.

CHECKPOINT is ADMIN work: compile actual changes at the accepted checkpoint cadence. Preserve deferral and meaningful earlier triggers. Full SAVE additionally archives remaining available source and performs the selected bounded review. END SESSION retains actual feedback and due mechanics. The short log supports those operations; it is neither a complete transcript nor a verified full save. Installation alone enables nothing.
