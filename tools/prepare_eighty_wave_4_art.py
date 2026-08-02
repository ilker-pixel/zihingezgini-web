#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the fourth 80-book wave."""

from pathlib import Path

import prepare_eighty_wave_3_art as base


ROOT = Path(__file__).resolve().parents[1]
base.TMP = ROOT / "tmp" / "eighty-wave-4"
base.SOURCES = {
    26: ("exec-e2f7474b-38a7-4d29-b6a6-d93df08255e0.png", "exec-27f76b14-8202-4b95-8107-7e9dfb97048d.png"),
    46: ("exec-0dd00724-6d26-498a-80d8-52faae8157ac.png", "exec-040d609d-aa0e-499d-a72b-3be92e00d478.png"),
    78: ("exec-dc326490-2e33-4cd2-86c9-329909f94b64.png", "exec-d6fd21de-e7a4-4b13-9fc7-9799f4f7b337.png"),
    105: ("exec-bbe68770-fa73-4f62-a19e-19417e2d24eb.png", "exec-46526c20-fde2-4acf-9811-c00e925db680.png"),
    147: ("exec-6fb9305d-fdb8-46b2-8b4c-a6be0321715f.png", "exec-64ed0d04-42c7-49f6-9bf0-85df71dd3cd5.png"),
    163: ("exec-cece1288-07a9-4aa5-b15c-d1eecb3deaf2.png", "exec-5618cf1b-b0e0-4be6-b325-e2c19680d68d.png"),
    197: ("exec-28e4867c-1272-4212-8926-a4453382f13b.png", "exec-f7c7e4fa-4b50-4542-a18f-bb52b078dc6f.png"),
    225: ("exec-24f4a851-9e47-4c26-9137-f525df3eb0d1.png", "exec-1f161a82-40e6-49c5-88a2-46804316d44b.png"),
    55: ("exec-b011a411-21de-48af-af8b-f8efbe305ed4.png", "exec-5ae7caa7-31a9-49d8-b1ad-9fdd1fae92e3.png"),
    242: ("exec-485e0f8a-829f-44b2-b091-815dfb475cc2.png", "exec-4a22e1dc-05fd-4f52-82aa-3c494ea20d62.png"),
}


if __name__ == "__main__":
    base.main()
    for old, new in (
        ("wave-3-covers-contact-sheet.jpg", "wave-4-covers-contact-sheet.jpg"),
        ("wave-3-chapter-art-master-contact-sheet.jpg", "wave-4-chapter-art-master-contact-sheet.jpg"),
    ):
        (base.TMP / old).replace(base.TMP / new)
