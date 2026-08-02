#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave two."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    128: ("exec-508bbc63-2e30-4fd4-ad6d-9a5c95118ec8.png", "exec-7a3f3ea2-3199-425b-af93-16ad57b7a323.png"),
    131: ("exec-d9e06b86-acee-47dd-b390-019211e8b3a2.png", "exec-90892b97-63b0-48b8-8f2f-be598bdf8932.png"),
    132: ("exec-5e11d0e0-665f-418a-98d7-8e3ae33cab31.png", "exec-211cf263-07d4-4a69-8728-4fd4866f1ad6.png"),
    133: ("exec-be8f4038-b8f1-43fc-938d-f4848a8172cc.png", "exec-a4f54acf-6e39-4845-8af5-dd1d24804a74.png"),
    134: ("exec-48a01273-7d5e-4af7-9914-fc4bc9510d29.png", "exec-18d8883a-e6d2-427b-8e11-5e5055cdf653.png"),
    144: ("exec-fc7292bb-f745-4ccb-bad1-44f77aefb300.png", "exec-e840b813-6013-4e4a-b3a3-b871167aaed8.png"),
    148: ("exec-76d08ffe-c36e-41f8-896d-c67986b94377.png", "exec-3fbda197-cc2a-482b-9351-aa16cef1461c.png"),
    170: ("exec-93a3cfc7-cdc3-463e-a159-17d20c0012f9.png", "exec-71425b70-be16-496a-8aba-2989e7e17d88.png"),
    174: ("exec-4456623e-8efe-49ed-b046-6ae6914c4129.png", "exec-4d5ade10-7623-44c2-b106-60cd177c84bd.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-2-art", "final-wave-2")
