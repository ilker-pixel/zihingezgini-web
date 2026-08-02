#!/usr/bin/env python3
"""Run the strict quality gate on the fifth 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (27, 49, 80, 106, 181, 164, 201, 251, 126, 293)


if __name__ == "__main__":
    qa.main()
