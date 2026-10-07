"""Focused taxonomy and navigation generation tests for Migration Step 4."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import load_resources, load_site, load_taxonomy, taxonomy_indexes  # noqa: E402
from shadow_catalog import published_resources, topic_records  # noqa: E402


class Step4TaxonomyNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (REPOSITORY_ROOT / "directory.js").read_text(encoding="utf-8")
        cls.communication = (REPOSITORY_ROOT / "communication.html").read_text(encoding="utf-8")
        cls.styles = (REPOSITORY_ROOT / "style.css").read_text(encoding="utf-8")
        cls.nav_source = (REPOSITORY_ROOT / "nav.js").read_text(encoding="utf-8")
        cls.site = load_site()
        cls.taxonomy = load_taxonomy()
        cls.indexes = taxonomy_indexes(cls.taxonomy)
        cls.resources = published_resources(load_resources())
        match = re.search(
            r"const worksheetDirectoryTaxonomy=Object\.freeze\((\{.*\})\);",
            cls.source,
        )
        if not match:
            raise AssertionError("Generated worksheetDirectoryTaxonomy was not found")
        cls.generated = json.loads(match.group(1))
        navigation_match = re.search(
            r"const worksheetDirectoryNavigation=Object\.freeze\((\{.*\})\);",
            cls.source,
        )
        if not navigation_match:
            raise AssertionError("Generated worksheetDirectoryNavigation was not found")
        cls.navigation = json.loads(navigation_match.group(1))

    def test_all_grades_subjects_and_planned_topics_match_taxonomy_order(self):
        grades = sorted(self.taxonomy["grades"], key=lambda item: item["order"])
        subjects = sorted(self.taxonomy["subjects"], key=lambda item: item["order"])
        keys = self.site["compatibility"]["directory"]["subjectLegacyKeys"]
        self.assertEqual(list(self.generated["grades"]), [item["id"] for item in grades])
        self.assertEqual(list(self.generated["subjectNames"]), [keys[item["id"]] for item in subjects])
        for subject in subjects:
            for grade in grades:
                expected = [
                    topic["label"]
                    for topic in sorted(self.taxonomy["topics"], key=lambda item: item["order"])
                    if topic["grade"] == grade["id"] and topic["subject"] == subject["id"]
                ]
                actual = self.generated["topics"][keys[subject["id"]]][grade["id"]].split("|")
                self.assertEqual(actual, expected)
        self.assertEqual(len(self.taxonomy["topics"]), 145)

    def test_all_five_subjects_are_present_for_every_grade(self):
        self.assertEqual(len(self.generated["subjectNames"]), 5)
        for grade_id in self.generated["grades"]:
            self.assertEqual(
                {subject for subject, grades in self.generated["topics"].items() if grade_id in grades},
                set(self.generated["subjectNames"]),
            )
        self.assertIn("Object.keys(subjectNames).map", self.source)

    def test_populated_empty_singleton_and_multi_resource_topics(self):
        records = topic_records(self.resources, self.taxonomy, self.indexes, self.site)
        populated = [record for record in records if record["resourceCount"]]
        empty = [record for record in records if not record["resourceCount"]]
        singletons = [record for record in records if record["resourceCount"] == 1]
        multi = [record for record in records if record["resourceCount"] >= 2]
        self.assertTrue(populated)
        self.assertTrue(empty)
        self.assertEqual(len(singletons), 23)
        early_writing = next(
            record for record in records
            if record["grade"] == "Preschool"
            and record["subject"] == "Reading & Language"
            and record["topic"] == "Early Writing"
        )
        self.assertEqual(
            early_writing["linkHref"],
            "resources/pre-writing-lines-strokes/",
        )
        conversation = next(
            record for record in records
            if record["grade"] == "Preschool"
            and record["subject"] == "Communication & Life Skills"
            and record["topic"] == "Conversation & Play"
        )
        self.assertEqual(
            conversation["linkHref"],
            "resources/phrases-i-can-use/",
        )
        self.assertTrue(multi)
        self.assertIn("Resources coming soon", self.source)
        self.assertIn("resources.length===1?resources[0].previewHref", self.source)

    def test_special_routes_are_generated_from_compatibility_config(self):
        self.assertEqual(
            self.generated["topicRouteOverrides"]["preschool|math|Numbers & Counting"],
            "numbers-counting.html",
        )
        self.assertEqual(
            self.generated["topicRouteOverrides"]["preschool|math|Early Addition & Subtraction"],
            "skill-directory.html?skill=addition",
        )
        self.assertIn("worksheetDirectoryTaxonomy.topicRouteOverrides", self.source)
        self.assertNotIn('topic==="Numbers & Counting"?', self.source)

    def test_skills_and_directory_file_routes_match_authoritative_data(self):
        self.assertEqual(self.generated["skills"], sorted(self.taxonomy["skills"], key=lambda item: (
            next(grade["order"] for grade in self.taxonomy["grades"] if grade["id"] == item["grade"]),
            next(subject["order"] for subject in self.taxonomy["subjects"] if subject["id"] == item["subject"]),
            next(topic["order"] for topic in self.taxonomy["topics"] if topic["grade"] == item["grade"] and topic["subject"] == item["subject"] and topic["id"] == item["topic"]),
            item["order"],
        )))
        directory = self.site["compatibility"]["directory"]
        self.assertEqual(self.generated["gradeFiles"], {path: key for key, path in directory["gradePaths"].items()})
        self.assertEqual(
            self.generated["subjectFiles"],
            {path: directory["subjectLegacyKeys"][key] for key, path in directory["subjectPaths"].items()},
        )

    def test_communication_custom_landing_is_preserved(self):
        self.assertIn("data-preserve-directory-content", self.communication)
        self.assertIn("data-taxonomy-topic-cards", self.communication)
        self.assertIn('communicationDirectoryScript.src = "directory.js?" + "v=30";', self.communication)
        self.assertIn("!library.hasAttribute(\"data-preserve-directory-content\")", self.source)
        self.assertIn("const reconcileTaxonomyTopicCards=()=>{", self.source)
        self.assertIn('data[subject][grade].split("|").forEach', self.source)
        self.assertIn('resources.length===1', self.source)
        topics = [
            topic["label"]
            for topic in sorted(self.taxonomy["topics"], key=lambda item: item["order"])
            if topic["grade"] == "preschool"
            and topic["subject"] == "communication-life-skills"
        ]
        self.assertEqual(topics, [
            "Understanding Language",
            "Expressing Needs & Ideas",
            "WH Questions",
            "Conversation & Play",
            "Feelings & Social Understanding",
            "Visual Supports & Routines",
            "Independence & Safety",
        ])
        communication_resources = [
            resource for resource in self.resources
            if resource["taxonomy"]["grade"] == "preschool"
            and resource["taxonomy"]["subject"] == "communication-life-skills"
        ]
        by_topic = {
            topic: [
                resource for resource in communication_resources
                if resource["taxonomy"]["topic"] == topic
            ]
            for topic in ("conversation-and-play", "visual-supports-and-routines")
        }
        self.assertEqual([resource["id"] for resource in by_topic["conversation-and-play"]], [
            "phrases-i-can-use",
        ])
        self.assertEqual({resource["id"] for resource in by_topic["visual-supports-and-routines"]}, {
            "my-self-care-routines",
            "my-everyday-routines",
        })

    def test_communication_topic_cards_keep_responsive_grid_behavior(self):
        self.assertIn(".library .card-container { grid-template-columns:repeat(3,1fr); }", self.styles)
        self.assertRegex(
            self.styles,
            r"(?s)@media \(max-width:900px\).*?\.library \.card-container \{ grid-template-columns:repeat\(2,1fr\); \}",
        )
        self.assertRegex(
            self.styles,
            r"(?s)@media \(max-width:600px\).*?\.library \.card-container \{ grid-template-columns:1fr; \}",
        )

    def test_primary_subject_and_grade_navigation_is_generated(self):
        match = re.search(r"const generatedPrimaryNavigation=(\"(?:\\.|[^\"])*\");", self.nav_source)
        self.assertIsNotNone(match)
        markup = json.loads(match.group(1))
        directory = self.site["compatibility"]["directory"]
        subject_positions = [markup.index(directory["subjectPaths"][item["id"]]) for item in sorted(self.taxonomy["subjects"], key=lambda item: item["order"])]
        grade_positions = [markup.index(directory["gradePaths"][item["id"]]) for item in sorted(self.taxonomy["grades"], key=lambda item: item["order"])]
        self.assertEqual(subject_positions, sorted(subject_positions))
        self.assertEqual(grade_positions, sorted(grade_positions))
        self.assertIn("links.innerHTML = generatedPrimaryNavigation;", self.nav_source)

    def test_manual_curriculum_matrix_and_route_ternary_are_removed(self):
        self.assertIn("const data=worksheetDirectoryTaxonomy.topics;", self.source)
        self.assertIn("const subjectNames=worksheetDirectoryTaxonomy.subjectNames;", self.source)
        self.assertIn("const grades=worksheetDirectoryTaxonomy.grades;", self.source)
        self.assertNotRegex(self.source, r"const data=\{\s*math:")
        self.assertNotRegex(self.source, r"const grades=\{preschool:")
        self.assertIn(
            "const numbersCountingSkills=worksheetDirectoryNavigation.numbersCountingSkills;",
            self.source,
        )
        self.assertIn(
            "const preschoolMathSkills=worksheetDirectoryNavigation.preschoolMathSkills;",
            self.source,
        )
        self.assertNotIn('...[' + '"trace-numbers-1-20"', self.source)

    def test_curated_math_navigation_copy_and_order_are_preserved(self):
        numbers = self.navigation["numbersCountingSkills"]
        self.assertEqual([card["title"] for card in numbers], [
            "Number Recognition", "Counting", "Number Order", "More, Fewer & Same",
            "Trace Numbers 1-20", "Missing Numbers 1-20", "Connect the Dots 1-20",
        ])
        self.assertEqual([card["title"] for card in self.navigation["preschoolMathSkills"][-4:]], [
            "Early Addition & Subtraction", "Patterns", "Measurement & Comparing", "Sorting & Data",
        ])
        self.assertEqual(self.navigation["preschoolMathSkills"][7]["href"], "skill-directory.html?skill=addition")

    def test_kindergarten_measurement_and_data_is_one_consolidated_topic(self):
        topics = [
            topic for topic in self.taxonomy["topics"]
            if topic["grade"] == "kindergarten" and topic["subject"] == "math"
        ]
        self.assertEqual([topic["label"] for topic in topics].count("Measurement & Data"), 1)
        self.assertNotIn("Measurement", [topic["label"] for topic in topics])
        skills = [
            skill for skill in self.taxonomy["skills"]
            if skill["grade"] == "kindergarten"
            and skill["subject"] == "math"
            and skill["topic"] == "sorting-and-data"
        ]
        self.assertEqual(
            [skill["label"] for skill in skills],
            ["Length & Height", "Weight", "Sorting & Data"],
        )

    def test_grade_directory_cards_use_natural_content_height(self):
        self.assertIn(".grade-directory { align-items:start; }", self.styles)


if __name__ == "__main__":
    unittest.main()
