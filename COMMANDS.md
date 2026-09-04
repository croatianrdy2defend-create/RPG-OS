# RPG OS command cheatsheet

This is a convenience summary for operators. `OS/BOOTSTRAP.md` and the referenced ADMIN contracts are authoritative if wording differs.

## Commands

| Input | Valid context | Result | Does not do | Authority |
|---|---|---|---|---|
| `NEW GAME` | A clean, unbound copy | Enters SETUP and builds a proposed engine/module/run manifest | Does not begin fiction or make drafts canon | `ADMIN/NEW_GAME.md` |
| `LOAD MODULE <id>` | A clean, unbound copy with that module installed | Validates and binds the existing module | Does not regenerate or merge the module | `ADMIN/LOAD.md` |
| `ACCEPT` | After SETUP displays the complete manifest | Authorizes exactly the disclosed write set and bind | Does not approve undisclosed additions | `ADMIN/NEW_GAME.md` |
| `Begin play` / `Continue` | A bound run | Establishes the saved immediate situation and hands control to the player | Does not choose the PC's first voluntary act | `OS/BOOTSTRAP.md` |
| `AUDIT` | After a non-AUDIT player turn | Reports paths/sections opened, reasons, and discovery commands used | Does not print file bodies or independently prove host isolation | `OS/BOOTSTRAP.md` |
| `VALIDATE` | Explicit OOC request | Runs a read-only structural diagnostic, preferably the shipped script | Does not certify semantics, host behavior, or future correctness | `ADMIN/VALIDATE.md` |
| `CHECKPOINT` | A bound run | Saves the compiled present and prints a new `save_id` | Does not archive exact scene wording | `ADMIN/CLOSE_CONTRACT.md` |
| `CLOSE` | A bound run | Saves the present plus indexed, scene-sharded historical evidence | Does not continue fiction afterward | `ADMIN/CLOSE_CONTRACT.md` |

There are no standard `SAVE`, `RESUME`, or `UNDO` aliases in v0.5. Use the canonical command whose contract matches the intended operation.

## First boot prompt

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start a scene.
```

An unbound kit must report ready and stop. `Begin play` must fail closed until a module is accepted or loaded.

## Fresh-session prompt

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md, and INSTANCE/CURRENT_SAVE.md.
Open the declared voice section only if fiction starts.
Begin at the saved immediate situation. Hand control back before my first voluntary act.
```

## The normal loop

1. Boot with the four-file prompt.
2. PLAY until a break or the end of the slice.
3. Use `CHECKPOINT` for a cheap present-state save, or `CLOSE` when exact evidence must also be archived.
4. Wait for the new `save_id`.
5. Start the next session in a fresh chat with the same folder.

Unsent UI suggestion chips are not commands or player input.

