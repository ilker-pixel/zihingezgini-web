#!/usr/bin/env python3
"""Structural, text-density, duplication and asset QA for the twenty summaries."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOKS = (8, 18, 34, 38, 61, 70, 92, 99, 121, 138, 151, 157, 182, 195, 211, 216, 238, 244, 266, 294)
FORBIDDEN = {"\ufffd": "replacement character", "\u2011": "non-breaking hyphen", "\u2013": "en dash", "\u2014": "em dash"}
WORD_RE = re.compile(r"[^\W_]+", re.UNICODE)


def words(value: str) -> list[str]:
    return WORD_RE.findall(value.casefold())


def iter_prose(summary: dict) -> list[str]:
    chunks = [summary.get("intro", "")]
    for chapter in summary["chapters"]:
        chunks.extend(chapter["paragraphs"])
    chunks.extend(item.get("title", "") for item in summary.get("sources", []))
    return chunks


def duplicate_sentences(chunks: list[str]) -> list[str]:
    sentences = []
    for chunk in chunks:
        for sentence in re.split(r"(?<=[.!?])\s+", chunk.strip()):
            normalized = " ".join(words(sentence))
            if len(normalized.split()) >= 12:
                sentences.append(normalized)
    return [sentence for sentence, count in Counter(sentences).items() if count > 1]


def main() -> None:
    errors: list[str] = []
    rows: list[str] = []

    for number in BOOKS:
        summary_path = ROOT / "data" / "summaries" / f"{number}.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary["bookNo"] != number:
            errors.append(f"{number}: wrong bookNo")

        prose = iter_prose(summary)
        all_text = "\n".join(prose)
        for character, label in FORBIDDEN.items():
            if character in all_text:
                errors.append(f"{number}: contains {label}")
        duplicates = duplicate_sentences(prose)
        if duplicates:
            errors.append(f"{number}: duplicate long sentences: {duplicates[:3]}")

        artworks = list(summary["chapterArtworks"].values())
        art_paths = [ROOT / artwork["image"].lstrip("/") for artwork in artworks]
        if len(artworks) != 16 or len(set(art_paths)) != 16:
            errors.append(f"{number}: artwork count/path uniqueness failure")
        hashes = []
        for path in art_paths:
            if not path.exists():
                errors.append(f"{number}: missing artwork {path}")
                continue
            with Image.open(path) as image:
                if image.size != (720, 720):
                    errors.append(f"{number}: artwork has wrong size {path.name}: {image.size}")
            hashes.append(hashlib.sha256(path.read_bytes()).hexdigest())
        if len(hashes) != len(set(hashes)):
            errors.append(f"{number}: duplicate artwork files")

        cover = ROOT / summary["coverImage"].lstrip("/")
        if not cover.exists():
            errors.append(f"{number}: missing cover")
        else:
            with Image.open(cover) as image:
                if image.size != (900, 1350):
                    errors.append(f"{number}: cover has wrong size {image.size}")

        pdf_path = ROOT / summary["pdfUrl"].lstrip("/")
        if not pdf_path.exists():
            errors.append(f"{number}: missing PDF")
            continue
        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)
        if not 25 <= pages <= 50:
            errors.append(f"{number}: {pages} PDF pages")
        page_words = [len(words(page.extract_text() or "")) for page in reader.pages]
        if page_words[0] < 25:
            errors.append(f"{number}: cover text too sparse ({page_words[0]} words)")
        sparse_body = [index + 1 for index, count in enumerate(page_words[1:], 1) if count < 65]
        if sparse_body:
            errors.append(f"{number}: sparse body pages {sparse_body}")
        for index, page in enumerate(reader.pages, 1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            if abs(width - 595.276) > 1 or abs(height - 841.89) > 1:
                errors.append(f"{number}: page {index} is not A4 ({width}x{height})")
        extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        if "\ufffd" in extracted:
            errors.append(f"{number}: replacement character in PDF text")

        rows.append(
            f"{number:03d} | {pages:02d} pages | {sum(page_words):4d} words | "
            f"body min {min(page_words[1:]):3d} | 16 unique images"
        )

    print("\n".join(rows))
    if errors:
        print("\nERRORS")
        print("\n".join(f"- {error}" for error in errors))
        raise SystemExit(1)
    print("\nQA PASSED: 20 PDFs, 320 unique chapter assets, 20 covers")


if __name__ == "__main__":
    main()
