import re
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DIRECTORY_SOURCE = REPOSITORY_ROOT / "directory.js"
PREVIEW_SOURCE = REPOSITORY_ROOT / "resource-preview.html"


class MultiPageMetadataTests(unittest.TestCase):
    def _resources(self):
        source = DIRECTORY_SOURCE.read_text(encoding="utf-8")
        pattern = re.compile(
            r'\{id:"(?P<id>[^"]+)".*?pdfPath:"(?P<bundle>[^"]+)"'
            r',thumbnailPath:"(?P<thumbnail>[^"]+)"'
            r',pageCount:(?P<count>\d+),pages:defineWorksheetPages\('
            r'(?P<pages_count>\d+),"(?P<pdf_directory>[^"]+)",'
            r'"(?P<preview_directory>[^"]+)"\)'
        )
        return [match.groupdict() for match in pattern.finditer(source)]

    def test_all_canonical_resources_have_complete_unique_page_metadata(self):
        resources = self._resources()
        self.assertEqual(len(resources), 21)
        resource_ids = {resource["id"] for resource in resources}
        self.assertEqual(len(resource_ids), 21)
        self.assertIn("3d-shapes", resource_ids)
        self.assertIn("positional-words", resource_ids)
        preview_paths = set()
        pdf_paths = set()

        for resource in resources:
            page_count = int(resource["count"])
            self.assertEqual(page_count, int(resource["pages_count"]))
            for page_number in range(1, page_count + 1):
                filename = f"page-{page_number:02d}"
                preview_path = f'{resource["preview_directory"]}/{filename}.png'
                pdf_path = f'{resource["pdf_directory"]}/{filename}.pdf'
                self.assertNotIn(preview_path, preview_paths)
                self.assertNotIn(pdf_path, pdf_paths)
                self.assertTrue((REPOSITORY_ROOT / preview_path).is_file(), preview_path)
                self.assertTrue((REPOSITORY_ROOT / pdf_path).is_file(), pdf_path)
                preview_paths.add(preview_path)
                pdf_paths.add(pdf_path)
            self.assertEqual(
                resource["thumbnail"],
                f'{resource["preview_directory"]}/page-01.png',
            )

        self.assertEqual(len(preview_paths), 102)
        self.assertEqual(len(pdf_paths), 102)

    def test_directory_runtime_validation_covers_page_invariants(self):
        source = DIRECTORY_SOURCE.read_text(encoding="utf-8")
        for expected in (
            "resources.length!==21",
            "resource.pages.length!==resource.pageCount",
            "page.number!==expectedNumber",
            "pagePreviewPaths.has(page.previewPath)",
            "pagePdfPaths.has(page.pdfPath)",
            "resource.thumbnailPath!==resource.pages[0].previewPath",
        ):
            self.assertIn(expected, source)


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

    def test_every_directory_loader_uses_version_four(self):
        references = []
        for path in REPOSITORY_ROOT.glob("*.html"):
            source = path.read_text(encoding="utf-8")
            references.extend(re.findall(r'directory\.js(?:\?v=\d+)?', source))
        references.extend(
            re.findall(
                r'directory\.js(?:\?v=\d+)?',
                (REPOSITORY_ROOT / "nav.js").read_text(encoding="utf-8"),
            )
        )
        self.assertEqual(len(references), 6)
        self.assertEqual(set(references), {"directory.js?v=4"})


if __name__ == "__main__":
    unittest.main()
