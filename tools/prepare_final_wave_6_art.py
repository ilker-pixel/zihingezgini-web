#!/usr/bin/env python3
"""Prepare the nine covers and 144 chapter images for final wave six."""

from prepare_final_wave_art import ROOT, prepare


SOURCES = {
    261: ("exec-019fb4fa-8281-4499-bf73-a81084904b66.png", "exec-601313db-de21-4742-b8e2-b983f4ef050b.png"),
    262: ("exec-01a6870a-ea6e-488e-87ed-2501b2bfd5e3.png", "exec-7d02d2b4-0974-4176-92f1-d84f2c1e2492.png"),
    264: ("exec-cd621302-7795-48b9-9c4b-3d63d8d3ff76.png", "exec-054cc466-46eb-450c-8a8e-5a86bec0c667.png"),
    265: ("exec-6541992e-3c9d-4b58-a0de-508cc3ba7427.png", "exec-27d3fbd6-f90a-46e4-8257-a8a4a97fd043.png"),
    267: ("exec-96b05c4c-9a00-46cd-bd3a-f6312f449cc6.png", "exec-b029e121-150e-4b6f-9de0-1bdeb29f9e71.png"),
    268: ("exec-b9afb80a-cf7f-4305-822a-0bf5409ce0a5.png", "exec-c1b31f43-d142-4765-862c-caf7c700d70b.png"),
    269: ("exec-26989ec7-8a4c-4a1d-91ea-cca968c86f93.png", "exec-6cd4ffde-d71d-4e21-84bf-5c0cfba0f6a0.png"),
    270: ("exec-5f34c23c-63f4-4667-8142-d243838e4752.png", "exec-b5f8df91-cec1-46e7-9735-c0dfd010a64f.png"),
    272: ("exec-fdac80e4-abcd-43cb-91da-9cb23f937b11.png", "exec-8bc76046-a74c-4c98-a8e3-766fb53e51ba.png"),
}


if __name__ == "__main__":
    prepare(SOURCES, ROOT / "tmp" / "final-wave-6-art", "final-wave-6")
