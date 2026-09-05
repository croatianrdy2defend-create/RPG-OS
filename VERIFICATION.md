# v0.7 verification — 2026-09-05

This report records checks actually performed during the v0.7 build. It is separate from proposed playtests.

| Check | Observed result |
|---|---|
| Optional structural validator on the revised unbound kit | PASS; no findings; initial/final tree stable; executed and target validator bytes match |
| Synthetic structural regression suite | 32 tests passed |
| Local documentation links | No missing file targets found |
| Integration review | Corrected safety-flag duplication, preserved legacy T0 compatibility, nonexistent future current-record pointers, and recovery handling of disclosed historical gaps |
| Live campaign / fresh-chat GM behavior | NOT RUN |
| Cross-provider host compatibility | NOT RUN |
| Long-campaign quality or semantic losslessness | NOT ESTABLISHED |

The automated checks used Python 3.11.9 on Windows and original synthetic campaign fixtures. They made no model/API calls and did not bind the distributed kit. Test-created fixtures are isolated from campaign state. The validator is read-only; the test runner creates disposable fixtures. Run them sequentially when validating a parent folder that contains those fixtures.

The regression cases cover clean and contaminated kits, bound character/opening consistency, agreement identity, required readable sections, benign metadata, source routes and path escapes, private watch pointers, active recovery, optional notes, real limit entries, complete-save/checkpoint evidence boundaries, legacy T0 preservation, and read-only validator provenance.

## Scope of the simplification

The entry point, startup guide, and GM core together changed from 5458 to 1605 whitespace-separated words, about 70.6% fewer. This excludes campaign-specific agreement, current save, setting brief, active limits, and cold retrieval instructions. It is a reproducible text-size observation, not a measured token cost or proof of better play.

Detailed rules, world records, current character/person/system state, PC knowledge, corrections, and historical evidence retain separate authority. Lower startup instruction volume does not mean the campaign data was compressed into one summary.

## Remaining playtesting

Use ADMIN/TESTS.md to observe universal setup, natural continuation, player control, source fidelity, exact recall, private processes, interruption recovery, and ordinary corrections in actual commercial hosts. Score player experience separately from file correctness. No structural pass certifies faithful model-written saves, concealment of private files, successful execution of recovery instructions, or consistent behavior across models.
