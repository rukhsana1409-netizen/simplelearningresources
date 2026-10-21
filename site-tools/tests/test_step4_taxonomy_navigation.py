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
        cls.math = (REPOSITORY_ROOT / "math.html").read_text(encoding="utf-8")
        cls.reading = (REPOSITORY_ROOT / "reading.html").read_text(encoding="utf-8")
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
                value = self.generated["topics"][keys[subject["id"]]].get(grade["id"], "")
                actual = value.split("|") if value else []
                self.assertEqual(actual, expected)
        self.assertEqual(len(self.taxonomy["topics"]), 145)

    def test_kindergarten_reading_topics_follow_literacy_progression(self):
        topics = [
            topic["label"]
            for topic in sorted(self.taxonomy["topics"], key=lambda item: item["order"])
            if topic["grade"] == "kindergarten"
            and topic["subject"] == "reading-language"
        ]
        self.assertEqual(topics, [
            "Alphabet & Print Concepts",
            "Phonological Awareness",
            "Phonics & Word Recognition",
            "Fluency",
            "Vocabulary & Oral Language",
            "Reading Comprehension",
            "Writing & Language",
        ])
        generated = self.generated["topics"]["reading"]["kindergarten"].split("|")
        self.assertEqual(generated, topics)
        self.assertNotIn("CVC Words", generated)
        self.assertNotIn("Story Elements", generated)

    def test_kindergarten_science_navigation_shows_only_populated_categories(self):
        self.assertEqual(
            self.navigation["topicVisibility"]["kindergarten|science"],
            ["Living Things", "Weather & Seasons", "Earth & Sky", "Materials & Motion"],
        )
        science_resources = {
            resource["id"]: resource
            for resource in self.resources
            if resource["taxonomy"]["grade"] == "kindergarten"
            and resource["taxonomy"]["subject"] == "science-discovery"
        }
        self.assertEqual(set(science_resources), {
            "living-things",
            "weather-watchers",
            "build-and-prepare",
            "earth-care",
            "pushes-and-pulls",
            "stop-or-turn",
        })
        resources_by_topic = {}
        for resource in science_resources.values():
            topic = self.indexes["topics"][(
                resource["taxonomy"]["grade"],
                resource["taxonomy"]["subject"],
                resource["taxonomy"]["topic"],
            )]["label"]
            resources_by_topic.setdefault(topic, []).append(resource["id"])
        self.assertEqual(resources_by_topic, {
            "Living Things": ["living-things"],
            "Earth & Sky": ["earth-care"],
            "Materials & Motion": ["pushes-and-pulls", "stop-or-turn"],
            "Weather & Seasons": ["weather-watchers", "build-and-prepare"],
        })

        kindergarten = (REPOSITORY_ROOT / "kindergarten.html").read_text(encoding="utf-8")
        science_section = re.search(r'<div id="science">(.*?)</div>', kindergarten).group(1)
        self.assertEqual(science_section.count("<li>"), 4)
        for visible in ("Living Things", "Weather &amp; Seasons", "Earth &amp; Sky", "Materials &amp; Motion"):
            self.assertIn(visible, science_section)
        for hidden in ("Plants", "Animals", "Human Body", "Scientific Thinking", "Resources coming soon"):
            self.assertNotIn(hidden, science_section)

        science = (REPOSITORY_ROOT / "science.html").read_text(encoding="utf-8")
        kindergarten_section = re.search(r'<div><h2>Kindergarten</h2>(.*?)</div>', science).group(1)
        self.assertEqual(kindergarten_section.count("<a "), 4)
        for visible in ("Living Things", "Weather &amp; Seasons", "Earth &amp; Sky", "Materials &amp; Motion"):
            self.assertIn(visible, kindergarten_section)
        for hidden in ("Plants", "Animals", "Human Body", "Scientific Thinking", "Resources coming soon"):
            self.assertNotIn(hidden, kindergarten_section)

    def test_kindergarten_reading_fallback_and_subject_metadata_are_current(self):
        kindergarten = (REPOSITORY_ROOT / "kindergarten.html").read_text(encoding="utf-8")
        for topic in (
            "Alphabet &amp; Print Concepts",
            "Phonological Awareness",
            "Phonics &amp; Word Recognition",
            "Fluency",
            "Vocabulary &amp; Oral Language",
            "Reading Comprehension",
            "Writing &amp; Language",
        ):
            self.assertIn(topic, kindergarten)
        self.assertEqual(kindergarten.count("Resources coming soon"), 5)
        self.assertIn(
            '<a href="resources/blending-segmenting/">Phonological Awareness</a>',
            kindergarten,
        )
        self.assertIn(
            '<a href="topic.html?grade=Kindergarten&amp;subject=Reading%20%26%20Language&amp;topic=Phonics%20%26%20Word%20Recognition">Phonics &amp; Word Recognition</a>',
            kindergarten,
        )
        self.assertNotIn("Phonological Awareness &amp; Phonics", kindergarten)
        self.assertIn(
            "<title>Reading & Language Resources by Grade | Learning Made Simple</title>",
            self.reading,
        )
        self.assertIn("Browse topics by grade.", self.reading)
        self.assertIn('class="directory-grid subject-directory"', self.reading)
        self.assertNotIn("Free Preschool Reading Worksheets", self.reading)
        self.assertIn(
            'subject==="reading"?"Reading & Language Resources by Grade | Learning Made Simple"',
            self.source,
        )

    def test_subject_visibility_keeps_thinking_preschool_only_and_social_studies_across_grades(self):
        self.assertEqual(len(self.generated["subjectNames"]), 6)
        self.assertEqual(
            self.generated["topics"]["socialStudies"],
            {"kindergarten": "Economics|Civics & Community|Maps & Places"},
        )
        visibility = self.navigation["subjectVisibility"]
        self.assertIn("thinking", visibility["preschool"])
        for grade in ("kindergarten", "grade-1", "grade-2"):
            self.assertNotIn("thinking", visibility[grade])
            self.assertIn("socialStudies", visibility[grade])
        self.assertIn("visibleSubjects(grade).map", self.source)
        self.assertIn("visibleGrades(subject).map", self.source)

    def test_kindergarten_social_studies_navigation_and_resources(self):
        resources = {
            resource["id"]: resource
            for resource in self.resources
            if resource["taxonomy"]["grade"] == "kindergarten"
            and resource["taxonomy"]["subject"] == "social-studies"
        }
        self.assertEqual(set(resources), {
            "needs-wants-working",
            "flag-rules",
            "working-it-out",
            "maps-globes",
        })
        self.assertEqual(
            resources["needs-wants-working"]["taxonomy"]["topic"],
            "economics-kindergarten",
        )
        self.assertEqual(
            resources["flag-rules"]["taxonomy"]["topic"],
            "civics-and-community",
        )
        self.assertEqual(
            resources["working-it-out"]["taxonomy"]["topic"],
            "civics-and-community",
        )
        self.assertEqual(resources["maps-globes"]["taxonomy"]["topic"], "maps-and-places")
        social_studies = (REPOSITORY_ROOT / "social-studies.html").read_text(encoding="utf-8")
        self.assertIn('href="resources/needs-wants-working/">Economics</a>', social_studies)
        self.assertIn(
            'href="topic.html?grade=Kindergarten&amp;subject=Social%20Studies&amp;topic=Civics%20%26%20Community">Civics &amp; Community</a>',
            social_studies,
        )
        self.assertIn('href="resources/maps-globes/">Maps &amp; Places</a>', social_studies)

    def test_populated_empty_singleton_and_multi_resource_topics(self):
        records = topic_records(self.resources, self.taxonomy, self.indexes, self.site)
        populated = [record for record in records if record["resourceCount"]]
        empty = [record for record in records if not record["resourceCount"]]
        singletons = [record for record in records if record["resourceCount"] == 1]
        multi = [record for record in records if record["resourceCount"] >= 2]
        self.assertTrue(populated)
        self.assertTrue(empty)
        self.assertEqual(len(singletons), 31)
        kindergarten_awareness = next(
            record for record in records
            if record["grade"] == "Kindergarten"
            and record["subject"] == "Reading & Language"
            and record["topic"] == "Phonological Awareness"
        )
        self.assertEqual(kindergarten_awareness["resourceCount"], 2)
        self.assertEqual(
            kindergarten_awareness["linkHref"],
            "topic.html?grade=Kindergarten&subject=Reading%20%26%20Language&topic=Phonological%20Awareness",
        )
        kindergarten_phonics = next(
            record for record in records
            if record["grade"] == "Kindergarten"
            and record["subject"] == "Reading & Language"
            and record["topic"] == "Phonics & Word Recognition"
        )
        self.assertEqual(kindergarten_phonics["resourceCount"], 3)
        self.assertEqual(
            kindergarten_phonics["linkHref"],
            "topic.html?grade=Kindergarten&subject=Reading%20%26%20Language&topic=Phonics%20%26%20Word%20Recognition",
        )
        kindergarten_print = next(
            record for record in records
            if record["grade"] == "Kindergarten"
            and record["subject"] == "Reading & Language"
            and record["topic"] == "Alphabet & Print Concepts"
        )
        self.assertEqual(kindergarten_print["resourceCount"], 1)
        self.assertEqual(
            kindergarten_print["linkHref"],
            "resources/understanding-print-sentences/",
        )
        kindergarten_fluency = next(
            record for record in records
            if record["grade"] == "Kindergarten"
            and record["subject"] == "Reading & Language"
            and record["topic"] == "Fluency"
        )
        self.assertEqual(kindergarten_fluency["resourceCount"], 1)
        self.assertEqual(
            kindergarten_fluency["linkHref"],
            "resources/emergent-decodable-reading/",
        )
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
        self.assertIn('communicationDirectoryScript.src = "directory.js?" + "v=41";', self.communication)
        self.assertIn("!library.hasAttribute(\"data-preserve-directory-content\")", self.source)
        self.assertIn("const reconcileTaxonomyTopicCards=()=>{", self.source)
        self.assertIn('visibleTopics(grade,subject).forEach', self.source)
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

    def test_primary_dropdowns_support_keyboard_focus(self):
        self.assertIn(".dropdown:focus-within .dropdown-menu", self.styles)
        self.assertIn('trigger.setAttribute("aria-haspopup", "true")', self.nav_source)
        self.assertIn('trigger.setAttribute("aria-expanded", "false")', self.nav_source)
        self.assertIn('dropdown.addEventListener("focusin"', self.nav_source)
        self.assertIn('dropdown.addEventListener("focusout"', self.nav_source)

    def test_math_uses_the_shared_subject_directory_renderer(self):
        self.assertNotIn('library.innerHTML=subject==="math"?', self.source)
        self.assertIn(
            'library.innerHTML=`<div class="library-header"><p class="eyebrow">RESOURCE DIRECTORY</p><h1>${subjectNames[subject]}</h1><p>Browse topics by grade.</p></div><div class="directory-grid subject-directory">',
            self.source,
        )
        self.assertIn("<title>Math Worksheets by Grade | Learning Made Simple</title>", self.math)
        self.assertIn('<link rel="canonical" href="https://simplelearningresources.com/math.html">', self.math)
        self.assertIn("<h1>Math</h1>", self.math)
        self.assertIn("Browse topics by grade.", self.math)
        self.assertNotIn("PRESCHOOL MATH", self.math)
        self.assertIn("<h1>Reading &amp; Language</h1>", self.reading)

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
        self.assertNotIn(
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

    def test_building_simple_sentences_uses_writing_and_language(self):
        resource = next(
            item for item in self.resources if item["id"] == "building-simple-sentences"
        )
        self.assertEqual(resource["taxonomy"]["grade"], "kindergarten")
        self.assertEqual(resource["taxonomy"]["subject"], "reading-language")
        self.assertEqual(resource["taxonomy"]["topic"], "writing-and-language")
        self.assertEqual(resource["taxonomy"]["skills"], ["sentences-and-mechanics"])

    def test_my_first_writing_adventures_uses_early_writing(self):
        resource = next(
            item for item in self.resources if item["id"] == "my-first-writing-adventures"
        )
        self.assertEqual(resource["taxonomy"]["grade"], "kindergarten")
        self.assertEqual(resource["taxonomy"]["subject"], "reading-language")
        self.assertEqual(resource["taxonomy"]["topic"], "writing-and-language")
        self.assertEqual(resource["taxonomy"]["skills"], ["early-writing-kindergarten"])

    def test_grade_directory_cards_flow_in_independent_columns(self):
        self.assertIn(
            ".grade-directory { display:block; columns:2; column-gap:20px; }",
            self.styles,
        )
        self.assertIn(
            ".grade-directory > div { break-inside:avoid; margin:0 0 20px; }",
            self.styles,
        )
        self.assertIn(".grade-directory { columns:1; }", self.styles)


if __name__ == "__main__":
    unittest.main()
