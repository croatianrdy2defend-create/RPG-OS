# ADMIN — Change the campaign agreement

Use for an explicit recalibration request or a natural request to change how future play runs. Read bound CURRENT_SAVE and its matching accepted CAMPAIGN_CONTRACT. Resolve pending recovery first. A legacy-shaped run uses `ADMIN/UPGRADE_V07.md` before its agreement is rewritten.

The editable surface is **Campaign promise; Player control; GM initiative; Time and transitions; Presentation**. This includes concrete routine grants, structural progression, initiative limits, compression, voice, and guidance. A style label does not grant PC control; permission is not a quota.

Engine/module identity, established fiction, PC values, archive evidence, and operator safety have separate procedures. A new operator limit applies immediately; it does not wait for this edit.

## Procedure

1. Show each affected existing clause and proposed replacement, with its prospective effect. Preserve unaffected clauses. If the player supplied the exact replacement or already accepted the displayed proposal, do not ask again. Otherwise obtain ordinary explicit acceptance; no special phrase is required.
2. If nothing materially changes, write nothing. Otherwise follow `ADMIN/RECOVERY.md` before mutation, including verified preimages and candidate paths.
3. Build a candidate under `INSTANCE/_SCHEMA.md`: preserve campaign/module identity and unchanged content; assign a new unique `contract_id`; increment `contract_rev`; set `contract_parent` to the prior id; use `status: candidate` while checking.
4. Check all five sections remain clear and compatible, every new grant is accepted, and no prepared scene or inferred player desire became an obligation. Set the publishable record to `status: accepted`, publish/read it back, and complete recovery. On failure, recover; never operate under a half-written agreement.

Changes apply from acceptance forward. They do not rewrite earlier PC choices, outcomes, clocks, state, or archive history. Optional Bearing tied to the old contract becomes stale; do not regenerate it or run REVIEW automatically. Report the new revision and changed clauses plainly.
