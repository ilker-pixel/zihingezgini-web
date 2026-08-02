#!/usr/bin/env python3
"""Build the eighth 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (56, 54, 125, 116, 188, 168, 210, 259, 129, 150)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-8"


if __name__ == "__main__":
    repaired.builder.main()
