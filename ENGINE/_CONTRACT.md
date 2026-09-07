# Engine contract — v0.8.1

An ENGINE supplies rules, not a setting, narrative voice, or campaign agreement. Any commercial, open, oracle-driven, or freeform system can be used when its required procedures and values are available. The kit ships only Freeform.

## Identity and contents

Use exactly one `ENGINE/<id>.md` or `ENGINE/<id>/ENGINE.md`. Scalar front matter includes:

- `id`, matching the flat filename stem or containing directory.
- `class: engine` exactly.
- `character_build_support`: `self-contained`, `operator-values-required`, or `no-mechanical-sheet`.

Ids use ASCII letters, digits, `.`, `_`, `-`, begin with a letter or digit, and contain no separators/traversal. Never install both forms for the same id or count aliases as engines.

The body states:

- How uncertainty is resolved and which procedures are actually supplied.
- How genuinely random results are obtained when required: an available real randomizer or player-provided results. No compulsory helper script; never report an invented model number as an actual roll.
- Character fields required before bind, permitted deferrals with their conditions, and optional fields.
- A compact creation order, or where the operator must supply procedures/values.
- When to retrieve this adapter or its specific subprocedures.
- Any relevant source/version and honest coverage limits.

A self-contained adapter supplies the advertised creation procedure and inputs/options needed for that scope. Operator-values-required may guide the order without claiming unavailable costs/tables. No-mechanical-sheet offers a profile instead of a fictitious full sheet.

## Setup and play

A substantive accepted PC record is always required, but a full mechanical sheet is required only when this engine and the opening need it. Values may be derived only from available procedures and inputs. Missing later-required values prompt narrow clarification instead of invention.

Campaign depth, GM initiative, routine delegation, compression, and presentation do not change resolution or supply missing stats. Conversely a rule does not grant unrelated authority over the PC. Involuntary effects and voluntary choices remain distinguished by the accepted rules and agreement.

An explicitly accepted fixed outcome or structured destination defines what is already settled within its scope; do not offer that result as an open roll or judgment. Resolve genuinely open matters with this engine. A fixed-scope agreement is not permission to falsify a roll, silently change a resolution procedure, or decide a reserved PC choice. Genuine mechanical errors remain correctable under ironman; dissatisfaction with a valid outcome is not an error.

MODULE names the installed engine. RULES_HOOKS may clarify compatible usage; an actual change to resolution or character rules needs a distinct engine id. Later explicit rulings remain in INSTANCE/CORRECTIONS.md.

## Independent establishment and generation

Use `OS/AGENT_STATE.md` for a materially unresolved agent establishment/change task. Opportunity selection, initialization of an eligible individual fact and resolution of an attempt are separate procedures. Existing fixed facts and deliberately open triggers retain their scope; no agent-state feature installs a universal reaction or relationship table.

A supplied optional generator states the context/population, eligible dimensions, constraints, outcome meanings, actual random-input method and establishment scope. Select the compatible procedure and mapping before obtaining its result. Hard constraints restrict eligible outcomes; conditional or correlated dimensions may preserve coherence. Preserve the obtained result and method at the scope needed for later retention. Do not reroll, remap or change contextual modifiers to satisfy an OOC hope or make play artificially difficult.

Use this engine's authorized judgment when no random method is selected. If a requested random method lacks a real source, obtain a player-supplied result or agree an alternative; model token sampling is not a reported die roll. A seed is useful only with the retained algorithm, inputs and mapping. A changed generator governs eligible future establishments, not existing people. An unchanged resolved opportunity gets no extra draw merely because it is queried more often; a new cause or eligible interval follows its governing procedure.

These procedures neither grant PC authorship nor authorize PLAY writes. Ordinary functional exchanges need no extra roll, record or subsystem. Existing record owners and requested save/checkpoint procedures retain established results; unsaved private state remains best-effort context.

## Locality and sources

Keep a compact adapter in one entrypoint. Split independently needed mechanics into explicit narrow routes under `ENGINE/<id>/` when useful; do not create empty hierarchies or duplicate procedures in indexes. Retrieve only the procedure relevant now.

Keep adapters to compact procedures and field requirements. Do not paste or reconstruct commercial books, chapters, bulk spell/equipment lists, or source tables. Use supplied values and accessible owned sources honestly; installation does not imply permission to redistribute third-party text. Missing source support stays visible rather than being replaced by model confidence.
