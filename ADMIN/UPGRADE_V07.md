# Upgrade an existing campaign to v0.7

Cold ADMIN procedure. Upgrading preserves a campaign; it never starts a new one or resets history. Support standard v0.6-series records and explicitly mapped older/custom records. Do not claim an unexamined private format is automatically compatible.

## Before changing files

Use the old compatible runtime to save outstanding accepted play, then keep a restorable complete copy of the old campaign and runtime. Work in a separate upgrade copy as described in INSTALLATION. Do not overwrite campaign-owned INSTANCE, ARCHIVE, module bodies, or custom engine adapters with blank kit templates.

Check RECOVERY/ACTIVE.md first. Reconcile any pending operation under ADMIN/RECOVERY.md. Read the preserved current save, agreement if present, relevant old schema, module descriptor/brief/policy, active limits, and selected current record pointers. Do not load private lore or the whole archive just to upgrade.

Identify the actual source version/layout. If accepted play is missing from the saved material, return to its source before conversion or state exactly what evidence is unavailable. Do not reconstruct it from inferred memory.

## Map the present

Build a v0.7 candidate under INSTANCE/_SCHEMA.md, retaining campaign, module, engine, character routes, exact current facts, and applicable limits.

| Older information | v0.7 destination |
|---|---|
| time and place | datetime/place metadata, retaining original units and uncertainty |
| immediate_scene, scene_status, status, uncommitted_time | Situation: actual frame, ongoing declaration, unresolved choice, and remaining/unknown time |
| tracked_resources and material PC conditions | Character state, with detailed records still authoritative at their scope |
| pc_declared_goals, appointments, known_open_matters | Open matters, preserving source and distinctions between goals and obligations |
| causal_frontier and live declared_state_flags | Active processes, preserving triggers, due conditions, private non-revealing pointers, and retirement conditions |
| hot_identifiers and other useful routes | Relevant records, with current correction pointers where applicable |
| prior archived evidence boundary | archive_ref and evidence_through independently of the latest present-only checkpoint |

The old checkpoint may have archive_ref=none despite earlier complete saves. Inspect the compact ARCHIVE/INDEX to locate the latest supported full evidence boundary for this run. Do not infer coverage beyond its records. Retain older archives unchanged, including legacy monolithic scenes. If no archived close exists, set both metadata values to `none` and describe any source gap in prose. If archived rows exist but their boundary cannot be resolved, repair or clarify the routing before publication; do not clear that history or use `unavailable` as a pseudo-id.

Assign a new save id, increment the prior save revision, and name its prior id as parent. The upgrade is a checkpoint: it changes present representation and retains the established historical evidence boundary. If the old record lacks usable lineage, show the proposed explicit lineage mapping and preserve the source identity in the upgrade record; obtain clarification/acceptance rather than claiming continuity that cannot be established.

## Map the agreement

Present one concrete five-section agreement. Preserve existing accepted commitments while translating their expression:

- Campaign promise: prior promise, scope/fit, exclusions, material development preferences, and source policy.
- Player control: prior ownership boundaries and actual explicit delegations. A character profile or campaign-form label supplies no new grant.
- GM initiative: what consequences must run and what new kinds of development may be introduced, under which conditions and limits. Preserve mandate-off as no standing permission for new discretionary consequential introductions unless the operator changes it.
- Time and transitions: existing compression and continuation permissions, and where the GM must stop for a decision.
- Presentation: accepted voice, guidance, cadence, and state-display preference, using old policy only for actual accepted defaults.

Old axis labels can be ambiguous. Show the concrete interpretation and ask only for unresolved material choices. This review is the acceptance point for the v0.7 wording; do not silently broaden authority. Preserve agreement lineage when present; an older campaign without an accepted contract receives its first explicitly accepted agreement.

Copy applicable module-imposed stronger restrictions into SAFETY with their origin distinguished from personal limits. Preserve all existing real operator limits. Update safety_state accordingly. Never infer a limit from a character's beliefs or a world's morality.

Keep existing valid Setting Brief content. If missing, use ADMIN/ADD_SETTING_BRIEF.md's drafting rules within this same staged upgrade and display the proposed brief. Read exact stable public sources needed to support it. A new world fact is an explicit additional change, not a formatting conversion.

## Review and publish

Show the proposed present, full agreement, any brief/limit changes, exact affected paths, and unresolved or unavailable evidence. Ordinary explicit acceptance is sufficient. Do not overwrite originals before the proposal is reviewable.

Use ADMIN/RECOVERY.md for the accepted operation, including verified preimages of every changed file and records of every new path. Publish supporting material, then the accepted agreement, and CURRENT_SAVE last. Inspect matching identities, required semantic sections, exact routes, engine/PC compatibility, safety, and retained evidence pointers. Complete the recovery operation only after its required checks.

Retain old Bearing as cold provisional notes; its old format or staleness does not block play. Do not reinterpret notes as accepted preferences. Do not rewrite NPCs, subsystem values, raw evidence, or authored private truths merely to make them look new.

Report the save/contract identities and any actual limitations. A fresh chat may then follow OS/AGENTS.md to resume. If interrupted, leave the active marker and recover before PLAY. Optional script validation may supplement the model's checks; it does not prove lossless semantic conversion.
