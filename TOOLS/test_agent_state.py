#!/usr/bin/env python3
"""Instruction-text and routing regressions for the universal behavioral basis.

No LLM calls, behavioral simulation, private-state inspection or campaign writes.
Passing these checks does not establish independent or enjoyable model behavior.
Run: python -B TOOLS/test_agent_state.py
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


def section(text: str, heading: str) -> str:
    """Require one exact level-two heading; never silently inspect another section."""
    pattern = rf"(?m)^## {re.escape(heading)}[ \t]*$"
    matches = list(re.finditer(pattern, text))
    if len(matches) != 1:
        raise AssertionError(f"Expected one section {heading!r}, found {len(matches)}")
    body = text[matches[0].end():]
    boundary = re.search(r"(?m)^## ", body)
    return body[:boundary.start()] if boundary else body


class AgentInstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.agent = read("OS/AGENT_STATE.md")
        cls.law = read("OS/LAW.md")
        cls.module = read("MODULES/_CONTRACT.md")
        cls.people = read("INSTANCE/PEOPLE/README.md")
        cls.engine = read("ENGINE/freeform.md")
        cls.cases = read("ADMIN/TEST_AGENT_STATE.md")

    def assert_phrases(self, text: str, *phrases: str) -> None:
        actual = normalized(text)
        for phrase in phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(normalized(phrase), actual)

    def test_independence_is_not_autonomy_or_human_deliberation(self) -> None:
        self.assert_phrases(section(self.agent, "Identify the actual decision"),
                            "Independence from the player's desired outcome is not individual autonomy",
                            "Some behavior needs no conscious deliberation",
                            "reserved control of a PC")

    def test_control_information_and_transition_are_distinct(self) -> None:
        self.assert_phrases(section(self.agent, "Nature and control"),
                            "Locate the decision owner and any local discretion",
                            "A shared objective does not imply shared knowledge",
                            "communication channels, scope and delays",
                            "supported transition rather than inventing freedom, paralysis or a new personality")

    def test_authority_distinguishes_hard_limits_and_tendencies(self) -> None:
        self.assert_phrases(section(self.agent, "Recover sufficient authority"),
                            "Existing individual facts outrank group tendencies",
                            "hard capability constraints remain binding",
                            "Appearance alone establishes neither a custom nor a capacity or incapacity")

    def test_inapplicable_is_not_an_unknown_or_zero(self) -> None:
        self.assert_phrases(section(self.agent, "Recover sufficient authority"),
                            "Not applicable is not unknown or a zero score awaiting improvement",
                            "an answer deliberately open until its trigger",
                            "An unread or broken route is not permission to regenerate")

    def test_generation_has_an_input_boundary(self) -> None:
        self.assert_phrases(section(self.agent, "Establish a minimal baseline on direct attention"),
                            "Prior causal history involving the PC is legitimate input",
                            "unverified interpretation", "an unperceived player wish",
                            "a proposed narrative role", "not evidence of private nature",
                            "separate those inputs from the admissible basis")

    def test_observations_do_not_reverse_establish_their_meaning(self) -> None:
        self.assert_phrases(section(self.agent, "Establish a minimal baseline on direct attention"),
                            "Preserve actual observed actions and speech as constraints",
                            "do not promote their perceived meaning into motive, disposition or capability",
                            "private state, outward presentation",
                            "Do not invent a PC interpretation",
                            "require every outward appearance to conceal a contrary motive")

    def test_basis_precedes_dependent_portrayal_without_attention_activation(self) -> None:
        self.assert_phrases(section(self.agent, "Establish a minimal baseline on direct attention"),
                            "before the first focused portrayal or resolution that depends on it",
                            "Player attention is not the fictional cause",
                            "An established order, relevant perception, due process or authorized initiative",
                            "never invent prior motives afterward")

    def test_late_deepening_cannot_backfill_prior_causes(self) -> None:
        deepening = section(self.agent, "Deepen prospectively, not retrospectively")
        self.assert_phrases(deepening,
                            "any private cause behind it that was not already established remains unresolved",
                            "accepted generation procedure whose admissible inputs do not include the player's interpretation",
                            "Do not choose either the player's interpretation or its opposite",
                            "leave the cause open",
                            "Do not rewrite that new state backward",
                            "A later self-report", "not independent proof of earlier establishment")
        self.assert_phrases(self.law,
                            "Later deepening is prospective by default",
                            "Do not use either the player's interpretation or its opposite as the hidden past",
                            "without rewriting that change backward")
        self.assert_phrases(self.engine,
                            "Late deepening is prospective by default",
                            "Do not select the player's interpretation or its opposite as hidden history")

    def test_state_stays_sparse_and_has_no_compulsory_psychology(self) -> None:
        self.assert_phrases(section(self.agent, "Nature and control"),
                            "reasoning prompts, not required fields",
                            "No duplicate control register, all-to-all relationship graph or cast-wide update")
        self.assert_phrases(section(self.agent, "Establish a minimal baseline on direct attention"),
                            "Background crowds need no individual preparation",
                            "Include supported opportunities and positive aims",
                            "a controlled organism needs no friendship inventory")

    def test_randomness_cannot_create_inapplicable_capacities(self) -> None:
        self.assert_phrases(section(self.agent, "Establish eligible gaps"),
                            "Fix admissible inputs, eligible scope, context, constraints and outcome meanings before drawing",
                            "obtain actual randomizer or player-supplied input",
                            "Randomness does not remove bias",
                            "unsupported capacity or an inapplicable relationship dimension",
                            "Never switch a table, reinterpret a result or reroll")

    def test_approval_and_cooperation_are_not_player_outcome_meters(self) -> None:
        self.assert_phrases(section(self.agent, "Portray and change"),
                            "A favorable evaluation by an entity need not produce a player-favorable consequence",
                            "Cooperation need not establish affection",
                            "Agency does not require refusal, agreement",
                            "there is no outcome quota")

    def test_change_is_scoped_and_not_retrospective_regeneration(self) -> None:
        self.assert_phrases(section(self.agent, "Portray and change"),
                            "changed orders", "Retain a short cause at the affected scope",
                            "without retroactively choosing what existed before the encounter",
                            "Repetition alone earns neither progress nor forced resistance")
        self.assert_phrases(section(self.agent, "Resolve operative opportunities"),
                            "Repeated queries or subdivisions create no extra draws",
                            "leave later time uncommitted")

    def test_retention_keeps_existing_owners_and_honest_limits(self) -> None:
        self.assert_phrases(section(self.agent, "Retain, save and transfer honestly"),
                            "Shared state has one authority",
                            "PLAY remains read-only",
                            "not an independently recoverable hidden commitment",
                            "not proof of independent generation",
                            "not internal reasoning",
                            "no automatic establishment checkpoint, background save or private scratch file",
                            "The receiving GM leaves source authorities frozen")

    def test_adoption_preserves_established_entities_and_history(self) -> None:
        self.assert_phrases(section(self.agent, "Retain, save and transfer honestly"),
                            "Adoption is preservation-first",
                            "do not regenerate existing individuals, controllers, relationships or history",
                            "ADMIN/CORRECT.md", "accepted prospective procedure",
                            "Relabeling a prior fact as an impression is not a silent repair")

    def test_core_module_and_current_owner_expose_the_same_boundary(self) -> None:
        self.assert_phrases(self.law, "entity-appropriate behavioral basis",
                            "Not applicable is not unknown or zero",
                            "Shared control does not grant shared knowledge",
                            "A roll cannot create an unsupported capacity")
        self.assert_phrases(self.module, "The module supplies entity-specific capacities",
                            "the OS supplies the procedure", "the ENGINE owns resolution",
                            "admissible inputs", "not required files, fields")
        self.assert_phrases(self.people, "not a human personality template",
                            "one selected NOW or other existing system authority",
                            "do not rerandomize an established entity",
                            "PLAY creates no files here")

    def test_behavioral_cases_are_present_and_explicitly_not_run(self) -> None:
        identifiers = re.findall(r"(?m)^### (U\d{2}) — ", self.cases)
        self.assertEqual(identifiers, [f"U{number:02d}" for number in range(1, 16)])
        self.assert_phrases(self.cases, "Behavioral status: **NOT RUN**",
                            "does not execute an LLM", "not internal reasoning",
                            "variation alone does not demonstrate bias",
                            "Late deepening cannot backfill an earlier hidden cause")
        self.assert_phrases(read("CONTRIBUTING.md"), "TOOLS/test_agent_state.py",
                            "ADMIN/TEST_AGENT_STATE.md")
        self.assert_phrases(read("README.md"), "ADMIN/TEST_AGENT_STATE.md",
                            "v0.9.1")
        self.assertEqual(read("VERSION").strip(), "0.9.1")
        self.assertTrue((ROOT / "V0.9.1_CHANGES.md").is_file())

    def test_procedure_and_fixtures_remain_cold(self) -> None:
        bootstrap = read("OS/BOOTSTRAP.md")
        self.assertNotIn("OS/AGENT_STATE.md", bootstrap)
        self.assertNotIn("TEST_AGENT_STATE.md", bootstrap)
        self.assert_phrases(self.agent, "Do not load it at every startup",
                            "No mandatory agent vector, draw, dossier, new state owner or writing permission")

    def test_section_reader_rejects_missing_or_duplicate_coverage(self) -> None:
        self.assertEqual(section("## A\nkept\n## B\nother\n", "A").strip(), "kept")
        for text in ("## B\nother\n", "## A\none\n## A\ntwo\n"):
            with self.subTest(text=text), self.assertRaises(AssertionError):
                section(text, "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
