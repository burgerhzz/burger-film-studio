"""整理成 site/works.json（網站唯一資料來源）並產生縮圖拼圖。"""
import glob, json, os, re, sys, urllib.request, io, math
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from series import SERIES, classify
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, SITE = f"{ROOT}/data", f"{ROOT}/site"
os.makedirs(f"{SITE}/sprites", exist_ok=True); os.makedirs(f"{DATA}/thumbs_raw", exist_ok=True)
D = {json.load(open(f))["id"]: json.load(open(f)) for f in glob.glob(f"{DATA}/details/*.json")}
cat = {}
for f in sorted(glob.glob(f"{DATA}/cat/*.json")):
    j = json.load(open(f))
    for e in j["entries"]: cat.setdefault(e["id"], j["title"])
L = lambda n: [e["id"] for e in json.load(open(f"{DATA}/{n}.json"))["entries"]]
long_ids, short_ids, perform_ids = L("long"), L("short"), L("perform")
voice_ids = [e["id"] for e in json.load(open(glob.glob(f"{DATA}/cat/PLpPaq7UZT1Wtutbr06qq3S2YLe8ce-S-N.json")[0]))["entries"]]
extra = [i for i in cat if i not in long_ids and i not in perform_ids and i not in short_ids and i not in voice_ids and "music" not in cat[i]]
meowma = re.findall(r"(?:youtu\.be/|watch\?v=)([A-Za-z0-9_-]{11})", open(f"{DATA}/old_sites/meowma_sheet.csv").read())
pool_long = [i for i in dict.fromkeys(long_ids + extra + meowma) if i not in short_ids and i in D]

FEATURED = ["wAKxwIRtOq4","18XdHHARSGk","q2qhfIAB6KI","zfGJNq-Vb-k","wlTROaDhodk","CIrzjbF3X2A","YUPwKSOXsRE","xFAHxgq8BI4",
            "DcTOvEZuDNY","Y5feeDqTcAQ","Atnpqw0sRM8","nSfwU_ccPKA","apABpKbsO-8","4t7EFWlc0uY","YoPYjvPF-Sc","2wlvNQsePY4","EBm3SWrrqm8","nIV0FMC_5qM"]

def base(i):
    d = D[i]
    return {"id": i, "t": d["title"], "ch": d["channel"], "d": (d["publish_date"] or "")[:10], "v": d["views"], "s": d["length_s"]}

works = {"long": [], "short": [], "perform": [], "voice": []}
for i in pool_long:
    key, name, group, role = classify(i, D[i]["title"], D[i]["channel"], cat.get(i, ""))
    w = base(i); w.update(series=key, role=role)
    if i in FEATURED: w["feat"] = FEATURED.index(i)
    works["long"].append(w)

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
    w = base(i); w["group"], w["role"] = short_group(D[i]); works["short"].append(w)
for i in perform_ids:
    if i in D: works["perform"].append(base(i))
for i in voice_ids:
    if i in D: works["voice"].append(base(i))

# 縮圖
def fetch(i, kind):
    p = f"{DATA}/thumbs_raw/{i}_{kind}.jpg"
    if not os.path.exists(p):
        name = "oar2.jpg" if kind == "v" else "mqdefault.jpg"
        try: data = urllib.request.urlopen(f"https://i.ytimg.com/vi/{i}/{name}", timeout=30).read()
        except Exception: data = urllib.request.urlopen(f"https://i.ytimg.com/vi/{i}/hqdefault.jpg", timeout=30).read()
        open(p, "wb").write(data)
    return p
jobs = [(w["id"], "v" if k == "short" else "h") for k in works for w in works[k]]
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda a: fetch(*a), dict.fromkeys(jobs)))

def sprites(items, kind, tw, th, cols, rows, prefix):
    per = cols * rows; info = {}
    uniq = list(dict.fromkeys(items))
    for n in range(math.ceil(len(uniq) / per)):
        sheet = Image.new("RGB", (tw * cols, th * rows), (20, 18, 16))
        for k, i in enumerate(uniq[n*per:(n+1)*per]):
            im = Image.open(fetch(i, kind)).convert("RGB")
            # 等比裁切填滿
            r = max(tw / im.width, th / im.height)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
            l, t = (im.width - tw) // 2, (im.height - th) // 2
            sheet.paste(im.crop((l, t, l + tw, t + th)), ((k % cols) * tw, (k // cols) * th))
            info[i] = [n, k % cols, k // cols]
        sheet.save(f"{SITE}/sprites/{prefix}{n}.jpg", quality=68, optimize=True, progressive=True)
    return {"cols": cols, "rows": rows, "files": [f"sprites/{prefix}{n}.jpg" for n in range(math.ceil(len(uniq)/per))], "map": info}

for f in glob.glob(f"{SITE}/sprites/*.jpg"): os.remove(f)
H = [w["id"] for k in ("long", "perform", "voice") for w in works[k]]
SP = {"h": sprites(H, "h", 320, 180, 10, 10, "h"), "v": sprites([w["id"] for w in works["short"]], "v", 240, 426, 10, 5, "v")}
series_meta = [{"key": s[0], "name": s[1], "group": s[2], "role": s[3]} for s in SERIES]
json.dump({"works": works, "series": series_meta, "sprites": SP}, open(f"{SITE}/works.json", "w"), ensure_ascii=False)
print({k: len(v) for k, v in works.items()}, "sprites", len(SP["h"]["files"]), len(SP["v"]["files"]))
