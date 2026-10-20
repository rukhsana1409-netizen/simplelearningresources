"""Prepare and lock worksheet packs for human review before Muse handoff.

This tool validates files and records approval evidence. It never changes Git
branches, uploads assets, publishes resources, or deploys the website.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

import pymupdf


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
US_LETTER = (612.0, 792.0)
MANIFEST_NAME = "review-manifest.json"
APPROVAL_NAME = "approval.json"


class ReviewError(RuntimeError):
    """A review pack is incomplete, invalid, or no longer approved."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ReviewError(f"Review files must stay inside the repository: {path}") from exc


def require_file(path: Path, label: str) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ReviewError(f"Missing or empty {label}: {path}")


def inspect_pdf(path: Path, expected_pages: int | None = None) -> list[dict]:
    require_file(path, "PDF")
    try:
        document = pymupdf.open(path)
    except Exception as exc:
        raise ReviewError(f"Cannot open PDF {path}: {exc}") from exc
    if document.needs_pass:
        raise ReviewError(f"Password-protected PDF is not reviewable: {path}")
    if expected_pages is not None and document.page_count != expected_pages:
        raise ReviewError(
            f"Unexpected page count for {path}: expected {expected_pages}, found {document.page_count}"
        )
    pages = []
    for number, page in enumerate(document, 1):
        width, height = page.rect.width, page.rect.height
        if abs(width - US_LETTER[0]) > 0.5 or abs(height - US_LETTER[1]) > 0.5:
            raise ReviewError(
                f"Page {number} in {path} is {width:g}x{height:g} pt; expected US Letter 612x792 pt"
            )
        try:
            pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        except Exception as exc:
            raise ReviewError(f"Page {number} in {path} did not render: {exc}") from exc
        pages.append(
            {
                "number": number,
                "widthPoints": width,
                "heightPoints": height,
                "renderWidth": pixmap.width,
                "renderHeight": pixmap.height,
                "pixelSha256": hashlib.sha256(pixmap.samples).hexdigest(),
            }
        )
    return pages


def inspect_image(path: Path) -> dict:
    require_file(path, "preview")
    try:
        pixmap = pymupdf.Pixmap(path)
    except Exception as exc:
        raise ReviewError(f"Cannot decode preview {path}: {exc}") from exc
    if pixmap.width < 600 or pixmap.height < 700:
        raise ReviewError(f"Preview is too small for useful review: {path} ({pixmap.width}x{pixmap.height})")
    return {"width": pixmap.width, "height": pixmap.height}


def file_record(path: Path, role: str, root: Path, **extra: object) -> dict:
    record = {
        "role": role,
        "path": repo_path(path, root),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    record.update(extra)
    return record


def git_branch(root: Path) -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"], cwd=root, check=True,
        capture_output=True, text=True, encoding="utf-8",
    )
    return result.stdout.strip()


def require_review_branch(branch: str) -> None:
    if not branch.startswith("muse/review/"):
        raise ReviewError(
            f"Draft preparation must run on a separate muse/review/<pack> branch; current branch is {branch!r}"
        )


def require_handoff_branch(branch: str) -> None:
    if not (branch.startswith("muse/") and branch.endswith("-handoff")):
        raise ReviewError(
            f"Promotion verification must run on a permanent muse/*-handoff branch; current branch is {branch!r}"
        )


def build_manifest(
    *, resource_id: str, bundle: Path, individual_pages: list[Path],
    previews: list[Path], parent_guide: Path | None, expected_pages: int,
    review_dir: Path, root: Path, branch: str,
) -> dict:
    if len(individual_pages) != expected_pages:
        raise ReviewError(f"Expected {expected_pages} individual PDFs, found {len(individual_pages)}")
    if len(previews) != expected_pages:
        raise ReviewError(f"Expected {expected_pages} previews, found {len(previews)}")

    bundle_pages = inspect_pdf(bundle, expected_pages)
    guide_pages = inspect_pdf(parent_guide) if parent_guide is not None else None
    if guide_pages is not None and not guide_pages:
        raise ReviewError("Parent guide must contain at least one page")

    records = [file_record(bundle, "combined-pdf", root, pageCount=expected_pages)]
    for index, path in enumerate(individual_pages):
        pages = inspect_pdf(path, 1)
        if pages[0]["pixelSha256"] != bundle_pages[index]["pixelSha256"]:
            raise ReviewError(
                f"Individual PDF does not render identically to bundle page {index + 1}: {path}"
            )
        records.append(file_record(path, "individual-page-pdf", root, pageNumber=index + 1, pageCount=1))
    for index, path in enumerate(previews):
        records.append(file_record(path, "preview", root, pageNumber=index + 1, **inspect_image(path)))
    if parent_guide is not None:
        records.append(file_record(parent_guide, "parent-guide", root, pageCount=len(guide_pages)))

    render_dir = review_dir / "renders"
    render_dir.mkdir(parents=True, exist_ok=True)
    for old_render in render_dir.glob("page-*.png"):
        old_render.unlink()
    document = pymupdf.open(bundle)
    for index, page in enumerate(document):
        output = render_dir / f"page-{index + 1:02d}.png"
        page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False).save(output)
        records.append(file_record(output, "review-render", root, pageNumber=index + 1, **inspect_image(output)))

    records.sort(key=lambda item: (item["role"], item.get("pageNumber", 0), item["path"]))
    chatgpt_review_set = [repo_path(bundle, root)]
    if parent_guide is not None:
        chatgpt_review_set.append(repo_path(parent_guide, root))
    chatgpt_review_set.extend(
        repo_path(render_dir / f"page-{number:02d}.png", root)
        for number in range(1, expected_pages + 1)
    )
    chatgpt_review_set.append(repo_path(review_dir / MANIFEST_NAME, root))

    review_checklist = ["Review the complete combined PDF in page order."]
    if parent_guide is not None:
        review_checklist.append("Review the complete parent guide.")
    review_checklist.extend(
        [
            "Check educational accuracy, instructions, artwork, clipping, overlap, and age appropriateness.",
            "Record every flagged page before Muse revises the pack.",
            (
                "Approve only the complete revised PDF and parent guide together."
                if parent_guide is not None
                else "Approve only the complete revised PDF."
            ),
        ]
    )

    return {
        "schemaVersion": 1,
        "resourceId": resource_id,
        "reviewBranch": branch,
        "expectedPageCount": expected_pages,
        "status": "awaiting-human-approval",
        "files": records,
        "chatgptReviewSet": chatgpt_review_set,
        "reviewChecklist": review_checklist,
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def manifest_file_map(manifest: dict, root: Path) -> dict[str, dict]:
    return {record["path"]: record for record in manifest["files"]}


def verify_manifest(manifest_path: Path, root: Path) -> dict:
    require_file(manifest_path, "review manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for relative, record in manifest_file_map(manifest, root).items():
        path = root / relative
        require_file(path, record["role"])
        actual = sha256(path)
        if actual != record["sha256"]:
            raise ReviewError(f"Reviewed file changed and requires reapproval: {relative}")
    return manifest


def create_approval(
    manifest_path: Path, approval_path: Path, root: Path,
    approved_by: str, approval_reference: str,
) -> dict:
    manifest = verify_manifest(manifest_path, root)
    records = manifest_file_map(manifest, root)
    bundle = next(record for record in records.values() if record["role"] == "combined-pdf")
    guide = next((record for record in records.values() if record["role"] == "parent-guide"), None)
    approval = {
        "schemaVersion": 1,
        "resourceId": manifest["resourceId"],
        "approvedBy": approved_by,
        "approvalReference": approval_reference,
        "approvedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "manifestSha256": sha256(manifest_path),
        "bundleSha256": bundle["sha256"],
        "statement": (
            "The complete combined PDF and parent guide were explicitly approved together."
            if guide is not None
            else "The complete combined PDF was explicitly approved."
        ),
    }
    if guide is not None:
        approval["parentGuideSha256"] = guide["sha256"]
    write_json(approval_path, approval)
    return approval


def verify_approval(manifest_path: Path, approval_path: Path, root: Path) -> tuple[dict, dict]:
    manifest = verify_manifest(manifest_path, root)
    require_file(approval_path, "approval record")
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    if approval.get("resourceId") != manifest.get("resourceId"):
        raise ReviewError("Approval resource ID does not match the review manifest")
    if approval.get("manifestSha256") != sha256(manifest_path):
        raise ReviewError("Review manifest changed after approval; complete reapproval is required")
    records = manifest_file_map(manifest, root)
    bundle = next(record for record in records.values() if record["role"] == "combined-pdf")
    guide = next((record for record in records.values() if record["role"] == "parent-guide"), None)
    if approval.get("bundleSha256") != bundle["sha256"]:
        raise ReviewError("Approved bundle hash no longer matches")
    if guide is not None and approval.get("parentGuideSha256") != guide["sha256"]:
        raise ReviewError("Approved parent-guide hash no longer matches")
    return manifest, approval


def expand_paths(root: Path, pattern: str) -> list[Path]:
    return sorted(root.glob(pattern))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="validate a complete draft and write review artifacts")
    prepare.add_argument("--resource-id", required=True)
    prepare.add_argument("--bundle", required=True, type=Path)
    prepare.add_argument("--individual-glob", required=True)
    prepare.add_argument("--preview-glob", required=True)
    prepare.add_argument("--parent-guide", type=Path)
    prepare.add_argument("--expected-pages", required=True, type=int)
    prepare.add_argument("--review-dir", required=True, type=Path)

    verify = subparsers.add_parser("verify", help="verify that reviewed files still match the manifest")
    verify.add_argument("--review-dir", required=True, type=Path)
    verify.add_argument("--require-approval", action="store_true")

    approve = subparsers.add_parser("approve", help="record explicit human approval of the complete pack")
    approve.add_argument("--review-dir", required=True, type=Path)
    approve.add_argument("--approved-by", required=True)
    approve.add_argument("--approval-reference", required=True)

    promotion = subparsers.add_parser("check-promotion", help="gate promotion on an unchanged approved pack")
    promotion.add_argument("--review-dir", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    root = REPOSITORY_ROOT
    review_dir = (root / args.review_dir).resolve()
    manifest_path = review_dir / MANIFEST_NAME
    approval_path = review_dir / APPROVAL_NAME
    branch = git_branch(root)

    if args.command == "prepare":
        require_review_branch(branch)
        manifest = build_manifest(
            resource_id=args.resource_id,
            bundle=(root / args.bundle).resolve(),
            individual_pages=expand_paths(root, args.individual_glob),
            previews=expand_paths(root, args.preview_glob),
            parent_guide=(root / args.parent_guide).resolve() if args.parent_guide else None,
            expected_pages=args.expected_pages,
            review_dir=review_dir,
            root=root,
            branch=branch,
        )
        write_json(manifest_path, manifest)
        if approval_path.exists():
            approval_path.unlink()
        print(
            f"REVIEW READY resource={args.resource_id} pages={args.expected_pages} "
            f"files={len(manifest['files'])} manifest={repo_path(manifest_path, root)}"
        )
    elif args.command == "approve":
        approval = create_approval(
            manifest_path, approval_path, root, args.approved_by, args.approval_reference
        )
        print(
            f"APPROVAL RECORDED resource={approval['resourceId']} "
            f"manifest_sha256={approval['manifestSha256']}"
        )
    elif args.command == "verify":
        if args.require_approval:
            manifest, _ = verify_approval(manifest_path, approval_path, root)
        else:
            manifest = verify_manifest(manifest_path, root)
        print(f"REVIEW VERIFIED resource={manifest['resourceId']} approval={args.require_approval}")
    elif args.command == "check-promotion":
        require_handoff_branch(branch)
        manifest, approval = verify_approval(manifest_path, approval_path, root)
        print(
            f"PROMOTION READY resource={manifest['resourceId']} "
            f"approval_reference={approval['approvalReference']}"
        )


if __name__ == "__main__":
    try:
        main()
    except (ReviewError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(1)
