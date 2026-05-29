#!/usr/bin/env python3
"""
News Automation Pipeline Orchestrator
Usage: python run.py [--skip-fetch] [--skip-analyze] [--skip-publish]
  --skip-fetch     Reuse existing news_data.json
  --skip-analyze   Reuse existing analysis_data.json
  --skip-publish   Skip static site generation
"""
import json
import sys
import io
import os
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_DIR = Path(__file__).parent
(BASE_DIR / "data").mkdir(exist_ok=True)


def _load_dotenv():
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved: {path}")


def step_fetch(skip=False):
    news_file = BASE_DIR / "data" / "news_data.json"
    if skip and news_file.exists():
        print(f"[1/4] SKIP fetch — loading {news_file}")
        return load_json(news_file)

    print("[1/4] Fetching RSS feeds...")
    from pipeline.fetcher import fetch_rss_feeds
    data = fetch_rss_feeds(str(BASE_DIR / "config" / "rss_sources.txt"))
    save_json(data, news_file)
    total = sum(len(e["entries"]) for cat in data.values() for e in cat)
    print(f"      Fetched {total} articles across {len(data)} categories.\n")
    return data


def step_analyze(raw_data, skip=False):
    analysis_file = BASE_DIR / "data" / "analysis_data.json"
    if skip and analysis_file.exists():
        print(f"[2/4] SKIP analyze — loading {analysis_file}")
        return load_json(analysis_file)

    print("[2/4] Running analysis via claude CLI...")
    from pipeline.analyzer import run_analyzer
    results = run_analyzer(raw_data)
    save_json(results, analysis_file)
    print(f"      Analyzed {results['metadata']['total_entries']} articles.\n")
    return results


def step_courier(analysis_data):
    print("[3/4] Generating report...")
    from pipeline.courier import generate_report
    report = generate_report(analysis_data)

    date_str = datetime.now().strftime("%Y%m%d")
    report_file = BASE_DIR / "reports" / f"report_{date_str}.md"
    report_file.write_text(report, encoding='utf-8')
    print(f"      Report saved: {report_file}\n")
    return report_file


def step_publish(analysis_data):
    print("[4/4] Publishing to docs/...")
    from pipeline.publisher import publish
    docs_dir = publish(analysis_data)
    print(f"      Published: {docs_dir}\n")
    return docs_dir


def main():
    args = set(sys.argv[1:])

    skip_fetch = "--skip-fetch" in args
    skip_analyze = "--skip-analyze" in args
    skip_publish = "--skip-publish" in args

    print("=" * 50)
    print("  News Automation Pipeline")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50 + "\n")

    raw_data = step_fetch(skip=skip_fetch)
    analysis_data = step_analyze(raw_data, skip=skip_analyze)
    report_file = step_courier(analysis_data)
    if not skip_publish:
        step_publish(analysis_data)

    print("=" * 50)
    print(f"Done! Report: {report_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
