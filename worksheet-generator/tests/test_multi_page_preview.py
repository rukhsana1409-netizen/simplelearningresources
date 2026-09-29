import re
import sys
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DIRECTORY_SOURCE = REPOSITORY_ROOT / "directory.js"
PREVIEW_SOURCE = REPOSITORY_ROOT / "resource-preview.html"
sys.path.insert(0, str(REPOSITORY_ROOT / "site-tools"))

from catalog_lib import extract_live_registry  # noqa: E402


class MultiPageMetadataTests(unittest.TestCase):
    def _resources(self):
        return extract_live_registry(DIRECTORY_SOURCE)

    def test_all_canonical_resources_have_complete_unique_page_metadata(self):
        resources = self._resources()
        self.assertEqual(len(resources), 43)
        resource_ids = {resource["id"] for resource in resources}
        self.assertEqual(len(resource_ids), 43)
        self.assertIn("3d-shapes", resource_ids)
        self.assertIn("positional-words", resource_ids)
        self.assertIn("pre-writing-lines-strokes", resource_ids)
        self.assertIn("phrases-i-can-use", resource_ids)
        preview_paths = set()
        pdf_paths = set()

        for resource in resources:
            page_count = resource["pageCount"]
            for page_number in range(1, page_count + 1):
                filename = f"page-{page_number:02d}"
                preview_path = f'{resource["previewDirectory"]}/{filename}.png'
                pdf_path = f'{resource["pagePdfDirectory"]}/{filename}.pdf'
                self.assertNotIn(preview_path, preview_paths)
                self.assertNotIn(pdf_path, pdf_paths)
                self.assertTrue((REPOSITORY_ROOT / preview_path).is_file(), preview_path)
                self.assertTrue((REPOSITORY_ROOT / pdf_path).is_file(), pdf_path)
                preview_paths.add(preview_path)
                pdf_paths.add(pdf_path)
            self.assertEqual(
                resource["thumbnailPath"],
                f'{resource["previewDirectory"]}/page-01.png',
            )

        expected_pages = sum(resource["pageCount"] for resource in resources)
        self.assertEqual(len(preview_paths), expected_pages)
        self.assertEqual(len(pdf_paths), expected_pages)

    def test_directory_runtime_validation_covers_page_invariants(self):
        source = DIRECTORY_SOURCE.read_text(encoding="utf-8")
        for expected in (
            "resource.pages.length!==resource.pageCount",
            "page.number!==expectedNumber",
            "pagePreviewPaths.has(page.previewPath)",
            "pagePdfPaths.has(page.pdfPath)",
            "resource.thumbnailPath!==resource.pages[0].previewPath",
        ):
            self.assertIn(expected, source)
        self.assertNotIn("resources.length!==", source)


class MultiPagePreviewBehaviorTests(unittest.TestCase):
    def test_canonical_preview_and_download_urls_have_expected_download_flags(self):
        source = PREVIEW_SOURCE.read_text(encoding="utf-8")
        self.assertIn('document.getElementById("view-complete").href = resource.pdfUrl;', source)
        self.assertIn(
            'document.getElementById("download-complete").href = `${resource.pdfUrl}?download=1`;',
            source,
        )
        self.assertIn("previewLink.href = page.pdfUrl;", source)
        self.assertIn('downloadLink.href = `${page.pdfUrl}?download=1`;', source)
        self.assertIn('if (index > 0) image.loading = "lazy";', source)

    def test_legacy_number_paths_and_actions_remain_unchanged(self):
        source = PREVIEW_SOURCE.read_text(encoding="utf-8")
        self.assertIn('pdfPath: `worksheets/preschool/math/number-recognition/number-${numberValue}.pdf`', source)
        self.assertIn('thumbnailPath: `thumbnails/preschool/math/number-recognition/number-${numberValue}.png`', source)
        self.assertIn('document.getElementById("download").href = resource.pdfPath;', source)
        self.assertIn('document.getElementById("open-preview").href = resource.pdfPath;', source)
        self.assertIn("thumbnail.src = resource.thumbnailPath;", source)

    def test_every_directory_loader_uses_version_eight(self):
        references = []
        for path in REPOSITORY_ROOT.glob("*.html"):
            source = path.read_text(encoding="utf-8")
            references.extend(re.findall(r'directory\.js\?v=\d+', source))
        references.extend(
            re.findall(
                r'directory\.js\?v=\d+',
                (REPOSITORY_ROOT / "nav.js").read_text(encoding="utf-8"),
            )
        )
        self.assertEqual(len(references), 7)
        self.assertEqual(set(references), {"directory.js?v=8"})


if __name__ == "__main__":
    unittest.main()
