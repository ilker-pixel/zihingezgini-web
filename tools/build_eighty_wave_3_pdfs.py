#!/usr/bin/env python3
"""Build the third 80-book wave with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (25, 45, 77, 101, 146, 162, 196, 223, 136, 169)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "eighty-wave-3"


if __name__ == "__main__":
    repaired.builder.main()
