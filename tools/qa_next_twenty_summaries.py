#!/usr/bin/env python3
"""Quality gate for the third twenty-book illustrated summary collection."""

from __future__ import annotations

import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOK_NUMBERS = (
    9, 33, 37, 50, 62, 63, 68, 75, 79, 87,
    89, 100, 107, 111, 145, 158, 172, 183, 199, 239,
)


def narrative(summary: dict) -> list[str]:
    texts = [summary.get("intro", "")]
    for chapter in summary.get("chapters", []):
        texts.extend(chapter.get("paragraphs", []))
        texts.extend(chapter.get("extraParagraphs", []))
    return [text for text in texts if text]


def colorfulness(path: Path) -> float:
    with Image.open(path) as opened:
        image = opened.convert("RGB").resize((90, 135))
        pixels = list(image.get_flattened_data())
    return statistics.mean(abs(r - g) + abs(g - b) + abs(b - r) for r, g, b in pixels)


def main() -> None:
    standard = json.loads((ROOT / "data" / "summary-production-standard.json").read_text(encoding="utf-8"))
    minimum = standard["content"]["minimumCharacters"]
    maximum = standard["content"]["maximumCharacters"]
    paragraph_locations: dict[str, list[int]] = defaultdict(list)
    all_art_hashes: dict[str, tuple[int, str]] = {}
    counts: list[int] = []
    failures: list[str] = []
    rows: list[str] = []

    for number in BOOK_NUMBERS:
        summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8"))
        texts = narrative(summary)
        characters = sum(map(len, texts))
        counts.append(characters)
        if not minimum <= characters <= maximum:
            failures.append(f"#{number}: {characters} narrative characters outside {minimum}-{maximum}")
        if summary.get("enrichmentStandardVersion") not in (1, 2):
            failures.append(f"#{number}: enrichment standard version missing")
        for paragraph in texts:
            if len(paragraph) >= 120:
                paragraph_locations[paragraph].append(number)

        artworks = summary.get("chapterArtworks", {})
        if len(artworks) != 16:
            failures.append(f"#{number}: {len(artworks)} chapter artworks instead of 16")
        local_hashes: set[str] = set()
        for artwork in artworks.values():
            path = ROOT / artwork["image"].lstrip("/")
            if not path.exists():
                failures.append(f"#{number}: missing artwork {path.relative_to(ROOT)}")
                continue
            with Image.open(path) as image:
                if image.size != (720, 720):
                    failures.append(f"#{number}: artwork {path.name} has size {image.size}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in local_hashes:
                failures.append(f"#{number}: duplicate interior artwork")
            if digest in all_art_hashes:
                failures.append(f"#{number}: artwork duplicates book #{all_art_hashes[digest][0]}")
            local_hashes.add(digest)
            all_art_hashes[digest] = (number, path.name)

        cover_path = ROOT / summary["coverImage"].lstrip("/")
        if not cover_path.exists():
            failures.append(f"#{number}: cover missing")
        else:
            with Image.open(cover_path) as cover:
                if cover.size != (900, 1350):
                    failures.append(f"#{number}: cover size {cover.size} instead of 900x1350")
            cover_hash = hashlib.sha256(cover_path.read_bytes()).hexdigest()
            if cover_hash in local_hashes:
                failures.append(f"#{number}: cover duplicates interior art")
            if colorfulness(cover_path) < 35:
                failures.append(f"#{number}: cover is not sufficiently colorful")

        pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
        if not pdf_path.exists():
            failures.append(f"#{number}: PDF missing")
            continue
        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)
        if not 25 <= pages <= 50:
            failures.append(f"#{number}: {pages} PDF pages outside 25-50")
        unique_images: set[str] = set()
        sparse_pages: list[int] = []
        for page_index, page in enumerate(reader.pages, 1):
            page_text = page.extract_text() or ""
            if page_index not in (1, 3) and len(page_text.strip()) < 180:
                sparse_pages.append(page_index)
            for embedded in page.images:
                unique_images.add(hashlib.sha256(embedded.data).hexdigest())
        if sparse_pages:
            failures.append(f"#{number}: unexpectedly sparse PDF pages {sparse_pages}")
        if len(unique_images) < 17:
            failures.append(f"#{number}: PDF has only {len(unique_images)} unique images")

        rows.append(
            f"#{number:03d} {characters:5d} chars · {pages:2d} pages · "
            f"{len(unique_images):2d} images · {summary['title']}"
        )

    shared = {
        paragraph: sorted(set(locations))
        for paragraph, locations in paragraph_locations.items()
        if len(set(locations)) > 1
    }
    if shared:
        example, locations = next(iter(shared.items()))
        failures.append(
            f"{len(shared)} exact long paragraphs shared across books; first in {locations}: {example[:100]}"
        )

    average = statistics.mean(counts)
    if not 19_750 <= average <= 20_500:
        failures.append(f"batch mean {average:.1f} is not approximately 20,000")

    print("\n".join(rows))
    print(
        f"\nBATCH: {len(BOOK_NUMBERS)} books · mean {average:.1f} chars · "
        f"min {min(counts)} · max {max(counts)} · {len(BOOK_NUMBERS) * 16} unique interior images · "
        f"exact shared paragraphs {len(shared)}"
    )
    if failures:
        print("\nFAILURES:")
        print("\n".join(f"- {failure}" for failure in failures))
        raise SystemExit(1)
    print("\nPASS: next twenty-summary quality gate")


if __name__ == "__main__":
    main()
