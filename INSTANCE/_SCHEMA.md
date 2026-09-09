# INSTANCE schema — v0.8.2

Cold ADMIN reference. An INSTANCE is one campaign run. The accepted agreement, current state, historical evidence, and optional review notes have different jobs. Normal PLAY does not load this schema.

## Current save

`CURRENT_SAVE.md` contains a compact resume state, not the complete character sheet, knowledge base, world, or history. Its front matter remains `id: instance.current_save`, `class: live-checkpoint`, `temperature: resident`.

Use one Markdown table headed `| Field | Value |`, with each required metadata field exactly once:

| Field | Meaning |
|---|---|
| engine | Installed safe engine id, or `unbound` |
| module | Bound safe module id, or `unbound` |
| pc_record | `INSTANCE/CHAR/PC.md` when bound, otherwise `none` |
| campaign_id | Unique portable id for this run, otherwise `none` |
| save_id | New unique portable id for each successful bind, CHECKPOINT, or full save |
| save_rev | Nonnegative ASCII integer; zero unbound, one at bind, increment thereafter |
| save_parent | Prior save id; `none` only for unbound/bind |
| commit_kind | `unbound`, `bind`, `checkpoint`, or `close` |
| archive_ref | Last archived evidence folder, POSIX path relative to ARCHIVE, or `none` |
| evidence_through | Save id owning that evidence folder, or `none` |
| safety_state | `floor-only` or `active` |
| datetime | Established time/date at the campaign's actual precision; no required human calendar |
| place | Established current location or operating scope |

Portable ids use ASCII letters, digits, `.`, `_`, and `-`, beginning with a letter or digit; no traversal token, slash, whitespace, or absolute path. Routes stay inside the designated tree, use `/`, and contain no `.`/`..` traversal or symlink route. Metadata values are nonblank; use `none` only for a known absence and preserve `unknown` in substantive state where that is the truth. Benign extra metadata produces a warning, not an invented failure; a conflicting identity, duplicate field, unsafe route, or competing authority remains a defect. Extra metadata is not permission to create facts.

After the table, include each of these level-two sections once. They are readable prose or concise bullets, not more control tables:

- **Situation:** the actual scene, ongoing declared action, unresolved choice, and remaining uncommitted time when relevant. Use ordinary language. A resolved scene does not decide an unanswered choice. Continuation/compression follows the accepted agreement; no compulsory lifecycle enum.
- **Character state:** materially current public conditions and selected resources, plus exact pointers to detailed PC authority. Do not reduce a complete sheet or consequential condition to a vague summary. A selected live total appears in exactly one current authority; other records may carry a maximum, derivation, or pointer.
- **Open matters:** actual explicit PC goals, obligations, appointments, and unresolved public matters. Keep uncertainty and declared wording where material. Observed behavior and OOC preferences do not become PC goals. A matter is not automatically an active event.
- **Active processes:** established due conditions/processes that may need checking, including non-revelatory private watch pointers. Give the relevant condition and exact current/definition route, not the hidden value. No forecast or queue of prepared scenes. An accepted continuation duty belongs here when currently operative; authority to do a kind of GMing remains in the agreement.
- **Relevant records:** exact useful routes to PC, people, current systems, knowledge, evidence, and applicable corrections. No compulsory hot roster, broad directory inventory, or instruction to load every route.

An empty section is `none`. Do not repeat a fact across sections merely to fill them. If a detail is owned elsewhere, retain a nonconflicting resume cue or pointer. Full detailed knowledge, private state, PC values, and lore remain independently retrievable.

## Identity and evidence boundaries

The distributed save is unbound: engine/module `unbound`; save_rev `0`; commit_kind `unbound`; safety_state `floor-only`; all other metadata and all five sections `none`. It contains no campaign residue. KNOWN, NOW, CAST_STATUS, and CORRECTIONS retain their distributed empty templates; CHAR and PEOPLE contain only their README files. No archive evidence belongs to an unbound kit.

A new module's T0_SAVE uses this metadata/section shape with the actual engine/module and future `pc_record: INSTANCE/CHAR/PC.md`, accepted opening time/place/state, but campaign_id/save_id/save_parent/archive_ref/evidence_through `none`, save_rev `0`, and commit_kind `unbound`. It is an opening template, never a bound run. LOAD supplies unique run/save identity, revision one, and commit_kind `bind`; it copies the exact accepted PC route closure into INSTANCE/CHAR. Only accepted opening facts may enter the instance. Legacy T0 formats are mapped by ADMIN without changing their source facts.

At bind, archive_ref/evidence_through are both `none`, KNOWN/NOW/CAST_STATUS/CORRECTIONS remain the distributed empty templates, and PEOPLE contains only its README. Accepted opening private/system state remains in its specifically named MODULE T0 authority until a later accepted change; accepted initial PC knowledge can remain in the copied baseline profile and its explicit references. Bind does not invent or preactivate INSTANCE overrides. A full Save uses commit_kind `close`, a new archive folder and campaign-index row, and evidence_through equal to the new save_id. CHECKPOINT updates the complete present but retains the previous archive_ref AND evidence_through unchanged. Either both are `none`, or both identify the same existing archived close. The checkpoint's own id has no archive row.

`evidence_through` identifies the last save whose available accepted evidence was archived. It is not proof that all earlier chat text survived. Full save must record missing source, incomplete coverage, or preserved uncertainty in its evidence folder and report material gaps. Never reconstruct missing wording from a state summary. Old evidence remains reachable after a later checkpoint.

## Accepted campaign agreement

`CAMPAIGN_CONTRACT.md` retains front matter `id: instance.campaign_contract`, `class: campaign-contract`, `temperature: resident`. Its Field/Value table contains campaign_id, contract_id, contract_rev, contract_parent, status, module exactly once. Identity matches CURRENT_SAVE. Contract ids use the save-id grammar; revision is zero unbound, one at bind, incremented for an accepted prospective change. Parent is `none` at bind and the prior contract id afterward. Fixed-path status is `unbound` or `accepted`; a draft marked `candidate` has no authority.

Use exactly these five substantive level-two sections:

- **Campaign promise:** accepted experience, scope, fit, exclusions, source/fidelity expectations, and the Play form clause. Knowingly accepted structural destinations or fixed outcomes may exist within their actual granted scope; do not present those as open resolution or override still-reserved PC decisions.
- **Player control:** meaningful choices and identity-scale domains reserved to the player, explicit standing grants, and the Retcon clause. Specify scope and limits. A brutal world, adult content, obedient role, or observed behavior does not supply delegation.
- **GM initiative:** concrete things the GM may and must do, their relevant conditions and limits, and the Form selection clause. Preparation and compatible content do not activate themselves; permission is not a quota. Include positive continuation responsibilities appropriate to the accepted form.
- **Time and transitions:** actual framing, declared-sequence compression, routine authorship, interruption, handback agreement, and the Cuts clause. Lived continuity is the default; an accepted bounded cut may skip authorized time or unfinished continuity but does not itself decide reserved PC choices. A player's declared sequence and standing delegation are distinct grounds for continuation.
- **Presentation:** accepted narrative voice, guidance, useful status display, and the Structure disclosure clause. Copy accepted module voice/defaults here so ordinary PLAY need not load POLICY. Real operator content limits remain SAFETY, not this section.

Every bound section is substantive, even if it states that no optional grant is made. Unbound sections are `none`; ids are `none`, revision `0`, status/module `unbound`. No mandatory calibration-axis enum, creative-mandate switch, review-mode gate, or magic acceptance phrase is required. Show the complete concrete proposal and obtain ordinary explicit acceptance. Unaccepted preferences remain proposals. RECALIBRATE changes the agreement prospectively, never historical facts.

### Five named prose clauses

New v0.7.1 bound agreements include each of these labels exactly once, as a plain or bullet line in the stated section, followed on that line by a substantive free-text value. These are short readable clauses, not another calibration table or mandatory A–E enum. Code examples, comments, blank values, and placeholders do not satisfy them. Other prose/bullets may accompany them.

| Section | Exact clause label | Meaning and proposed default |
|---|---|---|
| Campaign promise | Play form: | Record the actual accepted form/promise, mixed/custom if needed, or truthfully state bounded delegated selection. Never falsely call fixed directed play an unqualified sandbox. |
| GM initiative | Form selection: | Default: operator accepts the stated form. Optional GM selection requires explicit scope; it does not imply permission to conceal the choice. |
| Presentation | Structure disclosure: | Default: operator knows the general form; plot secrets stay hidden and PLAY need not recite structure. Optional concealment of the selected structure needs a separate knowing grant and truthful control record. |
| Time and transitions | Cuts: | Default: lived continuity, compress only declared/delegated routine, no cinematic jump. Any hard-cut exception specifies scope and conditions while preserving reserved PC decisions. |
| Player control | Retcon: | Default: OOC rewind available. Optional ironman/no-retcon constrains revising valid accepted outcomes, not stop/end, depiction changes, or correction of genuine errors. |

SETUP proposes these defaults within its single compact agreement; it need not ask five extra questions. A–E presets may help describe supported play, but the actual promise and grants govern. Structural validation checks label placement, occurrence, and substantive text, not acceptance, clarity, semantic compatibility, or GM compliance.

If structural selection/disclosure is delegated, the reviewable proposal shows the true delegation and its boundaries. It need not expose a secret selected structure or plot. Once a selection creates operative commitments, retain them in their proper current/private record and route them from the control record as needed; do not silently reselect after a fresh chat. Operator access to files and host disclosure limits still apply.

Existing v0.7 agreements missing these clauses receive focused supplementation through ADMIN/RECALIBRATE.md. Preserve established accepted terms; ask for unresolved material choices and show proposed wording/defaults before acceptance. An incomplete starting agreement is eligible for that repair. Do not reset current state, convert history, or infer old permissions from behavior. Older field-only records still use the full upgrade procedure.

## Current records and compilation

One current authority per value. This is a semantic check, not something a table shape can prove.

| Information | Current home |
|---|---|
| Resume essentials and selected public totals | CURRENT_SAVE |
| Full PC/profile and other mutable sheet/build values | INSTANCE/CHAR/PC.md or its explicit shards |
| What the PC learned, with rumor/belief/uncertainty and sources | KNOWN |
| Private conditions and mutable campaign/world-system state | NOW or explicit shards routed from NOW |
| Temporary state of currently participating entities | One Active encounter state block in NOW |
| Consequential enduring individual-agent/relationship state, including retained commitments and beliefs | PEOPLE/<person_id>.md or its explicit shards |
| Stable emergent-person identity | Minimal established CANON in that person's INSTANCE record |
| Stable person-id and route mapping | CAST_STATUS |
| Accepted rulings and corrections | CORRECTIONS, with a resume pointer when currently relevant |
| Operator content limits, including hard-no and veil boundaries | SAFETY |
| Accepted historical evidence | ARCHIVE evidence bodies |
| Optional provisional review | BEARING, explicit REVIEW only |

MODULE baseline files remain stable. Before any later transition or current override exists, and only while no declared transition has occurred or is due, one specifically named MODULE as-of-T0 snapshot may support current continuity. PLAY holds later accepted changes in chat. At the next save, apply still-unsaved changes exactly once to the selected authority. For a first person/system change, materialize the complete as-of-now mutable surface; do not merge a newer overlay with old T0 values. Stable CANON and unrelated private lore stay in MODULE.

An emergent person with durable causal state receives one stable person_id, minimal established CANON, complete current mutable state, and a CAST_STATUS route. A transient extra need not be promoted. An emergent durable system receives one stable system_id and `INSTANCE/NOW/<system_id>.md`, explicitly routed from NOW. Preserve its complete established current state and the minimum operating definition needed to continue: triggers/non-triggers, dependencies/order, and cue lifecycle when relevant. Missing rules stay unknown; do not invent them for completeness.

PEOPLE and existing person_id routes also support nonhuman individual agents. A collective/controller may instead use its selected NOW system owner; a shared variable never belongs to both. Known identity, nature, capacities and control remain governing inputs, not temporary traits to regenerate. Preserve fixed, deliberately unfixed, unknown-to-PC, missing-source and inapplicable distinctions; storage never supplies missing facts or treats an operational group as one private mind.

### Active encounter state

At an authorized save, one optional `## Active encounter state` block in `INSTANCE/NOW.md` owns the complete current temporary baseline set. Entry membership means active; no separate yes/no field or inactive roster is needed. Each concise entry identifies the participant or coordinated decision scope and covers **Condition and mode; Priorities and constraints; Perception and appraisal; Attraction; Engagement stance**, including applicable limitations and useful actual method/result or material-change provenance. A compact local identifier suffices for an incidental participant; no person file or CAST_STATUS promotion is required. If an established value is already owned by a durable person/system record, use its exact route instead of duplicating that value. Shared controller values are stored once, with only relevant local differences in entries. Do not create an empty active block or activate NPCs at T0 merely to install this procedure.

Use `OS/AGENT_STATE.md#Active participation and deactivation` for lifecycle decisions. Ordinary gaps in attention preserve participation. Genuinely ended involvement releases inconsequential private temporary state; retain consequential identity, relationships, commitments, injuries, knowledge, processes and unresolved matters at their existing appropriate owners. Do not preserve an entire baseline merely because one consequence survives or its private values appeared in an audit. At the next authorized save, omit expired entries and apply any necessary transfer to a durable owner once. Deliberate expiry is a current-state transition, not permission to delete historical evidence. No expired-state registry or archive purge is introduced.

A later incidental encounter may receive fresh temporary values within surviving established facts under the accepted lifecycle. Saving, switching models or briefly shifting attention is not deactivation. Missing state still needed for active participation or a consequential unresolved matter remains a source gap; do not relabel it expired, invent it during compilation or silently regenerate it. Historical evidence may document an earlier state without making that expired state current authority again. Removing an entry limits current-state maintenance; it does not erase old conversation tokens or promise recovery of discarded private values.

Optional portrayal anchors belong with the person's existing stable canon or current state according to what they describe. Keep one authority; they require no additional record or fields. Use `OS/AGENT_STATE.md` for a material establishment/change task, not as another startup dependency. Authorized private generation can establish a fact within the accepted scope without disclosing it to the PC; preparation and provisional interpretation do not become facts at save time.

When a private process remains live across fresh chats and no other resident fact makes its check discoverable, retain one non-revelatory condition/id/route in Active processes. Before an INSTANCE current record exists, that save pointer targets the existing MODULE baseline/definition body; the planned future INSTANCE destination belongs inside the definition. Once current state materializes, redirect the save pointer to that INSTANCE authority. Remove or demote a cue when it retires. Retrieval, review, and saving never advance a process. Elapsed time advances it only when its established rule says so. Retain the scope/result of an already evaluated opportunity when needed to avoid repeated effects; a motive or repeated query alone creates no new opportunity or draw.

Known-to-PC, private truth, exact fidelity, authorship ownership, and provisional interpretation are different distinctions, not mutually exclusive labels. Preserve the qualification needed for each fact. Hearing a rumor establishes that it was heard. Exact wording can be private. Missing historical evidence does not establish an event or make it available to invent retrospectively.

Across saving and correction, preserve a materially misleading claim as something its speaker said to its actual audience, separately from established private truth and any materially established NPC belief. An accepted utterance need not be true; do not infer that its speaker knew it was false. Retain belief uncertainty and source where established. Correcting the claim's assessed truth does not erase the utterance or tell its audience the correction unless that disclosure actually occurred.

## Optional review

BEARING is cold, optional, and never loaded at normal startup. Its notes cite campaign_id, base_save_id, base_contract_id and the files/headings actually reviewed. The empty template has `status: none`; a completed review is explicitly provisional. No fixed seven-section layout is required. At bind only campaign identity may be reset; no review is inferred.

Separate established references, explicit player preferences, observed conduct, and provisional interpretation wherever those appear. Newer state/agreement makes old notes historical interpretation, not current authority. Missing/stale/malformed review notes do not invalidate a playable save; ignore them and address the optional defect only if REVIEW is requested. Review never supplies facts, a continuation obligation, prepared-scene priority, or an inferred desire.

## Mutation and recovery

Scene handovers are optional operational records outside INSTANCE, governed by `ADMIN/SCENE_HANDOVER.md`. `HANDOVER/ACTIVE.md` pauses source play; the package's CONVERSATION and GM_STATE files are frozen transport copies, not competing current authorities. No new CURRENT_SAVE metadata or commit kind is introduced. CHECKPOINT still retains its evidence boundary. An accepted return is compiled into the existing current authorities and full-save evidence once; its retained RECEIPT identifies the result. Normal startup checks only the active marker, never old packages. Installing the handover procedure alone creates no marker, package, person or fictional progress.

PLAY writes no campaign files. Explicit Save/CLOSE/END SESSION uses ADMIN/CLOSE_CONTRACT.md; CHECKPOINT uses its reduced-evidence path. REVIEW writes only optional notes. RECALIBRATE writes only an explicitly accepted prospective agreement. CORRECT follows ADMIN/CORRECT.md for narrow current and historical repair. Safety changes take effect in the conversation immediately; durable changes use the recovery procedure and matching save flag.

Independent-agent establishment, updating and deactivation add no automatic write boundary, save kind or private scratch layer. During PLAY, the active set changes in conversation with best-effort retention; the next authorized save synchronizes its complete current membership and values. Requested CHECKPOINT still preserves every accepted current change, active baseline, consequential retained fact and pending declaration, not just the encounter block. The receiving GM cannot checkpoint frozen source authorities. Missing required retained state requires honest source/repair handling, not silent regeneration. Program adoption preserves existing saved facts; only subsequent authorized lifecycle transitions can expire eligible temporary state.

Before overwriting any campaign file, follow ADMIN/RECOVERY.md: verified preimages and planned new paths in RECOVERY/<operation-id>, plus RECOVERY/ACTIVE.md. Any present active marker blocks ordinary boot until recovery or completion is verified. CURRENT_SAVE is published last for bind/save, but this is not multi-file atomicity. Preserve recovery materials; never claim automatic rollback. A failed review or agreement operation does not change unrelated state, but any pending recovery marker must be resolved before PLAY.

Growing records may retain their canonical entrypoint as a compact index pointing to independently relevant bodies. Split only when it improves retrieval, not by a file-size quota; update routes with recovery protection. Indexes locate information and do not duplicate it. Existing v0.6 state/contract formats require explicit ADMIN/UPGRADE_V07.md mapping and acceptance; ordinary boot never silently rewrites them.
