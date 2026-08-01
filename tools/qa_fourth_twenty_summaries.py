#!/usr/bin/env python3
"""Run the established strict quality gate on the fourth twenty-book batch."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (
    10, 14, 35, 47, 58, 64, 71, 91, 104, 110,
    139, 153, 165, 176, 191, 200, 218, 229, 254, 285,
)


if __name__ == "__main__":
    qa.main()
