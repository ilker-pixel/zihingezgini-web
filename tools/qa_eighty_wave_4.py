#!/usr/bin/env python3
"""Run the strict quality gate on the fourth 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (26, 46, 78, 105, 147, 163, 197, 225, 55, 242)


if __name__ == "__main__":
    qa.main()
