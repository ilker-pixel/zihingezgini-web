#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave five."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    236: ("exec-d3e3a66c-6c08-4992-ab8e-98708e54b37a.png", "exec-c01cae27-950c-4fc2-a49e-45bf7472400a.png"),
    237: ("exec-ddf6c3a5-5b44-4b89-8ea7-a9fa79b339e1.png", "exec-e1a115dd-c06e-4ec6-94fb-6b865fa25c4e.png"),
    246: ("exec-4ff9b7a3-3da5-4679-a113-bf9b5c771f6d.png", "exec-47aa8ded-7b63-4a65-8cf9-c82a31fddc9b.png"),
    247: ("exec-30801fef-27b9-4512-9b09-fa1cbe1e0feb.png", "exec-94538ada-ca6f-4306-8a47-e7e34e21f996.png"),
    249: ("exec-8363bde8-0437-4010-9a9b-592ea9678717.png", "exec-8e24c80d-b190-4c38-aee8-30188ac52a08.png"),
    250: ("exec-53b85aa6-28f3-4d0c-a9f8-5eea2b1221bf.png", "exec-955fd205-75d1-4b70-9611-2790410a1a4c.png"),
    252: ("exec-5cb0914f-5a80-45c9-a3dd-ea8a7adea5a2.png", "exec-ef56eafb-f078-4e60-bde0-306699a9ab9e.png"),
    257: ("exec-332e1118-d7f0-4c79-9c68-47a2178899ef.png", "exec-11d3f51f-a0cd-4d2b-befb-3e919a25d61f.png"),
    260: ("exec-972a34e5-a641-4375-bb3e-d62fc9bfc14d.png", "exec-bc1d447b-e00e-4772-b75c-4ca5bf1d47a4.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-5-art", "final-wave-5")
