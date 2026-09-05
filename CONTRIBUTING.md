# Contributing to RPG OS v0.7.2

Useful contributions show a specific failure, its owning instruction or record, and a reproducible improvement. Keep public examples synthetic or sanitized.

## Evidence

Distinguish structural checks, observed host behavior, semantic judgments, and player ratings. A validator pass does not prove correct agency, pacing, meaningful memory, or enjoyable play. State the host/model only when actually known.

For a report, include the relevant accepted agreement, present situation, player request, necessary reference records, observed retrieval/write actions, and the expected versus actual result. Exact quotes matter when the defect concerns a promise, choice, or ambiguity. Do not publish an entire private campaign.

## Verification

Run the optional local checks:

```text
python TOOLS/validate.py --root .
python TOOLS/test_validate.py
```

The validator is read-only. Regression tests use temporary synthetic campaigns. Report actual output and limitations. Behavioral cases in ADMIN/TESTS.md require real play observation; do not mark them passed from reading the instructions.

Cross-check a change's owning contract, templates, loader, setup/save/recovery procedures, validator, tests, and documentation. Preserve legacy evidence and make format changes explicit. Avoid turning an optional world system into universal setup work.

Documentation/protocol contributions use CC BY 4.0; code/configuration use MIT. Do not include private campaigns, personal limits, account data, credentials, or unlicensed source material.
