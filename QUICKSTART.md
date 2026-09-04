# RPG OS v0.6 quickstart

RPG OS lets an AI run a solo tabletop campaign while ordinary Markdown files preserve the campaign between disposable chats. The AI is still expected to act as a GM: it frames and portrays the world, judges consequences, and follows the developing campaign. The files support that work; they do not replace it.

This public kit contains no world and only the `freeform` engine.

Already have a **bound v0.5 campaign**? Do not run NEW GAME or overwrite its campaign folders. Make a byte-for-byte backup, save any accepted play with the old v0.5 runtime, selectively install the v0.6 program/templates, then use the complete migration boot prompt in [INSTALLATION.md](INSTALLATION.md#upgrading-a-bound-v05-campaign). The bare command by itself is not the boot procedure.

## 1. Prepare the folder

1. Extract the download.
2. Keep a backup outside the AI service.
3. Attach only the extracted `RPG_OS` folder to a writable AI project or workspace.
4. Start a fresh chat.

Your host must be able to read named files and persist edits. A model name or subscription tier does not prove either capability.

## 2. Boot the empty kit

Paste:

```text
Open only OS/AGENTS.md, OS/BOOTSTRAP.md, OS/LAW.md,
INSTANCE/CURRENT_SAVE.md, and INSTANCE/CAMPAIGN_CONTRACT.md.
Do not search or list the rest of the folder.
Confirm the runtime is ready. Do not start fiction.
```

The kit should report that it is ready and unbound. It must not invent a campaign.

Optional: run `VALIDATE`. It checks deterministic file structure only. It does not certify GM quality, agency, host persistence, privacy, or provider policy compliance.

## 3. Create a campaign

Say:

```text
NEW GAME
```

The setup interview asks about:

- rules engine;
- campaign premise, voice, safety, and unwanted patterns;
- the **Campaign Contract**: what kind of campaign you want and how proactive the GM may be;
- optional world complexity, character detail, and mechanical sheet depth;
- a playable starting situation.

Sparse worldbuilding and an incomplete character sheet are valid. Nothing becomes canon until the AI shows the proposed manifest and you say `ACCEPT`.

After ACCEPT succeeds, leave setup and start a **new chat**.

## 4. Begin play

Use the same five-file boot prompt, then say `Begin play`.

The runtime also loads only the required voice/safety material and may load a current optional Bearing when REVIEW is enabled and its bases match. A **Bearing** is a short, provisional note about what the campaign may be becoming. It is not canon, a plot queue, or permission to force an event.

You write your character's voluntary actions, speech, thoughts, feelings, attraction, consent, and commitments. The GM runs the world.

## 5. Save and end sessions

- `CHECKPOINT` — saves the current present. It does not archive exact scene evidence.
- `CLOSE` — saves the present and writes indexed historical evidence.
- `REVIEW` — after a successful save, considers campaign patterns and may update the noncanonical Bearing. It cannot change canon.
- `END SESSION` — runs CLOSE first; only if CLOSE succeeds, runs REVIEW when the Campaign Contract enables it.

Do not discard a chat containing accepted play until CHECKPOINT or CLOSE prints the new `save_id`. Unsaved chat cannot be recovered by RPG OS.

Next session: new chat, same folder, same five-file boot. Do not paste the old transcript.

## Important limits

- Enforcement is instructions interpreted by one model context, not hard-coded game logic.
- File writes are not guaranteed to be atomic across several files. If an ADMIN write is interrupted, inspect or restore the folder before continuing.
- Some hosts inject whole files even when one section was requested. Physical sharding reduces exposure but does not prove isolation.
- Cloud providers may refuse content or restrict accounts under their policies. Keep your own local backup.
- v0.6 is a testing release, not proof of a 100-session campaign.

Full installation and capability checks: [INSTALLATION.md](INSTALLATION.md)  
Commands: [COMMANDS.md](COMMANDS.md)  
How the design works: [ARCHITECTURE.md](ARCHITECTURE.md)
