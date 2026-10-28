"""Verify that production resource previews are browser-loadable from a local server."""

from __future__ import annotations

import re
import struct
import threading
import urllib.request
from contextlib import contextmanager
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from catalog_lib import REPOSITORY_ROOT, CatalogValidationError, load_resources
from resource_discoverability import resource_page_href


ASSET_ORIGIN = "https://assets.simplelearningresources.com"
LOCAL_HOST_FALLBACK_MARKERS = (
    '["localhost", "127.0.0.1"]',
    'img[src^="https://assets.simplelearningresources.com/"]',
    "new URL(image.src).pathname",
)


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass


@contextmanager
def _local_server():
    handler = lambda *args, **kwargs: _QuietHandler(  # noqa: E731
        *args, directory=str(REPOSITORY_ROOT), **kwargs
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _get(url: str) -> tuple[bytes, str]:
    with urllib.request.urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise CatalogValidationError(f"Local preview request returned HTTP {response.status}: {url}")
        return response.read(), response.headers.get_content_type()


def _png_dimensions(data: bytes, url: str) -> tuple[int, int]:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise CatalogValidationError(f"Local preview response is not a valid PNG: {url}")
    return struct.unpack(">II", data[16:24])


def validate(resource_ids: set[str] | None = None) -> dict[str, int]:
    script = (REPOSITORY_ROOT / "resource-pages.js").read_text(encoding="utf-8")
    for marker in LOCAL_HOST_FALLBACK_MARKERS:
        if marker not in script:
            raise CatalogValidationError(f"Local preview fallback is missing: {marker}")

    published = [resource for resource in load_resources() if resource["status"] == "published"]
    if resource_ids is not None:
        published = [resource for resource in published if resource["id"] in resource_ids]
        missing = resource_ids - {resource["id"] for resource in published}
        if missing:
            raise CatalogValidationError(f"Unknown published resource IDs: {sorted(missing)}")

    preview_count = 0
    with _local_server() as origin:
        for resource in published:
            page_url = f"{origin}/{resource_page_href(resource)}"
            source, content_type = _get(page_url)
            if content_type != "text/html":
                raise CatalogValidationError(f"Local resource page is not HTML: {page_url}")
            image_urls = re.findall(r'<img[^>]+src="([^"]+)"', source.decode("utf-8"))
            preview_urls = [url for url in image_urls if url.startswith(f"{ASSET_ORIGIN}/thumbnails/")]
            if len(preview_urls) != len(resource["pages"]):
                raise CatalogValidationError(
                    f"{resource['id']}: preview count differs from page count "
                    f"({len(preview_urls)} != {len(resource['pages'])})"
                )
            for preview_url in preview_urls:
                local_url = f"{origin}{urlsplit(preview_url).path}"
                data, preview_content_type = _get(local_url)
                if preview_content_type != "image/png":
                    raise CatalogValidationError(
                        f"{resource['id']}: local preview has content type {preview_content_type}: {local_url}"
                    )
                if _png_dimensions(data, local_url) != (1224, 1584):
                    raise CatalogValidationError(
                        f"{resource['id']}: local preview dimensions are not 1224x1584: {local_url}"
                    )
                preview_count += 1

    return {"validatedPageCount": len(published), "validatedPreviewCount": preview_count}


if __name__ == "__main__":
    counts = validate()
    print(
        "LOCAL RESOURCE PREVIEWS VALID "
        f"pages={counts['validatedPageCount']} previews={counts['validatedPreviewCount']}"
    )
