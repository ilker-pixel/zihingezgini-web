#!/usr/bin/env python3
"""Create the next five illustrated 25-50 page summary PDFs."""

from __future__ import annotations

import json

from pypdf import PdfReader

import build_five_summary_pdfs as base


BOOK_NUMBERS = (2, 60, 81, 143, 243)


def main() -> None:
    base.register_fonts()
    base.PDF_DIR.mkdir(parents=True, exist_ok=True)
    base.TMP = base.ROOT / "tmp" / "pdfs" / "next-five-summaries"
    base.TMP.mkdir(parents=True, exist_ok=True)
    for number in BOOK_NUMBERS:
        summary = json.loads(
            (base.ROOT / "data" / "summaries" / f"{number}.json").read_text(encoding="utf-8")
        )
        path = base.PdfBook(summary).build()
        reader = PdfReader(str(path))
        words = sum(len((page.extract_text() or "").split()) for page in reader.pages)
        print(f"{path.relative_to(base.ROOT)}: {len(reader.pages)} pages, {words} extracted words")


if __name__ == "__main__":
    main()
