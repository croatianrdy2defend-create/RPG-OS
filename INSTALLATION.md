# Installation and portability — v0.9.6 experimental

## A new campaign

Download the [v0.9.6 release](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v0.9.6), extract its package into a dedicated campaign folder and make it available to your LLM. Use one active campaign per copy. Start from [Quick start](QUICKSTART.md). The release contains blank, unbound templates and only Freeform as a selectable engine; it carries no campaign module, character or artwork. The shared encounter helper is an optional procedure, not another engine. Earlier versions remain on the [published releases page](https://github.com/croatianrdy2defend-create/RPG-OS/releases).

The normal workflow requires the host to read named files, create and replace ordinary files, preserve them between chats, and let the model inspect what it wrote. An attachment may be readable without being writable. Establish the actual available operations during setup; use the export workflow below when needed. No paid API, background service or required script is part of the design. Smaller reference files help hosts that can only read entire files.

Do not begin from a folder containing another campaign's INSTANCE, ARCHIVE, or pending RECOVERY/HANDOVER state. Keep that campaign in its own copy.

## State, randomness and practical visibility

The agent-state procedure uses existing records for entity-appropriate nature/capabilities, control, information, applicable aims/drives/directives, circumstances and relationships where they exist. Setup can establish the small private opening basis under the accepted authoring scope. During ordinary play, newly established facts and changes remain unsaved in the conversation until an authorized save. Installing v0.9.6 alone does not enable autosave or create an invisible memory service.

The optional [announced autosave policy](ADMIN/AUTOSAVE.md) must be explicitly selected. It invokes the same protected complete-present CHECKPOINT after advance notice; no daemon or mandatory script is required. TOOLS/autosave.py is an optional read-only scheduling helper, not a saver. Context-pressure triggers require actual model-visible telemetry or an operator report. A visible UI meter does not prove the model can read it, and no fixed percentage guarantees enough capacity for a complete save.

When a selected procedure requires randomness, use an actual available randomizer or player-supplied input with agreed outcome meanings. If neither is available, settle an explicit judgment alternative or keep that resolution pending. Freeform judgment is a valid default; fabricated dice are not a substitute for the requested method. Merely supplying a seed does not define a reproducible generator without its procedure and inputs.

The optional [shared encounter generator](ENGINE/_shared/ENCOUNTER_GENERATION.md) requires selection by a compatible bound engine and the accepted agreement. MODULE supplies world facts and source bindings; ENGINE owns the chosen mechanics. Eligible condition, interpersonal appraisal and overall attraction each use an independent 2d6 direction/intensity band, after which the GM establishes the concrete value before behavior. At most three determinations use six independent faces. Priorities and constraints, factual perception, sourced nonsocial responses and derived engagement add no draws. See the [full explanation](MECHANICS.md#optional-encounter-generation-direction-then-concrete-state). Installing v0.9.6 does not select this helper or replace an existing generation method.

Current agent guidance establishes a compact five-field temporary basis before individual participation, appraisal or initiative. Visual focus alone retrieves required portrayal guidance without initializing an unaware actor. Supported nature, control, information and capabilities remain governing inputs. Retain active state through attention gaps; update relevant changes, then release inconsequential temporary state when participation genuinely ends. Keep consequential facts and unresolved matters; later incidental contact may receive fresh temporary values under the accepted method. Applicable attraction includes attraction, no particular attraction and aversion within its supported domain; duty or relationship status does not make it inapplicable. A nonhuman mechanism uses its actual capacities, rather than treating hunger or chemical response as interpersonal attraction. An unavailable required active fact is a source gap, not expiry. PC interpretation cannot establish private nature or retrofit a hidden past. See [Independent agent state](OS/AGENT_STATE.md).

The simple standing fallback from v0.8.1 remains available for eligible unauthored outcomes with insufficient basis for grounded judgment: one actual d6, 1–3 No and 4–6 Yes. Select it once in the accepted setup proposal or request its prospective adoption through [Recalibrate](ADMIN/RECALIBRATE.md). Established facts, applicable rules and other selected methods come first; selection removes the need for per-roll permission. Installing the program alone preserves an existing diceless agreement or another selected oracle. See the [fallback examples](MECHANICS.md#random-fallback-for-unresolved-outcomes).

Private records provide practical spoiler separation, not encryption. Tool arguments, results or writes may be visible to the operator. If a selected method depends on concealment, check with a harmless synthetic secret and explain the actual limitation. Do not expose a real plot fact to test the interface. A collapsed panel or a file named "private" does not establish secrecy.

Recheck only affected capabilities when moving hosts. A host change does not authorize regenerating recorded people or changing rules.

## Existing campaigns

**Never install blank INSTANCE or ARCHIVE templates over a campaign.**

1. Complete the latest save using the old compatible runtime. Finish or reconcile pending recovery and scene transfers before changing their dependencies.
2. Keep a restorable copy of the entire campaign and its original runtime. Create a separate upgrade copy.
3. Give the GM the v0.9.6 kit as the update source and say: "Open ADMIN/UPGRADE_V08.md from the new kit and prepare this campaign's upgrade in the separate copy."
4. Review the actual program-file change set and any material compatibility question. Preserve campaign-owned modules, engine adapters, instance records, archives, local modifications and recovery evidence as the procedure specifies.
5. Apply the authorized update with recovery protection and readback. Resume from the preserved save after verification.

Valid v0.7.3, v0.8.0, v0.8.1, v0.8.2, v0.9.0, v0.9.1, v0.9.2, v0.9.3 and v0.9.4 records retain their core metadata, fictional sections and save identities. The upgrade consolidates general operating guidance; it does not resample NPCs, rewrite historical motives, replace an accepted relationship, or require retrospective completion of personality fields. Existing active encounters keep their established state; use the accepted method for eligible gaps before dependent behavior. If that method does not cover a newly required determination, settle only the missing prospective choice through the upgrade or recalibration procedure. Only a separately accepted campaign change revises its agreement, generation method or autosave permission. Session continuity is compatible with missing legacy coverage and is adopted prospectively; do not infer played boundaries or unpaid awards. Include the session routine and any actual engine policy in the focused prospective agreement supplement. Do not create PREP during installation or bind.

Older field-only formats and missing agreement clauses still need the existing [v0.7 mapping](ADMIN/UPGRADE_V07.md) or focused [recalibration](ADMIN/RECALIBRATE.md), as routed by the compatible upgrade procedure. Do not infer old permissions from prior model behavior.

The runtime does not pin every referenced record to an immutable version. Keep a coherent campaign copy; matching filenames alone do not make arbitrary engines, modules or current-state files interchangeable.

## Continuing with another model

Before a planned model, reasoning-setting, provider, chat or GM change, the outgoing context saves and verifies first. Do not switch to a stronger model to compile unsaved state. This is a conservative preservation rule, not a claim that every host change wipes context or that a completed save guarantees full memory transfer.

After a successful full save, give the next model the same updated campaign folder and ask it to open OS/AGENTS.md and continue. Keep one active continuation. Saving, a new chat and handover preserve the same logical play session unless you also explicitly end it. Retain the build, model and known reasoning setting with your optional session note; do not invent settings the host does not expose. Different prose is expected; established facts and unresolved choices must survive. A checkpoint-only switch protects current state but leaves new exact dialogue unarchived; disclose that limitation and use full CLOSE or handover before discarding source.

For an unfinished scene, use [Scene handover](ADMIN/SCENE_HANDOVER.md). It captures accessible conversation and established GM state against a frozen workspace. A different host needs a deliberate copy; the procedure does not send files or grant external access. The source stays paused until checked return/import or cancellation.

The receiver leaves source authorities frozen. Its new unsaved facts must be captured in the permitted return; the source cannot be used as a live receiver checkpoint. Unavailable chat, unrecorded model intentions and inaccessible references cannot be transferred. See [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md).

## Hosts without direct workspace writes

1. Provide the startup records and specifically requested references.
2. At SAVE, ask for complete replacements for every changed file, a list of those files, and the historical evidence being retained.
3. Preserve the previous versions before installing the replacements yourself. Use generated downloadable files if available, otherwise copy complete contents.
4. Confirm that every replacement was installed and checked. The fresh chat must receive or access these updated files.

Until then, the result is **an export awaiting installation**, not a confirmed workspace save. Keep the conversation until installation. Visible exports cannot conceal private preparation; use reviewed, openly acknowledged or deliberately unresolved material as appropriate to the accepted method. An autosave notice cannot make an unwritable workspace writable; disclose the limitation instead of reporting a completed checkpoint.

## Source material and backups

Keep personal campaigns separate from a shareable unbound kit. Include only source material you may use and redistribute as appropriate. A franchise name alone does not establish edition, continuity or exact rules authority. Inspect referenced visuals only when the host can actually access and interpret them.

Recovery copies protect against identifiable interrupted edits; retain complete campaign backups as well. No model-operated file convention guarantees automatic rollback, perfect recall or universal model compatibility.

## Optional local source and audit tools

Python 3.10 or newer enables the supplied source reader, evidence helper and optional autosave scheduler. Scoped search additionally needs that Python installation's SQLite FTS5 support; `python -B TOOLS/read_source.py probe` reports observed support. No extra package, network service, model API or embedding service is required. These tools are optional: normal targeted file reading and campaign play remain available without them.

Store search databases, receipts and audit bundles outside the campaign roots they measure. Raw captures may live under the campaign's `EVIDENCE/captures/` area. Use actual platform exports or user-supplied source files and report their coverage; filesystem access does not imply access to complete chat history. See [Source access](ADMIN/SOURCE_ACCESS.md) and [Evidence audit](ADMIN/EVIDENCE_AUDIT.md).
