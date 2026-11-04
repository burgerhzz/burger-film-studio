# 作品集網站（Burger Film Studio）

這份是給 Claude 的工作規矩，在任何一台電腦打開這個資料夾都會讀到。進度和待辦看 `HANDOFF.md`。

## 改網站的流程
1. 改 `tools/site_template.html`（或 `tools/build_tool_pages.py`、`tools/build_works.py`），**不要直接改 `site/` 底下的產出檔**
2. 中文文案有新增或改動，`tools/i18n_en.py` 要同步加英文；標題型的詞（系列、人名、分類）放 `TERMS`
3. `python3 tools/build_site.py`（改工具頁就跑 `build_tool_pages.py`）
4. 用無頭瀏覽器截圖確認版面，桌機和手機寬度都要看
5. commit 後直接 `git push`，等 GitHub Actions 部署成功再回報。她說「做好推上去」就不用再問

## 文案
- 她貼上來的文案**照原文放**，不要自己改寫
- 她要求「去 AI 味」時，先列清單等她勾選才改。只拿掉空話和口號，**保留正式、完整的語氣**，不要改成口語碎句（曾經被退回）
- 平台名稱用官方寫法（Instagram、YouTube、Facebook），中英文之間加空格
- 影片標題不翻成英文；其他文字切到 EN 時要全部是英文

## 視覺
- 黑底、白字；重點色是黃色 `#ffe600`，紅色 `#d42121` 只用在很小的點綴
- 媒體網址由 `build_site.py` 自動加內容版本號，換檔不用改檔名
- 縮圖不能糊：縮圖用 2 倍解析度的 webp，影片用原始畫質
- 有影片的卡片都是自動播放、靜音、循環；捲出畫面就暫停

## 不能做的事
- 不要把 `data/`、`NOTES.md` 加進 git：裡面有她的本名，這個 repo 是公開的
- 不要把網站放到 claude.ai 上，以 GitHub Pages 為準
- commit 作者用她的 git 全域身分（burgerhzz），不要用公司信箱
