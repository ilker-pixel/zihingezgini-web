#!/usr/bin/env python3
"""Create compact visual-QA sheets from representative pages of all sixth-batch PDFs."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
RENDERS = ROOT / "tmp" / "sixth-twenty-pdf-renders"
OUT = ROOT / "tmp" / "sixth-twenty-summaries"
BOOKS = (16, 20, 22, 39, 43, 67, 76, 85, 98, 108, 135, 155, 161, 178, 184, 204, 212, 235, 255, 288)


def page_number(path: Path) -> int:
    return int(path.stem.rsplit("-", 1)[1])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for group_index in range(4):
        canvas = Image.new("RGB", (1440, 1260), "#2B2B2B")
        draw = ImageDraw.Draw(canvas)
        for row, book_no in enumerate(BOOKS[group_index * 5 : group_index * 5 + 5]):
            pages = sorted((RENDERS / str(book_no)).glob("page-*.png"), key=page_number)
            wanted = (1, 2, 3, 4, 8, 14, 20, len(pages))
            for column, number in enumerate(wanted):
                with Image.open(pages[number - 1]) as source:
                    thumb = ImageOps.contain(source.convert("RGB"), (170, 228))
                x = 5 + column * 180 + (170 - thumb.width) // 2
                y = 18 + row * 250 + (228 - thumb.height) // 2
                canvas.paste(thumb, (x, y))
                draw.text((x, y - 13), f"#{book_no} p{number}", fill="#FFFFFF")
        canvas.save(OUT / f"sixth-twenty-pdf-contact-{group_index + 1}.jpg", quality=90)


if __name__ == "__main__":
    main()
