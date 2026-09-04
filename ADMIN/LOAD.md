# LOAD — bind an existing module

Operator-side. Not PLAY. Not New Game.

Open only after an explicit **LOAD MODULE** request naming a module that already exists under `MODULES/`.

## Procedure

0. If CURRENT_SAVE `engine`/`module` is not unbound, **stop**. Do not overwrite a live run. Operator must use a separate folder/instance. Never empty ARCHIVE.
   If CURRENT_SAVE is unbound but ARCHIVE contains any campaign row, ledger row, session folder, or other prior-run evidence, or INSTANCE contains non-template registers/overlays or an unexpected path, also stop. Use a clean separate kit copy; never clear or inherit prior-run state.
   This guard authorizes one bounded ADMIN inventory of `ARCHIVE/` and `INSTANCE/` only; it does not authorize PLAY discovery or a repository-wide lore scan.
   Before resolving the operator-named module path, require a portable safe module id: ASCII letters, digits, `.`, `_`, and `-` only, beginning with a letter or digit; no slash, backslash, whitespace, absolute path, or traversal. Otherwise stop without constructing a path.

1. Confirm `MODULE.md`, `POLICY.md` (voice declared), `CHAR/PC.md`, `T0_SAVE.md` exist. Prefer the v0.4 descriptor grammar and exact `## Voice` heading. If the shipped script inspects a legacy descriptor, its provenance remains `SCRIPT-VERIFIED` and its result remains `INCOMPLETE`; any separate manual confirmation is `MODEL-CHECKED` and cannot upgrade that script result into a complete PASS.
2. Confirm the engine id in MODULE.md is itself a portable safe id and equals an installed engine with exact scalar `class: engine`, whose scalar front-matter `id` matches the flat filename stem in `ENGINE/<id>.md` or the containing directory name in `ENGINE/<id>/ENGINE.md`. Require scalar front matter `character_build_support: self-contained`, `operator-values-required`, or `no-mechanical-sheet`. Do not treat aliases or pointers as engines.
3. If voice is missing: not runnable. Stop.
4. Open MODULES/_CONTRACT.md, ENGINE/_CONTRACT.md, and INSTANCE/_SCHEMA.md. Run the validation checklist:

   - required module files present
   - exact `## Voice` heading present; for a legacy heading, manual confirmation is recorded while scripted coverage stays `INCOMPLETE`
   - v0.4 MODULE scalar front matter and exact capability table parse; for a legacy descriptor, manually confirm identity and every declared capability while scripted coverage stays `INCOMPLETE`
   - engine id resolves to exactly one file
   - the engine's required/deferred/optional character field groups and support class are readable; every nondeferrable bind field exists in the PC entrypoint/bundle, and every deferred field is both permitted by the engine and unnecessary to the accepted opening mechanics
   - every declared optional capability has an existing target entrypoint and at least one real authoritative body; an empty index does not pass
   - T0_SAVE contains the identity and present fields needed for bind (`engine`, `module`, `immediate_scene`, plus the v0.6 orientation fields); for a legacy T0 that lacks an orientation field, record the omission and require an explicit operator-accepted bind value rather than modifying MODULE or guessing
   - T0 `immediate_scene` is a playable, oriented starting frame with handback before any voluntary PC act and does not smuggle an unaccepted prior promise, crime, intimacy, purchase, risk, or commitment; a quiet frame or genuine solitude is valid, and no incident/hook is required
   - PC persona/background grants no standing GM authorship; every fact/value is supplied/accepted or explicitly unspecified, and mutable opening status agrees with T0 rather than duplicating a competing present
   - every `declared_state_flags` live-system cue names only a compact nonsecret id, causal/due-check condition, and resolvable declared capability/section route; any mutable capability marked initially implicated but not otherwise recognizable has such a cue, and a campaign with later independently live private systems reserves the optional field even if its T0 value is `none`
   - every mutable-system authoritative body stores readable triggers/non-triggers, selected post-change current route, cue lifecycle where applicable, and any dependency/update order it owns; any RULES_HOOKS declaration remains calibration rather than an ENGINE contradiction
   - detailed current resources, schedules, and mutable sheet values have one selected authority and no competing total
   - any machine-marked PC routing index reaches only non-placeholder Markdown bodies under that module's `CHAR/` tree; the exact transitive bundle contains no unrelated sibling
   - private bodies are checked only for required structure and reachable payload without printing their contents; sealed authoring never authorizes regeneration or disclosure during LOAD

   If any required check fails, or a legacy field lacks manual confirmation: not runnable. Do not bind. Manual confirmation may establish that a legacy module is runnable; it does not convert the script's structural result into PASS.

5. Establish the **run campaign contract**, including for a legacy module. MODULE/POLICY may propose defaults; they do not become accepted settings merely because they were loaded. Ask the operator to review and explicitly accept:

   - a compact `campaign_promise` that carries the accepted play experience and material tone/cadence, plus a `fit_envelope` that carries compatible material, exclusions, and routine anti-attractors, with no plot destination;
   - six independent axes: `structural_direction`, `gm_initiative`, `pressure_incident_density`, `time_handling`, `development_priorities`, and `guidance_visibility`;
   - `creative_mandate`, separately set to `off` or `on`; when on, separately accept `creative_mandate_scope` and `creative_mandate_boundaries`;
   - `review_mode`: exactly `off` or `bearing-only`.

   Do not infer initiative from pressure, direction from genre, a creative mandate from any axis, or player interest from authored module content. A boundary is an opportunity, not a warrant. `bearing-only` enables an optional later REVIEW; it does not activate seeds or create preparation. Show the complete proposed run contract and require explicit accept or revision before any write.
6. Ask whether this run has operator-specific safety extras beyond LAW. Write only explicitly accepted Hard-no/Fade sentences into INSTANCE/SAFETY.md and set `safety_state` accordingly (`active` only with at least one real sentence). Module-imposed stronger restrictions remain in POLICY and are not copied into the per-run safety file.
7. Compile the T0 orientation fields. Preserve supplied values. For a legacy T0, explicitly confirm any missing `scene_status`, `uncommitted_time`, exact `pc_declared_goals`, and established `causal_frontier`; use `none` when none is honestly established. Do not infer PC goals from persona/background or OOC preference, and do not put campaign interpretation or prepared possibilities in the causal frontier.
8. Assign a new unique portable `campaign_id`, a new safe `contract_id`, and a new safe `save_id`. Build the explicitly accepted contract at `INSTANCE/CAMPAIGN_CONTRACT.candidate.md` with the same campaign id, `contract_rev: 1`, `contract_parent: none`, `status: candidate`, and all other identity fields required by INSTANCE/_SCHEMA.md. Copy T0 into `INSTANCE/CURRENT_SAVE.candidate.md`; set `save_rev=1`, `save_parent=none`, `commit_kind=bind`, `archive_ref=none`, and compile every required orientation field. Reset `INSTANCE/BEARING.md` to the bound-empty shape: the new `campaign_id`, `status: none`, every base/evidence value `none` or `0` as specified by the schema, and every section `none`. This identity-only reset is not REVIEW content.
9. Copy the exact PC bundle rooted at `MODULES/<id>/CHAR/PC.md` to matching paths under `INSTANCE/CHAR/`, preserving bytes and relative paths. Point `pc_record` to `INSTANCE/CHAR/PC.md`. Do not copy unrelated CHAR siblings.
10. Initialize the canonical empty instance registers (NOW, KNOWN, CAST_STATUS, CORRECTIONS). Do not bulk-copy opening clocks, seeds, factions, institutions, people, or other optional bodies into INSTANCE, and do not create undiscoverable standalone status files. Accepted MODULE mutable baselines are immutable as-of-T0 snapshots, not permanent current claims. One specifically named snapshot may support current continuity only when the selected current authority and chat have no later value and no declared causal transition has occurred or is due. PLAY keeps later accepted change in chat RAM. At the next explicit CHECKPOINT/CLOSE, ADMIN applies unsaved transitions exactly once in the selected destination: NOW/person route, CURRENT_SAVE candidate, or PC bundle, and maintains only the cross-boot cues still required. A MODULE person's `## NOW` / `## PC` follows the same temporal rule. Do not activate or promote merely because a baseline exists.
11. Validate both Campaign Contract and CURRENT_SAVE candidates against INSTANCE/_SCHEMA.md, including matching campaign/module identity, contract enums, whitelist, overlay, safety, and present/orientation fields. If either is invalid, do not replace CURRENT_SAVE. Otherwise set the publishable contract to `status: accepted`, recheck it, publish it immediately before replacing CURRENT_SAVE, then replace CURRENT_SAVE with its candidate last and remove both candidate files.
   If any write, provider response, or generation is interrupted before replacement, the unbound save remains authoritative but partial contract/SAFETY/INSTANCE/candidate artifacts may exist. Do not call the module bound and do not start PLAY. Either complete only the already accepted load operation and validate the entire bind, or inspect and restore the clean pre-bind copy required by P19 before retrying. Do not claim automatic rollback.
12. Do **not** clear ARCHIVE. Step 0 requires an empty run archive before bind; prior history belongs in its original folder.
13. Tell the operator to start PLAY in a **fresh** chat with the accepted Campaign Contract and Current Save. A matching Bearing does not exist yet and is not required. Confirm `contract_id` and `save_id`.

Do not regenerate the module from a questionnaire.
Load only a module that already exists under MODULES/. This clean kit starts with none.
