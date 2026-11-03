"""讀 TikTok 單支影片頁的觀看數（個人頁讀不到，只能給影片連結）。
用法：python3 fetch_tiktok.py 連結1 連結2 …"""
import json, re, sys, urllib.request
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def walk(o, k):
    if isinstance(o, dict):
        for a, b in o.items():
            if a == k: yield b
            yield from walk(b, k)
    elif isinstance(o, list):
        for x in o: yield from walk(x, k)
for u in sys.argv[1:]:
    html = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "zh-TW"}), timeout=30).read().decode()
    m = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', html, re.S)
    it = next(walk(json.loads(m.group(1)), "itemStruct"), None) if m else None
    print(u, "|", (it or {}).get("stats", {}).get("playCount"), "|", (it or {}).get("desc", "讀不到")[:60])
