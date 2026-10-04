#!/usr/bin/env python3
"""Optional Playwright visual QA on an isolated local HTTP server; no deployment."""
import argparse
import datetime as dt
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import shutil
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--artifacts',type=Path,required=True)
    p.add_argument('--browser',help='Existing Chromium/Chrome executable; no install')
    args=p.parse_args();args.artifacts.mkdir(parents=True,exist_ok=True)
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    origin=f'http://127.0.0.1:{server.server_port}'
    pages=sorted((ROOT/'gazete').rglob('*.html'))
    checks=[]
    state=json.loads((ROOT/'gazete/data/current.json').read_text())
    topics=[t for b in state['bulletins'] for t in b['topics']]
    categories={t['category'] for t in topics}
    home_count=sum(min(3,sum(t['category']==c for t in topics)) for c in categories)
    first_story=[]
    try:
        with sync_playwright() as pw:
            executable=args.browser or shutil.which('chromium') or shutil.which('google-chrome')
            browser=pw.chromium.launch(executable_path=executable,headless=True,args=['--disable-background-networking','--disable-component-update','--disable-sync'])
            context=browser.new_context()
            page=context.new_page();errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            for width,height in [(1440,1000),(768,1024),(390,844),(320,720)]:
                page.set_viewport_size({'width':width,'height':height})
                for path in pages:
                    route='/'+str(path.relative_to(ROOT))
                    response=page.goto(origin+route,wait_until='load')
                    if response.status!=200:raise AssertionError(f'{route}: HTTP {response.status}')
                    sizes=page.evaluate('({body:document.body.scrollWidth,root:document.documentElement.scrollWidth,viewport:innerWidth})')
                    if max(sizes['body'],sizes['root'])>width:raise AssertionError(f'{route}, {width}: overflow {sizes}')
                    if page.locator('main').count()!=1:raise AssertionError(f'{route}: main missing')
                    if page.locator('.article').count():
                        expected='Kaynak anlatımı' if page.locator('.detail-article').count() else 'Ne oldu?'
                        if page.locator('.prose h2').first.inner_text()!=expected:raise AssertionError('Article structure')
                        if page.locator('.prose p').count()<1:raise AssertionError('Article text missing')
                        if page.locator('.source-list').count():raise AssertionError('Sources must be on separate page')
                checks.append({'width':width,'pages':len(pages),'overflow':False})
                page.goto(origin+'/gazete/',wait_until='networkidle')
                if page.locator('.freshness').get_attribute('open') is not None:raise AssertionError('Update info should be closed')
                if page.locator('.topic-group').count()!=len(categories):raise AssertionError('Category grouping')
                for box in page.locator('.story-actions a,.group-heading a,.masthead nav a').evaluate_all('(els)=>els.map(e=>({height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width}))'):
                    if box['height']<44 or box['width']<44:raise AssertionError(f'Tap area: {box}')
                story_top=page.locator('.story').first.bounding_box()['y']
                first_story.append({'width':width,'top':round(story_top,1)})
                if width<=390 and not 340<=story_top<=410:raise AssertionError(f'First mobile story too low/high: {story_top}')
                if width in (1440,390):
                    page.screenshot(path=str(args.artifacts/f'gazete-home-{width}.png'),full_page=True)
                    page.screenshot(path=str(args.artifacts/f'gazete-home-{width}-preview.png'))
                article=next((ROOT/'gazete/yazi').rglob('index.html'))
                page.goto(origin+'/'+str(article.relative_to(ROOT)),wait_until='networkidle')
                if width==390:
                    page.screenshot(path=str(args.artifacts/'gazete-article-mobile.png'),full_page=True)
                    page.screenshot(path=str(args.artifacts/'gazete-article-mobile-preview.png'))
                    page.locator('.detail-read').click()
                    if page.locator('.source-narrative').count()!=1:raise AssertionError('Detail navigation')
                    page.screenshot(path=str(args.artifacts/'gazete-detail-mobile-preview.png'))
                    page.goto(origin+'/gazete/kaynaklar/',wait_until='networkidle')
                    page.screenshot(path=str(args.artifacts/'gazete-sources-mobile-preview.png'))
            page.clock.install(time=dt.datetime.fromisoformat('2026-10-04T08:01:00+03:00'))
            page.goto(origin+'/gazete/',wait_until='networkidle')
            page.locator('.freshness summary').click()
            statuses=page.locator('.freshness .status').all_inner_texts()
            if statuses!=['Yeni bülten bekleniyor','Son bülten hazır','Son bülten hazır','Son bülten hazır']:
                raise AssertionError(f'Client freshness clock: {statuses}')
            if page.locator('.story').count()!=home_count:raise AssertionError('Freshness must not remove stories')
            if not page.locator('.freshness ul').is_visible():raise AssertionError('Update accordion')
            if errors:raise AssertionError(errors)
            browser.close()
        report={'viewports':checks,'first_story':first_story,'homepage_stories':home_count,'tap_targets_min_px':44,'freshness_clock':True,'js_errors':errors,'deployment':False,'mac_off_test':False}
        (args.artifacts/'browser-qa.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report))
    finally:
        server.shutdown();server.server_close()


if __name__=='__main__':main()
