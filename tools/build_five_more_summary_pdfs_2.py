#!/usr/bin/env python3
"""Build the five illustrated PDFs in this production batch."""

import build_five_summary_pdfs as base


base.BOOK_NUMBERS = (7, 36, 95, 185, 284)
base.TMP = base.ROOT / "tmp" / "pdfs" / "five-more-summaries-2"


if __name__ == "__main__":
    base.main()
