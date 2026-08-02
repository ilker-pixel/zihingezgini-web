#!/usr/bin/env python3
"""Render every page of a final wave and create per-book contact sheets."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]


def render(books: tuple[int, ...], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for no in books:
        pdfs = list((ROOT / "data" / "pdfs").glob(f"{no}-*.pdf"))
        if len(pdfs) != 1:
            raise RuntimeError(f"Book {no}: expected one PDF, found {len(pdfs)}")
        target = out / str(no)
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", "96", str(pdfs[0]), str(target / "page")],
            check=True,
        )
        pages = sorted(target.glob("page-*.jpg"))
        thumbs = []
        for page in pages:
            with Image.open(page) as image:
                thumbs.append(ImageOps.contain(image.convert("RGB"), (180, 255)).copy())
        columns = 5
        rows = (len(thumbs) + columns - 1) // columns
        canvas = Image.new("RGB", (columns * 188, rows * 264), "#C9C4BA")
        draw = ImageDraw.Draw(canvas)
        for index, thumb in enumerate(thumbs):
            x, y = (index % columns) * 188 + 4, (index // columns) * 264 + 4
            canvas.paste(thumb, (x, y))
            draw.text((x + 4, y + 238), str(index + 1), fill="#222222")
        canvas.save(out / f"{no}-all-pages.jpg", quality=90)
        print(f"{no}: {len(pages)} pages rendered")


__all__ = ["render", "ROOT"]
