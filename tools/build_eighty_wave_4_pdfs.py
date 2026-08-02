#!/usr/bin/env python3
"""Build the fourth 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (26, 46, 78, 105, 147, 163, 197, 225, 55, 242)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-4"


if __name__ == "__main__":
    repaired.builder.main()
