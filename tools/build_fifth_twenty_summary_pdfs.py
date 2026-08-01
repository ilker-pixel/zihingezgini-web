#!/usr/bin/env python3
"""Build the fifth twenty-book batch with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (
    15, 19, 24, 40, 48, 59, 65, 73, 82, 96,
    109, 127, 141, 154, 173, 193, 220, 240, 263, 290,
)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "fifth-twenty"


if __name__ == "__main__":
    repaired.builder.main()
