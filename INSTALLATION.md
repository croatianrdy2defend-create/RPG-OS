# Install and run RPG OS v0.6.2

This guide assumes you are not a programmer.

RPG OS is not an application you launch. It is a folder of Markdown instructions and campaign files. You give that folder to a capable AI, and the AI uses it to GM and to save the campaign.

## What you need

You need a host/model/tool combination that can:

1. open a folder or repository;
2. read exact named files;
3. write changes that remain after the chat closes;
4. start a new chat against the same updated folder.

A famous model, large context window, paid plan, or “Project” label does not guarantee these abilities. Test the actual setup.

Possible arrangements include:

- a desktop/workspace product with a writable local folder;
- a cloud project that genuinely persists file edits;
- an agent working in a private Git repository branch;
- a lawful local/offline model with file tools.

A normal chat box with a ZIP pasted into one message is not enough if edits cannot persist.

## 1. Download and extract

From GitHub, choose **Code → Download ZIP**, then extract it.

- Windows: right-click the ZIP → **Extract All**
- macOS: double-click the ZIP
- Linux: use your archive manager or `unzip <archive>.zip`

Open the extracted project root. It is the folder that directly contains `OS`, `ENGINE`, `MODULES`, `INSTANCE`, `ARCHIVE`, and `ADMIN`.

If you cloned with Git instead, use one private branch or one separate working copy per campaign. Do not let two active campaigns write into the same INSTANCE.

## 2. Make a backup

Before attaching the folder to any AI service, copy it somewhere the service cannot overwrite.

Keep regular backups throughout the campaign. Cloud project storage, chat history, and a Git branch are conveniences—not substitutes for a copy you control.

Do not publish a bound campaign repository unless you have removed private play, safety settings, personal data, copyrighted rules material, and spoilers.

## 3. Attach the folder

Add only this RPG OS folder to a writable project or workspace. Do not attach an older RPG OS version or another campaign ZIP alongside it; duplicate authorities can confuse retrieval.

Start a fresh chat inside that project.

## 4. First boot

Paste exactly:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start fiction.
```

A clean public kit should identify itself as unbound and stop without fiction. If it invents a tavern, character, world, or opening scene, this host/model did not follow the boot contract.

The five named files are the unchanged **technical boot set**. After a campaign is bound, BOOTSTRAP follows active safety, loads the module's required compact `SETTING_BRIEF.md` once, then loads required voice material before first fiction. It may load the optional `INSTANCE/BEARING.md` only when REVIEW is enabled and its base save/Contract revisions match.

The Setting Brief gives the GM only the stable public baseline it needs from the start: the world's identity, foundational facts that define what is ordinary, and the deeper information domains available if a later task needs them. Detailed lore, rosters, clocks, phases, seeds, private truth, and archive evidence remain cold. The brief must not become a campaign synopsis, roster, active-state file, or plot outline.

## 5. Optional structural validation

`VALIDATE` is read-only. It checks deterministic structure, not story quality.

If the host can execute Python, from the project root run:

```bash
python3 TOOLS/validate.py --root .
```

On Windows, this may be:

```powershell
py TOOLS\validate.py --root .
```

Interpret the result honestly:

- exit `0`: the script completed its declared structural checks without finding a violation;
- exit `1`: it found structural violations;
- exit `2`: coverage was incomplete because execution, access, parsing, validator identity, or a stable-tree condition failed.

The report separates:

- **STRUCTURAL** — deterministic files and references;
- **HOST OBSERVATION** — not established by the script;
- **SEMANTIC** — not established by the script.

A script pass does not prove that the GM will preserve agency, choose warrants well, keep hidden text out of narration, write persistently, or run a coherent campaign.

If code execution is unavailable, an AI inspection must say `MODEL-CHECKED` and list the exact files/checks it covered. It cannot certify the complete tree and should report `INCOMPLETE` unless it found a definite failure.

Do not rely on an old validation result after files change. v0.6.2 is a testing release; this guide does not claim your copy has passed.

## Upgrading a bound v0.6 or v0.6.1 campaign

This is a one-purpose ADMIN upgrade for a bound campaign whose module predates the required Setting Brief.

1. Under the existing runtime, run CHECKPOINT or CLOSE for every accepted play slice. Do not continue if accepted play exists only in chat.
2. Make a byte-for-byte backup of the complete bound folder outside the active workspace. Upgrade another working copy.
3. Install the v0.6.2 runtime, ADMIN documents, validator, root documentation, and generic `_CONTRACT.md` / `_SCHEMA.md` files. Preserve the campaign's module content, Current Save and other INSTANCE authorities, engine adapter, and ARCHIVE evidence.
4. Confirm `MODULES/<bound-module-id>/SETTING_BRIEF.md` is absent. If it already exists but is malformed, stop; this command may not overwrite or repair it.
5. Start a fresh ADMIN chat against the working copy and send this complete first message:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
This is an operator-attested backed-up bound v0.6 or v0.6.1 campaign copy.
A restorable byte-for-byte backup exists outside the active RPG OS folder.
INSTANCE/CURRENT_SAVE.md includes all accepted PLAY.
The bound module's fixed SETTING_BRIEF.md is absent.
UPGRADE SETTING BRIEF
Do not start fiction.
```

The operation may inspect only the stable public module material needed to draft the brief. It must display the complete proposed file, explain its source coverage, and wait for exact `ACCEPT SETTING BRIEF`. Review that it contains only world identity, what is ordinary, and available cold depth—not current state, a roster, private truth, clocks, phases, seeds, prepared scenes, or a plot queue.

After exact `ACCEPT SETTING BRIEF`, the operation writes only the previously absent `MODULES/<bound-module-id>/SETTING_BRIEF.md`. It does not modify the save, Contract, module descriptor, engine, archive, or any other campaign authority. Run `VALIDATE`, then start a fresh chat and use the normal five-file boot. The authoritative procedure is [ADMIN/ADD_SETTING_BRIEF.md](ADMIN/ADD_SETTING_BRIEF.md).

## Upgrading a bound v0.5 campaign

This is a one-time, explicit migration. It does **not** automatically merge two folders, recover unsaved chat, reinterpret old play, or rewrite the archive.

1. In the old v0.5 environment, first run CHECKPOINT or CLOSE for every accepted play slice. If accepted play exists only in chat, save it there before installing v0.6. If that is no longer possible, stop: migration cannot reconstruct it safely.
2. Make a byte-for-byte backup of the complete bound v0.5 folder outside the active AI workspace. Perform the migration on another working copy.
3. Selectively install the v0.6.2 runtime and generic documents. Replace `OS/`, `ADMIN/`, `TOOLS/`, the root documentation, and the generic `_CONTRACT.md` / `_SCHEMA.md` files. Add the canonical blank v0.6 `INSTANCE/CAMPAIGN_CONTRACT.md` and `INSTANCE/BEARING.md` templates.
4. Preserve the bound campaign's own files: its `MODULES/<module-id>/` tree, bound `INSTANCE/CURRENT_SAVE.md` and all other campaign INSTANCE records/shards, and all ARCHIVE evidence/indexes/ledgers. If the old module has no `SETTING_BRIEF.md`, migration may draft one only from stable public facts in the preserved module, must display it in full, and must obtain explicit acceptance before writing it. A malformed existing brief is a separate repair and must stop migration. If the run uses the shipped `freeform` engine, install the v0.6.2 `ENGINE/freeform.md`; preserve a custom bound adapter and review it against the current engine contract. Do not drag the whole clean release over the campaign and choose “Replace all.” Migration does not invent or repair rules.
5. Confirm the working copy has no unfinished candidate or partial migration residue. Start a fresh ADMIN chat against that copy and send this complete first message:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
This is an operator-attested bound v0.5 campaign copy.
MIGRATE V0.5
Do not start fiction.
```

Those five technical boot files let BOOTSTRAP dispatch the legacy migration before ordinary v0.6 bound-run validation.

The migration preflight requires your attestation that this is a bound v0.5 run, the external backup exists, and no accepted play follows the saved Current Save. It inspects the legacy identities, lineage, routes, module, and engine without pretending the legacy save already satisfies v0.6.

It then asks you to accept a complete first v0.6 Campaign Contract and to supply explicit values for:

- `scene_status`
- `uncommitted_time`
- `pc_declared_goals`
- `causal_frontier`

Review the full proposed manifest and diff. The model may preserve established legacy values, but it must not infer PC goals, grant itself a creative mandate, turn old open matters into a plot outline, or move old archive material into Bearing. Say `ACCEPT` only when the proposal is correct.

On success, the migrated Current Save keeps the legacy facts and receives a new checkpoint-style `save_id`, incremented `save_rev`, the old `save_id` as `save_parent`, `commit_kind: checkpoint`, and `archive_ref: none`. If required, the explicitly accepted missing Setting Brief publishes first; a bound `status: none` Bearing follows, then the accepted Contract publishes immediately before CURRENT_SAVE publishes last. Every other campaign-owned MODULE file and all ARCHIVE indexes, ledgers, and evidence remain unchanged.

Wait for the completion report and new `save_id`. Run `VALIDATE`, then start another fresh chat and use the normal five-file v0.6.2 boot. If migration is refused, interrupted, or reports a mismatch, do not continue PLAY and do not improvise a repair from chat memory; restore the backup or inspect the exact affected files. The authoritative transaction rules are in [ADMIN/MIGRATE_V05.md](ADMIN/MIGRATE_V05.md).

## 6. Create the campaign

Say:

```text
NEW GAME
```

NEW GAME is a setup interview, not roleplay. It should work in short clusters rather than dropping a giant questionnaire.

### Engine

The public package ships only `freeform`.

You may name another system. A compact local engine adapter may be created from procedures and values you lawfully supply. RPG OS can host adapters for systems such as GURPS, Dungeons & Dragons, Pathfinder, Call of Cthulhu, Fate, Savage Worlds, or an original system, but none of those adapters is included.

Do not ask the model to reconstruct or redistribute a rulebook. You still need lawful access to the rules.

### Campaign and safety

The interview establishes premise, voice, tone, unwanted patterns, and extra safety limits. Safety is asked before detailed world, character, or scenario drafting. From the accepted world choices, SETUP also drafts the required compact Setting Brief; it should ask one small clarification only if the public baseline is still genuinely unclear.

It then builds the run's **Campaign Contract**, including:

- campaign promise and fit envelope;
- structural direction;
- GM initiative;
- pressure/incident density;
- time handling;
- development priorities;
- guidance visibility;
- whether proactive creative mandate exists, its scope, and eligible boundaries;
- REVIEW mode.

These settings calibrate the GM. They never force a particular scene or outcome.

### Optional depth

World/campaign depth, PC profile depth, and mechanical-sheet depth are independent.

A sparse world, short profile, and deferred mechanical sheet are valid. A detailed campaign may selectively add phases, causal clocks, institutions, calendars, resources, relationships, private truth, or house rules. It should build only the domains you chose.

The AI may not guess missing PC statistics, personality, attraction, consent, backstory secrets, or commitments in order to make a sheet look complete.

### Acceptance

The AI drafts a playable starting situation and a file manifest. It must not author your character's first voluntary act.

Review the proposal. Correct it if needed. Say `ACCEPT` only when the manifest and Contract match what you want.

ACCEPT authorizes exactly the disclosed write set. After the commit succeeds, start a new chat rather than continuing the setup conversation as PLAY.

## 7. Begin PLAY

In the new chat, use the same five-file boot prompt. Then say:

```text
Begin play.
```

Before fiction, the GM reads the compact Setting Brief once so it knows the world's public baseline without opening the lore library. It should then orient to the saved campaign and give you a playable situation. It owns the world; you own your character's voluntary conduct and interior life.

During PLAY the model may retrieve only what its current GM task requires. It must not browse the repository for inspiration or activate something because it found the file.

## 8. Save correctly

PLAY does not write files.

- `CHECKPOINT` saves the authoritative present and causal frontier.
- `CLOSE` saves the same present plus scene-sharded historical evidence.
- `REVIEW` separately updates only the optional provisional Bearing after a successful save.
- `END SESSION` runs CLOSE first and, if enabled, REVIEW second.

Wait for a new `save_id` before closing or deleting the chat. If the chat is lost first, RPG OS cannot recover the unsaved play.

For the next session, open a new chat against the same updated folder and use the five-file boot prompt. Do not paste the previous transcript.

## 9. Test persistent writing

After the first bound play slice:

1. say `CHECKPOINT`;
2. record the new `save_id`;
3. close that chat;
4. start a fresh chat against the same folder;
5. run the five-file boot;
6. confirm the same new `save_id` and saved situation appear.

If they do not, the host did not persist the write. Do not trust that setup for disposable-chat continuity.

## 10. Test section handling

This is only a weak observation:

```text
Open only INSTANCE/_SCHEMA.md heading "## CURRENT_SAVE whitelist".
Quote that heading. Do not quote later headings.
```

If unrelated later sections appear, the host may inject whole files. Keep private or independently relevant material physically split into narrow files.

Even a clean answer does **not** prove that unused sections never entered the context. File labels and Markdown headings are not security boundaries.

## 11. Interrupted writes

v0.6 updates several files in some ADMIN operations. Publishing Current Save last protects the main save pointer, but the whole operation is not filesystem-atomic.

If CHECKPOINT, CLOSE, ACCEPT, LOAD, RECALIBRATE, or REVIEW is interrupted:

1. stop;
2. do not resume PLAY;
3. inspect the reported write plan and affected files;
4. restore from backup if consistency is uncertain;
5. validate again before continuing.

Do not tell the model to “finish from memory” after the original chat is gone.

## 12. Provider and privacy warning

RPG OS cannot change a provider's terms, moderation, logging, or account enforcement. Fiction, historical context, and private roleplay do not guarantee that material will be accepted. Content may be refused or a write may be interrupted; prohibited material may expose an account to restriction or termination.

Do not bypass provider safeguards. Change the campaign material or use a lawful environment that permits it. Keep the canonical campaign and backups outside the provider.

## Troubleshooting

| Symptom | Likely issue | Response |
|---|---|---|
| Fiction starts while unbound | Boot instructions not followed | Restart in a fresh chat and use the exact five-file prompt |
| The GM asks you to invent every next event | Clerk failure | Confirm the Contract and GM-first LAW loaded; report the semantic fixture |
| Random hooks appear because they fit | Fit treated as warrant | Stop/rewind; check creative mandate and causal frontier |
| New chat forgets the last scene | Write did not persist, or no PERSIST occurred | Restore the correct folder; rerun the persistent-write test |
| Old Bearing drives play after a save/Contract change | Stale Bearing was loaded | It must be ignored unless all base ids/revisions match |
| A private file leaks | Host may inject whole files | Split it physically; do not claim isolation |
| ADMIN was interrupted | Partial multi-file write possible | Stop and inspect/restore before PLAY |
| Another engine is not listed | Adapter missing or invalid | Follow `ENGINE/_CONTRACT.md` and `ADMIN/ADD_ENGINE.md` |

Next: [QUICKSTART.md](QUICKSTART.md)  
Commands: [COMMANDS.md](COMMANDS.md)  
Design: [ARCHITECTURE.md](ARCHITECTURE.md)  
Testing and reports: [CONTRIBUTING.md](CONTRIBUTING.md)
