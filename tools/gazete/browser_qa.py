#!/usr/bin/env python3
"""Optional Playwright visual QA on an isolated local HTTP server; no deployment."""
import argparse
import datetime as dt
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]


def main():
    p=argparse.ArgumentParser();p.add_argument('--artifacts',type=Path,required=True)
    args=p.parse_args();args.artifacts.mkdir(parents=True,exist_ok=True)
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
        def log_message(self,*a):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    origin=f'http://127.0.0.1:{server.server_port}'
    pages=sorted((ROOT/'gazete').rglob('*.html'))
    checks=[]
    try:
        with sync_playwright() as pw:
            executable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
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
                        if page.locator('.prose h2').inner_text()!='Ne oldu?':raise AssertionError('Article structure')
                        if page.locator('.prose p').count()<1:raise AssertionError('Article text missing')
                checks.append({'width':width,'pages':len(pages),'overflow':False})
                page.goto(origin+'/gazete/',wait_until='networkidle')
                if width in (1440,390):
                    page.screenshot(path=str(args.artifacts/f'gazete-home-{width}.png'),full_page=True)
                    page.screenshot(path=str(args.artifacts/f'gazete-home-{width}-preview.png'))
                article=next((ROOT/'gazete/yazi').rglob('index.html'))
                page.goto(origin+'/'+str(article.relative_to(ROOT)),wait_until='networkidle')
                if width==390:
                    page.screenshot(path=str(args.artifacts/'gazete-article-mobile.png'),full_page=True)
                    page.screenshot(path=str(args.artifacts/'gazete-article-mobile-preview.png'))
            page.clock.install(time=dt.datetime.fromisoformat('2026-10-04T08:01:00+03:00'))
            page.goto(origin+'/gazete/',wait_until='networkidle')
            statuses=page.locator('.freshness .status').all_inner_texts()
            if statuses!=['Yeni bülten bekleniyor','Son bülten hazır','Son bülten hazır','Son bülten hazır']:
                raise AssertionError(f'Client freshness clock: {statuses}')
            if page.locator('.story').count()!=41:raise AssertionError('Freshness must not remove stories')
            if errors:raise AssertionError(errors)
            browser.close()
        report={'viewports':checks,'freshness_clock':True,'js_errors':errors,'deployment':False,'mac_off_test':False}
        (args.artifacts/'browser-qa.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report))
    finally:
        server.shutdown();server.server_close()


if __name__=='__main__':main()
