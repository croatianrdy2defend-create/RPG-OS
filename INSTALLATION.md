# Installation and portability — v8.1.1 experimental

## A new campaign

Download the [v8.1.1 release](https://github.com/croatianrdy2defend-create/RPG-OS/releases/tag/v8.1.1), extract its package into a dedicated campaign folder and make it available to your LLM. Use one active campaign per copy. Start from [Quick start](QUICKSTART.md). The release contains blank, unbound templates and only the Freeform engine; it carries no campaign module, character or artwork. Earlier versions remain on the [published releases page](https://github.com/croatianrdy2defend-create/RPG-OS/releases).

The normal workflow requires the host to read named files, create and replace ordinary files, preserve them between chats, and let the model inspect what it wrote. An attachment may be readable without being writable. Establish the actual available operations during setup; use the export workflow below when needed. No paid API, background service or required script is part of the design. Smaller reference files help hosts that can only read entire files.

Do not begin from a folder containing another campaign's INSTANCE, ARCHIVE, or pending RECOVERY/HANDOVER state. Keep that campaign in its own copy.

## State, randomness and practical visibility

The agent-state procedure uses existing records for individual circumstances, beliefs, aims and relationships. Setup can establish the small private opening baseline under the accepted authoring scope. During ordinary play, newly established facts and changes remain unsaved in the conversation until a requested save. Installing v0.8 does not create automatic checkpoints or an invisible memory service.

When a selected procedure requires randomness, use an actual available randomizer or player-supplied input with agreed outcome meanings. If neither is available, settle an explicit judgment alternative or keep that resolution pending. Freeform judgment is a valid default; fabricated dice are not a substitute for the requested method. Merely supplying a seed does not define a reproducible generator without its procedure and inputs.

v8.1.1 adds a minimal individual baseline when the player singles out an NPC for direct attention or interaction, or the NPC directly engages the PC. A bare approach needs no explanation of purpose. Existing people are reused, and detail grows only as actual developments require it. See the [direct-approach example](MECHANICS.md#example-i-approach-her).

The simple standing fallback from v0.8.1 remains available for eligible unauthored outcomes with insufficient basis for grounded judgment: one actual d6, 1–3 No and 4–6 Yes. Select it once in the accepted setup proposal or request its prospective adoption through [Recalibrate](ADMIN/RECALIBRATE.md). Established facts, applicable rules and other selected methods come first; selection removes the need for per-roll permission. Installing the program alone preserves an existing diceless agreement or another selected oracle. See the [fallback examples](MECHANICS.md#random-fallback-for-unresolved-outcomes).

Private records provide practical spoiler separation, not encryption. Tool arguments, results or writes may be visible to the operator. If a selected method depends on concealment, check with a harmless synthetic secret and explain the actual limitation. Do not expose a real plot fact to test the interface. A collapsed panel or a file named "private" does not establish secrecy.

Recheck only affected capabilities when moving hosts. A host change does not authorize regenerating recorded people or changing rules.

## Existing campaigns

**Never install blank INSTANCE or ARCHIVE templates over a campaign.**

1. Complete the latest save using the old compatible runtime. Finish or reconcile pending recovery and scene transfers before changing their dependencies.
2. Keep a restorable copy of the entire campaign and its original runtime. Create a separate upgrade copy.
3. Give the GM the v8.1.1 kit as the update source and say: "Open ADMIN/UPGRADE_V08.md from the new kit and prepare this campaign's upgrade in the separate copy."
4. Review the actual program-file change set and any material compatibility question. Preserve campaign-owned modules, engine adapters, instance records, archives, local modifications and recovery evidence as the procedure specifies.
5. Apply the authorized update with recovery protection and readback. Resume from the preserved save after verification.

Valid v0.7.1–v0.7.3 and v0.8.0 records retain their formats and save identities. The upgrade consolidates general operating guidance; it does not resample NPCs, rewrite historical motives, replace an accepted relationship, or require retrospective completion of personality fields. Only a separately accepted campaign change revises its agreement or generation method.

Older field-only formats and missing agreement clauses still need the existing [v0.7 mapping](ADMIN/UPGRADE_V07.md) or focused [recalibration](ADMIN/RECALIBRATE.md), as routed by the v0.8 procedure. Do not infer old permissions from prior model behavior.

The runtime does not pin every referenced record to an immutable version. Keep a coherent campaign copy; matching filenames alone do not make arbitrary engines, modules or current-state files interchangeable.

## Continuing with another model

After a successful full save, give the next model the same updated campaign folder and ask it to open OS/AGENTS.md and continue. Keep one active continuation. Retain the build, model and known reasoning setting with your optional session note; do not invent settings the host does not expose. Different prose is expected; established facts and unresolved choices must survive.

For an unfinished scene, use [Scene handover](ADMIN/SCENE_HANDOVER.md). It captures accessible conversation and established GM state against a frozen workspace. A different host needs a deliberate copy; the procedure does not send files or grant external access. The source stays paused until checked return/import or cancellation.

The receiver leaves source authorities frozen. Its new unsaved facts must be captured in the permitted return; the source cannot be used as a live receiver checkpoint. Unavailable chat, unrecorded model intentions and inaccessible references cannot be transferred. See [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md).

## Hosts without direct workspace writes

1. Provide the startup records and specifically requested references.
2. At SAVE, ask for complete replacements for every changed file, a list of those files, and the historical evidence being retained.
3. Preserve the previous versions before installing the replacements yourself. Use generated downloadable files if available, otherwise copy complete contents.
4. Confirm that every replacement was installed and checked. The fresh chat must receive or access these updated files.

Until then, the result is **an export awaiting installation**, not a confirmed workspace save. Keep the conversation until installation. Visible exports cannot conceal private preparation; use reviewed, openly acknowledged or deliberately unresolved material as appropriate to the accepted method.

## Source material and backups

Keep personal campaigns separate from a shareable unbound kit. Include only source material you may use and redistribute as appropriate. A franchise name alone does not establish edition, continuity or exact rules authority. Inspect referenced visuals only when the host can actually access and interpret them.

Recovery copies protect against identifiable interrupted edits; retain complete campaign backups as well. No model-operated file convention guarantees automatic rollback, perfect recall or universal model compatibility.
