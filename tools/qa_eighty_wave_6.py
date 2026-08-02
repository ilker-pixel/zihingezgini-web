#!/usr/bin/env python3
"""Run the strict quality gate on the sixth 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (28, 51, 86, 112, 186, 166, 205, 256, 149, 171)


if __name__ == "__main__":
    qa.main()
