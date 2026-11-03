"""works.json + site_template.html → site/index.html"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLURB = {
 "cofit": "宋晏仁醫師與初日診所醫師群的健康節目",
 "pro": "feat. 火花羅、好味營養師品瑄、35 線上賞屋 TED、娘娘、雪薇英文、故宮、法律白話文、簡少年…｜25+ 集節目、100+ 支短影音",
 "book": "說書節目，Podcast／YouTube／Reels 同步產出｜21 集",
 "celeb": "ROLAND、阿部瑪利亞、阿基師、PEETA 葛格",
 "ppschool": "6 人問答節目｜18 集",
 "course": "線上課程開箱：烘焙、攝影、手作、機車、調酒、Vlog",
 "face": "feat. 簡少年｜第一、二季共 34 集",
 "street": "街頭訪問｜試播 2 集",
 "manzai": "feat. 達康.come、微笑丹尼｜來賓：許藍方、啾啾鞋、營養師 Ricky…｜11+ 集",
 "pbs": "feat. 達康.come、漫才少爺｜36 集",
 "dakang": "達康.come 的 Podcast 影音版｜22 集",
 "girl": "零基礎檔車教學到重機考照 feat. 大魔王 Singer、加菲貓、阿娟",
 "trivia": "汽機車冷知識 feat. 大魔王 Singer",
 "offroad": "越野入門騎乘教學 feat. 卡布麵大叔",
 "pk": "XMAX vs Forza、Gogoro 3 vs 中華 iE125",
 "ricoland": "feat. 大魔王 Singer、偷心漢堡",
 "moto": "機車介紹 23+ 集、試乘 15+ 集、國內外發表會 9+ 集、海外試乘、經典車庫",
 "brand": "得安 VR-1 安全帽、給通勤族的飆股報告書、接客啦！達康！…",
}
data = open(f"{ROOT}/site/works.json").read().replace("</", "<\\/")
html = open(f"{ROOT}/tools/site_template.html").read().replace("__DATA__", data).replace("__BLURB__", json.dumps(BLURB, ensure_ascii=False))
# 一般網站需要完整的文件標頭（claude.ai 預覽會自己包，這裡補上）
head = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta property="og:title" content="Burger Film Studio">
<meta property="og:description" content="偷心漢堡的影像作品集：網路節目、短影音、Podcast 的企劃、拍攝與剪輯，以及 AI 剪輯工具開發。">
<meta property="og:image" content="https://burgerhzz.github.io/burger-film-studio/media/hero.jpg">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🍔</text></svg>">
"""
i = html.index("</style>") + len("</style>")
html = head + html[:i] + "\n</head>\n<body>\n" + html[i:] + "\n</body>\n</html>\n"
open(f"{ROOT}/site/index.html", "w").write(html)
print(len(html) // 1024, "KB")
