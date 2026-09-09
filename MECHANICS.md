# How RPG OS works

RPG OS v0.9.4 is an experimental file protocol for running a roleplaying campaign with an LLM. The model portrays the world and adjudicates play; readable Markdown records preserve the agreement, present state, rules, and evidence needed to continue across chats.

It is not a trained model, background server, autonomous simulation, or replacement for a rules engine. Its procedures tell a capable host how to use ordinary files. The model still has to read the right source, make sound judgments, and perform the agreed operations correctly.

This guide explains the mechanics behind [Quick start](QUICKSTART.md). For compact technical ownership notes, see [Architecture](ARCHITECTURE.md); the linked operating files contain the full procedures.

## Contents

- [The operating loop](#the-operating-loop)
- [What lives where](#what-lives-where)
- [From fresh install to campaign](#from-fresh-install-to-campaign)
- [The agreement and authorship](#the-agreement-and-authorship)
- [Inside a turn](#inside-a-turn)
- [Independent people and other agents](#independent-people-and-other-agents)
- [Optional encounter generation: direction, then concrete state](#optional-encounter-generation-direction-then-concrete-state)
- [Random fallback for unresolved outcomes](#random-fallback-for-unresolved-outcomes)
- [Truth, knowledge, preparation, and history](#truth-knowledge-preparation-and-history)
- [Saving the present and preserving evidence](#saving-the-present-and-preserving-evidence)
- [Recovering interrupted work](#recovering-interrupted-work)
- [Handing an active scene to another GM](#handing-an-active-scene-to-another-gm)
- [Sources, visuals, and host capabilities](#sources-visuals-and-host-capabilities)
- [Exact retrieval and evidence audits](#exact-retrieval-and-evidence-audits)
- [What the checks establish](#what-the-checks-establish)

## The operating loop

The player supplies intentions and choices. The GM combines those with the accepted agreement, relevant records, and resolution rules. Accepted developments remain in the conversation until a save operation installs them in the workspace.

```mermaid
flowchart TD
    loopPlayer["Player: intentions and choices"] --> loopGM["LLM acting as GM"]
    loopFiles["Workspace: agreement, rules, world, state, evidence"] --> loopGM
    loopGM --> loopResponse["Response and next meaningful decision"]
    loopResponse --> loopPlayer
    loopGM --> loopChat["Accepted changes in conversation"]
    loopChat --> loopSave["Requested save and verified writes"]
    loopSave --> loopFiles
```

Conversation supplies temporary working context. Files supply durable, inspectable records. Merely mentioning a change does not establish that it was saved, and the existence of a file does not mean its contents are loaded into the model.

## What lives where

The fresh kit contains generic instructions and empty run templates. Campaign-specific records appear only through accepted setup and play. The tree below shows the main installed areas and the optional runtime areas created when needed.

```text
RPG_OS/
|-- OS/                    GM core, startup, targeted retrieval
|   `-- AGENT_STATE.md     Cold establishment and portrayal procedure
|-- ADMIN/                 Setup, saves, corrections, recovery, handover
|-- ENGINE/
|   |-- _CONTRACT.md       Adapter requirements
|   |-- freeform.md        Only bundled selectable rules adapter
|   `-- _shared/           Optional procedures for compatible engines
|-- MODULES/               Contracts; accepted worlds are added here
|-- INSTANCE/
|   |-- CURRENT_SAVE.md    Compact present and useful routes
|   |-- CAMPAIGN_CONTRACT.md
|   |-- CHAR/              Current character records after binding
|   |-- PEOPLE/            Current recurring-person records when needed
|   |-- KNOWN.md           What the played perspective has learned
|   |-- NOW.md             Current private and system state
|   `-- ...                Safety, corrections, routing, optional review
|-- ARCHIVE/               Indexes and accepted historical evidence
|-- EVIDENCE/              Optional raw captures; only README in the fresh kit
|-- TOOLS/                 Optional readers, search, audit helpers and tests
|-- RECOVERY/              Created for protected file operations
`-- HANDOVER/              Created for an authorized live-scene transfer
```

A module contains stable world material, source bindings and an opening baseline. ENGINE owns the selected generation and resolution mechanics; module facts constrain where those mechanics apply. An instance is one actual run through that material. Later mutable values belong in the instance, while unchanged world background remains in the module. Archives preserve what happened rather than competing with the current records over what is true now.

The layout does not require an encyclopedia or a file for every passing character. Records split when their subjects need independent retrieval. See the [module contract](MODULES/_CONTRACT.md) and [instance schema](INSTANCE/_SCHEMA.md).

## From fresh install to campaign

The public installation is **unbound**: no selected world, character, campaign history, or active handover. Freeform is the only bundled selectable engine, but setup still establishes the chosen engine. The shared encounter generator is an optional procedure, not an engine identity. Unbound describes installation state; it does not select a play style or override a host's capabilities.

Start with:

> Open OS/AGENTS.md. Start a new campaign with me using Quick start.

Quick start, Guided, and Detailed change the depth of the setup conversation. They are not different runtime engines. Quick start asks only what materially blocks a coherent proposal; supplied facts and deliberate unknowns remain useful.

```mermaid
flowchart TD
    setupFresh["Separate clean campaign folder"] --> setupRequest["Request setup and supply an idea"]
    setupRequest --> setupDraft["Develop only necessary world, PC, rules, and opening"]
    setupDraft --> setupProposal["Review one concrete campaign proposal"]
    setupProposal --> setupChoice{"Accept or revise?"}
    setupChoice -->|"Revise"| setupDraft
    setupChoice -->|"Accept"| setupBind["Protect writes and bind the accepted records"]
    setupBind --> setupVerify["Read back identities, contents, and routes"]
    setupVerify --> setupPlay["Resume the accepted opening"]
```

Binding gives the run its own campaign identity, save lineage, agreement identity, current PC bundle, and opening state. New Game does not clear a previous campaign to make room. Use a separate clean copy for another run.

World creation establishes a usable encounter-generation method for ordinary actors and necessary opening exceptions: supported sources, applicable fields, constraints, outcome meanings and the real input method where dice are chosen. Nature, control and capabilities govern the current fields; no universal human temperament or attraction table is imposed on organisms, machines, collectives or other beings. Existing individual facts retain priority, and a newly encountered kind needs compatible authority before dependent behavior.

Freeform uses established capabilities, circumstances, opposition, and stakes to judge uncertainty. It imposes no attribute list, compulsory dice system, or hidden stat block. A requested random method needs agreed meanings and an actual available randomizer or player-supplied result. More formal engines can be installed through the [adapter procedure](ADMIN/ADD_ENGINE.md).

## The agreement and authorship

The accepted [campaign contract](INSTANCE/CAMPAIGN_CONTRACT.md) turns preferences into concrete operating terms. Its five named clauses answer different questions:

| Clause | What it establishes |
|---|---|
| **Play form** | The accepted experience: exploration, missions, everyday life, directed chapters, or a described combination. |
| **Form selection** | Whether the GM may select a form, and the limits of that delegation. |
| **Structure disclosure** | What the player knows about the overall structure; plot secrets alone do not authorize concealing the form. |
| **Cuts** | Which transitions may compress or skip time, with meaningful reserved decisions preserved. |
| **Retcon** | Whether valid accepted outcomes may be rewound; genuine error correction remains a separate operation. |

The player controls the PC's voluntary actions, speech, inner experience, and commitments except for explicitly delegated scope. A biography, previous choice, or inferred preference grants no additional authority. The GM controls NPCs and world consequences within the agreement.

Initiative is meaningful without being compulsory incident generation. An established cause, applicable procedure, explicit request, or accepted initiative grant must justify a new consequential development before it is drafted. Permission to introduce trouble does not mean every scene owes trouble.

For example, permission to compress ordinary ferry travel can cover the declared crossing. It does not automatically choose whether the PC accepts a job offered aboard. [LAW](OS/LAW.md) defines these authorship and continuation rules; [Recalibrate](ADMIN/RECALIBRATE.md) changes accepted terms prospectively.

## Inside a turn

Startup checks recovery first, then loads the core, current save, and accepted contract. An active handover pauses source play. A bound run also reads its compact setting brief and any active operator limits; detailed lore and mechanics stay available for targeted retrieval. Every PLAY reply follows LAW's Understand → Establish → Resolve → Portray order. Routine dialogue may make each stage brief, but does not skip the relevant basis or source before authorship.

```mermaid
flowchart TD
    turnInput["Read the player's message"] --> turnKind{"Play or administration?"}
    turnKind -->|"Administration"| turnAdmin["Open the matching ADMIN procedure"]
    turnKind -->|"Play"| turnIntent["Identify declaration, situation, and existing authority"]
    turnIntent --> turnNeed{"Need a fact or rule?"}
    turnNeed -->|"Yes"| turnRead["Follow a direct route or bounded subject search"]
    turnRead --> turnEnough{"Enough reliable information?"}
    turnEnough -->|"No"| turnAsk["Keep the decision pending; retrieve or clarify"]
    turnEnough -->|"Yes"| turnResolve["Resolve the attempt and due consequences"]
    turnNeed -->|"No"| turnResolve
    turnResolve --> turnPresent["Portray results and return the next reserved decision"]
```

Retrieval asks what could materially change this response. Exact equipment needs the current character record. A disputed promise needs its evidence body. Ordinary conversation may need neither. Direct pointers can be followed immediately; an index is useful when the route is unclear.

After an event, Resolve carries its established changes into current working state before continuing, including what each affected entity actually perceived. An observer may remember a distinctive coat without having seen a face; being in the room does not prove either observation. Preserve the information at its actual scope even if that witness later leaves, while allowing inconsequential temporary mood to expire. This is a working-state duty, not permission for a per-turn file write.

Before a pending action proceeds, check its current conditions, information, means and resources. A failed transmitter does not deliver a message; a replacement battery needs a supported source and actual installation before it changes the situation. Preserve the unanswered message or other unresolved consequence without treating a plan as completed. These are illustrative examples, not reported test results.

Private processes advance when their recorded triggers apply. Reading a storm clock does not move it. Saving does not make the storm arrive. A time-based process advances because relevant time elapsed, while another process may depend on a specific event instead.

The [retrieval guide](OS/RETRIEVAL.md) preserves these distinctions. It also prohibits filling missing historical wording or exact values with plausible guesses.

## Independent people and other agents

An agent's relevant state gives the GM a basis for its decisions: what it is doing, what it can perceive, what it wants and how it currently regards the matter at hand. People, creatures, machines and collectives need different kinds of description. There is no universal list of emotions or a numerical relationship meter.

“Agent” means one of these fictional actors, including a decision-making system. The same GM portrays them through selectively retrieved facts; there are no separate AI workers running each NPC or continuously simulating the whole cast.

**Individual participation activates a temporary basis.** Before an individual appraisal, attention, initiative or separately resolved response involving the PC, complete the five current fields of the [Initial Encounter Baseline](OS/AGENT_STATE.md#initial-encounter-baseline). A bare approach can begin participation without selecting the PC's purpose; an NPC's own individual look or initiative can also activate it. Quietly observing an unaware individual does not require private state. First focused physical portrayal still follows the module-prescribed guide before description, reusing sufficient loaded guidance independently of activation.

| Depth | What the GM needs |
|---|---|
| Background people or coordinated group conduct | Ordinary setting-consistent portrayal, actual shared duties and information. Ten soldiers noticing the PC need not acquire ten personalities; no shared private attraction is inferred. |
| Individual participation, appraisal or separately resolved personal decision | Five current fields: condition/mode, priorities/constraints, perception/appraisal, attraction, engagement stance. Recover governing facts and active values; settle eligible gaps before behavior. Three independent drink decisions require three baselines. |
| Actual developments make more detail matter | Deepen the affected person as play supplies causes, disclosures or new needs. Retain durable consequences through the existing person/system owner when continuity requires them. |

These are scales of resolution, not new record types. Five current determinations can be concise; there is no permanent personality worksheet or public questionnaire. An activity alone does not complete the basis. Applicable overall attraction is established even on duty, while absent perception is a precise limitation rather than zero attraction. Overall attraction includes attraction, no particular attraction or aversion within the supported attraction domain, and remains distinct from approval, trust, hostility, availability and participation. Known subtype-specific constraints survive; finer meaning can be resolved later when relevant. During active participation, reuse state through attention gaps and update only what information, events or meaningful elapsed activity affects. At genuine deactivation release inconsequential private values; retain consequential facts and unresolved matters. A later incidental encounter may generate fresh temporary values under the accepted method, but missing active state and an ongoing negotiation never supply reset authority.

Established facts come first, including private facts the PC has not learned. A deliberately unfixed property keeps its agreed trigger. A missing source remains a retrieval problem. Eligible new details follow the accepted authoring or generation method; participation does not authorize replacing inaccessible facts or selecting an unaccepted random method. The [cold agent-state procedure](OS/AGENT_STATE.md) supplies the operating detail when needed and adds no unconditional startup read.

The NPC perceives only what is actually available to it: the PC's observable approach, words and conduct, plus any legitimately held prior knowledge. It may form a mistaken inference; that belief does not establish the PC's intent. Resolve the reaction from both the individual baseline and the applicable ENGINE procedure. The baseline supplies context, not arbitrary mechanical modifiers or permission to bypass a required reaction check. Do not resolve the same reaction twice, roll away fixed state, or invent a prior motive after seeing the result.

```mermaid
flowchart TD
    agentFocus["Individual participation, appraisal or initiative involving PC"] --> agentSource{"Relevant individual facts?"}
    agentSource -->|"Established"| agentUse["Retrieve and reuse the current baseline"]
    agentSource -->|"Eligible gaps"| agentEstablish["Complete five current fields under the accepted compatible method"]
    agentSource -->|"Missing source or protected unknown"| agentGap["Retrieve or preserve the gap; pause only dependent resolution"]
    agentEstablish --> agentUse
    agentUse --> agentPerceive["Use what the NPC can perceive; its inference is not PC intent"]
    agentPerceive --> agentResolve["Resolve and portray from the baseline and applicable ENGINE"]
    agentResolve --> agentCause["Update relevant fields; on genuine exit release inconsequential state"]
    agentCause --> agentChat["New state remains unsaved in conversation"]
    agentChat --> agentSave["Authorized save: active state in NOW; consequences in existing owners"]
    agentSave --> agentResume["Resume active state; fresh incidental values only after genuine expiry"]
```

### Example: “I approach her”

In a synthetic station scene, the player approaches a woman beside a departure board. The illustration supplies her current basis before her response: distracted while checking a delayed train; trying to follow the display with time for a brief question; perceiving an approaching stranger and provisionally interpreting them as another traveler; no particular attraction; open to a short exchange while monitoring announcements. These are illustrative fixed inputs, not claimed random results. They decide neither the PC's purpose nor her response to a yet-unspecified request. No enduring personality or explanation of her earlier life is needed.

If she can see the approach, she may turn toward the PC or respond according to the applicable reaction procedure. She might assume a traveler needs help, but that remains her inference. The player can speak, wait, leave or reveal a different purpose. The GM does not require a motive declaration merely to make her an individual, and it does not generate a new baseline when the PC next speaks. A later announcement or an actual exchange can change her attention or willingness at the relevant scope.

### Example: a coworker, a mistaken belief, and a fresh GM

In this illustrative station scene, coworker Mara values safe maintenance. She trusts the PC's technical skill, doubts their thoroughness, and keeps a personal distance. Her supplied current basis is calm and inspecting maintenance work, prioritizing safety, perceiving the known coworker through that established mixed appraisal, experiencing no particular attraction, and open to professional cooperation. A service hatch is actually open, but Mara believes it is sealed because she read an outdated log. Her mistaken belief and the hatch's true condition are separate established facts. These are illustrative fixed facts, not results of a live test.

| Stage | What happens and what remains true |
|---|---|
| **Before the encounter** | Individual participation retrieves Mara's established relationship, belief and current basis; it does not regenerate their fixed values. The GM can portray courteous, cautious cooperation. Neither the PC's wish for friendship nor Mara's wrong information changes the hatch's actual condition. |
| **A relevant event** | The player declares that the PC inspects the hatch and shows Mara the open latch. Mara looks and acknowledges the discrepancy. Direct observation changes her belief; this careful check gives her a reason to trust the PC's thoroughness more. Her personal distance remains unchanged. |
| **The player requests a full save** | The consequential current relationship and belief, with their cause, go into Mara's person record. Her still-active temporary basis goes into NOW with references to those enduring facts. The PC's observation goes into KNOWN. Available declarations and dialogue go into ARCHIVE. The unchanged hatch fact keeps its existing world owner; the save's useful pointers locate current records. No additional action or attitude change occurs during saving. |
| **A fresh GM resumes** | The new GM retrieves Mara's current record: greater professional trust, continued personal distance, and knowledge that the hatch is open. It does not replay the discovery, restore her old belief, or infer friendship. A later request for help is judged from these facts and the actual circumstances. |

The valid change is as important as the continuity. Ignoring the observation would make Mara rigid; turning a careful inspection into universal affection would erase the distinction between professional trust and personal closeness. Ordinary help or initiative can be appropriate without manufacturing an obstacle.

This example uses established facts and Freeform judgment, so it requires no random draw. If an eligible unknown instead uses a selected random procedure, its context and outcome meanings must be settled before obtaining real input. The result is then retained at its actual scope; repeated attempts or a new GM do not authorize another draw.

Stable background stays in MODULE; later mutable individual state uses PEOPLE, and collective/system state uses its selected NOW authority. Direct attention does not itself create a file or require durable promotion. A promise, consequential disclosure or continuing interaction may make retention necessary; a brief service exchange may leave nothing needing its own person record. Until the requested save succeeds, the encounter's new state remains in conversation. A full save preserves available evidence; a checkpoint preserves current state without adding that evidence. Neither can reconstruct a lost quotation or hidden determination.

Three distinctions keep the procedure honest:

| Distinction | Practical effect |
|---|---|
| Opportunity, initial state, attempted influence | Meeting another person, establishing an eligible trait and resolving persuasion are different questions. Repeating an equivalent attempt does not reroll identity or create another chance by itself. |
| Judgment and randomness | A random procedure needs actual input and predefined applicable outcomes. GM judgment remains valid when it is the accepted method; fabricated rolls do not add independence. |
| Motive, plan and event | Wanting to send a message does not mean it was sent. A real eligible opportunity can produce initiative; repeatedly checking for messages does not multiply a resolved opportunity. |

Ordinary conversation holds new state as working context. Authorized saves preserve the complete current active set in NOW and enduring/consequential facts in existing person/system owners. Genuine expiry removes an inconsequential temporary entry from current authority at its actual time; old transcripts remain historical evidence. This is not erasure of chat tokens. A required active fact lost through interruption remains a source gap, not a discarded value that can be rerolled. No per-contact checkpoint or private scratch layer is introduced.

The player does not operate this procedure turn by turn. Narration and dialogue should remain natural, with the next meaningful reserved choice returned promptly. Actual campaign play will test whether these instructions improve continuity and pacing; the [playtest guide](ADMIN/PLAYTEST_V08.md) keeps optional observations outside the fiction.

### Optional encounter generation: direction, then concrete state

[ENGINE/_shared/ENCOUNTER_GENERATION.md](ENGINE/_shared/ENCOUNTER_GENERATION.md) is a universal optional helper, used only when a compatible bound engine and the accepted agreement select it. It supplies eligible initial values within the five mandatory fields; it does not choose a response or replace the engine's resolution procedure. MODULE supplies the entity's supported nature, capacities, control, source routes and circumstances. Existing facts, active values and precise perception limits take priority over generation.

Before drawing, identify the unresolved facet of **condition**, **initial interpersonal appraisal** or **overall attraction**, and fix its scope. Use two independent actual d6 for each eligible facet and sum that pair:

| 2d6 total | Direction and intensity |
|---|---|
| 2–3 | Strongly negative |
| 4–5 | Negative |
| 6–8 | Neutral or mixed |
| 9–10 | Positive |
| 11–12 | Strongly positive |

**After each direction/intensity band is obtained, the GM establishes the concrete current value before choosing dependent behavior.** A label such as "positive" or "mixed" does not complete the field. There is no catalogue of moods, venues or six prepared states. The GM fills a short, meaningful value within the previously fixed facet, source constraints and accepted authoring scope. No additional intensity roll or invented past cause is needed. Strong means a marked degree within supported limits, granting no new capacity, compulsion, automatic cooperation or loss of boundaries. Neutral/mixed means a concrete absence of directional pull or supported countervailing considerations, rather than an empty placeholder.

The direction refers to different things in the three eligible facets:

| Facet | What the GM makes concrete |
|---|---|
| Condition | Favorable or adverse to the entity's own current functioning or activity in the previously selected physical, emotional or operational aspect. Preserve known injuries and other condition facts; a positive result grants no healing or equipment. |
| Initial interpersonal appraisal | A favorable or unfavorable evaluation of the PC from information actually perceived or already held. It cannot prove identity, trustworthiness or the PC's undeclared intent. |
| Overall attraction | Personal pull toward or aversion from the PC within the supported attraction domain. No particular pull or concrete ambivalence can fill the middle band. It establishes neither approval nor hostility, availability, commitment or participation. |

**Priorities and constraints** receive concrete current aims, drives, directives or operative processes and practical limits from sources, circumstances and eligible authorship. State what the entity pursues, preserves or avoids and how it matters now; a bare activity label can miss competing commitments. These aims are independent of the player's hoped-for result and receive no polarity roll. **Perception and appraisal** preserves actual detection, recognition, information and limitations. A nonsocial response follows its sourced sensing, classification, control and response mechanisms; predation or chemical response does not become interpersonal liking or attraction by analogy. **Engagement stance** is derived from the complete basis and situation without a willingness or stance draw. The bound engine then resolves the pending decision once.

Applicable overall attraction is completed at first sufficient perception even if the entity is busy, on duty or partnered. Physical/aesthetic, sexual and romantic detail can be resolved later within surviving constraints, but that does not leave the overall field blank. Supported inapplicability needs no draw; an unread source or unknown capacity remains a source gap. A precise lack of perception delays only the affected determination until the necessary information arrives.

A wholly eligible baseline uses **at most three 2d6 determinations, six independent faces total**. Fix pair-to-facet assignments before input; do not share faces between facets or entities. Fixed facts, supported inapplicability and precise perception limits reduce the input. The bands are game conventions, not population statistics: with fair independent dice, 6–8 occurs in 16 of 36 pairs and each strong band in 3 of 36. Drawing a uniform total from 2 to 12 changes the method. Use real input or agree an available alternative; do not fabricate rolls, reroll inconvenient directions or choose a response and fit the inputs afterward.

The existing active-state lifecycle and first-focus portrayal retrieval still apply. Reuse active values through attention gaps, update affected fields for actual developments and release inconsequential temporary values only on genuine deactivation. Retain consequential facts, unresolved matters and input references needed for continuity. The helper adds no ongoing attraction/reception roll, visible checklist, private scratch record, per-turn write or automatic checkpoint. An upgrade leaves the accepted generation method and diceless agreement intact unless a prospective change is separately accepted.

### Random fallback for unresolved outcomes

A current individual baseline does not settle every later opportunity. Sending a message, fulfilling a promise or passing on a secret may remain open after an encounter. Use retained consequential facts, any still-required active basis, actual developments and applicable ENGINE procedures. If an eligible outcome lacks enough basis for grounded judgment, use the accepted fallback within scope. This does not replace the basis required before individual participation, resurrect expired trivia, or add a second roll for a settled reaction. The [fallback oracle](OS/AGENT_STATE.md#fallback-oracle-for-eligible-unknowns) is a standing method the player can select once; it needs no permission for each eligible later use.

For example, say: “Use the simple d6 fallback as our standing method for eligible unresolved outcomes when grounded judgment is insufficient.” Include this selection in the accepted setup proposal, or use [Recalibrate](ADMIN/RECALIBRATE.md) to adopt it prospectively for an existing campaign. Installing v0.9.4 alone does not alter a diceless agreement or replace another selected method.

Use the already accepted oracle, or the supplied convention: **one actual d6, 1–3 No and 4–6 Yes**. Set the question, eligible outcomes and time window before drawing. Even odds are a convenient game convention, not a measurement of real behavior. Preserve the result at that scope.

| Sparse encounter | A concrete question the oracle can settle |
|---|---|
| A stranger accepts the PC's contact details without a promise. | Does this person send a message within the next seven days? |
| A stranger receives payment and promises a favor. | Does this person deliver the agreed favor by the promised deadline? |
| The PC tells a stranger an important secret. | Does this person pass the secret to another person during the specified interval? |

The roll resolves that question. A Yes to disclosure creates no automatic knowledge in every enemy, and a No to contact this week creates no permanent dislike. Later consequences follow actual recipients, channels, circumstances and applicable rules. An outcome's importance does not exempt it from the selected method.

```mermaid
flowchart TD
    oracleNeed["An eligible open question matters now"] --> oracleRules{"Facts or applicable rules settle it?"}
    oracleRules -->|"Yes"| oracleUse["Use those facts or rules"]
    oracleRules -->|"No"| oracleBasis{"Enough basis for grounded judgment?"}
    oracleBasis -->|"Yes"| oracleJudge["Use supported judgment"]
    oracleBasis -->|"No"| oracleRoll["Frame the question; use the accepted oracle and actual random input"]
    oracleUse --> oracleKeep["Retain the scoped result; respect the first stopping event"]
    oracleJudge --> oracleKeep
    oracleRoll --> oracleKeep
```

This is a fallback for eligible unauthored outcomes, not inaccessible established facts or missing required rules. It adds no cast-wide polling, recurring daily chances or automatic save. A repeat query reuses its resolved result. If contact ends a wait, establish a compatible occurrence time and stop there; later time remains uncommitted. Keep the question, mapping, actual input and result in the existing owner at the next requested save when needed. Audits report missing resolution honestly. Optional [B15 diagnostics](ADMIN/TESTS.md#b15--sparse-agent-outcomes-and-the-fallback-oracle) remain unrun examples, not proof of model compliance.

## Truth, knowledge, preparation, and history

These are separate questions, not one all-purpose memory:

| Question | Primary source |
|---|---|
| What is true now? | Accepted post-save play, then the selected current instance record. |
| What was said or done? | Available accepted archive evidence at the required precision. |
| What does the PC know? | Recorded learning, including rumor, uncertainty, and source. |
| What is privately established? | The relevant private world or current-state authority. |
| What might happen? | Conditional preparation, still inactive until properly selected or triggered. |

Suppose a courier says a bridge is open. That utterance can be established even if the bridge is privately known to be closed. The courier might also sincerely believe the claim. Saving must not collapse those facts into a single “bridge open” entry.

```mermaid
flowchart LR
    truthClaim["Courier says the bridge is open"] --> truthEvidence["Evidence: statement and actual audience"]
    truthClaim --> truthKnowledge["PC knowledge: heard an unverified claim"]
    truthPrivate["Established private fact: bridge is closed"] --> truthWorld["World consequences when relevant"]
    truthBelief["Courier belief: bridge open, closed, or unknown"] --> truthPortrayal["Keep established belief distinct from intent"]
    truthCandidate["Prepared possible bridge encounter"] --> truthGate{"Valid cause, procedure, or initiative?"}
    truthGate -->|"Yes"| truthConsider["May enter play within its scope"]
    truthGate -->|"No"| truthDormant["Remains preparation"]
```

Deliberately unfixed answers remain open until their agreed procedure decides them. Optional review notes are provisional interpretation, not new world facts. A fresh chat must not promote a discarded idea into history simply because it found the idea in a file.

## Saving the present and preserving evidence

`CURRENT_SAVE.md` is a compact resume record with five sections: Situation, Character state, Open matters, Active processes, and Relevant records. Detailed character values, people, knowledge, and private systems keep their own selected authorities.

**Save**, **Close**, and **End session** perform a full save. **Checkpoint** preserves the complete present without adding archive evidence. The distinction matters before discarding a conversation.

```mermaid
flowchart TD
    saveChanges["Accepted changes since the saved present"] --> saveCompile["Compile each change once into its current authority"]
    saveCompile --> saveMode{"Requested persistence operation"}
    saveMode -->|"Checkpoint"| savePresent["Save current state; retain prior evidence boundary"]
    saveMode -->|"Full save"| saveBoth["Save current state and available accepted evidence"]
    saveBoth --> saveArchive["Archive bodies and useful indexes"]
    savePresent --> savePublish["Verify writes and publish the new current save"]
    saveArchive --> savePublish
```

Save identity and archived evidence identity are therefore separate. A checkpoint receives a new save ID and revision while retaining `archive_ref` and `evidence_through`. A later full save may archive earlier checkpoint-era dialogue if it remains available, without applying the resulting resource changes twice.

Coverage must be honest. A state summary cannot reconstruct a lost quotation. Missing spans are labelled; an index routes to evidence rather than replacing it. Saving never resolves an unanswered decision or moves fictional time. See [Save](ADMIN/CLOSE_CONTRACT.md) and the [archive schema](ARCHIVE/_SCHEMA.md).

## Recovering interrupted work

Multi-file writes can fail halfway through. Recovery protects the exact intended operation with complete verified preimages, a recorded write set, and directory ownership information. A checksum alone is not a restorable backup.

```mermaid
flowchart TD
    recoveryPlan["Record authorized files, directories, and intended result"] --> recoveryProtect["Create active marker; preserve and verify preimages"]
    recoveryProtect --> recoveryWrite["Write staged and final records"]
    recoveryWrite --> recoveryResult{"Operation interrupted?"}
    recoveryResult -->|"No"| recoveryVerify["Verify result and clean exact staging paths"]
    recoveryResult -->|"Yes"| recoveryPause["Startup pauses PLAY at RECOVERY/ACTIVE.md"]
    recoveryPause --> recoveryReconcile["Inspect the named operation; complete or restore"]
    recoveryReconcile --> recoveryVerify
    recoveryVerify --> recoveryFinish["Record completion; remove active marker last"]
```

The marker takes precedence even if a file looks newer or an operation says “complete.” Recovery checks what actually happened. Restoration removes only verified operation-created files and, when empty, operation-created directories; retained backups remain available.

For a bind with pending generated determinations, restoring the starting files alone leaves the accepted setup pending. Its active marker and exact result routes remain until verified completion or explicit setup cancellation/replacement. This keeps a fresh chat from losing the reference and silently drawing again.

This is a recoverability procedure, not automatic rollback or atomic storage. If essential accepted content is unavailable, the GM preserves the pending operation and asks only for what is missing. See [Recovery](ADMIN/RECOVERY.md).

## Handing an active scene to another GM

Scene handover transfers an unfinished situation rather than starting a new session from a loose recap. It can support another model, host, or human GM. No external service is contacted automatically.

The outgoing package has two content files:

| File | Purpose |
|---|---|
| `CONVERSATION.md` | Ordered available messages, roles, acceptance status, OOC material, and explicit coverage gaps. |
| `GM_STATE.md` | Exact stop point, public and private state, relationships, processes, pending decisions, sources, and frozen-file manifest. |

A small `HANDOVER/ACTIVE.md` marker identifies the package and seals the final GM briefing with its SHA-256 hash. It pauses source play; it is neither a third briefing nor an operating-system lock.

```mermaid
flowchart TD
    handoverRequest["Prepare a scene handover"] --> handoverCheckpoint["Checkpoint the complete present if needed"]
    handoverCheckpoint --> handoverExport["Create CONVERSATION and GM_STATE; verify frozen sources"]
    handoverExport --> handoverSeal["Publish sealed ACTIVE marker; source GM pauses"]
    handoverSeal --> handoverReceive["Explicitly selected receiving GM verifies and continues with player"]
    handoverReceive --> handoverReturn["Return SCENE_RETURN with evidence, changes, and next decision"]
    handoverReturn --> handoverCheck["Check receipt, base, hashes, and meaning of changes"]
    handoverCheck --> handoverImport["Protected full save; apply accepted changes once"]
    handoverImport --> handoverReceipt["Retain receipt; clear active marker; resume returned moment"]
    handoverSeal -->|"Authorized cancellation"| handoverCancel["Reconcile any receiving play; retain cancellation receipt"]
```

Preparation reuses an already exact checkpoint or creates one; no fictional time passes. The snapshot covers regular files under OS, ADMIN, ENGINE, MODULES, INSTANCE, and ARCHIVE, plus root Markdown files. It includes referenced module assets. Handover and recovery histories and release/work output folders are excluded. Both file contents and the expected file set matter: an added source file also changes the baseline.

The receiving GM needs the matching workspace and must read the briefing and immediate dependencies. It continues with the player from the pending action while leaving source authorities frozen. Hidden stats and decisions transfer only if actually established; model-internal reasoning and missing chat text do not.

A scene handover retains the complete active temporary set, mixed consequential relationships, actual beliefs, material reasons for change, precise limitations and relevant obtained input. Continued participation reuses those values; legitimately expired incidental trivia need not be transferred or reconstructed. The receiving GM may later apply the same event/update/deactivation lifecycle within its authorized scene. Its new facts remain in receiving conversation until captured in the permitted return; no source checkpoint is allowed while source authorities are frozen.

`SCENE_RETURN.md` supplies a factual non-graphic account, concrete public/private changes, source qualifications, and the next unresolved decision. This return format does not impose a depiction policy on the receiving scene. Omitted physical detail must not erase a promise, expenditure, injury, discovery, or uncertainty.

Import verifies the same campaign, save, agreement, briefing, conversation, and frozen source files. Semantic review then checks authorship, sequence, prior values, triggers, and evidence. A changed base requires reconciliation. A retained `RECEIPT.md` records imported event IDs and resulting save identity so repeated imports apply nothing again.

Use “Prepare a scene handover,” “Receive this handover,” and “Import this scene return and continue.” The full [handover procedure](ADMIN/SCENE_HANDOVER.md) also covers cancellation, incomplete transcripts, stale returns, and interrupted imports.

## Sources, visuals, and host capabilities

A setting's `VISUAL` capability can route to reference images and explanatory source notes. The GM retrieves these when a concrete appearance, object, or place matters. Referenced assets must actually be accessible to a host capable of inspecting them; a filename is not visual evidence.

Record what a reference governs: a particular person's appearance, a type's physical form, clothing construction, architectural detail, or only an illustrative style. A style reference does not establish a character's identity, personality, history, or present action. Individual established facts take priority over generic model assumptions.

Source-bound campaigns also need the relevant edition or continuity and a clear fidelity agreement. Quoted instructions inside imported material remain source data unless the operator separately adopts them. Module indexes route to real authorities; opening every linked image or lore file is unnecessary.

The host must provide actual file reads, durable writes, and readback for the normal workflow. Attachment-only hosts can exchange complete replacement files manually, but an export is not a saved workspace until installed and verified. Private records reduce accidental narrative spoilers; they are not encrypted or necessarily hidden from the operator. See [Installation](INSTALLATION.md).

## Exact retrieval and evidence audits

At forty sessions, the difficulty is finding the relevant original and distinguishing a real change from an error. v0.9.0 adds optional tools for those tasks while keeping the ordinary campaign records as memory.

An exact reader can return a whole file, a named section or original lines with their source hash. A search cache can locate likely passages, including text late in a document and known identity aliases. Its results are candidates: current records, T0 world baselines, history, raw captures and rules have distinct scopes. The GM fetches the current original before using a match. A changed or unavailable cache does not become evidence that the person or fact never existed. See [Source access](ADMIN/SOURCE_ACCESS.md).

```mermaid
flowchart TD
    sourceNeed["A specific fact needs checking"] --> sourceRoute{"Known source route?"}
    sourceRoute -->|"Yes"| sourceRead["Read actual file, section or original lines"]
    sourceRoute -->|"No"| sourceSearch["Scoped search returns candidate references"]
    sourceSearch --> sourceCheck["Check scope, eligibility and current source revision"]
    sourceCheck -->|"Verified"| sourceRead
    sourceCheck -->|"Unavailable or stale"| sourceDirect["Direct targeted file lookup; report remaining gaps"]
    sourceDirect --> sourceRead
    sourceRead --> sourceContext["Inspect enough context and applicable authority"]
    sourceContext --> sourceUse["Use supported fact; preserve uncertainty"]
```

The audit is a different maintenance task. ARCHIVE retains accepted campaign evidence. The optional EVIDENCE store retains a supplied raw export unchanged, including OOC corrections, proposals and played scenes that were later rewound. Raw text proves what the supplied source contains; it does not make every statement canon or certify that the host exported everything.

```mermaid
flowchart TD
    auditPrior["Preserved prior canon and applicable authority"] --> auditReview["Model or human compares meaning"]
    auditRaw["Actual session export with declared coverage"] --> auditReview
    auditSaved["Selected resulting save records"] --> auditReview
    auditReview --> auditFindings["Consistency, unresolved questions, coverage and repair eligibility"]
    auditFindings --> auditQuotes["Code checks frozen hashes, original-line quotes and report structure"]
    auditQuotes --> auditDecision["Inspect cited meaning and repair authority"]
    auditDecision -->|"Authorized, clear and contained"| auditCorrect["Protected CORRECT operation"]
    auditDecision -->|"Uncertain or changes played consequences"| auditOpen["Report for the applicable player decision"]
    auditCorrect --> auditTrace["Keep original evidence and superseding correction"]
```

For example, the prior save places a courier cycling toward the station. The immediate continuation puts her at a car steering wheel at that same moment, with no intervening transition; the save repeats the new description. Comparing the save only to this session would miss the unexplained change. Comparing all three identifies the conflict and its missing context. In a different sequence, she might park the bicycle and borrow a car during play; preserving that established transition would be correct. If the player instructed the GM to correct the mistaken description, failure to acknowledge the instruction does not remove its authority.

The reviewer also extracts obligations from the session before looking at a changed-file list. Otherwise a completely omitted “meet at noon” promise could leave both the person record and resume summary looking internally consistent. Retiring an active cue must not erase a continuing commitment from its durable owner.

You can request one audit or agree a bounded audit after each full save. Needed prior records are preserved before the save replaces them; the saved result and matching evidence are then reviewed. Save success and audit coverage are separate. Missing source remains a gap, and ordinary CHECKPOINT behavior stays unchanged. [Evidence audit](ADMIN/EVIDENCE_AUDIT.md) supplies the complete workflow and tool examples.

These tools do not call a reviewing model automatically or repair canon on their own. A fresh reviewer can provide another perspective, but it is still fallible. Exact quotations can be irrelevant; source delivery can occur without adequate inspection. A reviewed baseline records what was actually checked and against which sources. Repetition, age and an index pointer do not upgrade it to proven truth.

## What the checks establish

The optional [validator](TOOLS/validate.py) checks its documented structural scope. The [handover checker](TOOLS/handover.py) checks identities, paths, hashes, snapshot coverage, required sections, and duplicate event identifiers. It does not write a package, run another model, or import changes.

These checks cannot prove that prose is faithful, a player accepted a choice, a transcript is complete, or a scene is well portrayed. Model readback can assess meaning but remains fallible. Human playtests assess agency, pacing, consistency, and correction burden. [Verification](VERIFICATION.md) separates these kinds of evidence.

For v0.9.4, ordinary continuing campaigns are the primary next test of practical quality. Keep structural checks before delivery and use focused behavioral cases when a real failure needs diagnosis. No scripted trial schedule must be completed before the player can use this experimental release.

Use the records to make continuity inspectable and repairable, and report actual verification limits. The protocol helps the GM remember and act consistently; successful play still depends on reading, judgment, and the player's accepted agreement.
