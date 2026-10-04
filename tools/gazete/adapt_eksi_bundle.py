#!/usr/bin/env python3
"""Normalize a verified completed Ekşi PDF text bundle; never rewrites stories."""
import argparse
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_gazete as g

CATEGORY_MAP = {
    'Ekonomi ve denetim': 'ekonomi', 'Siyaset ve kamuoyu': 'turkiye',
    'Eğitim ve toplum': 'turkiye', 'İlişkiler ve yaşam': 'felsefe',
    'Kültür ve medya': 'kultur', 'Spor': 'spor', 'Afet ve güvenlik': 'turkiye',
}


def adapt(source, evidence):
    g.fields(source, ('schema_version', 'bulletins'), ('prepared_at',), 'Ekşi kaynak paketi')
    if type(source['schema_version']) is not int or source['schema_version'] != 1 or not isinstance(source['bulletins'], list) or len(source['bulletins']) != 1:
        g.fail('Ekşi kaynak paketi tek tamamlanmış bülten içermeli')
    original = source['bulletins'][0]
    if original.get('feed_id') != 'eksi': g.fail('yalnız Ekşi kaynak paketi kabul edilir')
    items = original.get('topics')
    observations = evidence.get('topics')
    if not isinstance(items, list) or not isinstance(observations, list): g.fail('konu listeleri gerekli')
    ids = [t['id'] for t in items]
    if ids != [t['id'] for t in observations] or evidence.get('total_topics') != len(ids):
        g.fail('doğrulama kanıtındaki konu sayısı/sırası/kimlikleri uyuşmuyor')
    if evidence.get('original_completed_at') != original.get('completed_at'):
        g.fail('özgün tamamlanma zamanı kanıtla uyuşmuyor')
    prepared = original.get('prepared_at') or source.get('prepared_at')
    if prepared != evidence.get('prepared_at'): g.fail('hazırlama zamanı kanıtla uyuşmuyor')
    b = copy.deepcopy(original)
    b['prepared_at'] = prepared
    for t, observation in zip(b['topics'], observations):
        category = t['category']
        if category not in g.CATEGORIES and category not in CATEGORY_MAP:
            g.fail('tanımsız Ekşi kaynak kategorisi: ' + str(category))
        if observation.get('original_topic_url') not in [s['url'] for s in t['sources']]:
            g.fail('özgün konu URL kanıtla uyuşmuyor')
        tm = t.setdefault('metadata', {})
        tm.setdefault('original_category', category)
        tm['source_pdf_page'] = observation['pdf_page']
        t['category'] = CATEGORY_MAP.get(category, category)
    bm = b.setdefault('metadata', {})
    # Sampling/attribution limitations remain explicit rather than being
    # broadened into whole-site coverage or rewritten into the story bodies.
    notes = [bm.get('coverage_note'), evidence.get('selection_cutoff_note'), evidence.get('source_date_note')]
    bm['coverage_note'] = '\n\n'.join(dict.fromkeys(part for n in notes if n for part in n.split('\n\n')))
    return {'schema_version': 1, 'bulletins': [b]}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path);p.add_argument('evidence', type=Path);p.add_argument('output', type=Path)
    p.add_argument('--source-sha256', required=True);p.add_argument('--evidence-sha256', required=True)
    args = p.parse_args()
    for path, expected in ((args.source,args.source_sha256),(args.evidence,args.evidence_sha256)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:g.fail('kaynak/kanıt SHA256 eşleşmiyor')
    result = adapt(g.read_json(args.source),g.read_json(args.evidence))
    g.validate_bundle(result,dt.datetime.now(dt.timezone.utc))
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'topics':len(result['bulletins'][0]['topics']),
                      'sources':sum(len(t['sources']) for t in result['bulletins'][0]['topics'])}))


if __name__ == '__main__':main()
