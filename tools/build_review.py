"""產生「精選候選＋短影音分組」審稿頁。縮圖內嵌成 data URI（artifact 擋外部圖片）。"""
import base64, glob, html, json, os, urllib.request, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
D = {json.load(open(f))["id"]: json.load(open(f)) for f in glob.glob(f"{DATA}/details/*.json")}
TH = os.path.join(DATA, "thumbs"); os.makedirs(TH, exist_ok=True)

def thumb(vid):
    p = os.path.join(TH, vid + ".jpg")
    if not os.path.exists(p):
        open(p, "wb").write(urllib.request.urlopen(f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg", timeout=20).read())
    return "data:image/jpeg;base64," + base64.b64encode(open(p, "rb").read()).decode()

# (id, 系列, 分工, 為什麼選, 需要確認)
LONG = [
 ("wAKxwIRtOq4", "Cofit 初日醫學", "後製", "現職代表作，23.6 萬觀看", ""),
 ("18XdHHARSGk", "Cofit 初日醫學", "後製", "長篇訪談（23 分），13.9 萬觀看", ""),
 ("q2qhfIAB6KI", "殘酷擂台", "拍攝、剪輯、片頭片尾、視覺動畫設計", "全部作品觀看數最高（43 萬）", ""),
 ("zfGJNq-Vb-k", "小老婆冷知識", "拍攝、剪輯、視覺動畫設計", "37 萬觀看，知識型動畫包裝", ""),
 ("wlTROaDhodk", "讓 Pro 級的來", "企劃、拍攝、剪輯、視覺動畫", "自己企劃的節目，34 萬觀看", ""),
 ("CIrzjbF3X2A", "重機女孩養成記", "企劃、演出、剪輯、整體視覺動畫設計", "企劃＋演出＋剪輯一手包", ""),
 ("YUPwKSOXsRE", "機車試乘", "拍攝、剪輯、視覺動畫、封面設計", "30 萬觀看，代表小老婆時期", ""),
 ("xFAHxgq8BI4", "耳邊說書", "拍攝、收音、剪輯", "13 萬觀看，知識節目", ""),
 ("DcTOvEZuDNY", "線上課程開箱", "拍攝、演出、剪輯", "12.6 萬觀看，2022/8 雙 C 九份 Vlog 教學，片尾標「課程開麥拉」", "這支在你的「開箱｜線上課程」清單裡。分工照同清單「麻瓜行不行」寫拍攝、演出、剪輯，對嗎？"),
 ("Y5feeDqTcAQ", "名人專訪", "拍攝、剪輯、片頭、視覺設計、封面", "ROLAND 專訪，名人效應", ""),
 ("Atnpqw0sRM8", "Play Boy Station", "拍攝、剪輯、片頭動畫", "漫才綜藝，7.3 萬觀看", ""),
 ("nSfwU_ccPKA", "頑劣中學生", "拍攝、剪輯", "漫才節目，5.8 萬觀看", ""),
 ("apABpKbsO-8", "達康還在講", "拍攝、收音、剪輯", "Podcast 影音版代表", ""),
 ("4t7EFWlc0uY", "不負責任面相學", "拍攝、剪輯", "街訪節目，34 集系列", ""),
 ("YoPYjvPF-Sc", "火花羅", "企劃、拍攝", "2025 接案作品，8.5 萬觀看", ""),
 ("2wlvNQsePY4", "李靜 東京 VLOG", "剪輯", "VLOG 類型代表", ""),
 ("EBm3SWrrqm8", "Enzo 相機對決", "剪輯", "產品對決，2024", ""),
 ("nIV0FMC_5qM", "得安 VR-1 安全帽", "導演、企劃、剪輯、調色、視覺動畫設計、封面", "形象廣告，職稱最完整", ""),
]
S = json.load(open(f"{DATA}/short.json"))["entries"]
def find(sub): return next(e["id"] for e in S if sub in e["title"])
# (標題關鍵字, 系列, 分工, 為什麼選, 需要確認)
SHORT = [(find(k),) + tuple(rest) for k, *rest in [
 ("像獵人", "達康", "拍攝、剪輯", "109 萬觀看，全部作品最高", ""),
 ("盤子", "PressPlay 泰語", "拍攝、剪輯", "13.4 萬觀看，2024/6 發布", ""),
 ("按摩臉部", "PressPlay 中醫", "拍攝、剪輯", "11.9 萬觀看", ""),
 ("牙敗", "大久保麻梨子", "拍攝、剪輯", "4.6 萬觀看", ""),
 ("降血糖", "Cofit 初日醫學", "後製", "到職前試做", ""),
]]

def fmt_views(n):
    return f"{n/10000:.1f} 萬" if n >= 10000 else f"{n:,}"

def card(t, vertical=False):
    vid, series, role, why, ask = t
    d = D[vid]
    role_html = f'<p class="role">{html.escape(role)}</p>' if role else '<p class="role tbd">分工待填</p>'
    ask_html = f'<p class="ask">確認：{html.escape(ask)}</p>' if ask else ""
    return f'''<article class="card">
 <a class="th" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener"><img src="{thumb(vid)}" alt="" loading="lazy"><span class="dur">{d["length_s"]//60}:{d["length_s"]%60:02d}</span></a>
 <div class="body">
  <p class="meta"><span class="series">{html.escape(series)}</span><span>{d["publish_date"][:7].replace("-", "/")}</span><span>{fmt_views(d["views"])} 次</span></p>
  <h3><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">{html.escape(d["title"])}</a></h3>
  {role_html}
  <p class="why">{html.escape(why)}</p>{ask_html}
 </div></article>'''

# 短影音分組
groups = collections.OrderedDict()
def gkey(d, title):
    ch = d.get("channel", "")
    if "頑劣中學生" in title: return ("頑劣中學生 shorts", "拍攝、剪輯", "Strikingly 寫「拍攝、剪輯 YouTube & shorts」")
    if "耳邊說書" in title: return ("耳邊說書 shorts", "拍攝、收音、剪輯", "照 Strikingly 長影音版分工")
    if "讓pro級的來" in title.lower(): return ("讓 Pro 級的來 shorts", "企劃、拍攝、剪輯", "照 Strikingly 長影音版分工")
    if ch == "PressPlay Academy":
        y = d.get("publish_date", "")[:7]
        if y > "2024-06": return ("PressPlay 其他（2024/7 以後）", "拍攝、剪輯", "離職後接案")
        return ("PressPlay 其他（到 2024/6）", "拍攝、剪輯", "課程推廣短片：中醫、理財、韓語、泰語、冷知識…")
    if "達康" in ch: return ("達康.come笑Tube", "拍攝、剪輯", "")
    if "Corn" in ch: return ("今天有Corn", "拍攝、剪輯", "Podcast 切片")
    if "大久保" in ch: return ("大久保麻梨子", "拍攝、剪輯", "")
    return ("Cofit 初日醫學", "後製", "含到職前試做 2 支")
for e in S:
    d = D.get(e["id"])
    if not d: continue
    k = gkey(d, e["title"])
    g = groups.setdefault(k[0], {"role": k[1], "note": k[2], "items": []})
    g["items"].append(d)
rows = []
for name, g in groups.items():
    it = sorted(g["items"], key=lambda d: d["publish_date"])
    span = f'{it[0]["publish_date"][:7].replace("-", "/")}–{it[-1]["publish_date"][:7].replace("-", "/")}'
    top = max(it, key=lambda d: d["views"])
    role = html.escape(g["role"]) if g["role"] else '<span class="tbd">待填</span>'
    note = g["note"]
    note_html = (f'<span class="tbd">{html.escape(note)}</span><br>' if "？" in note else f"{html.escape(note)}<br>") if note else ""
    rows.append(f'<tr><td class="g">{html.escape(name)}</td><td class="num">{len(it)}</td><td class="num">{span}</td><td>{role}</td><td>{note_html}<span class="sample">最多人看：{html.escape(top["title"][:34])}（{fmt_views(top["views"])}）</span></td></tr>')

tpl = open(os.path.join(ROOT, "tools", "review_template.html")).read()
out = (tpl.replace("{{LONG}}", "\n".join(card(t) for t in LONG))
          .replace("{{SHORT}}", "\n".join(card(t) for t in SHORT))
          .replace("{{ROWS}}", "\n".join(rows))
          .replace("{{NLONG}}", str(len(LONG))).replace("{{NSHORT}}", str(len(SHORT)))
          .replace("{{SHORTTOTAL}}", str(sum(len(g["items"]) for g in groups.values()))))
open(os.path.join(ROOT, "review", "精選候選.html"), "w").write(out)
print("ok", len(LONG), len(SHORT), len(groups))
