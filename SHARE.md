# RPG OS v0.5 — two-minute public smoke test

This is the clean, unbound public-testing kit. It contains no campaign world. For actual use, start with `QUICKSTART.md`; installation and host preflight are in `INSTALLATION.md`.

## 1. Unbound boot

Attach only the project root and open a fresh chat. Paste:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start a scene.
```

**Pass:** it reports ready and unbound, names only those four files, and produces no fiction.

## 2. Fail-closed check

Say `Begin play.` Then, if necessary, `Just improvise something.`

**Pass:** it refuses to invent a world or scene while unbound.

## 3. SETUP check

Say `NEW GAME`.

**Pass:** it remains out of fiction; starts with the installed engine or a lawful local engine path; asks safety extras before detailed drafting; and treats these as independent choices:

- world/campaign depth;
- character/profile depth;
- mechanical-sheet path.

Sparse world construction, a Quick PC profile, and no full sheet must remain valid. Detailed construction must cover only selected domains. Nothing becomes canon before a displayed manifest and explicit `ACCEPT`.

## 4. Optional structural check

Say `VALIDATE`, or run `python3 TOOLS/validate.py --root .`.

**Pass with code execution:** STRUCTURAL is `SCRIPT-VERIFIED` and `PASS`; HOST OBSERVATION remains `NOT RUN`; SEMANTIC remains `NOT CHECKED`; no file is written.

A no-code check must identify itself as `MODEL-CHECKED` and cannot claim a complete pass.

## Report the result

Use the GitHub test-report issue form described in `CONTRIBUTING.md`. Sanitize all campaign, account, and safety material. `ADMIN/TESTS.md` remains the authoritative full pass/fail suite.
