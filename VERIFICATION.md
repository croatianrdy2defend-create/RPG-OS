# v0.7.3 verification — 2026-09-06

This report distinguishes observed checks on the isolated public release candidate from proposed playtests. The kit remains experimental. Historical [v0.7.2 trials](V0.7.2_TRIALS.md) retain their original scope; they are not new v0.7.3 or cross-provider handover results.

| Check | Observed result |
|---|---|
| Structural validator on the unbound candidate | PASS; zero findings, stable tree, matching executed/target validator bytes |
| Structural regression suite | 46 tests passed on Python 3.11 / Windows |
| Handover regression suite | 35 tests run: 34 passed, one OS-symlink fixture skipped because the host disallows symlink creation; the separate simulated Windows reparse-point check passed |
| Packaging regression suite | 12 tests passed on Python 3.11 / Windows |
| Mechanics guide diagrams | All seven parsed and rendered with Mermaid 10.9.3 in headless Chrome and were visually inspected |
| Local documentation links and public inventory | 63 local links resolved; 70-file candidate; empty current/archive templates preserved; only Freeform and generic module contracts included |
| Live exchange between different external providers | NOT RUN |
| Human campaign enjoyment / sustained live play | NOT RUN |
| Long-campaign quality or semantic losslessness | NOT ESTABLISHED |

The main validator identifies itself as `VALIDATE-v3.0.2`. Its additions check required extension files and active handover marker presence. A bound marker produces a warning requiring the separate handover check; an unbound marker is an error. The structural validator does not certify package contents or authorize resumption.

The handover suite uses disposable synthetic files. It exercises export/return identities, sealed briefing and conversation hashes, changed/added/omitted snapshot files, unsafe routes, malformed manifests, coverage gaps, required headings, receipts, and repeated event identifiers. The checker is read-only: it does not execute an external GM or import campaign changes.

The packaging suite tests clean committed exports and checksums, tracked dirt, bound state, populated registers, extra modules and private paths, missing required files, Git export omissions, Git-index symlinks, and hostile ZIP paths/collisions. The release workflow runs all three suites again on Linux before publishing assets; its run logs are the authority for the hosted result.

## Reproduce the checks

```text
python -B TOOLS/validate.py --root .
python -B TOOLS/test_validate.py
python -B TOOLS/test_handover.py
python -B TOOLS/test_package_release.py
```

Run validation separately from operations modifying the measured tree. Tests use temporary synthetic fixtures; they make no model/API calls. On a clean committed public checkout, `python -B TOOLS/package_release.py` validates a frozen Git export and verifies every packaged file against its Git blob, ZIP CRCs, and the written SHA-256 checksum. See [Contributing](CONTRIBUTING.md) for publishing steps.

## What remains unproven

Hash and identity checks detect specified byte changes and lineage mismatches. They cannot prove that a conversation was complete, an NPC's motive was recorded faithfully, a player accepted a choice, or a return preserved every meaningful consequence. A manifest is not a cryptographic identity for its author.

Recovery remains a model-operated procedure with verified preimages, not an atomic filesystem guarantee. The handover marker is a protocol pause, not an operating-system lock. Hidden records are not encrypted. The ordinary startup packet still does not pin every referenced revision; only an active handover's specified snapshot is frozen.

Use [ADMIN/TESTS](ADMIN/TESTS.md) and [the short playtest](SHARE.md) for observed agency, pacing, retrieval, save, correction, and handover behavior. A passing structural suite does not establish these outcomes. No claim of universal model-host compatibility or a fully lossless transfer is made.
