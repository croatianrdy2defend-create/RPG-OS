# RPG OS v0.6.2 — public smoke test

RPG OS is a Markdown-based runtime designed to let an AI GM remember a solo campaign across disposable chats. This clean public kit contains no campaign world and ships only the Freeform engine.

For normal use, start with [QUICKSTART.md](QUICKSTART.md). This page is a short reproducible test.

## 1. Unbound boot

Attach only the project folder to a writable AI workspace. In a fresh chat paste:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start fiction.
```

**Pass:** it reports ready and unbound, opens only the named technical boot files, and produces no fiction.

Then say `Begin play`.

**Pass:** it refuses because no campaign is bound.

## 2. New Game

Say `NEW GAME`.

**Pass:** it remains in SETUP; asks safety before detailed drafting; treats campaign depth, PC profile depth, and mechanical-sheet depth as separate choices; and builds an explicit run Campaign Contract.

The Contract should distinguish:

- campaign promise and fit;
- structural direction;
- GM initiative;
- pressure density;
- time handling;
- development priorities;
- guidance visibility;
- any creative mandate, its scope, and eligible boundaries;
- REVIEW mode.

Sparse construction and a deferred full sheet remain legal. Detailed construction covers only selected domains. Every accepted bound module receives one compact Setting Brief describing the world's identity, what is ordinary there, and what deeper information exists cold. The starting situation gives the GM something playable without choosing the PC's first voluntary act. Nothing becomes canon before a complete manifest and explicit `ACCEPT`.

## 3. GM-first behavior

After ACCEPT, start a new chat, run the same boot, and begin play.

Use two short probes:

1. End an opening situation, then take an ordinary action such as going home.
2. Enter a location where a dramatic incident would fit but is not independently warranted.

**Pass:** the GM provides orientation, ordinary function, established world motion, or a clean chance to close/advance time. It does not become an empty command parser. It also does not plant a stranger, clue, threat, or quest merely to look active.

Then ask a generic perception question about an ordinary public scene without supplying the campaign's distinctive vocabulary.

**Pass:** the GM respects the Setting Brief's foundational public reality without requiring a keyword from the player, opening the full lore library, reciting the brief, or turning the distinctive feature into a mandatory showcase or incident. Exact or local detail is retrieved only if the current task genuinely needs it.

This is semantic, player-evaluated evidence—not something the structural validator can prove.

## 4. Persistence and review

Play a short slice, then say `END SESSION`.

**Pass:** CLOSE persists the current state and archive evidence first. Only after it succeeds, and only if `review_mode: bearing-only`, REVIEW may update `INSTANCE/BEARING.md`. The two results are reported separately.

Start another fresh chat and boot again.

**Pass:** the same save resumes with no invented interval. A current Bearing may help orientation but does not act as canon or a scene queue.

## 5. Optional structural check

Say `VALIDATE` or run:

```bash
python3 TOOLS/validate.py --root .
```

Record the actual output and exit status. A script result covers only declared structural checks. HOST OBSERVATION, SEMANTIC behavior, and player experience remain separate. A no-code fallback must label itself `MODEL-CHECKED`, state exact coverage, and cannot certify the complete tree.

## Report results

Use the GitHub test-report issue form described in [CONTRIBUTING.md](CONTRIBUTING.md). Name the exact release/commit and sanitize all campaign, account, safety, and copyrighted material.
