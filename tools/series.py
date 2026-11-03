"""長影音歸系列。規則依序比對，第一個命中的算。分工來源：Strikingly 舊站的系列分工＋她在對話中的確認。"""
import re
# key, 顯示名稱, 大類, 分工, 比對函式(title, channel, cat)
SERIES = [
 ("talk",    "初日會客室",            "醫學健康", "拍攝",                          lambda t,c,k: "初日會客室" in t),
 ("cofit",   "初日醫學 Cofit",        "醫學健康", "後製",                         lambda t,c,k: "Cofit" in c),
 ("pro",     "讓 Pro 級的來",         "知識節目", "企劃、拍攝、剪輯、視覺動畫",     lambda t,c,k: re.search(r"讓\s*Pro級的來|讓pro級的來", t, re.I) or "專家QA" in k),
 ("book",    "耳邊說書",              "知識節目", "拍攝、收音、剪輯",              lambda t,c,k: "耳邊說書" in t or "耳邊說書" in k),
 ("celeb",   "名人專訪",              "名人專訪", "拍攝、剪輯、片頭、視覺設計、封面", lambda t,c,k: re.search(r"職人訪談|人物專訪", t) or re.search(r"ROLAND|羅蘭|阿基師|阿部瑪利亞|阿布瑪莉雅|Peeta|PEETA", t)),
 ("ppschool","PP 小學堂",            "知識節目", "企劃、演出、剪輯",              lambda t,c,k: "PP小學堂" in t),
 ("course",  "課程開麥拉・麻瓜行不行", "知識節目", "拍攝、剪輯",                    lambda t,c,k: re.search(r"課程開麥拉|麻瓜行不行|課程開箱", t) or "線上課程" in k),
 ("face",    "不負責任面相學",        "街訪",     "拍攝、剪輯",                    lambda t,c,k: "面相" in t or "簡少年" in k),
 ("street",  "PPA 街訪",              "街訪",     "企劃、演出",                    lambda t,c,k: "街頭訪問" in t),
 ("manzai",  "頑劣中學生",            "漫才喜劇", "拍攝、剪輯",                    lambda t,c,k: "頑劣中學生" in t or "頑劣中學生" in k),
 ("pbs",     "集合囉！Play Boy Station", "漫才喜劇", "拍攝、剪輯、片頭動畫",       lambda t,c,k: re.search(r"Play Boy Station|PBS|集合囉", t) or "Play Boy" in c),
 ("dakang",  "達康還在講",            "Podcast",  "拍攝、收音、剪輯",              lambda t,c,k: "達康還在講" in t or "達康還在講" in k),
 ("corn",    "今天有 Corn",           "Podcast",  "拍攝、剪輯",                    lambda t,c,k: "Corn" in c or "CORN" in t),
 ("girl",    "重機女孩養成記",        "知識節目", "企劃、演出、剪輯、整體視覺動畫設計", lambda t,c,k: "重機女孩" in t),
 ("trivia",  "小老婆冷知識",          "知識節目", "拍攝、剪輯、視覺動畫設計",       lambda t,c,k: "冷知識" in t or "冷知識" in k),
 ("offroad", "越野教室",              "知識節目", "拍攝、剪輯、視覺動畫設計",       lambda t,c,k: "越野教室" in t or "越野教室" in k),
 ("pk",      "殘酷擂台",              "產品對決", "拍攝、剪輯、片頭片尾、視覺動畫設計", lambda t,c,k: "殘酷擂台" in t),
 ("ricoland","日本 Ricoland",         "VLOG",     "拍攝、演出、剪輯、整體視覺動畫設計", lambda t,c,k: "Ricoland" in t),
 ("brand",   "形象宣傳",              "形象宣傳", "剪輯、視覺動畫設計",             lambda t,c,k: "形象" in k or "MV" in k),
 ("hanaro",  "火花羅",                "接案合作", "企劃、拍攝",                    lambda t,c,k: "火花羅" in c),
 ("enzo",    "興趣使然的攝影師 Enzo", "接案合作", "剪輯",                          lambda t,c,k: "Enzo" in c),
 ("leejing", "LEE-JING 李靜",         "VLOG",     "剪輯",                          lambda t,c,k: "李靜" in c),
 ("aquan",   "安筌運轉",              "VLOG",     "剪輯",                          lambda t,c,k: "安筌" in c),
 ("moto",    "機車介紹＆試乘",        "機車媒體", "拍攝、剪輯、視覺動畫、封面設計",  lambda t,c,k: "小老婆" in c or "發表會" in k or "產品測試" in k or "人物專訪" in k),
 ("ppatalk", "PressPlay 人物訪談",     "知識節目", "拍攝、剪輯",                    lambda t,c,k: "PressPlay" in c and re.search(r"feat\.", t) and "#shorts" not in t.lower()),
 ("ppa",     "PressPlay 節目",        "知識節目", "拍攝、剪輯",                    lambda t,c,k: "PressPlay" in c),
 ("other",   "其他合作",              "接案合作", "剪輯",                          lambda t,c,k: False),
 ("dakangch","達康.come笑Tube",       "漫才喜劇", "拍攝、剪輯",                    lambda t,c,k: "達康" in c),
]
# 單支覆寫：id -> (series key or None, role or None)
OVERRIDE = {
 "DcTOvEZuDNY": ("course", "拍攝、剪輯"),
 "nIV0FMC_5qM": ("brand", "導演、企劃、剪輯、調色、視覺動畫設計、封面"),
 "GaV_DLR59n8": ("brand", "拍攝、剪輯、視覺動畫設計、封面"),
 "NjP_ujIBExA": ("brand", "視覺動畫設計"),
 "prSXsuJQyhM": ("brand", None),
 "471FzqmM4ac": ("brand", None),
 "IxO8qdG-eok": ("other", None),
 "OdiaJyuHeoo": ("dakangch", None),
}
def classify(vid, title, channel, catname):
    key = role = None
    if vid in OVERRIDE: key, role = OVERRIDE[vid]
    for s in SERIES:
        if (key and s[0] == key) or (not key and s[4](title or "", channel or "", catname or "")):
            return s[0], s[1], s[2], role or s[3]
    return None, None, None, role
