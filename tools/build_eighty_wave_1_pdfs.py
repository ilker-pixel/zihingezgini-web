#!/usr/bin/env python3
"""Build the first 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (21, 42, 69, 94, 137, 159, 190, 217, 118, 215)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-1"


if __name__ == "__main__":
    repaired.builder.main()
