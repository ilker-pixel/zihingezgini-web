#!/usr/bin/env python3
"""Build the sixth twenty-book batch with the established natural-flow layout."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (
    16, 20, 22, 39, 43, 67, 76, 85, 98, 108,
    135, 155, 161, 178, 184, 204, 212, 235, 255, 288,
)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "sixth-twenty"


if __name__ == "__main__":
    repaired.builder.main()
