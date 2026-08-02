#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave three."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    175: ("exec-a614bdb9-6dac-4062-9149-048e8f424f7e.png", "exec-36cf9662-83a0-4bb5-abab-3ca942d4b19b.png"),
    177: ("exec-cce310bb-75fe-451e-a0e4-4251ec723862.png", "exec-58c9e872-1b5d-4f03-9070-d62ffe16442e.png"),
    180: ("exec-af165da2-8c4d-4568-9570-f196d61d7207.png", "exec-859408bd-ca81-45b3-aa87-7d174521a850.png"),
    198: ("exec-b5448a5b-db9b-4f17-b7e9-118ce762df6b.png", "exec-f813fa18-8960-485d-8ca0-a7ea2b94fa4e.png"),
    202: ("exec-4de1520a-d8c7-4d0a-9d35-aecb972f968c.png", "exec-52e8c2e0-0d40-4669-ab22-2f1c47896354.png"),
    203: ("exec-c303b468-5e76-4499-b627-5aad1385622e.png", "exec-43c257c4-4c87-4fcc-8a1e-7bcc3d3af3b1.png"),
    206: ("exec-1e478418-99b7-44d6-84cc-d0f88282b794.png", "exec-51599b4d-701d-4aa4-8014-e9467a2b7ca9.png"),
    207: ("exec-369ac217-8950-4e6f-9073-b9c0ee864f43.png", "exec-e11f7e2c-030b-4882-a530-8f1ee118ecec.png"),
    208: ("exec-04764621-6167-4436-af72-21b3848f2e12.png", "exec-b2e697d1-108f-4993-a6a1-24ba50df7991.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-3-art", "final-wave-3")
