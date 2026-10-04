#!/usr/bin/env python3
"""Gazete contract, replacement, recovery and output tests; never reads live data."""
import copy
import datetime as dt
from html.parser import HTMLParser
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

import build_gazete as g

NOW = dt.datetime.fromisoformat("2026-10-03T23:59:00+03:00")


def bulletin(feed="morning", day="2026-10-03", topics=None):
    hour = g.FEEDS[feed][1]
    return {
        "feed_id": feed, "bulletin_id": f"{feed}-{day}",
        "scheduled_for": f"{day}T{hour:02}:00:00+03:00",
        "completed_at": f"{day}T{hour:02}:05:00+03:00",
        "coverage_start": f"{day}T00:00:00+03:00",
        "coverage_end": f"{day}T{hour:02}:00:00+03:00",
        "topics": topics or [{
            "id": f"test-{feed}", "category": "bilim" if feed == "morning" else "teknoloji",
            "title": "Test yazısı: araştırma sonucu", "summary": "Bu cümle yalnız otomatik test içindir.",
            "what_happened": "Bu paragraf yalnız yazılım testi içindir. Kaynak sonucu henüz bağımsız doğrulamamıştır.\n\n" + "Tam metin korunur. " * 150,
            "sources": [{"name": "Test kaynağı", "url": "https://example.com/source", "published_at": "2026-10-02"}]
        }]
    }


def bundle(*bs):
    return {"schema_version": 1, "bulletins": list(bs)}


def files(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []; self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.urls += [attrs[k] for k in ('href','src') if k in attrs]
        if 'id' in attrs: self.ids.add(attrs['id'])


class GazeteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root/'unrelated').mkdir()
        (self.root/'unrelated/site.html').write_text('DO NOT CHANGE')
        (self.root/'gazete/baski/old').mkdir(parents=True)
        (self.root/'gazete/baski/old/index.html').write_text('obsolete')
        (self.root/'gazete/eksi.html').write_text('obsolete')
    def tearDown(self):
        self.tmp.cleanup()
    def import_(self, *bs):
        return g.import_bundle(self.root, bundle(*bs), NOW)
    def state(self):
        return g.load_current(self.root, NOW)
    def test_topics_in_categories_and_old_newspaper_removed(self):
        self.import_(*(bulletin(f) for f in g.FEEDS))
        self.assertFalse((self.root/'gazete/baski').exists())
        self.assertFalse((self.root/'gazete/eksi.html').exists())
        self.assertEqual((self.root/'unrelated/site.html').read_text(), 'DO NOT CHANGE')
        self.assertTrue((self.root/'gazete/konu/bilim/index.html').exists())
        self.assertTrue((self.root/'gazete/konu/teknoloji/index.html').exists())
        self.assertFalse((self.root/'gazete/konu/youtube_am').exists())
        article=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
        self.assertIn('02.10.2026',(self.root/'gazete/kaynaklar/index.html').read_text())
        self.assertIn('03.10.2026 08.00',article)
        self.assertIn('Kaynak sonucu henüz bağımsız doğrulamamıştır.',article)
        self.assertEqual(article.count('Tam metin korunur.'),150)
        self.assertNotIn('Neden önemli?',article)
        self.assertNotIn('Dikkat',article)
    def test_replay_is_noop(self):
        self.import_(bulletin())
        before=files(self.root)
        result=self.import_(bulletin())
        self.assertEqual(result,{'changed':[],'duplicate':['morning'],'stale':[]})
        self.assertEqual(before,files(self.root))
    def test_one_feed_replaces_only_its_articles(self):
        self.import_(bulletin('morning','2026-10-02'),bulletin('ai'))
        old_ai=copy.deepcopy(self.state()['bulletins'][1])
        b=bulletin(); b['topics'][0]['id']='replacement'
        self.import_(b)
        self.assertEqual(self.state()['bulletins'][1],old_ai)
        self.assertFalse((self.root/'gazete/yazi/morning/test-morning').exists())
        self.assertTrue((self.root/'gazete/yazi/morning/replacement/index.html').exists())
    def test_late_missing_source_keeps_previous(self):
        self.import_(bulletin('youtube_pm','2026-10-02'),bulletin('ai'))
        old=copy.deepcopy(self.state()['bulletins'][1])
        self.import_(bulletin())
        self.assertEqual(self.state()['bulletins'][2],old)
        home=(self.root/'gazete/index.html').read_text()
        self.assertIn('Yeni bülten bekleniyor',home)
        self.assertIn('02.10.2026 22.00',home)
        self.assertTrue((self.root/'gazete/yazi/youtube_pm/test-youtube_pm/index.html').exists())
    def test_out_of_order_ignored(self):
        self.import_(bulletin())
        before=files(self.root)
        r=self.import_(bulletin(day='2026-10-02'))
        self.assertEqual(r['stale'],['morning'])
        self.assertEqual(before,files(self.root))
    def test_corrected_slot_requires_new_id_and_later_completion(self):
        self.import_(bulletin())
        b=bulletin();b['bulletin_id']='morning-correction';b['completed_at']='2026-10-03T08:15:00+03:00'
        b['topics'][0]['summary']='Düzeltilmiş test cümlesi.'
        self.assertEqual(self.import_(b)['changed'],['morning'])
    def test_conflicting_id_rejected_whole_bundle(self):
        self.import_(bulletin())
        before=files(self.root)
        b=bulletin();b['topics'][0]['title']='Changed'
        with self.assertRaises(g.InvalidBulletin):self.import_(bulletin('ai'),b)
        self.assertEqual(before,files(self.root))
    def test_invalid_data_preserves_entire_site(self):
        variants=[]
        for path,value in [('feed_id','podcast'),('feed_id',[]),('scheduled_for','2026-10-03T09:00:00+03:00'),('completed_at','2026-10-04T08:00:00+03:00'),('coverage_start','2026-10-03T09:00:00+03:00'),('topics',[])]:
            b=bulletin();b[path]=value;variants.append(b)
        for path,value in [('id','../../bad'),('category','ai_haberleri'),('category',[]),('summary',''),('summary','two\nlines'),('what_happened','')]:
            b=bulletin();b['topics'][0][path]=value;variants.append(b)
        for url in ['javascript:alert(1)','file:///etc/passwd','https://user:secret@example.com','https://example.com/bad path']:
            b=bulletin();b['topics'][0]['sources'][0]['url']=url;variants.append(b)
        b=bulletin();b['topics'][0]['sources'][0]['published_at']='2026-02-30';variants.append(b)
        b=bulletin();b['audio']='unrequested.mp3';variants.append(b)
        before=files(self.root)
        for b in variants:
            with self.subTest(b=b):
                with self.assertRaises(g.InvalidBulletin):self.import_(bulletin('ai'),b)
                self.assertEqual(before,files(self.root))
    def test_duplicates_inside_bundle_rejected(self):
        for bs in [(bulletin(),bulletin()),]:
            with self.assertRaises(g.InvalidBulletin):self.import_(*bs)
        b=bulletin();b['topics']*=2
        with self.assertRaises(g.InvalidBulletin):self.import_(b)
    def test_html_escaped_and_unknown_dates_preserved(self):
        b=bulletin();b['topics'][0]['title']='<script>alert(1)</script>'
        b['topics'][0]['what_happened']='<img src=x onerror=alert(1)>'
        b['topics'][0]['sources'][0]['published_at']=None
        self.import_(b)
        page=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
        self.assertNotIn('<img src=x',page)
        self.assertIn('&lt;img',page)
        self.assertIn('Yayın tarihi kaynakta belirtilmemiş',(self.root/'gazete/kaynaklar/index.html').read_text())
    def test_all_local_links_resolve(self):
        self.import_(*(bulletin(f) for f in g.FEEDS))
        for page in (self.root/'gazete').rglob('*.html'):
            parser=Links();parser.feed(page.read_text())
            for url in parser.urls:
                parsed=urlsplit(url)
                if parsed.scheme:continue
                if parsed.path:
                    self.assertTrue(parsed.path.startswith('/gazete/'),url)
                    target=self.root/parsed.path.lstrip('/')
                    if parsed.path.endswith('/'):target/='index.html'
                    self.assertTrue(target.is_file(),f'{page}: {url}')
                    if parsed.fragment:
                        target_parser=Links();target_parser.feed(target.read_text())
                        self.assertIn(parsed.fragment,target_parser.ids)
                elif parsed.fragment:self.assertIn(parsed.fragment,parser.ids)
    def test_sources_navigation_is_in_footer_on_every_page(self):
        self.import_(*(bulletin(f) for f in g.FEEDS))
        for path in (self.root/'gazete').rglob('*.html'):
            page=path.read_text()
            header=page.split('<header',1)[1].split('</header>',1)[0]
            footer=page.split('<footer>',1)[1].split('</footer>',1)[0]
            self.assertNotIn('/gazete/kaynaklar/',header,str(path))
            self.assertIn('class="footer-sources" href="/gazete/kaynaklar/"',footer,str(path))
            self.assertEqual(footer.count('class="footer-sources"'),1)
            self.assertEqual('aria-current="page"' in footer,path==self.root/'gazete/kaynaklar/index.html')
        short=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
        detail=(self.root/'gazete/yazi/morning/test-morning/detay/index.html').read_text()
        for page in (short,detail):self.assertIn('/gazete/kaynaklar/#kaynak-morning-test-morning',page)
    def test_sitemap_matches_generated_pages(self):
        import xml.etree.ElementTree as ET
        self.import_(bulletin())
        tree=ET.parse(self.root/'gazete/sitemap.xml')
        for loc in tree.findall('.//{*}loc'):
            target=self.root/urlsplit(loc.text).path.lstrip('/')/'index.html'
            self.assertTrue(target.is_file(),loc.text)
    def test_render_failure_preserves_site(self):
        self.import_(bulletin())
        before=files(self.root)
        with patch.object(g,'render',side_effect=OSError('test failure')):
            with self.assertRaises(OSError):self.import_(bulletin('ai'))
        self.assertEqual(before,files(self.root))
        self.assertFalse(list(self.root.glob('.gazete-stage-*')))
    def test_commit_failure_restores_previous(self):
        self.import_(bulletin())
        before=files(self.root)
        original=Path.rename
        def rename(p,target):
            if '.gazete-stage-' in str(p):raise OSError('test rename failure')
            return original(p,target)
        with patch.object(Path,'rename',rename):
            with self.assertRaises(OSError):self.import_(bulletin('ai'))
        self.assertEqual(before,files(self.root))
    def test_crash_recovery_before_loading_state(self):
        self.import_(bulletin())
        (self.root/'gazete').rename(self.root/'.gazete-previous')
        self.import_(bulletin('ai'))
        self.assertEqual(len(self.state()['bulletins']),2)
        self.assertFalse((self.root/'.gazete-previous').exists())
    def test_repeated_updates_do_not_accumulate_editions(self):
        for day in ['2026-10-01','2026-10-02','2026-10-03']:self.import_(bulletin(day=day))
        self.assertEqual(len(self.state()['bulletins']),1)
        self.assertEqual(len(list((self.root/'gazete/yazi').rglob('index.html'))),2)
        self.assertFalse((self.root/'gazete/baski').exists())
        self.assertFalse(list((self.root/'gazete').rglob('*.mp3')))
        self.assertFalse(list((self.root/'gazete').rglob('*.pdf')))
    def test_duplicate_json_keys_rejected(self):
        p=self.root/'bad.json';p.write_text('{"schema_version":1,"schema_version":2}')
        with self.assertRaises(g.InvalidBulletin):g.read_json(p)
    def test_blank_current_can_render(self):
        g.replace_site(self.root,{'schema_version':1,'bulletins':[]},NOW)
        self.assertIn('İlk tamamlanmış bülten', (self.root/'gazete/index.html').read_text())
        self.assertEqual(self.state()['bulletins'],[])
    def test_unknown_completion_does_not_become_schedule_time(self):
        b=bulletin();b['completed_at']=None;b['prepared_at']='2026-10-03T20:52:00Z'
        b['coverage_start']=None;b['coverage_end']=None
        self.import_(b)
        stored=self.state()['bulletins'][0]
        self.assertIsNone(stored['completed_at'])
        page=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
        records=(self.root/'gazete/kaynaklar/index.html').read_text()
        self.assertIn('Bülten tamamlandı: Kaynakta belirtilmemiş',records)
        self.assertIn('Paket hazırlandı: 03.10.2026 23.52',records)
        self.assertIn('Kesin kapsam başlangıcı ve sonu kaynakta belirtilmemiş',records)
    def test_repackaging_is_idempotent(self):
        b=bulletin();b['prepared_at']='2026-10-03T20:45:00Z';self.import_(b)
        before=files(self.root)
        b['prepared_at']='2026-10-03T20:52:00Z'
        self.assertEqual(self.import_(b)['duplicate'],['morning'])
        self.assertEqual(before,files(self.root))
    def test_concurrent_different_feeds_do_not_lose_updates(self):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda b:self.import_(b),[bulletin(),bulletin('ai')]))
        self.assertEqual(len(self.state()['bulletins']),2)
        self.assertTrue(all(r['changed'] for r in results))
    def test_same_topic_id_in_different_feeds_keeps_distinct_urls(self):
        a,b=bulletin(),bulletin('ai');b['topics'][0]['id']=a['topics'][0]['id']
        self.import_(a,b)
        self.assertTrue((self.root/'gazete/yazi/morning/test-morning/index.html').exists())
        self.assertTrue((self.root/'gazete/yazi/ai/test-morning/index.html').exists())
    def test_changed_category_removes_old_category_and_topic(self):
        self.import_(bulletin(day='2026-10-02'))
        b=bulletin();b['topics'][0]['category']='felsefe';self.import_(b)
        self.assertFalse((self.root/'gazete/konu/bilim').exists())
        self.assertTrue((self.root/'gazete/konu/felsefe/index.html').exists())
    def test_source_publication_and_event_dates_stay_separate(self):
        b=bulletin();b['topics'][0]['metadata']={'publication':{'at':None,'date':'2026-10-01','note':'Tarihin saati bilinmiyor.'},'event_time':{'start':'2026-09-30','end':None,'note':'Olay tarihi ayrı.'}}
        self.import_(b)
        page=(self.root/'gazete/kaynaklar/index.html').read_text()
        self.assertIn('Yayın/kayıt tarihi: 01.10.2026',page)
        self.assertIn('Olay başlangıcı: 30.09.2026',page)
        self.assertIn('Tarihin saati bilinmiyor.',page)
    def test_source_adapter_preserves_all_text_and_times(self):
        import sys
        sys.path.insert(0,str(Path(__file__).parent/'gazete'))
        from adapt_source_bundle import adapt
        source={'schema_version':'gundemgazetesi-source-bundle/1','timezone':'Europe/Istanbul','assembled_at':'2026-10-03T20:52:00Z',
                'feeds':[{'id':'general_morning_08','edition_date':'2026-10-03','scheduled_time_local':'08:00','generation_completed_at':None,'window':None,'research_cutoff':{'at':'2026-10-03T06:15:00Z','precision':'approximate'}}],
                'articles':[{'id':'test-source','feed_id':'general_morning_08','topic_id':'hava','title':'Test başlığı','summary':'Tek test cümlesi.','what_happened':['Birinci paragraf.','İkinci paragraf, kaynak çekincesi.'],'sources':[{'label':'Test','url':'https://example.com'}],'publication':{'at':None,'date':'2026-10-02'}}]}
        normalized=adapt(source);g.validate_bundle(normalized,NOW)
        b=normalized['bulletins'][0];self.assertIsNone(b['completed_at']);self.assertIsNone(b['coverage_start'])
        self.assertEqual(b['metadata']['research_cutoff']['precision'],'approximate')
        self.assertEqual(b['topics'][0]['what_happened'],'Birinci paragraf.\n\nİkinci paragraf, kaynak çekincesi.')
        self.assertIsNone(b['topics'][0]['sources'][0]['published_at'])
        self.assertEqual(b['topics'][0]['metadata']['publication']['date'],'2026-10-02')
        b2=copy.deepcopy(source);b2['assembled_at']='2026-10-03T20:59:00Z'
        self.assertEqual(adapt(b2)['bulletins'][0]['bulletin_id'],b['bulletin_id'])

    def test_long_source_is_separate_and_short_copy_unchanged(self):
        b=bulletin('ai'); original=copy.deepcopy(b['topics'][0])
        t=b['topics'][0]
        t['full_text']='Özgün uzun kaynak anlatımı.\n\nKişisel tedavi önerisi değildir.\n\n'+'Kaynak ayrıntısı. '*400
        t['full_text_sources']=[{'name':'Uzun metnin kaynağı','url':'https://example.com/detail','published_at':None}]
        self.import_(b)
        stored=self.state()['bulletins'][0]['topics'][0]
        for key in original:self.assertEqual(stored[key],original[key])
        short=(self.root/'gazete/yazi/ai/test-ai/index.html').read_text()
        detail=(self.root/'gazete/yazi/ai/test-ai/detay/index.html').read_text()
        self.assertNotIn('Kaynak ayrıntısı.',short)
        self.assertEqual(detail.count('Kaynak ayrıntısı.'),400)
        self.assertIn('Kişisel tedavi önerisi değildir.',detail)
        self.assertIn('Detaylı oku',short)
        self.assertIn('Kısa yazıya dön',detail)
        self.assertIn('Gazete ana sayfası',detail)
        self.assertNotIn('https://example.com/source',short)
        self.assertNotIn('https://example.com/detail',detail)
        sources=(self.root/'gazete/kaynaklar/index.html').read_text()
        self.assertIn('https://example.com/source',sources)
        self.assertIn('https://example.com/detail',sources)

    def test_original_equal_or_shorter_is_not_expanded(self):
        for full_text in ['Gerçek kısa kaynak.',bulletin()['topics'][0]['what_happened']]:
            b=bulletin();b['topics'][0]['full_text']=full_text
            g.validate_bundle(bundle(b),NOW)
            g.replace_site(self.root,bundle(b),NOW)
            page=(self.root/'gazete/yazi/morning/test-morning/detay/index.html').read_text()
            self.assertIn('kaynak metni kısa yazıdan daha uzun değildir',page)
            self.assertNotIn('Daha fazla bilgi',page)

    def test_missing_long_source_has_honest_fallback(self):
        self.import_(bulletin())
        page=(self.root/'gazete/yazi/morning/test-morning/detay/index.html').read_text()
        self.assertIn('ayrı bir uzun kaynak anlatımı bulunmuyor',page)
        self.assertEqual(page.count('Tam metin korunur.'),150)
        self.assertNotIn('full_text',self.state()['bulletins'][0]['topics'][0])

    def test_detail_html_and_markdown_links_are_safe(self):
        b=bulletin();b['topics'][0]['full_text']='<script>alert(1)</script>\n\n[Kaynak](https://example.com/ok)\n\n[Kötü](javascript:alert(1))'
        self.import_(b)
        page=(self.root/'gazete/yazi/morning/test-morning/detay/index.html').read_text()
        self.assertNotIn('<script>alert(1)',page)
        self.assertIn('&lt;script&gt;',page)
        self.assertIn('href="https://example.com/ok"',page)
        self.assertNotIn('href="javascript:',page)

    def test_invalid_details_fail_before_any_write(self):
        variants=[]
        for key,value in [('full_text',''),('full_text',None),('full_text','x'*200001),('full_text_sources',[]),('full_text_sources',[{'name':'Bad','url':'javascript:alert(1)','published_at':None}]),('full_text_sections',[{'heading':'H','timestamp':'99:99','url':None,'paragraphs':['Test']}])]:
            b=bulletin();b['topics'][0]['full_text']='Kaynak anlatımı.';b['topics'][0][key]=value;variants.append(b)
        b=bulletin();b['topics'][0]['full_text_sources']=b['topics'][0]['sources'];variants.append(b)
        before=files(self.root)
        for b in variants:
            with self.subTest(b=b):
                with self.assertRaises(g.InvalidBulletin):self.import_(b)
                self.assertEqual(before,files(self.root))

    def test_timestamp_sections_keep_video_links(self):
        b=bulletin();t=b['topics'][0]
        t['full_text']='Giriş.\n\n00:53 · Bölüm başlığı\n\nKaynak çekincesi.'
        t['full_text_sections']=[{'heading':'Bölüm başlığı','timestamp':'00:53','url':'https://www.youtube.com/watch?v=test&t=53s','paragraphs':['Kaynak çekincesi.'],'warning':True}]
        self.import_(b)
        page=(self.root/'gazete/yazi/morning/test-morning/detay/index.html').read_text()
        self.assertIn('00:53 · Bölüm başlığı',page)
        self.assertIn('href="https://www.youtube.com/watch?v=test&amp;t=53s"',page)
        self.assertIn('source-warning',page)

    def test_sources_replace_with_feed_and_other_sources_stay(self):
        self.import_(bulletin('morning','2026-10-02'),bulletin('ai'))
        b=bulletin();b['topics'][0]['id']='replacement';b['topics'][0]['sources'][0]['url']='https://example.com/new'
        self.import_(b)
        page=(self.root/'gazete/kaynaklar/index.html').read_text()
        self.assertNotIn('id="kaynak-morning-test-morning"',page)
        self.assertIn('id="kaynak-morning-replacement"',page)
        self.assertIn('id="kaynak-ai-test-ai"',page)
        self.assertFalse((self.root/'gazete/yazi/morning/test-morning/detay').exists())

    def test_home_groups_cap_at_three_and_category_keeps_all(self):
        b=bulletin();b['topics']=[dict(copy.deepcopy(b['topics'][0]),id=f'topic-{i}') for i in range(5)]
        self.import_(b)
        home=(self.root/'gazete/index.html').read_text()
        category=(self.root/'gazete/konu/bilim/index.html').read_text()
        self.assertEqual(home.count('<article class="story">'),3)
        self.assertEqual(home.count('Detaylı oku'),0)
        self.assertEqual(category.count('<article class="story">'),5)
        self.assertIn('Tümünü gör',home)
        self.assertIn('<details class="freshness">',home)

    def test_morning_uses_full_original_body_without_detail_buttons(self):
        b=bulletin();t=b['topics'][0]
        t['what_happened']='Daha önce kısaltılmış metin.'
        t['full_text']='Özgün kaynak paragrafı.\n\nKaynak çekincesi korunur.\n\n'+'Eksiksiz haber. '*40
        original=copy.deepcopy(t)
        self.import_(b)
        self.assertEqual(self.state()['bulletins'][0]['topics'][0],original)
        article=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
        self.assertIn(g.prose(t['full_text']),article)
        self.assertNotIn('Daha önce kısaltılmış metin.',article)
        for path in ('gazete/index.html','gazete/konu/bilim/index.html','gazete/yazi/morning/test-morning/index.html'):
            page=(self.root/path).read_text()
            self.assertNotIn('Detaylı oku',page)
            self.assertNotIn('/test-morning/detay/',page)
        self.assertTrue((self.root/'gazete/yazi/morning/test-morning/detay/index.html').is_file())

    def test_morning_single_sentence_and_missing_full_text_stay_exact(self):
        for include_full in (False,True):
            b=bulletin();t=b['topics'][0]
            t['what_happened']='Bu kısa haberin özgün tek cümlesi aynen kalır.'
            if include_full:t['full_text']=t['what_happened']
            g.replace_site(self.root,bundle(b),NOW)
            page=(self.root/'gazete/yazi/morning/test-morning/index.html').read_text()
            self.assertIn(g.prose(t['what_happened']),page)
            self.assertEqual(page.count(t['what_happened']),1)
            self.assertNotIn('Detaylı oku',page)

    def test_other_feeds_keep_short_body_and_detail_buttons(self):
        for feed in ('ai','youtube_am','youtube_pm'):
            b=bulletin(feed);t=b['topics'][0];t['full_text']='Yalnız detay sayfasına ait kaynak anlatımı.'
            g.replace_site(self.root,bundle(b),NOW)
            page=(self.root/'gazete'/g.article_path(b,t)/'index.html').read_text()
            self.assertIn(g.prose(t['what_happened']),page)
            self.assertNotIn(t['full_text'],page)
            self.assertIn('Detaylı oku',page)
            self.assertIn('Detaylı oku',g.card(b,t))

    def test_five_feed_contract_and_schema_match(self):
        bs=[bulletin(f) for f in g.FEEDS]
        g.validate_bundle(bundle(*bs),NOW)
        self.assertEqual(len(bs),5)
        schema=json.loads((g.ROOT/'tools/gazete/bundle.schema.json').read_text())
        self.assertEqual(schema['properties']['bulletins']['maxItems'],5)
        self.assertEqual(set(schema['$defs']['bulletin']['properties']['feed_id']['enum']),set(g.FEEDS))
        with self.assertRaises(g.InvalidBulletin):g.validate_bundle(bundle(*bs,bulletin('eksi')),NOW)
        wrong=bulletin('eksi');wrong['scheduled_for']='2026-10-03T19:00:00+03:00'
        with self.assertRaises(g.InvalidBulletin):g.validate_bundle(bundle(wrong),NOW)

    def test_eksi_twenty_topics_keep_original_text_sources_and_uncertainty(self):
        b=bulletin('eksi');prototype=b['topics'][0]
        b['topics']=[dict(copy.deepcopy(prototype),id=f'eksi-test-{i}',category='turkiye' if i%2 else 'kultur',
                          what_happened=f'{i}. yazı yalnız yazılım testi. Görüş kaynağa aittir; kesinleşmiş bulgu değildir.') for i in range(20)]
        original=copy.deepcopy(b)
        self.import_(b)
        self.assertEqual(self.state()['bulletins'][0],original)
        for t in b['topics']:
            page=(self.root/'gazete'/g.article_path(b,t)/'index.html').read_text()
            self.assertIn(g.prose(t['what_happened']),page)
            self.assertNotIn('https://example.com/source',page)
            self.assertNotIn('Detaylı oku',page)
        self.assertIn('https://example.com/source',(self.root/'gazete/kaynaklar/index.html').read_text())
        self.assertIn('Ekşi gündem',(self.root/'gazete/index.html').read_text())

    def test_eksi_replay_and_stale_import_are_noops(self):
        self.import_(*(bulletin(f) for f in g.FEEDS));before=files(self.root)
        self.assertEqual(self.import_(bulletin('eksi'))['duplicate'],['eksi'])
        self.assertEqual(before,files(self.root))
        self.assertEqual(self.import_(bulletin('eksi','2026-10-02'))['stale'],['eksi'])
        self.assertEqual(before,files(self.root))

    def test_eksi_replacement_preserves_other_four_feeds_and_clears_own_sources(self):
        self.import_(*(bulletin(f,'2026-10-02') for f in g.FEEDS))
        old={b['feed_id']:copy.deepcopy(b) for b in self.state()['bulletins'] if b['feed_id']!='eksi'}
        b=bulletin('eksi');b['topics'][0]['id']='eksi-replacement';b['topics'][0]['sources'][0]['url']='https://example.com/eksi-new'
        self.import_(b)
        self.assertEqual({x['feed_id']:x for x in self.state()['bulletins'] if x['feed_id']!='eksi'},old)
        self.assertFalse((self.root/'gazete/yazi/eksi/test-eksi').exists())
        source_page=(self.root/'gazete/kaynaklar/index.html').read_text()
        self.assertNotIn('id="kaynak-eksi-test-eksi"',source_page)
        self.assertIn('id="kaynak-eksi-eksi-replacement"',source_page)
        self.assertEqual(len(self.state()['bulletins']),5)

    def test_concurrent_eksi_and_youtube_pm_keep_both_updates(self):
        from concurrent.futures import ThreadPoolExecutor
        self.import_(*(bulletin(f,'2026-10-02') for f in g.FEEDS))
        with ThreadPoolExecutor(2) as pool:
            results=list(pool.map(lambda b:self.import_(b),[bulletin('eksi'),bulletin('youtube_pm')]))
        latest={b['feed_id']:b for b in self.state()['bulletins']}
        self.assertEqual(len(latest),5)
        self.assertEqual(latest['eksi']['bulletin_id'],'eksi-2026-10-03')
        self.assertEqual(latest['youtube_pm']['bulletin_id'],'youtube_pm-2026-10-03')
        self.assertTrue(all(r['changed'] for r in results))

    def test_eksi_detail_cta_requires_meaningfully_longer_original(self):
        for count in (0,10,110,120,150):
            b=bulletin('eksi');t=b['topics'][0];t['what_happened']='Kısa kaynak. '*50
            if count:t['full_text']='Özgün ' * count
            g.replace_site(self.root,bundle(b),NOW)
            page=(self.root/'gazete'/g.article_path(b,t)/'index.html').read_text()
            self.assertIn(g.prose(t['what_happened']),page)
            expected=count>=120
            self.assertEqual('Detaylı oku' in page,expected)
            self.assertEqual('Detaylı oku' in g.card(b,t),expected)
            if expected:self.assertIn(g.prose(t['full_text']),(self.root/'gazete'/g.detail_path(b,t)/'index.html').read_text())

    def test_eksi_invalid_conflict_preserves_all_five_feeds(self):
        self.import_(*(bulletin(f) for f in g.FEEDS));before=files(self.root)
        b=bulletin('eksi');b['topics'][0]['what_happened']='Çelişkili test değişikliği.'
        with self.assertRaises(g.InvalidBulletin):self.import_(b)
        self.assertEqual(before,files(self.root))

    def test_source_adapter_accepts_eksi_without_rewriting_story(self):
        import sys
        sys.path.insert(0,str(Path(__file__).parent/'gazete'))
        from adapt_source_bundle import adapt
        source={'schema_version':'gundemgazetesi-source-bundle/1','timezone':'Europe/Istanbul','assembled_at':'2026-10-03T20:52:00Z',
                'feeds':[{'id':'eksi_20','edition_date':'2026-10-03','scheduled_time_local':'20:00','generation_completed_at':None,'window':None}],
                'articles':[{'id':'test-eksi-source','feed_id':'eksi_20','topic_id':'turkiye','title':'Test başlığı','summary':'Test özeti.',
                             'what_happened':['Özgün kaynak paragrafı.','Belirsizlik ve atıf korunur.'],'sources':[{'label':'Test','url':'https://example.com'}]}]}
        normalized=adapt(source);g.validate_bundle(normalized,NOW)
        b=normalized['bulletins'][0]
        self.assertEqual(b['feed_id'],'eksi')
        self.assertEqual(b['topics'][0]['what_happened'],'Özgün kaynak paragrafı.\n\nBelirsizlik ve atıf korunur.')
        self.assertIsNone(b['completed_at']);self.assertIsNone(b['coverage_start'])

    def test_verified_eksi_adapter_preserves_story_sources_order_and_times(self):
        import sys
        sys.path.insert(0,str(Path(__file__).parent/'gazete'))
        from adapt_eksi_bundle import adapt
        b=bulletin('eksi');t=b['topics'][0];t['category']='Ekonomi ve denetim'
        source=dict(bundle(b),prepared_at='2026-10-03T20:52:00Z')
        evidence={'prepared_at':source['prepared_at'],'original_completed_at':b['completed_at'],'total_topics':1,
                  'selection_cutoff_note':'Görüşlerin bir örneklemi; bütün kayıtlar taranmadı.',
                  'source_date_note':'Bilinmeyen tarih uydurulmadı.',
                  'topics':[{'id':t['id'],'pdf_page':2,'original_topic_url':t['sources'][0]['url']}]}
        original=copy.deepcopy(source);result=adapt(source,evidence);g.validate_bundle(result,NOW)
        self.assertEqual(source,original)
        topic=result['bulletins'][0]['topics'][0]
        for name in ('id','title','summary','what_happened','sources'):self.assertEqual(topic[name],t[name])
        self.assertEqual(topic['category'],'ekonomi')
        self.assertEqual(topic['metadata']['original_category'],'Ekonomi ve denetim')
        self.assertEqual(result['bulletins'][0]['prepared_at'],source['prepared_at'])
        self.assertIn('bütün kayıtlar taranmadı',result['bulletins'][0]['metadata']['coverage_note'])
        self.assertEqual(adapt(result,evidence),result)
        bad=copy.deepcopy(evidence);bad['total_topics']=2
        with self.assertRaises(g.InvalidBulletin):adapt(source,bad)
        bad=copy.deepcopy(evidence);bad['prepared_at']='2026-10-03T20:51:00Z'
        with self.assertRaises(g.InvalidBulletin):adapt(source,bad)
        bad_source=copy.deepcopy(source);bad_source['bulletins'][0]['topics'][0]['category']='Tanımsız kategori'
        with self.assertRaises(g.InvalidBulletin):adapt(bad_source,evidence)

    def test_details_adapter_preserves_short_fields_and_rejects_mismatches(self):
        import sys
        sys.path.insert(0,str(Path(__file__).parent/'gazete'))
        from add_full_details import attach
        current=bundle(bulletin())
        source={'schema_version':'gundemgazetesi-full-details/1','assembled_at':'2026-10-03T10:00:00+03:00','details_by_article_id':{'test-morning':{
            'article_id':'test-morning','feed_id':'general_morning_08','full_text':'Özgün metin.',
            'sections':[{'heading':None,'timestamp':None,'paragraphs':['Özgün metin.']}],
            'sources':[{'label':'Özgün kaynak','url':'https://example.com/original'}],
            'provenance':[{'source_id':'original','library_file_id':'private-id'}]}}}
        original=copy.deepcopy(current)
        result=attach(current,source);g.validate_bundle(result,NOW)
        self.assertEqual(current,original)
        old=original['bulletins'][0]['topics'][0];new=result['bulletins'][0]['topics'][0]
        for key in old:self.assertEqual(old[key],new[key])
        self.assertNotEqual(result['bulletins'][0]['bulletin_id'],original['bulletins'][0]['bulletin_id'])
        self.assertNotIn('private-id',json.dumps(result))
        self.assertEqual(attach(result,source),result)
        bad=copy.deepcopy(source);bad['details_by_article_id']['test-morning']['feed_id']='ai_21'
        with self.assertRaises(g.InvalidBulletin):attach(current,bad)
        bad=copy.deepcopy(source);bad['details_by_article_id']['extra']=bad['details_by_article_id']['test-morning']
        with self.assertRaises(g.InvalidBulletin):attach(current,bad)


if __name__=='__main__':unittest.main(verbosity=2)
