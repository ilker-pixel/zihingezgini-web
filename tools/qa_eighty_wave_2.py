#!/usr/bin/env python3
"""Run the strict quality gate on the second 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (23, 44, 74, 97, 140, 160, 192, 221, 120, 286)


if __name__ == "__main__":
    qa.main()
