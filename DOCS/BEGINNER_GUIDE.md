# Your first RPG OS campaign

**A beginner's guide to downloading, setting up, playing, saving and returning.** No programming knowledge is required. [Back to the homepage](../README.md#start-your-first-campaign).

## What am I installing?

RPG OS is a collection of readable instructions and campaign files. An AI acts as the game master: you describe your character's choices, it portrays the world and resolves events, and it writes campaign records when you save. If selected during setup, a tiny write-only note also retains each exchange between saves. Those records let a later chat recover the saved situation and relevant history.

You install or open an **AI application** and give it the **RPG OS campaign folder**. RPG OS itself has no executable, account, server or installation command. You do not need to clone a Git repository or run the developer tests.

The public kit is a fresh start with the Freeform rules engine. It contains no prebuilt world, character or artwork. Setup helps you create them. Other rules and references can be added through setup; you do not need extra rulebooks for a first Freeform campaign.

## What you need

- A computer and a place to keep your campaign folder.
- An AI application with access to read, create and update files in that folder. This guide uses **Codex on desktop** as one concrete route. Other applications need equivalent file access; their exact setup differs.
- Access to a model through that application. RPG OS is free to download, but the AI service has its own plans, limits and charges. Check the access available in your account rather than assuming every model or feature is included.

For Codex, signing in with ChatGPT uses your account's Codex access; API-key sign-in is a separate usage-billed option. **This beginner route does not require an API key.** [Official sign-in explanation](https://learn.chatgpt.com/docs/auth).

## Ask your AI agent to help with installation

If you already have an AI agent, start by giving it the [RPG OS repository link](https://github.com/croatianrdy2defend-create/RPG-OS) and asking it to help. You can use an agent running Claude, GPT, or another capable model; the application determines which setup steps it can perform.

Paste this request into your agent:

```text
Help me install RPG OS and create my first campaign:
https://github.com/croatianrdy2defend-create/RPG-OS

Read the repository README and DOCS/BEGINNER_GUIDE.md, and follow their
current installation instructions. Help me make a separate campaign copy
of the GAME folder and give this chat access to read and save its files.
Handle the setup steps you can, and walk me through anything I must do
myself. Keep any existing campaign files intact.

Once the folder is ready, open its OS/AGENTS.md and help me start a new
campaign using Quick start. Check file access and tell me clearly if
you cannot save changes.
```

Tell it your operating system and which AI application you want to play in if it cannot determine them. It should read the repository's current instructions, identify the playable **GAME** folder, and help you put a separate campaign copy somewhere you can find again. It can then guide you through connecting that folder, checking access, and starting the new-game conversation.

An agent with suitable browser, file and terminal tools may be able to download, extract and prepare the folder for you. App installation, sign-in or granting folder access may still need your input. If it cannot perform a step, ask it for the exact action you need to take, then let it continue from there.

**The GitHub link starts the setup conversation; your own editable campaign folder holds your progress.** Ask the agent to show which folder it will use and confirm that it can read and save files there. Keep existing campaigns intact and use a fresh copy for a new game.

Once setup is complete, review and accept the campaign proposal as described in [Step 3](#step-3-start-setup), then begin play. You can also follow the manual steps below from the beginning, or use them whenever you need to do a step yourself.

## Step 1: Get the game files

1. **[Download the latest RPG OS files — ZIP](https://github.com/croatianrdy2defend-create/RPG-OS/archive/refs/heads/main.zip).** This includes the same-version v0.9.7 saving fixes. The older tagged game-only download remains the original build.
2. Extract the ZIP. Windows: right-click → **Extract All**. macOS: double-click. On other systems, use your file manager's extract function.
3. Open **RPG-OS-main**, then copy its **GAME** folder to a location you can find again, such as Documents. Rename that copy to your campaign's name.
4. Open your copied GAME folder until these folders appear together:

```text
Your campaign folder/       ← open THIS folder in the AI app
    OS/
        AGENTS.md          ← the AI's starting instructions
    ADMIN/
    INSTANCE/
    MODULES/
    ENGINE/
    ARCHIVE/
    README.md
    VERSION
    ...other included files
```

Keep all included files and folders together. The `.md` files are ordinary text documents; the extension stands for Markdown. You do not have to read or edit them to begin.

If you used GitHub's green **Code → Download ZIP**, you downloaded the entire development repository. Its **GAME** folder contains the playable kit. Copy that GAME folder for your campaign as described above. The documentation, tests and development tools are optional reading outside the game kit.

## Step 2: Give the AI access to your campaign

Install and open the desktop app using [OpenAI's official setup guide](https://learn.chatgpt.com/docs/quickstart). It includes an illustration of the product selector. Select **Codex** when that selector is present. Older desktop versions may be branded Codex; current documentation describes Codex inside the ChatGPT desktop app. [Windows installation and interface guide](https://learn.chatgpt.com/docs/windows/windows-app).

Sign in, then add the extracted campaign folder as a **local project**. In the current project interface, open the project menu → **Edit project → Add folder**. Make this folder primary if you attached several. Start a chat in that project. App labels can differ by version; the goal is that the chat can work on the actual folder on your computer. [Official project and folder guide](https://learn.chatgpt.com/docs/projects#use-local-projects-for-folders-and-codebases).

If an environment choice is shown, use **Local** to work in this folder. Keep this one folder as the active campaign. Let the app request the permissions needed to read and save its files. If access is refused or unavailable, resolve that before expecting a confirmed file save.

Choose a capable model available in your app. There is no mandatory RPG OS model, paid API or special reasoning setting. Models can differ in their ability to follow the procedures; report the model and setting when sharing playtest feedback. Begin with one GM chat; multiple agents are not needed for ordinary play.

## Step 3: Start setup

Paste this into the chat:

```text
Open OS/AGENTS.md in this campaign folder. Help me start a new RPG campaign.
Follow ADMIN/NEW_GAME.md, including Neutrality before worldbuilding and
Campaign spirit, and use Quick start. Ask only what you need next.
Check the available file access and tell me if you cannot save changes here.
```

This tells the AI where its operating instructions are and asks it to run the setup conversation. It should read the files, reuse any preferences you give it, and help you settle a playable proposal.

Tell it what kind of world you want, who you want to play, your preferred tone and boundaries, and what makes a game enjoyable for you. You can bring an existing character or ask for help making one. If you are unsure, say **“Give me a few options.”** If you have no rules preference, say **“Use the included Freeform rules.”** You can request Guided or Detailed setup if you want to spend more time on the choices.

An example exchange, purely to show how the conversation can work:

> **You:** I want exploration, relationships and practical problems. Help me choose a setting and character. Use Freeform.
>
> **GM:** Which part would you like to emphasize first? I can propose a few starting situations.
>
> **You:** Give me options. I want room to get to know people, and occasional adventures.

Your GM's actual questions and proposals will depend on your answers. These example preferences are not required campaign defaults.

The GM should summarize the proposed campaign and how it will run. Ask for changes until it fits, then clearly accept it. It should create the initial campaign files and confirm that it has saved and checked them. After that, say:

> Begin the campaign.

That starts actual play. Setup alone should not decide your character's first action.

## Step 4: Play in ordinary language

Write what your character says or attempts. You can use direct dialogue, describe an action, ask what you can see, or ask for information your character would reasonably know.

> I ask what happened and listen to the answer.
>
> I examine the damage before deciding what to do.
>
> I get ready and head to the appointment, aiming to arrive early.

The GM portrays the response and applies the selected rules. Outcomes follow those rules and the situation; you keep control of your character's choices. Ask for an explanation when a ruling is unclear. Dice and extra mechanics are used only where the selected method calls for them.

You can also speak out of character: **“OOC: slow down and let this conversation play out,” “Summarize the routine part,”** or **“That detail contradicts what happened earlier.”** You do not need special commands or to edit the records yourself.

At session start and end, the GM briefly reminds you about **SAVE**, **CHECKPOINT** (current records only), **END SESSION SAVE** and ordinary OOC requests. You can ask “What commands can I use?” at any time; the [command guide](../GAME/COMMANDS.md) lists the options.

## Step 5: Save and end a session

To save without ending play:

> Save the campaign.

To finish the session:

> END SESSION SAVE

“End the session, take my feedback, and save the campaign” means the same thing. The GM stops fiction and asks for feedback before saving. Tell it what worked, what felt awkward and what you want more or less of, or say “skip feedback”. It waits for your reply, explains and incorporates permitted adjustments for next time, then performs the applicable wrap-up and saves the current state and available history. You do not need to issue SAVE again. If you need it to save immediately without waiting for feedback, say so; unfinished feedback remains identified.

**Wait for the save confirmation before closing the chat.** It should identify the save and say what was actually written and verified, including any relevant limitation or unfinished step. “I will save” is a promise to act, not confirmation that it happened.

New campaigns default to a tiny write-only outcome note after each completed PLAY response and an announced CHECKPOINT every 20 completed PLAY replies. You can decline either during setup or disable/customize them later through recalibration. Checkpointing is not a background service. A checkpoint protects the current state but does not archive new exact dialogue. Use a full **Save** before leaving a chat or changing your GM/model/reasoning setting. [Save and switching details](../GAME/INSTALLATION.md#continuing-with-another-model).

## Step 6: Continue next time

Open the same updated folder in your AI application and start a fresh chat in its local project. Paste:

```text
Open OS/AGENTS.md and continue my saved campaign. Resume from the saved point.
```

The GM should read the saved situation and retrieve the relevant records. You should not need to rebuild the character or retell the whole campaign. If it starts proposing a new campaign, clarify that you want to continue the existing save and have it verify which folder it opened.

Keep only one active continuation of a campaign. Two GM chats changing the same files can produce conflicting progress.

After a confirmed save, make a backup by copying or zipping the **entire campaign folder** to a separate location. Keep the latest working folder easy to identify. Starting another campaign means extracting another clean kit into another folder; updates to an existing campaign use the [protected upgrade procedure](../GAME/ADMIN/UPGRADE_V08.md).

## Common problems

### I cannot find anything to run

Open your AI application and select the campaign folder. There is no RPG OS `.exe`. Paste the starting message from Step 3 into the AI chat.

### The AI says it cannot find OS/AGENTS.md

Check the folder shown in Step 1. You may have selected the Downloads folder, the still-compressed ZIP, or a parent folder. In the full repository download, select **GAME**. Ask the AI to show the folder it is using and whether `OS/AGENTS.md` exists there.

### It can read the files but cannot save them

Check the project's folder access and the app's permission message. A readable attachment is not necessarily an editable file. If the app cannot write the folder, use a suitable local-file application or the manual export route below. Keep the current chat and files until the save is actually installed and checked.

### Can I use another AI app or a browser chat?

Yes, if it provides the required file operations. The normal route needs named-file reading, file creation and updates, persistence between chats, and the ability to inspect the written result. Capability varies by application and account; RPG OS does not promise identical support in every chat interface.

If only attachments or text output are available, a **manual export** route is possible: supply the files the GM requests, have it produce complete replacements for every changed file and the history being retained, preserve the old versions, install all replacements yourself, and have the result checked. Provide those updated files next time. Until installation and checking finish, this is an export awaiting installation rather than a confirmed save. Follow [the complete manual workflow](../GAME/INSTALLATION.md#hosts-without-direct-workspace-writes).

### It is trying to build an app or explain the code

Say: **“Use the existing RPG OS files to GM a campaign for me. Follow OS/AGENTS.md and the new-game procedure; I am asking to play.”** Then give your campaign preferences.

### I only pasted the GitHub link

Ask the agent to help install it using the [agent-assisted setup prompt](#ask-your-ai-agent-to-help-with-installation). The link points to the public starting kit; it does not by itself give the AI a durable, editable copy of your campaign. The agent still needs to help you prepare and connect that folder, or guide you through the manual steps if its tools cannot do so.

### Something still does not work

Share your operating system, AI application, model/reasoning setting if known, the step you reached, and the exact error or unexpected response. A short relevant excerpt is more useful than “it broke.” Remove private information before posting. [Report an issue](https://github.com/croatianrdy2defend-create/RPG-OS/issues).

## Further reading

[In-game Quick start](../GAME/QUICKSTART.md) · [Installation and alternate workflows](../GAME/INSTALLATION.md) · [Everyday requests](../GAME/COMMANDS.md) · [Optional playtest guidance](ADMIN/PLAYTEST_V08.md)

This guide explains the existing v0.9.7 workflow. It does not change game rules, turn on optional policies or certify every AI host. Desktop labels and sign-in instructions were checked against the linked official OpenAI documentation on 12 September 2026. The beginner instructions still need feedback from first-time users.
