# Installation and first run

For people who are not programmers.

This folder is a campaign operating system for a solo RPG. The AI is the GM. Your character's choices stay yours. The world is saved in files, not in the chat.

You need an AI that can **read and write files in a project folder**. If you only have a normal chat box with no folder, this will not work well.

Potentially suitable: any host/model combination that can open named files, persist edits to the attached project, and pass the preflight below. Product name, model name, or subscription tier alone proves none of those capabilities. A blank chat with nothing attached is not enough.

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

Message A:

```
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start a scene.
```

You want: ready, unbound, no tavern, and it says it opened only those four files.

Message B (optional): `Begin play.` It must refuse.

Message C: `New game.`

Before Message B, you may say `VALIDATE`. If the host can run code, it should execute the shipped read-only `TOOLS/validate.py`, report a STRUCTURAL result as `SCRIPT-VERIFIED`, print the scanned tree digest, and keep HOST OBSERVATION (`NOT RUN`) and SEMANTIC (`NOT CHECKED`) separate. It must not create a report file or change campaign state.

If the host cannot execute code, the fallback must say `MODEL-CHECKED` with the exact files and checks inspected. It reports `INCOMPLETE` unless it observed a definite defect and reports `FAIL`; either way, it cannot certify the complete tree.

---

## 4. New Game

First question is the rules. The public pack ships **freeform**. You may name another system; the AI may draft a compact local engine file from procedures and values you supply or are entitled to use. It must not reconstruct or redistribute a copyrighted rulebook.

Then: title, voice, tone, anti-attractors, safety extras, and three separate choices:

- world/campaign depth — Sparse, Focused, Detailed, or Custom;
- character/profile depth — Quick, Standard, Detailed, or Custom;
- mechanical sheet — No full sheet now, Minimum required, Guided full sheet, or Import and review.

Profile depth and mechanical-sheet path are independent. A completed mechanical sheet is optional. The AI must still create a substantive PC baseline from facts you supplied or accepted; it may not fill missing stats or personality by guessing. Detailed campaign building covers only the domains you select and does not mean “generate an encyclopedia.”

Safety extras are asked before detailed world, character, or scenario drafting. Then: starting moment, dependency/interaction audit where needed, **starting scenario** (2–3 live hooks; pick one), optional capability bodies, and a manifest showing separately what is built, omitted, or deliberately unfixed.

Nothing is canon until you **Accept**.

---

## 5. Play in a NEW chat

Same folder. Paste the four-file opening. You get the starting situation only. Then you say what your character does.

---

## 6. Session loop

CHECKPOINT saves time/place/resources. CLOSE also keeps exact messages and scene evidence.
Do not discard the chat until ADMIN confirms the new save_id.
Next time: new chat, four files, the save is memory.

---

## 7. Preflight — isolation and writes

These tests detect hosts. They cannot prove tokens never entered context.

**A. Section quote (weak)**

```
Open only INSTANCE/_SCHEMA.md heading "## CURRENT_SAVE whitelist". Quote that heading. Do not quote later headings.
```

Pass: only that heading appears.
Fail: later headings appear. Then this host injects whole files. Keep PRIVATE and long transcripts in **separate small files**. Treat as **unsupported for privacy-sensitive large records** until you split.
A clean quote still does **not** prove the rest of the file stayed out of context.

**B. Persistent write**

After a bound run (or on unbound: skip until after first ACCEPT):

```
CHECKPOINT. Confirm the new save_id. I will open a new chat next.
```

Pass: ADMIN prints a new save_id; a fresh chat four-file boot shows that save_id.
Fail: save_id unchanged, or the new chat is still the previous moment. Then this host cannot persist files — the OS will not survive killing the chat.

**C. Structural validator (optional but recommended)**

From a terminal opened in the extracted `RPG_OS` folder (Python 3.8 or newer):

```text
python3 TOOLS/validate.py
```

On Windows, use `py TOOLS\validate.py`. The report shows separate hashes for the validator that executed and the copy inside the target tree; a mismatch is incomplete coverage. Exit `0` means the declared deterministic structural checks completed without a violation. It does not test narrative judgment, player agency, host isolation, persistent writes, provider moderation, or future correctness after the files change. Exit `1` means structural violations were found; exit `2` means declared coverage is incomplete because execution/access failed, the tree changed during the scan, the validator copies differed, or a declared machine-readable surface could not be completely parsed (including a legacy descriptor outside the supported v0.4 grammar).

---

## Extra warnings

Unsent UI suggestions are not player input.
Do not edit OS/LAW.md. Put voice/cadence/boundaries in POLICY. Nonconflicting campaign calibration may use RULES_HOOKS; an actual mechanical override needs a distinct ENGINE id; later table rulings go in INSTANCE/CORRECTIONS.
CHECKPOINT is a real save of the present. CLOSE adds the archive.
Keep one folder copy per active campaign.
Keep the canonical folder and regular backups outside the AI provider. A cloud Project is not your only backup. Policy changes, moderation, account restrictions, or service closure can make a campaign temporarily or permanently inaccessible.
CURRENT_SAVE-last is not a filesystem-wide atomic transaction. If CHECKPOINT or CLOSE is interrupted while several INSTANCE files are changing, do not resume PLAY until the affected files are inspected or restored from backup.

Next: `QUICKSTART.md`. Command reference: `COMMANDS.md`. Public test reports: `CONTRIBUTING.md`.
