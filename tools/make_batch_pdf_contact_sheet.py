#!/usr/bin/env python3
"""Combine per-PDF contact sheets into one compact batch overview."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
BOOKS = (12, 17, 32, 41, 66, 72, 93, 103, 122, 124, 152, 156, 189, 194, 214, 222, 241, 253, 271, 275)
SOURCE = ROOT / "tmp" / "visual-qa-twenty-more"
TARGET = SOURCE / "twenty-more-pdf-contact-sheets.jpg"


canvas = Image.new("RGB", (1220, 1540), "#D2CDC1")
draw = ImageDraw.Draw(canvas)
for index, number in enumerate(BOOKS):
    path = SOURCE / str(number) / "full-contact-sheet.jpg"
    with Image.open(path) as source:
        thumb = ImageOps.contain(source.convert("RGB"), (290, 285))
    row, column = divmod(index, 4)
    x = 10 + column * 302
    y = 28 + row * 302
    canvas.paste(thumb, (x + (290 - thumb.width) // 2, y))
    draw.text((x + 4, y - 18), f"#{number}", fill="#24282B")
canvas.save(TARGET, quality=92)
print(TARGET)
