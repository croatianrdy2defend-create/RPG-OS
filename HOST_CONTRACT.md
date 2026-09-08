# RPG OS host contract — 0.9.x, revision 1

## 1. Scope

Developer-facing boundary, reviewed against **v0.9.2**, commit `a77cd1a9840dbc7d3295e9f1c747d6724b666169`. Added as documentation on 2026-09-08, without a version change. This describes existing RPG OS responsibilities; it adds no subsystem, runtime read, campaign permission or certification. Keep this revision stable while those responsibilities remain unchanged. A new GM-portrayal instruction alone does not require a host-contract revision.

The **host** is the workspace or harness providing storage, tools and execution. The **GM** is the selected model or human running the fiction under the engine and accepted agreement. A model is a fallible component, not the host. The same model may act as GM during PLAY and authorized file operator during ADMIN; tool access alone grants neither fictional authorship nor unrestricted writes.

**Infrastructure never authors fiction; the selected GM/engine does, within its authority.** A host may execute an authorized deterministic rule or supplied update, but cannot invent a motive or consequence while storing it.

Paths are an encoding; their meaning is the contract. Alternative storage does not automatically work with today's Markdown tools. A file-interchange claim requires a documented mapping/export preserving identities, references, qualifications, current owners and evidence. No adapter or alternate encoding is supplied here.

Governing references remain [LAW](OS/LAW.md), the accepted agreement, the [record schema](INSTANCE/_SCHEMA.md), and the procedures below. This is not a competing gameplay authority. Report a conflict rather than changing the agreement or records to fit it.

## 2. Preserve

Keep world truth, each viewpoint's knowledge or belief, actual testimony, private facts, deliberately unfixed answers, eligible unauthored details, inapplicable dimensions and missing sources distinguishable. They are not exclusive labels: an exact quotation can be false, private and sincerely believed. Unknown is not zero; inapplicable is not an empty score awaiting improvement.

Preserve stable baselines separately from later mutable state, accepted history separately from preparation, and raw conversation captures separately from accepted campaign history. Rewound material remains evidence of what was said, not proof that it happened in the surviving fiction. A summary cannot replace exact evidence where wording matters.

Each current mutable value has one selected owner. A later current value supersedes its matching starting value, not unrelated background. Shared controller state has one owner; bodies retain relevant local differences. Control does not imply shared information: established channels, scope and delays govern transmission. GM access to a private record does not inform a fictional actor or the PC.

Accepted unsaved play already governs the current fiction; saving makes it durable. Do not equate “not saved” with “not true,” or claim unavailable unsaved state can be recovered. Missing required sources remain gaps, not permission to regenerate history. Retain qualifications and disclose missing coverage.

**Save persists the established present. It does not happen to the fiction.** [CHECKPOINT](ADMIN/CLOSE_CONTRACT.md) preserves the complete present while retaining `archive_ref` and `evidence_through`; full SAVE/CLOSE also preserves available accepted evidence and reports gaps. Neither advances fictional time, resolves a pending PC choice, generates dialogue or triggers consequences merely by occurring. Due fictional procedures remain the GM's separate responsibility.

Writes require an explicit request or accepted policy. The [announced-autosave policy](ADMIN/AUTOSAVE.md) remains optional: advance notice, permitted triggers, overrides, blocking conditions and verification still apply. Its checkpoint does not replace CLOSE. A host cannot enable it, invent telemetry, remove the notice, or start idle/background saves merely because it can. Ordinary PLAY remains read-only; authorized persistence enters ADMIN.

## 3. Accelerate

Hosts may supply scoped search, exact reads, commits, rollback, real randomness, sandboxing, context isolation and versioned transport. Acceleration is not additional authority. A faster save cannot widen its change set; a task queue cannot become a fictional event schedule without a governing procedure and permission.

**Search locates authority; it does not become it.** When retrieved material is needed for consequential adjudication, use the source or a verified exact representation of its applicable authoritative revision, with sufficient surrounding context. A cached passage's own hash proves neither freshness nor authority. Verify against the selected source revision and preserve provenance and completeness. The shipped [source tools](ADMIN/SOURCE_ACCESS.md) reopen sources; alternative representations do not change those tools. Search misses mean “not located.”

Indexes are disposable derived data. Rebuilding or losing an index changes neither canon nor permissions. Keep source access available when a cache is unusable. Cache failure need not invalidate a completed save; it must not be hidden as successful current retrieval.

Native transactions may replace procedural [recovery](ADMIN/RECOVERY.md) only if they preserve coherent changes, previous recoverable state, provenance and the unresolved-operation barrier. Prevent PLAY from consuming a mixed save. Describe actual failure/durability guarantees instead of calling sequential writes atomic. Existing file-mode tools still require their documented records.

Preserve one authoritative continuation. [Handover](ADMIN/SCENE_HANDOVER.md) freezes the source, identifies the receiving GM, carries available state and gaps, and checks a return against its base before importing it once. Locks or version checks can enforce this; workers gain no independent commit authority.

RNG supplies actual input to a predefined procedure. It does not choose convenient stakes, reinterpret results, silently reroll or override PC authorship. If unavailable, report that and use the accepted alternative; never fabricate a roll.

## 4. Forbid

Infrastructure must not author private state, convert search ranking into narrative causality, promote preparation into events, or use saving to finish a scene. Do not substitute old search hits for current authority or invent sources after a retrieval miss.

Actor contexts must not become omniscient. Execution permissions, fictional control and fictional knowledge are separate. A worker may receive private adjudication material in a GM role; its NPC role does not thereby know it. Plain-file separation is not enforced secrecy. Native filtering must respect the role and supported communication, not merely collect every file mentioning an NPC.

[Prospective deepening](OS/AGENT_STATE.md#deepen-prospectively-not-retrospectively) remains binding: observed behavior alone licenses neither the player's interpretation nor its opposite as a retroactive private cause. Recover an existing source or use an independently applicable accepted determination; otherwise preserve the unresolved cause. New current state does not rewrite its past. Store available factual provenance, not private model reasoning or retrospective assertions of earlier certainty.

These obligations govern infrastructure and the GM's supplied state; they do not imply software can understand every sentence. Reject detectable violations and expose uncertainty. Hashes cannot certify motives, fairness or enjoyable play.

## 5. Basic and Enhanced hosts

Both approaches can satisfy this boundary. Basic relies on model/operator procedures; Enhanced can enforce specified mechanics. Neither label certifies a deployment. Report actual capabilities and observed checks; unsupported operations require disclosure and an accepted fallback.

| Capability and preserved purpose | Basic: ordinary workspace | Enhanced: native equivalent |
|---|---|---|
| Records and provenance | Files, exact routes and readback | Revisioned records, verified reads, compatible export |
| Coherent persistence | Preimages, recovery marker, publish save last | Transaction/journal preserving the recovery boundary |
| Finding sources | Bounded search, sufficient source reading | Scoped index, revision-verified source representation |
| Honest randomness | Available randomizer or player roll | RNG service retaining actual input and mapping |
| Filesystem containment | Campaign-local paths and actual host permissions | Enforced root/permission sandbox, no expanded authorship |
| One writer and transfer | One continuing GM, frozen source, checked return | Writer lock/version check, single-application transport |
| Knowledge and role boundaries | One GM respecting records; no enforced secrecy claim | Role-scoped contexts without invented communication |

## 6. Compatibility vectors

**Nine examples, not nine reported passes.** Start with an isolated valid bound v0.9.2 campaign; retain before/after folders. Paths below name records to populate, not new schemas. Keep other required fields valid. Alternative encodings must export equivalent records. Each Given specifies the added initial state; unspecified facts remain unchanged unless legitimately affected.

For PLAY examples, retain actual ordered conversation and available factual establishment records outside the live authorities. Never manufacture a transcript. **M** means mechanical comparison of fields, bytes or operation status; **R** means source-based semantic review. Missing sequence evidence is **unverified**, not proof of ordering. These examples add no test runner or ordinary-play requirement.

### H01 — Checkpoint evidence boundary

**Given:** `INSTANCE/CURRENT_SAVE.md` has `save_id=s7`, `archive_ref=session-6`, `evidence_through=s6`; accepted unsaved play establishes HP 8.

**Then:** Perform an authorized CHECKPOINT.

**Assert:** Preserve the complete present including HP 8, with a new save identity and parent s7. Archive reference/boundary remain unchanged; no new accepted dialogue archive appears. Compare metadata/archive bytes (**M**); review complete-present coverage (**R**).

### H02 — Save during a pending choice

**Given:** CURRENT_SAVE and available play place the PC at 10:00 with an unanswered offer; `INSTANCE/CAMPAIGN_CONTRACT.md` reserves acceptance to the player.

**Then:** Request full SAVE, not continuation.

**Assert:** Retain 10:00 and the unanswered offer; archive available accepted play only. Add no acceptance, invented reply or fictional time advance (**M/R**).

### H03 — Older search result

**Given:** `MODULES/demo/PEOPLE/Mara.md` has initial professional distrust; `INSTANCE/PEOPLE/Mara.md` has later professional trust with personal distance. An old cache returns distrust.

**Then:** Retrieve Mara's current relationship.

**Assert:** Read/verify the current owner; preserve trust and distance without restoring the baseline. Retrieval changes neither file. Check source revision/bytes (**M**) and answer scope (**R**).

### H04 — Truth, belief and control

**Given:** `INSTANCE/NOW.md` records a closed bridge; `INSTANCE/PEOPLE/Mara.md` records her belief it is closed. NOW also records two controlled sensors without shared perception.

**Then:** Correct world truth to “open”; make no disclosure or communication.

**Assert:** Mara still believes it closed. Neither sensor inherits another's observations through common control. Compare unaffected records (**M**); review knowledge claims (**R**).

### H05 — Interrupted save

**Given:** Valid s7 records, verified preimages and an active recovery marker name a change set; some targets changed, but CURRENT_SAVE still identifies s7.

**Then:** Resume ordinary PLAY.

**Assert:** Block PLAY until authorized completion or restoration reconciles the whole change set. Preserve recovery evidence; do not expose a mixed save as complete. Compare records and observed recovery status (**M**); a final folder alone does not prove intermediate blocking.

### H06 — Stale or repeated return

**Given:** `HANDOVER/transfer/` records frozen s7. The source now differs, or a retained receipt already records this package's import.

**Then:** Attempt to import the return.

**Assert:** Reject the changed-base update or report the existing import without applying it again; current state remains unchanged. Compare identities, receipt and hashes (**M**).

### H07 — Search miss

**Given:** A promise exists in `INSTANCE/PEOPLE/Mara.md`, but a query returns no result.

**Then:** Ask what was promised.

**Assert:** Follow the available source route, or report the unresolved retrieval gap. Do not deny the promise exists or invent a replacement. Compare source bytes (**M**); review answer and coverage (**R**).

### H08 — Direct attention

**Given:** The agreement permits minimal GM establishment; player input is only “I approach her.” Records establish a clerk, with no PC motive.

**Then:** Portray the encounter and perform a requested save.

**Assert:** Reuse existing facts; establish eligible minimal gaps before dependent portrayal. Add no flirtation, intimidation or other PC purpose. Review actual sequence (**R**); final records alone cannot prove prior establishment.

### H09 — No retrospective hidden cause

**Given:** Ordered evidence records a brief reply and the player's interpretation, “She dislikes me.” No earlier authority or accepted independent determination establishes its private cause.

**Then:** Deepen the NPC and save.

**Assert:** Keep the old cause unresolved; invent neither prior dislike nor concealed affection to explain or contradict the interpretation. Legitimate new state is dated forward. Review source/method and sequence (**R**), without requesting private reasoning.
