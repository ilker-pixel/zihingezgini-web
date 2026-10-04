#!/usr/bin/env python3
"""Attach verified original narratives to existing topics without editing short copy."""
import argparse
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_gazete as g
from adapt_source_bundle import FEED_MAP


def attach(current, source):
    if source.get('schema_version') != 'gundemgazetesi-full-details/1':
        g.fail('tanımsız kaynak detay şeması')
    details = source.get('details_by_article_id')
    if not isinstance(details, dict): g.fail('details_by_article_id nesnesi gerekli')
    topics = {t['id']: (b, t) for b in current['bulletins'] for t in b['topics']}
    if len(topics) != sum(len(b['topics']) for b in current['bulletins']):
        g.fail('bu eşleme için yazı kimlikleri kaynaklar arasında benzersiz olmalı')
    if set(details) != set(topics): g.fail('detay eşlemesi güncel yazıların tamamıyla eşleşmiyor')
    result = copy.deepcopy(current)
    for b in result['bulletins']:
        for t in b['topics']:
            detail = details[t['id']]
            if detail.get('article_id') != t['id'] or FEED_MAP.get(detail.get('feed_id')) != b['feed_id']:
                g.fail('detay yazı/kaynak kimliği uyuşmuyor')
            t['full_text'] = detail['full_text']
            for provenance in detail.get('provenance', []):
                expected = provenance.get('body_sha256')
                if expected and hashlib.sha256(t['full_text'].encode()).hexdigest() != expected:
                    g.fail('özgün metin SHA256 eşleşmiyor')
            t['full_text_sections'] = [{**{k: copy.deepcopy(s.get(k)) for k in ('heading', 'timestamp', 'url', 'paragraphs')},
                                       **({'warning': s['warning']} if 'warning' in s else {})}
                                      for s in detail['sections']]
            t['full_text_sources'] = [{'name': s['label'], 'url': s['url'], 'published_at': s.get('published_at')}
                                      for s in detail['sources']]
            t['full_text_metadata'] = {k: copy.deepcopy(detail[k]) for k in (
                'original_title', 'detail_kind', 'publication', 'event_time', 'channel',
                'original_video_title', 'duration_label', 'video_id', 'source_url', 'overview', 'quick_read_pages',
                'length_note', 'provenance') if k in detail}
            # Native Library ids stay in the private input, never the public state.
            def public(value):
                if isinstance(value, dict):
                    return {k: public(v) for k,v in value.items() if k not in ('library_file_id', 'file_id')}
                if isinstance(value, list): return [public(v) for v in value]
                return value
            t['full_text_metadata'] = public(t['full_text_metadata'])
        # Enrichment is a corrected completed bulletin. Respect the importer's
        # same-id conflict rule and use the source's real preparation timestamp.
        b['prepared_at'] = source['assembled_at']
        identity = {k:v for k,v in b.items() if k not in ('bulletin_id', 'prepared_at')}
        b['bulletin_id'] = 'detail-' + hashlib.sha256(g.canonical(identity).encode()).hexdigest()[:24]
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--sha256', required=True, help='Verified original source checksum')
    p.add_argument('--root', type=Path, default=g.ROOT)
    args = p.parse_args()
    raw = args.source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != args.sha256: g.fail('kaynak SHA256 eşleşmiyor')
    now = dt.datetime.now(dt.timezone.utc)
    current = g.load_current(args.root, now)
    result = attach(current, g.read_json(args.source))
    g.validate_bundle(result, now)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'feeds': len(result['bulletins']), 'details': sum(len(b['topics']) for b in result['bulletins'])}))


if __name__ == '__main__': main()
