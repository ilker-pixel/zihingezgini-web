#!/usr/bin/env python3
"""Prepare one nine-book final wave from 4x4 sheets and portrait covers."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")


def prepare(sources: dict[int, tuple[str, str]], tmp: Path, label: str) -> None:
    if len(sources) != 9:
        raise RuntimeError(f"{label}: expected nine art pairs, found {len(sources)}")
    tmp.mkdir(parents=True, exist_ok=True)
    base.TMP = tmp
    cover_thumbs: list[Image.Image] = []

    for book_no, (sheet_name, cover_name) in sources.items():
        summary = json.loads(
            (ROOT / "data" / "summaries" / f"{book_no}.json").read_text(encoding="utf-8")
        )
        sheet_path, cover_path = GENERATED / sheet_name, GENERATED / cover_name
        if not sheet_path.exists() or not cover_path.exists():
            raise FileNotFoundError(f"Missing source art for book {book_no}")
        artwork_paths = [ROOT / value["image"].lstrip("/") for value in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly sixteen artwork paths")

        with Image.open(sheet_path) as source:
            sheet = ImageOps.fit(source.convert("RGB"), (1254, 1254), method=Image.Resampling.LANCZOS)
            cells = base.crop_cells(sheet)
        for cell, output in zip(cells, artwork_paths, strict=True):
            output.parent.mkdir(parents=True, exist_ok=True)
            base.monochrome(cell, summary["chapterArtColor"]).save(
                output, "WEBP", quality=84, method=6
            )

        cover_output = ROOT / summary["coverImage"].lstrip("/")
        cover_output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(cover_path) as source:
            cover = ImageOps.fit(source.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            cover = ImageEnhance.Contrast(cover).enhance(1.03)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            cover_thumbs.append(ImageOps.contain(cover, (162, 243)).copy())

        base.make_art_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: sixteen chapter images plus independent cover")

    cover_canvas = Image.new("RGB", (880, 520), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(tmp / f"{label}-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 452), "#D9D3C6")
    for index, book_no in enumerate(sources):
        with Image.open(tmp / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(tmp / f"{label}-chapter-art-master-contact-sheet.jpg", quality=92)


__all__ = ["prepare"]
