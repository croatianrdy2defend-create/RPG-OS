# RPG OS Retrieval Service

Detailed PLAY routing manual. This file is cold at startup.

Open it only after LAW's operating order has identified a concrete GM task that requires a nonresident fact, exact record, private current state, or rules procedure. Retrieval answers **where to look**. It does not decide what deserves a scene, what becomes true, or what the GM must create.

## Retrieval request

Before following a route, identify internally:

1. the GM task;
2. the specific fact or procedure needed;
3. whether the question is current truth, historical evidence, mechanics, private fixed truth, or provisional interpretation;
4. the smallest authority likely to answer it;
5. the stopping condition.

Do not expose this checklist, routes, filenames, rejected material, or private analysis in fiction.

## Universal controls

- Retrieve context **sufficient and proportionate** to the GM task. A broad task may legitimately need several narrow authorities; a narrow task should not receive a domain dump.
- Use accepted post-save developments already established in the current chat before older current-state files.
- Prefer an explicit resident pointer over an index. Use an index only to choose a target. Stop when sufficient authority is found.
- Do not run `find`, `ls`, recursive search, repository inventory, or neighbor discovery during PLAY.
- Do not browse sibling files, people, seeds, clocks, or archive scenes merely because they share a directory or index.
- A cross-link permits retrieval only when the current task independently needs the linked authority. It is not a reading assignment.
- Retrieval does not confer importance, salience, activation, truth, or camera time.
- Zero additional retrieval and zero-result retrieval are valid. If an authority is required and unavailable, preserve the correct unknown or unfixed state rather than guessing.
- Missing stored authority does not prove a prospective detail is forbidden to author. It also does not warrant authorship. Apply LAW's creation rules.
- Repository existence is not relevance. Location is not a roster. Status is not a body. A cue is not the value it points toward.
- If a host returns a whole file, use only the addressed section and discard unrelated content from GM judgment. If tests show leakage, physical splitting is the supported isolation escape hatch.
- Never substitute another campaign pack, another engine, or memory from another chat.

## Capability routing

Module paths are relative to `MODULES/<module>/`, where `<module>` is the safe bound id in CURRENT_SAVE and CAMPAIGN_CONTRACT. Engine paths use the safe bound `engine` id. Do not hard-code a campaign name.

When a task requires an optional module capability:

1. Open the bound `MODULE.md` and address only `## Capabilities`.
2. Confirm the needed capability is declared with a real entrypoint.
3. Open that entrypoint.
4. If it is a routing index, follow only the explicit target that answers the task. Recurse through another index only when it materially narrows retrieval.
5. Stop at the smallest sufficient authoritative body or section.

If a capability is omitted, no stored authority of that capability exists. Do not infer a hidden body or invent retrospective fact. This does not remove the GM's lawful prospective creative space.

Indexes locate information; they do not duplicate or outrank it. A compact index may answer an unambiguous routing or existence question. Exact wording, quantity, sequence, subtle context, current private state, or disputed fact requires the pointed authority.

## Rules and character

| Needed authority | Deterministic route |
|---|---|
| Listed PC value or sheet requirement | CURRENT_SAVE `pc_record` → smallest named section or explicit shard under `INSTANCE/CHAR/`. Never browse sibling shards. |
| Current operator ruling or correction | `INSTANCE/CORRECTIONS.md` → one explicitly pointed shard if the entrypoint has become an index. Stop if it settles the question. |
| Bound ENGINE procedure | On the first mechanic in a fresh chat, inspect the matching scope in `INSTANCE/CORRECTIONS.md`; then test only `ENGINE/<engine>.md` and `ENGINE/<engine>/ENGINE.md` without listing. Exactly one must exist. Open its relevant procedure. Neither or both is a fail-closed engine defect. |
| Campaign rules hook | Bound `MODULE.md#Capabilities` → declared RULES_HOOKS entrypoint → one matching section or target. ENGINE wins a contradiction; a genuine resolution change requires another ENGINE id. |

Do not retrieve a sheet merely to fill narration. Retrieve it when the identified task needs a listed value, limit, ability, resource authority, or build requirement.

When a required value is absent, ask once or proceed without a mechanical success/failure. Do not invent a target or leave the contest hanging.

## Contract, policy, and public world

| Needed authority | Deterministic route |
|---|---|
| Campaign promise, fit envelope, axes, creative mandate, guidance, REVIEW mode | Resident `INSTANCE/CAMPAIGN_CONTRACT.md`. Do not replace an accepted run setting with a MODULE default. |
| Broad stable setting assumptions and ordinary public reality | The pre-fiction-loaded `MODULES/<module>/SETTING_BRIEF.md`. Do not reopen it every turn or treat `Available depth` as a reading assignment. |
| Narrative voice or module safety extras | Bound `POLICY.md`, named section. BOOTSTRAP loads these before first fiction. |
| Other module cadence, tone, anti-attractor, or relationship policy | Bound `POLICY.md`, only the named section required by the task. |
| Module identity or capability list | Bound `MODULE.md`, descriptor or `## Capabilities` only. |
| Public setting, place, culture, or institution function | Bound MODULE capability WORLD or INST → one explicit authoritative target/section. |
| Visual interpretation | Declared VISUAL entrypoint → one target; open an image only if the image itself is required. |

Campaign Contract settings calibrate authorship but never prove a specific person, event, clue, or opportunity exists. The Setting Brief supplies broad public defaults at its scope, including which foundational features are ordinary; it does not identify the occupants of a particular place or settle exact, local, quantitative, disputed, private, or causally material detail. Route those questions to the narrow WORLD or INST authority when the task actually needs them.

A public world description supplies fit and facts at its scope; general world logic remains fit, not warrant. Neither the Setting Brief nor a detailed public authority creates an incident, activates a person, or imposes a representative quota.

## Current state and causal systems

Begin with accepted post-save change already established in this chat, then resident CURRENT_SAVE, then the one selected current INSTANCE authority.

| Needed authority | Deterministic route |
|---|---|
| Immediate present, scene state, due obligation, PC-declared goal, or causal frontier | Resident CURRENT_SAVE. Follow one explicit route only if the required detail is not resident. |
| Learned durable public fact | `INSTANCE/KNOWN.md` → one explicitly pointed shard if needed. |
| Current private register | `INSTANCE/NOW.md` → one explicitly pointed entry or shard. |
| Saved ruling | `INSTANCE/CORRECTIONS.md` → one explicit target if routed. |
| Mutable subsystem current status | Accepted post-save transition → explicit resident/INSTANCE current authority named by the causal cue → only when no current override or due transition exists, the one named MODULE as-of-T0 snapshot. |
| Preauthored subsystem definition or trigger | Its explicitly named declared MODULE capability and section, reached from a current fact, due cue, or immediate task. Never scan the capability or load every tracker. |
| Emergent durable subsystem | Exact `INSTANCE/NOW/<system_id>.md` route explicitly recorded by NOW or a resident cue. Never browse NOW siblings. |
| Phase, clock, front, faction, institution, economy, or logistics body | Only the specific current state and definition needed to resolve the selected causal check; never load the family of trackers. |

A MODULE mutable value is an immutable as-of-T0 snapshot, not permanent current truth. Once an INSTANCE authority or accepted post-save transition exists, use it for current status. If a declared transition may be due, retrieve and resolve its exact rule instead of assuming the T0 value persisted.

Elapsed time advances a system only when that system's authoritative rule declares elapsed time as a cause. Reading it, reaching a threshold in a different system, ending a session, PERSIST, or REVIEW does nothing unless an explicit causal rule says otherwise.

A compact private cue may justify checking an exact authority. It does not reveal, activate, or advance the hidden value. Do not use the cue's filename or id in fiction.

## People and relationships

Retrieve a person only when already present, named by player intent, scheduled, implicated by an established cause, or otherwise independently authorized under LAW. A place, roster, index, hot list, attractive description, or retrieved name never introduces them.

| Needed authority | Deterministic route |
|---|---|
| Current NOW of a known preauthored person | Accepted post-save change → exact `INSTANCE/PEOPLE/<person_id>.md#NOW` if an overlay exists → only if no overlay/change/due transition exists, that person's named MODULE as-of-T0 `## NOW`. |
| Current relationship state with PC | Accepted post-save change → exact INSTANCE person overlay `## PC` → only if no overlay/change/due transition exists, named MODULE as-of-T0 `## PC`. Use ARCHIVE separately for exact history. |
| Stable identity of a preauthored person | Declared PEOPLE entrypoint → that already named person's `## CANON` or explicit CANON shard. |
| Stable identity of an emergent promoted person | Exact `INSTANCE/PEOPLE/<person_id>.md#CANON` reached from an already known id. |
| Hidden fixed private life | That person's exact INSTANCE or MODULE `## PRIVATE` authority, only when causally required. |
| Mapping for an already named emergent person | Exact `INSTANCE/CAST_STATUS.md` mapping. Never browse the roster or use it to choose someone to introduce. |
| Promotion roster or discovery | `INSTANCE/CAST_STATUS.md` is ADMIN-only for discovery. PLAY does not open it to find cast. |

For a MODULE person, NOW and PC are T0 snapshots. After an INSTANCE overlay exists, do not merge it with the older snapshot to create current truth. An emergent person has no retroactive MODULE history.

Promotion is a persistence decision for durable causal state, not permission to portray or a reward for being memorable. A transient ordinary occupant may function without a durable identity.

## Fixed private truth, seeds, and preparation

| Needed authority | Deterministic route |
|---|---|
| Fixed private causal truth | Declared TRUTH entrypoint → one exact target, only when the identified GM task makes that truth causally relevant. |
| Seed or optional prepared possibility | Only after authority has been established **without candidate text**: a responsive trigger, still-valid external warrant, or accepted creative mandate. Then declared SEEDS entrypoint → one already implicated or deliberately selected target. |

Opening a seed or possibility never activates it, establishes it, or requires its use. A fresh lawful realization or selecting none when discretionary remains valid. Do not inspect candidates to discover a warrant, and do not let a candidate backfill one.

When the responsive trigger is an explicit accepted request for **new authored material**, do not satisfy it merely by substituting a stored candidate or use “none” to avoid authorship. Author a fresh lawful realization; if a hard boundary makes the request impossible, explain that constraint OOC.

Durable preparation is disabled by default in v0.6. Do not invent a preparation file, preload candidates, or treat Bearing as preparation.

## Historical evidence

ARCHIVE is historical evidence, not the living present.

| Needed authority | Deterministic route |
|---|---|
| Exact past event, roll, quantity, or sequence | If the session/slice is unknown: `ARCHIVE/INDEX.md` → that session `INDEX.md` → one scene shard/heading. Skip known levels when a trusted current pointer or the operator identifies the target. |
| Exact message wording | `ARCHIVE/MESSAGES_LEDGER.md` → one exact-message heading in the pointed scene shard; follow a legacy MESSAGES pointer as written. |
| Embodied or intimacy recall | `ARCHIVE/RELATION_LEDGER.md` → one pointed scene heading; follow a legacy TRANSCRIPT pointer as written. |
| Cross-session development | Current relation/state first → only the archive indexes and scene shards proportionate to the actual question. |

Do not retrieve a whole session because one detail was requested. Archive indexes may summarize routes but do not replace source evidence for exact or contested claims.

Preserve recorded modality exactly: `might`, `suspected`, `conditional`, `unknown`, `not decided`, rumor, and private belief do not become established outcome.

## Bearing

BOOTSTRAP may load one current matching `INSTANCE/BEARING.md`. Do not retrieve an old Bearing during PLAY to look for direction.

Bearing may orient stewardship but never answers “what is true,” “what must happen,” or “what warrants this candidate.” If a task needs evidence cited by Bearing, retrieve the actual current or historical authority independently and proportionately.

Do not browse rejected, superseded, or cold candidate material mentioned by a Bearing. Preparation remains cold.

## Safety

Operator safety entries are loaded only by BOOTSTRAP when CURRENT_SAVE `safety_state` is `active`, or when the player explicitly changes or asks about them. The deterministic authority is `INSTANCE/SAFETY.md`.

Module safety extras are the named section in bound `POLICY.md`. LAW's floor always applies.

Safety boundaries guide omission, veil, rewind, and refusal. Their literal wording stays out of NPC dialogue.

## Missing, conflicting, or excessive results

- **Missing exact/current authority:** state the uncertainty OOC only when necessary to continue; ask once for a required value or ruling; never invent retrospective truth.
- **Conflict:** apply LAW's question-specific authority. Report an unresolved contradiction OOC instead of disguising it in fiction.
- **Too much returned:** use only the addressed authority; unrelated content is not available for selection or color.
- **Still insufficient:** follow one additional explicit pointer only when it materially narrows or completes the same task. Stop when sufficient.
- **Task changed:** end the prior retrieval plan. Re-orient and identify the new task before opening a different branch.

Every lookup ends in GM judgment. A route can prevent a lie; it cannot decide whether the campaign should move.
