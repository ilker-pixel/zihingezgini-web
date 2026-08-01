#!/usr/bin/env python3
"""Build the fourth twenty-book batch with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (
    10, 14, 35, 47, 58, 64, 71, 91, 104, 110,
    139, 153, 165, 176, 191, 200, 218, 229, 254, 285,
)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "fourth-twenty"


if __name__ == "__main__":
    repaired.builder.main()
