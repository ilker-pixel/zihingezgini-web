#!/usr/bin/env python3
"""Build the twenty illustrated summaries with the established PDF renderer."""

from pathlib import Path

import build_five_summary_pdfs as builder


builder.BOOK_NUMBERS = (
    8, 18, 34, 38, 61,
    70, 92, 99, 121, 138,
    151, 157, 182, 195, 211,
    216, 238, 244, 266, 294,
)
builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "twenty-summaries"


if __name__ == "__main__":
    builder.main()
