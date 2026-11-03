"""把試算表「全部作品」分頁的修改轉成 tools/sheet_overrides.json（以「區塊|網址」為鍵，同一支可能同時在長影音和演出）。
輸入：Sheets get_values 的 JSON（範圍 全部作品!A1:J…，含標題列），存成檔案後執行：
    python3 tools/apply_sheet.py 讀回的檔案.json
只記錄「跟網站目前資料不同」的欄位：系列／頻道、分工、顯示＝隱藏。"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = json.load(open(f"{ROOT}/site/works.json"))
SN = {s["key"]: s["name"] for s in J["series"]}
OV_PATH = f"{ROOT}/tools/sheet_overrides.json"
ov = json.load(open(OV_PATH)) if os.path.exists(OV_PATH) else {}

def url_of(k, w):
    if w.get("only"): return w["xlink"]
    return f"https://www.youtube.com/{'shorts/' if k == 'short' else 'watch?v='}{w['id']}"
KIND = {"long": "長影音", "short": "短影音", "perform": "演出", "voice": "配音"}
cur = {}
for k in J["works"]:
    for w in J["works"][k]:
        cur[KIND[k] + "|" + url_of(k, w)] = (k, SN.get(w.get("series"), "") if k == "long" else w.get("group", w["ch"]), w.get("role", ""))

data = json.load(open(sys.argv[1]))
rows = data["values"] if isinstance(data, dict) else data
head = rows[0]; col = {h: i for i, h in enumerate(head)}
get = lambda r, h: (r[col[h]] if col.get(h) is not None and col[h] < len(r) else "").strip()
changes = []
for r in rows[1:]:
    if not get(r, "網址"): continue
    u = get(r, "區塊") + "|" + get(r, "網址")
    o = {}
    if u in cur:
        k, grp, role = cur[u]
        if get(r, "系列／頻道") and get(r, "系列／頻道") != grp: o["series"] = get(r, "系列／頻道")
        if get(r, "分工") != role and (get(r, "分工") or role): o["role"] = get(r, "分工")
    if get(r, "顯示") == "隱藏": o["hide"] = True
    if get(r, "備註（給 Claude 的說明）"): o["note"] = get(r, "備註（給 Claude 的說明）")
    prev = ov.get(u, {})
    merged = {**{k2: v for k2, v in prev.items() if k2 not in ("hide",)}, **o}
    if o.get("hide") is None: merged.pop("hide", None)
    if merged != prev: changes.append((u, prev, merged))
    if merged: ov[u] = merged
    elif u in ov: del ov[u]
json.dump(ov, open(OV_PATH, "w"), ensure_ascii=False, indent=1)
for u, a, b in changes: print(u, a, "→", b)
print(len(changes), "處變動；目前覆寫共", len(ov), "支")
