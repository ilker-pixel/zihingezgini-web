#!/usr/bin/env python3
"""Weekly health check for the cited external sources in all summaries."""

from __future__ import annotations

import concurrent.futures
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARD_FAILURES = {404, 410}


def source_urls() -> list[str]:
    urls = set()
    for path in (ROOT / "data" / "summaries").glob("*.json"):
        summary = json.loads(path.read_text(encoding="utf-8"))
        urls.update(source.get("url", "") for source in summary.get("sources", []))
    return sorted(url for url in urls if url.startswith(("http://", "https://")))


def request_status(url: str, context, method: str) -> int:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ZihinGezgini-LinkMonitor/1.0)"}
    if method == "GET":
        headers["Range"] = "bytes=0-1024"
    request = urllib.request.Request(url, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=15, context=context) as response:
        return response.status


def check_with_context(url: str, context) -> tuple[int | None, str | None]:
    try:
        return request_status(url, context, "HEAD"), None
    except urllib.error.HTTPError as error:
        if error.code in {404, 405, 410}:
            try:
                return request_status(url, context, "GET"), None
            except urllib.error.HTTPError as get_error:
                if get_error.code in {403, 429}:
                    return get_error.code, None
                return get_error.code, str(get_error)
        if error.code in {403, 429}:
            return error.code, None
        return error.code, str(error)
    except Exception as error:
        raise error


def check(url: str) -> tuple[str, int | None, str | None]:
    try:
        status, error = check_with_context(url, ssl.create_default_context())
        return url, status, error
    except urllib.error.URLError as error:
        if "CERTIFICATE_VERIFY_FAILED" not in str(error):
            return url, None, str(error)
        try:
            status, fallback_error = check_with_context(url, ssl._create_unverified_context())
            return url, status, fallback_error or "certificate verification fallback"
        except Exception as fallback_error:
            return url, None, str(fallback_error)
    except Exception as error:
        return url, None, str(error)


def main() -> int:
    urls = source_urls()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(check, urls))
    failures = [(url, status) for url, status, _ in results if status in HARD_FAILURES]
    warnings = [(url, error) for url, status, error in results if status is None and error]
    print(f"Checked {len(urls)} external sources: {len(failures)} hard failures, {len(warnings)} transient warnings.")
    for url, status in failures:
        print(f"- HTTP {status}: {url}")
    for url, error in warnings[:20]:
        print(f"! transient: {url} ({error})")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
