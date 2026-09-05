# ADMIN — Change the campaign agreement

Use for an explicit recalibration request or a natural request to change how future play runs. Read bound CURRENT_SAVE and the matching stored agreement; verify their identities and existing accepted content. Resolve pending recovery first. Older state/contract shapes use `ADMIN/UPGRADE_V07.md`. A v0.7 five-section agreement missing the new named clauses is specifically eligible for focused supplementation here: do not require those clauses or a complete v0.7.1 validator PASS before starting this repair, and do not migrate/reset its state.

The editable surface remains **Campaign promise; Player control; GM initiative; Time and transitions; Presentation**. This includes concrete grants, structural progression, initiative, cuts, retcon, voice, and guidance. A style label does not grant PC control; permission is not a quota.

Every completed v0.7.1 agreement includes exactly one substantive clause in each assigned section: `Play form:` in Campaign promise; `Form selection:` in GM initiative; `Structure disclosure:` in Presentation; `Cuts:` in Time and transitions; `Retcon:` in Player control. Use NEW_GAME's meanings and proposed defaults, but never blanket-apply defaults to an existing run or infer missing grants. Preserve explicit accepted terms; show focused supplements or faithful clause labels for acceptance.

Engine/module identity, established fiction, PC values, archive evidence, and operator safety have separate procedures. A new operator limit applies immediately; it does not wait for this edit.

## Procedure

1. Show each affected existing clause or omission and proposed replacement/supplement, with its prospective effect. Preserve unaffected content. Form selection and nondisclosure are separate grants. Under accepted opacity, show the truthful delegation envelope rather than revealing a concealed choice; never manufacture a false form claim. If the player supplied the exact replacement or already accepted the displayed proposal, do not ask again. Otherwise obtain ordinary explicit acceptance; no special phrase is required.
2. If neither accepted content nor required clause formatting changes, write nothing. Otherwise follow `ADMIN/RECOVERY.md` before mutation, including verified preimages, candidate paths, and any directory creation.
3. Build a candidate under `INSTANCE/_SCHEMA.md`: preserve campaign/module identity and unchanged content; assign a new unique `contract_id`; increment `contract_rev`; set `contract_parent` to the prior id; use `status: candidate` while checking.
4. Check all five sections and correctly placed named clauses remain clear and compatible. Every new grant must be accepted; a prepared possibility or inferred desire does not become an obligation by editing. An explicitly accepted structured destination/fixed outcome may be recorded within scope, without fake open rolls or overriding reserved choices. Cuts default to lived continuity unless a bounded hardcut grant is accepted. Retcon distinguishes OOC rewind from accepted ironman for valid outcomes; genuine error correction, stopping, and depiction changes remain separate. Set the publishable record to `status: accepted`, publish/read it back, and complete recovery. On failure, recover; never operate under a half-written agreement.

Changes apply from acceptance forward. They do not rewrite earlier PC choices, outcomes, clocks, state, or archive history. Optional Bearing tied to the old contract becomes stale; do not regenerate it or run REVIEW automatically. Report the new revision and changed clauses plainly.

An off-premise proposal is handled OOC by agreeing a return, recalibration, or ending; do not enforce the old premise with fabricated world barriers. Recalibration alone does not reverse a prior valid ironman outcome. Any separate retrospective change requires its own explicit treatment under the accepted Retcon policy and correction procedure.
