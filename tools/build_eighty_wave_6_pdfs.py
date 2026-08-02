#!/usr/bin/env python3
"""Build the sixth 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (28, 51, 86, 112, 186, 166, 205, 256, 149, 171)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-6"


if __name__ == "__main__":
    repaired.builder.main()
