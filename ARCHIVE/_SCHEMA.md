---
id: archive.schema
class: admin-contract
archive_schema: hierarchical-scene-v1
temperature: cold
---

# ARCHIVE schema — hierarchical-scene-v1

Cold ADMIN reference. ARCHIVE preserves historical evidence; INSTANCE records govern the present. Indexes locate sources. They may answer simple unambiguous existence questions, but exact wording, quantities, sequence, rolls, subtle context, or disputed history require the pointed source.

## Layout

```text
ARCHIVE/
  _SCHEMA.md
  INDEX.md
  MESSAGES_LEDGER.md       optional useful exact-record routes; may remain empty
  RELATION_LEDGER.md       optional useful relationship routes; may remain empty
  sessions/<close-folder>/
    INDEX.md
    01_<episode>.md
    02_<episode>.md        only if another useful retrieval boundary exists
```

A full Save/CLOSE/END SESSION creates one folder per closed available slice. A CHECKPOINT creates no evidence folder and retains the earlier archive_ref/evidence_through. The latter pair identifies the latest archived close, not necessarily the current save id.

An outgoing scene handover creates transport records under HANDOVER, not an archived close. On accepted return, preserve the available non-graphic return account through the normal full-save evidence layout, identifying its coverage and original package/return source. Do not claim omitted raw dialogue was archived or apply already-imported state changes again. Retained handover copies are provenance, not another current authority or a replacement for required archive bodies and indexes. `ADMIN/SCENE_HANDOVER.md` owns return identity and receipt checks.

Use safe POSIX paths relative to ARCHIVE for archive_ref, campaign folder/session_index, and ledger pointers. Session INDEX File values are relative to that index's folder. New folders are direct children of sessions/. No absolute path, backslash, traversal, or symlink route. Existing `ARCHIVE/`-prefixed legacy routes remain readable with a noncanonical warning. Stable pointer fragments name literal heading text, not host-generated slugs.

## Accepted source and fidelity

Preserve the accepted evidence actually available since the previous evidence boundary. A prior checkpoint may have saved the resulting state without archiving its source; include that source if still available, without applying its state transitions twice. Preserve consequential declarations/dialogue, exact promises/messages, rolls and margins, quantities and resource changes, chronology, participants, learned facts, choices and uncertainties when present.

One coherent episode can be one detailed body. Split only at independently useful retrieval boundaries such as a conversation, journey, purchase, battle, investigation, or return. Do not require one file per action, time-of-day category, person, or romantic exchange. Together the bodies preserve available accepted source at its original fidelity; they are not aggressively compressed summaries.

Each new evidence body has a unique stable heading such as `## E-<save_id>-01`. Useful exact records may use subheadings such as `### M-<save_id>-01`, `### ROLL-<save_id>-01`, or `### TX-<save_id>-01`. Ids are aids, not a quota.

Do not reconstruct unavailable source from model memory, CURRENT_SAVE, an old index, or a genre expectation. Record a source gap explicitly: what span/detail is unavailable, what surviving authority establishes, and what remains uncertain. `evidence_through` does not certify a complete transcript. A defensible private current value does not prove its unrecorded historical cause. Do not invent private events while saving.

Rejected/rewound fiction, unsent suggestions, hidden candidate generation, and OOC ADMIN/provider responses are not accepted fictional evidence. An explicitly accepted correction may be stored as a clearly labeled record correction, identifying what it supersedes; it must not be narrated as a new fictional event. Keep the unaffected original evidence and its uncertainty.

Do not create a duplicate full-session transcript after a faithful partition. If partition equivalence is uncertain, preserve the original detailed source and route to it. Disk duplication during a protected recovery operation is a backup, not a second canonical evidence record.

## Session INDEX

Retain the existing compact entry grammar so old readers and routes remain usable. One route per new evidence shard:

```markdown
## R-<save_id>-01 — concise label
File: `01_<episode>.md`
Evidence: `E-<save_id>-01`
Time: known span or `unknown`
People: established participants or `none`
Places: established locations or `unknown`
Topics: compact search terms
Notable:
- one or two routing facts, including a source-gap warning when relevant
```

For hierarchical-scene-v1 writes use those seven fields once and in that order; keep the entry at no more than 12 nonblank lines. Indexes route rather than retell. Several legacy route entries may address different stable headings in one retained source. New evidence shards have one route each. Source bodies use .md files, and pointed headings are unique within their file.

## Campaign INDEX

Keep one row per archived close using the existing columns:

`save_id | commit_kind | session | span | place | route_terms | notes | folder | session_index | event_heading`

commit_kind is `close`; folder and session_index identify the new folder and its INDEX. New writes leave legacy event_heading blank. Preserve established session identities. route_terms contain compact neutral names/subjects sufficient to locate likely requested evidence; they do not enumerate every scene or reveal private outcomes. notes is terse operational information, including a meaningful source gap or superseding correction route where needed, never a plot recap.

The table uses outer pipes and one contiguous row block. Do not add rows after a blank line. Skip campaign-level routing when a current record, the operator, or a ledger already identifies the exact session/source. If campaign routing becomes unwieldy, improve its explicit indexes in separate maintenance rather than turning it into a campaign bible.

## Optional direct ledgers

MESSAGES_LEDGER may point directly to useful exact wording. RELATION_LEDGER may point to relationship-affecting evidence. These are optional shortcuts: a complete save does not require an entry in either just because a message, intimacy, or relationship occurred.

Keep existing column grammar and POSIX source-file-plus-literal-heading pointers when adding a row. Preserve unknown values explicitly, and store only a compact routing gist. Do not copy the exchange. Existing MESSAGES.md, TRANSCRIPT.md, and other legacy source pointers remain valid. A current person record may carry the same useful source pointer without copying its scene.

## Retrieval, history, and maintenance

Current questions begin with current INSTANCE authority. Historical questions use the narrowest sufficient route: campaign INDEX only if needed, selected session INDEX, then the relevant source body/heading. A broad cross-session question may justify several selected sources. One small fact does not justify loading every scene about a person.

Preserve recorded scope, time, modality and knowledge: suspected, conditional, not decided, unknown, rumor, and private belief do not become outcome. Reading old preparation or an unresolved possibility never activates it. Later current state does not retroactively rewrite what was known then.

Archive evidence is immutable. Routing metadata and lossless partitions may be changed only by a separate protected ADMIN operation that retains reachable original evidence whenever equivalence is uncertain. Use ADMIN/RECOVERY.md before modifying existing indexes/ledgers. Reindexing never changes CURRENT_SAVE, save identity, history, or facts. Corrections use ADMIN/CORRECT.md and explicit supersession rather than silent historical editing.

Legacy DELTA.md, TRANSCRIPT.md, MESSAGES.md and prior hierarchical-scene-v1 sources remain readable. No forced migration or deletion accompanies schema adoption. Exact wording, sequence, quantities, ambiguity, contradictions, and original identifiers survive any optional partition.

Physical sharding helps selective reading but does not prove a host returned only an addressed section. Inspect actual host behavior; do not treat an instruction to ignore visible neighboring text as isolation.

The optional `EVIDENCE/` store is a distinct exception to the rule against duplicate accepted-history transcripts. It preserves an actual raw export unchanged, including OOC, superseded and rewound material. It is not another accepted ARCHIVE body, does not establish canon, and cannot advance `evidence_through`. Normal PLAY does not preload it. Capture and reconciliation follow `ADMIN/EVIDENCE_AUDIT.md`.
