#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the third 80-book wave."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
TMP = ROOT / "tmp" / "eighty-wave-3"

# Each tuple is (exact 4x4 chapter sheet, independent portrait cover).
SOURCES = {
    25: ("exec-360abd33-57ff-4fc3-a583-7c2a232deb3a.png", "exec-06273c0b-f790-4fae-a100-1f95fefccbbc.png"),
    45: ("exec-93e132e5-3952-4083-b658-51ba5dfca684.png", "exec-d2e896ba-2e04-46a3-8ccf-c8f747353f2b.png"),
    77: ("exec-50d3f8c5-41eb-43d7-9c0f-b16299281433.png", "exec-76e851e3-80d2-4457-8311-4eb2dd5ef306.png"),
    101: ("exec-ef746f68-e2dc-4eee-a05f-eec278f552e0.png", "exec-9b1e7fe3-1179-4d16-a9d6-500422f03115.png"),
    146: ("exec-b66265c5-6b6b-4737-8f2b-9fd4eecd18ed.png", "exec-4674f3e7-91ab-432a-88e0-30b4ff6b93b6.png"),
    162: ("exec-c1591816-c87b-4c79-b10f-10f21092ceba.png", "exec-58da5a84-481e-4508-b2d2-6f189a75de2c.png"),
    196: ("exec-48cad52e-5d72-42eb-8edc-a86ac613badc.png", "exec-62dc3281-840c-4019-807c-a00ad0d07ebb.png"),
    223: ("exec-f6857e56-b6c9-4159-833f-c34c10d1ec1f.png", "exec-88a9f08b-73b2-4b83-b8c3-39555caf325f.png"),
    136: ("exec-45bdaff6-3b7e-4a3b-81d0-8eaa7db2684f.png", "exec-08545580-a2b0-42f8-94eb-023c90c557db.png"),
    169: ("exec-da6cf044-df27-4bea-b1e6-33710b425a2b.png", "exec-2bcdd6c5-13bf-45a5-b938-2e4bdd68b354.png"),
}


def main() -> None:
    if len(SOURCES) != 10:
        raise RuntimeError(f"Expected 10 art pairs, found {len(SOURCES)}")
    TMP.mkdir(parents=True, exist_ok=True)
    base.TMP = TMP
    cover_thumbs: list[Image.Image] = []

    for book_no, (sheet_name, cover_name) in SOURCES.items():
        summary = json.loads(
            (ROOT / "data" / "summaries" / f"{book_no}.json").read_text(encoding="utf-8")
        )
        sheet_path = GENERATED / sheet_name
        cover_path = GENERATED / cover_name
        if not sheet_path.exists() or not cover_path.exists():
            raise FileNotFoundError(f"Missing source art for book {book_no}")

        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")

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
        print(f"{book_no}: 16 chapter images + independent cover")

    cover_canvas = Image.new("RGB", (880, 520), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(TMP / "wave-3-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 452), "#D9D3C6")
    for index, book_no in enumerate(SOURCES):
        with Image.open(TMP / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(TMP / "wave-3-chapter-art-master-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
