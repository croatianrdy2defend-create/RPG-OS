# Contributing to RPG OS

RPG OS v0.6.2 is a public-testing release. The most valuable contribution is a small, reproducible result that distinguishes filesystem integrity from actual GM quality.

## Useful contributions

- a GM-first success or clerk/railroad failure with a sanitized transcript excerpt;
- fresh-chat resume and persistent-write observations;
- a narrow contract correction with its cross-file dependencies;
- structural validator defects or missing deterministic checks;
- archive needle and retrieval-locality results;
- fresh-chat Setting Brief results, especially generic-default drift or unnecessary lore loading;
- complex-campaign results involving clocks, phases, institutions, or private state;
- long-running campaign reports, including operator friction;
- plain-language documentation improvements.

## Keep evidence classes separate

| Evidence | What it can support | What it cannot prove |
|---|---|---|
| **STRUCTURAL** | Paths, formats, identities, references, deterministic invariants | Good GM judgment or host behavior |
| **HOST OBSERVATION** | What one named setup did at one observed time | Universal model/platform capability |
| **SEMANTIC** | Agency, warrant use, portrayal, archive meaning, or campaign coherence | Mechanically certified truth |
| **PLAYER-RATED** | Whether play felt alive, fair, coherent, and usable | Filesystem correctness |

Do not average a structural pass into a claim that the GMing was good.

Model-reported identity or AUDIT output is supporting evidence, not independent proof. Use operator-attested or host-exposed environment details when available and write `unknown` when they are not.

## Before reporting

1. Start from a clean release or name the exact commit.
2. State whether any runtime or campaign file was modified.
3. Name the relevant `P#`/fixture or command where possible.
4. Reduce the problem to the smallest sufficient files and steps.
5. State expected and actual behavior.
6. Include complete validator output and exit status for structural reports.
7. Sanitize the evidence.

Do not upload a whole private campaign merely to demonstrate one failure.

## Semantic reports

For GM behavior, include enough context to evaluate both opposing risks:

- **clerk:** the AI refuses to frame, portray, advance established causes, or answer a responsive task because nothing was prewritten;
- **railroad:** the AI treats setting fit, retrieval, preparation, or liveness as authority for an incident.

Useful reports explain the Campaign Contract settings, current causal frontier, player declaration, what the model retrieved, and why the result passed or failed. Do not expose private spoilers merely to make the report comprehensive.

## Before a pull request

Run from the repository root:

```bash
python3 TOOLS/validate.py --root .
```

Report the actual exit status and full diagnostics. Do not hard-code an old tree digest; it changes with tracked content.

Then check:

- the change begins in the file that owns the behavior, not only in README prose;
- GM Core, Campaign Contract, Setting Brief, Current Save, Bearing, ADMIN operations, schemas, tests, and public documentation still agree where affected;
- PERSIST and REVIEW authority remain separate;
- no preparation, fit, route, index, or Bearing accidentally becomes activation authority;
- no campaign world, bound save, private dossier, safety boundary, credential, account identifier, provider transcript, or personal data was added;
- no third-party rulebook text, tables, catalogues, artwork, or other unlicensed material was added;
- Markdown links resolve with exact filename case;
- any `OS/LAW.md` change identifies the cross-campaign runtime defect that requires a kernel edit and includes semantic tests for both clerk and railroad routes.

`ADMIN/TESTS.md` is the canonical test specification. `ARCHITECTURE.md` explains the design boundary. Public guides summarize; they do not override runtime contracts.

## Privacy, safety, and provider policy

Assume issues and pull requests remain public permanently. Remove real names, campaign prose, private safety settings, credentials, provider account information, spoilers, prohibited material, and anything that could expose a player.

Do not use the repository to test evasion or bypass provider safeguards.

## Contribution licensing

By intentionally submitting a contribution, you agree that its Markdown/protocol material may be distributed under CC BY 4.0 and its validator or repository-automation code under MIT, matching the repository's existing license notices.
