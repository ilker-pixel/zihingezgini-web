#!/usr/bin/env python3
"""Crop the next five ImageGen 4x4 sheets into final monochrome web assets."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "next-five-summaries"

SOURCES = {
    2: {
        "sheet": GENERATED / "exec-845fa147-3142-4bd4-b044-80c8b235adca.png",
        "cover": GENERATED / "exec-6178e5a2-3e51-456a-8554-c6a50f0ce411.png",
    },
    60: {
        "sheet": GENERATED / "exec-4132c93e-fbd0-4acf-b28c-a547c515deac.png",
        "cover": GENERATED / "exec-3d13b002-0b15-4124-901e-5ef7667de677.png",
    },
    81: {
        "sheet": GENERATED / "exec-3946bcbd-b01d-4af9-ad16-bf763256d7c6.png",
        "cover": GENERATED / "exec-09d8b986-9b50-41b8-89ba-e7551b0f2cd8.png",
    },
    143: {
        "sheet": GENERATED / "exec-01886a08-d5ab-48b7-8b38-5736430d018f.png",
        "cover": GENERATED / "exec-c1e4a64a-275d-494a-96e6-5de48b749672.png",
    },
    243: {
        "sheet": GENERATED / "exec-4254868c-0852-48ec-9f6c-3a7b1d886883.png",
        "cover": GENERATED / "exec-f4425de9-fcdd-4478-97a9-7346b6968a8f.png",
    },
}

INKS = {
    2: "#315B68",
    60: "#8A4F58",
    81: "#6C5536",
    143: "#3F4A54",
    243: "#665078",
}


def crop_cells(sheet: Image.Image) -> list[Image.Image]:
    """Detect and crop the 16 cells while excluding irregular ivory separators."""
    if sheet.size != (1254, 1254):
        raise ValueError(f"Unexpected sheet size: {sheet.size}")

    gray = ImageOps.grayscale(sheet)

    def separator_groups(axis: str) -> list[tuple[int, int]]:
        values = []
        limit = gray.height if axis == "y" else gray.width
        for position in range(limit):
            strip = (
                gray.crop((0, position, gray.width, position + 1))
                if axis == "y"
                else gray.crop((position, 0, position + 1, gray.height))
            )
            stats = ImageStat.Stat(strip)
            if stats.mean[0] > 230 and stats.stddev[0] < 10:
                values.append(position)
        groups: list[list[int]] = []
        for position in values:
            if not groups or position > groups[-1][-1] + 1:
                groups.append([position])
            else:
                groups[-1].append(position)
        result = [(group[0], group[-1]) for group in groups]
        if len(result) != 5:
            raise ValueError(f"Expected five {axis}-axis separator bands, found {result}")
        return result

    x_bands = separator_groups("x")
    y_bands = separator_groups("y")
    cells = []
    for row in range(4):
        for column in range(4):
            left = x_bands[column][1] + 1
            right = x_bands[column + 1][0]
            top = y_bands[row][1] + 1
            bottom = y_bands[row + 1][0]
            cell = sheet.crop((left, top, right, bottom))
            cells.append(ImageOps.fit(cell, (300, 300), method=Image.Resampling.LANCZOS))
    return cells


def monochrome(cell: Image.Image, ink: str) -> Image.Image:
    gray = ImageOps.grayscale(cell)
    gray = ImageOps.autocontrast(gray, cutoff=(1, 1))
    gray = ImageEnhance.Contrast(gray).enhance(1.08)
    colored = ImageOps.colorize(gray, black=ink, white="#EEE8DA")
    return colored.resize((720, 720), Image.Resampling.LANCZOS)


def make_contact_sheet(book_no: int, assets: list[Path]) -> None:
    thumbs = []
    for path in assets:
        with Image.open(path) as image:
            thumbs.append(ImageOps.contain(image.convert("RGB"), (210, 210)))
    canvas = Image.new("RGB", (900, 900), "#D9D3C6")
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
        for kind, source in sources.items():
            if not source.exists():
                raise FileNotFoundError(f"Missing {kind} source for book {book_no}: {source}")

        summary = json.loads((ROOT / "data" / "summaries" / f"{book_no}.json").read_text(encoding="utf-8"))
        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")
        if summary["chapterArtColor"].upper() != INKS[book_no]:
            raise ValueError(f"Book {book_no} ink color does not match summary metadata")

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
            cover_thumbs.append(ImageOps.contain(cover, (270, 405)).copy())

        make_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (1470, 435), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        cover_canvas.paste(thumb, (10 + index * 290 + (270 - thumb.width) // 2, 15))
    cover_canvas.save(TMP / "five-covers-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
