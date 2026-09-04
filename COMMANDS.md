# RPG OS v0.6 command cheatsheet

These are player/operator commands, written out of character. The runtime and ADMIN contracts are authoritative if this summary ever differs.

## Everyday commands

| Command | When to use it | What it does | What it does not do |
|---|---|---|---|
| `NEW GAME` | Clean, unbound folder | Starts the setup interview and drafts a new module, run contract, PC baseline, and starting situation | Does not begin fiction or make a draft canon |
| `LOAD MODULE <id>` | Clean, unbound folder with that module installed | Validates and binds an existing module into a new run | Does not merge campaigns or overwrite a bound run |
| `MIGRATE V0.5` | Inside the complete migration boot prompt from `INSTALLATION.md`, against a backed-up bound v0.5 campaign copy after all accepted play was saved under v0.5 | Runs the one-time v0.5→v0.6 ADMIN conversion, with an accepted first Campaign Contract and explicit values for the four new Current Save fields | Does not work as a context-free bare command; merge folders; recover unsaved chat; reinterpret history; or migrate archives |
| `ACCEPT` | After SETUP shows the complete manifest | Authorizes exactly the disclosed files and settings | Does not approve unlisted additions |
| `Begin play` / `Continue` | Bound run | Orients the GM to the saved campaign and resumes fiction | Does not choose the PC's first voluntary act |
| `CHECKPOINT` | During or after PLAY | Persists the authoritative present and causal frontier; prints a new `save_id` | Does not archive exact scene evidence |
| `CLOSE` | End of a play slice | Persists the present, then writes indexed scene evidence | Does not interpret campaign direction |
| `REVIEW` | After a successful PERSIST | Reviews the saved campaign and may update the optional provisional Bearing | Does not change canon, clocks, history, the Contract, or Current Save |
| `END SESSION` | Normal session end | Runs CLOSE first; if it succeeds and `review_mode: bearing-only`, runs REVIEW second and reports them separately | REVIEW never runs after a failed CLOSE |
| `RECALIBRATE` | You want to change the campaign promise or GM style | Drafts prospective Campaign Contract changes and applies them only after explicit acceptance | Does not rewrite past play; a changed Contract makes old Bearing stale |

**PERSIST** is a design term, not an additional command. CHECKPOINT and CLOSE are the two PERSIST operations.

## Diagnostic commands

| Command | Result | Limitation |
|---|---|---|
| `AUDIT` | Reports the files/sections opened on the previous non-AUDIT player turn, why they were opened, and whether discovery commands ran | Model self-report, not independent proof |
| `VALIDATE` | Runs a read-only structural diagnostic, preferably `TOOLS/validate.py` | Does not test GM quality, semantic judgment, host writes, isolation, or future correctness |

## Boot prompt

Use this in every new chat:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start fiction.
```

For a bound game, say `Begin play` after boot. Required safety and voice material are loaded through the declared routes before fiction; a current optional `INSTANCE/BEARING.md` is loaded only when REVIEW is enabled and its bases match.

## Normal session

1. Boot.
2. Play.
3. Use CHECKPOINT when you need a safe stopping point.
4. Use END SESSION when you want present state, archive evidence, and—if enabled—a campaign review.
5. Wait for the new `save_id` and separate REVIEW result.
6. Start the next session in a fresh chat.

Unsent suggested-reply buttons are not commands or player input. There are no standard `SAVE`, `RESUME`, or `UNDO` aliases in v0.6.
