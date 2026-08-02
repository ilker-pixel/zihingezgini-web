#!/usr/bin/env python3
"""Build the seventh 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (29, 53, 123, 114, 187, 167, 209, 258, 57, 245)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-7"


if __name__ == "__main__":
    repaired.builder.main()
