# News Auto — 專案說明

## 研究定位

這是一個服務學術研究的新聞自動化分析管道，不是娛樂觀察工具。

**研究核心**：以數位人類學視角，探索偶像／遊戲／娛樂產業在亞洲地緣政治版圖的競合關係。  
**方法論立場**：空間規畫的量化方法作為探索框架（方法論仍在發展中）。  
**關注交集**：虛擬偶像 × 遊戲 × 音樂 × 平台演算法 × 文化政策。  
**分析框架**：Digital-Physical Entanglement（數位-實體糾纏），觀察數位流量如何影響實體場域的資源配置與空間政治。  
**訊號標準**：產業結構、政策動向、平台權力關係、跨國資本流動。排除純娛樂八卦與藝人私生活。

---

## 執行流程

```
RSS 抓取 (fetcher.py) → Claude 分析 (analyzer.py) → Markdown 週報 (courier.py)
```

需要 `.env` 設定 `ANTHROPIC_API_KEY`。

```bash
python run.py                   # 完整跑全流程
python run.py --skip-fetch      # 跳過抓取，重用 news_data.json
python run.py --skip-analyze    # 跳過分析，重用 analysis_data.json
```

---

## 關鍵檔案

| 檔案／資料夾 | 用途 |
|---|---|
| `rss_sources.txt` | RSS 來源，分 Japanese / Thai / Korean 三個語系 |
| `fetcher.py` | 抓取 RSS，輸出 `data/news_data.json` |
| `analyzer.py` | 呼叫 Claude API 分析，輸出 `data/analysis_data.json` |
| `analyzer_schema.json` | 分析輸出的 JSON schema |
| `courier.py` | 生成 `reports/report_YYYYMMDD.md` 週報 |
| `run.py` | 串接三個步驟的 orchestrator |
| `data/` | 中間資料：`news_data.json`（原始抓取）、`analysis_data.json`（分析結果） |
| `reports/` | 輸出週報，每次執行生成一份 `report_YYYYMMDD.md` |

---

## 分析 JSON 結構（每篇文章）

```json
{
  "title": "原始標題",
  "original_link": "連結",
  "category": "Japanese / Thai / Korean",
  "summary_zh": "100字以內繁體中文摘要",
  "analysis": {
    "location": { "city": "城市", "specific_node": "具體場域或平台" },
    "keywords": ["關鍵詞陣列，涵蓋產業、平台、政策、行為者、地緣節點"],
    "digital_physical_entanglement": "數位輿論流動如何與實體空間互動（2-3句）"
  },
  "signal_strength": "high / medium / low"
}
```

**注意**：`signal_strength` 的判斷標準尚未明確定義，是已知的待優化項目。

---

## 常見任務

### 跑本週分析

直接執行 `python run.py`。若 RSS 來源有問題，先用 `--skip-fetch` 確認分析流程正常。

### 討論優化

目前已知可優化的環節：

1. ~~**篩選邏輯**：現在每個語系盲取前 5 篇~~  
   → **已完成**：`analyzer.py` 現在是兩段式——先由 Claude 依研究框架從全部候選標題中挑選（`_select_articles()`），再對選中文章做深度分析（`_analyze_article()`）。最多 5 篇／語系，無相關訊號可為 0 篇。
2. **`signal_strength` 標準**：目前由 Claude 自由判斷，缺乏明確的研究導向判斷條件。
3. **跨語系比較**：目前三個語系分開分析，JSON 層面沒有跨文章關聯機制。
4. **`digital_physical_entanglement` 描述品質**：框架尚在探索，描述深度不穩定。

### GitHub Actions 自動化（待下次對話實作）

目標：每天定時自動跑完整流程，報告 commit 回 repo。

已確認可行，下次對話需要做：
1. `git init` + 建立 GitHub repo
2. 建立 `.github/workflows/daily.yml`（cron 排程，跑 `python run.py`）
3. 將 `ANTHROPIC_API_KEY` 存入 repo secrets
4. workflow 結尾自動 commit 新報告回 `reports/` 資料夾

### 調整研究框架

研究方法論仍在發展中。若要調整分析角度，主要修改：
- `analyzer.py` 的 `SYSTEM_PROMPT`（系統角色定位）
- `_analyze_article()` 裡的 prompt（輸出欄位與描述指引）
- `analyzer_schema.json`（同步更新 schema）
- `courier.py` 的 `_format_article()`（報告顯示格式）
