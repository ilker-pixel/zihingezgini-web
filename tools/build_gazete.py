#!/usr/bin/env python3
"""Import completed bulletins and render only /gazete/. No network/model calls."""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TR = ZoneInfo("Europe/Istanbul")
FEEDS = {
    "morning": ("Sabah gündemi", 8),
    "ai": ("AI gündemi", 21),
    "youtube_am": ("YouTube sabah", 10),
    "youtube_pm": ("YouTube akşam", 22),
}
CATEGORIES = {
    "bilim": "Bilim", "teknoloji": "Teknoloji", "ekonomi": "Ekonomi",
    "dunya": "Dünya", "turkiye": "Türkiye", "kultur": "Kültür",
    "saglik": "Sağlık", "cevre": "Çevre", "spor": "Spor",
    "felsefe": "Zihin ve Felsefe", "hava": "Hava Durumu",
}
ORIGIN = "https://zihingezgini.net"
MAX_BYTES = 4_000_000


class InvalidBulletin(ValueError):
    pass


def fail(message):
    raise InvalidBulletin(message)


def fields(obj, required, optional=(), label="nesne"):
    if not isinstance(obj, dict):
        fail(f"{label}: nesne gerekli")
    missing = set(required) - obj.keys()
    unknown = obj.keys() - set(required) - set(optional)
    if missing or unknown:
        fail(f"{label}: eksik={sorted(missing)}, tanımsız={sorted(unknown)}")


def text(value, label, maximum, single_line=False):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        fail(f"{label}: boş olmayan, en çok {maximum} karakterli metin gerekli")
    if any(ord(c) < 32 and c not in "\n\t" for c in value):
        fail(f"{label}: kontrol karakteri")
    if single_line and ("\n" in value or "\r" in value):
        fail(f"{label}: tek satır gerekli")
    return value.strip()


def identifier(value, label):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}", value):
        fail(f"{label}: güvenli, en çok 96 karakterli kimlik gerekli")
    return value


def timestamp(value, label):
    if not isinstance(value, str):
        fail(f"{label}: saat dilimli ISO 8601 gerekli")
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{label}: geçersiz ISO 8601")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        fail(f"{label}: saat dilimi gerekli")
    return parsed


def source_date(value):
    if value is None:
        return
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            dt.date.fromisoformat(value)
            return
        except ValueError:
            pass
    timestamp(value, "kaynak yayın tarihi")


def metadata(value, label):
    if not isinstance(value, dict) or len(canonical(value)) > 40_000:
        fail(f"{label}: en çok 40.000 karakterli JSON nesnesi gerekli")


def order(b):
    return (timestamp(b["scheduled_for"], "slot"),
            timestamp(b.get("prepared_at") or b["completed_at"], "paket hazırlama/tamamlanma"))


def validate_bulletin(b, now):
    fields(b, ("feed_id", "bulletin_id", "scheduled_for", "completed_at", "coverage_start",
               "coverage_end", "topics"), ("prepared_at", "metadata"), label="bülten")
    feed = b["feed_id"]
    if not isinstance(feed, str) or feed not in FEEDS:
        fail("tanımsız kaynak bülten")
    identifier(b["bulletin_id"], "bulletin_id")
    scheduled = timestamp(b["scheduled_for"], "scheduled_for")
    completed = timestamp(b["completed_at"], "completed_at") if b["completed_at"] is not None else None
    prepared = timestamp(b["prepared_at"], "prepared_at") if b.get("prepared_at") else None
    if completed is None and prepared is None:
        fail("tamamlanma saati bilinmiyorsa ayrı prepared_at gerekli")
    start = timestamp(b["coverage_start"], "coverage_start") if b["coverage_start"] is not None else None
    end = timestamp(b["coverage_end"], "coverage_end") if b["coverage_end"] is not None else None
    local = scheduled.astimezone(TR)
    if (local.hour, local.minute, local.second, local.microsecond) != (FEEDS[feed][1], 0, 0, 0):
        fail(f"{feed}: Türkiye saati {FEEDS[feed][1]:02}:00 bekleniyor")
    if bool(start) != bool(end) or (start and (start > end or end > (completed or prepared))):
        fail("bilinen kapsam başlangıcı <= kapsam sonu <= tamamlanma/paket zamanı gerekli")
    if any(t and t > now + dt.timedelta(minutes=5) for t in (completed, prepared, scheduled)):
        fail("gelecekteki bülten yayımlanamaz")
    if "metadata" in b:
        metadata(b["metadata"], "bülten metaverisi")
        bm = b['metadata']
        if bm.get('delivered_at'): timestamp(bm['delivered_at'], 'teslim zamanı')
        cutoff = bm.get('research_cutoff')
        if cutoff is not None:
            if not isinstance(cutoff, dict): fail('research_cutoff: nesne gerekli')
            if cutoff.get('at'): timestamp(cutoff['at'], 'araştırma kesimi')
        gaps = bm.get('source_gaps')
        if gaps is not None and (not isinstance(gaps, list) or any(not isinstance(x,dict) for x in gaps)):
            fail('source_gaps: nesne listesi gerekli')
    topics = b["topics"]
    if not isinstance(topics, list) or not 1 <= len(topics) <= 30:
        fail("bülten 1–30 tamamlanmış konu içermeli")
    seen = set()
    for t in topics:
        fields(t, ("id", "category", "title", "summary", "what_happened", "sources"), ("metadata",), label="konu")
        identifier(t["id"], "konu kimliği")
        if t["id"] in seen:
            fail("yinelenen konu kimliği")
        seen.add(t["id"])
        if not isinstance(t["category"], str) or t["category"] not in CATEGORIES:
            fail("tanımsız konu kategorisi")
        text(t["title"], "başlık", 160, True)
        text(t["summary"], "tek cümle özet", 500, True)
        text(t["what_happened"], "Ne oldu?", 50_000)
        if "metadata" in t:
            metadata(t["metadata"], "konu metaverisi")
            if "publication" in t["metadata"]:
                pub = t["metadata"]["publication"]
                if not isinstance(pub, dict): fail("publication: nesne gerekli")
                source_date(pub.get("at"))
                source_date(pub.get("date"))
            event = t['metadata'].get('event_time')
            if event is not None:
                if not isinstance(event,dict):fail('event_time: nesne gerekli')
                source_date(event.get('start'))
                source_date(event.get('end'))
        if not isinstance(t["sources"], list) or not 1 <= len(t["sources"]) <= 32:
            fail("konu 1–32 kaynak içermeli")
        for s in t["sources"]:
            fields(s, ("name", "url", "published_at"), label="kaynak")
            text(s["name"], "kaynak adı", 160, True)
            url = text(s["url"], "kaynak URL", 2048, True)
            try:
                u = urlsplit(url)
                good = u.scheme in ("http", "https") and u.hostname and not u.username and not u.password
            except ValueError:
                good = False
            if not good or any(c.isspace() for c in url):
                fail("kaynak URL: kimlik bilgisi içermeyen HTTP(S) adresi gerekli")
            source_date(s["published_at"])
    return b


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_json(path):
    raw = Path(path).read_bytes()
    if len(raw) > MAX_BYTES:
        fail("JSON paketi 4 MB sınırını aşıyor")
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail(f"yinelenen JSON alanı: {key}")
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=unique_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"JSON okunamadı: {exc}")


def validate_bundle(bundle, now):
    fields(bundle, ("schema_version", "bulletins"), label="paket")
    if type(bundle["schema_version"]) is not int or bundle["schema_version"] != 1:
        fail("schema_version=1 gerekli")
    if not isinstance(bundle["bulletins"], list) or not 1 <= len(bundle["bulletins"]) <= 4:
        fail("paket 1–4 bülten içermeli")
    seen = set()
    for b in bundle["bulletins"]:
        validate_bulletin(b, now)
        if b["feed_id"] in seen:
            fail("pakette aynı kaynak iki kez bulunamaz")
        seen.add(b["feed_id"])


def load_current(root, now):
    path = root / "gazete/data/current.json"
    if not path.exists():
        return {"schema_version": 1, "bulletins": []}
    current = read_json(path)
    fields(current, ("schema_version", "bulletins"), label="durum")
    if current.get("bulletins"):
        validate_bundle(current, now)
    elif current != {"schema_version": 1, "bulletins": []}:
        fail("geçersiz boş durum")
    return current


def merge(current, bundle):
    by_feed = {b["feed_id"]: b for b in current["bulletins"]}
    changed, duplicate, stale = [], [], []
    for b in bundle["bulletins"]:
        feed = b["feed_id"]
        old = by_feed.get(feed)
        if old:
            if b["bulletin_id"] == old["bulletin_id"]:
                # Repackaging the same completed text is not a new bulletin.
                if canonical({k:v for k,v in b.items() if k != 'prepared_at'}) != canonical({k:v for k,v in old.items() if k != 'prepared_at'}):
                    fail(f"{feed}: aynı bulletin_id farklı içerikle gönderildi")
                duplicate.append(feed)
                continue
            new_order, old_order = order(b), order(old)
            if new_order < old_order:
                stale.append(feed)
                continue
            if new_order == old_order:
                fail(f"{feed}: aynı yayın zamanı için çelişkili bülten")
        by_feed[feed] = b
        changed.append(feed)
    result = {"schema_version": 1, "bulletins": [by_feed[f] for f in FEEDS if f in by_feed]}
    if len(canonical(result).encode()) > MAX_BYTES:
        fail("birleşik durum 4 MB sınırını aşıyor")
    return result, {"changed": changed, "duplicate": duplicate, "stale": stale}


def esc(value):
    return html.escape(str(value), quote=True)


def date_label(value):
    if value is None:
        return "Yayın tarihi kaynakta belirtilmemiş"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return dt.date.fromisoformat(value).strftime("%d.%m.%Y")
    return timestamp(value, "tarih").astimezone(TR).strftime("%d.%m.%Y %H.%M") + " TSİ"


def article_path(b, topic):
    return f"yazi/{b['feed_id']}/{topic['id']}/"


def shell(title, body, categories, route="", active=""):
    nav = ''.join(f'<a href="/gazete/konu/{c}/"{chr(32)+"aria-current=\"page\"" if c == active else ""}>{esc(CATEGORIES[c])}</a>' for c in categories)
    return f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · Gündem Gazetesi</title><meta name="description" content="Tamamlanmış bültenlerden, konuya göre düzenlenen günlük gazete.">
<link rel="canonical" href="{ORIGIN}/gazete/{route}"><link rel="stylesheet" href="/gazete/static/style.css"></head>
<body><a class="skip" href="#icerik">İçeriğe geç</a><header class="masthead"><a class="brand" href="/gazete/">Gündem Gazetesi</a><p>Dünyadan gelişmeler, açık bir dille.</p>
<nav aria-label="Gazete konuları">{nav}</nav></header><main id="icerik">{body}</main>
<footer>Gündem Gazetesi · Saatler Türkiye saatidir. Kaynakların yayın tarihleri yazıların içinde yer alır.</footer><script src="/gazete/static/freshness.js" defer></script></body></html>'''


def card(b, t):
    label = FEEDS[b["feed_id"]][0]
    return f'''<article class="story"><p class="eyebrow">{esc(CATEGORIES[t['category']])} <span>· {esc(label)}</span></p>
<h2><a href="/gazete/{article_path(b,t)}">{esc(t['title'])}</a></h2><p>{esc(t['summary'])}</p>
<a class="read" href="/gazete/{article_path(b,t)}">Yazıyı oku <span aria-hidden="true">→</span></a></article>'''


def freshness(current, now):
    by_feed = {b["feed_id"]: b for b in current["bulletins"]}
    rows = []
    for feed, (label, hour) in FEEDS.items():
        expected = now.astimezone(TR).replace(hour=hour, minute=0, second=0, microsecond=0)
        if expected > now:
            expected -= dt.timedelta(days=1)
        b = by_feed.get(feed)
        late = b is None or timestamp(b["scheduled_for"], "slot") < expected
        status = "Yeni bülten bekleniyor" if late else "Son bülten hazır"
        content = ('<span>Tamamlanma saati belirtilmemiş</span>' if b and b['completed_at'] is None else
                   f'<time datetime="{esc(b["completed_at"])}">{date_label(b["completed_at"])}</time>') if b else '<span>Henüz bülten yok</span>'
        if b: content += f'<small>Bülten saati: {date_label(b["scheduled_for"])}</small>'
        slot = b["scheduled_for"] if b else ""
        rows.append(f'<li data-hour="{hour}" data-slot="{esc(slot)}"><strong>{label}</strong><span class="status" aria-live="polite">{status}</span>{content}</li>')
    return '<aside class="freshness" aria-label="Bülten güncelliği"><h2>Son bültenler</h2><ul>' + ''.join(rows) + '</ul><p>Yeni bülten geldiğinde yalnız o kaynağın yazıları yenilenir. Bekleyen bültenlerde son yazılar okunmaya devam eder.</p></aside>'


def render(current, output, now):
    output.mkdir(parents=True)
    (output / "data").mkdir()
    (output / "data/current.json").write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "static").mkdir()
    css = (ROOT / "tools/gazete/style.css").read_text(encoding="utf-8")
    (output / "static/style.css").write_text(css, encoding="utf-8")
    shutil.copyfile(ROOT / "tools/gazete/freshness.js", output / "static/freshness.js")
    shutil.copyfile(ROOT / "tools/gazete/bundle.schema.json", output / "bundle.schema.json")
    pairs = [(b,t) for b in current["bulletins"] for t in b["topics"]]
    pairs.sort(key=lambda pair: timestamp(pair[0]["scheduled_for"], "slot"), reverse=True)
    categories = [c for c in CATEGORIES if any(t["category"] == c for _,t in pairs)]
    routes = []
    def write(route, title, body, active=""):
        dest = output / route / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(shell(title, body, categories, route, active), encoding="utf-8")
        routes.append(route)
    lead = '<section class="intro"><p class="eyebrow">GÜNLÜK GAZETE</p><h1>Bugün ne oldu?</h1><p>Bilimden ekonomiye, günün gelişmeleri ve onları anlatan yazılar.</p></section>'
    stories = ''.join(card(b,t) for b,t in pairs) or '<p class="empty">İlk tamamlanmış bülten geldiğinde yazılar burada yer alacak.</p>'
    write("", "Bugün ne oldu?", lead + freshness(current, now) + '<section class="stories" aria-label="Son yazılar">' + stories + '</section>')
    for c in categories:
        write(f"konu/{c}/", CATEGORIES[c], f'<section class="intro"><p class="eyebrow">KONU</p><h1>{CATEGORIES[c]}</h1></section><section class="stories">' + ''.join(card(b,t) for b,t in pairs if t["category"] == c) + '</section>', c)
    for b,t in pairs:
        paragraphs = ''.join(f'<p>{esc(p.strip())}</p>' for p in re.split(r"\n\s*\n", t["what_happened"]) if p.strip())
        sources = ''.join(f'<li><a href="{esc(s["url"])}" rel="noopener noreferrer">{esc(s["name"])}</a><span>{date_label(s["published_at"])}</span></li>' for s in t["sources"])
        tm, bm = t.get('metadata', {}), b.get('metadata', {})
        pub = tm.get('publication', {})
        source_time = pub.get('at') or pub.get('date')
        notes = []
        if source_time: notes.append(f'Yayın/kayıt tarihi: {date_label(source_time)}')
        if pub.get('note'): notes.append(esc(pub['note']))
        event = tm.get('event_time', {})
        if event.get('start'): notes.append(f'Olay başlangıcı: {date_label(event["start"])}')
        if event.get('end'): notes.append(f'Olay sonu: {date_label(event["end"])}')
        if event.get('note'): notes.append(esc(event['note']))
        completed_label = date_label(b['completed_at']) if b['completed_at'] else 'Kaynakta belirtilmemiş'
        timing = [f'Bülten tamamlandı: {completed_label}']
        if b.get('prepared_at'): timing.append(f'Paket hazırlandı: {date_label(b["prepared_at"])}')
        if b['coverage_start']:
            timing.append(f'Kapsanan dönem: {date_label(b["coverage_start"])} – {date_label(b["coverage_end"])}')
        else: timing.append('Kesin kapsam başlangıcı ve sonu kaynakta belirtilmemiş')
        if bm.get('delivered_at'): timing.append(f'Teslim: {date_label(bm["delivered_at"])}')
        cutoff = bm.get('research_cutoff') or {}
        if cutoff.get('at'): timing.append(f'Araştırma kesimi: {date_label(cutoff["at"])} ({esc(cutoff.get("precision", ""))})')
        if cutoff.get('note'): timing.append(esc(cutoff['note']))
        if bm.get('coverage_note'): timing.append(esc(bm['coverage_note']))
        for gap in bm.get('source_gaps') or []:
            timing.append('Bekleyen kaynak: ' + esc(gap.get('title','')) + '. ' + esc(gap.get('reason','')))
        source_notes = ''.join(f'<p class="coverage">{n}</p>' for n in notes)
        timing_html = '<br>'.join(timing)
        body = f'''<article class="article"><a class="back" href="/gazete/konu/{t['category']}/">← {CATEGORIES[t['category']]}</a>
<p class="eyebrow">{FEEDS[b['feed_id']][0]} · Bülten: {date_label(b['scheduled_for'])}</p><h1>{esc(t['title'])}</h1><p class="dek">{esc(t['summary'])}</p>
<section class="prose"><h2>Ne oldu?</h2>{paragraphs}</section><section class="sources"><h2>Kaynaklar</h2><ul>{sources}</ul>{source_notes}</section>
<p class="coverage">{timing_html}</p></article>'''
        write(article_path(b,t), t["title"], body, t["category"])
    # Old newspaper URLs terminate here rather than retaining obsolete topics/editions.
    (output / "404.html").write_text(shell("Yazı bulunamadı", '<section class="intro"><h1>Bu yazı artık güncel gazetede yok.</h1><p><a href="/gazete/">Son yazılara dön</a></p></section>', categories), encoding="utf-8")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{ORIGIN}/gazete/{r}</loc></url>\n' for r in routes) + '</urlset>\n'
    (output / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (output / ".nojekyll").write_text("", encoding="utf-8")


@contextlib.contextmanager
def locked(root):
    # Keep lock and staging outside the tracked tree. Serializes import/read/merge/render.
    token = hashlib.sha256(str(root.resolve()).encode()).hexdigest()[:24]
    lock = Path(tempfile.gettempdir()) / f"gazete-{token}.lock"
    with lock.open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def replace_site(root, current, now):
    target = root / "gazete"
    recovery = root / ".gazete-previous"
    if recovery.exists():
        if not target.exists():
            recovery.rename(target)
        else:
            shutil.rmtree(recovery)
    stage_parent = Path(tempfile.mkdtemp(prefix=".gazete-stage-", dir=root))
    try:
        stage = stage_parent / "gazete"
        render(current, stage, now)
        if target.exists():
            target.rename(recovery)
        try:
            stage.rename(target)
        except BaseException:
            if recovery.exists() and not target.exists():
                recovery.rename(target)
            raise
        if recovery.exists():
            shutil.rmtree(recovery)
    finally:
        shutil.rmtree(stage_parent, ignore_errors=True)


def import_bundle(root, bundle, now):
    validate_bundle(bundle, now)  # Validate all feeds before changing any feed.
    with locked(root):
        recovery = root / ".gazete-previous"
        if recovery.exists() and not (root / "gazete").exists():
            recovery.rename(root / "gazete")
        current = load_current(root, now)
        merged, result = merge(current, bundle)
        if result["changed"]:
            replace_site(root, merged, now)
        return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--import-bundle", type=Path)
    group.add_argument("--check-bundle", type=Path)
    group.add_argument("--render", action="store_true")
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--now", help="Test/preview clock only; production uses real UTC time")
    args = p.parse_args(argv)
    now = timestamp(args.now, "now") if args.now else dt.datetime.now(dt.timezone.utc)
    root = args.root.resolve()
    if not root.is_dir() or root == Path('/') or root == Path.home():
        p.error("mevcut depo/önizleme kök dizini gerekli")
    try:
        if args.check_bundle:
            validate_bundle(read_json(args.check_bundle), now)
            result = {"valid": True}
        elif args.import_bundle:
            result = import_bundle(root, read_json(args.import_bundle), now)
        else:
            with locked(root):
                replace_site(root, load_current(root, now), now)
            result = {"rendered": True}
        print(json.dumps(result, ensure_ascii=False))
    except (InvalidBulletin, OSError) as exc:
        print(f"Gazete değişmedi: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
