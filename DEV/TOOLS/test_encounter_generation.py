#!/usr/bin/env python3
"""Instruction and routing regressions for optional encounter generation.

These checks inspect the selected procedure's documented boundary, input budget,
and one direction table. They do not run an LLM, infer private reasoning, prove
source retrieval happened during play, or simulate behavior.
Run after installation: python -B TOOLS/test_encounter_generation.py
"""
from __future__ import annotations

import posixpath
import re
import unittest

from test_agent_state import BASELINE_DIMENSIONS, ROOT, normalized, read


HELPER = "ENGINE/_shared/ENCOUNTER_GENERATION.md"


def markdown_tables(text: str) -> list[list[list[str]]]:
    """Read contiguous Markdown table rows without treating prose as a table."""
    blocks = re.findall(r"(?m)(?:^\|[^\n]*\|[ \t]*(?:\n|$))+", text)
    return [[[cell.strip() for cell in line.strip().strip("|").split("|")]
             for line in block.splitlines()] for block in blocks]


class EncounterGenerationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.helper = read(HELPER)
        cls.body = normalized(cls.helper.replace("*", ""))

    def assert_route(self, text: str, target: str, owner: str = HELPER) -> None:
        spellings = {target, posixpath.relpath(target, posixpath.dirname(owner))}
        self.assertTrue(any(route in text for route in spellings),
                        f"Missing route from {owner} to {target}")
        self.assertTrue((ROOT / target).is_file(), target)

    def test_helper_is_optional_support_and_not_an_engine_identity(self) -> None:
        self.assertEqual(posixpath.dirname(HELPER), "ENGINE/_shared")
        self.assertNotEqual(posixpath.basename(HELPER), "ENGINE.md")
        self.assertNotRegex(self.helper, r"(?mi)^class:\s*engine\s*$")
        self.assertNotRegex(self.helper, r"(?mi)^id:\s*\S+")
        for concept in ("selected", "bound engine", "agreement"):
            self.assertIn(concept, self.body)
        self.assertIn("not a default random policy", self.body)
        self.assertIn("_shared", read("ENGINE/_CONTRACT.md"))

    def test_one_direction_table_covers_two_dice_totals_and_all_36_outcomes(self) -> None:
        tables = markdown_tables(self.helper)
        self.assertEqual(len(tables), 1,
                         "The helper owns one direction map, not a state catalogue")
        header, separator, *rows = tables[0]
        self.assertEqual(len(header), 2)
        self.assertRegex(normalized(header[0]), r"\b2d6\b")
        self.assertIn("direction", normalized(header[1]))
        self.assertEqual(len(separator), len(header))
        expected = [(2, 3, "strongly negative"), (4, 5, "negative"),
                    (6, 8, "neutral or mixed"), (9, 10, "positive"),
                    (11, 12, "strongly positive")]
        self.assertEqual(len(rows), len(expected))
        covered = []
        actual_bands = []
        for row, (start, end, direction) in zip(rows, expected):
            with self.subTest(row=row):
                self.assertEqual(len(row), len(header))
                match = re.fullmatch(r"(\d+)\s*[\u2013-]\s*(\d+)", row[0])
                self.assertIsNotNone(match, row[0])
                self.assertEqual((int(match[1]), int(match[2])), (start, end))
                label = normalized(row[1]).replace("neutral/mixed", "neutral or mixed")
                self.assertEqual(label, direction)
                covered.extend(range(start, end + 1))
                actual_bands.append((int(match[1]), int(match[2]), label))
        self.assertEqual(covered, list(range(2, 13)))

        # Enumerate the actual independent-face sample space, rather than
        # treating the eleven possible totals as equally likely. These counts
        # validate the documented map; they do not exercise an LLM or randomizer.
        counts = {direction: 0 for _, _, direction in actual_bands}
        for first in range(1, 7):
            for second in range(1, 7):
                matches = [direction for start, end, direction in actual_bands
                           if start <= first + second <= end]
                self.assertEqual(len(matches), 1, (first, second))
                counts[matches[0]] += 1
        self.assertEqual(counts, {"strongly negative": 3, "negative": 7,
                                  "neutral or mixed": 16, "positive": 7,
                                  "strongly positive": 3})
        self.assertEqual(sum(counts.values()), 36)

    def test_three_eligible_determinations_use_at_most_six_independent_faces(self) -> None:
        self.assertRegex(self.body, r"at most (?:three|3).{0,70}(?:determinations|2d6)")
        self.assertRegex(self.body, r"(?:two|2) independent (?:actual )?d6")
        self.assertRegex(self.body, r"(?:sum|add).{0,35}(?:pair|dice|faces)")
        self.assertRegex(self.body, r"(?:six|6).{0,25}faces")
        for concept in ("condition", "interpersonal", "attraction", "with replacement",
                        "player-supplied", "before", "eligible"):
            self.assertIn(concept, self.body)
        self.assertNotRegex(self.helper, r"(?mi)^\|\s*Modified total\s*\|")
        self.assertNotRegex(self.body, r"\b3d6\b")
        self.assertNotRegex(self.body, r"at most (?:three|3) independent d6")
        # Concrete priorities and the final engagement stance remain required,
        # but a direction of good/bad must not generate either automatically.
        self.assertRegex(self.body, r"priorit.{0,280}(?:no|not|without).{0,50}(?:roll|draw)")
        self.assertRegex(self.body, r"(?:derive|derived).{0,80}engagement|engagement.{0,80}(?:derive|derived)")

    def test_source_gates_and_concrete_state_precede_dependent_behavior(self) -> None:
        self.assert_route(self.helper, "OS/AGENT_STATE.md")
        for field in BASELINE_DIMENSIONS:
            self.assertIn(normalized(field), self.body)
        for concept in ("source", "control", "capacities", "perception", "concrete",
                        "before", "received", "unknown", "inapplicab"):
            self.assertIn(concept, self.body)
        self.assertRegex(self.body, r"(?:before|prior to).{0,150}(?:draw|input)")
        self.assertRegex(self.body, r"before.{0,100}(?:behavior|behaviour|response|conduct)")
        self.assertIn("nonsocial", self.body)
        self.assertRegex(self.body, r"unknown is not|unknown does not")

    def test_reusable_procedure_contains_no_campaign_binding_or_venue_table(self) -> None:
        self.assertNotRegex(self.helper, r"(?i)\b(?:Tellus|Elias|Anthari|Saurari|Munich|Südwacht|bartender|nightclub|doorman)\b")
        self.assertNotIn("MODULES/tellus/", self.helper)
        self.assertNotIn("Patron with current drink", self.helper)
        self.assertNotIn("Staff secondary priority", self.helper)
        self.assertNotRegex(self.helper, r"\b(?:Carousing 13|Sex Appeal 12|200-point)\b")

    def test_reuse_and_retention_do_not_install_reception_rolls_or_play_writes(self) -> None:
        for concept in ("active", "deactivation", "temporary", "consequen", "reception",
                        "willingness", "now", "person", "system", "write"):
            self.assertIn(concept, self.body)
        self.assertIn("active encounter state", self.body)
        self.assertRegex(self.body, r"no.{0,80}(?:ongoing|reception)|(?:ongoing|reception).{0,80}no")
        self.assertRegex(self.body, r"(?:no|not).{0,100}(?:scratch|per-turn|play write)")
        self.assertIn("host", self.body)


if __name__ == "__main__":
    unittest.main(verbosity=2)
