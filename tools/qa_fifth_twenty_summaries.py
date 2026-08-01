#!/usr/bin/env python3
"""Run the established strict quality gate on the fifth twenty-book batch."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (
    15, 19, 24, 40, 48, 59, 65, 73, 82, 96,
    109, 127, 141, 154, 173, 193, 220, 240, 263, 290,
)


if __name__ == "__main__":
    qa.main()
