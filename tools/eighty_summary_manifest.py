#!/usr/bin/env python3
"""Create and maintain the recoverable 80-book production manifest."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKS_PATH = ROOT / "data" / "books.json"
MANIFEST_PATH = ROOT / "data" / "eighty-summary-manifest.json"

BATCHES = (
    (21, 42, 69, 94, 137, 159, 190, 217, 118, 215),
    (23, 44, 74, 97, 140, 160, 192, 221, 120, 286),
    (25, 45, 77, 101, 146, 162, 196, 223, 136, 169),
    (26, 46, 78, 105, 147, 163, 197, 225, 55, 242),
    (27, 49, 80, 106, 181, 164, 201, 251, 126, 293),
    (28, 51, 86, 112, 186, 166, 205, 256, 149, 171),
    (29, 53, 123, 114, 187, 167, 209, 258, 57, 245),
    (56, 54, 125, 116, 188, 168, 210, 259, 129, 150),
)

STAGES = (
    "selected",
    "researched",
    "text_ready",
    "art_ready",
    "pdf_ready",
    "qa_passed",
    "site_ready",
    "published",
)


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_manifest() -> dict:
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    by_no = {int(book["no"]): book for book in books}
    selected = [number for batch in BATCHES for number in batch]
    if len(selected) != 80 or len(set(selected)) != 80:
        raise RuntimeError("The production list must contain 80 unique books")

    rows = []
    for batch_no, numbers in enumerate(BATCHES, 1):
        for position, number in enumerate(numbers, 1):
            book = by_no[number]
            if book.get("hasSummary"):
                raise RuntimeError(f"Book {number} is already summarized")
            rows.append({
                "no": number,
                "author": book["author"],
                "title": book["title"],
                "category": book["category"],
                "batch": batch_no,
                "position": position,
                "stage": "selected",
                "checks": {},
                "updatedAt": now(),
            })

    return {
        "version": 1,
        "createdAt": now(),
        "updatedAt": now(),
        "targetCharacters": 20000,
        "characterGate": [18500, 22000],
        "pageGate": [25, 50],
        "chapterImagesPerBook": 16,
        "stages": list(STAGES),
        "batches": [list(batch) for batch in BATCHES],
        "books": rows,
    }


def load_or_create() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return create_manifest()


def write(manifest: dict) -> None:
    manifest["updatedAt"] = now()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def set_stage(book_numbers: list[int], stage: str, checks: dict | None = None) -> None:
    if stage not in STAGES:
        raise ValueError(f"Unknown stage: {stage}")
    manifest = load_or_create()
    wanted = set(book_numbers)
    found = set()
    for row in manifest["books"]:
        if row["no"] not in wanted:
            continue
        if STAGES.index(stage) < STAGES.index(row["stage"]):
            raise RuntimeError(f"Refusing to move book {row['no']} backwards")
        row["stage"] = stage
        row["updatedAt"] = now()
        if checks:
            row["checks"].update(checks)
        found.add(row["no"])
    missing = wanted - found
    if missing:
        raise KeyError(f"Books not present in manifest: {sorted(missing)}")
    write(manifest)


def report(manifest: dict) -> None:
    counts = {stage: 0 for stage in STAGES}
    for row in manifest["books"]:
        counts[row["stage"]] += 1
    print(f"Manifest: {len(manifest['books'])} books in {len(manifest['batches'])} batches")
    for stage in STAGES:
        if counts[stage]:
            print(f"  {stage}: {counts[stage]}")


if __name__ == "__main__":
    current = load_or_create()
    write(current)
    report(current)
