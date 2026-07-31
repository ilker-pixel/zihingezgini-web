#!/usr/bin/env python3
"""Crop five ImageGen 4×4 sheets into final monochrome web assets."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "five-new-summaries"

SOURCES = {
    31: {
        "sheet": GENERATED / "exec-4749afb5-a366-467c-bcfe-f54881acd2ed.png",
        "cover": GENERATED / "exec-939814f5-2495-4304-a840-c22af2f7e40f.png",
    },
    88: {
        "sheet": GENERATED / "exec-2ba5f0d1-bda8-47ef-8211-23335d843a9f.png",
        "cover": GENERATED / "exec-6a6fea48-0bd5-4356-a518-0c24e313e7c7.png",
    },
    142: {
        "sheet": GENERATED / "exec-c6fe01bb-57fe-4b95-a3da-07c5a15290a1.png",
        "cover": GENERATED / "exec-e56ad741-814a-4f9b-b6d7-1da3ffaeaa3b.png",
    },
    213: {
        "sheet": GENERATED / "exec-2535d9ff-a010-4b3a-b2c1-f06169b9066e.png",
        "cover": GENERATED / "exec-58238393-21e7-4d96-9eae-a955418be0da.png",
    },
    287: {
        "sheet": GENERATED / "exec-ecc96615-d39e-41a0-a311-9a0139edc4ce.png",
        "cover": GENERATED / "exec-3efc2713-b025-45ff-ad96-6ba023f226f1.png",
    },
}

INKS = {
    31: "#355A78",
    88: "#754B4B",
    142: "#554D79",
    213: "#566148",
    287: "#976037",
}


def crop_cells(sheet: Image.Image) -> list[Image.Image]:
    # ImageGen's production sheets are 1254×1254 with ~8 px outer and 12 px gutters.
    # Crop conservatively inside each cell so no white separator leaks into the art.
    if sheet.size != (1254, 1254):
        raise ValueError(f"Unexpected sheet size: {sheet.size}")
    cells = []
    for row in range(4):
        for column in range(4):
            x = 8 + column * 312
            y = 8 + row * 312
            cells.append(sheet.crop((x, y, x + 300, y + 300)))
    return cells


def monochrome(cell: Image.Image, ink: str) -> Image.Image:
    gray = ImageOps.grayscale(cell)
    gray = ImageOps.autocontrast(gray, cutoff=(1, 1))
    gray = ImageEnhance.Contrast(gray).enhance(1.08)
    paper = "#EEE8DA"
    colored = ImageOps.colorize(gray, black=ink, white=paper)
    return colored.resize((720, 720), Image.Resampling.LANCZOS)


def make_contact_sheet(book_no: int, assets: list[Path]) -> None:
    thumbs = []
    for path in assets:
        with Image.open(path) as image:
            thumbs.append(ImageOps.contain(image.convert("RGB"), (210, 210)))
    canvas = Image.new("RGB", (4 * 220 + 20, 4 * 220 + 20), "#D9D3C6")
    for index, thumb in enumerate(thumbs):
        x = 10 + (index % 4) * 220 + (210 - thumb.width) // 2
        y = 10 + (index // 4) * 220 + (210 - thumb.height) // 2
        canvas.paste(thumb, (x, y))
    canvas.save(TMP / f"{book_no}-chapter-art-contact-sheet.jpg", quality=90)


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    cover_thumbs = []
    for book_no, sources in SOURCES.items():
        summary_path = ROOT / "data" / "summaries" / f"{book_no}.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")

        with Image.open(sources["sheet"]) as sheet:
            cells = crop_cells(sheet.convert("RGB"))
        for cell, output in zip(cells, artwork_paths, strict=True):
            output.parent.mkdir(parents=True, exist_ok=True)
            monochrome(cell, INKS[book_no]).save(output, "WEBP", quality=84, method=6)

        cover_output = ROOT / summary["coverImage"].lstrip("/")
        with Image.open(sources["cover"]) as cover:
            cover = ImageOps.fit(cover.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            cover = ImageEnhance.Contrast(cover).enhance(1.03)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            thumb = ImageOps.contain(cover, (270, 405))
            cover_thumbs.append((book_no, thumb.copy()))

        make_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (5 * 290 + 20, 435), "#D9D3C6")
    for index, (_book_no, thumb) in enumerate(cover_thumbs):
        cover_canvas.paste(thumb, (10 + index * 290 + (270 - thumb.width) // 2, 15))
    cover_canvas.save(TMP / "five-covers-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
