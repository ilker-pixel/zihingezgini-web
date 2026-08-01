#!/usr/bin/env python3
"""Build the second 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (23, 44, 74, 97, 140, 160, 192, 221, 120, 286)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-2"


if __name__ == "__main__":
    repaired.builder.main()
