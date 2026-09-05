# v0.7.1 verification — 2026-09-05

This report records checks actually performed during the v0.7.1 repair. It is separate from proposed playtests. The kit remains an experimental candidate pending observed campaign use.

| Check | Observed result |
|---|---|
| Optional structural validator on the revised unbound kit | PASS; no findings; initial/final tree stable; executed and target validator bytes match |
| Synthetic structural regression suite | 44 tests passed; all original 32 retained |
| Local documentation links | No missing file targets found |
| Integration review | Checked clause persistence and supplementation, selection/disclosure separation, cuts and retcon boundaries, recovery directory ownership, and candidate cleanup before marker removal |
| Live campaign / fresh-chat GM behavior | NOT RUN |
| Model-operated interruption recovery | NOT RUN; automated fixture simulations only |
| Cross-provider host compatibility | NOT RUN |
| Tellus migration | NOT RUN |
| Long-campaign quality or semantic losslessness | NOT ESTABLISHED |

The automated checks used Python 3.11.9 on Windows and original synthetic campaign fixtures. They made no model/API calls and did not bind the distributed kit. Test-created fixtures are isolated from campaign state. The validator is read-only; the test runner creates disposable fixtures. Run them sequentially when validating a parent folder that contains those fixtures.

The new regressions check the five required prose clauses for presence, section, uniqueness, and substantive content; both previously malformed provenance failure branches; and interrupted-save directory cleanup. The recovery simulation demonstrates that restoring file bytes alone leaves an orphan finding, then verifies that removing recorded, operation-created empty directories restores structural validity. It also tests preservation of pre-existing/nonempty directories and rejection of unsafe or protected paths. This is evidence about the procedure's fixture logic, not proof that a commercial LLM will execute it correctly.

The retained cases cover clean and contaminated kits, character/opening consistency, agreement identity, source routes and path escapes, private watch pointers, active recovery, optional notes, real limit entries, complete-save/checkpoint evidence boundaries, legacy T0 preservation, and read-only validator provenance. Clause checks do not certify informed acceptance or semantic conformity.

## Scope of the simplification

The entry point, startup guide, and GM core total 2,105 whitespace-separated words in v0.7.1, compared with 5,458 in v0.6.3: about 61.4% fewer. The original v0.7 total was 1,605 words; these repairs add explicit operating boundaries. Counts exclude campaign-specific agreement, current save, setting brief, active limits, and cold retrieval instructions. This is a reproducible text-size observation, not a measured token cost or proof of better play.

Detailed rules, world records, current character/person/system state, PC knowledge, corrections, and historical evidence retain separate authority. The startup packet is not an immutable revision-bound capsule: arbitrary engine, module, agreement, or mutable-record version swaps generally cannot be detected.

## Remaining playtesting

Use ADMIN/TESTS.md to observe universal setup, natural continuation, player control, source fidelity, exact recall, private processes, interruption recovery, and ordinary corrections in actual commercial hosts. New proposed fixtures specifically cover structural opacity, ironman/error correction, permitted and denied hard cuts, and off-premise handling. Score player experience separately from file correctness. No structural pass certifies faithful model-written saves, concealment of private files, successful execution of recovery instructions, or consistent behavior across models.
