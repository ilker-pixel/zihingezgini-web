#!/usr/bin/env python3
"""Check current newspaper only; never modifies it."""
import datetime as dt
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_gazete as g


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []; self.ids = set()
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        for key in ('href', 'src'):
            if key in attrs: self.urls.append(attrs[key])
        if 'id' in attrs: self.ids.add(attrs['id'])


def check(root):
    state = g.load_current(root, dt.datetime.now(dt.timezone.utc))
    expected = {'index.html', '404.html'}
    for b in state['bulletins']:
        for t in b['topics']:
            expected.add(g.article_path(b,t) + 'index.html')
            expected.add(f"konu/{t['category']}/index.html")
    site = root / 'gazete'
    actual = {str(p.relative_to(site)) for p in site.rglob('*.html')}
    if actual != expected: raise ValueError(f'Gazete sayfaları uyuşmuyor: {actual ^ expected}')
    for page in site.rglob('*.html'):
        parser = Links(); parser.feed(page.read_text(encoding='utf-8'))
        for link in parser.urls:
            parsed = urlsplit(link)
            if parsed.scheme: continue
            if parsed.path:
                if not parsed.path.startswith('/gazete/'): raise ValueError(f'Gazete dışı bağlantı: {page}: {link}')
                target = root / parsed.path.lstrip('/')
                if parsed.path.endswith('/'): target /= 'index.html'
                if not target.is_file(): raise ValueError(f'Kırık bağlantı: {page}: {link}')
            elif parsed.fragment and parsed.fragment not in parser.ids:
                raise ValueError(f'Kırık sayfa içi bağlantı: {page}: {link}')
    for loc in ET.parse(site/'sitemap.xml').findall('.//{*}loc'):
        target = root / urlsplit(loc.text).path.lstrip('/') / 'index.html'
        if not target.is_file(): raise ValueError(f'Kırık sitemap: {loc.text}')
    allowed = actual | {'data/current.json', 'static/style.css', 'static/freshness.js', 'bundle.schema.json', 'sitemap.xml', '.nojekyll'}
    extras = {str(p.relative_to(site)) for p in site.rglob('*') if p.is_file()} - allowed
    if extras: raise ValueError(f'Eski/fazladan gazete dosyaları: {extras}')
    print(f'Gazete doğrulandı: {len(state["bulletins"])} kaynak, {len(actual)} HTML sayfası; tüm yerel bağlantılar geçerli.')


if __name__ == '__main__': check(g.ROOT)
