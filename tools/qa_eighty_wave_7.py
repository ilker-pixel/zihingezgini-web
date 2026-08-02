#!/usr/bin/env python3
"""Run the strict quality gate on the seventh 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (29, 53, 123, 114, 187, 167, 209, 258, 57, 245)


if __name__ == "__main__":
    qa.main()
