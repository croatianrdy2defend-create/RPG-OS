# RPG OS v0.6 — a file-native AI GM runtime

[![Structural validation](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/validate.yml/badge.svg)](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/validate.yml)
[![Documentation: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey.svg)](LICENSE)

RPG OS is a folder of plain Markdown files that helps a capable large language model run a persistent solo tabletop campaign.

The simple idea is:

> **The GM imagines and judges. The rules constrain and clarify. The files remember.**

The chat is temporary working memory. The campaign's accepted present and history live in files. The design lets a fresh chat resume the same campaign without pasting the entire transcript—but the AI is still expected to act as a GM, not as a database waiting to be queried.

**Release:** v0.6 public-testing build.  
**Maturity:** experimental; not production-proven and not tested through 100 sessions.  
**Contents:** an unbound kit, no campaign world, and the `freeform` engine only.

Start with [QUICKSTART.md](QUICKSTART.md). For setup details, use [INSTALLATION.md](INSTALLATION.md). The short command list is [COMMANDS.md](COMMANDS.md).

Do not load this README during PLAY. It explains the project to people; it is not runtime context.

---

## What problem does it solve?

Long AI-run campaigns often break in two opposite ways:

1. **Amnesia:** a new chat forgets established details, relationships, resources, or unresolved consequences.
2. **Context overload:** keeping every transcript and lore file loaded makes old material too salient, encourages accidental spoilers, and consumes the context window.

An earlier RPG OS prototype solved much of the filing problem but revealed a third failure: the AI could become an excellent clerk and a passive GM. It would retrieve correctly, avoid invention, and wait for the player to supply every new situation.

v0.6 is a GM-first redesign. It keeps the persistence and retrieval discipline, but the runtime now begins from:

- where the campaign and current scene are;
- what the player intends;
- what the GM owes the table now;
- what established causes or accepted permissions allow;
- which facts or rules are actually needed.

Only then does it retrieve files.

The player should feel:

> *This is a GM who remembers.*

Not:

> *This is a database I must interrogate until it produces a scene.*

---

## The five ideas to understand

| Term | Meaning in ordinary language |
|---|---|
| **GM Core** | The runtime duties and limits: frame the situation, portray an autonomous world, judge consequences fairly, protect player authorship, and keep the campaign coherent |
| **Campaign Contract** | The run you explicitly accepted: its promise, fit envelope, direction, initiative, pressure/time handling, priorities, visible guidance, and any bounded proactive mandate |
| **Current Save** | The authoritative present: where and when the PC is, their current state, what just happened, and which established causes may still matter |
| **Bearing** | An optional, revisable note about what the campaign may be becoming; useful orientation, never canon or a queued plot |
| **PERSIST / REVIEW** | PERSIST records facts; REVIEW separately interprets the campaign without changing those facts |

### A few more terms

- **Bound / unbound:** an unbound kit has no campaign. A bound folder belongs to one accepted run.
- **PLAY:** fiction and adjudication. PLAY never writes files.
- **SETUP:** the New Game interview. Drafts are not canon until ACCEPT.
- **ADMIN:** explicit file-changing work such as CHECKPOINT, CLOSE, REVIEW, or RECALIBRATE.
- **Causal frontier:** the compact list of established consequences, due conditions, live processes, pending decisions, and narrow current-state cues that could matter next. The Current Save keeps explicitly declared PC goals and leftover PC time in separate fields. None of these is a list of planned scenes.
- **Cold file:** stored on disk but not normally loaded. Existence and retrieval do not grant narrative importance.
- **Warrant:** an independent reason a particular consequential development may occur, such as an established cause, due condition, player goal, explicit request, or authorized procedure.
- **Creative mandate:** an explicit Campaign Contract permission for proactive, campaign-consistent GM introductions at eligible boundaries. It permits; it never imposes a quota.

---

## What is in the folder?

RPG OS retains five storage areas:

| Area | Job |
|---|---|
| `OS/` | GM Core, authority, agency, safety, boot, and the cold task-first retrieval service |
| `ENGINE/` | Swappable resolution procedures and character-sheet requirements |
| `MODULES/` | Reusable world/genre/voice baselines and optional campaign capabilities |
| `INSTANCE/` | This run's Contract, Current Save, character/current-state records, corrections, safety, and optional Bearing |
| `ARCHIVE/` | Cold historical evidence and narrow routes to exact past details |

`ADMIN/` contains setup, loading, one-time v0.5 migration, persistence, review, recalibration, validation, and tests. `TOOLS/` contains the optional read-only structural validator.

This public repository contains **no setting, adventure, or campaign world**. Tellus and other authored campaigns are not included.

---

## How a campaign runs

### 1. Technical boot

Every new chat begins by opening exactly:

1. `OS/AGENTS.md`
2. `OS/BOOTSTRAP.md`
3. `OS/LAW.md`
4. `INSTANCE/CURRENT_SAVE.md`
5. `INSTANCE/CAMPAIGN_CONTRACT.md`

For a bound run, the loader then opens only required safety and voice material. It may load `INSTANCE/BEARING.md` if review is enabled and that Bearing was built from the current save and Contract. A stale or absent Bearing never blocks play.

The archive, rule bodies, world lore, rosters, clocks, private truth, and other large records remain cold until a specific GM task needs them.

### 2. New Game

`NEW GAME` is SETUP, not fiction. The AI asks one manageable cluster at a time about:

- engine;
- premise and campaign promise;
- narrative voice, tone, and unwanted patterns;
- safety boundaries before detailed drafting;
- Campaign Contract axes;
- optional world and campaign complexity;
- PC profile depth and an independent mechanical-sheet choice;
- the starting time, place, and playable situation.

You can build:

- a sparse freeform campaign with a short PC profile;
- a detailed mechanical character;
- a world with phases, clocks, institutions, resource rules, and private causality;
- or any smaller selection between those extremes.

“Detailed” means deeper only in the domains you chose. It does not authorize an encyclopedia, empty folder trees, a mass NPC roster, or a prewritten railroad.

The AI displays a manifest. Nothing becomes canon until you explicitly say `ACCEPT`.

### 3. PLAY: GM first, retrieval second

For each player declaration, the runtime:

1. orients to the campaign and current scene;
2. understands player intent;
3. identifies the GM task;
4. checks what is required or authorized;
5. retrieves facts or procedures sufficient and proportionate to that task;
6. imagines and judges;
7. portrays only the selected result;
8. returns agency or closes the beat.

This avoids both extremes:

- **clerk failure:** “nothing was prewritten, so nothing happens”;
- **railroad failure:** “this would fit the setting, so I will force it into play.”

A quiet evening may genuinely contain no incident. It must still provide orientation, ordinary function when appropriate, and a clean chance to continue or advance time. A busy thriller may move established processes aggressively when the accepted Contract calls for it. Neither style creates a mandatory dilemma quota.

### 4. PERSIST

PERSIST is the umbrella term for two commands:

| Command | Saves authoritative present | Saves exact historical evidence |
|---|---:|---:|
| `CHECKPOINT` | Yes | No |
| `CLOSE` | Yes | Yes, through indexed scene shards |

PERSIST records what became true and what accepted evidence was delivered. It cannot infer what the campaign “should” become, manufacture history, or save rejected ideas.

Do not discard a chat containing accepted play until CHECKPOINT or CLOSE confirms a new `save_id`.

### 5. REVIEW

REVIEW is separate from saving. After a successful PERSIST it may examine the accepted Contract, current state, prior Bearing, and narrowly selected evidence to ask:

- What has accumulated?
- Which consequences or player goals remain active?
- Is a recognizable pattern forming?
- Which directions weakened, contradicted themselves, or ended?
- Is “no stable pattern yet” the honest answer?

Its only durable output is the optional provisional Bearing. REVIEW cannot edit the Current Save, history, people, clocks, safety, or Contract. If REVIEW fails, the saved campaign remains valid and playable.

v0.6 ships **no durable GM-preparation bank**. Optional module seeds or possibilities may still exist as cold, nonauthoritative campaign material, but Bearing is not a hidden adventure queue. The GM may author a fresh realization when responsive duty, an external warrant, or the Contract's accepted creative mandate permits it; no prepared candidate is required.

### 6. END SESSION

`END SESSION` is the convenient normal sequence:

1. run CLOSE;
2. stop if CLOSE fails;
3. if CLOSE succeeds and the Contract uses `review_mode: bearing-only`, run REVIEW;
4. report the PERSIST and REVIEW results separately.

### 7. RECALIBRATE

Campaign preferences can change. `RECALIBRATE` drafts a prospective Contract change—for example, less pressure, more visible guidance, or a different GM-initiative setting. It applies only after explicit OOC acceptance, never rewrites earlier play, and makes older Bearing material stale.

### 8. Migrating a bound v0.5 campaign

`MIGRATE V0.5` is a one-time ADMIN conversion for an existing **bound** v0.5 campaign. It is not `LOAD MODULE`, a normal CHECKPOINT, or an automatic folder merge.

Work only on a byte-for-byte backup after all accepted play has been saved by the old v0.5 runtime. Selectively install the v0.6 program, contracts, schemas, and blank Campaign Contract/Bearing templates while preserving the campaign's MODULE, Current Save and other INSTANCE authorities, and ARCHIVE evidence. Install the v0.6 shipped Freeform adapter when applicable; preserve and separately review a custom adapter. Then use the complete five-file migration boot prompt in [INSTALLATION.md](INSTALLATION.md#upgrading-a-bound-v05-campaign); do not send the bare command by itself.

The migration asks for and displays the first complete v0.6 Campaign Contract and explicit values for `scene_status`, `uncommitted_time`, `pc_declared_goals`, and `causal_frontier`. It must not infer those values or reinterpret old play. On acceptance it creates checkpoint lineage from the old save, initializes a bound-empty Bearing, and publishes Current Save last. It does not reshard or rewrite the archive. See [INSTALLATION.md](INSTALLATION.md#upgrading-a-bound-v05-campaign) and [ADMIN/MIGRATE_V05.md](ADMIN/MIGRATE_V05.md).

---

## Player agency and world initiative

The player owns the PC's voluntary:

- actions and speech;
- thoughts and feelings;
- attraction and consent;
- commitments, purchases, risks, messages, and political or moral choices.

The GM owns:

- NPCs and institutions;
- the environment and calendar;
- consequences and established off-screen processes;
- framing, pacing, adjudication, and campaign stewardship.

Player-driven does not mean the player must invent the world for the GM. Established NPCs and processes may act without waiting for the player to type a verb. A new consequential situation may also be authored when an independent warrant or explicitly accepted creative mandate permits it.

But compatibility is not permission by itself. “An ambush could happen in this setting” does not mean an ambush is authorized here. A retrieved seed, candidate, NPC file, or clock never activates merely because it was opened.

Dice cannot create consent, love, friendship, ideological conversion, or the PC's will.

---

## Campaign complexity

Complex campaigns are supported without making complexity mandatory.

Optional systems may include:

- changing phases or operating conditions;
- causal clocks, fronts, pressures, and deadlines;
- autonomous people, factions, and institutions;
- calendars, travel, appointments, and selective time compression;
- public and private information;
- relationships with independently tracked dimensions;
- resources, money, equipment, status, and logistics;
- house-rule calibration and engine overrides;
- large worlds split into narrow, independently retrievable files.

These systems obey the same state lifecycle:

- stable definitions and T0 baselines belong in MODULE;
- changing authoritative state belongs in INSTANCE;
- due or operative facts reach the Current Save's causal frontier when established;
- archive evidence records what happened;
- REVIEW may interpret a pattern but cannot advance a clock.

Reading a clock does not tick it. Ending a session does not tick it unless an accepted causal rule specifically makes that event a trigger. A phase describes changed conditions, not a compulsory story chapter.

---

## Engines

The OS is not GURPS, D&D, or any other ruleset. ENGINE is a swappable service.

The public v0.6 kit bundles only **Freeform**, which uses fictional positioning and transparent GM judgment rather than a full numerical system.

You may create a compact local adapter for a system you own or are entitled to use—for example GURPS, Dungeons & Dragons, Pathfinder, Call of Cthulhu, Fate, Savage Worlds, or your own design. These are examples of possible local engines, not bundled content, endorsements, or claims of affiliation.

An engine adapter should contain only the minimum operating procedure and sheet fields needed for play. Do not ask the AI to reconstruct, copy, or redistribute a copyrighted rulebook. You still need lawful access to and knowledge of the game you use.

Narrative flavor is not an engine override. A real change to resolution belongs in the ENGINE layer; campaign-specific presentation belongs in policy; later rulings belong in INSTANCE corrections.

---

## Retrieval locality and archives

The filesystem may be large. Active context should not be.

RPG OS uses:

```text
large domain -> compact index -> narrow authoritative record
```

Indexes answer “where should I look?” They do not duplicate the world, make their contents important, or authorize an encounter. Files split when their parts are normally needed independently—not merely when they cross a word count.

CLOSE archives accepted play as semantic scene shards with compact indexes and stable heading identifiers. A precise question can follow a ledger or index to one source heading instead of loading a whole campaign chronicle.

Archive is evidence, not the living present. Reading that someone “might call” in an old record does not make the call happen.

---

## Strengths

- **Fresh-chat continuity by design:** the authoritative present lives outside the conversation and can be tested on each host.
- **GM-first orientation:** campaign and intent come before repository navigation.
- **Separation of truth and interpretation:** Current Save is canon; Bearing is provisional.
- **Failure isolation:** REVIEW can fail without damaging a valid save.
- **Player authorship:** PC interiority and voluntary decisions have explicit ownership.
- **Autonomous world:** NPCs, institutions, time, and established processes need not wait to be poked.
- **No preparation entitlement:** stored, retrieved, or fitting material is not automatically activated.
- **Task-first retrieval:** exact facts and rules are fetched only when the GM work requires them.
- **Retrieval locality:** large lore and archives remain addressable without becoming resident.
- **Swappable rules:** Freeform ships; lawful local engines can be added.
- **Human-readable persistence:** Markdown can be inspected, backed up, diffed, and version-controlled.
- **Structural tooling:** deterministic format and route defects can be checked separately from narrative quality.

---

## Weaknesses and honest limits

- **Instruction enforcement, not hard isolation.** On a normal host, one model context interprets the rules, reads files, judges, and narrates. It can still misunderstand, rationalize, leak filenames, or expose rejected material.
- **No recovery of unsaved chat.** If the chat disappears before CHECKPOINT or CLOSE, RPG OS cannot reconstruct the missing accepted play.
- **Non-atomic multi-file writes.** Writing Current Save last protects the main pointer, but an interrupted update may leave another INSTANCE or ARCHIVE file changed. Inspect or restore from backup before resuming.
- **Host dependence.** Folder reads, durable writes, range/section behavior, and tool access vary. A model name or paid tier does not guarantee compatibility.
- **Privacy is not guaranteed.** “PRIVATE” is an instruction and storage convention, not encryption or proof that a host did not ingest the file.
- **Provider policy and account risk.** The OS cannot override content policies, moderation, terms, or account enforcement. Fictional or historical context is not a guarantee of acceptance. Do not bypass safeguards; change the material or use a lawful local/offline environment that permits it.
- **Administrative work remains.** PLAY does not write. The user must run PERSIST, protect backups, and handle interrupted writes honestly.
- **Structural validation is limited.** A passing script cannot prove good GMing, consent compliance, semantic fidelity, host persistence, or future behavior.
- **Scale is unproven.** v0.6 has not demonstrated a 20-session or Session-100 campaign under this new architecture.
- **No dedicated UI.** There is no map, character-sheet application, automated dice panel, or vector database.

If saving files feels like too much overhead, this prototype may not suit you yet. If long-chat amnesia and lore saturation are the bigger problems, it may be worth testing.

---

## Validation and evidence

`VALIDATE` runs a read-only structural diagnostic. With code execution, `TOOLS/validate.py` can check declared deterministic file invariants. Without code execution, a model inspection must label itself `MODEL-CHECKED` and disclose exactly what it examined.

Keep four kinds of evidence separate:

1. **STRUCTURAL:** mechanically checked paths, formats, identities, and references.
2. **HOST OBSERVATION:** what one host/model/tool setup did at one time.
3. **SEMANTIC:** human/model judgment about agency, warrants, archive fidelity, or GM behavior.
4. **PLAYER-RATED:** whether the campaign actually felt coherent, alive, fair, and easy enough to operate.

Do not average a clean filesystem into a claim of good play.

The packaged v0.6 release tree is required to pass its shipped structural validator before publication. Re-run it after extraction or modification, use [ADMIN/TESTS.md](ADMIN/TESTS.md) for the broader fixtures, and report the actual result; a release-time pass is not a guarantee about a changed copy or future play.

---

## Folder map

```text
RPG_OS/
  OS/           GM Core, loader, boot, and cold retrieval service
  ENGINE/       engine contract and bundled freeform engine
  MODULES/      module contract; no campaign world in the public kit
  INSTANCE/     Campaign Contract, Current Save, optional Bearing, live records
  ARCHIVE/      historical schema, indexes, ledgers, and later scene shards
  ADMIN/        New Game, Load, Migrate, Persist, Review, Recalibrate, Validate, tests
  TOOLS/        read-only structural validator
  README.md     project overview
  QUICKSTART.md shortest route to play
  INSTALLATION.md host setup and preflight
  COMMANDS.md   command cheatsheet
  ARCHITECTURE.md design and authority boundaries
  CHANGELOG.md  version history
  CONTRIBUTING.md reports and pull requests
  SHARE.md      short public smoke test
```

---

## Documentation map

| File | Read it for |
|---|---|
| [QUICKSTART.md](QUICKSTART.md) | Shortest path from download to play |
| [INSTALLATION.md](INSTALLATION.md) | Host requirements, extraction, boot, validation, and write tests |
| [COMMANDS.md](COMMANDS.md) | Operator command reference |
| [ADMIN/MIGRATE_V05.md](ADMIN/MIGRATE_V05.md) | One-time bound v0.5→v0.6 migration contract |
| [ARCHITECTURE.md](ARCHITECTURE.md) | GM-first design, authority separation, retrieval, and limitations |
| [ADMIN/TESTS.md](ADMIN/TESTS.md) | Canonical structural and semantic pass/fail fixtures |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Reproducible reports and pull requests |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

Public guides summarize the runtime. If wording conflicts, `OS/`, the relevant `_CONTRACT.md` or `_SCHEMA.md`, and the applicable `ADMIN/` contract are authoritative.

---

## Project status and version history

v0.6 is the first GM-first implementation:

- a separately authoritative run Campaign Contract;
- an orienting Current Save with a causal frontier;
- optional noncanonical Bearing;
- PERSIST and REVIEW as separate operations;
- RECALIBRATE and END SESSION;
- explicit, fail-closed migration of backed-up bound v0.5 campaigns;
- task-first retrieval;
- no durable preparation subsystem.

v0.5 remains the important memory-and-integrity prototype from which this redesign grew. Earlier releases introduced structural validation, scene-sharded archives, retrieval locality, provider-risk warnings, lifecycle safeguards, and the original file-native separation.

See [CHANGELOG.md](CHANGELOG.md) for details.

---

## Credits and method

Project author and maintainer: [`croatianrdy2defend-create`](https://github.com/croatianrdy2defend-create).

RPG OS was developed through iterative campaign testing and adversarial multi-model review. A compiler, auditor, semantic critic, and runtime GM need not be the same model. The Markdown must work without the original design conversation.

---

## License and third-party material

Except where noted, original Markdown documentation and protocol material is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE).

`TOOLS/validate.py` and repository automation/configuration are licensed under the [MIT License](TOOLS/LICENSE).

Preferred attribution: “RPG OS” by `croatianrdy2defend-create`, <https://github.com/croatianrdy2defend-create/RPG-OS>. Indicate if you modified the material.

These licenses cover only material the project is entitled to license. They do not grant rights in third-party games, rules, trademarks, settings, artwork, or user-created campaign content. The public package ships no third-party ruleset adapter.

---

## Start

Open [QUICKSTART.md](QUICKSTART.md), make a backup, attach the folder, boot the five runtime files, run `NEW GAME`, review the manifest, `ACCEPT`, and begin PLAY in a fresh chat.
