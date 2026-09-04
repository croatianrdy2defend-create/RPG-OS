---
id: archive.index
class: cold-routing-index
archive_schema: hierarchical-scene-v1
---

# ARCHIVE INDEX

Sparse campaign-level router. PLAY does not load this during normal resident startup.
After a bound CLOSE, BOOTSTRAP may open this file only to match `save_id`, `archive_ref`, and the required nonempty `session_index` route.

One row per CLOSE. `route_terms` uses enough neutral established people, places, institutions, objects, or topics to cover every independently retrievable subject likely to be queried; one discriminator may cover several shards. Keep it non-revelatory: do not expose private outcomes, mechanically enumerate every shard, or turn the row into a recap. The session INDEX performs finer routing. If adequate coverage cannot remain compact, flag that as evidence for later router redesign rather than dropping the route. This table is not a session summary or a trivia list. `notes` is reserved for terse operational or fallback information, never plot recap. `folder` and `session_index` use POSIX paths relative to `ARCHIVE/`; `session_index` is the full relative path to that folder's `INDEX.md` and is required for hierarchical-scene-v1 CLOSE operations.

The machine-readable table uses outer `|` delimiters and one contiguous row block; do not place a row after a blank line. A new hierarchical CLOSE uses a direct child of `ARCHIVE/sessions/`, supplies nonempty `route_terms`, and leaves `event_heading` empty.

Heading ids in pointed files must be unique within that file. Pointer fragments name literal heading text. The existing `event_heading` column remains as an optional legacy route so older DELTA-style rows and pointers stay valid.

| save_id | commit_kind | session | span | place | route_terms | notes | folder | session_index | event_heading |
|---|---|---|---|---|---|---|---|---|---|
