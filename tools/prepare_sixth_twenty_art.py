#!/usr/bin/env python3
"""Prepare independent covers and 16 chapter images for the sixth twenty-book batch."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "sixth-twenty-summaries"

# Each tuple is (exact 4x4 interior sheet, independent full-color cover).
SOURCES = {
    16: ("exec-25574422-4373-42d7-a8d7-d682f48ef819.png", "exec-1d968fa0-985d-47b1-9b0a-cf34f8b52a7b.png"),
    20: ("exec-4324f89c-531e-4cbe-88a3-3302fb851fdf.png", "exec-b93723e2-5000-4653-94fb-6385005bae0c.png"),
    22: ("exec-8e671a81-50bc-4ae1-871d-4c067f03a46d.png", "exec-a85a124c-6e2a-4856-8c5f-eb602ba6bac2.png"),
    39: ("exec-7601da31-5e49-410d-a98b-7a7f7ebace88.png", "exec-1acb7e5f-7cc2-4334-a28b-b6104f215226.png"),
    43: ("exec-2f5fad7e-a7e0-4925-83ec-e15e024b2647.png", "exec-4276db06-e77d-4a19-9b16-51d337d9c6eb.png"),
    67: ("exec-cbfb0537-38e1-4c85-9dd0-ae8097b4826b.png", "exec-1f01dc15-c24e-4ae2-80ad-70ea358aa57d.png"),
    76: ("exec-0c65f8a9-b150-4c11-9409-b27e1e8b9ffc.png", "exec-b07c6b6a-8743-4b8b-93dd-705aca76957c.png"),
    85: ("exec-2fe87521-c2bc-410c-9797-b6888763104f.png", "exec-4f602469-4618-41a2-b1c6-0f665432a92d.png"),
    98: ("exec-2785b42b-66ab-4781-a769-be2dd6a66b11.png", "exec-095c4fff-0111-4f24-987f-72f17cd231ad.png"),
    108: ("exec-e18df1ad-4f9f-45b7-885f-244ecd103d43.png", "exec-298c0a17-c767-4086-be9a-dddb9c1b3c3f.png"),
    135: ("exec-0af0feb6-eeeb-4575-b212-b44ca9325351.png", "exec-8e950ff1-8bb0-42e2-9be7-a708f96512be.png"),
    155: ("exec-0a43bc91-79fd-4ca2-99e4-e57e75c1a1e1.png", "exec-33bc72af-1bd2-4216-859a-2b543a48af2e.png"),
    161: ("exec-ea0a47eb-6376-4b70-a8bc-05aab7de0183.png", "exec-8ab920f5-edb4-40be-bc24-2dd16d3cad50.png"),
    178: ("exec-d614f53e-b508-4c0c-99a2-1d0319bcdd35.png", "exec-86143b4b-a74a-40c2-842e-581a31d42bb3.png"),
    184: ("exec-25e66660-0770-4ca8-91ef-6591331dd001.png", "exec-3bd8d7ee-d5a3-4d41-b4ed-d7836cd130cd.png"),
    204: ("exec-b66552bb-06ac-4cf4-a1bc-1a55084bc9d1.png", "exec-be93cd5f-8e05-4aa3-9642-8b235741658a.png"),
    212: ("exec-05ad2c01-efc0-47f1-ab7c-8bcfeb8db8dd.png", "exec-e2ca4a04-94b2-4514-bae5-2c77c4898ef0.png"),
    235: ("exec-23e6e645-21f4-4af1-be5f-d8d48818761f.png", "exec-974e1df6-1271-4266-9db8-a8f3b46ee39e.png"),
    255: ("exec-f64e94f4-4d52-4c72-adb0-a68ef437c428.png", "exec-8e50ec7c-071d-4276-b77a-b5e53a0aeaa4.png"),
    288: ("exec-27ce5879-d0ce-488c-b078-4cbec8d6ee1b.png", "exec-052b14b3-c76d-43b6-99d2-8284952ac003.png"),
}


def main() -> None:
    if len(SOURCES) != 20:
        raise RuntimeError(f"Expected 20 art pairs, found {len(SOURCES)}")
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
            if book_no in {108, 212}:
                cover = ImageEnhance.Color(cover).enhance(1.75)
            cover.save(cover_output, "WEBP", quality=88, method=6)
            cover_thumbs.append(ImageOps.contain(cover, (162, 243)).copy())

        base.make_art_contact_sheet(book_no, artwork_paths)
        print(f"{book_no}: 16 chapter images + cover")

    cover_canvas = Image.new("RGB", (880, 1032), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        x = 8 + (index % 5) * 174 + (162 - thumb.width) // 2
        y = 8 + (index // 5) * 256 + (243 - thumb.height) // 2
        cover_canvas.paste(thumb, (x, y))
    cover_canvas.save(TMP / "sixth-twenty-covers-contact-sheet.jpg", quality=92)

    art_canvas = Image.new("RGB", (1120, 900), "#D9D3C6")
    for index, book_no in enumerate(SOURCES):
        with Image.open(TMP / f"{book_no}-chapter-art-contact-sheet.jpg") as source:
            thumb = ImageOps.fit(source.convert("RGB"), (216, 216), method=Image.Resampling.LANCZOS)
        x = 4 + (index % 5) * 224
        y = 4 + (index // 5) * 224
        art_canvas.paste(thumb, (x, y))
    art_canvas.save(TMP / "sixth-twenty-chapter-art-master-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
