#!/usr/bin/env python3
"""Run the strict gate for final wave seven."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (273, 274, 276, 278, 279, 280, 281, 282, 283),
        ROOT / "tmp" / "final-wave-7-pdf-renders",
    )
