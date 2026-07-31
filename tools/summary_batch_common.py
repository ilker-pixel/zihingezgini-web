#!/usr/bin/env python3
"""Shared helpers for long-form Zihin Gezgini summary batches."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "summaries"


def slugify(value: str) -> str:
    table = str.maketrans({
        "ç": "c", "Ç": "c", "ğ": "g", "Ğ": "g", "ı": "i", "İ": "i",
        "ö": "o", "Ö": "o", "ş": "s", "Ş": "s", "ü": "u", "Ü": "u",
    })
    normalized = unicodedata.normalize("NFKD", value.translate(table))
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return re.sub(r"[^a-zA-Z0-9]+", "-", normalized.lower()).strip("-")


def entry(title: str, paragraphs: list[str], section: str, *, art: str = "", caption: str = "") -> dict:
    return {"title": title, "paragraphs": paragraphs, "section": section, "art": art, "caption": caption}


def assemble(source: dict) -> dict:
    book = dict(source)
    raw_entries = book.pop("entries")
    chapters = []
    artworks = {}
    art_index = 0
    for index, raw in enumerate(raw_entries, 1):
        chapter_id = f"durak-{index:02d}-{slugify(raw['title'])}"
        chapters.append({
            "id": chapter_id,
            "section": raw["section"],
            "title": raw["title"],
            "paragraphs": raw["paragraphs"],
        })
        if raw.get("art"):
            art_index += 1
            image = f"/images/summary-art-{book['bookNo']}-chapter-{art_index:02d}-{raw['art']}-v1.webp"
            artworks[chapter_id] = {"image": image, "imageCaption": raw["caption"]}
    if art_index != 16:
        raise ValueError(f"Book {book['bookNo']} has {art_index} artworks; expected 16")
    book["chapters"] = chapters
    book["chapterArtworks"] = artworks
    return book


def write_books(books: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source in books:
        summary = assemble(source)
        target = OUT / f"{summary['bookNo']}.json"
        target.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        words = sum(len(p.split()) for c in summary["chapters"] for p in c["paragraphs"])
        print(f"{summary['bookNo']}: {len(summary['chapters'])} durak, {words} kelime, 16 görsel")
