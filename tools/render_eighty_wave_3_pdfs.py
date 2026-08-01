#!/usr/bin/env python3
"""Render every page of wave 3 PDFs and build compact contact sheets."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageOps, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tmp" / "eighty-wave-3-pdf-renders"
BOOKS = (25, 45, 77, 101, 146, 162, 196, 223, 136, 169)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for no in BOOKS:
        pdf = next((ROOT / "data" / "pdfs").glob(f"{no}-*.pdf"))
        target = OUT / str(no)
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-jpeg", "-r", "72", str(pdf), str(target / "page")], check=True)
        pages = sorted(target.glob("page-*.jpg"))
        thumbs = []
        for page in pages:
            with Image.open(page) as im:
                thumbs.append(ImageOps.contain(im.convert("RGB"), (150, 212)).copy())
        cols = 5
        rows = (len(thumbs) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * 158, rows * 220), "#C9C4BA")
        draw = ImageDraw.Draw(canvas)
        for i, thumb in enumerate(thumbs):
            x = (i % cols) * 158 + 4
            y = (i // cols) * 220 + 4
            canvas.paste(thumb, (x, y))
            draw.text((x + 4, y + 194), str(i + 1), fill="#222222")
        canvas.save(OUT / f"{no}-all-pages.jpg", quality=88)
        print(f"{no}: {len(pages)} pages rendered")


if __name__ == "__main__":
    main()
