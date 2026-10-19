from pathlib import Path
import tempfile
import unittest

import pymupdf

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from review_pack import (  # noqa: E402
    APPROVAL_NAME,
    MANIFEST_NAME,
    ReviewError,
    build_manifest,
    create_approval,
    require_handoff_branch,
    require_review_branch,
    verify_approval,
    verify_manifest,
    write_json,
)


def make_pdf(path: Path, texts: list[str], size=(612, 792)) -> None:
    document = pymupdf.open()
    for text in texts:
        page = document.new_page(width=size[0], height=size[1])
        page.insert_text((72, 72), text)
    document.save(path)


class ReviewPackTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.pack = self.root / "pack"
        self.previews = self.root / "previews"
        self.review = self.root / "tmp" / "reviews" / "sample"
        self.pack.mkdir()
        self.previews.mkdir()
        self.bundle = self.pack / "sample-review.pdf"
        self.guide = self.pack / "sample-parent-guide.pdf"
        make_pdf(self.bundle, ["Page one", "Page two"])
        make_pdf(self.guide, ["Parent guide"])
        bundle = pymupdf.open(self.bundle)
        self.individuals = []
        self.preview_files = []
        for index, page in enumerate(bundle):
            individual = self.pack / f"sample-page-{index + 1:02d}.pdf"
            output = pymupdf.open()
            output.insert_pdf(bundle, from_page=index, to_page=index)
            output.save(individual)
            self.individuals.append(individual)
            preview = self.previews / f"page-{index + 1:02d}.png"
            page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False).save(preview)
            self.preview_files.append(preview)

    def tearDown(self):
        self.temporary.cleanup()

    def prepare(self):
        manifest = build_manifest(
            resource_id="sample",
            bundle=self.bundle,
            individual_pages=self.individuals,
            previews=self.preview_files,
            parent_guide=self.guide,
            expected_pages=2,
            review_dir=self.review,
            root=self.root,
            branch="muse/review/sample",
        )
        manifest_path = self.review / MANIFEST_NAME
        write_json(manifest_path, manifest)
        return manifest_path, manifest

    def test_prepare_records_complete_review_set_and_hashes(self):
        manifest_path, manifest = self.prepare()
        self.assertEqual(manifest["expectedPageCount"], 2)
        self.assertEqual(len(manifest["files"]), 8)
        self.assertEqual(len(manifest["chatgptReviewSet"]), 5)
        self.assertEqual(verify_manifest(manifest_path, self.root)["resourceId"], "sample")

    def test_changed_file_requires_reapproval(self):
        manifest_path, _ = self.prepare()
        self.individuals[0].write_bytes(self.individuals[0].read_bytes() + b"changed")
        with self.assertRaisesRegex(ReviewError, "requires reapproval"):
            verify_manifest(manifest_path, self.root)

    def test_approval_locks_manifest_bundle_and_parent_guide(self):
        manifest_path, _ = self.prepare()
        approval_path = self.review / APPROVAL_NAME
        create_approval(manifest_path, approval_path, self.root, "Reviewer", "review-123")
        manifest, approval = verify_approval(manifest_path, approval_path, self.root)
        self.assertEqual(approval["resourceId"], manifest["resourceId"])
        manifest["reviewChecklist"].append("Changed after approval")
        write_json(manifest_path, manifest)
        with self.assertRaisesRegex(ReviewError, "manifest changed"):
            verify_approval(manifest_path, approval_path, self.root)

    def test_rejects_non_letter_page(self):
        make_pdf(self.bundle, ["Wrong size"], size=(600, 800))
        with self.assertRaisesRegex(ReviewError, "expected US Letter"):
            build_manifest(
                resource_id="sample", bundle=self.bundle,
                individual_pages=self.individuals[:1], previews=self.preview_files[:1],
                parent_guide=self.guide, expected_pages=1,
                review_dir=self.review, root=self.root, branch="muse/review/sample",
            )

    def test_review_branch_is_separate_from_permanent_handoff(self):
        require_review_branch("muse/review/sample")
        with self.assertRaises(ReviewError):
            require_review_branch("muse/kindergarten-handoff")

    def test_promotion_requires_permanent_handoff_branch(self):
        require_handoff_branch("muse/kindergarten-handoff")
        with self.assertRaises(ReviewError):
            require_handoff_branch("muse/review/sample")


if __name__ == "__main__":
    unittest.main()
