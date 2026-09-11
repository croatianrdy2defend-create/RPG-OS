# Contributing to RPG OS v0.9.6

> **Repository-layout update:** current commands and packaging instructions are in [DEV/README.md](../DEV/README.md). The flat paths in the retained discussion below describe campaign workspaces and the historical developer layout; explanatory documents and regression files are no longer shipped in the player download.

Useful contributions show a specific failure, its owning instruction or record, and a reproducible improvement. For a four-stage failure, identify the missing source, establishment or resolution dependency before proposing another outcome-specific rule. Keep public examples synthetic or sanitized.

## Evidence

Distinguish structural checks, observed host behavior, semantic judgments, and player ratings. A validator pass does not prove correct agency, pacing, meaningful memory, or enjoyable play. State the host/model only when actually known.

For a report, include the relevant accepted agreement, present situation, player request, necessary reference records, observed retrieval/write actions, and the expected versus actual result. Exact quotes matter when the defect concerns a promise, choice, or ambiguity. Do not publish an entire private campaign.

For the current experimental release, ordinary campaign play is the primary evaluation of practical quality. A brief incident note is useful; players need not complete scripted trials or interrupt every scene with checks. When known, preserve the model, reasoning setting, build and starting save alongside the relevant conversation. Keep this operational context outside fictional state. See [Real-campaign playtesting](ADMIN/PLAYTEST_V08.md).

When diagnosing an agent-state failure, distinguish portrayal of a retained fact, initialization of a new fact, prospective change, late deepening, and loss or omission during retention. Check both unsupported accommodation and artificial resistance, and whether actual evidence can change the appropriate belief or relationship. An unexplained earlier presentation should not acquire a new hidden past cause merely because the player interpreted it, nor should the opposite interpretation be selected to demonstrate independence. A saved biased result is still biased; intact file bytes alone do not establish fair GMing. Optional paired replays from a separate saved copy can isolate a reported failure without rewinding the live campaign.

The [universal behavioral-basis cases](ADMIN/TEST_AGENT_STATE.md) add perception-versus-private-state, nonhuman drives, shared control, information boundaries, inapplicable dimensions, adoption, sparse-state and prospective-deepening controls. They remain NOT RUN until their exact fixtures are observed. Text-presence checks do not validate semantics or hidden independence. Keep factual basis and available generation provenance separate from internal reasoning, which is neither required evidence nor a durable record.

The [announced-autosave cases](ADMIN/TEST_AUTOSAVE.md) separately cover permission, notice timing, overrides, context-source limits, recovery/handover, evidence boundaries and save-before-switch behavior. Scheduler unit tests and synthetic metadata fixtures are not observed model-operated saves. Do not infer host context transfer, hidden-state completeness or background execution from a passing helper.

## Verification

Run the optional local checks:

```text
python TOOLS/validate.py --root .
python TOOLS/test_validate.py
python TOOLS/test_handover.py
python TOOLS/test_package_release.py
python TOOLS/test_read_source.py
python TOOLS/test_search_index.py
python TOOLS/test_evidence.py
python TOOLS/test_save_audit.py
python TOOLS/test_agent_state.py
python TOOLS/test_autosave.py
python TOOLS/test_encounter_generation.py
```

The validator is read-only. Regression tests use temporary synthetic campaigns where needed; the agent-state suite reads instruction text and routes without making model calls or campaign writes. The autosave suite checks a read-only scheduler, instruction routes and synthetic present/evidence metadata. The encounter-generation suite checks the optional helper's instructions, routes, input budget and documented direction table; it does not observe source retrieval or generated behavior during play. Run suites and whole-tree scans sequentially. Report actual output and limitations. Behavioral cases in ADMIN/TESTS.md, ADMIN/TEST_AGENT_STATE.md and ADMIN/TEST_AUTOSAVE.md require real play observation; do not mark them passed from reading the instructions.

Cross-check a change's owning contract, templates, loader, setup/save/recovery procedures, validator, tests, and documentation. Preserve legacy evidence and make format changes explicit. Avoid turning an optional world system into universal setup work.

Documentation/protocol contributions use CC BY 4.0; code/configuration use MIT. Do not include private campaigns, personal limits, account data, credentials, or unlicensed source material.

## Publish a fresh-install release

Maintainer packaging requires a Git checkout and Python 3.10 or newer. It is optional tooling, not a requirement for playing. A downloaded ZIP has no Git history and cannot run this packaging command on itself.

1. Work from the public unbound repository. Set `VERSION` and add matching `V<version>_CHANGES.md`; update current documentation and verification evidence.
2. Run all regression suites and review the public inventory. Keep Freeform as the only selectable engine, generic module contracts, and empty campaign registers. The optional generic helper at `ENGINE/_shared/ENCOUNTER_GENERATION.md` may ship as support selected by a bound engine and accepted agreement; it is not another selectable engine or a default random policy. Other setting or campaign engine content remains outside the public kit. Check documentation links and render changed Mermaid diagrams. A release branch may run the same checks in GitHub Actions when a local checkout is unavailable; report the actual execution location.
3. Commit the intended tree. Packaging rejects staged or unstaged tracked changes. Run `python -B TOOLS/package_release.py` to export and verify that commit.
4. Inspect `.release/RPG_OS_v<version>.zip` and `.release/SHA256SUMS`. Untracked files are excluded. `--output-dir` selects another destination; existing output is refused unless `--overwrite` is explicitly supplied.
5. Push the reviewed version change to `main`. The release workflow reruns checks and publishes the tag, ZIP, and checksum using the matching version notes. Manual dispatch also requires `main`.

Treat published version tags and assets as immutable. An existing complete release for the same commit is left unchanged; conflicting or incomplete releases fail for inspection. A different release commit needs a new version and corresponding notes. The workflow does not publish a live campaign or infer release permission from ordinary campaign work. Repository-only TEST_REPORTS stays on GitHub and is excluded from the fresh-install ZIP; every selected kit file still matches its committed blob, and other unexpected tracked campaign content is rejected.

The explicitly authorized v0.9.0 numbering correction is a single recorded exception: after verifying the corrected release's commit and published assets, its workflow retires only the mistaken v9.0.0 release/tag at commit `3d6ad58c920691929295fdc19ba185029a38dbbe`. It preserves commit history and refuses any changed target. This exception grants no general permission to replace other releases.

## Evidence-audit contributions

Seed omissions as well as incorrect values, retain unchanged controls, and repeat independent semantic runs. Include authorized OOC directives without acknowledgment, genuinely ambiguous suggestions, legitimate change, rewinds, testimony versus truth, missing source, a misleading index with conflicting source body, consequential numeric repairs and retired cues whose durable obligations remain. Score citation relevance separately from exact quotation. Record actual inspected sources, source gaps and reviewer identity. No fixture result establishes reliability over forty live sessions or across hosts.
