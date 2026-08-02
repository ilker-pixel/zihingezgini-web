#!/usr/bin/env python3
"""Run the strict gate for final wave eight."""

from qa_final_wave import ROOT, run


if __name__ == "__main__":
    run(
        (289, 291, 292, 295, 296, 297, 298, 299, 300),
        ROOT / "tmp" / "final-wave-8-pdf-renders",
    )
