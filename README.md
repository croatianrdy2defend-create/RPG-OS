# RPG OS v0.5 — Universal Campaign Operating System

[![Structural validation](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/validate.yml/badge.svg)](https://github.com/croatianrdy2defend-create/RPG-OS/actions/workflows/validate.yml)
[![Documentation: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey.svg)](LICENSE)

**Release:** v0.5 public testing. **Maturity:** file-native prototype; initial lifecycle validated, not Session-100-proven. This release retains hierarchical scene-sharded archives and the cross-domain retrieval-locality doctrine, adds optional guided character and complex-campaign construction, and includes an executable read-only structural validator with explicit evidence boundaries. **LAW is frozen.** It is not a video game, virtual tabletop, or product of any RPG publisher.

**Start here:** [`QUICKSTART.md`](QUICKSTART.md) · [`INSTALLATION.md`](INSTALLATION.md) · [`COMMANDS.md`](COMMANDS.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`CHANGELOG.md`](CHANGELOG.md)

Do not load this whole README during PLAY. It is the public project overview, not resident campaign context.

---

## 1. What this is

RPG OS is a **file-native operating system for solo tabletop play with a large language model as GM**.

The campaign does not live in the chat. The chat is a disposable working set. Persistence is a folder of Markdown files.

Four layers:

| Layer | Job | Swappable? |
|---|---|---|
| **OS** | How an LLM is allowed to run any campaign: agency, retrieval, privacy, PLAY vs ADMIN, situation-before-fiction | No. Frozen kernel (`OS/LAW.md`). |
| **ENGINE** | How uncertainty is resolved: dice, moves, an oracle, or freeform judgment | Yes. Plugin under `ENGINE/`. |
| **MODULE** | What world this is: voice, tone, PC baseline, lore, optional PEOPLE/WORLD/SEEDS | Yes. Born via New Game or loaded. |
| **INSTANCE** | This particular run: compiled present + cold archive | Yes. One module can seed separate runs, each in its own folder copy. |

Resident PLAY payload after boot is **two files only**:

1. `OS/LAW.md` — immutable execution law
2. `INSTANCE/CURRENT_SAVE.md` — compiled present (this kit ships **unbound**)

Everything else is retrieved only when the *immediate* moment causally requires it.

This public kit contains **no campaign world**. Every setting is a client of the contract, not part of the OS. You create a world with **New Game**.

---

## 2. Purpose

The purpose is to keep a **long, detailed persistent world** without stuffing that world into the model's context window.

Typical LLM campaigns fail because:

- the adventure lives in an infinitely scrolling chat
- the model forgets Tuesday and invents a quest on Wednesday
- NPCs decide what the player character feels
- one name lookup dumps the entire relationship basement
- a new conversation is amnesia
- “being helpful” fills blanks, completes schemas, and manufactures drama

RPG OS attacks those failure modes directly:

- **Files are the disk. Chat is RAM.** Killing the thread is a feature if ADMIN compiled the save.
- **Minimum necessary retrieval.** Zero extra files is valid. A retrieved bakery is not an encounter table.
- **Retrieval locality.** Large domains expose compact indexes that route to independently useful authoritative records; the filesystem may be huge while the active context stays small.
- **Player agency is law**, not a vibe. The GM does not author voluntary PC thoughts, attraction, consent, purchases, or first acts.
- **Quiet days are legal.** Seeds are possibilities, not obligations.
- **Archive is evidence**, not the living world. Exact SMS or an intimate scene can be recalled in session 15 *if* the present moment makes that recall causal. Sharing coffee with that person later does not reload the night.
- **Any ruleset is a plugin.** Freeform is bundled. Other systems can be represented by compact local engine files at New Game — procedure + sheet fields, never a redistributed or reconstructed rulebook.
- **Complexity is opt-in by domain.** Sparse campaigns and minimal PC baselines are valid. Detailed campaigns may add phases, causal clocks, institutions, private causality, resources, or house-rule calibration without putting those bodies into resident PLAY context.

The success criterion is **not** “can an LLM GM a session.” It is: **can Session 2 continue in a fresh chat from LAW + CURRENT_SAVE only, and can one exact old fact be retrieved without hauling the basement into the room?**

That test (fresh-chat resume + needle) has been run on one accepted play slice. The long-campaign claim remains deliberately unproven.

---

## 3. Origin and method

RPG OS grew out of a detailed solo campaign whose world lore, rules, current state, private causality, and archive had become entangled. The redesign separated those concerns into OS, ENGINE, MODULE, and INSTANCE; then tested unbound refusal, SETUP-versus-PLAY separation, one accepted play slice, CHECKPOINT/CLOSE, fresh-chat resume, and one narrow historical retrieval.

Later releases closed cross-file authority gaps, made archives retrieval-local, added a read-only structural validator, and introduced optional character and complex-campaign builders. Multiple models served as compiler, auditor, and adversarial reviewer so the published Markdown would have to work without the original conversation.

Early internal prototypes used a compact GURPS adapter while proving engine separation. The public v0.5 repository does **not** distribute that adapter or any campaign world; it ships Freeform and the generic contract for lawful local engines.

See [CHANGELOG.md](CHANGELOG.md) for the full design and release history.

## 4. What we chose *not* to be

- Not a dedicated app with SQLite, embeddings, and a custom NPC simulator (those exist; this is Markdown + an LLM with a folder).
- Not “one long chat plus Memory Bank.”
- Not event-sourcing in PLAY (replaying a chronicle recreates the bloat problem). ADMIN writes history; PLAY reads a compiled snapshot.
- Not a setting-specific rules prompt with configurable lore. If one module's voice or assumptions survive into another, MODULE has leaked into OS.
- Not legally a replacement for owning your rulebooks. Engine files are procedures.

---

## 5. How it works

### 5.1 Operational modes

```
BOOT  →  SETUP (New Game)  →  ADMIN commit  →  PLAY  →  CHECKPOINT / CLOSE  →  fresh PLAY chat
              \                 LOAD MODULE ↗
```

| Mode | May | May not |
|---|---|---|
| **BOOT** | Confirm ready | Invent a world |
| **SETUP** | Ask, draft, show samples | Narrate a scene, write canon, play NPCs |
| **ADMIN** | Write files, compile save, archive | Speak as fiction |
| **PLAY** | Fiction + public footer | Write files |

SETUP may create possibilities. PLAY produces candidate events. ADMIN persists accepted history and canon.

### 5.2 Boot (every new chat)

Attach **only** this `RPG_OS` folder. First message: open four paths, do not list the repo:

- `OS/AGENTS.md`
- `OS/BOOTSTRAP.md`
- `OS/LAW.md`
- `INSTANCE/CURRENT_SAVE.md`

If unbound: ready only. “Begin play” and “just improvise” must fail closed.

If bound: establish `CURRENT_SAVE` immediate scene, retrieve POLICY voice (and POLICY safety extras, SAFETY.md only if `safety_state` is `active`), hand back before the first voluntary PC act.

### 5.3 New Game

Interview, one cluster at a time:

1. Rules engine (list installed when scalar front matter has exact `class: engine` and `id` matches the flat filename stem or the containing directory name for `<id>/ENGINE.md`; skip aliases/pointers). Draft a compact engine if missing.
2. Title and premise
3. Narrative voice (required; OS does not pick close-third)
4. Tone and cadence
5. Anti-attractors
6. Extra safety → `INSTANCE/SAFETY.md` + flag, before detailed drafting
7. World/campaign depth — Sparse, Focused, Detailed, or Custom. Detailed means deeper only in selected domains.
8. PC concept plus two independent choices: Quick/Standard/Detailed/Custom profile depth, and No full sheet/Minimum required/Guided full sheet/Import mechanical path. A completed sheet is optional.
9. T0 time/place plus dependency and interaction audits where needed
10. **Starting scenario** — 2–3 live hooks; pick one. No idle “you stand in front of the house.” No authored first PC act. No smuggled “you already agreed.”
11. Optional capabilities only if a real body and route will exist
12. Manifest → explicit ACCEPT → validation checklist (`MODULES/_CONTRACT.md`, `ENGINE/_CONTRACT.md`, `INSTANCE/_SCHEMA.md`) → bind

Focused/Detailed/Custom world construction uses `ADMIN/CAMPAIGN_BUILD.md`. Character construction uses `ADMIN/CHARACTER_BUILD.md`. Both are SETUP-only and conditional; neither becomes resident PLAY context.

The campaign builder can model an emergent sandbox, episodes, a broad phase trajectory, causal clocks/fronts, autonomous factions or institutions, inactive possibilities, multidimensional relationships, selective/exact resources, bounded private-truth modes, and compact house-rule calibration. Each is optional. Complex interactions receive an explicit cause/update-order audit; private systems that remain independently live across fresh boot receive a minimal non-revelatory watch cue only when needed, updated or demoted at explicit saves.

If CURRENT_SAVE is already bound, New Game and LOAD **stop**. Use a separate folder for a second run.

At bind: copy the exact PC body/routed bundle to `INSTANCE/CHAR/`, with `PC.md` as the stable entrypoint. MODULE stays the immutable baseline.

Then: **new chat** to play. Do not continue in the questionnaire.

### 5.4 PLAY retrieval

Open the **smallest sufficient set**. Default extra files: zero.

A retrieved fact gains **no** narrative weight. Location ≠ roster. One name ≠ the relation ledger. Quiet Tuesday stays quiet.

A tool may return a whole file. Treat only the addressed section as in play and discard the rest. That **mitigates**; it does not isolate tokens. If PRIVATE leaks, split the file physically. That is the escape hatch.

#### Retrieval locality

Persistent information should be addressable at approximately the granularity at which it is normally needed:

```text
large domain → compact routing index → narrow authoritative record
```

This can apply recursively to world lore, locations, institutions, mature NPCs, INSTANCE registers, engine extensions, equipment, or private material. A declared capability entrypoint may be the body itself while small, then remain as a compact index if independent retrieval later justifies splitting.

Split by relevance, not a token threshold. A long cohesive file may be correct; a shorter file containing unrelated subjects may be wrong. Do not prebuild empty hierarchies. Indexes answer “where should I look?”, do not duplicate the bodies, and do not authorize repository-wide discovery. Explicit cross-links are routes, not automatic relevance.

### 5.5 CHECKPOINT vs CLOSE

| | CHECKPOINT | CLOSE |
|---|---|---|
| Present (time, place, resources, pending act) | Yes — this **is** a real save of the present | Yes |
| Exact wording, scene evidence, ledgers | No | Yes |
| Write order | Candidate + plan → preflight → selected INSTANCE bodies → assembled-state check → CURRENT_SAVE last | Candidate + plan → preflight → selected INSTANCE bodies → archive shards/indexes/ledgers → assembled-state check → CURRENT_SAVE last |
| `commit_kind` | `checkpoint` | `close` |

Do not leave until ADMIN prints the new `save_id`. Next session is a **new chat**. The save is memory.

### 5.6 Archive (cold)

```
ARCHIVE/
  _SCHEMA.md            hierarchical-scene-v1 contract
  INDEX.md              sparse campaign-level router
  MESSAGES_LEDGER.md    pointer to one exact-message heading
  RELATION_LEDGER.md    pointer to one relationship-scene heading
  sessions/sNN-dXX/
    INDEX.md             compact routes for this closed slice
    01_<scene>.md        detailed historical evidence
    02_<scene>.md        another independently retrievable event
```

The archive compresses routing, not evidence. Scene shards preserve detailed accepted play; indexes only locate it. For an exact-detail question: campaign INDEX if the session is unknown → session INDEX → one shard/heading. If a trusted pointer already identifies the shard, skip the indexes. Stop when the evidence is sufficient.

Indexes may answer a simple unambiguous existence fact. Exact wording, rolls, quantities, sequence, subtle relationship context, or disputed history must come from the source shard. Retrieval breadth follows question breadth.

Pre-v0.3.2 DELTA/TRANSCRIPT/MESSAGES archives remain valid. They need not be migrated. Optional migration is partition + index, never rewrite + reinterpret.

Needle: ledger or index → one source heading. Not the whole basement. Sharing bread with someone in session 15 does not load session 1’s intimate scene. Recalling exact embodied detail is legal only when that person is present, the topic arose, or the player invited it. Reading “might happen” in an old shard never makes it happen.

### 5.7 Authority (when files disagree)

1. LAW
2. Explicit player rulings (including active SAFETY.md)
3. Accepted saved play compiled into CURRENT_SAVE
4. CURRENT_SAVE
5. ENGINE + instance PC sheet
6. MODULE baseline
7. Private records, only if causally required
8. ARCHIVE (historical, not automatically present)

Never disguise a contradiction as an in-world twist.

### 5.8 Agency (non-negotiable)

The player owns voluntary PC: actions, words, thoughts, emotions, attraction, consent, purchases, risks, commitments, messages, weapon handling.

The GM owns NPCs, world, camera, calendar, consequences, private causality.

Dice cannot manufacture consent or relationships. They may resolve situational cooperation inside existing NPC boundaries.

Sexual/erotic content: adults only. Ordinary children may exist in the world. The player may pause, veil, rewind without in-character penalty. MODULE may be stricter, never weaker.

### 5.9 Operator commands (out of character)

- `AUDIT` — files opened on the previous non-AUDIT turn, reasons, whether find/ls ran. No bodies.
- `VALIDATE` — read-only ADMIN structural diagnostic. Prefer the shipped script; no-code inspection cannot certify the tree and is incomplete unless it finds a definite failure. It writes no certificate or campaign state.
- `CHECKPOINT` — save present.
- `CLOSE` — save present + archive.
- Unsent UI suggested-reply chips are **not** player input.

---

## 6. Folder map

```
RPG_OS/
  OS/           LAW, BOOTSTRAP, AGENTS          (kernel)
  ENGINE/       _CONTRACT, freeform             (plugins)
  MODULES/      _CONTRACT                       (empty until New Game)
  INSTANCE/     CURRENT_SAVE, registers, CHAR/, PEOPLE/, SAFETY
  ARCHIVE/      _SCHEMA, campaign INDEX, ledgers, session indexes/shards
  ADMIN/        NEW_GAME, CHARACTER_BUILD, CAMPAIGN_BUILD, LOAD, CLOSE, VALIDATE, TESTS, ADD_ENGINE
  TOOLS/        dependency-free read-only structural validator
  QUICKSTART.md INSTALLATION.md COMMANDS.md README.md SHARE.md ARCHITECTURE.md
  CHANGELOG.md CONTRIBUTING.md LICENSE .github/
```

Do not edit `OS/LAW.md` for house rules. POLICY owns voice/cadence/boundaries; RULES_HOOKS may calibrate but not contradict ENGINE; a real mechanical override uses a distinct compact ENGINE id; later table rulings go in INSTANCE/CORRECTIONS.

---

## 7. Strengths

- **Persistence outside chat.** The interesting claim is fresh-resume-shaped: new conversation, same minute, one cold fact on demand.
- **Salience control.** Most AI-GM projects add memory. This one subtracts it until needed.
- **Retrieval locality.** Broad categories no longer imply broad reads; stable entrypoints route to the independently relevant authority.
- **Checkable agency.** Authorship is an enumerated list, not “be a good GM.”
- **Fail closed.** Unbound boot invents nothing. Missing voice is not runnable. Missing capability is absent, not faked.
- **Modular boundary** forces honesty: genre, voice, and campaign-specific assumptions belong in MODULE/POLICY, not LAW. Different modules should feel genuinely different under the same OS.
- **Exact recall without a fat prompt** via campaign routing, session indexes, scene shards, ledgers, and stable heading ids.
- **Promotion/demotion** stops every bartender from becoming sticky.
- **Portable Markdown.** You can read the save. You can grep it. You can keep it offline.
- **Mechanical checks where judgment is unnecessary.** VALIDATE can catch broken identities, paths, PC route graphs/copies, archive pointers, save grammar, stale candidates, and initial-state contamination without claiming to assess story quality or every interrupted transaction.
- **Honest labeling.** v0.5 is ready for public testing, not proof of a 100-session campaign. Known failure modes are listed.
- **Cross-model compilation procedure.** One model writes; another boots. Markdown must not depend on the compiler’s private dialect.

---

## 8. Weaknesses and known limits

- **Narrative enforcement is prose.** VALIDATE checks deterministic structure only. It cannot prove that PLAY stayed read-only, a shard is coherent, history came only from accepted play, or agency was honored. Reliability still depends on model instruction-following plus operator discipline. AUDIT is useful self-report, not independent ground truth.
- **You must close.** Skip ADMIN compile and you have chat amnesia. CHECKPOINT is a real present-save; CLOSE is required for exact wording.
- **Platform fragility.** Needs a host/model combination that can read and persistently write a project folder. A naked chat will not do this. Product names and subscription tiers do not prove capability: P17/P18 decide. If the host changes folder behavior, fresh-chat resume can fail.
- **Provider policy and account risk.** RPG OS does not override the host's terms, moderation systems, or changing content policies. Campaign material may be refused or interrupted, and material violating provider rules may lead to account restrictions or termination. Fictional, historical, private, or roleplaying context is not a guarantee of acceptance. Keep the canonical campaign folder and regular backups outside the provider. For material a cloud provider does not permit, change the material or use a lawful local/offline model; do not attempt to bypass provider safeguards.
- **Whole-file injection.** Many hosts cannot range-read a heading. Unused tokens can still affect salience. Scene shards reduce the damage but do not prove isolation; split PRIVATE physically if tests leak. Heading-only quotes **cannot prove isolation** (P17).
- **Write capability is not guaranteed** until P18: CHECKPOINT then a new chat must show the new `save_id`.
- **Multi-file commits are not filesystem-atomic in v0.5.** CURRENT_SAVE-last protects the live save pointer, but an interruption after a separate INSTANCE body was overwritten can still require inspection or restoration. Keep an offline backup before ADMIN writes and do not resume after an interrupted CHECKPOINT/CLOSE until P19 consistency is restored. A versioned immutable state-manifest is a possible later structural solution, not a capability this release claims.
- **Friction.** The operator becomes a part-time registrar. That tax is intentional: reducing it without equivalent safeguards can reintroduce drift, invented hooks, and incomplete saves.
- **Suggested-reply chips** in some UIs are attractors. Ignore them.
- **Filenames can bleed into prose.** Treat that as a runtime defect and report it.
- **Copyright.** Engine drafts must stay procedures. You still need to know/own your system.
- **One validated morning**, then architecture work. Not dozens of sessions, not a large archive under load, not Session 100. The architecture *predicts* a small PLAY working set over a huge archive. That is unproven at scale.
- **No map UI, no automated dice window, no vector database.**
- **Models may overuse `find`/`ls`.** Test 0 fails if they explore the repository instead of following explicit routes.

If that chore list is a deal-breaker, this kit is not for you yet. If forgetting Tuesday is the deal-breaker, it might be.

---

## 9. What “ready” means

**READY WITH MINOR CHANGES** (v0.2 audit) meant:

- structural P0 blockers closed (engine identity, commit order, bound-run protection, capability honesty, SAFETY load graph, overlays, retrieval budget, archive needles, compilation matrix, AUDIT window)
- remaining issues are tester/platform detection, not authority or campaign-state holes
- LAW was not edited to get there

It does **not** mean:

- Session 100
- every model will obey
- physical privacy isolation
- any campaign world is included
- an authored module should be regenerated with New Game rather than **LOAD**ed in a clean instance

v0.5 is the **final-for-testing** build of this design pass: its declared deterministic structure is script-checkable, while the remaining campaign-scale claims must be established through use. “Final for testing” is not “production proven.”

---

## 10. How to test (short)

See `ADMIN/TESTS.md` for pass/fail lines.

Minimum public path:

1. Four-file boot → ready, unbound
2. `VALIDATE` → SCRIPT-VERIFIED structural result if code runs; otherwise an honest MODEL-CHECKED `INCOMPLETE` or definite observed `FAIL`
3. `Begin play` / `Just improvise` → refuse
4. `New game` → SETUP only; starting scenario; ACCEPT; bind
   - Test both Sparse + Quick profile + deferred sheet, and a selected Detailed campaign/profile + guided full-sheet path.
5. Fresh chat → opening situation, handback
6. Play a slice → CHECKPOINT → CLOSE into a session index plus scene shards
7. Fresh chat → same present
8. Ask one archived exact wording → one heading
9. `AUDIT` when retrieval feels fat

Useful bug reports: a forced sheet or encyclopedia; guessed PC values/persona; a phase treated as a mission list; a clock advanced without cause; duplicate resource totals; an engine override hidden in RULES_HOOKS; invented quest on a quiet day; GM chose PC feelings; new chat forgot the save; whole archive dumped for one name; LOAD wiped a live run; SAFETY quoted by an NPC.

---

## 11. Release history

v0.5 adds optional character construction, selective complex-campaign machinery, and the full T0-to-live persistence lifecycle on top of v0.4 validation and v0.3.2 retrieval-local archives. The public GitHub package ships Freeform and generic local-engine support only.

See [`CHANGELOG.md`](CHANGELOG.md) for the complete version-by-version history.

## 12. Documentation map

| File | Use it for |
|---|---|
| [`QUICKSTART.md`](QUICKSTART.md) | The shortest path from download to first scene |
| [`INSTALLATION.md`](INSTALLATION.md) | Extraction, host requirements, validation, and persistence preflight |
| [`COMMANDS.md`](COMMANDS.md) | Human-facing command cheatsheet |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Layer boundaries, retrieval locality, and validation limits |
| [`ADMIN/TESTS.md`](ADMIN/TESTS.md) | Canonical adversarial pass/fail suite |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Bug reports, test evidence, and pull requests |
| [`CHANGELOG.md`](CHANGELOG.md) | Complete prototype and release history |

Runtime authority remains in `OS/`, the relevant `_CONTRACT.md` / `_SCHEMA.md`, and `ADMIN/`; these public-facing guides summarize those files.

## 13. Credits and method

Project author and maintainer: [`croatianrdy2defend-create`](https://github.com/croatianrdy2defend-create).

Designed through a multi-model workflow (Grok as file compiler, ChatGPT/Sol MAX as cross-file auditor, Claude as adversarial tester/UX reviewer). Compiler ≠ runtime GM. A change set should be booted by a model that did not write it.

For architectural compatibility, derivatives are encouraged to retain the four-layer names and keep campaign-specific material out of the kernel.

---

## 14. License and third-party material

Except where noted, the original Markdown documentation and protocol material is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE).

`TOOLS/validate.py` and repository configuration/automation are licensed under the [MIT License](TOOLS/LICENSE).

Preferred attribution: “RPG OS” by `croatianrdy2defend-create`, <https://github.com/croatianrdy2defend-create/RPG-OS>. Indicate if you changed the material.

These licenses grant rights only in material the project is entitled to license. They do not grant rights in third-party rules, names, or trademarks, and they do not claim ownership of campaign content later created by users. The public package ships no third-party ruleset adapter or campaign world. Do not paste or redistribute copyrighted rulebooks through `ENGINE/`.

---

## 15. Immediate next step

Open `QUICKSTART.md`. Attach this folder. Four files. Ready. Validate. New Game. Accept. New chat. Play. Close.
