#!/usr/bin/env python3
"""Track the final 72-summary production in eight nine-book waves."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKS_PATH = ROOT / "data" / "books.json"
MANIFEST_PATH = ROOT / "data" / "final-seventy-two-manifest.json"

BATCHES = (
    (30, 52, 83, 84, 102, 113, 115, 117, 119),
    (128, 131, 132, 133, 134, 144, 148, 170, 174),
    (175, 177, 180, 198, 202, 203, 206, 207, 208),
    (219, 226, 227, 228, 230, 231, 232, 233, 234),
    (236, 237, 246, 247, 249, 250, 252, 257, 260),
    (261, 262, 264, 265, 267, 268, 269, 270, 272),
    (273, 274, 276, 278, 279, 280, 281, 282, 283),
    (289, 291, 292, 295, 296, 297, 298, 299, 300),
)
STAGES = ("selected", "researched", "text_ready", "art_ready", "pdf_ready", "qa_passed", "site_ready", "published")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def create_manifest() -> dict:
    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    by_no = {int(book["no"]): book for book in books}
    selected = [number for batch in BATCHES for number in batch]
    if len(selected) != 72 or len(set(selected)) != 72:
        raise RuntimeError("Final production list must contain 72 unique works")
    rows = []
    for batch_no, numbers in enumerate(BATCHES, 1):
        for position, number in enumerate(numbers, 1):
            book = by_no[number]
            if book.get("hasSummary"):
                raise RuntimeError(f"Book {number} is already summarized")
            rows.append({
                "no": number, "author": book["author"], "title": book["title"],
                "category": book["category"], "batch": batch_no, "position": position,
                "stage": "selected", "checks": {}, "updatedAt": now(),
            })
    return {
        "version": 1, "createdAt": now(), "updatedAt": now(),
        "targetCharacters": 20000, "characterGate": [18000, 22000],
        "denseBookMaximumCharacters": 24000, "pageGate": [25, 50],
        "chapterImagesPerBook": 16, "stages": list(STAGES),
        "batches": [list(batch) for batch in BATCHES], "books": rows,
    }


def load_or_create() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else create_manifest()


def write(manifest: dict) -> None:
    manifest["updatedAt"] = now()
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def set_stage(book_numbers: list[int], stage: str, checks: dict | None = None) -> None:
    if stage not in STAGES:
        raise ValueError(f"Unknown stage: {stage}")
    manifest = load_or_create()
    wanted, found = set(book_numbers), set()
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
    print(f"Manifest: {len(manifest['books'])} works in {len(manifest['batches'])} waves")
    for stage in STAGES:
        if counts[stage]:
            print(f"  {stage}: {counts[stage]}")


if __name__ == "__main__":
    current = load_or_create()
    write(current)
    report(current)
