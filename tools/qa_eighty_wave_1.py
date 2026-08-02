#!/usr/bin/env python3
"""Run the strict quality gate on the first 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (21, 42, 69, 94, 137, 159, 190, 217, 118, 215)


if __name__ == "__main__":
    qa.main()
