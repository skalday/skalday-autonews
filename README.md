# SkalDay AutoNews

[English](#english) | [中文](#中文)

---

<a name="english"></a>

## The Struture Behind the Pop Culture

SkalDay AutoNews is an automated daily newsletter covering the business side of pop culture across Japan, Korea, and Thailand.
<img width="2110" height="1198" alt="skalday autonews header" src="https://github.com/user-attachments/assets/354bf421-25f3-4d53-ba07-7dbacf4029e9" />

[![Website](https://img.shields.io/badge/Newsletter-Read%20Online-blue)](https://skalday.github.io/skalday-autonews)
[![RSS](https://img.shields.io/badge/RSS-Subscribe-orange)](https://skalday.github.io/skalday-autonews/feed.xml)
[![License](https://img.shields.io/github/license/skalday/skalday-autonews)](LICENSE)

## What We Track

- **Industry moves**: label expansions, mergers, corporate decisions
- **Policy shifts**: cultural policy, content regulation, government intervention
- **Platform power**: algorithmic changes, content governance, digital PR management
- **Cross-border capital**: brand deals, transnational idol projects, geopolitical competition
- **Digital-to-physical flows**: how online fandoms drive foot traffic to concerts, pop-ups, and fan events

## From News to Trend: The Analysis Framework

Every piece starts from a single news event and works outward: what happened, why it happened, and where it might be heading.

> **★ Streaming Chart Watch | A virtual idol, idol group A, and idol group B compete for algorithm visibility in the same week**
>
> A Japanese music media outlet's weekly streaming column tracked a sudden surge in YouTube music video rankings. Three very different acts competed for the same algorithmic spotlight in one week: a virtual idol riding a viral track, idol group A leaning into personality contrast, and idol group B projecting raw intensity.
>
> **What happened**
> All three released music videos timed to their release cycles, optimizing for the short burst window the algorithm rewards. The virtual idol showing up in this arena at all is itself the signal worth noting.
>
> **Why it happened**
> The platform's ranking logic puts virtual idols and human idol groups inside the same visibility framework, collapsing the audience silos that used to be separated by media channel. Fanbases that never competed before are now fighting for the same stream counts.
>
> **Where it's heading**
> The virtual-vs-physical boundary in the idol industry is blurring at the platform level. Long-term, this could reshape how resources flow across concerts, merchandise, and the physical spaces where fans gather.

## Heads Up

This newsletter is AI-generated, filtered through a manually configured editorial lens. Treat the analysis as a starting point for your own thinking, not a final word. The framework is still evolving, and feedback and suggestions are welcome via Issues.

## Self-Hosting

<details>
<summary>Deploy your own version with custom news sources</summary>

**Requirements**
- Python 3
- [Claude Code CLI](https://claude.ai/code) (must be logged in)

**Steps**

1. Clone the repo

```bash
git clone https://github.com/skalday/skalday-autonews.git
cd skalday-autonews
```

2. Set your news sources in `config/rss_sources.txt`

```
[Category A]
https://feed-1.com/rss
https://feed-2.com/rss
[Category B]
https://feed-3.com/rss
```

3. Run

```bash
python run.py
```

Output: Markdown reports in `reports/` and a static site in `docs/`.

</details>

<details>
<summary>Customize the analysis framework</summary>

Edit the prompt in `pipeline/analyzer.py`.

</details>

---

<a name="中文"></a>

## 用產業視角讀流行文化

SkalDay AutoNews 自動彙整日本、韓國、泰國流行文化產業新聞。

[![Website](https://img.shields.io/badge/電子報網站-線上閱讀-blue)](https://skalday.github.io/skalday-autonews)
[![RSS](https://img.shields.io/badge/RSS-訂閱-orange)](https://skalday.github.io/skalday-autonews/feed.xml)
[![License](https://img.shields.io/github/license/skalday/skalday-autonews)](LICENSE)

## 新聞篩選標準

- 廠牌擴張、資本併購、企業決策等**產業結構變動**
- 文化政策、數位管制、政府介入等**政策動向**
- 演算法、平台治理、數位輿論管理等**平台權力關係**
- 品牌合作、跨境偶像、地緣競合等**跨國資本流動**
- 演唱會、快閃店、展覽等**數位流量與實體場域的連結**

## 新聞摘要分析架構

每則分析從單一新聞事件出發，逐層往上推：行為、結構、趨勢。範例如下：

> **★ 串流排行榜定點觀測｜虛擬偶像、偶像團體 A、偶像團體 B 同台競爭串流資源**
>
> 某日本音樂媒體的週刊串流觀測專欄，紀錄近期 YouTube 音樂影片排行榜的急升動向。本期聚焦三組截然不同的行動者：以特定曲目衝榜的虛擬偶像，展現虛擬偶像在串流平台的獨特存在性；偶像團體 A 以個性反差作為賣點；偶像團體 B 則呈現強烈的意志感。三組題材橫跨不同系譜的偶像，在同一週的演算法排行榜上競爭曝光。
>
> **從新聞了解行為**
> 三組行動者各自於發片週期釋出音樂影片，利用平台演算法的短期衝榜窗口最大化曝光，虛擬偶像陣營正主動搶占與肉身偶像相同的串流競技場。
>
> **從行為了解結構**
> 平台音樂排行榜的演算法邏輯將虛擬偶像與不同系譜的偶像團體置於同一可見性框架內，各方粉絲社群在同一平台爭奪串流資源的態勢已然成形。
>
> **從結構了解趨勢**
> 虛擬偶像與人類偶像同台競爭串流排行，指向偶像產業的平台化趨勢正在重劃「虛擬 vs. 肉身」的市場邊界，長期可能重塑演唱會、周邊商品與粉絲聚集實體場域的資源分配邏輯。

## 注意事項

這份電子報由 AI 自動篩選與撰寫，篩選標準來自一組人工設定的價值觀立場，關注流行文化作為產業與政治場域的面向。使用過程建議查證與獨立判斷。

這個工具還在成長，離理想狀態還有一段距離，也歡迎指教。

## 自行架設

<details>
<summary>如果您想用自己的新聞來源部署私有版本</summary>

**前置條件**
- Python 3
- [Claude Code CLI](https://claude.ai/code)（需已登入）

**步驟**

1. Clone 此 repo

```bash
git clone https://github.com/skalday/skalday-autonews.git
cd skalday-autonews
```

2. 設定新聞來源：編輯 `config/rss_sources.txt`

```
[類別A]
https://feed-1.com/rss
https://feed-2.com/rss
[類別B]
https://feed-3.com/rss
```

3. 執行

```bash
python run.py
```

輸出結果：`reports/` 的 Markdown 週報，以及 `docs/` 的靜態網站。

</details>

<details>
<summary>如果您想調整分析框架</summary>

在 `pipeline/analyzer.py` 修改 prompt。

</details>

---

## Topics

`kpop` `jpop` `tpop` `idol` `gaming` `entertainment-news` `media-industry` `newsletter` `rss` `automation` `claude-ai` `cultural-policy` `platform-economy`
