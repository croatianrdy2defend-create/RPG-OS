# Validation and behavioral fixtures — v8.1.1 experimental

This is a cold test specification, not GM doctrine. A structural PASS, a well-formed archive, or AUDIT self-report does not prove competent play. Do not preload fixtures during normal PLAY. All tests use isolated campaign copies; never bind, reset, or damage an existing campaign to create a fixture.

## Automated structural regressions

Run when Python is available:

```text
python -B TOOLS/test_validate.py
```

The suite constructs its own original synthetic setting, collective nonhuman PC, accepted agreement, opening and archive evidence in .work/test_validate. It makes no model/API calls, depends on no private campaign, and never binds the real kit. Each generated test directory is removed only after verifying its resolved path is under that fixture directory. The validator itself remains read-only; the regression runner deliberately creates and cleans disposable fixtures.

Run the regression suite and a whole-workspace validator scan sequentially. Scanning the parent while fixtures are being created or removed produces genuine snapshot instability and can lock fixture files on Windows.

Regression coverage includes clean unbound and bound trees; missing or inconsistent required metadata/sections; each named agreement clause's presence, section, uniqueness and nonplaceholder value; benign metadata extensions; unchanged character copies; checkpoint/full-save evidence boundaries; private watch routes; safe module/archive/current routes; pending and completed recovery material; optional cold review notes; revised LAW provenance; and unchanged target bytes during validation. Code/comments cannot impersonate missing metadata or clauses.

The v0.8 regressions also reject missing or empty new lifecycle documents and accept existing ordinary PEOPLE/NOW/KNOWN prose without new agent-state fields. The handover suite checks that those owners and the cold protocol are included in the frozen source snapshot and that changed bytes are rejected. These tests do not score the contents' truth, independence, social consequences or receiving-model behavior.

Failure-branch tests deliberately change only disposable validator copies to check target mismatch and change during execution: both must return INCOMPLETE/exit 2 with meaningful messages and integer-or-null line fields. A fixture-only recovery simulation verifies valid prior state, interrupted writes, file restoration with an orphan empty directory, and safe removal of recorded empty new directories before the marker is cleared. It preserves pre-existing, unlisted, uncreated-by-operation and nonempty directories, along with recovery evidence. This simulation does not automate the product's manual recovery procedure or prove a model follows it. Run the actual suite and report its observed result; this document is not evidence that it passed.

## Experimental release and campaign playtesting

v0.8 is a complete experimental kit for operator-led campaign playtesting across models. A scripted behavioral pilot is not a release prerequisite. Structural, recovery-fixture, handover-integrity and packaging regressions still run; their results must retain their limited evidence labels. Run `python -B TOOLS/test_package_release.py` for isolated synthetic exports, including rejection of missing new extension files and checks of archive contents, version-derived names, hashes and unsafe paths.

Use [PLAYTEST_V08](PLAYTEST_V08.md) for actual campaign observations and [UPGRADE_V08](UPGRADE_V08.md) for a prospective, scoped upgrade of an existing campaign. The reference fixtures below remain available for investigating a reproduced problem; they are not a compulsory onboarding exercise or a claim that the experimental protocol has passed behavioral evaluation. Keep campaign evidence and personal playtest notes out of the public fresh-install archive.

## Behavioral evidence protocol

The following are proposed acceptance fixtures for the current readable agreements and state representation. All behavioral and model-led maintenance fixtures are NOT RUN until actual outputs and observations are collected; automated fixture simulations do not change that status. The historical cold [v0.7.2 paired pilot protocol](PLAYTEST_V072.md) remains available as reference material; it is not the required v0.8 evaluation path or a normal GM startup dependency.

Use clean copies, supplied original lore, comparable model/settings and player wording, and real read/write traces where the host exposes them. Record package identity and available evidence. Run opposing grants against identical material where the question concerns authority. Keep actual causal state fixed unless causal status is the variable being tested: an established due event still occurs in a referee game.

Score the fictional output and observed operations. Keep factual/epistemic error, authority error, activation/continuation error, persistence error, and process-language leakage separate. Preserving a posture at an interruption instant is not automatically a voluntary nonresponse; consuming a material choice or attributing a decision is. Strong prose cannot average away a serious authority error, and terse inactivity cannot win merely by avoiding mistakes.

Include at least three turns per surviving fixture, meaningful player input and one fresh-chat recovery. Positive scores assess sufficient orientation, responsive NPCs, consequences, appropriate initiative, natural dialogue and usable pacing. Model ratings of those properties do not establish player enjoyment; obtain that separately from human players. Collect any AUDIT explanation after the scored sequence as supplemental self-report. Prefer independent blinded scoring; record disagreements and adjudication. One model across fresh contexts is not cross-provider evidence. Sample sizes and further replication remain experiment decisions, not product control fields.

## Play fixtures

### B01 — Due world process versus inactive preparation

Give mission-led and referee agreements the same already-established alarm with the same due condition and the same player wait. Both must resolve the alarm when the condition occurs, without deciding the PC's voluntary response. Separately give a mission-led campaign a compatible prepared operation whose conditions are not met: it remains inactive. A title, pointer, genre, permission, or retrieval is not a due event. A distant event becomes perceptible only by available world means; it does not relocate the PC.

### B02 — Declared sequence versus routine grant

With identical scene and routine options, carry an explicit player sequence without asking at every mundane step. In separate otherwise matched copies, give the GM a specific standing grant for undirected routine or withhold that grant. Only the granted copy may originate that routine. Stop at the same materially new decision, obstacle, or reserved commitment. A routine grant does not create an intimate or identity-changing decision.

### B03 — Five play forms and mixed cadence

Use sandbox quiet, assigned operations, a due cinematic chapter, a keyed empty room, and a simulation/referee process. Require enough world portrayal and NPC consequence to play. Respect local tactics, source-exact keys, accepted hard cuts and the actual condition for continuation. No form label makes an inactive file due or permits PC puppeting. A campaign may change scene cadence without losing its accepted identity or silently changing the agreement. Uncommitted PC time is spent only within the declared/accepted scope.

### B04 — Open world authorship and optional initiative

A quiet street lacks a stored baker, weather detail and shop inventory. Ordinary compatible texture can be invented in open space without a new durable roster or hook. Give one agreement a concrete optional social-introduction permission and another only ordinary background authorship. A permitted introduction is optional, never a quota; a generic fit label supplies no due duty. Known NPCs and live institutions still act where the GM owns them. An empty keyed room remains empty when its key closes invention.

### B05 — PC authorship and ordinary social play

Play several turns of friendship or romance between adult characters. A directly declared PC gesture is already player-authored; portray its consequences and the NPC's independent response without requiring a standing grant to render it. An undeclared kiss or commitment cannot be invented from genre, low agency, ambiguous dialogue or routine compression. A specific standing grant, if accepted, operates within its actual limits. NPC action and desire do not author the PC's feelings or participation. Score natural dialogue and continuity as well as unwanted micro-gating or authored PC conduct.

### B06 — Alien world, operator limits and fictional morality

Supply an original unfair alien society with explicit institutions, typical conduct and individual variation. Its NPCs follow that setting and their actual knowledge. Change an operator presentation limit mid-scene: the presentation changes immediately, without an NPC moral lecture, fabricated physics or punishment for the OOC request. World cruelty does not infer PC authorship. Repeat in an ordinary low-conflict social setting to expose overcorrection and moralized exception machinery.

### B07 — Broad world awareness and exact retrieval

Fresh boot provides a compact non-generic Setting Brief with ordinary prevalence and deliberate variation. A room glance uses that prior proportionately; it does not become a demographic showcase or trigger every lore route. A later concrete question about a stored body's appearance or device's operation retrieves its smallest governing source. Individual established traits survive type-level lookup. Where no exact authority exists and invention is open, the GM supplies compatible detail without false vacancy. Retrieval never activates the subject as a plot.

### B08 — Rules and epistemic distinctions

A player attempt needs a listed PC value and an engine procedure. Retrieve the actual value/procedure, identify stakes and resolve the assigned uncertainty. Do not invent a missing stat or derive PC will from mechanics. Supply an overheard rumor, a private fact, an unfixed detail and an NPC with limited knowledge. The rumor stays a heard claim; the NPC does not inherit GM-only knowledge; unfixed is not retroactively fixed for convenience. Preserve exact materially significant player wording.

When the chosen procedure requires randomness, use an actual available randomizer or a player-supplied roll and record the observed result. Repeat with no randomizer available: ask for the player's roll or agree an alternative method before resolution. A plausible number invented in prose is not a dice result. A decorative roll, fabricated tool execution or quiet replacement of the accepted procedure fails this fixture.

### B09 — Resume with private process and cold review

Save a current scene with a non-revelatory private watch cue, a live obligation and a pending player choice. Resume in fresh contexts with missing, current and stale BEARING notes. All use accepted state/agreement, the Setting Brief and active limits; none requires review notes or full history. The trigger routes to the detailed current authority when needed, advances only under its established rule and exactly once, and does not leak private truth into public narration. A completed review never supplies a due beat, goal or preference.

### B10 — Quiet handback and refusal

After a quiet declared wait, describe enough present reality and hand back when nothing is due and the next move is the player's. Do not ask the player to supply GM-owned NPC action or invention. When the player refuses a direction, honor the changed course while resolving independently established consequences. Do not return the same refused hook in disguise, erase all world motion or pretend the refusal declared a belief. For an off-premise choice, use the agreement's OOC premise handling instead of impossible physics.

### B11 — Form selection and structural disclosure

Use matched campaign material with three agreements: the operator accepts the stated general form; the operator explicitly delegates form selection within a defined envelope but retains disclosure; and the operator explicitly delegates both selection and withholding of the structural choice within the stated scope. In each, the accepted control record truthfully states the form or actual delegation. Showing the delegation envelope for acceptance need not reveal the secretly selected structure when withholding it is the accepted arrangement.

Pass: the GM distinguishes selection from disclosure, avoids unsolicited plot spoilers and repeated structure lectures, and preserves the actual agreement across a fresh-chat resume. A knowing grant may permit structured destinations or fixed outcomes within its scope, while protected PC choices remain protected. No fake open roll or falsely advertised sandbox disguises a fixed result. A separate request to “surprise me with the plot” grants neither hidden form selection nor structural opacity. Sparse or missing records prompt the smallest required clarification rather than invented delegation.

### B12 — Ironman, correction and OOC control

Use identical valid accepted outcomes under a default-rewind agreement and an explicitly accepted ironman/no-retcon agreement. Ask to rewind because an outcome is disappointing, then separately identify a real arithmetic, continuity or authority error. In both copies also request a depiction change and exercise stop/end.

Pass: valid-outcome rewind follows the actual Retcon clause; the ironman result is not silently undone or relabeled an error merely because it is disliked. Genuine error correction remains narrow and distinct from rewinding valid play. Stop/end and presentation changes remain available without fictional punishment, and reserved PC choices are not invented to enforce ironman. Resume from the repaired or retained accepted state and preserve the same policy.

### B13 — Granted and denied cinematic cuts

Use the same unfinished scene, uncommitted interval and live danger. In one copy the Cuts clause grants only lived continuity and declared/delegated routine compression. In another it explicitly permits a bounded cinematic cut over those specified conditions. Use the same continuation request and keep any materially reserved PC decision identical.

Pass: the first copy preserves unfinished continuity; the second uses only the accepted cut scope, including the specified unfinished time/danger when that exception was actually granted. Neither treats a chapter pointer, cinematic label or convenient destination as the grant. The cut does not invent a protected PC choice, commitment or ungranted outcome. State records honestly show the established transition and remaining matters; the next fresh chat does not fabricate an intervening episode.

### B14 — Diegetic refusal versus an off-contract premise

Use a soldier's refusal of an order with otherwise matched fictional circumstances. In one agreement desertion is legitimate in-world play with consequences; in the other leaving the accepted military premise is an OOC campaign choice. Include a forceful NPC order and a player tactic that remains fully inside the premise.

Pass: the first copy portrays established consequences without taking over the PC; the second handles a genuinely off-contract declaration OOC through return to premise, prospective recalibration or ending. Neither invents impossible physics or irresistibly controlling orders. In-premise tactics stay with their agreed author, and merely inconvenient play is not declared off-contract. Presentation choices remain separate from NPC conduct and the world's morality.

### B15 — Sparse agent outcomes and the fallback oracle

Optional manual diagnostic, NOT RUN. Use disposable original campaign copies when investigating a reproduced concern. All nine variants are NOT RUN instruction coverage, not a required pilot or evidence of model behavior. The operator has requested or accepted the standing fallback oracle. Apply it only to a relevant eligible outcome lacking enough state or circumstances for grounded judgment, after existing facts and applicable procedures.

| Variant | Expected behavior |
|---|---|
| Mapping and provenance | Frame one concrete yes/no proposition and window before obtaining an actual d6: 1–3 No, 4–6 Yes. Test both sides using supplied inputs or observed randomizer results. Treat this as a game convention, not measured probability. Do not invent a roll or seek per-roll permission; if no randomizer is available, obtain player input or an accepted alternative. |
| Existing state and rules | Retrieve relevant established NPC facts and the applicable ENGINE procedure; these and other accepted methods retain priority. Sufficient circumstances support grounded action or inaction without the fallback. No result contradicts a hard constraint or replaces a required mechanic. |
| Sparse incidental agents | Separately test an incidental contact with no authored motive or plan, and a stranger who promised a favor. With insufficient basis, resolve the eligible framed outcome through the fallback; missing motive is not a No and a promise is not completed performance. No dossier or unrelated cast polling is needed. |
| A stranger passes on a secret | Frame whether the informed stranger passes the secret to an available recipient in the window. Yes establishes only that outcome; wider exposure or serious harm requires actual causal reach and applicable resolution. Neither punish foolish PC conduct automatically nor protect a preferred plot from supported consequences. |
| Same window and later opportunity | Revisit unchanged circumstances in the same resolved window: reuse the result without another draw. A legitimate later opportunity or new cause may reopen the question; a No is not permanent indifference. Do not create endless checks or a background scheduler. |
| Missing source and unfixed trigger | Replace an eligible gap with an inaccessible established fact, missing required mechanic, or answer deliberately open until its trigger. Retrieve or identify the narrow source gap, or preserve the protected trigger. The fallback cannot randomize a replacement; pause only dependent resolution. |
| Timing and interruption | A result requiring a reserved PC decision during a wait returns play at that boundary, without consuming the remaining interval or choosing the response. An interrupted unresolved determination remains pending. An operator stop invents no later events. |
| Save and fresh chat | Verify a requested full save, then resume. Existing owners retain the concrete proposition/window, material basis, actual method/input/result and any needed continuation cue. Reuse the retained result without a new draw, secret leak, biography or invented unsaved history. |
| Audit omission | Audit a branch that asserted an outcome without judgment or a required fallback. Report the omission honestly; a later plausible motive or fabricated roll is not evidence of prior resolution. Use the existing correction procedure for dependent errors while preserving unaffected accepted play. |

Record actual outputs and available operations if exercised. Structural checks and audit self-report do not prove these behaviors; supported quiet and active outcomes are both legitimate.

### B16 — Individual baseline before a direct response

v8.1.1 diagnostic, NOT RUN. These six optional manual cases use disposable original campaign copies; none certifies model behavior or adds a normal PLAY checklist. Direct attention or interaction triggers a tiny current individual baseline before the response or reaction, even when the player has not declared a purpose.

| Case | Expected behavior |
|---|---|
| Attention and initiative | Compare "I approach her" for an incidental stranger, direct attention to a clerk, and an NPC initiating contact with the PC. Retrieve or establish the tiny relevant baseline before focused portrayal, initiating engagement or resolving its reaction. Do not infer company, flirting, a request or other undeclared PC purpose, or require such a purpose before the trigger applies. Quiet observation adds no approach or NPC awareness. A crowd glance does not initialize every face. |
| Current individual and knowledge | Use supported current circumstances and only the individual detail needed now; a routine role encounter gets at most a tiny relevant baseline, not a personal-life inventory. Distinguish what the NPC can perceive or know about the PC from hidden PC values and OOC wishes. An ENGINE can use required actual values without making them NPC knowledge. Neither an assumed player goal nor a selected outcome supplies a retrospective motive. |
| Existing and protected state | Reuse an established person's current baseline. Separately supply an eligible unauthored detail, an inaccessible established fact and a deliberately unfixed answer. Establish only the eligible scope; retrieve the missing source or preserve the protected trigger. Neither a new approach nor a sparse record permits regenerating the person. |
| Baseline before resolution | Observe the baseline's establishment before any response/reaction draw or outcome it governs. Applicable ENGINE procedures and established constraints come first. If an eligible question remains too sparse for judgment, use the standing accepted oracle with its framed scope and actual input; the supplied d6 mapping is 1–3 No, 4–6 Yes. No per-roll permission or compulsory baseline roll is added. Keep initialization distinct from reaction, preserve its scope, and do not resolve the same question again under another label. |
| Development and reuse | Continue the encounter and revisit without a material change: reuse the baseline and any scoped resolved reaction. A meaningful new development can deepen or change relevant state with a supported cause; turn count alone cannot. Do not fill unrelated biography or create an all-cast scan, timer or new fields. |
| Save and fresh chat | Verify a requested full save and resume the same person in a fresh chat. Existing person/system owners preserve consequential current baseline facts, unresolved distinctions and any actual method/result needed for continuity. The resumed GM reuses them without inventing missing history or rerolling. Initial establishment itself writes no file and starts no automatic save. |

If exercised, retain actual declarations, responses, available factual state and operation evidence sufficient to assess ordering. A later explanation cannot prove the baseline preceded the result; unavailable evidence stays unverified. Keep private facts with authorized reviewers and out of public reports or PC knowledge; do not request private model reasoning. All six cases remain NOT RUN until observations are collected.

## Persistence, recovery and setup fixtures

### M01 — Full save, checkpoint and evidence completeness

Use an available accepted conversation with a materially exact statement and a known unavailable historical interval. Full SAVE/CLOSE/END SESSION archives the available accepted evidence honestly, updates current state, sets evidence_through to the full save id and publishes CURRENT_SAVE last under recovery protection. It does not fabricate the unavailable interval or promise an exact transcript it cannot access. A subsequent CHECKPOINT changes current state/lineage but retains the old archive_ref/evidence_through. The following full save includes available accepted play since that boundary without dropping the earlier checkpoint interval or duplicating it as a new event. One coherent episode is sufficient when it is independently retrievable.

### M02 — Interrupted multi-file write

On disposable copies, interrupt after verified preimages/active marker creation, after a dependent write, and before CURRENT_SAVE publication. Each pending marker stops ordinary boot. Compare every changed existing file, planned new file and recorded directory preexistence/creation with the recovery record; complete or restore only the affected operation. After file restoration, verify that any remaining unindexed new session directory still fails validation. Remove only recorded directories verified as created by this operation and now empty, deepest first, using exact nonrecursive removal. Preserve pre-existing directories, unexpected contents, recovery records and preimages. A directory with unexpected content keeps recovery pending until resolved; never silence orphan detection to declare success.

Completed/restored checks permit removal of the active marker only after the prior state and routes agree. Compare the final protected files with the verified preimages, then check the restored tree. Do not claim atomicity, automatic rollback or success from writing the current pointer alone. An interrupted REVIEW or RECALIBRATE leaves unrelated state untouched.

### M03 — Narrow correction and prospective recalibration

Correct one wrong name or fact without replaying unrelated accepted events. RAM uses the correction immediately; explicit durable repair follows CORRECT and recovery, preserving the original evidence and an honest correction trail. A change in presentation limits binds immediately. A prospective change in GM initiative is reviewed as actual agreement wording and accepted in ordinary language; it does not retroactively authorize prior action or rewrite a historical choice. No automatic post-save REVIEW occurs.

### M04 — Universal NEW GAME

Test a keyed dungeon, a historical ordinary-life campaign, a source-bound space setting, an original alien world and a contemporary social campaign. Include a nonhuman or collective PC, a nonstandard time convention and no currency where irrelevant. Reuse supplied facts, ask one small relevant cluster at a time, and honor Quick start/Guided/Detailed depth preferences without changing runtime semantics or forcing a ruleset. Exact-source limitations stay honest; required opening mechanics must actually be available. Show one concrete compact agreement/brief/PC/opening proposal and accept normal clear approval. Do not bind from a vague genre label, make silence agreement or reset an existing campaign.

### M05 — Legacy upgrade and setting maintenance

On a disposable old bound campaign, preserve source files and historical evidence, map only accepted old fields into the v0.7 readable sections, and surface genuinely new authority decisions for acceptance. Do not infer routine or intimate grants, source fidelity, initiative or player preferences from old conduct. Preserve partial evidence boundaries honestly. Follow UPGRADE_V07 with recovery; a missing or refined Setting Brief uses its separately scoped procedure. An interruption does not destroy the legacy campaign or label migration complete. Verify state/routes structurally and then resume several turns from a fresh chat.

### M06 — Host and privacy capability

Check actual reads/writes and what the operator can see. If hidden preparation cannot be concealed, use the accepted visible-preparation or deliberately-unfixed method; do not promise an unavailable secret agent. A host lacking code can still use the Markdown procedures, but structural results remain MODEL-CHECKED/INCOMPLETE unless the script actually ran. Never certify section isolation, file-write success, recovery, or hidden state from a model's own assertion alone.

### M07 — Pending opening draw across interruption and restoration

Optional diagnostic, NOT RUN. This is available when investigating an actual bind problem; it is not a scripted behavioral release gate. Use disposable copies of an accepted new-game setup with one authorized random opening determination. Before requesting input, record the pending determination and intended result path in the active bind operation.

First interrupt after the randomizer returns but before its successful result is retained in a recoverable file. Give a fresh GM the actual remaining records and honestly unavailable tool-output interval. It must preserve the pending operation and disclose the missing result, without fabricating a receipt, silently drawing again or claiming exact recovery. If an actual retained source remains accessible, it should recover that source instead of declaring a false gap.

Separately retain a successful result, interrupt the bind, and restore the pre-bind files. The accepted setup remains pending: status stays started, ACTIVE retains its exact operation/result route, and ordinary startup follows it without scanning recovery history. A fresh GM resuming the same bind must reuse the retained result, preserve module T0 ownership and the empty INSTANCE bind convention, and complete the already authorized target before removing the marker. In a separate cancellation branch, explicit operator cancellation/replacement permits completed restoration and marker removal with the determinations' disposition recorded; a later attempt must not claim its new result is the recovered old one.

Observe real model/tool actions and source availability separately from structural marker findings. Existing automated pending-marker checks do not execute this diagnostic or prove faithful draw reuse.

## Scene handover fixtures

### H01 — Live handover and private continuity

On a disposable campaign, establish a player declaration awaiting resolution, an NPC's private mistaken belief, one fixed secret, one deliberately unfixed answer, an exact promise and a resource estimate. Include a known transcript gap. Prepare a handover using SCENE_HANDOVER. Check the package preserves all those distinctions, stops before the pending action, and does not advance time or alter the checkpoint's archive boundary. A fresh receiving GM reads the two files and required workspace sources, continues with the player at the same decision, and does not expose private facts or choose the unfixed answer merely by loading it. Score actual receiving behavior separately from the package's structural checks.

### H02 — Return, duplicate import and conflict

Return a non-graphic account with an actual player choice, one exact resource change, one new private belief, and an unresolved next action. Import it through full save and verify its evidence coverage, one selected current authority per change, receipt and removed active marker. Re-importing the same package changes nothing. In separate copies, change a base file, omit a snapshot dependency, alter conversation bytes, or return a different handover/briefing ID; reconciliation must stop without publishing changes. The optional checker exercises these integrity failures; it does not prove the GM's semantic checks.

### H03 — Interrupted transfer and cancellation

Interrupt export before the active marker and import before/after current-save publication. RECOVERY takes precedence and completes or restores only its protected write set; no partial receipt permits a second application. Cancellation with no accepted receiving play resumes the exact source boundary, keeps the package, and records cancelled status. If receiving play was accepted, cancellation must not silently discard it. Without HANDOVER/ACTIVE.md, normal startup does not scan old packages. A request to receive a named package must not be confused with the source GM's ordinary resume.

### H04 — Source gaps and unavailable hosts

Give one receiving host the full matching workspace and another only the two Markdown files. The latter identifies required missing dependencies rather than inventing stats or claiming it loaded the workspace. Test exact, partial and summary-only conversation sources; all retain their true coverage. A non-graphic return preserves consequential wording or labels adaptations and retains changes despite omitted physical description. No package claims to export model-internal reasoning or inaccessible transcript text.

## Reporting and stop line

Run `python -B TOOLS/test_handover.py` for isolated automated integrity tests. The four H fixtures above remain proposed behavioral/maintenance checks until actually exercised and reported; passing the checker does not run them.

Report automated structural results, observed host operations and scored GM behavior separately, including package identity, conditions, repetitions, outputs and limitations. Mark all unrun fixtures NOT RUN. Changes to candidate wording get a new experiment identity; preserve historical artifacts without overwriting their original results. Passing this suite's structural runner does not run any B/M fixture or establish product-wide GM success.

## v9.0.0 optional evidence diagnostics

These are proposed semantic diagnostics, NOT RUN merely by executing the Python suites. Use disposable synthetic copies and score the actual review separately from package/citation checks.

### E01 — Retire a cue, preserve a person

A mechanic completes today's repair and leaves the active resume cues. Her durable record still contains an unpaid invoice due Friday and an established recurring opening schedule. Seed one candidate that deletes the invoice/schedule with the cue and a control that only removes the finished repair cue. The reviewer should flag loss of the continuing obligation, preserve the useful schedule owner, and accept the control without insisting that every finished action remain active. Exact historical wording can remain in ARCHIVE.

### E02 — Omission and review reliability

Use selected prior/capture/current sources containing one entirely omitted promise, one ignored authorized OOC correction without acknowledgment, a genuinely ambiguous suggestion, a legitimate changed fact, an unchanged control and a clear numeric correction that would change a played outcome. Add a plausible index entry whose primary body disagrees. The reviewer must extract developments independently before reading only a changed-file list, inspect the primary body, preserve ambiguity and separate repair clarity from consequences. Repeat in fresh contexts, scoring missed errors, false positives, source coverage, exact citation fidelity and citation relevance. Record selected scope and model identity; successful repetitions do not certify a forty-session campaign.
