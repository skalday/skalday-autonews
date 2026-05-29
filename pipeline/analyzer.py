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


_ANALYZE_PROMPT_TEMPLATE = """請針對以下新聞進行數位人類學分析，並輸出 JSON。

標題：{title}
摘要：{summary}
連結：{link}
語言分類：{category}

輸出必須完全符合此 JSON 結構，不要包含 markdown 標籤或其他文字：
{{
  "title": "原始標題",
  "original_link": "連結",
  "category": "語言分類",
  "summary_zh": "200字以內的繁體中文摘要。貼合原文內容翻譯，中立客觀描述新聞重點，不加入分析或評論。",
  "analysis": {{
    "location": ["事件發生的城市或具體場域，每個地點獨立一項，若無明確地點則留空陣列"],
    "actors": ["行動者或相關組織名稱，每個獨立一項，共1至3項。包含主動發起行動的主體與直接受影響的客體"],
    "keywords": ["研究關鍵詞1（從產業結構／平台權力／文化政策／地緣競合中擇一切入）", "研究關鍵詞2", "研究關鍵詞3"],
    "actor_logic": "一句話描述行動者在此事件中的個體利益考量與行動動機。聚焦於「這個主體為何在此時此刻選擇這樣做」，可涉及商業利益、聲譽管理、市場卡位等個體層次的判斷。若新聞無明確單一行動者，則描述推動事件發生的主導力量。",
    "structural_change": "一句話描述行動者背後的結構力量（產業邏輯、平台權力、資本關係、政策框架）如何透過這個行動作用於其他客體（粉絲社群、競爭者、監管機構、實體場域）。重點是「誰或什麼被這個行動影響，以及影響的傳導機制是什麼」。",
    "trend_implication": "一句話描述被影響的客體背後存在什麼結構性脈絡，這個脈絡與行動者的結構碰撞之後，指向什麼更大的產業、地緣或文化趨勢變化。"
  }}
}}

location 填入事件相關的實體地點，純數位事件（平台政策、線上輿論）若無對應實體場域則留空陣列 []。
actors 填入人名或組織名，不填職稱描述。
keywords 填入3個詞，每個詞對應一個分析維度，不重複、不使用過於寬泛的詞（如「娛樂產業」）。{extra}"""


def _analyze_article(entry):
    def _build_prompt(extra=""):
        return _ANALYZE_PROMPT_TEMPLATE.format(
            title=entry['title'],
            summary=entry.get('summary', '（無摘要）'),
            link=entry['link'],
            category=entry['category'],
            extra=extra,
        )

    text = _extract_json(_call_claude(_build_prompt()))
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  JSON parse error ({e}), retrying with escaping hint...", file=sys.stderr)
        retry_note = "\n\n重要：輸出 JSON 時，所有字串值內的雙引號必須以 \\\" 跳脫，不得出現未跳脫的裸引號。"
        text = _extract_json(_call_claude(_build_prompt(retry_note)))
        return json.loads(text)


def run_analyzer(raw_data):
    candidates = _collect_candidates(raw_data)
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
                analysis = _analyze_article(entry)
                results["articles"].append(analysis)
                results["metadata"]["total_entries"] += 1
            except Exception as e:
                print(f"  Error: {e}", file=sys.stderr)

        results["metadata"]["categories"][category] = len(selected)

    results["metadata"]["daily_digest"] = _generate_daily_digest(results["articles"])
    return results


def _generate_daily_digest(articles):
    if not articles:
        return ""
    listing = "\n".join(
        f"- [{a.get('category', '')}] {a.get('title', '')}：{a.get('summary_zh', '')[:60]}"
        for a in articles
    )
    prompt = f"""以下是今天篩選出的新聞清單，每條附有標題與簡短摘要：

{listing}

請用一句話（60字以內），中立客觀地讓讀者快速了解今天篩選了哪些面向的新聞，不加入分析或評論。只輸出這一句話，不要加任何前綴或標點符號以外的文字。"""
    try:
        return _call_claude(prompt).strip()
    except Exception as e:
        print(f"  Daily digest error: {e}", file=sys.stderr)
        return ""


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
