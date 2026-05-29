import json
import sys
import subprocess
import re
from datetime import datetime

MAX_PER_CATEGORY = 5

SYSTEM_PROMPT = """你是一位專注於「數位人類學」的研究助理。你的分析必須基於以下原則：
1. 關注「數位資訊」與「物理空間」之間互相影響的關係（Digital-Physical Entanglement）。
2. 挖掘具體的空間政治表現：社群平台上的數位流動如何引導人流進入特定的實體場域（演唱會、快閃店、粉絲聚集點），反之亦然。
3. 請保持中立分析角度。"""

RESEARCH_FOCUS = """研究關注交集：偶像 × 遊戲 × 音樂 × 演算法 × 文化政策。
訊號標準（有其中一項即值得納入）：
- 產業結構變動（廠牌擴張、資本併購、企業決策）
- 政策動向（文化政策、數位管制、政府介入）
- 平台權力關係（演算法、平台治理、數位輿論管理）
- 跨國資本流動（品牌合作、跨境偶像、地緣競合）
- 數位流量與實體場域的具體連結（演唱會、快閃店、展覽、粉絲聚集）

排除：純娛樂八卦、藝人私生活、單純 MV／單曲發布公告、與上述框架無交集的一般新聞。"""


def _call_claude(prompt):
    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
    result = subprocess.run(
        'claude',
        input=full_prompt,
        capture_output=True,
        text=True,
        encoding='utf-8',
        shell=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI error: {result.stderr.strip()}")
    output = result.stdout.strip()
    if not output:
        raise RuntimeError(f"claude CLI returned empty output. stderr: {result.stderr.strip()}")
    return output


def _extract_json(text):
    # Strip markdown code fences if Claude wraps output in them
    text = re.sub(r'^```(?:json)?\n?', '', text.strip())
    text = re.sub(r'\n?```$', '', text.strip())
    return text.strip()


def _load_signal_examples():
    from pathlib import Path
    feedback_file = Path(__file__).parent.parent / "data" / "signal_feedback.json"
    if not feedback_file.exists():
        return []
    with open(feedback_file, encoding='utf-8') as f:
        return json.load(f)


def _build_examples_context(signal_examples):
    if not signal_examples:
        return ""
    high = [e for e in signal_examples if e["user_signal"] == "high"][-4:]
    low  = [e for e in signal_examples if e["user_signal"] == "low"][-4:]
    if not high and not low:
        return ""
    parts = ["以下是研究者標記過的參考案例，請參考這些案例校準你的 signal_strength 判斷：\n"]
    for e in high:
        kws = ', '.join(e.get('keywords', [])[:5])
        parts.append(f"[研究者標記: high] {e['title']}")
        parts.append(f"  關鍵詞: {kws}")
    for e in low:
        kws = ', '.join(e.get('keywords', [])[:5])
        parts.append(f"[研究者標記: low] {e['title']}")
        parts.append(f"  關鍵詞: {kws}")
    return "\n".join(parts) + "\n\n"


def _collect_candidates(raw_data):
    candidates = {}
    for category, sources in raw_data.items():
        seen = set()
        articles = []
        for source in sources:
            for entry in source.get("entries", []):
                title = entry.get("title", "").strip()
                if title and title not in seen:
                    seen.add(title)
                    articles.append({**entry, "category": category})
        candidates[category] = articles
    return candidates


def _select_articles(category, articles):
    listing = "\n".join(
        f"{i}. {a['title']}｜{a.get('summary', '')[:80]}"
        for i, a in enumerate(articles)
    )
    prompt = f"""以下是 {category} 語系的新聞標題清單。請依照研究框架，挑出值得深入分析的文章。

{RESEARCH_FOCUS}

最多選 {MAX_PER_CATEGORY} 篇，沒有符合的可以選 0 篇。

清單：
{listing}

請只輸出一個 JSON 陣列，內容為選中文章的編號（0-based index），例如 [0, 3, 5]。不要包含任何其他文字。"""

    text = _extract_json(_call_claude(prompt))
    indices = json.loads(text)
    selected = [articles[i] for i in indices if 0 <= i < len(articles)]
    print(f"  Selected indices: {indices} → {len(selected)} articles", file=sys.stderr)
    return selected


def _analyze_article(entry, signal_examples=None):
    examples_context = _build_examples_context(signal_examples)
    prompt = f"""請針對以下新聞進行文化地緣政治分析，並輸出 JSON。

{examples_context}標題：{entry['title']}
摘要：{entry.get('summary', '（無摘要）')}
連結：{entry['link']}
語言分類：{entry['category']}

輸出必須完全符合此 JSON 結構，不要包含 markdown 標籤或其他文字：
{{
  "title": "原始標題",
  "original_link": "連結",
  "category": "語言分類",
  "summary_zh": "100字以內的繁體中文摘要",
  "analysis": {{
    "tags": [
      "事件地點（城市或具體場域，1-2個詞）",
      "事件名稱（1個詞）",
      "相關人物或組織名稱（1-3個詞，每個詞獨立一項）",
      "研究關鍵詞1（與產業/平台/政策/地緣相關）",
      "研究關鍵詞2",
      "研究關鍵詞3"
    ],
    "digital_physical_entanglement": "深入描述數位輿論流動如何與實體空間互動（2-3句）"
  }},
  "signal_strength": "high/medium/low"
}}

tags 陣列請依序填入：事件地點 → 事件名稱 → 相關人物或組織 → 3個研究關鍵詞，共6至9個項目。每個項目為一個字串。"""

    text = _extract_json(_call_claude(prompt))
    return json.loads(text)


def run_analyzer(raw_data):
    candidates = _collect_candidates(raw_data)
    signal_examples = _load_signal_examples()
    if signal_examples:
        print(f"  Loaded {len(signal_examples)} signal feedback examples.", file=sys.stderr)
    results = {
        "metadata": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source_category": "Digital-Anthropology-Research",
            "total_entries": 0,
            "categories": {}
        },
        "articles": []
    }

    for category, articles in candidates.items():
        if not articles:
            continue
        print(f"\n[{category}] {len(articles)} candidates → selecting...", file=sys.stderr)
        try:
            selected = _select_articles(category, articles)
        except Exception as e:
            print(f"  Selection error: {e}, falling back to first {MAX_PER_CATEGORY}", file=sys.stderr)
            selected = articles[:MAX_PER_CATEGORY]
        print(f"  → analyzing {len(selected)}...", file=sys.stderr)

        for i, entry in enumerate(selected, 1):
            print(f"  ({i}/{len(selected)}) {entry['title'][:60]}...", file=sys.stderr)
            try:
                analysis = _analyze_article(entry, signal_examples=signal_examples)
                results["articles"].append(analysis)
                results["metadata"]["total_entries"] += 1
            except Exception as e:
                print(f"  Error: {e}", file=sys.stderr)

        results["metadata"]["categories"][category] = len(selected)

    return results


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    try:
        raw_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    results = run_analyzer(raw_data)
    print(json.dumps(results, indent=2, ensure_ascii=False))
