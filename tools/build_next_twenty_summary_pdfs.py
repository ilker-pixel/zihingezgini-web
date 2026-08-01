#!/usr/bin/env python3
"""Build the third twenty-book batch with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (
    9, 33, 37, 50, 62, 63, 68, 75, 79, 87,
    89, 100, 107, 111, 145, 158, 172, 183, 199, 239,
)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "next-twenty"


if __name__ == "__main__":
    repaired.builder.main()
