#!/usr/bin/env python3
"""Run the strict gate for final wave five."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (236, 237, 246, 247, 249, 250, 252, 257, 260),
        ROOT / "tmp" / "final-wave-5-pdf-renders",
    )
