#!/usr/bin/env python3
"""Build the fifth 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (27, 49, 80, 106, 181, 164, 201, 251, 126, 293)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-5"


if __name__ == "__main__":
    repaired.builder.main()
