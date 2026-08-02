#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the sixth 80-book wave."""

from pathlib import Path

import prepare_eighty_wave_3_art as base


ROOT = Path(__file__).resolve().parents[1]
base.TMP = ROOT / "tmp" / "eighty-wave-6"
base.SOURCES = {
    28: ("exec-c6586ab6-c456-4b1d-b9e0-5845b0e8d3e6.png", "exec-f4c67e0d-0c8b-433c-9f57-c9942bf71c1e.png"),
    51: ("exec-e40b0ee0-c314-4650-9b3a-c21974fd920d.png", "exec-f3caf145-9275-4e34-b813-87f6510509a8.png"),
    86: ("exec-f589ce82-7bd8-46eb-8465-e876605de4e0.png", "exec-4632332c-3ea5-40c5-8e94-43b2ba7b43b1.png"),
    112: ("exec-4987168b-0d61-4ecc-8b5c-9f757016e930.png", "exec-77a4e7d7-d613-4cfb-82a7-8dc1d1c0d03d.png"),
    186: ("exec-9ab7774b-7d12-4fed-afcd-88f19caef2fb.png", "exec-bc5e3ea5-b0b3-417d-a379-a00ede819084.png"),
    166: ("exec-93d7f44e-fa99-4a22-a65c-c79a88c163ee.png", "exec-fec8eb2b-c25c-4218-9f13-0c476a73f372.png"),
    205: ("exec-ededc52f-1e86-44d0-89f8-9db5dcc4cde7.png", "exec-c07507f5-358a-4d1b-a7de-e8fd56ec7fcc.png"),
    256: ("exec-caeba3b5-4c4f-436e-8a34-1bda524a518e.png", "exec-df223dd5-2f44-4fdc-a6e5-266dec856f75.png"),
    149: ("exec-a9711711-0a59-443c-ab72-c981b50d379b.png", "exec-422264d9-f76d-4999-a75b-2d2378e4c13f.png"),
    171: ("exec-0c0ade82-3152-4c22-8084-9a7d736349c0.png", "exec-4421e7c5-26e1-4def-8617-fe3519529b75.png"),
}


if __name__ == "__main__":
    base.main()
    for old, new in (
        ("wave-3-covers-contact-sheet.jpg", "wave-6-covers-contact-sheet.jpg"),
        ("wave-3-chapter-art-master-contact-sheet.jpg", "wave-6-chapter-art-master-contact-sheet.jpg"),
    ):
        (base.TMP / old).replace(base.TMP / new)
