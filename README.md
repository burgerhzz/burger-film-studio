# Burger Film Studio 作品集

偷心漢堡的影像作品集網站。`site/` 是可以直接上線的靜態網站，推上 `main` 後 GitHub Actions 會自動發布到
https://burgerhzz.github.io/burger-film-studio/

## 在另一台電腦接手

```bash
git clone https://github.com/burgerhzz/burger-film-studio.git
cd burger-film-studio
gh auth login          # 要能 push 才需要
```

| 想做的事 | 需要什麼 | 這台電腦能不能做 |
|---|---|---|
| 改文字、版面、配色、英文版 | Python 3（只用標準函式庫） | 可以：改 `tools/site_template.html` 或 `tools/i18n_en.py`，再跑 `python3 tools/build_site.py` |
| 改工具介紹頁 | Python 3＋Pillow（`pip3 install pillow`） | 可以：改 `tools/build_tool_pages.py`，再跑它 |
| 新增作品、改系列分類、改分工 | `data/` 資料夾＋Pillow | 要先把原本那台電腦的 `data/` 複製過來（AirDrop、隨身碟都行），或用 `tools/fetch_*.py` 重新抓 |
| 重做流程區的動畫影片 | 字型與無頭瀏覽器，見 `tools/flow/` | 只在原本那台電腦上設定好 |

`data/` 不進版控：裡面的 YouTube 說明欄有本名，這個 repo 是公開的。

## 檔案
- `tools/site_template.html`：首頁版型、CSS、JS 都在這裡，**改首頁從這裡改**，不要直接改 `site/index.html`
- `tools/build_site.py`：把 template＋`site/works.json`＋英文對照表組成 `site/index.html`，並替媒體網址加版本號
- `tools/i18n_en.py`：英文版對照表（中文原文 → 英文）。**新增或修改中文文案時，這裡要同步改**，不然英文版會漏翻
- `tools/build_tool_pages.py`：四個 AI 工具介紹頁（中文 `site/tools/*.html`、英文 `*.en.html`）
- `tools/build_works.py`：整理作品資料、產生縮圖、輸出 `site/works.json`；精選清單和案例說明在 `FEATURED`
- `tools/series.py`、`tools/topics.py`、`tools/xplatform.py`：系列歸類、短影音主題、跨平台觀看數
- `tools/flow/`：剪輯流程區的動畫頁面（`*.html`）與逐格輸出腳本
- `site/media/`：hero 影片（1080p 桌機、720p 手機）、流程區影片、精選圖
- `site/thumbs/`：每支影片一張縮圖（webp）

## 更新作品資料（需要 `data/`）
```bash
python3 tools/fetch_playlist.py <播放清單ID> data/long.json      # 抓播放清單
python3 tools/fetch_details.py data/ids.txt data/details         # 抓每支影片的說明欄和觀看數
python3 tools/build_works.py                                     # 歸系列、產生縮圖、輸出 works.json
python3 tools/build_site.py                                      # 套版產生 index.html
```

## 從試算表改作品
試算表「全部作品」分頁可以直接改「系列／頻道」「分工」，或在「顯示」欄選「隱藏」。
1. 讀取 `全部作品!A1:L` 的資料，存成 JSON 檔
2. `python3 tools/apply_sheet.py 存好的檔.json`：比對後寫入 `tools/sheet_overrides.json`，以「區塊|網址」當鍵
3. `python3 tools/build_works.py && python3 tools/build_site.py`
