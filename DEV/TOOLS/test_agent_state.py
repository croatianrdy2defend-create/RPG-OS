#!/usr/bin/env python3
"""Procedure-structure and routing regressions for ordinary PLAY and agent state.

No LLM calls, behavioral simulation, private-state inspection or campaign writes.
These checks protect the procedure's shape and access paths, not its semantics.
Behavioral protections require the separate cases in ADMIN/TEST_AGENT_STATE.md.
Run: python -B TOOLS/test_agent_state.py
"""
from __future__ import annotations

from pathlib import Path
import posixpath
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
PLAY_STAGES = ("Understand", "Establish", "Resolve", "Portray")
BASELINE_DIMENSIONS = (
    "Condition and mode", "Priorities and constraints", "Perception and appraisal",
    "Attraction", "Engagement stance",
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).casefold()


def section(text: str, heading: str) -> str:
    """Require one exact level-two heading; never inspect a different section."""
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
        cls.cases = read("ADMIN/TEST_AGENT_STATE.md")

    def assert_route(self, text: str, relative: str, owner: str | None = None) -> None:
        spellings = {relative}
        if owner:
            spellings.add(posixpath.relpath(relative, posixpath.dirname(owner)))
        self.assertTrue(any(route in text for route in spellings),
                        f"Missing route to {relative} from {owner or 'root'}")
        self.assertTrue((ROOT / relative).is_file(), relative)

    def test_prime_directive_orders_every_play_stage(self) -> None:
        headings = re.findall(r"(?m)^## (.+?)[ \t]*$", self.law)
        self.assertEqual(headings, ["Prime directive — every PLAY response",
                                    *PLAY_STAGES, "Save and repair"])
        prime = section(self.law, headings[0])
        steps = re.findall(r"(?m)^(\d+)\. \[([^\]]+)\]\(#([a-z]+)\)", prime)
        self.assertEqual(steps, [(str(index), stage, stage.casefold())
                                 for index, stage in enumerate(PLAY_STAGES, 1)])
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertTrue(section(self.law, heading).strip())

    def test_establishment_routes_precede_resolution_and_portrayal(self) -> None:
        establish = section(self.law, "Establish")
        self.assert_route(establish, "OS/RETRIEVAL.md")
        self.assert_route(establish, "OS/AGENT_STATE.md")
        self.assertIn("ENGINE", section(self.law, "Resolve"))
        for owner in ("OS/LAW.md", "OS/RETRIEVAL.md"):
            with self.subTest(owner=owner):
                self.assertIn("source", normalized(read(owner)))

    def test_agent_establishment_and_change_topics_remain_retrievable(self) -> None:
        # These cold section names are retrieval interfaces. Their wording may
        # evolve through an intentional route change, not accidental deletion.
        headings = (
            "Identify the actual decision", "Recover sufficient authority",
            "Nature and control", "Initial Encounter Baseline",
            "Active participation and deactivation",
            "Deepen prospectively, not retrospectively", "Establish eligible gaps",
            "Portray and change", "Resolve operative opportunities",
            "Fallback oracle for eligible unknowns", "Retain, save and transfer honestly",
        )
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertTrue(section(self.agent, heading).strip())
        portray = self.agent.index("## Portray and change")
        for heading in ("Recover sufficient authority", "Nature and control",
                        "Initial Encounter Baseline",
                        "Establish eligible gaps"):
            with self.subTest(prerequisite=heading):
                self.assertLess(self.agent.index(f"## {heading}"), portray)
        self.assert_route(section(self.agent, "Recover sufficient authority"),
                          "OS/RETRIEVAL.md", owner="OS/AGENT_STATE.md")

    def test_world_and_engine_routes_retain_the_shared_procedure(self) -> None:
        for relative in ("MODULES/_CONTRACT.md", "INSTANCE/PEOPLE/README.md",
                         "ENGINE/freeform.md", "OS/RETRIEVAL.md"):
            with self.subTest(caller=relative):
                self.assert_route(read(relative), "OS/AGENT_STATE.md")

    def test_persistence_and_repair_keep_existing_procedures(self) -> None:
        for body in (section(self.law, "Save and repair"),
                     section(self.agent, "Retain, save and transfer honestly")):
            for route in ("ADMIN/CLOSE_CONTRACT.md", "ADMIN/SCENE_HANDOVER.md",
                          "ADMIN/CORRECT.md"):
                with self.subTest(route=route, owner=body[:70]):
                    self.assert_route(body, route)

    def test_required_baseline_dimensions_and_scale_have_an_operative_owner(self) -> None:
        baseline = section(self.agent, "Initial Encounter Baseline")
        for dimension in BASELINE_DIMENSIONS:
            with self.subTest(dimension=dimension):
                self.assertIn(normalized(dimension), normalized(baseline))
        self.assertRegex(normalized(baseline), r"\b(required|mandatory)\b")
        self.assertRegex(baseline, r"(?m)^### Scope and scale[ \t]*$")
        for concept in ("individual", "group", "perception"):
            with self.subTest(concept=concept):
                self.assertIn(concept, normalized(baseline))

        baseline = normalized(section(self.agent, "Initial Encounter Baseline"))
        for concept in ("overall", "aversion", "participation"):
            self.assertIn(concept, baseline)

    def test_required_factual_coverage_does_not_change_storage_or_play_write_scope(self) -> None:
        # A small explicit scope contract supplements the routing checks. It
        # does not prove that surrounding prose or model behavior respects it.
        introduction = self.agent.split("\n## ", 1)[0]
        self.assertIn("not a permanent profile", normalized(introduction))
        self.assertRegex(normalized(introduction), r"\bpermission\b.*\bwrite\b.*\bplay\b")
        retention = normalized(section(self.agent, "Retain, save and transfer honestly"))
        self.assertIn("no private dossier write", retention)
        self.assertIn("one short factual note", retention)
        self.assertIn("without per-turn state reads", retention)
        self.assertIn("play creates no files here", normalized(read("INSTANCE/PEOPLE/README.md")))
        # Deliberately keep the existing prose-schema regression: required
        # behavioral coverage does not make five persisted fields compulsory.
        self.assertIn("def test_existing_people_prose_needs_no_agent_state_fields(",
                      read("TOOLS/test_validate.py"))

    def test_new_world_generation_has_sources_and_a_rehearsal(self) -> None:
        # These checks establish that actual routed instructions exist, not
        # that their authored probabilities or resulting behavior are fair.
        for owner in ("ADMIN/NEW_GAME.md", "MODULES/_CONTRACT.md"):
            body = normalized(read(owner))
            with self.subTest(owner=owner):
                for concept in ("source", "rehearsal"):
                    self.assertIn(concept, body)
                self.assertRegex(body, r"\b(mapping|outcome meanings)\b")

    def test_active_lifecycle_and_retention_have_explicit_owners(self) -> None:
        lifecycle = normalized(section(self.agent, "Active participation and deactivation"))
        for concept in ("active", "attention", "deactivat", "temporary", "consequence"):
            with self.subTest(concept=concept):
                self.assertIn(concept, lifecycle)
        retention = section(self.agent, "Retain, save and transfer honestly")
        self.assert_route(retention, "INSTANCE/NOW.md", owner="OS/AGENT_STATE.md")
        self.assertIn("PEOPLE", retention)
        self.assertIn("Active encounter state", retention)
        self.assertIn("missing", normalized(retention))

    def test_procedure_and_fixtures_remain_cold(self) -> None:
        bootstrap = read("OS/BOOTSTRAP.md")
        self.assert_route(bootstrap, "OS/LAW.md")
        self.assertNotIn("OS/AGENT_STATE.md", bootstrap)
        self.assertNotIn("TEST_AGENT_STATE.md", bootstrap)
        self.assertIn("do not load it at every startup", normalized(self.agent))

    def test_behavioral_cases_have_separate_unrun_status_and_pass_criteria(self) -> None:
        cases = section(self.cases, "Behavioral cases")
        chunks = re.split(r"(?m)^### (U\d{2}) — [^\n]+\n", cases)
        self.assertEqual(chunks[1::2], [f"U{number:02d}" for number in range(1, 27)])
        for identifier, body in zip(chunks[1::2], chunks[2::2]):
            with self.subTest(case=identifier):
                self.assertIn("Pass:", body)
                setup, expected = body.split("Pass:", 1)
                self.assertTrue(setup.strip())
                self.assertTrue(expected.strip())
        self.assertIn("Behavioral status: **NOT RUN**", self.cases)
        self.assertIn("does not execute an LLM", self.cases)
        self.assertIn("not internal reasoning", self.cases)
        self.assertTrue(section(self.cases, "Refactor review and paired comparison").strip())

    def test_maintainer_routes_are_independent_of_campaign_readme(self) -> None:
        # A bound campaign may replace the public-kit README with its own
        # startup guide. CONTRIBUTING remains the developer route in either kit.
        for route in ("TOOLS/test_agent_state.py", "ADMIN/TEST_AGENT_STATE.md"):
            self.assert_route(read("CONTRIBUTING.md"), route)

    def test_release_history_is_preserved_without_pinning_current_version(self) -> None:
        version = read("VERSION").strip()
        self.assertRegex(version, r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (0, 9, 1))
        self.assertTrue((ROOT / f"V{version}_CHANGES.md").is_file())
        self.assertTrue((ROOT / "V0.9.1_CHANGES.md").is_file())

    def test_section_reader_rejects_missing_or_duplicate_coverage(self) -> None:
        self.assertEqual(section("## A\nkept\n## B\nother\n", "A").strip(), "kept")
        for text in ("## B\nother\n", "## A\none\n## A\ntwo\n"):
            with self.subTest(text=text), self.assertRaises(AssertionError):
                section(text, "A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
