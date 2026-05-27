# Newsletter Style Guide
> 本文件定義 Skal Day Newsletter 的視覺規範，供 Claude Code 在生成或修改任何前端檔案時直接沿用。

---

## 1. 色票 Color Palette

| 變數名稱 | Hex | 用途 |
|---|---|---|
| `--color-bg` | `#F2F2F2` | 頁面背景、卡片內容區背景 |
| `--color-primary` | `#0051ba` | 主色、標題色、連結色、標題列背景 |
| `--color-primary-mid` | `#2E5BB8` | 按鈕背景 |
| `--color-primary-dark` | `#0F2B5B` | Win98 邊框陰影側（右、下） |
| `--color-primary-light` | `#89B4E8` | Win98 邊框高光側（左、上）、次要資訊文字 |
| `--color-text` | `#111111` | 所有正文 |
| `--color-chrome` | `#c0c0c0` | Win98 UI chrome 專用，不用於內容區 |
| `--color-white` | `#ffffff` | Win98 視窗內部邊框高光 |

**規則：**
- 背景永遠使用 `#F2F2F2`，不使用純白 `#ffffff` 作為頁面底色
- `#c0c0c0` 僅限 Win98 視窗外框（`.win98-box`），不用於內容排版
- 禁止使用漸層、陰影（box-shadow）、blur 等效果

---

## 2. 字型 Typography

### 載入方式

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chiron+GoRound+TC:wght@600&family=Noto+Sans+TC:wght@300&family=Oleo+Script:wght@700&family=Inter:wght@400;700&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
```

### 字型分配規則

| 情境 | 字型 | Weight | 備註 |
|---|---|---|---|
| 中文標題 H1–H6 | `'Chiron GoRound TC', sans-serif` | 600 | 所有中文標題統一使用 |
| 中文內文 | `'Noto Sans TC', sans-serif` | 300 | 段落、摘要、說明文字 |
| 英文 Display 標題 | `'Oleo Script', system-ui` | 700 | 網站名稱、期號大標 |
| 英文 Section label / metadata | `'Courier Prime', monospace` | 400 / 700 | 標籤、日期、issue 編號 |
| 英文內文 | `'Inter', Arial, sans-serif` | 400 | 英文段落內容 |

### 字級規範

```css
h1 { font-size: 26px; }
h2 { font-size: 20px; }
h3 { font-size: 16px; }
h4, h5, h6 { font-size: 14px; }

/* 中文標題共用 */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Chiron GoRound TC', sans-serif;
  font-weight: 600;
  color: #111;
  line-height: 1.4;
}

/* 正文 */
body, p {
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 300;
  font-size: 14px;
  line-height: 1.8;
  color: #111;
}

/* Section label */
.label {
  font-family: 'Courier Prime', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #0051ba;
}

/* Metadata / timestamps */
.meta {
  font-family: 'Courier Prime', monospace;
  font-size: 12px;
  color: #89B4E8;
}
```

---

## 3. Win98 UI 元件

所有視覺裝飾以 Win98 立體邊框為唯一語言。邊框使用非對稱 border 模擬光源從左上打入的效果。**禁止使用任何動畫（animation、transition）。**

### 3-1 視窗卡片 `.win98-box`

```css
.win98-box {
  background: #c0c0c0;
  border-top: 2px solid #ffffff;
  border-left: 2px solid #ffffff;
  border-right: 2px solid #555555;
  border-bottom: 2px solid #555555;
}

.win98-title-bar {
  background: #0051ba;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 700;
  padding: 3px 6px;
  display: flex;
  align-items: center;
}

.win98-body {
  background: #F2F2F2;
  margin: 2px;
  padding: 12px 14px;
}
```

### 3-2 按鈕 `.win98-cta`

```css
.win98-cta {
  display: inline-block;
  background: #2E5BB8;
  color: #ffffff;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 24px;
  border-top: 3px solid #89B4E8;
  border-left: 3px solid #89B4E8;
  border-right: 3px solid #0F2B5B;
  border-bottom: 3px solid #0F2B5B;
  cursor: pointer;
  text-decoration: none;
}
```

按下（`:active`）狀態時邊框左右對調：

```css
.win98-cta:active {
  border-top: 3px solid #0F2B5B;
  border-left: 3px solid #0F2B5B;
  border-right: 3px solid #89B4E8;
  border-bottom: 3px solid #89B4E8;
}
```

### 3-3 內嵌引用區塊 `.win98-inset`

```css
.win98-inset {
  background: #F2F2F2;
  border-top: 2px solid #555555;
  border-left: 2px solid #555555;
  border-right: 2px solid #ffffff;
  border-bottom: 2px solid #ffffff;
  padding: 8px 10px;
  font-family: 'Courier Prime', monospace;
  font-size: 13px;
  color: #111;
}
```

### 3-4 標籤 `.tag`

```css
.tag {
  display: inline-block;
  background: #F2F2F2;
  color: #0051ba;
  font-family: 'Noto Sans TC', sans-serif;
  font-weight: 300;
  font-size: 11px;
  padding: 2px 8px;
  border: 1px solid #0051ba;
}

/* 強調標籤（featured） */
.tag-primary {
  background: #0051ba;
  color: #F2F2F2;
  border-color: #0F2B5B;
  font-family: 'Inter', sans-serif;
  font-weight: 700;
}
```

---

## 4. Newsletter 版型結構

```
┌─────────────────────────────────────┐
│  .nl-header  （藍底，Oleo Script 標題）  │
├─────────────────────────────────────┤
│  .nl-body                           │
│    .nl-section-head（Courier Prime）  │
│    .win98-box（文章卡片）              │
│    .win98-box（文章卡片）              │
│    .nl-section-head                 │
│    quick links（Courier Prime）       │
├─────────────────────────────────────┤
│  .nl-footer  （黑底，Courier Prime）   │
└─────────────────────────────────────┘
```

```css
.nl-preview {
  max-width: 600px;
  background: #F2F2F2;
  border: 2px solid #111;
  font-family: 'Inter', sans-serif;
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
}

.nl-section-head {
  font-family: 'Courier Prime', monospace;
  font-size: 11px;
  font-weight: 700;
  color: #0051ba;
  letter-spacing: 2px;
  text-transform: uppercase;
  border-bottom: 1px solid #0051ba;
  padding-bottom: 4px;
  margin-bottom: 10px;
}

.nl-footer {
  background: #111;
  color: #F2F2F2;
  font-family: 'Courier Prime', monospace;
  font-size: 11px;
  padding: 8px 16px;
}
```

---

## 5. 設計禁止事項

以下效果一律禁止，不論任何情境：

- `animation` / `@keyframes` / `transition`
- `box-shadow` / `text-shadow` / `filter: drop-shadow`
- `background: linear-gradient(...)` 或任何漸層
- `border-radius`（Win98 風格不使用圓角）
- `backdrop-filter` / `blur`

---

## 6. 圖示使用

使用 `★` 作為裝飾符號（沿用網站設定），不使用 emoji，不引入 icon font。

```
★ Section 標題前綴
→ 連結列表前綴
© 版權聲明
```

---

## 7. 設計理念備註

這套規範的核心是用 **Win98 非對稱邊框** 作為唯一裝飾語言，搭配 `#F2F2F2` 背景和藍色系主色，呈現一種折衷版的網路懷舊感——有個性但不過度。所有視覺趣味來自靜態的邊框對比，不依賴任何動態效果。中文排版以 Chiron GoRound TC（圓潤感）搭配 Noto Sans TC 輕量內文，延續網站 Oleo Script 的手感調性。
