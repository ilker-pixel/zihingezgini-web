#!/usr/bin/env python3
"""Apply the approved 12-phase pedagogical route without changing stable book ids."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKS_PATH = ROOT / "data/books.json"

PHASES = (
    (58, 142, 144, 6, 143, 36, 49, 89, 2, 3, 13, 275, 244, 11, 32, 53, 31, 37, 33, 42, 50, 60, 62, 68, 286),
    (1, 4, 145, 146, 147, 5, 258, 293, 10, 7, 9, 8, 15, 12, 16, 18, 19, 20, 21, 252, 291, 30, 288, 17, 287),
    (35, 40, 41, 277, 240, 34, 51, 52, 46, 47, 43, 44, 45, 57, 255, 294, 38, 54, 39, 276, 55, 56, 59, 88, 239),
    (61, 63, 64, 65, 66, 69, 67, 75, 70, 71, 73, 74, 76, 72, 79, 80, 82, 84, 271, 273, 272, 77, 78, 87, 110),
    (274, 121, 125, 126, 127, 122, 123, 124, 128, 129, 130, 131, 132, 133, 85, 86, 263, 90, 260, 262, 265, 267, 268, 266, 134),
    (135, 138, 140, 139, 137, 136, 141, 148, 149, 150, 181, 182, 183, 184, 185, 186, 187, 27, 190, 191, 192, 189, 245, 202, 203),
    (22, 23, 24, 25, 26, 28, 29, 14, 159, 92, 105, 103, 175, 176, 180, 289, 83, 112, 113, 278, 241, 217, 237, 209, 167),
    (91, 95, 93, 94, 101, 98, 96, 97, 99, 109, 100, 120, 118, 107, 108, 111, 115, 114, 116, 119, 117, 153, 152, 106, 102),
    (151, 173, 157, 154, 155, 104, 160, 161, 162, 156, 166, 168, 174, 178, 163, 164, 158, 170, 171, 169, 172, 177, 179, 282, 295),
    (193, 194, 198, 195, 196, 197, 279, 280, 281, 204, 290, 213, 214, 211, 212, 205, 207, 208, 215, 216, 220, 219, 222, 223, 221),
    (188, 229, 224, 210, 227, 226, 225, 230, 231, 232, 233, 228, 218, 234, 235, 236, 238, 246, 247, 269, 270, 201, 206, 200, 264),
    (284, 285, 283, 250, 261, 249, 251, 248, 253, 254, 257, 259, 256, 199, 242, 243, 165, 81, 48, 292, 296, 297, 298, 299, 300),
)


def main() -> None:
    if len(PHASES) != 12 or any(len(phase) != 25 for phase in PHASES):
        raise ValueError("The route must contain exactly 12 phases of 25 books")
    route = [book_no for phase in PHASES for book_no in phase]
    if sorted(route) != list(range(1, 301)):
        raise ValueError("The route must use every stable book id exactly once")

    books = json.loads(BOOKS_PATH.read_text(encoding="utf-8"))
    if sorted(int(book["no"]) for book in books) != list(range(1, 301)):
        raise ValueError("data/books.json must contain stable ids 1..300")

    position_by_no = {book_no: position for position, book_no in enumerate(route, 1)}
    updated_books = []
    for book in books:
        stable_no = int(book["no"])
        position = position_by_no[stable_no]
        updated = {}
        for key, value in book.items():
            if key in {"readingOrder", "routePhase"}:
                continue
            updated[key] = value
            if key == "evre":
                updated["readingOrder"] = position
                updated["routePhase"] = ((position - 1) // 25) + 1
        updated_books.append(updated)

    BOOKS_PATH.write_text(
        json.dumps(updated_books, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Applied reading route: 300 books, 12 phases, stable ids preserved.")


if __name__ == "__main__":
    main()
