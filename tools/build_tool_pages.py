"""產生 AI 工具的獨立介紹頁：site/tools/<slug>.html。

文案都在下面的 TOOLS，改文字只改這裡，再跑一次這支就好。
內容經過她逐段確認（2026-11-04），沒有她提供的經驗不要自己補。
"""
import html, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/site/tools"
SALES = "https://burgerhzz.github.io/"

TOOLS = [
    {
        "slug": "burgersub", "name": "burgerSub", "sub": "本機自動字幕", "kind": "Premiere Pro 擴充 · Mac App",
        "before": "以前做字幕要先丟到剪映生成，出來是簡體，要再轉成繁體，最後把 SRT 匯進 Premiere。"
                  "台灣的說法也常常聽錯，像「欸」會變成「哎」。口音、語速、背景音一有變化，錯字就跟著變多，每一關都要手動處理。",
        "how": [
            ("不用離開 Premiere", "直接在面板讀時間軸上的音訊。一小時的錄影剪成三分鐘，就只轉那三分鐘。"),
            ("不用再簡轉繁", "使用針對台灣華語訓練的語音模型，直接輸出繁體，「欸」也不會再被聽成「哎」。"),
            ("錯過的字不會一直錯", "在編輯器改過的專有名詞會記下來，下次辨識時就先餵給模型。"),
            ("斷行不用一條條修", "用繁體中文的斷詞模型，斷在語法的段落上，不是硬切在第 N 個字。"),
            ("有稿子就直接對", "把文字對到時間軸上。沒念出來的句子會標成灰色，後面的時間不會跑掉。"),
        ],
        "features": ["語音辨識", "文檔對位", "專有名詞字典", "只轉錄用到的片段", "In-Out 範圍",
                     "字幕編輯器：切分、合併、改時間、搜尋取代", "Mac 獨立版 burgerSub Studio"],
        "thought": "斷句的每一個門檻，都是拿真實節目的字幕量出來的，不是隨手設一個數字。"
                   "想多救幾個案例就把門檻放寬，通常會連錯的一起放進來。所以每次要調整，都要先拿整個字幕庫做修改前、修改後的比對。",
        "status": "2026 年 10 月發布 1.0 版。全程在本機跑，音訊不會離開電腦，也沒有用量費用。",
    },
    {
        "slug": "burgerbo", "name": "burgerbo", "sub": "YouTube 影片直接匯入 Pr", "kind": "Premiere Pro 擴充",
        "before": "剪片常需要引用網路上的影片片段當素材。以前要找下載網站、下載、畫質或編碼不對還要轉檔、匯入專案、拖上時間軸，每一支都重來一次。",
        "how": [
            ("一次完成", "在 Premiere 面板貼上網址、選好解析度，下載、轉碼、匯入、放上時間軸一次完成。"),
            ("不多轉一次", "來源本身就是 H.264 的話直接匯入，必要時才轉碼。"),
            ("整批處理", "別處整理好的網址清單，用 ⌘V 一次貼進來排隊下載。"),
        ],
        "features": ["最高 4K", "可轉成 ProRes 422", "多支排隊下載", "放上時間軸的方式可以選"],
        "thought": [
            "多支下載是一支一支跑，不同時跑。頻寬和轉檔資源是共用的，同時跑三支只會三支都變慢，進度條也說不清楚在講哪一支。",
            "中間有一支失敗不會中斷整批。跑完後成功的從清單清掉、失敗的留著，剩下的就是要重試的清單。",
            "Enter 原本是直接下載，後來改成「加入清單」。建清單時每加一支都要去摸滑鼠太麻煩。輸入框空著時按 Enter 還是會開始下載，舊習慣只多按一下。",
        ],
        "sales": True,
    },
    {
        "slug": "burgerguide", "name": "burgerGuide", "sub": "影片安全區預覽", "kind": "Premiere Pro 擴充",
        "img": ("~/Desktop/burgerGuide/docs/preview-platforms.png", "TikTok、Instagram Reels、YouTube Shorts 三個平台的擬真介面疊在畫面上，紅色虛線是安全框"),
        "before": "短影音的字卡、logo、人臉常常被平台的按鈕和文案蓋住，剪的時候看不出來，發出去才發現。"
                  "以前的作法有兩種：一種是匯入現成的安全框素材圖，但只有一種版型可以選；另一種是自己手動拉參考線。",
        "how": [
            ("不用另外找素材圖", "TikTok、Instagram Reels、Facebook Reels、YouTube Shorts 的擬真介面都內建在面板裡，按一下就疊到時間軸最上層。"),
            ("版型可以換", "四個平台的介面各自獨立，還有一個「三平台都安全」的保守框，另外有橫式 16:9 的 YouTube 介面。"),
            ("不用手拉參考線", "三分法、中心十字、動作安全框、字幕安全框都可以直接打開。也可以自訂格線，存成自己的預設。"),
            ("一支滑桿調透明度", "所有疊圖合成一個片段，透明度用一支滑桿就能調。"),
        ],
        "features": ["四個平台的擬真介面", "三平台都安全的保守框", "橫式 16:9 YouTube 介面",
                     "三分法、中心十字、動作安全框、字幕安全框", "自訂格線，可存成預設"],
        "thought": "Premiere 沒有讓外掛畫參考線的功能，所以改用疊一層透明圖片來做。代價是輸出前要記得關掉那一軌，不然疊圖會一起被輸出。",
        "sales": True,
    },
    {
        "slug": "prsort", "name": "PR 打包專案整理器", "short": "PR Sort", "sub": "Premiere 打包資料夾一鍵分類", "kind": "macOS App",
        "before": "用 Premiere 的「專案管理」打包後，所有檔案都攤平在同一層，素材、音樂、專案檔全混在一起。"
                  "接手的人一打開資料夾就眼花撩亂，很難找到東西放在哪。",
        "how": [
            ("照習慣的結構分好", "把資料夾拖進 App，就會照剪輯師習慣的結構分好，接手的人照資料夾名稱就找得到："),
        ],
        "tree": [
            ("Projects", "專案檔和 Premiere 的快取"),
            ("Footage", "每台相機自動分成 CAM_A、B、C，照片、旁白另外分開"),
            ("Assets", "動態素材、音樂、音效。音樂和音效以 90 秒為界分開"),
            ("Exports", "輸出檔"),
        ],
        "after_tree": "沒把握的檔案會標橘色問號，讓你用下拉選單確認。",
        "features": ["只在同一顆硬碟裡搬，不改檔名、不複製、不刪除", "每次搬移都留紀錄，可以一鍵還原", "Intel 和 Apple 晶片的 Mac 都能跑"],
        "thought": "有一次整理完專案打不開，差點以為是工具搬壞的，查下去才發現專案打包出來時就已經壞了。所以使用步驟的第一步改成：整理前先開一次專案，確認能開。",
    },
]

UI = {
 "zh": {"html": "zh-Hant", "back": "← 回作品集", "before": "以前怎麼做、卡在哪", "how": "它怎麼改善", "feat": "核心功能", "thought": "做的時候想清楚的事",
        "sales": "官方介紹與下載頁 ↗", "others": "其他工具", "prev": "上一個", "next": "下一個", "foot": "© Burger Film Studio · 偷心漢堡"},
 "en": {"html": "en", "back": "← Back to portfolio", "before": "How it used to work", "how": "What it changes", "feat": "Core features", "thought": "Decisions behind it",
        "sales": "Product page & download ↗", "others": "Other tools", "prev": "Previous", "next": "Next", "foot": "© Burger Film Studio"},
}

TOOLS_EN = [
 {"slug": "burgersub", "name": "burgerSub", "sub": "On-device auto subtitles", "kind": "Premiere Pro extension · Mac app",
  "before": "Subtitles used to mean running the audio through CapCut, converting the Simplified Chinese output to Traditional, then importing the SRT into Premiere. Taiwanese expressions were often misheard (欸 came out as 哎), and any change in accent, pace or background noise meant more errors to fix by hand at every step.",
  "how": [("Never leave Premiere", "It reads the audio straight from the timeline. If an hour of footage is cut down to three minutes, only those three minutes get transcribed."),
          ("No more conversion", "A speech model trained for Taiwanese Mandarin outputs Traditional Chinese directly, and 欸 is no longer heard as 哎."),
          ("Fix a word once", "Terms corrected in the editor are remembered and fed to the model on the next run."),
          ("Line breaks that make sense", "A Traditional Chinese word-segmentation model breaks lines at phrase boundaries instead of at a fixed character count."),
          ("Align to a script", "If there's already a script, the text is aligned to the timeline. Lines that weren't spoken turn grey and don't throw off the timing after them.")],
  "features": ["Speech recognition", "Script alignment", "Custom dictionary", "Transcribes only the parts in use", "In/Out range", "Subtitle editor: split, merge, retime, find & replace", "Standalone Mac app: burgerSub Studio"],
  "thought": "Every line-break threshold was measured against real show subtitles, not picked at random. Loosening a threshold to rescue a few more cases usually lets the wrong ones through too, so every change is checked with a before-and-after comparison across the whole subtitle library.",
  "status": "Version 1.0 released October 2026. Runs entirely on your Mac: audio never leaves the computer and there are no usage fees."},
 {"slug": "burgerbo", "name": "burgerbo", "sub": "YouTube videos straight into Premiere", "kind": "Premiere Pro extension",
  "before": "Edits often need clips from online videos. That used to mean finding a download site, downloading, transcoding when the resolution or codec was wrong, importing and dragging it onto the timeline, for every single clip.",
  "how": [("All in one go", "Paste a URL in the Premiere panel, choose a resolution, and it downloads, transcodes, imports and places the clip on the timeline."),
          ("No unnecessary transcodes", "H.264 sources are imported as-is; it only transcodes when it has to."),
          ("Batch it", "Paste a whole list of URLs with ⌘V and they queue up.")],
  "features": ["Up to 4K", "ProRes 422 output", "Batch download queue", "Choice of timeline placement"],
  "thought": ["Batches run one clip at a time, not in parallel. Bandwidth and transcoding are shared, so running three at once just makes all three slower, and the progress bar can't say which one it's talking about.",
              "One failure doesn't stop the batch. When it's done, successful clips leave the queue and failed ones stay, so what's left is exactly the retry list.",
              "Enter used to start the download; it now adds the URL to the list, because building a list shouldn't need the mouse for every clip. Pressing Enter on an empty field still starts the download, so the old habit costs one extra key."],
  "sales": True},
 {"slug": "burgerguide", "name": "burgerGuide", "sub": "Video safe-zone preview", "kind": "Premiere Pro extension",
  "img": ("~/Desktop/burgerGuide/docs/preview-platforms.png", "TikTok, Instagram Reels and YouTube Shorts interfaces overlaid on a frame, with the safe area in red dashed lines"),
  "before": "Text cards, logos and faces in short-form video often end up hidden behind platform buttons and captions, and you only find out after posting. The options used to be a downloaded safe-zone template with a single layout, or dragging guides by hand.",
  "how": [("No template hunting", "Realistic TikTok, Instagram Reels, Facebook Reels and YouTube Shorts interfaces are built into the panel and drop onto the top track in one click."),
          ("Switchable layouts", "Each platform has its own overlay, plus a conservative frame that's safe on all three and a 16:9 YouTube layout."),
          ("No more manual guides", "Rule of thirds, centre cross, action-safe and title-safe areas are a toggle away, and custom grids can be saved as presets."),
          ("One opacity slider", "Everything is merged into a single clip, so one slider controls the opacity.")],
  "features": ["Realistic UI for four platforms", "Safe-on-all-three frame", "16:9 YouTube layout", "Rule of thirds, centre cross, action-safe, title-safe", "Custom grids saved as presets"],
  "thought": "Premiere doesn't let extensions draw guides, so the overlay is a transparent image on its own track. The trade-off: that track has to be switched off before export, or the overlay will be rendered too.",
  "sales": True},
 {"slug": "prsort", "name": "PR Sort", "short": "PR Sort", "sub": "One-click sorting for Premiere project packages", "kind": "macOS app",
  "before": "Packaging a project with Premiere's Project Manager dumps every file into one flat folder: footage, music and project files all mixed together. Whoever takes over opens the folder and can't tell where anything is.",
  "how": [("Sorted the way editors expect", "Drop the folder into the app and it's organised into a structure editors already know, so whoever takes over can find things by folder name:")],
  "tree": [("Projects", "Project files and Premiere caches"), ("Footage", "One folder per camera (CAM_A, B, C), with photos and voice-over kept separate"),
           ("Assets", "Motion graphics, music and sound effects, with music and SFX split at 90 seconds"), ("Exports", "Rendered files")],
  "after_tree": "Files it isn't sure about get an orange question mark and a drop-down so you can decide.",
  "features": ["Moves within the same drive only: no renaming, copying or deleting", "Every move is logged and can be undone in one click", "Runs on Intel and Apple silicon Macs"],
  "thought": "Once, a project wouldn't open after sorting. It looked like the tool had broken it, but the package had come out of Premiere already broken. So step one of the instructions became: open the project once before sorting to make sure it works."},
]

e = html.escape

def page(t, prev, nxt, lang='zh'):
    U = UI[lang]; sx = '' if lang == 'zh' else '.en'
    shown = t.get("short", t["name"])
    img = ""
    if t.get("img"):
        src, alt = t["img"]
        if lang == 'zh': Image.open(os.path.expanduser(src)).convert("RGB").save(f"{OUT}/{t['slug']}.webp", "WEBP", quality=85, method=6)
        w, h = Image.open(f"{OUT}/{t['slug']}.webp").size
        img = f'<figure class="shot"><img src="{t["slug"]}.webp" alt="{e(alt)}" width="{w}" height="{h}"></figure>'
    how = "".join(f"<li><b>{e(a)}</b>{e(b)}</li>" for a, b in t["how"])
    tree = ""
    if t.get("tree"):
        tree = '<ul class="tree">' + "".join(f"<li><code>{e(a)}/</code><span>{e(b)}</span></li>" for a, b in t["tree"]) + "</ul>"
        tree += f"<p>{e(t['after_tree'])}</p>"
    thought = t["thought"] if isinstance(t["thought"], list) else [t["thought"]]
    thought = "".join(f"<p>{e(p)}</p>" for p in thought)
    status = f'<p class="status">{e(t["status"])}</p>' if t.get("status") else ""
    sales = f'<p class="sales"><a href="{SALES}" target="_blank" rel="noopener">{U["sales"]}</a></p>' if t.get("sales") else ""
    return f"""<!doctype html>
<html lang="{U['html']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(shown)} | Burger Film Studio</title>
<meta name="description" content="{e(t['name'])}: {e(t['sub'])}. {e(t['before'][:80])}…">
<meta property="og:title" content="{e(t['name'])} | {e(t['sub'])}">
<meta property="og:image" content="https://burgerhzz.github.io/burger-film-studio/media/hero.jpg">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍔</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;700;900&family=Red+Hat+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="tool.css">
</head>
<body>
<nav class="nav"><div class="wrap">
  <a class="mark" href="../index.html?lang={lang}">Burger Film Studio</a>
  <span class="nav-r"><a class="back" href="../index.html?lang={lang}#tools">{U['back']}</a><span class="lang"><a href="{t['slug']}.html" class="{'on' if lang=='zh' else ''}">TW</a><a href="{t['slug']}.en.html" class="{'on' if lang=='en' else ''}">EN</a></span></span>
</div></nav>
<main class="wrap doc">
  <header>
    <p class="kind">{e(t['kind'])}</p>
    <h1>{e(t['name'])}</h1>
    <p class="sub">{e(t['sub'])}</p>
  </header>
  {img}
  <section><h2>{U['before']}</h2><p>{e(t['before'])}</p></section>
  <section><h2>{U['how']}</h2><ul class="how">{how}</ul>{tree}</section>
  <section><h2>{U['feat']}</h2><ul class="feat">{"".join(f"<li>{e(f)}</li>" for f in t['features'])}</ul>{status}</section>
  <section class="thought"><h2>{U['thought']}</h2>{thought}</section>
  {sales}
  <nav class="pager" aria-label="{U['others']}">
    <a href="{prev['slug']}{sx}.html"><small>{U['prev']}</small>{e(prev.get('short', prev['name']))}</a>
    <a href="{nxt['slug']}{sx}.html"><small>{U['next']}</small>{e(nxt.get('short', nxt['name']))}</a>
  </nav>
</main>
<footer class="wrap">{U['foot']}</footer>
</body>
</html>
"""

CSS = """:root{color-scheme:dark;--bg:#0d0d0d;--surface:#121212;--line:#1c1c1c;--line-2:#2a2a2a;--fg:#fff;--muted:#999;--dim:#666;
--display:"Red Hat Display","Noto Sans TC","PingFang TC",sans-serif;--body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;--mono:"Red Hat Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.75;-webkit-font-smoothing:antialiased}
a{color:inherit}
a:focus-visible{outline:2px solid var(--fg);outline-offset:3px;border-radius:4px}
.wrap{max-width:820px;margin:0 auto;padding-inline:max(16px,env(safe-area-inset-left,0px)) max(16px,env(safe-area-inset-right,0px))}
.nav{position:sticky;top:0;z-index:5;background:color-mix(in oklab,var(--bg) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:60px;max-width:1280px}
.mark{font-family:var(--display);font-weight:900;font-size:19px;letter-spacing:-.02em;text-decoration:none;text-transform:uppercase}
.back{font-size:14px;color:var(--muted);text-decoration:none}\n.nav-r{display:flex;align-items:center;gap:14px}\n.lang{display:flex;border:1px solid var(--line-2);border-radius:999px;padding:2px;gap:2px}\n.lang a{font:700 12px/1 var(--display);letter-spacing:.06em;text-decoration:none;color:var(--muted);padding:7px 10px;border-radius:999px}\n.lang a.on{background:var(--fg);color:var(--bg)}
.back:hover{color:var(--fg)}
.doc header{padding:56px 0 28px;border-bottom:1px solid var(--line-2);margin-bottom:8px}
.kind{margin:0 0 10px;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)}
h1{margin:0;font-family:var(--display);font-weight:900;font-size:clamp(40px,8vw,72px);line-height:1;letter-spacing:-.03em}
.sub{margin:12px 0 0;font-size:18px;font-weight:700}
.shot{margin:28px 0 8px}
.shot img{display:block;width:100%;height:auto;border-radius:10px;border:1px solid var(--line-2)}
section{padding:28px 0;border-bottom:1px solid var(--line)}
h2{margin:0 0 12px;font-size:15px;font-weight:700;letter-spacing:.02em;color:var(--muted)}
section p{margin:0 0 10px}
.how{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.how b{display:block;font-size:17px;margin-bottom:2px}
.how li{color:#ccc}
.tree{list-style:none;margin:16px 0;padding:14px 18px;background:var(--surface);border:1px solid var(--line-2);border-radius:10px;display:grid;gap:8px}
.tree li{display:grid;grid-template-columns:7.5em minmax(0,1fr);gap:12px;font-size:15px}
.tree code{font-family:var(--mono);color:var(--fg)}
.tree span{color:var(--muted)}
.feat{margin:0;padding-left:1.2em;display:grid;gap:4px;color:#ccc}
.status{margin-top:16px!important;color:var(--muted);font-size:14px}
.thought p{color:#ccc}
.sales{padding:24px 0 0;margin:0}
.sales a{font-weight:700;text-decoration:none;border-bottom:1px solid var(--dim)}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:32px 0 8px}
.pager a{display:block;padding:14px 18px;border:1px solid var(--line-2);border-radius:10px;text-decoration:none;font-family:var(--display);font-weight:700;font-size:18px}
.pager a:last-child{text-align:right}
.pager a:hover{border-color:var(--dim)}
.pager small{display:block;font-family:var(--body);font-weight:500;font-size:12px;color:var(--dim)}
footer{padding:40px 0 48px;color:var(--dim);font-size:13px}
@media (max-width:520px){.tree li{grid-template-columns:minmax(0,1fr);gap:0}}
"""

os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/tool.css", "w").write(CSS)
for n, t in enumerate(TOOLS):
    open(f"{OUT}/{t['slug']}.html", "w").write(page(t, TOOLS[n - 1], TOOLS[(n + 1) % len(TOOLS)]))
for n, t in enumerate(TOOLS_EN):
    open(f"{OUT}/{t['slug']}.en.html", "w").write(page(t, TOOLS_EN[n - 1], TOOLS_EN[(n + 1) % len(TOOLS_EN)], 'en'))
print("tool pages:", [t["slug"] for t in TOOLS])
