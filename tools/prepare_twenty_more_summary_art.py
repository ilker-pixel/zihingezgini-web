#!/usr/bin/env python3
"""Crop twenty 4x4 AI sheets into chapter art and derive matching covers."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from prepare_twenty_summary_art import crop_cells, monochrome


ROOT = Path(__file__).resolve().parents[1]
GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")
IMAGES = ROOT / "images"
TMP = ROOT / "tmp" / "twenty-more-summaries"

SOURCES = {
    12: "exec-efffac7f-d961-47ba-9a8f-a3add6c42644.png",
    17: "exec-c7d2df43-5d76-41ef-9228-aef42a5623a7.png",
    32: "exec-63141c92-6cd2-4f3c-96a0-770962080f85.png",
    41: "exec-76de08b3-6263-4171-8ed9-1a5b1642e485.png",
    66: "exec-3daa8c8c-1cfd-4435-ae07-3a2a161e48c4.png",
    72: "exec-f8db8fdc-22e0-4d01-8725-34e3e22a68d1.png",
    93: "exec-0b527030-15d2-4fc5-b6ff-a7604d412976.png",
    103: "exec-43a00f25-8250-4541-a45a-64b14d531fea.png",
    122: "exec-2587f575-ebb9-4e19-9a62-5fb7dac612e5.png",
    124: "exec-b8368ebc-e688-4ef8-affb-80aa721d1b2a.png",
    152: "exec-b4e90155-cc70-4ad8-9c45-477031ed4471.png",
    156: "exec-14865b51-833f-4984-90cd-97d3929af927.png",
    189: "exec-e66bfdf3-beb6-4211-9fe1-f84691461dfe.png",
    194: "exec-baee29a0-d15e-4acf-8e2e-059c182ba4a2.png",
    214: "exec-c48de580-bbed-43c1-a291-2b6c64f31778.png",
    222: "exec-8cb7e397-b8df-4f67-a32b-6ec6f405f285.png",
    241: "exec-3f2208ee-ef69-4806-8606-b8908d76f64d.png",
    253: "exec-d98f4900-a994-4c69-9988-697c1b1aaae9.png",
    271: "exec-218bd95d-e61c-478b-9e6b-93c7ba9349eb.png",
    275: "exec-1ca20b38-e70e-4d20-a422-4eaf2dfe6728.png",
}


def make_contact(paths: list[Path], output: Path) -> None:
    canvas = Image.new("RGB", (900, 900), "#D9D3C6")
    for index, path in enumerate(paths):
        with Image.open(path) as source:
            thumb = ImageOps.fit(source.convert("RGB"), (210, 210), Image.Resampling.LANCZOS)
        x = 10 + (index % 4) * 220
        y = 10 + (index // 4) * 220
        canvas.paste(thumb, (x, y))
    canvas.save(output, quality=90)


def make_cover(cell: Image.Image, ink: str) -> Image.Image:
    paper = "#EEE8DA"
    cover = Image.new("RGB", (900, 1350), paper)
    art = monochrome(cell, ink).resize((900, 900), Image.Resampling.LANCZOS)
    cover.paste(art, (0, 225))
    draw = ImageDraw.Draw(cover)
    draw.rectangle((0, 0, 900, 22), fill=ink)
    draw.rectangle((0, 1328, 900, 1350), fill=ink)
    draw.rectangle((35, 190, 865, 198), fill=ink)
    draw.rectangle((35, 1152, 865, 1160), fill=ink)
    return cover


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    cover_thumbs = []
    sheet_thumbs = []

    for number, filename in SOURCES.items():
        summary = json.loads((ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8"))
        source_path = GENERATED / filename
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        with Image.open(source_path) as source:
            sheet = source.convert("RGB")
            cells = crop_cells(sheet)
            sheet_thumbs.append(ImageOps.contain(sheet, (240, 240)))

        artworks = [ROOT / item["image"].lstrip("/") for item in summary["chapterArtworks"].values()]
        if len(artworks) != 16:
            raise ValueError(f"{number}: expected 16 artwork targets")
        for cell, target in zip(cells, artworks, strict=True):
            target.parent.mkdir(parents=True, exist_ok=True)
            monochrome(cell, summary["chapterArtColor"]).save(target, "WEBP", quality=84, method=6)

        cover_target = ROOT / summary["coverImage"].lstrip("/")
        cover = make_cover(cells[0], summary["chapterArtColor"])
        cover.save(cover_target, "WEBP", quality=88, method=6)
        cover_thumbs.append(ImageOps.contain(cover, (162, 243)))
        make_contact(artworks, TMP / f"{number}-chapter-art-contact-sheet.jpg")
        print(f"{number}: 16 chapter images + cover")

    covers = Image.new("RGB", (880, 1032), "#D9D3C6")
    for index, thumb in enumerate(cover_thumbs):
        covers.paste(thumb, (8 + (index % 5) * 174, 8 + (index // 5) * 256))
    covers.save(TMP / "twenty-more-covers-contact-sheet.jpg", quality=92)

    sheets = Image.new("RGB", (1020, 1020), "#D9D3C6")
    for index, thumb in enumerate(sheet_thumbs):
        sheets.paste(thumb, (10 + (index % 4) * 250, 10 + (index // 4) * 250))
    sheets.save(TMP / "twenty-more-source-sheets-contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
