# RPG OS v0.7 startup

Load a campaign when asked to run, resume, or set one up. Development and review requests do not start PLAY.

## Load

1. Check the exact path `RECOVERY/ACTIVE.md`. If present, leave PLAY idle and open `ADMIN/RECOVERY.md`; reconcile an interrupted operation before continuation. Absence is normal. Do not inventory the recovery folder.
2. Read `OS/LAW.md`, `INSTANCE/CURRENT_SAVE.md`, and `INSTANCE/CAMPAIGN_CONTRACT.md`.
3. If unbound, there is no campaign to portray. Route a new-game or load request below; otherwise state readiness briefly.
4. For a bound v0.7 run, confirm the save and accepted agreement name the same campaign and module, the save has a positive revision and identity, and its five present sections and the agreement's five substantive terms are readable. Missing control/initiative terms require repair; do not infer a grant. An older field-only save needs `ADMIN/UPGRADE_V07.md`; do not silently reinterpret it. Detailed schema inspection belongs to ADMIN.
5. Check that the bound ENGINE entrypoint and `pc_record` exist without preloading their bodies. The engine resolves to exactly one of `ENGINE/<engine>.md` or `ENGINE/<engine>/ENGINE.md`. Safe ids start with a letter/digit and contain only letters/digits/dot/underscore/hyphen; no traversal or absolute path. Follow only campaign-local record paths.
6. Read `MODULES/<module>/SETTING_BRIEF.md`. Its identity must match and its world orientation must be usable. Require `safety_state` to be exactly `floor-only` or `active`; a missing/invalid flag requires repair. Read `INSTANCE/SAFETY.md` when active; that requires real limits. Presentation is already accepted in the agreement. Do not load POLICY or Bearing during ordinary startup.
7. Orient to Situation, Character state, Open matters, Active processes, and Relevant records. Follow private watch or other detailed pointers only when the present task calls for them. Resolve essential conflicts before fiction; harmless extra metadata or heading order alone need not prevent play.

## Respond

If asked to continue, resume the recorded moment and ongoing declaration within accepted delegation. No second "begin" command is needed. Do not invent elapsed time, erase a pending choice, or automatically restart a resolved scene. If asked only to check readiness, report readiness without fiction.

Exact PC values, detailed lore, subsystem bodies, and historical evidence remain available through targeted retrieval. If files cannot actually be read or written, explain and use the export workflow in INSTALLATION; never claim workspace memory from attachments alone.

## Route ordinary requests

| Request or alias | Procedure |
|---|---|
| Start a new game / NEW GAME | `ADMIN/NEW_GAME.md` |
| Use an existing module / LOAD MODULE | `ADMIN/LOAD.md` |
| Save / CLOSE / END SESSION | `ADMIN/CLOSE_CONTRACT.md` |
| Quick present-only save / CHECKPOINT | Checkpoint section in that procedure |
| Correct that / revise an established fact | `ADMIN/CORRECT.md` |
| Change how we play / RECALIBRATE | `ADMIN/RECALIBRATE.md` |
| Review the campaign / REVIEW | `ADMIN/REVIEW.md` |
| Upgrade an older campaign | `ADMIN/UPGRADE_V07.md` |
| Add or refine the world brief | `ADMIN/ADD_SETTING_BRIEF.md` or `ADMIN/REFINE_SETTING_BRIEF.md` |
| Check the files / VALIDATE | `ADMIN/VALIDATE.md` |

Recognize clear natural-language intent. Explicit acceptance of a displayed proposal is sufficient; a particular token is not required. Retrieve other maintenance instructions only for that task. AUDIT reports only files/actions actually observed, with uncertainty about anything not verified.
