#!/usr/bin/env python3
"""Verify that the retired public newspaper stays absent; never modifies files."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def check(root):
    site = Path(root) / 'gazete'
    if site.exists() or site.is_symlink():
        raise ValueError('Herkese açık Gazete kaldırıldı; gazete/ dizini veya bağlantısı yeniden yayımlanamaz.')
    print('Gazete yayından kaldırma kontrolü geçti: herkese açık gazete/ bulunmuyor.')


if __name__ == '__main__':
    check(ROOT)
