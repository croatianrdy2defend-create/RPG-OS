# Engine contract — v0.8.2

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
- Applicable lifecycle procedures, including beginning/end boundaries, or an explicit statement that none are supplied; identify their source, triggers, required inputs, effect owners and player choices.
- When to retrieve this adapter or its specific subprocedures.
- Any relevant source/version and honest coverage limits.

A self-contained adapter supplies the advertised creation procedure and inputs/options needed for that scope. Operator-values-required may guide the order without claiming unavailable costs/tables. No-mechanical-sheet offers a profile instead of a fictitious full sheet.

## Setup and play

A substantive accepted PC record is always required, but a full mechanical sheet is required only when this engine and the opening need it. Values may be derived only from available procedures and inputs. Missing later-required values prompt narrow clarification instead of invention.

Campaign depth, GM initiative, routine delegation, compression, and presentation do not change resolution or supply missing stats. Conversely a rule does not grant unrelated authority over the PC. Involuntary effects and voluntary choices remain distinguished by the accepted rules and agreement.

An explicitly accepted fixed outcome or structured destination defines what is already settled within its scope; do not offer that result as an open roll or judgment. Resolve genuinely open matters with this engine. A fixed-scope agreement is not permission to falsify a roll, silently change a resolution procedure, or decide a reserved PC choice. Genuine mechanical errors remain correctable under ironman; dissatisfaction with a valid outcome is not an error.

MODULE names the installed engine. RULES_HOOKS may clarify compatible usage; an actual change to resolution or character rules needs a distinct engine id. Later explicit rulings remain in INSTANCE/CORRECTIONS.md.

## Lifecycle procedures

`ADMIN/SESSION.md` routes actual play-session beginnings and endings to this engine. Identify each supplied procedure's real trigger and timing, source, required inputs, resulting current owner, and unresolved player choices. Session completion, scenario completion, rest and downtime are distinct triggers when the rules distinguish them. Supply no universal XP scheme, healing reset, world tick or award cadence. Settle any campaign-dependent application prospectively within the accepted rules and agreement.

Adjudicate separately from persistence. Keep a settled application, including a zero result or a ruling of inapplicability where relevant, with its play-session/boundary/rule identity at the selected effect owner and preserve available evidence. Beginning and ending applications are distinct even when the rule name matches. An active resume may complete an expressly pending procedure but creates no new beginning trigger. Saves, retries, chats, handovers and repeated end requests do not repeat an application; prospective legacy identity adoption alone proves no earlier trigger. Missing sources or a missing application record are not permission to guess an effect or award again.

Awarding resources is separate from choosing how to spend them. Preserve required player selections and unavailable rules or inputs as precise pending items; resolve no dependent action without what its rule requires. Use existing current owners and authorized persistence, with outstanding administrative routes in Session continuity. PREP owns neither a balance nor the sole proof of application. References may be compacted only into surviving evidence, not erased at the next session boundary.

## Independent establishment and generation

Use `OS/AGENT_STATE.md` for a materially unresolved agent establishment/change task. Opportunity selection, initialization of an eligible individual fact and resolution of an attempt are separate procedures. Existing fixed facts and deliberately open triggers retain their scope; no agent-state feature installs a universal reaction or relationship table.

A supplied optional generator states the context/population, eligible dimensions, constraints, outcome meanings, actual random-input method and establishment scope. Select the compatible procedure and mapping before obtaining its result. Hard constraints restrict eligible outcomes; conditional or correlated dimensions may preserve coherence. Preserve the obtained result and method at the scope needed for later retention. Do not reroll, remap or change contextual modifiers to satisfy an OOC hope or make play artificially difficult.

Use this engine's authorized judgment when no random method is selected. If a requested random method lacks a real source, obtain a player-supplied result or agree an alternative; model token sampling is not a reported die roll. A seed is useful only with the retained algorithm, inputs and mapping. A changed generator governs eligible future establishments, not existing people. An unchanged resolved opportunity gets no extra draw merely because it is queried more often; a new cause or eligible interval follows its governing procedure.

These procedures neither grant PC authorship nor authorize PLAY writes. Ordinary functional exchanges need no extra roll, record or subsystem. Existing record owners and requested save/checkpoint procedures retain established results; unsaved private state remains best-effort context.

## Locality and sources

Reusable, non-selectable mechanics helpers may live under `ENGINE/_shared/` and must be explicitly routed by a selecting adapter. They are not another engine identity or an automatic default. Keep setting populations, current people, occupations, places and source bindings in the selected MODULE/INSTANCE owners; the shared helper receives their relevant facts. A direction-based generator fixes eligibility and the meaning of direction before input, then the GM authors the concrete eligible state before dependent behavior. It requires no prewritten state catalogue.

Keep a compact adapter in one entrypoint. Split independently needed mechanics into explicit narrow routes under `ENGINE/<id>/` when useful; do not create empty hierarchies or duplicate procedures in indexes. Retrieve only the procedure relevant now.

Keep adapters to compact procedures and field requirements. Do not paste or reconstruct commercial books, chapters, bulk spell/equipment lists, or source tables. Use supplied values and accessible owned sources honestly; installation does not imply permission to redistribute third-party text. Missing source support stays visible rather than being replaced by model confidence.
