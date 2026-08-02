#!/usr/bin/env python3
"""Small declarative helpers for the final seventy-two summaries."""

from __future__ import annotations

from final_summary_common import topic as t


def book(
    no, slug, title, author, original, color, subtitle, intro, reading_note,
    opening_scene, sources, chapters, misreading, misreading_example,
    reading_guard, reception, criticism, debate_scene, questions, daily_test,
    reader_scene, essence, cover_metaphor, original_invitation, dense=False,
    deepenings=None,
):
    """Return one fully explicit book specification.

    ``chapters`` contains sixteen seven-field tuples.  Keeping the five narrative
    layers in the source files makes it possible to audit every paragraph before
    layout; the common builder never pads short manuscripts with generic prose.
    """
    prepared = [t(*chapter) for chapter in chapters]
    if deepenings is not None:
        if len(deepenings) != 16:
            raise ValueError(f"Book {no} needs sixteen chapter deepenings")
        for chapter, deepening in zip(prepared, deepenings):
            chapter["today"] = f"{chapter['today']} {deepening.strip()}"
    return {
        "no": no, "slug": slug, "title": title, "author": author,
        "original": original, "color": color, "subtitle": subtitle,
        "intro": intro, "reading_note": reading_note,
        "opening_scene": opening_scene, "sources": sources,
        "chapters": prepared,
        "misreading": misreading, "misreading_example": misreading_example,
        "reading_guard": reading_guard, "reception": reception,
        "criticism": criticism, "debate_scene": debate_scene,
        "questions": questions, "daily_test": daily_test,
        "reader_scene": reader_scene, "essence": essence,
        "cover_metaphor": cover_metaphor,
        "original_invitation": original_invitation, "dense": dense,
    }


__all__ = ["book", "t"]
