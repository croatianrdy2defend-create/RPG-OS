# v8.1.1 experimental campaign play

This release is for ordinary human campaign play with optional feedback. Start or resume a real chosen campaign, make the decisions you want to make, save it normally, and judge whether its world remains coherent and enjoyable. No scripted behavioral pilot, rejection quota, scoring worksheet or special gameplay command is required. Structural/tool checks describe their own technical scope; they do not certify NPC independence or player enjoyment.

## Begin from a known build

Use one dedicated campaign folder. A new campaign follows NEW_GAME or LOAD; an existing v0.7.3 campaign follows `ADMIN/UPGRADE_V08.md` with its old complete backup preserved. Read the release's actual limitations: no automatic private-establishment checkpoint or new live-state store is supplied. Fixed setup records and completed requested saves can be reread; newly unrecorded hidden state has only best-effort conversational retention.

If feedback may be useful, note the installed version and available commit/package identity, actual model and reasoning setting when known, campaign's starting save id, and whether this is a new or upgraded campaign. Missing model/setting information stays unknown. These are optional observations, not new CURRENT_SAVE metadata or setup questions. Keep any notes outside campaign authority unless a separately requested provisional REVIEW belongs in BEARING.

## Play and switch naturally

Use the accepted agreement, ordinary PC declarations and the established world. Other agents may cooperate, refuse, initiate, change their minds or remain indifferent for actual reasons. Neither frequent success nor frequent refusal alone demonstrates independence. Helpful things to notice include whether relevant new information changes behavior, whether unrelated OOC hopes change NPC knowledge, whether a repeated unchanged request becomes an unexplained reroll, and whether maintenance interrupts ordinary conversation. There is no need to probe these deliberately or disclose GM-only facts to keep playing.

Before discarding a chat or switching models at a stopping point, request a full save and wait for verified success and honest evidence coverage. Open the saved campaign in the fresh chat; do not ask it to infer unsaved history. A checkpoint preserves the present without archiving new exact evidence, so it is not a substitute for a full save before losing source conversation.

To switch during an unresolved scene while keeping unsaved context, use `ADMIN/SCENE_HANDOVER.md`. Keep the source paused, continue only through the named receiving package, then return/import accepted changes once. Do not let two models write or continue the same campaign concurrently. Do not update program files while a handover snapshot is active. Model names or provider access do not change these rules.

## Optional incident notes

Record only a moment worth reporting, not every exchange. A short note can include:

- Build, model/reasoning setting if known, and the starting or most relevant completed save id.
- What the player actually declared, the relevant existing fact/rule or known uncertainty, and what response occurred.
- The specific concern or improvement: unsupported state change, missed justified change, OOC knowledge leak, lost continuity, repeated lookup, excess setup/maintenance, or an especially natural result.
- Available exact excerpt or saved source route, with missing wording labelled; any correction and its observed result.

Separate observation from interpretation. A summary is not an exact transcript; an unread private record does not prove the NPC had no reason. Keep real secrets out of public reports unless their disclosure is authorized. Do not export private model reasoning or publish campaign files merely because feedback is useful. Optional notes never create NPC motives, player preferences, historical events or new authoring permissions.

For unsupported silence or initiative, an optional note can identify the outcome/window, known facts, applicable procedure and any actual fallback input/result. Sparse NPC detail alone does not settle the outcome. Once requested or accepted, the standing fallback needs no per-roll permission; note whether it respected established facts, real causal reach and save/resume continuity. A later audit cannot supply an omitted roll or prove a past judgment. The optional [B15 diagnostic in TESTS](TESTS.md#b15--sparse-agent-outcomes-and-the-fallback-oracle) provides nine NOT RUN variants for investigation, not an extra campaign routine or behavioral certification.

For the temporary encounter baseline, an optional note can capture the first individual participation/appraisal, actual establishment evidence, response, an attention gap and genuine exit/return. Visual-only observation should retrieve applicable portrayal guidance without initializing an unaware actor. Check concrete priority effects, complete applicable attraction, reuse within participation, fresh incidental state only after authorized expiry, and surviving consequences at save/resume. Do not expose hidden facts or request private model reasoning; unavailable ordering evidence remains unverified. The optional [B16 diagnostic in TESTS](TESTS.md#b16--individual-baseline-before-a-direct-response) and [agent cases](TEST_AGENT_STATE.md) are separate tests, not play-time bookkeeping.

For a clear current error, use ordinary CORRECT; for a desired future approach, use RECALIBRATE. An explicit REVIEW can compare actual sources and describe provisional patterns without changing state. Preserve the unaffected campaign and requested fixes rather than restarting it to produce a cleaner report. Continue normal play whenever the current state is sound.
