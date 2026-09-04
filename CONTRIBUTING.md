# Contributing to RPG OS

RPG OS v0.5 is a public-testing prototype. The most useful contributions are reproducible failures, cross-host observations, narrow contract corrections, validator fixes, and results from long-running campaigns.

## Before reporting

1. Start from a clean public release or identify the exact commit.
2. State whether `OS/LAW.md` was changed. LAW is frozen for v0.5.
3. Name the relevant `P#` test from `ADMIN/TESTS.md` when possible.
4. Separate the evidence class:
   - **STRUCTURAL** — deterministic filesystem/schema behavior;
   - **HOST OBSERVATION** — what one named host/model/tool configuration did at one time;
   - **SEMANTIC** — agency, salience, fidelity, shard coherence, or other judgment-bound behavior.
5. Reproduce the issue with the smallest sufficient files. Do not upload an entire private campaign when a sanitized fixture will do.

Use the GitHub test-report form and include environment, steps, expected behavior, actual behavior, and sanitized evidence. For structural failures, include the complete validator output and exit status.

## Before a pull request

Run from the repository root:

```bash
python3 TOOLS/validate.py --root .
```

Expected for the untouched public kit: exit status `0`, STRUCTURAL `PASS`, and `installed_engine_ids` containing `freeform`. The tree digest changes whenever tracked content changes; do not hard-code an old digest.

Then check:

- the change begins in the file that owns the rule, not only in README prose;
- cross-file references, tests, and validator assumptions still agree;
- no campaign world, live save, private dossier, safety boundary, credential, account identifier, or provider transcript was added;
- no third-party rulebook text, table, catalogue, artwork, or other material lacking redistribution permission was added;
- new Markdown links resolve with the repository's exact case;
- `OS/LAW.md` remains byte-identical unless the issue demonstrates a cross-module kernel hole and explicitly justifies reopening it.

`ADMIN/TESTS.md` is the canonical adversarial test specification. `ARCHITECTURE.md` owns the design boundary. Public-facing guides summarize the runtime contracts; they do not override them.

## Privacy and safety

Assume issue reports and pull requests are public forever. Redact campaign prose, real names, private safety settings, credentials, provider account details, and material that could expose a player. Do not use a public issue to test prohibited content or to bypass a provider's safeguards.

## Contribution licensing

By intentionally submitting a contribution, you agree that its Markdown/protocol material may be distributed under CC BY 4.0 and its validator or repository-automation code under MIT, matching the repository's existing license notices.

