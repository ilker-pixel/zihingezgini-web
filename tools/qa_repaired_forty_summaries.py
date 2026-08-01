#!/usr/bin/env python3
"""Quality gate for the repaired forty-summary batch."""

from __future__ import annotations

import hashlib
import json
import re
import statistics
import subprocess
from collections import defaultdict
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOK_NUMBERS = (
    8, 18, 34, 38, 61, 70, 92, 99, 121, 138,
    151, 157, 182, 195, 211, 216, 238, 244, 266, 294,
    12, 17, 32, 41, 66, 72, 93, 103, 122, 124,
    152, 156, 189, 194, 214, 222, 241, 253, 271, 275,
)
NEW_COVER_BOOKS = set(BOOK_NUMBERS[20:])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> bytes:
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.run(
        ["git", "show", f"HEAD:{relative}"], cwd=ROOT,
        check=True, capture_output=True,
    ).stdout


def narrative(summary: dict) -> list[str]:
    texts = [summary.get("intro", "")]
    for chapter in summary.get("chapters", []):
        texts.extend(chapter.get("paragraphs", []))
        texts.extend(chapter.get("extraParagraphs", []))
    return [text for text in texts if text]


def colorfulness(path: Path) -> float:
    with Image.open(path) as opened:
        image = opened.convert("RGB").resize((90, 135))
        channels = ImageStat.Stat(image).mean
        pixels = list(image.get_flattened_data())
    distances = [
        abs(r - g) + abs(g - b) + abs(b - r)
        for r, g, b in pixels
    ]
    return statistics.mean(distances)


def main() -> None:
    standard = json.loads((ROOT / "data" / "summary-production-standard.json").read_text(encoding="utf-8"))
    minimum = standard["content"]["minimumCharacters"]
    maximum_dense = standard["content"]["allowedDenseBookMaximumCharacters"]
    narrative_counts: list[int] = []
    paragraph_locations: dict[str, list[int]] = defaultdict(list)
    failures: list[str] = []
    report_rows: list[str] = []

    for number in BOOK_NUMBERS:
        summary_path = ROOT / "data" / "summaries" / f"{number}.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        texts = narrative(summary)
        characters = sum(len(text) for text in texts)
        narrative_counts.append(characters)
        if not minimum <= characters <= maximum_dense:
            failures.append(f"#{number}: narrative characters {characters} outside {minimum}-{maximum_dense}")
        if summary.get("enrichmentStandardVersion") != 1:
            failures.append(f"#{number}: missing enrichment standard version")
        for text in texts:
            if len(text) >= 120:
                paragraph_locations[text].append(number)
        if any("Bu rehber sınav notu gibi" in text for text in texts):
            failures.append(f"#{number}: removed shared padding returned")

        artworks = summary.get("chapterArtworks", {})
        if len(artworks) != 16:
            failures.append(f"#{number}: expected 16 interior artworks, got {len(artworks)}")
        art_hashes: set[str] = set()
        for art in artworks.values():
            path = ROOT / art["image"].lstrip("/")
            if not path.exists():
                failures.append(f"#{number}: missing interior artwork {path.relative_to(ROOT)}")
                continue
            current = path.read_bytes()
            original = git_blob(path)
            if hashlib.sha256(current).digest() != hashlib.sha256(original).digest():
                failures.append(f"#{number}: interior artwork changed: {path.relative_to(ROOT)}")
            art_hashes.add(hashlib.sha256(current).hexdigest())

        cover_path = ROOT / summary["coverImage"].lstrip("/")
        if not cover_path.exists():
            failures.append(f"#{number}: missing cover {cover_path.relative_to(ROOT)}")
        else:
            if sha256(cover_path) in art_hashes:
                failures.append(f"#{number}: cover duplicates an interior artwork")
            if number in NEW_COVER_BOOKS:
                with Image.open(cover_path) as cover:
                    if cover.size != (900, 1350):
                        failures.append(f"#{number}: new cover size is {cover.size}, expected 900x1350")
                score = colorfulness(cover_path)
                if score < 35:
                    failures.append(f"#{number}: cover colorfulness too low ({score:.1f})")

        pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
        if not pdf_path.exists():
            failures.append(f"#{number}: missing PDF")
            continue
        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)
        if not 25 <= pages <= 50:
            failures.append(f"#{number}: PDF has {pages} pages")
        unique_images: set[str] = set()
        extracted = []
        low_text_pages = 0
        for page_index, page in enumerate(reader.pages, 1):
            page_text = page.extract_text() or ""
            extracted.append(page_text)
            if page_index not in (1, 3) and len(page_text.strip()) < 180:
                low_text_pages += 1
            for image in page.images:
                unique_images.add(hashlib.sha256(image.data).hexdigest())
        if len(unique_images) < 17:
            failures.append(f"#{number}: PDF embeds only {len(unique_images)} unique images; expected cover + 16 interior")
        if low_text_pages:
            failures.append(f"#{number}: {low_text_pages} unexpectedly sparse PDF page(s)")
        report_rows.append(
            f"#{number:03d} {characters:5d} chars · {pages:2d} pages · "
            f"{len(unique_images):2d} unique images · {summary['title']}"
        )

    shared = {
        paragraph: locations
        for paragraph, locations in paragraph_locations.items()
        if len(set(locations)) > 1
    }
    if shared:
        example, locations = next(iter(shared.items()))
        failures.append(
            f"{len(shared)} exact long paragraph(s) shared across books; first in {sorted(set(locations))}: {example[:90]}"
        )

    average = statistics.mean(narrative_counts)
    if not 19_750 <= average <= 20_500:
        failures.append(f"Batch average is {average:.1f}, expected about 20,000")

    print("\n".join(report_rows))
    print(
        f"\nBATCH: {len(BOOK_NUMBERS)} books · mean {average:.1f} chars · "
        f"min {min(narrative_counts)} · max {max(narrative_counts)} · exact shared paragraphs {len(shared)}"
    )
    if failures:
        print("\nFAILURES:")
        print("\n".join(f"- {failure}" for failure in failures))
        raise SystemExit(1)
    print("\nPASS: repaired forty-summary quality gate")


if __name__ == "__main__":
    main()
