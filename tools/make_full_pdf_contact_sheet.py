#!/usr/bin/env python3
"""Create one compact, numbered visual-QA sheet for every rendered PDF directory."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


parser = argparse.ArgumentParser()
parser.add_argument("source", type=Path)
args = parser.parse_args()


def page_number(path: Path) -> int:
    match = re.search(r"(\d+)$", path.stem)
    return int(match.group(1)) if match else 0


source = args.source
pages = sorted(source.glob("page-*.png"), key=page_number)
if not pages:
    raise SystemExit(f"No rendered pages in {source}")

columns = 5
thumb_width = 180
margin = 8
label_height = 17
with Image.open(pages[0]) as first:
    thumb_height = round(thumb_width * first.height / first.width)
rows = math.ceil(len(pages) / columns)
canvas = Image.new(
    "RGB",
    (
        columns * thumb_width + (columns + 1) * margin,
        rows * (thumb_height + label_height) + (rows + 1) * margin,
    ),
    "#D9D3C6",
)
draw = ImageDraw.Draw(canvas)
for index, path in enumerate(pages):
    with Image.open(path) as source_image:
        page = ImageOps.contain(source_image.convert("RGB"), (thumb_width, thumb_height))
    row, column = divmod(index, columns)
    x = margin + column * (thumb_width + margin)
    y = margin + row * (thumb_height + label_height)
    canvas.paste(page, (x, y))
    draw.text((x + 2, y + thumb_height + 2), f"{index + 1:02d}", fill="#202020")

target = source / "full-contact-sheet.jpg"
canvas.save(target, quality=91)
print(target)
