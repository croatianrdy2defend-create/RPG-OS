"""Read-only verification of this curated publication, not a semantic detector.
Run from any directory: python -B path/to/verify_published.py
Uses only the Python standard library. Does not modify campaign or evidence files.
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> dict:
    checked_files = 0
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        path = (ROOT / relative).resolve()
        require(path.is_relative_to(ROOT), f"Manifest path escapes publication: {relative}")
        require(path.is_file(), f"Missing published file: {relative}")
        require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
                f"Published file hash mismatch: {relative}")
        checked_files += 1

    transcript_sources = {}
    pairs = 0
    for number in range(1, 31):
        suffix = "md" if number <= 10 else "txt"
        path = ROOT / f"transcripts/session-{number:02}.{suffix}"
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        if number <= 10:
            player_count = len(re.findall(r"^\*\*Simulated player:\*\*", text, re.MULTILINE))
            gm_count = len(re.findall(r"^\*\*GM:\*\*", text, re.MULTILINE))
            expected = 10
        else:
            player_count = len(re.findall(r"^Simulated player:", text, re.MULTILINE))
            gm_count = len(re.findall(r"^GM:", text, re.MULTILINE))
            expected = 8
        require(player_count == gm_count == expected,
                f"Unexpected pair count in session {number}: {player_count}/{gm_count}")
        pairs += player_count
        transcript_sources[hashlib.sha256(raw).hexdigest()] = text

    reports = load_json("evidence/primary-audit-statuses.json")["reports"]
    statuses = collections.Counter(row["status"] for row in reports)
    require(len(reports) == 20, "Expected twenty primary reports")
    require(dict(statuses) == {"consistent": 14, "inconsistent": 5, "undetermined": 1},
            "Primary report status totals differ")
    dossier = load_json("evidence/semantic-cases.json")
    kinds = collections.Counter(row["kind"] for row in dossier["cases"])
    require(dict(kinds) == {"mutation": 20, "valid_control": 6, "scope_probe": 2},
            "Semantic case counts differ")
    transcript_citations_checked = 0
    other_source_citations_not_rechecked = 0
    for case in dossier["cases"]:
        for citation in case["citations"]:
            text = transcript_sources.get(citation["sha256"])
            if text is None:
                other_source_citations_not_rechecked += 1
                continue
            lines = text.splitlines(keepends=True)
            start, end = citation["start_line"], citation["end_line"]
            require(1 <= start <= end <= len(lines), f"Invalid citation range: {case['id']}")
            require("".join(lines[start - 1:end]) == citation["quote"],
                    f"Transcript quotation mismatch: {case['id']}")
            transcript_citations_checked += 1

    suites = load_json("evidence/regressions.json")
    discovered = sum(row["cases"] for row in suites)
    skipped = sum(row["skipped"] for row in suites)
    require(len(suites) == 9 and discovered == 277 and skipped == 4,
            "Recorded regression totals differ")
    require(all(row["exit_code"] == 0 for row in suites), "Recorded suite failure")
    verification = load_json("evidence/verification.json")
    require(verification["new_player_GM_pairs"] == 160 and pairs == 260,
            "Recorded pair totals differ")
    require(verification["later_primary_review_misses"] == 2,
            "Do not suppress the documented review misses")
    require(bool(verification["known_unrepaired_semantic_issue"]),
            "Do not suppress the known final-save issue")
    return {
        "kind": "Read-only publication integrity/count/quotation verification",
        "not_a_semantic_detector": True,
        "manifest_files_checked": checked_files,
        "published_sessions": 30,
        "recorded_pairs": pairs,
        "primary_report_statuses": dict(statuses),
        "semantic_case_kinds": dict(kinds),
        "transcript_citations_checked": transcript_citations_checked,
        "other_source_citations_requiring_full_archive": other_source_citations_not_rechecked,
        "recorded_regression_discovered": discovered,
        "recorded_regression_passed": discovered - skipped,
        "recorded_regression_skipped": skipped,
        "new_gameplay_or_semantic_review": False,
        "known_final_save_issue": verification["known_unrepaired_semantic_issue"],
    }


if __name__ == "__main__":
    try:
        print(json.dumps(main(), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Publication verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
