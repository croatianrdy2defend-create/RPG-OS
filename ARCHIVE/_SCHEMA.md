---
id: archive.schema
class: admin-contract
archive_schema: hierarchical-scene-v1
temperature: cold
---

# ARCHIVE schema — hierarchical-scene-v1

ADMIN maintenance contract. No fiction.

ARCHIVE stores accepted historical evidence. It is not the living present and is never resident at boot.

Core rules:

> Compress the routing layer, not the historical source.

> Index to locate; source shard to establish detail.

## Authority

- `CURRENT_SAVE` and current INSTANCE records govern what is true now.
- ARCHIVE establishes what happened or was known at a past moment.
- An index is routing metadata. It may answer a simple, unambiguous existence question, but it is not preferred authority for exact wording, quantities, sequence, rolls, subtle context, or disputed facts.
- Reading an old possibility, intention, seed, or unresolved matter does not activate it.
- Preserve uncertainty exactly: *might*, *suspected*, *conditional*, *not decided*, and *unknown* must not become facts or future commitments.

## Layout

Use the existing campaign-level router and ledgers:

```text
ARCHIVE/
  _SCHEMA.md
  INDEX.md
  MESSAGES_LEDGER.md
  RELATION_LEDGER.md
  sessions/<close-folder>/
    INDEX.md
    01_<semantic-slug>.md
    02_<semantic-slug>.md
    ...
```

`archive_ref` points to the closed session/slice folder. A folder may represent one full table session or one closed slice; do not relabel established session identities merely to fit the example.

For v0.4-and-later writes, `archive_ref`, campaign INDEX `folder`/`session_index`, and ledger pointers are POSIX-style paths relative to `ARCHIVE/`: for example, `sessions/s01-d001` and `sessions/s01-d001/INDEX.md`. Session INDEX `File` values are filenames or paths relative to that session INDEX directory. Do not store absolute paths, backslashes, `.`/`..` traversal, or symlink routes. An older route prefixed with `ARCHIVE/` may remain reachable with a noncanonical warning; absolute, backslash, traversal, and symlink forms fail validation rather than receiving legacy status.

## Semantic shards

Each future CLOSE partitions accepted PLAY evidence into coherent events likely to be retrieved independently. Good boundaries include a particular conversation, journey, work problem, meeting, investigation, purchase, combat, message exchange, intimate scene, or return home.

Shard only from accepted PLAY actually available in the just-closed slice. Do not reconstruct an omitted scene from model memory, a save summary, an older archive, or an example. If the accepted source is unavailable, preserve that absence and report the fallback.

Do not impose fixed morning/afternoon/evening categories when several independent events occurred. Do not split every micro-action into its own file. A short closed slice containing one coherent event may have one shard.

Use ordered, concise, filesystem-safe Markdown filenames such as `01_arrival.md` or `04_cafe_conversation.md`. Source shards and legacy sources routed by a session index use the `.md` extension. Do not put campaign-specific categories into this universal contract.

Each shard must contain a unique stable evidence heading such as:

```markdown
## E-<save_id>-01
```

Together, the shards preserve the complete accepted PLAY evidence for the closed slice at the same fidelity the former monolithic transcript would have held. Do not aggressively summarize. Rejected/rewound material, unsent UI suggestions, and OOC ADMIN/provider responses are not accepted PLAY. Preserve, when present and relevant:

- accepted player declarations and consequential NPC dialogue;
- exact promises, commitments, messages, formal statements, and important wording;
- rolls, effective values, results, and margins actually recorded;
- timestamps, places, participants, actions, consequences, and sequence;
- purchases, money, equipment, and tracked-resource changes;
- facts learned, unresolved matters created, and choices rejected when historically relevant;
- relationship-affecting exchanges and established incidental physical details;
- uncertainty and missing information as uncertainty and missing information.

Disk size is not the optimization target. Retrieval size is. The shards together preserve the evidence; do not also create a duplicate monolithic transcript for a successfully sharded CLOSE.

## Session INDEX

Every hierarchical session/slice folder contains a compact `INDEX.md`. It routes to evidence and does not retell the session.

Use one entry per shard:

```markdown
## R-<save_id>-01 — concise label
File: `01_<semantic-slug>.md`
Evidence: `E-<save_id>-01`
Time: known span or `unknown`
People: established participants only
Places: established locations only
Topics: compact search terms
Notable:
- one or two routing facts only
```

For v0.4-and-later entries, keep the seven fields exactly once and in the shown order. `Time`, `People`, `Places`, and `Topics` require an explicit value; write `unknown` or `none` when that is the preserved truth rather than leaving a blank. Several routes may point to different headings in one retained legacy monolith, but each new `E-*` semantic shard has one route entry.

Do not copy whole dialogue or scene summaries into the index. If exact or nuanced detail is requested, open the pointed source shard.

Keep each shard entry at no more than 12 nonblank lines. Count from its `## R-...` heading through the line before the next level-two heading, including the route heading and every nonblank metadata/bullet line. If routing cannot fit, shorten the metadata; do not turn the index into a second chronicle.

## Campaign INDEX

`ARCHIVE/INDEX.md` is the sparse campaign-level router. One row per CLOSE identifies the likely session/slice by compact names/search terms, folder, and full path to its session index (for example, `sessions/s01-d001/INDEX.md`). Keep `route_terms` non-revelatory: use enough neutral established people/places/institutions/objects/topics to locate every independently retrievable subject likely to be queried, while one discriminator may cover several shards. Do not expose private outcomes, mechanically enumerate every shard, or retell events. The session INDEX performs finer routing. The campaign INDEX answers “which session should I inspect?”, not “what exactly happened?” If adequate subject coverage cannot remain compact, report evidence for a later router redesign rather than omitting the route or turning this row into a recap. Keep `notes` terse and operational or fallback-only, never a plot recap. The retained `event_heading` field is an optional legacy route, not a requirement for new shards.

Do not turn it into a campaign bible or duplicate every shard summary. If the exact session or shard is already identified by CURRENT_SAVE, an INSTANCE pointer, a ledger, or the operator, skip unnecessary higher routing levels.

## Exact records and ledgers

Use stable subheadings inside the relevant shard only when future exact retrieval is plausibly useful, for example:

```markdown
### M-<save_id>-01
### ROLL-<save_id>-01
### TX-<save_id>-01
```

`MESSAGES_LEDGER.md` and `RELATION_LEDGER.md` point directly to the shard and stable heading. Pointer fragments name the literal stable heading text, not a host-generated Markdown slug, and new ids use the owning CLOSE `save_id`. Ledger routing columns are explicit rather than blank. Do not copy the entire exchange into the ledger. Existing pointers to legacy `MESSAGES.md` or `TRANSCRIPT.md` headings remain valid.

Do not mint exact-record ids for every greeting, trivial action, or disposable line. Stable ids are retrieval aids, not a telemetry quota.

## Retrieval

Use the narrowest sufficient route:

```text
ARCHIVE/INDEX.md, only if the session is not already known
→ session/slice INDEX.md
→ one or a few source shards/headings
→ answer and return to the present
```

Stop when sufficient authoritative evidence is found. A broad cross-session question may justify several selected indexes or shards; one small fact does not.

Do not automatically load every session involving a person, an entire dossier, all relationship history, or neighboring shards. Current authoritative state should answer current-state questions without archive retrieval when sufficient.

Sharding reduces irrelevant whole-file retrieval; it does not prove that a host injected only the addressed section. Section-addressability preflight and AUDIT remain the evidence available to the operator.

## Legacy compatibility and migration

Pre-v0.3.2 `DELTA.md`, `TRANSCRIPT.md`, `MESSAGES.md`, or other monolithic session records remain valid evidence. Do not require immediate conversion. A new session `INDEX.md` may point to a stable heading or addressed section in a legacy file.

Optional migration is **partition + index**, never rewrite + reinterpret:

- preserve exact wording, rolls, times, resources, uncertainty, and contradictions;
- invent no connective material and resolve no ambiguity silently;
- retain the original legacy source whenever exact equivalence is uncertain;
- do not alter CURRENT_SAVE, canon, or save identity merely because the archive schema changed.

Schema adoption and legacy migration are separate ADMIN operations. Do not rewrite old sessions in the same turn that adopts this schema. If migration later becomes useful, perform it on a backup or copy and validate the routes before replacing any established source.

Archive evidence is immutable. Routing metadata and lossless partitions may be revised in a later, separate ADMIN maintenance operation when retrieval improves, provided the original evidence remains reachable and no wording, uncertainty, sequence, or meaning changes. This applies to an awkward hierarchical-scene-v1 boundary as well as a legacy monolith; it is permission to reroute or partition, never to reinterpret.

If safe sharding cannot be completed at a future CLOSE, preserve the detailed source in one legacy-compatible file with stable headings, create a session index that routes to it, and report the fallback. Never discard evidence merely to satisfy the preferred layout.

## Live-state boundary

Archive detail stays in ARCHIVE. Promote only durable, presently causal state into CURRENT_SAVE or INSTANCE overlays. Do not inflate NPC records with complete conversations. A person overlay may retain a compact durable fact and direct pointer; the shard retains the scene.

When accepted play changes a phase, clock/front, faction/institution, economy/resource track, or other mutable subsystem, the source shard preserves the established causal event and exact transition when relevant. Its resulting current value belongs in the selected INSTANCE authority. Closing, indexing, retrieving, or merely ending a session never advances it.
