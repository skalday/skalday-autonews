import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import json
import sys
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

ITEMS_PER_SOURCE = 10
HOURS_WINDOW = 24

def fetch_rss_feeds(file_path):
    sources = _parse_source_file(file_path)
    results = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for category, urls in sources.items():
        results[category] = []
        for url in urls:
            entries = _fetch_single_feed(url, headers)
            results[category].append({"url": url, "entries": entries})
            total = sum(len(s["entries"]) for s in results[category])
            print(f"  [{category}] {url} => {len(entries)} articles (category total: {total})", file=sys.stderr)

    return results


def _parse_source_file(file_path):
    sources = {}
    current_category = "General"
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                current_category = line[1:-1]
                sources.setdefault(current_category, [])
            else:
                sources.setdefault(current_category, []).append(line)
    return sources


def _encode_url(url):
    parts = urllib.parse.urlsplit(url)
    encoded = parts._replace(
        path=urllib.parse.quote(parts.path, safe='/:@!$&\'()*+,;='),
        query=urllib.parse.quote(parts.query, safe='=&+:@!$\'()*,;/?')
    )
    return urllib.parse.urlunsplit(encoded)


def _parse_pubdate(raw):
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


ATOM_NS = 'http://www.w3.org/2005/Atom'


def _normalize_raw(raw):
    """Re-encode EUC-KR (or other non-UTF-8) XML to UTF-8 so ElementTree can parse it."""
    import re as _re
    m = _re.search(rb'encoding=["\']([^"\']+)["\']', raw[:200])
    if not m:
        return raw
    enc = m.group(1).decode('ascii', 'ignore').lower()
    if enc in ('utf-8', 'utf8'):
        return raw
    try:
        text = raw.decode(enc)
        text = _re.sub(r'encoding=["\'][^"\']+["\']', 'encoding="utf-8"', text, count=1)
        return text.encode('utf-8')
    except Exception:
        return raw


def _extract_entries(root):
    """Return (items, format) handling both RSS <item> and Atom <entry>."""
    items = root.findall('.//item')
    if items:
        return items, 'rss'
    entries = root.findall(f'.//{{{ATOM_NS}}}entry')
    return entries, 'atom'


def _entry_fields(el, fmt):
    if fmt == 'rss':
        title = el.findtext('title', '').strip()
        link = el.findtext('link', '').strip()
        pub_raw = el.findtext('pubDate', '')
        summary = (el.findtext('description', '') or '')[:300].strip()
    else:
        title = (el.findtext(f'{{{ATOM_NS}}}title', '') or '').strip()
        link_el = el.find(f'{{{ATOM_NS}}}link')
        link = (link_el.get('href', '') if link_el is not None else '').strip()
        pub_raw = el.findtext(f'{{{ATOM_NS}}}published', '') or el.findtext(f'{{{ATOM_NS}}}updated', '')
        summary = (el.findtext(f'{{{ATOM_NS}}}summary', '') or '')[:300].strip()
    return title, link, pub_raw, summary


def _fetch_single_feed(url, headers):
    try:
        req = urllib.request.Request(_encode_url(url), headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = _normalize_raw(response.read())
        root = ET.fromstring(raw)
        elements, fmt = _extract_entries(root)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_WINDOW)
        entries = []
        for el in elements[:ITEMS_PER_SOURCE]:
            title, link, pub_raw, summary = _entry_fields(el, fmt)
            pub_dt = _parse_pubdate(pub_raw)
            if pub_dt is not None and pub_dt < cutoff:
                continue
            entries.append({
                "title": title,
                "link": link,
                "pub_date": pub_dt.isoformat() if pub_dt else None,
                "summary": summary
            })
        return entries
    except Exception as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    from pathlib import Path
    file_path = Path(__file__).parent.parent / "config" / "rss_sources.txt"
    print(f"Fetching RSS feeds from {file_path}...", file=sys.stderr)
    data = fetch_rss_feeds(str(file_path))
    total = sum(len(e) for cat in data.values() for s in cat for e in [s["entries"]])
    print(f"\nTotal articles fetched: {total}", file=sys.stderr)
    print(json.dumps(data, indent=2, ensure_ascii=False))
