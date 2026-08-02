#!/usr/bin/env python3
"""Run the strict quality gate on the third 80-book wave."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (25, 45, 77, 101, 146, 162, 196, 223, 136, 169)


if __name__ == "__main__":
    qa.main()
