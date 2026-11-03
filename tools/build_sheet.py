"""產生溝通用試算表（xlsx，上傳 Google Drive 轉成試算表）。"""
import json, os, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = json.load(open(f"{ROOT}/site/works.json"))
W, SER = J["works"], {s["key"]: s for s in J["series"]}
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="2B2724")
IN = PatternFill("solid", fgColor="FFF4D6")
wb = Workbook()

def sheet(ws, headers, rows, widths, input_cols=(), note=None):
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(italic=True, color="7A7067"); r0 = 3
    for c, h in enumerate(headers, 1):
        x = ws.cell(r0, c, h); x.font = H; x.fill = HF
    for i, row in enumerate(rows, r0 + 1):
        for c, v in enumerate(row, 1):
            x = ws.cell(i, c, v); x.alignment = Alignment(vertical="top", wrap_text=c in widths.get("wrap", ()))
            if c in input_cols: x.fill = IN
    for c, w in enumerate(widths["w"], 1): ws.column_dimensions[chr(64 + c)].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    return r0

LEGEND = "黃底欄位給你填。改完不用通知格式，跟我說「看試算表」我就會照著改網站。"
ws = wb.active; ws.title = "修改清單"
todo = [
 ("2026-11-03", "經歷", "自由接案 2024/7–2026/1", "期間和列的頻道是我推的，對嗎？", "待確認", ""),
 ("2026-11-03", "自介", "「具 9 年影像製作經驗」", "從 2017/2 算到現在，寫 9 年可以嗎？", "待確認", ""),
 ("2026-11-03", "自製工具", "四個工具卡片", "目前沒有截圖，有的話可以給我，或要不要我幫 PR 打包專案整理器自己截一張", "待確認", ""),
 ("2026-11-03", "長影音系列", "今天有 Corn", "分工先寫「拍攝、剪輯」，對嗎？", "待確認", ""),
 ("2026-11-03", "長影音系列", "形象宣傳（中信兄弟 MV、波波電玩展等）", "分工先寫「剪輯、視覺動畫設計」，各支實際分工？", "待確認", ""),
 ("2026-11-03", "上線", "GitHub Pages", "repo 要公開才能用免費的 GitHub Pages，可以嗎？", "待確認", ""),
 ("（範例）", "短影音", "達康去面試", "這支不要放", "", ""),
]
r0 = sheet(ws, ["日期", "區塊", "位置／哪一支", "要改什麼", "狀態", "Claude 回覆"], todo,
           {"w": [12, 14, 34, 52, 10, 40], "wrap": (3, 4, 6)}, input_cols=(4, 5), note=LEGEND)
dv = DataValidation(type="list", formula1='"待確認,待處理,處理中,完成,不改"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"E{r0+1}:E300")

ws = wb.create_sheet("精選")
feat = sorted([w for w in W["long"] if "feat" in w], key=lambda w: w["feat"])
rows = [(w["feat"] + 1, SER[w["series"]]["name"], w["t"], w["role"], w["v"], f"https://www.youtube.com/watch?v={w['id']}", "保留", "") for w in feat]
r0 = sheet(ws, ["順序", "系列", "標題", "分工", "觀看數", "網址", "保留／拿掉", "換成哪一支（貼網址）"], rows,
           {"w": [6, 18, 60, 34, 10, 44, 11, 40], "wrap": (3,)}, input_cols=(1, 4, 7, 8), note=LEGEND + " 改「順序」數字就會調整排列。")
dv = DataValidation(type="list", formula1='"保留,拿掉"'); ws.add_data_validation(dv); dv.add(f"G{r0+1}:G100")

ws = wb.create_sheet("系列")
cnt = {}
for w in W["long"]: cnt[w["series"]] = cnt.get(w["series"], 0) + 1
blurb = json.loads(re.search(r"BLURB = (\{.*?\})\n", open(f"{ROOT}/tools/build_site.py").read().replace("\n ", " ")).group(1)) if False else {}
rows = [(s["name"], s["group"], s["role"], cnt.get(s["key"], 0), "", "", s["key"]) for s in J["series"] if cnt.get(s["key"])]
sheet(ws, ["系列名稱", "類別", "分工（網站顯示）", "支數", "要改的分工", "其他修改", "代號（勿改）"], rows,
      {"w": [26, 12, 40, 8, 34, 40, 12], "wrap": (3, 5, 6)}, input_cols=(5, 6), note=LEGEND)

ws = wb.create_sheet("全部作品")
rows = []
KIND = {"long": "長影音", "short": "短影音", "perform": "演出", "voice": "配音"}
for k in ("long", "short", "perform", "voice"):
    for w in sorted(W[k], key=lambda w: w["d"], reverse=True):
        grp = SER[w["series"]]["name"] if k == "long" else w.get("group", w["ch"])
        u = f"https://www.youtube.com/{'shorts/' if k == 'short' else 'watch?v='}{w['id']}"
        rows.append((KIND[k], grp, w["d"][:7], w["t"], w.get("role", ""), w["v"], u, "", ""))
r0 = sheet(ws, ["區塊", "系列／頻道", "發布", "標題", "分工", "觀看數", "網址", "顯示", "備註"], rows,
           {"w": [8, 22, 9, 64, 28, 10, 44, 9, 30]}, input_cols=(5, 8, 9), note=LEGEND + " 不想放的在「顯示」選「隱藏」。")
dv = DataValidation(type="list", formula1='"顯示,隱藏"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"H{r0+1}:H{r0+len(rows)}")
ws.auto_filter.ref = f"A{r0}:I{r0+len(rows)}"
out = f"{ROOT}/review/作品集修改清單.xlsx"; wb.save(out)
print(out, os.path.getsize(out), len(rows))
