"""整理成 site/works.json（網站唯一資料來源）並產生每支影片的縮圖。"""
import glob, json, os, re, sys, urllib.request, io, math
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from series import SERIES, classify
from xplatform import XP
from topics import topic_of
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, SITE = f"{ROOT}/data", f"{ROOT}/site"
os.makedirs(f"{DATA}/thumbs_raw", exist_ok=True)
# 精選：以出鏡人物的知名度為主（她 11/3 指定），(影片 ID, 顯示的人名)
FEATURED = [  # (影片 ID, 顯示的人名, 人臉在縮圖中的水平位置 0–1)
    ("goeUtfe5wiU", "宋晏仁醫師", 0.83),
    ("xFAHxgq8BI4", "瓦基", 0.85),
    ("Y5feeDqTcAQ", "ROLAND 羅蘭", 0.66),
    ("am4VsQIHdfA", "阿基師", 0.78),
    ("UJkHlNDEJUo", "阿部瑪利亞", 0.50),
    ("nSfwU_ccPKA", "許藍方", 0.87),
    ("Atnpqw0sRM8", "達康.come", 0.72),
]
# 短影音最上面固定的名人區
SHORT_PIN = [
    ("gLg6L4u7AAc", "達康.come"),
    ("Xd3mFFdQRsw", "娘娘"),
    ("qQNVwO6P1YU", "娘娘"),
    ("wfjymOkyMbQ", "樂咖"),
    ("R6j_95gO2s4", "樂咖"),
]
# 不是她做的作品，整站不放
EXCLUDE = {"DAm1nPpNG60"}  # GQ Taiwan 羅蘭職業秘辛（上集）

D = {json.load(open(f))["id"]: json.load(open(f)) for f in glob.glob(f"{DATA}/details/*.json")}
cat = {}
for f in sorted(glob.glob(f"{DATA}/cat/*.json")):
    j = json.load(open(f))
    for e in j["entries"]: cat.setdefault(e["id"], j["title"])
L = lambda n: [e["id"] for e in json.load(open(f"{DATA}/{n}.json"))["entries"]]
long_ids, short_ids, perform_ids = L("long"), L("short"), L("perform")
shoot_ids = [e["id"] for e in json.load(open(f"{DATA}/cat/shoot.json"))["entries"]]  # 拍攝作品清單
voice_ids = [e["id"] for e in json.load(open(glob.glob(f"{DATA}/cat/PLpPaq7UZT1Wtutbr06qq3S2YLe8ce-S-N.json")[0]))["entries"]]
extra = [i for i in cat if i not in long_ids and i not in perform_ids and i not in short_ids and i not in voice_ids and "music" not in cat[i] and cat[i] != cat.get(shoot_ids[0])]
meowma = re.findall(r"(?:youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})", open(f"{DATA}/old_sites/meowma_sheet.csv").read())
pool_long = [i for i in dict.fromkeys(long_ids + extra + meowma + shoot_ids) if i not in short_ids and i in D and i not in EXCLUDE]

def base(i):
    d = D[i]
    return {"id": i, "t": d["title"], "ch": d["channel"], "d": (d["publish_date"] or "")[:10], "v": d["views"], "s": d["length_s"]}

works = {"long": [], "short": [], "perform": [], "voice": []}
for i in pool_long:
    key, name, group, role = classify(i, D[i]["title"], D[i]["channel"], cat.get(i, ""))
    if i in shoot_ids and role and "拍攝" not in role: role = "拍攝、" + role
    w = base(i); w.update(series=key, role=role)
    works["long"].append(w)
byid = {w["id"]: w for w in works["long"]}
for n, (i, who, fx) in enumerate(FEATURED):
    byid[i]["feat"] = n; byid[i]["person"] = who; byid[i]["fx"] = fx

def short_group(d):
    c = d["channel"]
    if "Cofit" in c or "偷心漢堡" in c: return "Cofit 初日醫學", "後製"
    if "達康" in c: return "達康.come笑Tube", "拍攝、剪輯"
    if "Corn" in c: return "今天有 Corn", "拍攝、剪輯"
    if "大久保" in c: return "大久保麻梨子", "拍攝、剪輯"
    return "PressPlay Academy", "拍攝、剪輯"
SHORT_FEAT = ["8-g34z-1FHE"]  # 預留
for i in short_ids:
    if i not in D: continue
    w = base(i); w["group"], w["role"] = short_group(D[i])
    pin = [n for n, (p, _) in enumerate(SHORT_PIN) if p == i]
    if pin: w["pin"] = pin[0]; w["person"] = SHORT_PIN[pin[0]][1]
    works["short"].append(w)
# 長影音清單裡標 #shorts 的其實是短影音（她 11/3 指示移過去）
moved = [w for w in works["long"] if "#shorts" in w["t"].lower()]
works["long"] = [w for w in works["long"] if "#shorts" not in w["t"].lower()]
for w in moved:
    w["group"] = "PressPlay Academy" if "PressPlay" in w["ch"] else w["ch"]
    w.pop("series", None); w.pop("feat", None)
    works["short"].append(w)

# 跨平台觀看數：對到 YouTube 的補上 IG／TikTok 數字；只在 IG／TikTok 的另外新增
sbyid = {w["id"]: w for w in works["short"]}
for n, (link, plat, views, yt, title, who) in enumerate(XP):
    if yt and yt in sbyid:
        w = sbyid[yt]
        if plat != "YT" and views > max(w["v"], w.get("xv", 0)): w.update(xv=views, xp=plat, xlink=link)
        elif plat == "YT": w["v"] = max(w["v"], views)
        if who and "person" not in w: w["person"] = who
    elif not yt:
        code = re.search(r"/(?:reel|video)/([^/?]+)", link).group(1)
        nid = ("ig_" if plat == "IG" else "tt_") + code
        # 縮圖：Strikingly 截圖去掉底部的觀看數列
        raw = f"{DATA}/thumbs_raw/{nid}_v.jpg"
        if not os.path.exists(raw):
            im = Image.open(f"{DATA}/strikingly_shorts/{n:02d}.jpg").convert("RGB")
            im.crop((0, 0, im.width, int(im.height * 0.86))).save(raw, quality=90)
        w = {"id": nid, "t": title, "ch": "PressPlay Academy", "d": "", "v": views, "s": 0,
             "group": "PressPlay Academy", "role": "拍攝、剪輯", "xp": plat, "xv": views, "xlink": link, "only": plat}
        if who: w["person"] = who
        works["short"].append(w); sbyid[nid] = w

for i in perform_ids:
    if i in D: works["perform"].append(base(i))
for i in voice_ids:
    if i in D: works["voice"].append(base(i))

# 短影音主題（自動歸類，試算表可覆寫）
for w in works["short"]: w["topic"] = topic_of(w["t"], w.get("group", ""))

# 試算表「全部作品」分頁的修改（apply_sheet.py 產生）：改系列、改分工、隱藏
OV = json.load(open(f"{ROOT}/tools/sheet_overrides.json")) if os.path.exists(f"{ROOT}/tools/sheet_overrides.json") else {}
SKEY = {s[1]: s[0] for s in SERIES}
unknown = []
for k in works:
    keep = []
    for w in works[k]:
        u = {"long": "長影音", "short": "短影音", "perform": "演出", "voice": "配音"}[k] + "|" + (w["xlink"] if w.get("only") else f"https://www.youtube.com/{'shorts/' if k == 'short' else 'watch?v='}{w['id']}")
        o = OV.get(u, {})
        if o.get("hide"): continue
        if "role" in o: w["role"] = o["role"]
        if o.get("topic") and k == "short": w["topic"] = o["topic"]
        if "person" in o:
            if o["person"]: w["person"] = o["person"]
            elif "feat" not in w: w.pop("person", None)
        if "series" in o:
            if k == "long":
                if o["series"] in SKEY: w["series"] = SKEY[o["series"]]
                else: unknown.append((u, o["series"]))
            else: w["group"] = o["series"]
        keep.append(w)
    works[k] = keep
if unknown: print("⚠ 試算表裡有不存在的系列名稱（沒套用）：", unknown)

# 縮圖：每支一張，存成 2 倍解析度的 webp（橫式 640×360、直式 480×854），前端捲到才載入
def fetch(i, kind):
    """下載原始縮圖到 data/。橫式抓 hq720（1280×720），沒有就退回 sddefault／hqdefault（之後裁掉黑邊）"""
    p = f"{DATA}/thumbs_raw/{i}_{'h720' if kind == 'h' else 'v'}.jpg"
    if not os.path.exists(p):
        names = ["hq720.jpg", "sddefault.jpg", "hqdefault.jpg"] if kind == "h" else ["oar2.jpg", "hqdefault.jpg"]
        for name in names:
            try: data = urllib.request.urlopen(f"https://i.ytimg.com/vi/{i}/{name}", timeout=30).read(); break
            except Exception: continue
        open(p, "wb").write(data)
    return p

SIZE = {"h": (640, 360), "v": (480, 854)}
def thumb(i, kind):
    out = f"{SITE}/thumbs/{kind}/{i}.webp"
    if os.path.exists(out): return
    tw, th = SIZE[kind]
    im = Image.open(fetch(i, kind)).convert("RGB")
    if kind == "h" and abs(im.width / im.height - 4 / 3) < .01:   # 4:3 的 sddefault／hqdefault 上下有黑邊，先裁成 16:9
        h = round(im.width * 9 / 16); t = (im.height - h) // 2; im = im.crop((0, t, im.width, t + h))
    r = max(tw / im.width, th / im.height)   # 等比裁切填滿
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - tw) // 2, (im.height - th) // 2
    im.crop((l, t, l + tw, t + th)).save(out, "WEBP", quality=80, method=6)

jobs = list(dict.fromkeys([(w["id"], "v" if k == "short" else "h") for k in works for w in works[k]]))
for kind in SIZE: os.makedirs(f"{SITE}/thumbs/{kind}", exist_ok=True)
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda a: thumb(*a), jobs))
want = {f"{SITE}/thumbs/{k}/{i}.webp" for i, k in jobs}
for p in glob.glob(f"{SITE}/thumbs/*/*.webp"):
    if p not in want: os.remove(p)   # 已排除或隱藏的作品，縮圖一起清掉
series_meta = [{"key": s[0], "name": s[1], "group": s[2], "role": s[3]} for s in SERIES]
json.dump({"works": works, "series": series_meta}, open(f"{SITE}/works.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in works.items()}, "thumbs", len(want))
