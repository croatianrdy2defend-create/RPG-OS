# RPG OS — locked boundary

Status: RPG OS v0.5 final-for-testing package. Prototype maturity; initial lifecycle validated, not Session-100-proven. LAW frozen.

Layers: OS → ENGINE → MODULE → INSTANCE.

Resident PLAY: OS/LAW.md + INSTANCE/CURRENT_SAVE.md (this kit ships unbound).

This public kit contains no campaign world. Testers use New Game.

P0/P1 execution contradictions from the prior audit are closed in ADMIN/BOOTSTRAP/SCHEMA. P17 documents the section-isolation limit; P18 tests persistent writes; P19 tests provider interruption during ADMIN. `ARCHIVE/_SCHEMA.md` defines hierarchical-scene-v1; P20–P23 test semantic sharding, source authority, nonactivation, and legacy compatibility; P24 tests general retrieval locality. P25–P26 test executable validation and an honest no-code fallback. P27–P39 test optional character construction, selective campaign complexity, T0-to-live state, preauthored and emergent people/systems, resource authority, house-rule placement, interacting systems, private-system cues, spoiler modes, LOAD parity, and routed PC bundles. No LAW edit.

## Optional construction depth

NEW GAME always asks separately for world/campaign depth, character/profile depth, and mechanical-sheet path. A sparse campaign, Quick profile, and deferred full sheet are first-class valid outcomes. A completed character sheet is optional; a substantive operator-approved PC baseline is required.

Focused or detailed construction opens separate ADMIN guidance and builds only selected domains. The standard campaign vocabulary can express phases/arcs, causal clocks/fronts, autonomous institutions and factions, inactive possibilities, generic and intimate relationship dimensions, resource/accounting precision, private-truth disclosure modes, and house-rule calibration without making any of them universal requirements.

Stable definitions and immutable as-of-T0 snapshots remain in declared MODULE bodies. They do not compete with later current state. PLAY keeps accepted post-save transitions in chat RAM and writes nothing; the next explicit CHECKPOINT/CLOSE applies each transition once in the selected single authority—CURRENT_SAVE candidate, NOW/person route, or PC bundle. A durable subsystem first established after bind instead receives one routed INSTANCE/NOW shard containing its established minimum operating definition and current state; MODULE remains untouched. A private system that must remain independently live across fresh boot gets a compact non-revelatory watch cue only when no other resident fact makes its check discoverable; explicit saves update or demote that cue with its lifecycle. This avoids preactivating every tracker or copying an entire world into the live instance.

The PC entrypoint may likewise remain one cohesive body or become a compact routing index when sheet/profile/resource parts are independently useful. Bind copies only its exact transitive route closure into INSTANCE; detailed construction does not force sharding.

House-rule authority is explicit: POLICY controls presentation/cadence/boundaries; RULES_HOOKS may calibrate but not contradict ENGINE; a real rules override uses a distinct compact ENGINE id; later table rulings live in INSTANCE/CORRECTIONS.

## Retrieval locality — design axiom

> Large information domain → compact routing/index layer → narrowly scoped authoritative shards.

Persistent information should be stored at approximately the smallest practical authoritative granularity likely to be independently relevant during play. No large file should exist merely because all of its contents belong to the same broad category.

Split by retrieval locality, not by an arbitrary token or word threshold. A cohesive long file may be correct when most queries need most of it. A shorter file containing unrelated facts is a poor unit when those facts are normally retrieved separately.

When independent retrieval becomes useful:

1. preserve a stable declared entrypoint;
2. make that entrypoint a compact routing index or capability map;
3. route through explicit file/section pointers to narrower authoritative records;
4. recurse only where another level materially reduces unrelated retrieval;
5. stop when the requested authoritative unit has been reached.

Indexes answer “where should I look?” They do not duplicate the bodies they route to and do not become global summaries. Cross-links name likely dependencies; they are not permission to browse neighbors or retrieve material without an immediate causal reason.

Do not shard prematurely. A small NPC, engine, institution, location, or register remains one file. If it later grows so that CANON, current state, relationship history, private state, geography, culture, equipment, rules, or other parts are routinely needed independently, retain a compact entrypoint and split only those authoritative parts.

This axiom applies to ARCHIVE, MODULE world/lore/people/institutions, INSTANCE registers and overlays, ENGINE extensions, rules hooks, equipment catalogs, bestiaries, timelines, relationships, and private GM material.

The filesystem may be huge. The active context should not be.

## Validation boundary

`VALIDATE` is an ADMIN-only, OOC, read-only diagnostic. When code execution exists, `TOOLS/validate.py` mechanically checks only deterministic structural invariants: required release files and validator identity, frozen-LAW bytes, CURRENT_SAVE grammar and commit state, clean initial INSTANCE registers, safe engine identity/support metadata, the bound module using v0.4 descriptor grammar where machine-parseable, PC route closure and bind-copy integrity, safety flags, archive routes and heading targets, route-entry budgets, ledger pointers, path containment, stale candidate residue, initial archive contamination, and routed orphan sessions. It does not prove that every structurally complete archive write belongs to a completed transaction; P19 remains the interruption test.

Its report is ephemeral. It is not a campaign register, is never resident at boot, and must not be written into CURRENT_SAVE. A deterministic digest identifies the scanned path/type/content snapshot for that one run; it is not a continuing certificate.

The report keeps three evidence classes visibly separate:

- **STRUCTURAL** — `SCRIPT-VERIFIED` when the shipped script actually ran; otherwise `MODEL-CHECKED` and necessarily `INCOMPLETE` unless a definite defect was observed.
- **HOST OBSERVATION** — not run by structural validation. Section isolation, persistent writes, provider interruption, and model identity require separate observations.
- **SEMANTIC** — not checked. Shard coherence and source fidelity, agency, salience, uncertainty preservation, and copyright judgment remain prose tests or human review.

Archive metrics are observations, not fixed split triggers. Do not add host profiles, recursive campaign-index machinery, or repartition metadata merely to make the specification appear complete; add them only if campaign evidence establishes the need.

CURRENT_SAVE-last protects the authoritative save pointer but does not make several separately overwritten INSTANCE bodies a filesystem-atomic transaction. P19 therefore remains a real fault-injection test for hosts and complex campaigns. Keep an external backup before ADMIN writes; after any interrupted multi-file CHECKPOINT/CLOSE, do not resume PLAY until the current save and all affected INSTANCE/archive bodies have been inspected or restored. An immutable commit-manifest design is a possible later structural change, not silently claimed by v0.5.
