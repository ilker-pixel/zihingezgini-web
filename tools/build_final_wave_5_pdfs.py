#!/usr/bin/env python3
"""Build the nine visually rich PDFs for final wave five."""

from pathlib import Path

import build_repaired_forty_summary_pdfs as repaired


repaired.builder.BOOK_NUMBERS = (236, 237, 246, 247, 249, 250, 252, 257, 260)
repaired.builder.TMP = Path(__file__).resolve().parents[1] / "tmp" / "pdfs" / "final-wave-5"


if __name__ == "__main__":
    repaired.builder.main()
