# Engine contract

An ENGINE is a ruleset plugin. It is not the OS, a campaign, or the Campaign Contract.

The OS does not assume any particular commercial, open, oracle-driven, or freeform system.
A playable bound run names an installed engine in CURRENT_SAVE. If that file is missing, the instance is not runnable.
Campaign promise, structural direction, initiative, pressure, time handling, development priorities, guidance, creative mandate, and REVIEW mode never come from ENGINE. Conversely, none of those contract settings changes an ENGINE resolution procedure, supplies a missing character value, or authorizes the GM to decide the PC's voluntary conduct.

## Required file

`ENGINE/<id>.md` or `ENGINE/<id>/ENGINE.md`

Must state scalar front matter `id`, `class: engine`, and `character_build_support`:

- `id` (example: `dice_pool`, `oracle`, `pbta`, `freeform`)
- `class: engine` (exact; pointer/alias files are not engines)
- how uncertainty is resolved (dice, moves, oracle, none)
- which PC-sheet fields exist and must be retrieved, never guessed
- which character field groups are required before bind, which may be deferred until a subsystem enters play, and which are optional
- a compact guided-build order, or an explicit statement that creation procedures/values must be supplied by the operator
- `character_build_support`: exactly `self-contained`, `operator-values-required`, or `no-mechanical-sheet`
- when this file should be opened
- that it contains no setting, no NPC names, no literary voice

## Character creation support

A completed mechanical sheet is optional during NEW GAME unless the selected ENGINE explicitly requires one before the chosen kind of play can begin. The stable `CHAR/PC.md` baseline is still required and must contain substantive operator-approved material.

If the operator chooses a guided or full build, SETUP follows only this engine's declared field groups and procedure, one group at a time. It may derive a value only when both the procedure and inputs are present. It never invents values, silently chooses options, or reconstructs missing rules.

The engine must distinguish:

- fields required before bind;
- fields that may remain deferred until a named subsystem enters play;
- optional character/profile fields.

If later adjudication requires a deferred value, pause and ask rather than guess. For a commercial system whose creation rules are not lawfully present, request operator-supplied values, an imported sheet, or reference to an owned source; do not reproduce its tables or catalogues.

NEW GAME's initial engine summary states the support class and what that means before the operator chooses a sheet path. `operator-values-required` may guide the order but cannot supply missing costs/tables; `no-mechanical-sheet` must say that Guided full sheet is unavailable rather than pretending to build one.

## Identity

For a flat engine, the filename stem in `ENGINE/<id>.md` must equal the scalar front-matter `id`. For a directory engine, the containing directory name in `ENGINE/<id>/ENGINE.md` must equal that `id`.
New ids are portable safe tokens: ASCII letters, digits, `.`, `_`, and `-` only, beginning with a letter or digit. No slash, backslash, whitespace, absolute path, or traversal segment.
Do not list alias, pointer, or README files as engines.
The bundled public-release engine is `freeform` → `ENGINE/freeform.md`.

## Optional

`ENGINE/<id>/` extra sections (combat, magic, vehicles) retrieved only when that question exists.

## Retrieval locality

Keep a compact engine in its required root file. If mechanics or extensions become large and are normally needed independently, the root file remains the declared entrypoint/capability map and points explicitly to narrower authoritative files or named sections under `ENGINE/<id>/`.

Split by independent retrieval relevance, not by an arbitrary size threshold. Do not prebuild empty rules hierarchies. An index routes to procedure; it does not duplicate the procedure, and a cross-link does not authorize unrelated retrieval.

PLAY opens only the mechanic required by the present adjudication. It does not browse neighboring rule files.

## Bound module

`MODULE.md` names `engine: <id>`. ADMIN will not bind a module to an engine that is not installed.

A MODULE `RULES_HOOKS` capability may clarify or calibrate use of the bound ENGINE but cannot contradict it. Neither MODULE Campaign defaults nor the accepted run contract can override it. A real change to resolution or character rules uses a distinct compact ENGINE id. Later explicit table rulings live in `INSTANCE/CORRECTIONS.md`.

## Copyright / compactness

Procedure + sheet fields only. Do **not** paste a copyrighted rulebook.
This constraint applies to the initial draft **and every later addition** to an engine file.
If uncertain, ask the operator; do not reconstruct a book.
No bulk spell lists, equipment catalogs, or chapter reconstructions.

## Bundled examples

This public pack ships `ENGINE/freeform.md` only.
You may add a compact engine for another ruleset the same way you add a module, using procedures and values you are entitled to use. Do not edit LAW to teach the new dice, and do not redistribute third-party rule text without permission.
