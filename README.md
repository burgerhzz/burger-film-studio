# Burger Film Studio 作品集

偷心漢堡的影像作品集網站。`site/` 是可以直接上線的靜態網站。

## 檔案
- `site/index.html`：網站本體，作品資料直接寫在頁面裡
- `site/works.json`：全部作品的資料，包含系列、分工、觀看數
- `site/sprites/`：縮圖拼圖，一張大圖裡放很多支影片的縮圖
- `.github/workflows/pages.yml`：推上 main 就自動發布 `site/` 到 GitHub Pages
- `site/media/hero.mp4`：首頁主視覺影片，從 meowma.com 原檔轉成網頁用的版本

## 更新流程
```bash
python3 tools/fetch_playlist.py <播放清單ID> data/long.json      # 抓播放清單
python3 tools/fetch_details.py data/ids.txt data/details         # 抓每支影片的說明欄和觀看數
python3 tools/build_works.py                                     # 歸系列、產生縮圖拼圖、輸出 works.json
python3 tools/build_site.py                                      # 套版產生 index.html
```

- 系列歸類規則和每個系列的分工寫在 `tools/series.py`
- 精選清單寫在 `tools/build_works.py` 的 `FEATURED`

## 從試算表改作品
試算表「全部作品」分頁可以直接改「系列／頻道」「分工」，或在「顯示」欄選「隱藏」。
1. 讀取 `全部作品!A1:J` 的資料，存成 JSON 檔
2. `python3 tools/apply_sheet.py 存好的檔.json`：比對後寫入 `tools/sheet_overrides.json`，以「區塊|網址」當鍵
3. `python3 tools/build_works.py && python3 tools/build_site.py`
