#!/usr/bin/env python3
"""Run structural, density, duplication and asset QA for the second batch."""

import qa_twenty_summaries as qa


qa.BOOKS = (
    12, 17, 32, 41, 66,
    72, 93, 103, 122, 124,
    152, 156, 189, 194, 214,
    222, 241, 253, 271, 275,
)


if __name__ == "__main__":
    qa.main()
