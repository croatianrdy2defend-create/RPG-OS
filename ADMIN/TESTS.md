# Validation and behavioral fixtures — v0.7.2

This is a cold test specification, not GM doctrine. A structural PASS, a well-formed archive, or AUDIT self-report does not prove competent play. Do not preload fixtures during normal PLAY. All tests use isolated campaign copies; never bind, reset, or damage an existing campaign to create a fixture.

## Automated structural regressions

Run when Python is available:

```text
python -B TOOLS/test_validate.py
```

The suite constructs its own original synthetic setting, collective nonhuman PC, accepted agreement, opening and archive evidence in .work/test_validate. It makes no model/API calls, depends on no private campaign, and never binds the real kit. Each generated test directory is removed only after verifying its resolved path is under that fixture directory. The validator itself remains read-only; the regression runner deliberately creates and cleans disposable fixtures.

Run the regression suite and a whole-workspace validator scan sequentially. Scanning the parent while fixtures are being created or removed produces genuine snapshot instability and can lock fixture files on Windows.

Regression coverage includes clean unbound and bound trees; missing or inconsistent required metadata/sections; each named agreement clause's presence, section, uniqueness and nonplaceholder value; benign metadata extensions; unchanged character copies; checkpoint/full-save evidence boundaries; private watch routes; safe module/archive/current routes; pending and completed recovery material; optional cold review notes; revised LAW provenance; and unchanged target bytes during validation. Code/comments cannot impersonate missing metadata or clauses.

Failure-branch tests deliberately change only disposable validator copies to check target mismatch and change during execution: both must return INCOMPLETE/exit 2 with meaningful messages and integer-or-null line fields. A fixture-only recovery simulation verifies valid prior state, interrupted writes, file restoration with an orphan empty directory, and safe removal of recorded empty new directories before the marker is cleared. It preserves pre-existing, unlisted, uncreated-by-operation and nonempty directories, along with recovery evidence. This simulation does not automate the product's manual recovery procedure or prove a model follows it. Run the actual suite and report its observed result; this document is not evidence that it passed.

## Behavioral evidence protocol

The following are proposed acceptance fixtures for the current readable agreements and state representation. All behavioral and model-led maintenance fixtures are NOT RUN until actual outputs and observations are collected; automated fixture simulations do not change that status. The optional cold [v0.7.2 paired pilot protocol](PLAYTEST_V072.md) specifies an original small campaign, fixed player inputs, fresh-context continuation and file-based scoring. It is coordinator material, never a normal GM startup dependency.

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

Supply an original unfair alien society with explicit institutions, typical conduct and individual variation. Its NPCs follow that setting and their actual knowledge. Change an operator presentation limit mid-scene: the presentation changes immediately, without an NPC moral lecture, fabricated physics or punishment for the OOC request. World cruelty does not infer PC authorship. Provider/product restrictions remain external. Repeat in an ordinary low-conflict social setting to expose overcorrection and moralized exception machinery.

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

Pass: the first copy portrays established consequences without taking over the PC; the second handles a genuinely off-contract declaration OOC through return to premise, prospective recalibration or ending. Neither invents impossible physics or irresistibly controlling orders. In-premise tactics stay with their agreed author, and merely inconvenient play is not declared off-contract. Depiction limits remain separate from NPC conduct and the world's morality.

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

## Reporting and stop line

Report automated structural results, observed host operations and scored GM behavior separately, including package identity, conditions, repetitions, outputs and limitations. Mark all unrun fixtures NOT RUN. Changes to candidate wording get a new experiment identity; preserve historical artifacts without overwriting their original results. Passing this suite's structural runner does not run any B/M fixture or establish product-wide GM success.
