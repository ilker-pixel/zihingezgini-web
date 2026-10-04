#!/usr/bin/env python3
"""Normalize the named completed source bundle. Preserves text and time semantics."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_gazete as g

FEED_MAP = {'general_morning_08':'morning', 'ai_21':'ai', 'youtube_am_10':'youtube_am', 'youtube_pm_22':'youtube_pm'}


def adapt(source):
    if source.get('schema_version') != 'gundemgazetesi-source-bundle/1':
        g.fail('tanımsız kaynak paket şeması')
    if source.get('timezone') != 'Europe/Istanbul': g.fail('kaynak saat dilimi değişmiş')
    articles = source.get('articles')
    if not isinstance(articles, list): g.fail('kaynak articles listesi gerekli')
    feeds = source.get('feeds')
    if not isinstance(feeds, list): g.fail('kaynak feeds listesi gerekli')
    known_ids = [f.get('id') for f in feeds]
    if len(set(known_ids)) != len(known_ids): g.fail('yinelenen kaynak feed')
    if any(a.get('feed_id') not in known_ids for a in articles): g.fail('sahipsiz kaynak makale')
    result = []
    for f in feeds:
        if f['id'] not in FEED_MAP: g.fail('desteklenmeyen kaynak feed')
        items = []
        for a in articles:
            if a['feed_id'] != f['id']: continue
            paragraphs = a['what_happened']
            if not isinstance(paragraphs, list) or any(not isinstance(p,str) or not p.strip() for p in paragraphs):
                g.fail('kaynak Ne oldu? boş olmayan paragraf listesi olmalı')
            metadata = {k:a[k] for k in ('publication','event_time','channel','original_title','duration_label','source_broadcast','carried_over_from') if k in a}
            item = {'id':a['id'], 'category':a['topic_id'], 'title':a['title'], 'summary':a['summary'],
                          'what_happened':'\n\n'.join(paragraphs),
                          'sources':[{'name':s['label'],'url':s['url'],'published_at':None} for s in a['sources']],
                          'metadata':metadata}
            if 'full_text' in a:
                full_text = a['full_text']
                if not isinstance(full_text, list) or not full_text or any(not isinstance(p,str) or not p.strip() for p in full_text):
                    g.fail('kaynak full_text boş olmayan paragraf listesi olmalı')
                item['full_text'] = '\n\n'.join(full_text)
            if 'full_text_sources' in a:
                g.validate_sources(a['full_text_sources'])
                item['full_text_sources'] = a['full_text_sources']
            for key in ('full_text_sections', 'full_text_metadata'):
                if key in a: item[key] = a[key]
            items.append(item)
        window = f.get('window') or {}
        metadata = {k:f[k] for k in ('delivered_at','research_cutoff','coverage_note','source_gaps') if k in f}
        if window: metadata['window_semantics'] = {k:v for k,v in window.items() if k not in ('start','end')}
        b = {'feed_id':FEED_MAP[f['id']], 'scheduled_for':f"{f['edition_date']}T{f['scheduled_time_local']}:00+03:00",
             'completed_at':f.get('generation_completed_at'), 'prepared_at':source['assembled_at'],
             'coverage_start':window.get('start'), 'coverage_end':window.get('end'), 'topics':items, 'metadata':metadata}
        # Source content/time semantics determine identity. Assembly time alone is not a new revision.
        identity = {k:v for k,v in b.items() if k != 'prepared_at'}
        digest = hashlib.sha256(g.canonical(identity).encode()).hexdigest()[:16]
        b['bulletin_id'] = f"{b['feed_id']}-{f['edition_date']}-{digest}"
        result.append(b)
    if source.get('counts',{}).get('articles_total',len(articles)) != len(articles):g.fail('kaynak makale sayısı uyuşmuyor')
    return {'schema_version':1,'bulletins':result}


def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--sha256',help='Expected Library source checksum')
    args=p.parse_args()
    raw=args.source.read_bytes()
    if args.sha256 and hashlib.sha256(raw).hexdigest()!=args.sha256:g.fail('kaynak SHA256 eşleşmiyor')
    source=g.read_json(args.source)
    normalized=adapt(source)
    import datetime as dt
    g.validate_bundle(normalized,dt.datetime.now(dt.timezone.utc))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(normalized,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'feeds':len(normalized['bulletins']),'articles':sum(len(b['topics']) for b in normalized['bulletins'])},ensure_ascii=False))


if __name__=='__main__':main()
