"""One-time bootstrap of the modular catalog from the production registry."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from catalog_lib import CATALOG_ROOT, REPOSITORY_ROOT, extract_live_registry, load_publisher_contracts


GRADES = [("preschool", "Preschool"), ("kindergarten", "Kindergarten"), ("grade-1", "Grade 1"), ("grade-2", "Grade 2")]
SUBJECTS = [
    ("math", "Math"),
    ("reading-language", "Reading & Language"),
    ("communication-life-skills", "Communication & Life Skills"),
    ("science-discovery", "Science & Discovery"),
    ("thinking-our-world", "Thinking & Our World"),
]
TOPICS = {
    "math": {
        "preschool": "Numbers & Counting|Early Addition & Subtraction|Shapes & Spatial Skills|Patterns|Measurement & Comparing|Sorting & Data",
        "kindergarten": "Numbers & Counting|Addition|Subtraction|Shapes & Geometry|Patterns|Measurement|Sorting & Data",
        "grade-1": "Numbers & Place Value|Addition|Subtraction|Measurement|Time|Shapes & Fractions|Data & Graphing|Mathematical Thinking",
        "grade-2": "Numbers & Place Value|Addition|Subtraction|Equal Groups & Arrays|Measurement|Time|Money|Data & Graphing|Geometry & Equal Shares",
    },
    "reading-language": {
        "preschool": "Alphabet|Print Awareness|Sounds & Beginning Phonics|Rhymes & Word Beats|Words & Vocabulary|Story & Comprehension|Early Writing",
        "kindergarten": "Alphabet & Letter Formation|Phonological Awareness|Phonics|CVC Words|High-Frequency Words|Vocabulary|Sentences|Early Comprehension|Story Elements|Early Writing",
        "grade-1": "Phonics & Word Reading|High-Frequency Words|Fluency|Vocabulary|Grammar & Sentences|Reading Comprehension|Story Elements|Informational Reading|Writing",
        "grade-2": "Advanced Phonics|Fluency|Vocabulary|Grammar|Reading Comprehension|Literature|Informational Reading|Writing",
    },
    "communication-life-skills": {
        "preschool": "Understanding Language|Expressing Needs & Ideas|WH Questions|Conversation & Play|Feelings & Social Understanding|Visual Supports & Routines|Independence & Safety",
        "kindergarten": "Following Directions|WH Questions|Expressing Ideas|Conversation|Social Skills|Feelings & Regulation|Routines & Independence|Safety & Self-Advocacy",
        "grade-1": "Following Directions|WH Questions|Describing & Explaining|Conversation|Social Communication|Emotions & Regulation|Independence|Self-Advocacy & Safety",
        "grade-2": "Following Complex Directions|Asking & Answering Questions|Describing & Explaining|Conversation|Social Understanding|Emotional Problem Solving|Independence & Organization|Self-Advocacy & Safety",
    },
    "science-discovery": {
        "preschool": "Animals|Plants & Nature|Human Body & Five Senses|Weather & Seasons|Earth & Space|Living & Non-Living|Exploring Materials|Little Scientist",
        "kindergarten": "Living Things|Plants|Animals|Human Body|Weather & Seasons|Earth & Sky|Materials & Motion|Scientific Thinking",
        "grade-1": "Plants & Animals|Human Body & Health|Earth & Space|Weather|Materials & Motion|Scientific Thinking",
        "grade-2": "Plants & Animals|Habitats & Life Cycles|Earth & Environment|Weather|Matter & Materials|Forces & Motion|Light & Sound|Scientific Thinking",
    },
    "thinking-our-world": {
        "preschool": "Logic & Matching|Myself & Family|Community|Maps & Places|Time & Sequence",
        "kindergarten": "Logic & Problem Solving|Myself & Family|Community|Maps & Places|Past & Present|Needs & Wants",
        "grade-1": "Logic & Reasoning|Families & Communities|Maps & Geography|Past & Present|Needs & Wants|Culture & Our World",
        "grade-2": "Logic & Reasoning|Communities|Maps & Geography|Past & Present|Economics|People & Culture",
    },
}


def slug(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.replace("&", " and ")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build() -> None:
    resources_root = CATALOG_ROOT / "resources"
    if resources_root.exists() and any(resources_root.rglob("*.json")):
        raise SystemExit("Refusing to overwrite existing authoritative resource definitions.")

    live = extract_live_registry(REPOSITORY_ROOT / "directory.js")
    contracts = load_publisher_contracts(REPOSITORY_ROOT / "worksheet-generator" / "content")
    grade_ids = {label: item_id for item_id, label in GRADES}
    subject_ids = {label: item_id for item_id, label in SUBJECTS}
    topic_ids = {}
    topics = []
    for subject_id, per_grade in TOPICS.items():
        for grade_id, topic_text in per_grade.items():
            for order, label in enumerate(topic_text.split("|"), 1):
                topic_id = slug(label)
                topic_ids[(grade_id, subject_id, label)] = topic_id
                topics.append({"id": topic_id, "label": label, "grade": grade_id, "subject": subject_id, "order": order})

    retired = {
        "id": "story-comprehension",
        "title": "Story & Comprehension",
        "description": "Explore picture stories, put events in order, and tell what happens next.",
        "grade": "Preschool",
        "subject": "Reading & Language",
        "topic": "Story & Comprehension",
        "skill": "Story Comprehension",
        "keywords": ["stories", "story comprehension", "look and answer", "picture sequencing", "what happens next", "draw what happens next", "beginning middle end"],
        "bundlePdf": "worksheets/preschool/reading/letters/story-comprehension.pdf",
        "thumbnailPath": "thumbnails/preschool/reading/letters/story-comprehension/page-01.png",
        "pageCount": 5,
        "pageLabels": ["Look and Answer", "Picture Sequencing", "What Happens Next?", "Draw What Happens Next", "Beginning, Middle & End"],
        "pagePdfDirectory": "worksheets/preschool/reading/letters/story-comprehension",
        "previewDirectory": "thumbnails/preschool/reading/letters/story-comprehension",
        "backHref": "topic.html?grade=Preschool&subject=Reading%20%26%20Language&topic=Story%20%26%20Comprehension",
        "backLabel": "Back to Story & Comprehension",
        "seo": {"title": "Story & Comprehension Printable Pack | Learning Made Simple", "description": "A five-page printable preschool pack with picture questions, sequencing, prediction, and beginning-middle-end activities."},
    }
    all_records = live + [retired]
    skill_seen = set()
    skills = []
    skill_order = defaultdict(int)
    for record in all_records:
        grade_id = grade_ids[record["grade"]]
        subject_id = subject_ids[record["subject"]]
        topic_id = topic_ids[(grade_id, subject_id, record["topic"])]
        key = (grade_id, subject_id, topic_id, record["skill"])
        if key not in skill_seen:
            skill_seen.add(key)
            skill_order[(grade_id, subject_id, topic_id)] += 1
            skills.append({"id": slug(record["skill"]), "label": record["skill"], "grade": grade_id, "subject": subject_id, "topic": topic_id, "order": skill_order[(grade_id, subject_id, topic_id)]})

    write_json(CATALOG_ROOT / "site.json", {"schemaVersion": 1, "canonicalOrigin": "https://simplelearningresources.com", "assetOrigin": "https://assets.simplelearningresources.com", "legacyResourcePath": "resource-preview.html"})
    write_json(CATALOG_ROOT / "taxonomy" / "grades.json", [{"id": item_id, "label": label, "order": order} for order, (item_id, label) in enumerate(GRADES, 1)])
    write_json(CATALOG_ROOT / "taxonomy" / "subjects.json", [{"id": item_id, "label": label, "order": order} for order, (item_id, label) in enumerate(SUBJECTS, 1)])
    write_json(CATALOG_ROOT / "taxonomy" / "topics.json", topics)
    write_json(CATALOG_ROOT / "taxonomy" / "skills.json", skills)

    within_topic = defaultdict(int)
    for catalog_order, record in enumerate(all_records, 1):
        grade_id = grade_ids[record["grade"]]
        subject_id = subject_ids[record["subject"]]
        topic_id = topic_ids[(grade_id, subject_id, record["topic"])]
        status = "published" if catalog_order <= len(live) else "retired"
        within_topic[(grade_id, subject_id, topic_id)] += 1
        contract = contracts[record["id"]]
        page_labels = record.get("pageLabels")
        pages = [{"label": label} if page_labels else {} for label in (page_labels or range(record["pageCount"]))]
        definition = {
            "schemaVersion": 1,
            "id": record["id"],
            "status": status,
            "title": record["title"],
            "description": record["description"],
            "taxonomy": {"grade": grade_id, "subject": subject_id, "topic": topic_id, "skills": [slug(record["skill"])]},
            "keywords": record["keywords"],
            "pages": pages,
            "assets": {"bundlePdf": record["bundlePdf"], "pagePdfDirectory": record["pagePdfDirectory"], "previewDirectory": record["previewDirectory"], "preview": {"width": 1224, "height": 1584, "dpi": 144, "format": "png"}},
            "seo": record["seo"],
            "source": {"type": "generated" if contract["hasGeneratorTemplate"] else "approved-bundle", "publisherContract": contract["path"], "generatorConfig": contract["path"] if contract["hasGeneratorTemplate"] else None},
            "ordering": {"catalog": catalog_order, "withinTopic": within_topic[(grade_id, subject_id, topic_id)]},
            "legacy": {"previewHref": f"resource-preview.html?resource={record['id']}", "backHref": record["backHref"], "backLabel": record["backLabel"]},
        }
        if status == "retired":
            definition["retiredReason"] = "Removed from the public registry pending replacement with a better structure."
        write_json(resources_root / grade_id / subject_id / topic_id / f"{record['id']}.json", definition)

    print(f"Created {len(live)} published and 1 retired resource definitions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="create the Step 1 catalog files")
    args = parser.parse_args()
    if not args.write:
        parser.error("--write is required")
    build()
