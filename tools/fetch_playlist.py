"""抓 YouTube 播放清單全部影片（yt-dlp 在這台只拿到前 100 支，所以自己走 innertube 續頁）。
用法：python3 fetch_playlist.py <playlist_id> <輸出.json>"""
import json, re, sys, urllib.request

HDR = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36",
       "Accept-Language": "zh-TW,zh;q=0.9"}

def get(url, data=None):
    h = dict(HDR)
    if data is not None:
        data = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    return urllib.request.urlopen(urllib.request.Request(url, data, h), timeout=30).read().decode()

def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o: yield from walk(v, key)

def text(t):
    if not t: return ""
    return t.get("simpleText") or "".join(r.get("text", "") for r in t.get("runs", []))

def main(pid, out):
    html = get(f"https://www.youtube.com/playlist?list={pid}&hl=zh-TW&gl=TW")
    data = json.loads(re.search(r'(?:var ytInitialData|window\["ytInitialData"\]) = (\{.*?\});\s*</script>', html).group(1))
    key = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', html).group(1)
    ver = re.search(r'"INNERTUBE_CLIENT_VERSION":"([^"]+)"', html).group(1)
    title = next((h.get("pageTitle") for h in walk(data, "pageHeaderRenderer") if isinstance(h, dict)), "")
    items, seen, used = [], set(), set()
    vd = re.search(r'"VISITOR_DATA":"([^"]+)"', html).group(1)
    while True:
        for r in walk(data, "lockupViewModel"):
            vid = r.get("contentId")
            if not vid or vid in seen or r.get("contentType") != "LOCKUP_CONTENT_TYPE_VIDEO": continue
            seen.add(vid)
            md = r["metadata"]["lockupMetadataViewModel"]
            rows = [p["text"]["content"] for row in walk(md, "metadataRows") for x in row
                    for p in x.get("metadataParts", []) if "text" in p]
            badge = [b.get("text") for b in walk(r, "thumbnailBadgeViewModel") if isinstance(b, dict)]
            items.append({"id": vid, "title": md["title"]["content"],
                          "channel": rows[0] if rows else "", "meta": rows[1:],
                          "duration": badge[0] if badge else None})
        toks = [c["token"] for c in walk(data, "continuationCommand") if isinstance(c, dict) and "token" in c]
        toks = [t for t in toks if t not in used]
        if not toks: break
        used.add(toks[0])
        data = json.loads(get(f"https://www.youtube.com/youtubei/v1/browse?key={key}",
                              {"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "zh-TW", "gl": "TW", "visitorData": vd}},
                               "continuation": toks[0]}))
    json.dump({"playlist_id": pid, "title": title, "entries": items}, open(out, "w"), ensure_ascii=False, indent=1)
    print(pid, len(items))

main(*sys.argv[1:])
