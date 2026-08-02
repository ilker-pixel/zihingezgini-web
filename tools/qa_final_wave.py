#!/usr/bin/env python3
"""Strict content, artwork, PDF and rendered-page gate for a final wave."""

from __future__ import annotations

import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


def narrative(summary: dict) -> list[str]:
    output = [summary.get("intro", "")]
    for chapter in summary.get("chapters", []):
        output.extend(chapter.get("paragraphs", []))
        output.extend(chapter.get("extraParagraphs", []))
    return [text for text in output if text]


def sentences(texts: list[str]) -> list[str]:
    return [
        sentence.strip()
        for text in texts
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if len(sentence.strip()) >= 70
    ]


def colorfulness(path: Path) -> float:
    with Image.open(path) as source:
        pixels = list(source.convert("RGB").resize((90, 135)).get_flattened_data())
    return statistics.mean(abs(r - g) + abs(g - b) + abs(b - r) for r, g, b in pixels)


def run(numbers: tuple[int, ...], render_root: Path) -> None:
    standard = json.loads((ROOT / "data" / "summary-production-standard.json").read_text())
    minimum = standard["content"]["minimumCharacters"]
    maximum = standard["content"]["maximumCharacters"]
    dense_maximum = standard["content"]["allowedDenseBookMaximumCharacters"]
    exact_locations: dict[str, list[int]] = defaultdict(list)
    long_paragraphs: list[tuple[int, str]] = []
    global_art: dict[str, int] = {}
    counts: list[int] = []
    failures: list[str] = []
    rows: list[str] = []

    for number in numbers:
        summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text())
        texts = narrative(summary)
        characters = sum(map(len, texts))
        counts.append(characters)
        upper = dense_maximum if summary.get("meta", {}).get("dense") else maximum
        if not minimum <= characters <= upper:
            failures.append(f"#{number}: {characters} characters outside {minimum}-{upper}")
        if summary.get("enrichmentStandardVersion") != 3:
            failures.append(f"#{number}: final enrichment standard version is not 3")
        if len(summary.get("chapters", [])) != 21:
            failures.append(f"#{number}: chapter count is not 21")
        for paragraph in texts:
            if len(paragraph) >= 120:
                exact_locations[paragraph].append(number)
                long_paragraphs.append((number, paragraph))
        repeated_sentences = [sentence for sentence, count in Counter(sentences(texts)).items() if count > 1]
        if repeated_sentences:
            failures.append(f"#{number}: repeated long sentence: {repeated_sentences[0][:100]}")

        artworks = summary.get("chapterArtworks", {})
        if len(artworks) != 16:
            failures.append(f"#{number}: {len(artworks)} chapter artworks")
        local_hashes: set[str] = set()
        for item in artworks.values():
            path = ROOT / item["image"].lstrip("/")
            if not path.exists():
                failures.append(f"#{number}: missing {path.relative_to(ROOT)}")
                continue
            with Image.open(path) as image:
                if image.size != (720, 720):
                    failures.append(f"#{number}: {path.name} size {image.size}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest in local_hashes or digest in global_art:
                failures.append(f"#{number}: duplicate chapter artwork")
            local_hashes.add(digest)
            global_art[digest] = number

        cover = ROOT / summary["coverImage"].lstrip("/")
        if not cover.exists():
            failures.append(f"#{number}: cover missing")
        else:
            with Image.open(cover) as image:
                if image.size != (900, 1350):
                    failures.append(f"#{number}: cover size {image.size}")
            digest = hashlib.sha256(cover.read_bytes()).hexdigest()
            if digest in local_hashes:
                failures.append(f"#{number}: cover duplicates chapter artwork")
            if colorfulness(cover) < 35:
                failures.append(f"#{number}: cover colorfulness is too low")

        pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
        if not pdf_path.exists():
            failures.append(f"#{number}: PDF missing")
            continue
        reader = PdfReader(str(pdf_path))
        page_count = len(reader.pages)
        if not 25 <= page_count <= 50:
            failures.append(f"#{number}: {page_count} PDF pages")
        embedded: set[str] = set()
        sparse: list[int] = []
        for index, page in enumerate(reader.pages, 1):
            page_text = (page.extract_text() or "").strip()
            if index not in (1, 3) and len(page_text) < 180:
                sparse.append(index)
            for image in page.images:
                embedded.add(hashlib.sha256(image.data).hexdigest())
        if sparse:
            failures.append(f"#{number}: sparse pages {sparse}")
        if len(embedded) < 17:
            failures.append(f"#{number}: only {len(embedded)} unique embedded images")

        render_dir = render_root / str(number)
        renders = sorted(render_dir.glob("page-*.jpg"))
        if len(renders) != page_count:
            failures.append(f"#{number}: {len(renders)} renders for {page_count} pages")
        elif min(path.stat().st_mtime for path in renders) < pdf_path.stat().st_mtime:
            failures.append(f"#{number}: page renders are older than the final PDF")

        rows.append(
            f"#{number:03d} {characters:5d} chars · {page_count:2d} pages · "
            f"{len(embedded):2d} PDF images · {summary['title']}"
        )

    shared = {
        paragraph: sorted(set(locations))
        for paragraph, locations in exact_locations.items()
        if len(set(locations)) > 1
    }
    if shared:
        first, locations = next(iter(shared.items()))
        failures.append(f"{len(shared)} exact long paragraphs shared across books {locations}: {first[:100]}")

    # Whole-paragraph near duplicates catch disguised padding while ignoring the
    # deliberately short connective clauses in the common style system.
    fuzzy: list[tuple[int, int, float, str]] = []
    for index, (left_no, left) in enumerate(long_paragraphs):
        for right_no, right in long_paragraphs[index + 1:]:
            if left_no == right_no:
                continue
            if abs(len(left) - len(right)) > max(len(left), len(right)) * 0.18:
                continue
            ratio = SequenceMatcher(None, left, right, autojunk=False).ratio()
            if ratio >= 0.88:
                fuzzy.append((left_no, right_no, ratio, left[:90]))
    if fuzzy:
        failures.append(f"near-duplicate paragraphs detected: {fuzzy[0]}")

    print("\n".join(rows))
    print(
        f"\nWAVE: {len(numbers)} books · mean {statistics.mean(counts):.1f} chars · "
        f"min {min(counts)} · max {max(counts)} · {len(global_art)} unique chapter images · "
        f"exact shared paragraphs {len(shared)} · near duplicates {len(fuzzy)}"
    )
    if failures:
        print("\nFAILURES:\n" + "\n".join(f"- {failure}" for failure in failures))
        raise SystemExit(1)
    print("\nPASS: final-wave quality gate")


__all__ = ["run", "ROOT"]
