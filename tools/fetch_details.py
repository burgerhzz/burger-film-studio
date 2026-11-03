"""讀每支影片頁面的 ytInitialPlayerResponse，取說明欄、發布日、長度、觀看數。
用法：python3 fetch_details.py ids.txt details_dir"""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
HDR = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36",
       "Accept-Language": "zh-TW,zh;q=0.9", "Cookie": "CONSENT=YES+1"}

def one(vid, out):
    p = os.path.join(out, vid + ".json")
    if os.path.exists(p): return "skip"
    try:
        html = urllib.request.urlopen(urllib.request.Request(f"https://www.youtube.com/watch?v={vid}&hl=zh-TW&gl=TW", headers=HDR), timeout=30).read().decode()
        m = re.search(r"var ytInitialPlayerResponse = (\{.*?\});(?:var|</script>)", html)
        pr = json.loads(m.group(1))
        vd = pr.get("videoDetails", {}); mf = pr.get("microformat", {}).get("playerMicroformatRenderer", {})
        rec = {"id": vid, "title": vd.get("title"), "description": vd.get("shortDescription", ""),
               "channel": vd.get("author"), "channel_id": vd.get("channelId"),
               "length_s": int(vd.get("lengthSeconds") or 0), "views": int(vd.get("viewCount") or 0),
               "publish_date": mf.get("publishDate"), "category": mf.get("category"),
               "embeddable": pr.get("playabilityStatus", {}).get("playableInEmbed"),
               "status": pr.get("playabilityStatus", {}).get("status"),
               "keywords": vd.get("keywords", [])}
        json.dump(rec, open(p, "w"), ensure_ascii=False, indent=1)
        return "ok"
    except Exception as e:
        return f"ERR {vid} {e}"

ids = [l.strip().split("v=")[-1] for l in open(sys.argv[1]) if l.strip()]
os.makedirs(sys.argv[2], exist_ok=True)
with ThreadPoolExecutor(int(os.environ.get("J", 6))) as ex:
    res = list(ex.map(lambda v: one(v, sys.argv[2]), ids))
print({k: sum(1 for r in res if r.startswith(k)) for k in ("ok", "skip", "ERR")})
for r in res:
    if r.startswith("ERR"): print(r)
