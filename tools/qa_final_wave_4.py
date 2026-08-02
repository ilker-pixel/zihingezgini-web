#!/usr/bin/env python3
"""Run the strict gate for final wave four."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (219, 226, 227, 228, 230, 231, 232, 233, 234),
        ROOT / "tmp" / "final-wave-4-pdf-renders",
    )
