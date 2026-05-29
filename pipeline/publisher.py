import json
import html as html_lib
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"

SITE_URL = "https://skalday.github.io/skalday-autonews"
SITE_TITLE = "SkalDay AutoNews"
SITE_DESC = "每天多思考一些流行文化新聞"

_FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '  <link href="https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@600'
    '&family=Noto+Sans+TC:wght@300&family=Oleo+Script:wght@700'
    '&family=Inter:wght@400;700&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">'
)

_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #F2F2F2;
  font-family: 'Noto Sans TC', 'Inter', sans-serif;
  font-weight: 300;
  font-size: 14px;
  line-height: 1.8;
  color: #111111;
}
a { color: #0051ba; text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3, h4, h5, h6 {
  font-family: 'Chiron GoRound TC', 'Inter', sans-serif;
  font-weight: 600;
  color: #111111;
  line-height: 1.4;
}
h1 { font-size: 26px; }
h2 { font-size: 20px; }
h3 { font-size: 16px; }
h4, h5, h6 { font-size: 14px; }
p { margin-bottom: 8px; }
.meta {
  font-family: 'Courier Prime', 'Noto Sans TC', monospace;
  font-size: 12px;
  color: #0051ba;
  margin-bottom: 6px;
}
.win98-box {
  background: #c0c0c0;
  border-top: 2px solid #ffffff;
  border-left: 2px solid #ffffff;
  border-right: 2px solid #555555;
  border-bottom: 2px solid #555555;
  margin-bottom: 16px;
}
.win98-title-bar {
  background: #0051ba;
  color: #ffffff;
  font-family: 'Inter', 'Chiron GoRound TC', sans-serif;
  font-size: 12px;
  font-weight: 700;
  padding: 3px 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.win98-body {
  background: #F2F2F2;
  margin: 2px;
  padding: 12px 14px;
}
.win98-inset {
  background: #F2F2F2;
  border-top: 2px solid #555555;
  border-left: 2px solid #555555;
  border-right: 2px solid #ffffff;
  border-bottom: 2px solid #ffffff;
  padding: 8px 10px;
  font-family: 'Noto Sans TC', 'Inter', sans-serif;
  font-weight: 300;
  font-size: 13px;
  color: #111111;
  margin: 8px 0;
}
.win98-cta {
  display: inline-block;
  background: #2E5BB8;
  color: #ffffff;
  font-family: 'Inter', 'Noto Sans TC', sans-serif;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 24px;
  border-top: 3px solid #0051ba;
  border-left: 3px solid #0051ba;
  border-right: 3px solid #0F2B5B;
  border-bottom: 3px solid #0F2B5B;
  text-decoration: none;
  margin-top: 10px;
}
.win98-cta:active {
  border-top: 3px solid #0F2B5B;
  border-left: 3px solid #0F2B5B;
  border-right: 3px solid #0051ba;
  border-bottom: 3px solid #0051ba;
}
.tag {
  display: inline-block;
  background: #F2F2F2;
  color: #0051ba;
  font-family: 'Noto Sans TC', 'Inter', sans-serif;
  font-weight: 300;
  font-size: 11px;
  padding: 2px 8px;
  border: 1px solid #0051ba;
  margin: 2px 2px 0 0;
}
.tag-primary {
  background: #0051ba;
  color: #F2F2F2;
  border-color: #0F2B5B;
  font-family: 'Courier Prime', 'Noto Sans TC', monospace;
  font-weight: 700;
}
.nl-preview {
  max-width: 760px;
  margin: 0 auto;
  background: #F2F2F2;
  border: 2px solid #111111;
}
.nl-header {
  background: #0051ba;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 3px solid #0F2B5B;
}
.nl-title {
  font-family: 'Oleo Script', system-ui;
  font-size: 22px;
  color: #F2F2F2;
  font-weight: 700;
}
.nl-body { padding: 16px; }
.nl-section-head {
  font-family: 'Courier Prime', 'Chiron GoRound TC', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #0051ba;
  letter-spacing: 2px;
  text-transform: uppercase;
  border-bottom: 1px solid #0051ba;
  padding-bottom: 4px;
  margin-bottom: 10px;
  margin-top: 20px;
}
.nl-footer {
  background: #111111;
  color: #F2F2F2;
  font-family: 'Courier Prime', 'Noto Sans TC', monospace;
  font-size: 11px;
  padding: 8px 16px;
}
.nl-footer a { color: #0051ba; }
.nl-header a { color: #F2F2F2; text-decoration: none; }
.nl-header a:hover { text-decoration: none; color: #ffed00; }
.report-list { list-style: none; }
"""


def _e(text):
    return html_lib.escape(str(text))


def _week_range_str(date_str):
    d = datetime.strptime(date_str, "%Y%m%d")
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%Y%m%d')}~{sunday.strftime('%Y%m%d')}"


def _rss_date(date_str):
    d = datetime.strptime(date_str, "%Y%m%d")
    return d.strftime("%a, %d %b %Y 00:00:00 +0000")


def _article_html(article):
    analysis = article.get("analysis", {})
    location = analysis.get("location", [])
    actors = analysis.get("actors", [])
    keywords = analysis.get("keywords", [])
    actor_logic = analysis.get("actor_logic", "")
    structural_change = analysis.get("structural_change", "")
    trend_implication = analysis.get("trend_implication", "")
    title = article.get("title", "")
    link = article.get("original_link", "#")
    summary = article.get("summary_zh", "")

    all_tags = (location or ["純數位"]) + actors + keywords
    tag_html = " ".join(f'<span class="tag">{_e(t)}</span>' for t in all_tags)

    analysis_html = (
        f'<p style="margin-bottom:6px"><span class="meta">從新聞了解行為</span><br>{_e(actor_logic)}</p>'
        f'<p style="margin-bottom:6px"><span class="meta">從行為了解結構</span><br>{_e(structural_change)}</p>'
        f'<p style="margin-bottom:0"><span class="meta">從結構了解趨勢</span><br>{_e(trend_implication)}</p>'
    )

    return f"""<div class="win98-box">
  <div class="win98-title-bar">
    <span>&#9733;</span>
    <span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{_e(title)}</span>
  </div>
  <div class="win98-body">
    <p>{_e(summary)}</p>
    <div class="win98-inset">{analysis_html}</div>
    <p style="margin-top:8px;margin-bottom:6px">{tag_html}</p>
    <a href="{_e(link)}" target="_blank" rel="noopener">&#8594; 閱讀新聞原文</a>
  </div>
</div>"""


def _report_html(analysis_data, date_str):
    date_formatted = datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
    meta = analysis_data.get("metadata", {})
    total = meta.get("total_entries", 0)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    daily_digest = meta.get("daily_digest", "")

    by_category = {}
    for article in analysis_data.get("articles", []):
        cat = article.get("category", "其他")
        by_category.setdefault(cat, []).append(article)

    sections = []
    for cat, articles in by_category.items():
        articles_html = "\n".join(_article_html(a) for a in articles)
        sections.append(articles_html)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_TITLE} {date_formatted}</title>
  {_FONTS}
  <style>{_CSS}</style>
</head>
<body>
<div class="nl-preview">
  <div class="nl-header">
    <a href="index.html" class="nl-title">{SITE_TITLE}</a>
  </div>
  <div class="nl-body">
    <h2>&#9733; {date_formatted}</h2>
    <p class="meta">生成時間：{generated_at}　總計：{total} 篇</p>
    {'<p style="margin-bottom:12px">' + _e(daily_digest) + '</p>' if daily_digest else ''}
    <p style="margin-bottom:16px"><a href="index.html">&#8592; 返回彙整</a></p>
{"".join(sections)}
  </div>
  <div class="nl-footer">
    <p>&#169; {SITE_TITLE} &nbsp;|&nbsp; <a href="feed.xml">RSS 訂閱</a> &nbsp;|&nbsp; {SITE_DESC}</p>
  </div>
</div>
</body>
</html>"""


def _index_html(reports):
    items = []
    for r in reports:
        date_str = r["date"]
        total = r.get("total_entries", 0)
        cats = r.get("categories", {})
        cat_str = "　".join(f"{k} {v}篇" for k, v in cats.items())
        digest = r.get("daily_digest", "")
        digest_html = f'<p style="margin-bottom:8px">{_e(digest)}</p>' if digest else ""
        items.append(f"""<li>
  <div class="win98-box">
    <div class="win98-title-bar">
      <span>&#9733;</span>
      <span style="flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis">{_e(date_str)}</span>
    </div>
    <div class="win98-body">
      <p class="meta">{_e(cat_str)} &nbsp;|&nbsp; 共 {total} 篇</p>
      {digest_html}<a href="{_e(date_str)}.html">&#8594; 看更多</a>
    </div>
  </div>
</li>""")

    items_html = "\n".join(items)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_TITLE}</title>
  {_FONTS}
  <style>{_CSS}</style>
</head>
<body>
<div class="nl-preview">
  <div class="nl-header">
    <a href="index.html" class="nl-title">{SITE_TITLE}</a>
  </div>
  <div class="nl-body">
    <ul class="report-list">
{items_html}
    </ul>
  </div>
  <div class="nl-footer">
    <p>&#169; {SITE_TITLE} &nbsp;|&nbsp; <a href="feed.xml">RSS 訂閱</a> &nbsp;|&nbsp; {SITE_DESC}</p>
  </div>
</div>
</body>
</html>"""


def _feed_xml(analysis_data, date_str, index):
    pub_date = _rss_date(date_str)

    items = []
    for r in index:
        d = r["date"]
        wr = r.get("week_range", d)
        total = r.get("total_entries", 0)
        link = f"{SITE_URL}/{d}.html"
        pd = _rss_date(d)
        items.append(f"""    <item>
      <title>SkalDay AutoNews - {d}</title>
      <link>{link}</link>
      <guid>{link}</guid>
      <pubDate>{pd}</pubDate>
      <description>本期收錄 {total} 則新聞摘要</description>
    </item>""")

    items_xml = "\n".join(items)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{SITE_URL}</link>
    <description>{SITE_DESC}</description>
    <language>zh-Hant</language>
    <lastBuildDate>{pub_date}</lastBuildDate>
{items_xml}
  </channel>
</rss>"""


def publish(analysis_data):
    DOCS_DIR.mkdir(exist_ok=True)

    date_str = analysis_data["metadata"]["date"].replace("-", "")

    report_html = _report_html(analysis_data, date_str)
    (DOCS_DIR / f"{date_str}.html").write_text(report_html, encoding="utf-8")

    index_file = DOCS_DIR / "index.json"
    index = json.loads(index_file.read_text(encoding="utf-8")) if index_file.exists() else []
    entry = {
        "date": date_str,
        "week_range": _week_range_str(date_str),
        "total_entries": analysis_data["metadata"]["total_entries"],
        "categories": analysis_data["metadata"].get("categories", {}),
        "daily_digest": analysis_data["metadata"].get("daily_digest", ""),
    }
    index = [e for e in index if e["date"] != date_str] + [entry]
    index.sort(key=lambda e: e["date"], reverse=True)
    index_file.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    (DOCS_DIR / "index.html").write_text(_index_html(index), encoding="utf-8")
    (DOCS_DIR / "feed.xml").write_text(_feed_xml(analysis_data, date_str, index), encoding="utf-8")

    return DOCS_DIR


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    data_file = BASE_DIR / "data" / "analysis_data.json"
    if not data_file.exists():
        print("找不到 data/analysis_data.json", file=sys.stderr)
        sys.exit(1)

    analysis_data = json.loads(data_file.read_text(encoding="utf-8"))
    docs_dir = publish(analysis_data)
    print(f"Published to: {docs_dir}", file=sys.stderr)
