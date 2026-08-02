#!/usr/bin/env python3
"""Run the strict quality gate on the eighth 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (56, 54, 125, 116, 188, 168, 210, 259, 129, 150)


if __name__ == "__main__":
    qa.main()
