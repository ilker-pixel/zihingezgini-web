#!/usr/bin/env python3
"""Prepare independent covers and 16 chapter images for the fourth twenty-book batch."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

import prepare_twenty_summary_art as base


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "fourth-twenty-summaries"

# Each tuple is (4x4 interior sheet, independent full-color cover).
SOURCES = {
    10: ("exec-6be6020e-6ab0-4104-9a1a-8c9f8f4fcaa7.png", "exec-e53a0521-10ca-4276-afb4-67f27bf7536c.png"),
    14: ("exec-1c8db963-8b17-4637-a019-11a1784311a9.png", "exec-c56bd35f-e699-4a43-9788-81df90411881.png"),
    35: ("exec-dec29aa9-f612-45ae-ae74-e592ac77f855.png", "exec-2be4b439-84bf-4d7a-b857-39b03e0552d9.png"),
    47: ("exec-8be89aaa-ab2c-4c00-9f07-e2e82640bc35.png", "exec-5cbd4a2f-06df-45f0-89de-bd19396446de.png"),
    58: ("exec-f509bff7-3ade-4061-b24e-48097358e653.png", "exec-7dbe2662-1299-4e80-b0cc-59abbb133525.png"),
    64: ("exec-864637e1-0136-4646-b29a-3149d0c3a60d.png", "exec-d4e296b5-464b-4b78-8970-68e2d21c815f.png"),
    71: ("exec-f286c003-06ec-42b6-b059-3b54174d886a.png", "exec-73591a23-a4cd-4346-b71e-d67639e35c05.png"),
    91: ("exec-9b5ce649-6414-49dc-8357-9011b188a25f.png", "exec-92481fd8-dedd-4ae2-9a6a-df553983eac3.png"),
    104: ("exec-694fb33b-3347-48da-93b7-683300fd77fc.png", "exec-3c1991c2-10d8-4404-83f8-bb720115923c.png"),
    110: ("exec-87dc2e01-c682-4e31-9ed4-616b3bf10f7c.png", "exec-00cf487b-e58e-4a1a-be5c-460c81e29b25.png"),
    139: ("exec-f1ad91eb-131b-4243-8dfa-d13ea6403291.png", "exec-fde63f4a-90e1-43af-8796-1dca12da4c72.png"),
    153: ("exec-12875dae-177a-4a31-9de2-a6a563f46401.png", "exec-8963449a-98f1-42d0-9756-0d841476a2a2.png"),
    165: ("exec-9b6d5a84-ec94-41e6-b7f3-2b9b584ea343.png", "exec-656ab235-7f15-4243-b030-0e52df269f8b.png"),
    176: ("exec-b26dbe8d-a75c-436a-90d7-4bdf3dcd15b7.png", "exec-ec8f6b06-758e-4ffe-a9c5-8f61d4d3081b.png"),
    191: ("exec-1fd39297-048f-44ae-ac3b-ec059a284ff5.png", "exec-dfc58629-ce85-4d2a-9ba1-e42bef51c33e.png"),
    200: ("exec-a06a99bb-65d9-48cd-93b7-e3b977318b68.png", "exec-d1bc691b-5fe7-4eac-9313-1866835ad6c4.png"),
    218: ("exec-dbdf247a-8330-4a56-aae9-9f80908f6e96.png", "exec-ff122096-a2e4-4011-a011-7bc1f729b8e7.png"),
    229: ("exec-4b07cf4c-a04d-48de-8d03-2a50ab0e6601.png", "exec-bf0e8d40-a45e-491e-98dc-62aa5a54071f.png"),
    254: ("exec-2cf6391b-b1a3-4c55-a3c5-80a360e70ef0.png", "exec-c251f47c-a884-437f-a5a4-4967ab5fa82d.png"),
    285: ("exec-9ce5bbaf-69bf-4d89-a3e3-048ba254da2e.png", "exec-8f76d938-7f5d-4cea-977a-fc6a78bf0c17.png"),
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
    cover_canvas.save(TMP / "fourth-twenty-covers-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
