#!/usr/bin/env python3
"""Prepare covers and 16 monochrome chapter images for the twenty-book batch."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "twenty-summaries"

SOURCES = {
    8: ("exec-f93a8a19-8fbc-44fb-87f3-cb6de451fcfb.png", "exec-ce16a63e-49ee-4211-9fba-07fd9a19b994.png"),
    18: ("exec-6da50387-318f-4a18-9287-742cb391a0ad.png", "exec-5b4af374-4811-471d-b168-2ad3333cfcf5.png"),
    34: ("exec-8e1ed1e1-eec5-43a3-abf7-18e75d2aac10.png", "exec-a33488f5-9cbb-4af5-a988-c7d3d632aba9.png"),
    38: ("exec-5a161f0a-7da8-4442-9992-36838dd0fb48.png", "exec-d69f09c5-21ed-48d5-b298-6c9cd25c7d40.png"),
    61: ("exec-40359113-3919-46ea-a695-e19be89b661a.png", "exec-fca10f60-a9f2-4f81-8e7b-706c31e564e8.png"),
    70: ("exec-f470364b-9344-41de-877c-eda9701a2b6a.png", "exec-d1bf24c8-6ea6-445c-887d-4d7bcda94d46.png"),
    92: ("exec-8cc80813-bd21-405d-beec-8bc3bfc7e000.png", "exec-eafc058d-d243-49df-bcb5-81297d2259b3.png"),
    99: ("exec-f29c0760-efb1-437c-b728-ef9e436c0033.png", "exec-3cc8a905-5633-4823-b3e5-5894086a1562.png"),
    121: ("exec-8626bccd-a3cb-42f8-8f9f-eec1baec9875.png", "exec-5d2e71ae-420d-47f3-ae58-1e9cbebdf0c0.png"),
    138: ("exec-e8679fd5-d0df-4874-bc60-e8ca92929133.png", "exec-d078d486-4723-4535-89a1-e17255787327.png"),
    151: ("exec-35d3b983-cd16-4b28-8c8c-c62bfbbcdbf5.png", "exec-911fc03e-4c8a-4f49-ab63-fd34912816f5.png"),
    157: ("exec-b6161ea2-39a5-490f-861a-b98603cafb2f.png", "exec-be500f19-c23a-4815-a748-ede8b5b078fc.png"),
    182: ("exec-7f5607c6-b448-442e-b2d3-f4a749bed4f0.png", "exec-082ef80b-7985-4770-94c1-9086dd416a43.png"),
    195: ("exec-1655c80a-42b0-4987-960c-88324bfd1a6a.png", "exec-7f73a8c8-5434-47d5-bb49-31b8b5d75b5f.png"),
    211: ("exec-af349c04-15a3-4f0e-9ba0-4358699d5582.png", "exec-63351414-2a69-4887-b437-2056dd76d8c2.png"),
    216: ("exec-c9b9a96c-bc07-403a-af30-4a1f2834dc73.png", "exec-d7c8f3c5-303b-4348-abed-d4d14bcbef79.png"),
    238: ("exec-17016b15-6ce8-4bb9-94a9-223049e1158b.png", "exec-9ba5311f-8c2b-4d9b-ad9f-3f62799bace4.png"),
    244: ("exec-36b01e5d-b02f-46c7-a103-5bee57252f71.png", "exec-e04906a9-c88a-4b38-adce-91fd7b0060ce.png"),
    266: ("exec-b3175342-39a9-41bf-a841-d1052bbb7bd2.png", "exec-4c12b0d7-e106-4f52-9c43-1f2b0d076aa0.png"),
    294: ("exec-a73cb3b5-589b-4cce-8cf4-41e24a046c5b.png", "exec-d076e304-f910-4684-8a21-b826a7b442cd.png"),
}


def crop_cells(sheet: Image.Image) -> list[Image.Image]:
    if sheet.width != sheet.height:
        raise ValueError(f"Expected square sheet, found {sheet.size}")

    gray = ImageOps.grayscale(sheet)

    def best_gutters(axis: str) -> list[int]:
        limit = gray.width if axis == "x" else gray.height
        gutters = [0]
        for index in range(1, 4):
            expected = round(index * limit / 4)
            candidates: list[tuple[float, int]] = []
            for position in range(expected - 24, expected + 25):
                strip = (
                    gray.crop((position, 0, position + 1, gray.height))
                    if axis == "x"
                    else gray.crop((0, position, gray.width, position + 1))
                )
                stats = ImageStat.Stat(strip)
                score = stats.mean[0] - 0.75 * stats.stddev[0]
                candidates.append((score, position))
            gutters.append(max(candidates)[1])
        gutters.append(limit)
        return gutters

    x_bounds = best_gutters("x")
    y_bounds = best_gutters("y")
    inset = max(4, round(sheet.width / 280))
    cells = []
    for row in range(4):
        for column in range(4):
            box = (
                x_bounds[column] + inset,
                y_bounds[row] + inset,
                x_bounds[column + 1] - inset,
                y_bounds[row + 1] - inset,
            )
            cells.append(ImageOps.fit(sheet.crop(box), (300, 300), method=Image.Resampling.LANCZOS))
    return cells


def monochrome(cell: Image.Image, ink: str) -> Image.Image:
    gray = ImageOps.grayscale(cell)
    gray = ImageOps.autocontrast(gray, cutoff=(1, 1))
    gray = ImageEnhance.Contrast(gray).enhance(1.07)
    return ImageOps.colorize(gray, black=ink, white="#EEE8DA").resize(
        (720, 720), Image.Resampling.LANCZOS
    )


def make_art_contact_sheet(book_no: int, paths: list[Path]) -> None:
    canvas = Image.new("RGB", (900, 900), "#D9D3C6")
    for index, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = ImageOps.contain(source.convert("RGB"), (210, 210))
        x = 10 + (index % 4) * 220 + (210 - thumb.width) // 2
        y = 10 + (index // 4) * 220 + (210 - thumb.height) // 2
        canvas.paste(thumb, (x, y))
    canvas.save(TMP / f"{book_no}-chapter-art-contact-sheet.jpg", quality=90)


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    cover_thumbs: list[Image.Image] = []

    for book_no, (sheet_name, cover_name) in SOURCES.items():
        summary_path = ROOT / "data" / "summaries" / f"{book_no}.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        sheet_path = GENERATED / sheet_name
        cover_path = GENERATED / cover_name
        if not sheet_path.exists() or not cover_path.exists():
            raise FileNotFoundError(f"Missing source art for book {book_no}")

        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")

        with Image.open(sheet_path) as sheet:
            cells = crop_cells(sheet.convert("RGB"))
        for cell, output in zip(cells, artwork_paths, strict=True):
            output.parent.mkdir(parents=True, exist_ok=True)
            monochrome(cell, summary["chapterArtColor"]).save(output, "WEBP", quality=84, method=6)

        cover_output = ROOT / summary["coverImage"].lstrip("/")
        with Image.open(cover_path) as source:
            cover = ImageOps.fit(source.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            cover = ImageEnhance.Contrast(cover).enhance(1.03)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            cover_thumbs.append(ImageOps.contain(cover, (162, 243)).copy())

        make_art_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (880, 1032), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(TMP / "twenty-covers-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
