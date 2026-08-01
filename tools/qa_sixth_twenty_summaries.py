#!/usr/bin/env python3
"""Run the established strict quality gate on the sixth twenty-book batch."""

import qa_next_twenty_summaries as qa


qa.BOOK_NUMBERS = (
    16, 20, 22, 39, 43, 67, 76, 85, 98, 108,
    135, 155, 161, 178, 184, 204, 212, 235, 255, 288,
)


if __name__ == "__main__":
    qa.main()
