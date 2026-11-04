# 交接｜Burger Film Studio 作品集
最後更新：2026-11-04 14:40（session 02fb64e0）

## 現在的狀態
網站已上線：https://burgerhzz.github.io/burger-film-studio/ 。repo 是公開的 `burgerhzz/burger-film-studio`，推上 `main` 就會自動發布。工作規矩在 `CLAUDE.md`，檔案說明和「在另一台電腦接手」在 `README.md`。

首頁由上到下：
1. hero 影片（YouTube nIV0FMC_5qM 的 1080p，手機用 720p）
2. 自我介紹：大標「影音製作 × AI 工作流程開發」、兩段自介、數據
3. 服務項目：4 張卡，沒有實例那行
4. AI 工具：4 張卡只到「過往痛點」，整張可點進介紹頁 `site/tools/*.html`
5. 一集節目怎麼做：6 張流程卡，S 形排列，進畫面自動播放，點開用 GSAP Flip 展開；③ 分成 03A MG 動畫、03B 圖卡動畫兩種形式
6. 精選：7 支，滑過展開案例說明，不放觀看數
7. 作品：分頁順序是長影音（預設）→ 短影音 → Podcast 影音製作 → 出鏡演出 → 配音
8. 經歷、聯絡

右上角有 TW／EN 切換，英文對照表在 `tools/i18n_en.py`。

## 未完成／待決定
- [ ] **下個 session 開始時先問**：讓別台電腦也能新增作品（11/4 討論，她還沒選）
  - A（推薦）：`data/` 推進 repo 前把本名換成代號，抓取和分類程式改成認代號；縮圖原檔快取 81 MB 不推
  - B：另開私人 repo 放 `data/`
  - C：repo 改私人，但免費帳號不能用 Pages，不考慮
  - 順便：流程動畫字型（思源宋體，免費授權）放進 repo，`tools/flow/render_html.js` 改成不依賴本機 skills 路徑
- [ ] **下個 session 開始時先問**：YouTube 播放清單更新時怎麼同步（11/4 討論，建議 A）
  - A：她說「更新作品」，跑一支整合腳本，列出新影片和歸類，她看過再推
  - B：GitHub Actions 每週全自動，分類錯了會直接上線，而且常被 YouTube 擋，不建議
  - C：每週自動偵測，有新影片就通知
- [ ] **下個 session 開始時先問**：她說「整個作品集文字太多了」，刪減還沒做完。服務項目、AI 工具卡已經照她的版本處理，剩下：
  - 自我介紹
  - 作品分頁說明
  - 經歷（軟體、器材、現場三行要刪掉還是改成點開才顯示）
  - 聯絡
- [ ] **下個 session 開始時先問**：上一輪「說人話」清單有 4 條她還沒回：
  - 自介兩段
  - 精選說明寫了「品牌內容」，但 7 支精選裡沒有品牌內容，事實對不上
  - burgerSub 介紹頁的「錯過的字不會一直錯」應該是「改過的字」
- [ ] 英文版的人名、節目名是自己取或翻的，要她確認（清單在 `tools/i18n_en.py` 的 TERMS）
  - 標「？」的特別要看：Genesis Clinic、Waki、Chef A-Chi、Dr. Gracie Hsu、Books in Your Ear、Huohualuo、Today's Corn、Anquan Motors、Zero Li
- [ ] 工具卡和介紹頁「Pr」「Premiere」混用，要不要統一
- [ ] burgerGuide 介紹頁的內文還是舊說法，例如「四個平台的擬真介面」，要不要跟首頁卡片統一
- [ ] 服務卡「影像拍攝與後期製作」要不要補一行實例。目前四張都拿掉實例了，所以先不用
- [ ] 還沒在真機上驗收：
  - 手機上的自動播放（iPhone 低耗電模式可能停在第一格）
  - 流程卡展開的手感
  - VIEW 游標
- [ ] 舊的待辦（11/3）：
  - 試算表修改清單第 2～6 列
  - 長影音要不要也用主題分類
  - TikTok 上對不到的高觀看影片
  - 3 支 IG 對應

## 這次的產出（11/4）
| 檔案 | 說明 |
|---|---|
| `tools/site_template.html` | 版面重排、六步流程卡、語言切換、各區文案 |
| `tools/i18n_en.py` | 英文對照表（新） |
| `tools/build_tool_pages.py` | 四個工具介紹頁＋英文版 |
| `tools/flow/*.html`、`render_html.js` | 流程區六支動畫的原始頁面與逐格輸出 |
| `site/media/flow/*.mp4` | 字幕校正、粗剪示意、MG、圖卡、組片、字卡六宮格 |
| `site/media/hero.mp4`、`hero_720.mp4` | 1080p／720p hero |
| `site/thumbs/` | 逐張高畫質縮圖（取代舊的拼圖） |
| `CLAUDE.md`、`README.md`、`HANDOFF.md` | 換電腦也能接手 |

## 好用指令
- 「做好推上去」：改完直接 commit、push、等部署成功再回報
- 「說人話」或「去 AI 味」：先列清單等她勾選，只去空話，保留正式語氣
- 貼一段新文案加上「改為」：照原文替換，英文版同步改

## 下次怎麼接
- 改文字、版面：改 `tools/site_template.html`，同步 `tools/i18n_en.py`，再跑 `python3 tools/build_site.py`，截圖確認後 push
- 新增作品：需要 `data/`，只在原本那台電腦上有，見 README
- 重做流程動畫：`tools/flow/` 的 HTML 加 `render_html.js`，需要原本那台電腦上的字型和無頭瀏覽器

## 歷次 session
- 2026-11-03 35131575：作品集第一版上線、試算表雙向流程、TikTok 觀看數
- 2026-11-04 02fb64e0：架構重排、高畫質縮圖與 hero、六步流程卡、TW／EN、工具介紹頁、大量文案修改 → 對話紀錄在原本那台電腦的 `~/Desktop/claude/session_logs/2026-11-04_02fb64e0_*.md`
