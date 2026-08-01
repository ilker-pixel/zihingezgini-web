#!/usr/bin/env python3
"""Compact, book-specific input helpers for the fifth twenty-book collection."""

from __future__ import annotations

from summary_batch_common import slugify
from next_twenty_common import write_specs


def topic(title: str, section: str, claim: str, scene: str, nuance: str, today: str):
    """Create one fully illustrated chapter spec without duplicating art metadata."""
    art = slugify(title)[:42]
    caption = f"{title} fikrini somutlaştıran simgesel sahne."
    return (title, section, claim, scene, nuance, today, art, caption)


__all__ = ["topic", "write_specs"]
