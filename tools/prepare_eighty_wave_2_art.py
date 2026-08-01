#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the second 80-book wave."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
TMP = ROOT / "tmp" / "eighty-wave-2"

# Each tuple is (exact 4x4 chapter sheet, independent portrait cover).
SOURCES = {
    23: ("exec-1f7dc513-a19e-4ea4-b03f-17e784a80393.png", "exec-81809a09-9796-465e-98af-a1a55b8e4483.png"),
    44: ("exec-e71e8157-9627-4999-a14c-129aab82dd08.png", "exec-e9a8dac0-2099-4302-b04d-6fcd11737ce3.png"),
    74: ("exec-7512f95a-33d9-44c2-be81-e2602fb63886.png", "exec-0f05f3d3-255f-4fa1-9aa9-c55bae1be527.png"),
    97: ("exec-388f1bd3-02d2-4c81-a96a-f14e30220e9d.png", "exec-259882bc-7a2c-4cf6-a8aa-b0ad97a7d46f.png"),
    140: ("exec-2d48b786-64b5-408e-bd7c-0fb34246475a.png", "exec-33677f8f-6057-4bfe-a591-56e5819f3a8c.png"),
    160: ("exec-2d2eca9d-4fde-4fab-8c44-b17e73d23a77.png", "exec-74a04d11-2c89-4848-8d2f-928c5047248c.png"),
    192: ("exec-fc962cdf-7a23-4416-9714-a28d6ca90abf.png", "exec-c453e0cc-182f-44aa-85f0-95631d05499b.png"),
    221: ("exec-0880fca2-78c5-414e-91c8-51842762b9c2.png", "exec-d7539578-c138-41a7-9f8e-ab9d52f81c2e.png"),
    120: ("exec-02844381-52b2-466f-a4ca-3a5c985280ef.png", "exec-1b0b0064-c947-45e6-a1f6-465df7c84994.png"),
    286: ("exec-32fbe4d6-0846-4a57-b5a3-36d36aafe743.png", "exec-bdddf4c5-bfef-4e59-96bf-c197df22bf91.png"),
}


def normalized_sheet(book_no: int, source: Image.Image) -> Image.Image:
    """Remove the one generator footer artifact before regular 4x4 cropping."""
    rgb = source.convert("RGB")
    if book_no == 140:
        rgb = rgb.crop((0, 0, rgb.width, 1180))
        rgb = ImageOps.fit(rgb, (1254, 1254), method=Image.Resampling.LANCZOS)
    return rgb


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
            prepared = normalized_sheet(book_no, sheet)
            if prepared.width != prepared.height:
                raise ValueError(f"Book {book_no} sheet is not square: {prepared.size}")
            cells = base.crop_cells(prepared)
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
    cover_canvas.save(TMP / "wave-2-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 452), "#D9D3C6")
    for index, book_no in enumerate(SOURCES):
        with Image.open(TMP / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(TMP / "wave-2-chapter-art-master-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
