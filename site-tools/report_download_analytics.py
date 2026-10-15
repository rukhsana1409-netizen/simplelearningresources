"""Export private worksheet download summaries from Cloudflare Analytics Engine."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import urllib.request
from pathlib import Path
from typing import Any

from catalog_lib import load_resources


API_TEMPLATE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/analytics_engine/sql"
DATASET_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
CONTROLLED_TEST_RESOURCE_ID = "analytics-deployment-check"


def query_rows(account_id: str, token: str, dataset: str, days: int) -> list[dict[str, Any]]:
    if not DATASET_PATTERN.fullmatch(dataset):
        raise ValueError("CLOUDFLARE_ANALYTICS_DATASET must be a simple SQL identifier")
    sql = f"""
SELECT index1 AS resource_id, blob1 AS download_type, toUInt32(double1) AS page_number,
       sum(_sample_interval) AS clicks
FROM {dataset}
WHERE timestamp >= NOW() - INTERVAL '{days}' DAY
GROUP BY resource_id, download_type, page_number
ORDER BY resource_id, download_type, page_number
FORMAT JSON
""".strip()
    request = urllib.request.Request(
        API_TEMPLATE.format(account_id=account_id),
        data=sql.encode("utf-8"),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "text/plain; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise RuntimeError("Cloudflare Analytics Engine returned an unexpected response")
    return payload["data"]


def build_reports(rows: list[dict[str, Any]], resources: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    published = {resource["id"]: resource for resource in resources if resource["status"] == "published"}
    counts: dict[str, dict[str, Any]] = {}
    for row in rows:
        resource_id = str(row["resource_id"])
        if resource_id not in published:
            continue
        download_type = str(row["download_type"])
        page_number = int(row["page_number"])
        clicks = int(row["clicks"])
        item = counts.setdefault(resource_id, {"pack": 0, "pages": {}})
        if download_type == "pack" and page_number == 0:
            item["pack"] += clicks
        elif download_type == "page" and 1 <= page_number <= len(published[resource_id]["pages"]):
            item["pages"][page_number] = item["pages"].get(page_number, 0) + clicks

    summary = []
    pages = []
    for resource_id in sorted(published, key=lambda value: published[value]["ordering"]["catalog"]):
        resource = published[resource_id]
        item = counts.get(resource_id, {"pack": 0, "pages": {}})
        page_total = sum(item["pages"].values())
        summary.append({
            "resource_id": resource_id,
            "resource_name": resource["title"],
            "full_pack_clicks": item["pack"],
            "individual_page_clicks": page_total,
            "total_clicks": item["pack"] + page_total,
        })
        for page_number, page in enumerate(resource["pages"], start=1):
            pages.append({
                "resource_id": resource_id,
                "resource_name": resource["title"],
                "page_number": page_number,
                "page_name": page.get("label", f"Page {page_number}"),
                "clicks": item["pages"].get(page_number, 0),
            })
    return summary, pages


def build_validation_report(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clicks = sum(
        int(row["clicks"])
        for row in rows
        if str(row["resource_id"]) == CONTROLLED_TEST_RESOURCE_ID
    )
    return [{
        "resource_id": CONTROLLED_TEST_RESOURCE_ID,
        "event_class": "controlled_deployment_test",
        "clicks": clicks,
        "included_in_worksheet_totals": "no",
    }]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("Report rows must not be empty")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--output-directory", type=Path, default=Path("tmp/download-analytics"))
    args = parser.parse_args()
    if not 1 <= args.days <= 90:
        parser.error("--days must be between 1 and 90")

    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    dataset = os.environ.get("CLOUDFLARE_ANALYTICS_DATASET", "lms_download_clicks")
    if not account_id or not token:
        parser.error("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN are required")

    rows = query_rows(account_id, token, dataset, args.days)
    summary, pages = build_reports(rows, load_resources())
    validation = build_validation_report(rows)
    write_csv(args.output_directory / "worksheet-downloads.csv", summary)
    write_csv(args.output_directory / "worksheet-page-downloads.csv", pages)
    write_csv(args.output_directory / "download-analytics-validation.csv", validation)
    print(
        f"DOWNLOAD ANALYTICS REPORT resources={len(summary)} pages={len(pages)} "
        f"controlled_test_events={validation[0]['clicks']} days={args.days} output={args.output_directory}"
    )


if __name__ == "__main__":
    main()
