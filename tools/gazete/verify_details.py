#!/usr/bin/env python3
"""Verify every existing short article and every supplied original detail locally."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_gazete as g


class Page(HTMLParser):
    def __init__(self, value):
        super().__init__(); self.parts=[]; self.hrefs=[]; self.active=[]
        self.feed(value)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'href' in attrs:self.hrefs.append(attrs['href'])
        if tag in ('h1','h3','h4','p','li'):self.active.append([tag,[]])
    def handle_data(self, data):
        for _,parts in self.active:parts.append(data)
    def handle_endtag(self, tag):
        if self.active and self.active[-1][0]==tag:
            _,parts=self.active.pop();self.parts.append(''.join(parts))


def normalized(value):
    value=re.sub(r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)',r'\1',value)
    return ' '.join(value.split())


def verify(root, baseline, source):
    current=g.read_json(root/'gazete/data/current.json')
    old={(b['feed_id'],t['id']):t for b in baseline['bulletins'] for t in b['topics']}
    new={(b['feed_id'],t['id']):(b,t) for b in current['bulletins'] for t in b['topics']}
    assert old.keys()==new.keys(),'Existing article ids changed'
    assert {t['id'] for _,t in new.values()}==source['details_by_article_id'].keys(),'Source mapping ids changed'
    sections=0; quick_pages=0
    for key,original in old.items():
        b,t=new[key];detail=source['details_by_article_id'][t['id']]
        for name,value in original.items():assert t[name]==value,f'{key}: existing {name} changed'
        assert t['full_text']==detail['full_text'],f'{key}: source body changed'
        short=Page((root/'gazete'/g.article_path(b,t)/'index.html').read_text())
        long=Page((root/'gazete'/g.detail_path(b,t)/'index.html').read_text())
        short_parts={normalized(p) for p in short.parts};long_parts={normalized(p) for p in long.parts}
        assert normalized(t['title']) in short_parts and normalized(t['summary']) in short_parts,f'{key}: short header changed'
        for paragraph in re.split(r'\n\s*\n',t['what_happened']):
            if paragraph.strip():assert normalized(paragraph) in short_parts,f'{key}: short paragraph missing'
        for paragraph in re.split(r'\n\s*\n',detail['full_text']):
            if paragraph.strip():assert normalized(paragraph) in long_parts,f'{key}: original paragraph/heading missing'
        visible=' '.join(normalized(p) for p in long.parts)
        for page in detail.get('quick_read_pages',[]):
            values=[page['title'],page['about'],page.get('takeaway',''),page.get('caveat','')]
            for name in ('main','example','importance'):
                if page.get(name):values += [page[name]['heading'],page[name]['text']]
            diagram=page.get('diagram')
            if diagram:
                values += [diagram['title'],diagram.get('caption','')]
                for step in diagram['steps']:values += [step['label'],step['text']]
            for value in values:assert normalized(value) in visible,f'{key}: quick reading content missing'
            quick_pages+=1
        for section in detail['sections']:
            if not section.get('timestamp'):continue
            label=section['timestamp']+' · '+section['heading']
            assert normalized(label) in long_parts,f'{key}: timestamp heading missing'
            url=section.get('url')
            if not url:
                seconds=0
                for part in section['timestamp'].split(':'):seconds=seconds*60+int(part)
                video=detail['source_url'];url=video+('&' if '?' in video else '?')+f't={seconds}s'
            assert url in long.hrefs,f'{key}: timestamp navigation missing'
            sections+=1
        assert '/gazete/'+g.article_path(b,t) in long.hrefs and '/gazete/' in long.hrefs,f'{key}: returns missing'
        assert not any('/api/library/' in x or 'libfile_' in x for x in short.hrefs+long.hrefs),'Private Library link exposed'
    return {'articles':len(old),'all_original_topic_fields_unchanged':True,'all_rendered_short_paragraphs_preserved':True,
            'full_text_verbatim':True,'all_source_paragraphs_rendered':True,'youtube_timestamp_sections':sections,
            'quick_read_pages':quick_pages,'all_timestamp_links_and_return_links_valid':True}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--root',type=Path,default=g.ROOT);p.add_argument('--report',type=Path)
    args=p.parse_args()
    result=verify(args.root,g.read_json(args.baseline),g.read_json(args.source))
    result['source_sha256']=hashlib.sha256(args.source.read_bytes()).hexdigest()
    if args.report:args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
