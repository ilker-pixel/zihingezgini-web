#!/usr/bin/env python3
"""Prepare covers and 16 chapter images for the fifth 80-book wave."""

from pathlib import Path

import prepare_eighty_wave_3_art as base


ROOT = Path(__file__).resolve().parents[1]
base.TMP = ROOT / "tmp" / "eighty-wave-5"
base.SOURCES = {
    27: ("exec-263b92ab-aeb2-4238-b852-09a83d04c1db.png", "exec-3c3f756e-c06e-4619-a54a-d1f64a412d26.png"),
    49: ("exec-3ddac17d-f7ca-4ce8-89c6-88f30c80cecd.png", "exec-eb29d2af-133b-40e6-9a91-d6a6b3931c49.png"),
    80: ("exec-1173526b-2d61-4e91-b97e-4f5143c21f6c.png", "exec-5cd28769-9c4c-46b6-9b10-24e79513d153.png"),
    106: ("exec-a4813d0e-c724-4a10-9a0f-a978d51d251e.png", "exec-bf97ea2f-767c-4d55-ac0a-3f12e5af0555.png"),
    181: ("exec-5bbdfce3-1513-4c5f-a7ec-5c951e026a88.png", "exec-d64e069d-9424-48ab-b4a3-9774eeba7041.png"),
    164: ("exec-b73121cb-64e0-4b60-9e14-00c29c3a11fc.png", "exec-97224813-e8df-4640-a9c4-63caee755156.png"),
    201: ("exec-ee64f289-c950-49cc-9f41-30acd2ab50a4.png", "exec-3a0ae774-bd38-4141-8b5e-28ee51804484.png"),
    251: ("exec-8124140c-9b3f-49c4-b7bc-f50886574d88.png", "exec-1a479ff7-403f-4ae2-9c46-4960769041fd.png"),
    126: ("exec-b318c910-3539-480f-b250-368f195f3ffd.png", "exec-8c6c9bc6-e5e0-4407-a9b9-fa3903b28bf4.png"),
    293: ("exec-a039a8f2-0365-4c1a-9107-9798cd05227c.png", "exec-d4a71827-1984-4ea7-bee0-d3eaf08adc0a.png"),
}


if __name__ == "__main__":
    base.main()
    for old, new in (
        ("wave-3-covers-contact-sheet.jpg", "wave-5-covers-contact-sheet.jpg"),
        ("wave-3-chapter-art-master-contact-sheet.jpg", "wave-5-chapter-art-master-contact-sheet.jpg"),
    ):
        (base.TMP / old).replace(base.TMP / new)
