import json
import sys
from datetime import datetime, timedelta


def _week_range():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return f"{monday.strftime('%Y%m%d')}~{sunday.strftime('%Y%m%d')}"



def generate_report(analysis_data):
    date_range = _week_range()
    lines = []

    lines.append(f"# SkalDay 週報 {date_range}")
    lines.append(f"\n> 生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 總計分析：{analysis_data['metadata']['total_entries']} 篇\n")

    lines.append("---\n")
    lines.append("## 本週重點摘要\n")
    lines.append(_generate_executive_summary(analysis_data))
    lines.append("\n---\n")

    # Group articles by category
    by_category = {}
    for article in analysis_data.get("articles", []):
        cat = article.get("category", "其他")
        by_category.setdefault(cat, []).append(article)

    for category, articles in by_category.items():
        lines.append(f"## {category} 新聞分析\n")
        for article in articles:
            lines.append(_format_article(article))
        lines.append("---\n")

    return "\n".join(lines)


def _generate_executive_summary(analysis_data):
    by_category = {}
    for a in analysis_data.get("articles", []):
        cat = a.get("category", "其他")
        by_category.setdefault(cat, []).append(a["title"])
    summary_lines = []
    for cat, titles in by_category.items():
        summary_lines.append(f"**{cat}**：{len(titles)} 篇")
        for t in titles:
            summary_lines.append(f"- {t}")
    return "\n".join(summary_lines)


def _format_article(article):
    analysis = article.get("analysis", {})
    location = analysis.get("location", [])
    actors = analysis.get("actors", [])
    keywords = analysis.get("keywords", [])
    actor_logic = analysis.get("actor_logic", "")
    structural_change = analysis.get("structural_change", "")
    trend_implication = analysis.get("trend_implication", "")

    location_str = "、".join(location) if location else "（純數位）"
    actors_str = "、".join(actors) if actors else "N/A"
    keywords_str = "、".join(keywords) if keywords else "N/A"

    lines = [
        f"### {article.get('title', 'N/A')}",
        f"",
        f"**場域**：{location_str}　**行動者**：{actors_str}",
        f"",
        f"**摘要**：{article.get('summary_zh', 'N/A')}",
        f"",
        f"**行動邏輯**：{actor_logic}",
        f"",
        f"**結構作用**：{structural_change}",
        f"",
        f"**趨勢指向**：{trend_implication}",
        f"",
        f"**關鍵詞**：{keywords_str}",
        f"",
        f"🔗 [{article.get('title', '')}]({article.get('original_link', '#')})",
        f"",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    try:
        analysis_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(analysis_data)
    from pathlib import Path
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = Path(__file__).parent / "reports" / f"report_{date_str}.md"
    output_file.write_text(report, encoding='utf-8')
    print(f"Report saved to: {output_file}", file=sys.stderr)
    print(report)
