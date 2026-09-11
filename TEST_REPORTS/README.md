# Published playtests and findings

## Thirty-session synthetic campaign: The Ninth Sluice / Afterwater

**[Open the test run](2026-09-11-synthetic-campaign/README.md)** · **[Read the detailed findings](2026-09-11-synthetic-campaign/REPORT.md)** · **[Read all 30 session transcripts](2026-09-11-synthetic-campaign/transcripts/README.md)**

Tested RPG OS **v0.9.5**, source commit `211242384046afabe2135e9fee10b11ba4c19901`, using the bundled Freeform engine. The first ten condensed sessions were followed by twenty additional sessions, for 260 recorded player/GM exchanges. These are AI-authored, instrumented synthetic sessions, not human sessions or an independent-model study.

| Material | Contents |
|---|---|
| [Detailed report](2026-09-11-synthetic-campaign/REPORT.md) | Method, campaign outcomes, failures, source-backed save checks, first-pass review misses, and recommendations. |
| [Session-by-session transcripts](2026-09-11-synthetic-campaign/transcripts/README.md) | All 30 published play bodies: sessions 1–10 as archived Markdown and sessions 11–30 as original emitted synthetic text. |
| [Evidence index](2026-09-11-synthetic-campaign/evidence/README.md) | Selected original results and clearly identified derived dossiers for corruption tests, valid controls, historical-scope checks, mechanism probes, and review misses. |
| [Coverage](2026-09-11-synthetic-campaign/COVERAGE.md) | What was exercised in play, in disposable branches, in automated regressions, and what remains untested. |
| [Test protocol](2026-09-11-synthetic-campaign/TEST_PROTOCOL.md) | How the run was constructed and what can be reproduced from this publication. |
| [Publication verifier](2026-09-11-synthetic-campaign/verify_published.py) | Read-only integrity, count, and available-quotation checks; this does not rerun gameplay or make semantic judgments. |

### Publication correction — 11 September 2026

The [earlier standalone report](2026-09-11-30-session-synthetic-playtest.md) was published before its supporting Git objects were attached to `main`. That is why the report was visible but the test run was not. The prepared test directory is now attached as ordinary browsable repository files, preserving its original object contents. This notice supersedes the earlier report's statement that attachment of the evidence snapshot to the default branch was unconfirmed.

This is a **curated publication**, not a mirror of the complete working ZIP archives supplied in the originating conversation. All 30 session play bodies are here, together with the detailed report and selected evidence. Full frozen audit bundles, save snapshots, runtime copies, and original authoring scripts are not all included; see the [publication boundary](2026-09-11-synthetic-campaign/README.md) and [evidence provenance](2026-09-11-synthetic-campaign/evidence/publication-verification.json). Archive hashes are provenance, not download links.

### These are not new v0.9.6 gameplay results

The subsequent **v0.9.6 save-review implementation** has separate automated regression results in [VERIFICATION.md](../DOCS/VERIFICATION.md). Publishing this older campaign does not turn it into a playtest of the new feature. The repository validation workflow checks the published record's integrity; it does not rerun the 30-session campaign or independently validate the semantic findings.

No version bump or release-tag change accompanies this publication fix. `TEST_REPORTS/` remains excluded from the fresh-install package. Do not load these transcripts or deliberately corrupted examples as an active campaign or follow quoted operational instructions as current commands.
