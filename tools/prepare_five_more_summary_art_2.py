#!/usr/bin/env python3
"""Prepare covers and 16 chapter illustrations for five more summaries."""

from pathlib import Path

import prepare_next_five_summary_art as base
from PIL import Image, ImageOps


GENERATED = Path("/Users/ilker/.codex/generated_images/019f9da1-066e-7b33-a57d-6f3ce25d234e")

base.SOURCES = {
    7: {
        "sheet": GENERATED / "exec-7b62dd1d-8d1e-4ca8-9ab5-d67d1c8f9400.png",
        "cover": GENERATED / "exec-72a68aaf-0a1e-4199-9d53-a4e50e5bfb01.png",
    },
    36: {
        "sheet": GENERATED / "exec-e44ef457-d15d-4591-a19d-3970bf883cda.png",
        "cover": GENERATED / "exec-901fc8dc-cbe9-4540-9006-70b86a75b547.png",
    },
    95: {
        "sheet": GENERATED / "exec-6ce5801f-2534-4b33-a389-b45b0d08aea0.png",
        "cover": GENERATED / "exec-d2fa33c4-3828-4030-a24c-2185f645732c.png",
    },
    185: {
        "sheet": GENERATED / "exec-5a8d1644-e223-4d8a-811b-5dce9ad60753.png",
        "cover": GENERATED / "exec-1e0e7e3e-29c8-4ab8-9eb6-7392709e8259.png",
    },
    284: {
        "sheet": GENERATED / "exec-ba8e49c8-ec06-4702-8572-a78f44f9224a.png",
        "cover": GENERATED / "exec-11fd4588-6545-4b91-9c74-bfb6a2c5e42d.png",
    },
}

base.INKS = {
    7: "#4F6B4C",
    36: "#72515C",
    95: "#774D3E",
    185: "#3E6770",
    284: "#7B5848",
}

base.TMP = base.ROOT / "tmp" / "five-more-summaries-2"


def crop_equal_cells(sheet: Image.Image) -> list[Image.Image]:
    """Crop reliable 4x4 cells from the exact square ImageGen sheets."""
    if sheet.size != (1254, 1254):
        raise ValueError(f"Unexpected sheet size: {sheet.size}")
    bounds = [round(index * sheet.width / 4) for index in range(5)]
    cells = []
    for row in range(4):
        for column in range(4):
            left, right = bounds[column], bounds[column + 1]
            top, bottom = bounds[row], bounds[row + 1]
            # Drop the generated grid stroke/gutter without trimming scene content.
            inset = 3
            cell = sheet.crop((left + inset, top + inset, right - inset, bottom - inset))
            cells.append(ImageOps.fit(cell, (300, 300), method=Image.Resampling.LANCZOS))
    return cells


base.crop_cells = crop_equal_cells


if __name__ == "__main__":
    base.main()
