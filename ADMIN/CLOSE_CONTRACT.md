# ADMIN Close Contract

ADMIN maintenance. No fiction.
PLAY never executes this file.
ADMIN writes history. PLAY reads state.
Follow INSTANCE/_SCHEMA.md compilation matrix. MODULE files stay untouched.
For CLOSE, also open and follow `ARCHIVE/_SCHEMA.md` (`hierarchical-scene-v1`).

Promote only durable instance state. Do not promote because someone appeared or was retrieved.

Before compiling the save, identify every causally changed mutable subsystem or person since the prior save and consult the compilation matrix plus its selected single current authority. PLAY has kept those accepted transitions in chat RAM and has written nothing. For a preauthored system/person assigned to NOW/person state with no INSTANCE override, begin from its specifically named MODULE as-of-T0 snapshot and materialize complete as-of-now status by applying every accepted transition exactly once. An emergent person or durable subsystem with no MODULE source follows the established-PLAY rules below. If an override exists, apply only still-unsaved transitions once. A value assigned to CURRENT_SAVE changes only in the candidate; a value assigned to the PC bundle changes only there. Never create a NOW copy merely because a system changed, and never patch MODULE or merge its T0 value back into current INSTANCE state.

Compile private-system watch cues into the candidate at the same time. If a system remains causally live across fresh boot and no other resident fact makes its bounded check discoverable, add/update one non-revelatory `declared_state_flags` cue to its selected current authority. ADMIN may introduce that already-whitelisted optional field here when an accepted emergent durable private subsystem first requires it; no universal reservation is required. If state just materialized, replace any MODULE-snapshot route with the current INSTANCE route. Remove/demote the cue when the system retires or another resident fact supersedes it. Do not add a cue for every dormant system.

## Write order (CHECKPOINT and CLOSE)

Never overwrite CURRENT_SAVE first.

1. Build a **candidate** at `INSTANCE/CURRENT_SAVE.candidate.md` (new unique `save_id`, incremented `save_rev`, `save_parent`, `commit_kind`, `archive_ref`, whitelist fields only) and prepare the compilation plan for every selected INSTANCE authority.
2. Preflight the candidate's whitelist/commit metadata and check that every changed fact has exactly one planned destination. Do not claim full assembled-state validation before those bodies and, for CLOSE, archive routes exist. If this preflight fails, leave all live bodies untouched.
3. Write the selected non-save INSTANCE bodies: NOW/shards (including any first-save emergent-system shard), person overlays, PC entrypoint/shards, KNOWN, CAST_STATUS, and CORRECTIONS only where the compilation matrix requires them.
4. **CLOSE only:** write semantic scene shards with stable heading ids, then the session/slice `INDEX.md`, then the campaign `ARCHIVE/INDEX.md` row (`save_id`, `commit_kind=close`, `folder`, `session_index`). Write ledger pointers last among archive records.
5. Before replacement, perform one bounded prospective consistency check over the candidate and the assembled write set now on disk: candidate fields/metadata satisfy INSTANCE/_SCHEMA.md; every planned INSTANCE body exists at its exact route; each changed fact has one authority; and, for CLOSE, archive/session/ledger routes and headings resolve and agree with the candidate `save_id`/`archive_ref`. The live CURRENT_SAVE still names the prior commit, so this is not a whole-tree VALIDATE PASS. If any check fails, stop and follow P19 restoration; do not replace CURRENT_SAVE.
6. Replace CURRENT_SAVE with the candidate last (delete candidate after success).
7. Confirm the new `save_id` and `commit_kind` to the operator.

If a write fails before replacement, the previous CURRENT_SAVE remains the live pointer, but separately overwritten INSTANCE bodies may already be ahead of it. Stop; do not resume PLAY. Inspect or restore every affected body and archive route from the external backup required by P19, remove a stale candidate only after its diagnostic value is no longer needed, and retry only after consistency is established. Do not claim multi-file rollback or atomicity.
A provider moderation/refusal response or interrupted generation during ADMIN counts as a failed step: keep it OOC, do not treat refusal text as fiction or campaign data, and follow the same P19 inspection/restoration rule.

## CLOSE contents — hierarchical-scene-v1

Present only in CURRENT_SAVE: time, place, compact selected resource totals, pending act, durable flags, `hot_identifiers`. Detailed current inventory, finance, calendar, clock, faction, institution, or other subsystem state has one explicit INSTANCE authority; do not duplicate competing totals.

The `archive_ref` session/slice folder contains:

```text
INDEX.md                    compact routing entries
01_<semantic-slug>.md       detailed accepted historical evidence
02_<semantic-slug>.md       another independently retrievable event, if any
...
```

Partition by coherent events likely to be retrieved independently: a particular conversation, journey, work problem, meeting, investigation, purchase, combat, message exchange, intimate scene, or similar causal unit. Do not impose fixed time-of-day buckets when several independent events occurred. Do not shard every micro-action. One coherent closed slice may have one shard.

Derive shards only from accepted PLAY actually available in the just-closed slice. Do not reconstruct scenes from model memory, CURRENT_SAVE summaries, archive hints, or examples. If exact source text is unavailable, preserve only what the authoritative record establishes and mark missing detail as unavailable.

Together, the scene shards preserve the complete accepted PLAY evidence for the closed slice at the same fidelity the former monolithic transcript would have held. Do not aggressively summarize them. Rejected/rewound material, unsent UI suggestions, and OOC ADMIN/provider responses are not accepted PLAY. Preserve exact consequential wording, accepted declarations, dialogue, messages, promises, rolls and margins, times, places, participants, sequence, resource/equipment changes, facts learned, established incidental details, unresolved matters, and uncertainty when present. Disk size is not the optimization target; retrieval size is.

Every shard has a unique stable evidence heading such as `## E-<save_id>-01`. Exact messages, consequential promises, rolls, transactions, identifiers, or other retrieval-sensitive records may use stable subheadings inside that shard when future exact recall is plausible. Do not mint IDs for every trivial utterance or action.

The session/slice `INDEX.md` contains one compact routing entry per shard: file, evidence heading, known time, established people/places, topics, and no more than one or two notable routing facts. Each entry is at most 12 nonblank lines. It does not duplicate the scene.

The campaign INDEX row must include the same `save_id` as CURRENT_SAVE after CLOSE, the same folder as `archive_ref`, the full `session_index` path, and compact non-revelatory `route_terms`. Use enough neutral established people, places, institutions, objects, or topics to cover every independently retrievable subject likely to be queried; one discriminator may cover several shards. Do not expose private outcomes, mechanically enumerate every shard, or turn the row into a recap. If adequate coverage cannot remain compact, report evidence for later router redesign rather than dropping the route. These are POSIX paths relative to `ARCHIVE/`, as defined by ARCHIVE/_SCHEMA.md. New rows leave legacy `event_heading` empty. Do not turn the campaign index into a global summary.

Indexes locate evidence. They may answer a simple unambiguous existence fact, but exact wording, quantities, sequence, rolls, subtle context, or disputed history require the source shard.

If a message had exact wording: store it under a stable heading in the relevant shard and add a MESSAGES_LEDGER pointer. Live save stores at most: “nothing waiting” / “N unread” / “open thread with X”.

If accepted play included intimacy or other embodied detail: scene-shard heading; RELATION_LEDGER row; INSTANCE person overlay `## PC` pointer only. Never write progression into MODULES/. Prior intimacy is a fact, not an obligation to start or continue a romance.

On the first CHECKPOINT/CLOSE after person promotion or durable change, create `INSTANCE/PEOPLE/<person_id>.md` as the complete as-of-now mutable surface (`NOW`, `PC`, and only affected current PRIVATE state), applying each accepted transition once. The PEOPLE/CAST_STATUS route, `hot_identifiers` when hot, and record use the same stable portable id. For a preauthored person, keep stable CANON and unrelated PRIVATE lore in MODULE. For an emergent promoted person with no MODULE record, the INSTANCE record also receives only established minimal CANON and CAST_STATUS receives the id/record mapping. Never invent missing identity or promote a transient appearance. PC sheet changes go only to the INSTANCE PC entrypoint or its explicit shards.

On the first CHECKPOINT/CLOSE after an emergent non-person subsystem gains durable causal state, assign one stable portable `system_id` and create exactly one `INSTANCE/NOW/<system_id>.md` shard routed from NOW. Store only its established complete current state and the minimum operational definition needed to continue it after fresh boot: triggers/non-triggers, current-state route, cue lifecycle if needed, and dependency/update order if needed. Do not invent missing operating rules, promote a transient condition for drama, or patch MODULE. Later saves update that same shard. Add a compact non-revelatory cue only if the ordinary cross-boot cue conditions require one.

For a clock, phase, front, faction, institution, economy, resource, or similar mutable system, record the exact established transition and cause in the relevant scene shard when historical evidence matters; keep the resulting current value only in its selected INSTANCE authority. Do not advance a tracker because the session ended, CLOSE ran, its body was retrieved, or time passed unless elapsed time is an explicitly declared cause.

Archive a private/offscreen transition or its cause only if it was explicitly established in the accepted just-closed PLAY context. If the source detail never entered the available accepted record, persist only the defensible current private state and mark the missing historical cause/detail unavailable or unfixed. Never reconstruct hidden history from model memory at CLOSE. Whether repeated use later justifies a separate provenance-bearing private-event record is a testing question, not a license to invent one now.

Do not duplicate all archive detail into NPC overlays. Store only compact durable present state and a direct pointer when current retrieval needs one.

## Checkpoint (cheap)

Overwrite via the same candidate write-order, `commit_kind: checkpoint`, `archive_ref: none`.
Do not write ARCHIVE, indexes, ledgers, or scene shards.

After CHECKPOINT, say plainly: the present (time/place/resources/pending act) is saved. Exact wording since last CLOSE is **not** in the archive.

Suggest checkpoint in the footer as `checkpoint available` — never as fiction. Do not nag every turn.

CHECKPOINT is a complete save of the present. CLOSE adds archival evidence and exact recall. Do a full CLOSE before ending the day if wording must survive.

## Grain

One folder per closed slice, not one row per cigarette. Within it, one shard per coherent independently retrievable event, not one file per action.
The session index stays short. Shards stay detailed.
Weeks later, exact wording → ledger or campaign index → session index → one source heading. Not the whole basement.

PLAY retrieves that heading only when the present situation makes recall causally natural.

## Legacy archives

Existing `DELTA.md`, `TRANSCRIPT.md`, `MESSAGES.md`, or other monolithic archives remain valid. Do not migrate them merely because this schema exists. A session `INDEX.md` may point to stable headings or addressed sections in those files.

Optional migration is partition + index, never rewrite + reinterpret. Preserve exact wording, rolls, times, resources, uncertainty, and contradictions. Invent nothing. Retain the original source whenever exact equivalence is uncertain. Archive migration never changes CURRENT_SAVE, campaign canon, or save identity.

Do not combine adoption of this schema with legacy migration during active play. Migrate later as a separate ADMIN maintenance job on a backup/copy, and only when useful.

If safe sharding cannot be completed during a future CLOSE, preserve the detailed accepted source in one legacy-compatible file with stable headings, add a session index that routes to it, and report the fallback. Never destroy evidence to force the preferred layout.

## Forbidden

- Boot-loading transcripts
- Copying transcript prose into CURRENT_SAVE
- One ever-growing CHRONICLE.md
- One giant campaign index that summarizes every scene
- Treating index metadata as authority for exact or disputed detail
- Creating a duplicate full-session transcript after detailed shards were successfully written
- Activating an archived possibility merely because it was retrieved or indexed
- Rewriting or interpreting legacy history during partition
- Patching MODULE CHAR or MODULE PEOPLE
- Clearing ARCHIVE
- Setting safety_state active without a real Hard-no/Fade sentence
