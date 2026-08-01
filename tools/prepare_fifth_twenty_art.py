#!/usr/bin/env python3
"""Prepare independent covers and 16 chapter images for the fifth twenty-book batch."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "fifth-twenty-summaries"

# Each tuple is (exact 4x4 interior sheet, independent full-color cover).
SOURCES = {
    15: ("exec-ba2fbdc6-bf02-474f-ba0f-ab5997a32394.png", "exec-092998b2-cb46-42df-879f-2a1e6e882f16.png"),
    19: ("exec-cef2eeff-7193-4c27-abff-621afe985a0c.png", "exec-0e26c972-2080-477b-9388-a7447dd16772.png"),
    24: ("exec-c625c27d-9c7e-41a0-9e58-48b587d8c98b.png", "exec-c4971afe-d807-4dea-8eaf-0500b08c1acb.png"),
    40: ("exec-7b19b914-4fb2-483d-b8bd-b0970283ace4.png", "exec-2943c470-a959-46d6-8557-7674bf178c25.png"),
    48: ("exec-35af65cf-4d1e-462f-925e-2e438ce417ad.png", "exec-8ef032fa-f18d-49c4-9433-a1b4f23ff4e2.png"),
    59: ("exec-949ebccb-533f-41eb-81ca-3b8e1cc88d37.png", "exec-ac2e4fa3-c660-445c-9102-dbb81a04e2fc.png"),
    65: ("exec-80bacc16-66e1-44a6-a9c1-c077ae0ca48f.png", "exec-394c1671-0607-45ec-9395-f91dfa58a6e7.png"),
    73: ("exec-d98c3125-dfb3-49ec-83f7-24666683c9fe.png", "exec-014a2d4e-16eb-4269-924d-675d7813d205.png"),
    82: ("exec-f4165bab-4d01-42c4-b897-6306af35f17c.png", "exec-5a9a7712-3e77-4219-a888-f48a17d81a11.png"),
    96: ("exec-c17b4e5b-78aa-4fee-a6fb-f994a5f45c16.png", "exec-fbc618ff-c7b4-4904-9ed9-397d9edf091c.png"),
    109: ("exec-5aae9f92-1831-47e1-b0c0-678006327414.png", "exec-2d9cf8d3-8cfc-449b-8574-8b70604d75ab.png"),
    127: ("exec-531cec94-63b0-491a-a01d-0e511e3ef249.png", "exec-c897c12a-5ad3-407e-8a33-2615ae31e09c.png"),
    141: ("exec-282b9fb4-d7b3-4e8e-a4ca-832e4d257b70.png", "exec-78d3a8c8-519c-4241-ba98-fba5864c653b.png"),
    154: ("exec-ed97a36a-80a7-43d6-870e-4de95e06b9b6.png", "exec-c14fbcf6-d079-4fae-9ce5-b42b2b971cff.png"),
    173: ("exec-61dd903c-eba2-444d-bfb7-f3b8378b6f0b.png", "exec-23e6a788-a7dc-4d73-bdcb-f6716f75e036.png"),
    193: ("exec-b37e419d-aa83-4695-b374-f0b1f70087ca.png", "exec-da553d71-385d-42d0-a2dd-cabfbd2b215a.png"),
    220: ("exec-52792352-a8bf-479c-baa9-097e16b07895.png", "exec-1a3dd498-0d70-4069-8149-963ebc5075df.png"),
    240: ("exec-91fc1e62-7301-4870-acbd-3397de612496.png", "exec-139c86bd-c55b-4f5d-8183-2b00119d59c0.png"),
    263: ("exec-a836d998-eb2e-459d-895d-5d450478d2bb.png", "exec-0a8e5ca1-994e-484c-ae16-1ef7054d8ff8.png"),
    290: ("exec-4c65905b-982a-461f-a70a-93b8a27a5ba2.png", "exec-6da5294a-7f7d-4132-88bb-24249751bd6e.png"),
}


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    base.TMP = TMP
    cover_thumbs: list[Image.Image] = []

    for book_no, (sheet_name, cover_name) in SOURCES.items():
        summary = json.loads((ROOT / "data" / "summaries" / f"{book_no}.json").read_text(encoding="utf-8"))
        sheet_path = GENERATED / sheet_name
        cover_path = GENERATED / cover_name
        if not sheet_path.exists() or not cover_path.exists():
            raise FileNotFoundError(f"Missing source art for book {book_no}")

        artwork_paths = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artwork_paths) != 16:
            raise ValueError(f"Book {book_no} must have exactly 16 artwork paths")

        with Image.open(sheet_path) as sheet:
            cells = base.crop_cells(sheet.convert("RGB"))
        for cell, output in zip(cells, artwork_paths, strict=True):
            output.parent.mkdir(parents=True, exist_ok=True)
            base.monochrome(cell, summary["chapterArtColor"]).save(output, "WEBP", quality=84, method=6)

        cover_output = ROOT / summary["coverImage"].lstrip("/")
        cover_output.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(cover_path) as source:
            cover = ImageOps.fit(source.convert("RGB"), (900, 1350), method=Image.Resampling.LANCZOS)
            cover = ImageEnhance.Contrast(cover).enhance(1.03)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            cover_thumbs.append(ImageOps.contain(cover, (162, 243)).copy())

        base.make_art_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (880, 1032), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(TMP / "fifth-twenty-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 900), "#D9D3C6")
    for index, book_no in enumerate(SOURCES):
        with Image.open(TMP / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(TMP / "fifth-twenty-chapter-art-master-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
