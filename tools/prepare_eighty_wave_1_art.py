#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the first 80-book wave."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
TMP = ROOT / "tmp" / "eighty-wave-1"

# Each tuple is (exact 4x4 chapter sheet, independent portrait cover).
SOURCES = {
    21: ("exec-d0b17f69-cadd-4f93-962c-b8a32a11432a.png", "exec-a0b92e25-9f6f-48fc-8720-641b711f90a7.png"),
    42: ("exec-d971ecfa-0c35-46e1-b099-f12682b7ff7d.png", "exec-2d029703-529a-4bba-a7ad-87c0ec11c73a.png"),
    69: ("exec-0fe13d98-05f0-4623-85b4-327c27280578.png", "exec-7893e71e-ddac-408b-8d23-a49d051ccbf1.png"),
    94: ("exec-93f12eb5-e594-4a43-aac1-4ef72b23c733.png", "exec-ff4fb260-c0ba-4f0c-8831-0fd7785ec0ce.png"),
    137: ("exec-93bc09ce-bfff-4574-9520-018b2a012c26.png", "exec-9f3cee1e-33f5-4f2c-b388-7b51c9f1fef8.png"),
    159: ("exec-ab948cf1-9491-485f-8b83-4be90559e8d7.png", "exec-4f5ebd71-8364-4e66-8bde-57f3fae030fe.png"),
    190: ("exec-3d927c8b-9ac9-4afd-a992-36fee5e69983.png", "exec-2cd1f714-c81f-47b9-88bd-69f6631b0a92.png"),
    217: ("exec-8da274a8-6890-4628-99de-f35a990a60b6.png", "exec-d21f47a4-e550-42cb-9e5a-7d30aa432453.png"),
    118: ("exec-f2fee4e8-38ff-42a7-93f2-b1ce692734ac.png", "exec-525d08ba-e7ff-4ba1-977f-59eb58dff90c.png"),
    215: ("exec-50fb5c0b-4e45-4153-a616-faf89ddce660.png", "exec-ce01e42a-36e6-46ea-b0ed-f85295eb269d.png"),
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

        with Image.open(sheet_path) as sheet:
            if sheet.width != sheet.height:
                raise ValueError(f"Book {book_no} sheet is not square: {sheet.size}")
            cells = base.crop_cells(sheet.convert("RGB"))
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
    cover_canvas.save(TMP / "wave-1-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 452), "#D9D3C6")
    for index, book_no in enumerate(SOURCES):
        with Image.open(TMP / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(TMP / "wave-1-chapter-art-master-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
