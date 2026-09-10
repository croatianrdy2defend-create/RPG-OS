# RPG OS v0.9.5 startup

Load a campaign when asked to run, resume, or set one up. Development and review requests do not start PLAY.

## Load

1. Check the exact path `RECOVERY/ACTIVE.md`. If present, leave PLAY idle and open `ADMIN/RECOVERY.md`; reconcile an interrupted operation before continuation. Absence is normal. Do not inventory the recovery folder.
2. Read `OS/LAW.md`, `INSTANCE/CURRENT_SAVE.md`, and `INSTANCE/CAMPAIGN_CONTRACT.md`.
   Before ordinary PLAY, also check the exact path `HANDOVER/ACTIVE.md`. If present, keep source play paused and open `ADMIN/SCENE_HANDOVER.md`. An explicit request to receive that named package selects the receiving-GM procedure; an ordinary resume request does not claim that role. Return/import, cancellation and malformed markers are handled there. Recovery always takes priority. If absent, do not scan handover history.
3. If unbound, there is no campaign to portray. Route a new-game or load request below; otherwise state readiness briefly.
4. For a bound run, confirm the save and accepted agreement name the same campaign and module, the save has a positive revision and identity, and its five present sections and the agreement's five substantive terms are readable. Require the agreement's Play form, Form selection, Structure disclosure, Cuts, and Retcon clauses from LAW. Missing or conflicting terms need focused RECALIBRATE supplementation before PLAY; do not infer a grant or assume a chosen form from genre. An older field-only save instead needs `ADMIN/UPGRADE_V07.md`. Detailed schema inspection belongs to ADMIN.
5. Check that the bound ENGINE entrypoint and `pc_record` exist without preloading their bodies. The engine resolves to exactly one of `ENGINE/<engine>.md` or `ENGINE/<engine>/ENGINE.md`. Safe ids start with a letter/digit and contain only letters/digits/dot/underscore/hyphen; no traversal or absolute path. Follow only campaign-local record paths.
6. Read `MODULES/<module>/SETTING_BRIEF.md`. Its identity must match and its world orientation must be usable. Require `safety_state` to be exactly `floor-only` or `active`; a missing/invalid flag requires repair. Read `INSTANCE/SAFETY.md` when active; that requires real limits. Presentation is already accepted in the agreement. Do not load POLICY or Bearing during ordinary startup.
7. Orient to Situation, Character state, Open matters, Active processes, and Relevant records, plus the administrative Session continuity section when present. The latter distinguishes active, closing and ended play; `none` means not started and absence means legacy/unrecorded, not an unpaid award. Follow private watch or other detailed pointers only when the present task calls for them. Resolve essential conflicts before fiction; harmless extra metadata or heading order alone need not prevent play.
8. Only if the accepted agreement explicitly enables autosave, follow `ADMIN/AUTOSAVE.md` for its cadence and advance notice. Absent policy means off, not a missing required field. A clean boot from a verified save starts its operational count at zero; never invent an old warning or unsaved state. Recovery and handover still take priority. No context-meter access is assumed.

## Respond

For an actual request to begin or resume PLAY, follow `ADMIN/SESSION.md` after this loading and recovery/handover precedence. It recovers causal context, explicit feedback, relevant preparation and any genuinely due engine beginning procedure while preserving the exact stopping point. A readiness check, feedback alone or development work starts no session. Return here only for an unmet loading requirement; SESSION's reference to normal boot does not recursively restart the loader.

For every PLAY response, including the first after loading, execute LAW's `Prime directive — every PLAY response`: Understand → Establish → Resolve → Portray, in that order. Startup supplies the initial authorities; it does not replace the procedure on later turns.

If asked to continue, resume the recorded moment and ongoing declaration within accepted delegation, including an explicitly applicable Cuts grant. No second "begin" command is needed. Without that grant, preserve lived continuity and uncommitted time. A cut does not invent elapsed events or decide a reserved pending choice; keep its unresolved facts and consequences honest. Do not automatically restart a resolved scene. If asked only to check readiness, report readiness without fiction.

Exact PC values, detailed lore, subsystem bodies, and historical evidence remain available through targeted retrieval. If files cannot actually be read or written, explain and use the export workflow in INSTALLATION; never claim workspace memory from attachments alone.

## Route ordinary requests

| Request or alias | Procedure |
|---|---|
| Start a new game / NEW GAME | `ADMIN/NEW_GAME.md` |
| Use an existing module / LOAD MODULE | `ADMIN/LOAD.md` |
| Save / bare CLOSE | `ADMIN/CLOSE_CONTRACT.md` |
| End the session / save and end / END SESSION | `ADMIN/SESSION.md`, including the full save |
| Quick present-only save / CHECKPOINT | Checkpoint section in that procedure |
| Enable/disable autosave, delay/resume a pending autosave | `ADMIN/AUTOSAVE.md`; persistent policy changes use `ADMIN/RECALIBRATE.md` |
| Hand this scene to another GM / SCENE HANDOVER | `ADMIN/SCENE_HANDOVER.md` — prepare |
| Continue from this handover | `ADMIN/SCENE_HANDOVER.md` — receive |
| Import the scene return / RETURN SCENE | `ADMIN/SCENE_HANDOVER.md` — import |
| Cancel the handover | `ADMIN/SCENE_HANDOVER.md` — cancel |
| Correct that / revise an established fact | `ADMIN/CORRECT.md` |
| Change how we play / RECALIBRATE | `ADMIN/RECALIBRATE.md` |
| Review the campaign / REVIEW | `ADMIN/REVIEW.md` |
| Upgrade this campaign | `ADMIN/UPGRADE_V08.md` — routes older formats through the existing v0.7 mapping when needed |
| Add or refine the world brief | `ADMIN/ADD_SETTING_BRIEF.md` or `ADMIN/REFINE_SETTING_BRIEF.md` |
| Check the files / VALIDATE | `ADMIN/VALIDATE.md` |
| Read an exact source section / build or use scoped search | `ADMIN/SOURCE_ACCESS.md` |
| Capture this session export / audit a save against source | `ADMIN/EVIDENCE_AUDIT.md` |

Recognize clear natural-language intent. Explicit acceptance of a displayed proposal is sufficient; a particular token is not required. Retrieve other maintenance instructions only for that task. AUDIT reports only files/actions actually observed, with uncertainty about anything not verified.
