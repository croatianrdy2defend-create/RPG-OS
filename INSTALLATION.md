# Installation and first run

For people who are not programmers.

RPG OS is a folder that helps an AI run and remember a solo tabletop RPG. The AI is the GM, but your character's choices remain yours. The campaign is saved in readable files instead of depending on one endlessly growing chat.

You do not need to open, study, or edit every file. Most of them are instructions for the AI.

## The short version

1. Download and extract the folder.
2. Add the whole folder to an AI workspace that can open and save files.
3. Start a new chat and paste the startup message in section 3.
4. Say `New game`, answer the questions, review the final summary, and say `Accept`.
5. After the AI confirms the save IDs, start a fresh chat with the same folder and use the play/resume message in section 5.
6. Play normally. Use `CHECKPOINT` for a break and `CLOSE` at session end. Wait for the new `save_id` before closing the chat.

## Will your AI workspace work?

It must be able to answer **yes** to all three questions:

- Can it open exact named files from the attached workspace?
- Can it save edits back into that same workspace?
- Can a fresh chat access the updated workspace?

If not, the normal RPG OS workflow will not persist reliably. A plain chat box with no writable workspace is not enough. Product names, model names, and subscription tiers do not prove compatibility.

---

## 1. Download

Download the v0.5 source archive from the GitHub repository's **Code → Download ZIP** menu, or use a separately supplied `RPG_OS_v0.5.zip`. GitHub may name its generated folder `RPG-OS-main`; the folder name is not authoritative.

On Windows: right-click → Extract All. Open the extracted project root containing `OS`, `ENGINE`, `INSTANCE`, and `ADMIN`; you may rename that root `RPG_OS` for clarity.

On Mac: double-click the archive.

On Linux: `unzip <downloaded-archive>.zip`

If you see `OS/LAW.md` and `INSTANCE/CURRENT_SAVE.md`, you extracted it correctly.

---

## 2. Attach ONLY this folder

Open a writable project or workspace and add the whole `RPG_OS` folder. Do not also attach other campaign zips. Open a new chat inside that project or workspace. Use a capable model.

---

## 3. First messages

Start a **new chat inside the workspace that contains the RPG OS folder**. Paste this exactly:

```
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start a scene.
```

Expected result: the AI says RPG OS is ready, but no campaign exists yet. It must not invent a world or opening scene.

Now say:

```
New game.
```

The AI should begin the setup questionnaire, one small group of questions at a time. Optional compatibility and validator checks are collected later in this guide; you do not need to run them before trying New Game.

---

## 4. New Game

The first question is which rules to use. The public pack includes **Freeform**, which lets the AI judge uncertain outcomes without a detailed game system. You may name another system, but RPG OS may store only a compact adapter based on procedures and values you provide or are entitled to use. It must not reconstruct or redistribute a copyrighted rulebook.

The questionnaire then asks about:

- the campaign title, premise, narrative style, tone, and pacing;
- **anti-attractors** — themes or recurring patterns you want the GM to avoid or limit;
- optional safety boundaries;
- world/campaign depth — Sparse, Focused, Detailed, or Custom;
- character detail — Quick, Standard, Detailed, or Custom;
- mechanical sheet — No full sheet now, Minimum required, Guided full sheet, or Import and review.

Character detail and mechanical-sheet detail are separate choices. A completed mechanical sheet is optional. The AI may not guess missing statistics, personality, attraction, consent, or backstory just to fill a form. “Detailed campaign” means developing only the areas you select, not generating an encyclopedia.

Finally, you choose a starting situation and review a **manifest**: a plain summary of what the AI intends to create, omit, or deliberately leave undecided. Optional systems such as clocks or factions are created only when you choose them and the required files will exist.

Nothing becomes campaign canon until you say **`Accept`**. Afterward, wait until the AI confirms that writing finished and prints both a `campaign_id` and a `save_id`.

---

## 5. Play in a NEW chat

Do not continue playing inside the setup questionnaire. Open a fresh chat in the same workspace and paste:

```
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Do not search or list the rest of the folder.
Follow BOOTSTRAP for anything else required to begin.
Resume at the saved situation and return control before my character acts.
```

The AI should establish only the accepted starting situation and then return control to you. You decide what your character does, says, thinks, feels, accepts, buys, risks, or commits to.

---

## 6. Saving and returning later

- Use **`CHECKPOINT`** when taking a break or when you want to protect the current situation. It saves the complete playable present, but not detailed historical evidence.
- Use **`CLOSE`** at session end or before discarding a chat when you also want exact messages and detailed scenes preserved for later retrieval.

In both cases, wait until the AI confirms a new `save_id`. If the write is interrupted, do not assume the save succeeded.

Next time, open a new chat in the same workspace and paste the play/resume message from section 5. The files—not the old conversation—are the campaign's memory.

---

## 7. Confirm that saving really works

This is the important compatibility test. Run it after a campaign has been accepted:

```
CHECKPOINT. Confirm the new save_id. I will open a new chat next.
```

Write down the new `save_id`. Open a fresh chat in the same workspace and use the play/resume message from section 5.

- **Pass:** the fresh chat reports the same new `save_id` and resumes at the saved situation.
- **Fail:** the ID or situation is old. That workspace is not persisting RPG OS changes reliably.

Do not trust a platform's advertised file support in place of this test.

---

## 8. Optional checks and troubleshooting

These checks are useful for testing a host or diagnosing problems. They are not required reading before your first New Game.

### A. Deliberate unbound refusal

On a clean, unbound kit, say `Begin play.` RPG OS should refuse because no campaign exists. This is a successful safety check, not an installation failure.

### B. Section-reading test

```
Open only INSTANCE/_SCHEMA.md heading "## CURRENT_SAVE whitelist". Quote that heading. Do not quote later headings.
```

- **Pass:** only the requested heading appears.
- **Fail:** later headings also appear. The host probably injects whole files. Keep private material and long transcripts in separate small files.

Even a clean result does **not** prove that unread text stayed outside the model's context.

### C. Structural validator

If you have Python 3.8 or newer, open a terminal in the extracted RPG OS folder and run:

```text
python3 TOOLS/validate.py
```

On Windows, use:

```text
py TOOLS\validate.py
```

- Exit `0`: the declared structural checks completed without finding a violation.
- Exit `1`: structural problems were found.
- Exit `2`: the validator could not completely check what it claims to cover.

This validator checks file structure, references, and supported schemas. It does **not** prove story quality, player-agency compliance, privacy, persistent saving, moderation compatibility, or future correctness after files change. Full details: [`ADMIN/VALIDATE.md`](ADMIN/VALIDATE.md).

---

## Important warnings

- Unsent suggested-reply buttons are not player input.
- Keep one separate folder copy for each active campaign.
- Keep regular backups outside the AI provider. A cloud workspace should not be your only copy.
- `CHECKPOINT` is a real save of the present; `CLOSE` adds detailed archive evidence.
- If `CHECKPOINT` or `CLOSE` is interrupted while files are changing, do not resume play until the files are inspected or restored from backup.
- RPG OS cannot override a provider's moderation rules, account policies, outages, or service closure.

### For advanced customization

Do not edit `OS/LAW.md` for campaign preferences. `POLICY` holds tone, pacing, and boundaries. `RULES_HOOKS` may add nonconflicting guidance for applying the chosen rules. A real mechanical change needs a distinct `ENGINE`; later table rulings belong in `INSTANCE/CORRECTIONS`.

You do not need to understand those files for an ordinary first game.

Next: [`QUICKSTART.md`](QUICKSTART.md). Command reference: [`COMMANDS.md`](COMMANDS.md). Public test reports: [`CONTRIBUTING.md`](CONTRIBUTING.md).
