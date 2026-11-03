"""短影音主題（她 11/3 定：一層、每支只歸一類）。依序比對，第一個命中的算；試算表「主題」欄可覆寫。"""
import re
TOPICS = ["語言", "理財・房產", "喜劇・娛樂", "醫學健康", "心理・成長", "生活冷知識", "玄學", "交通機車"]
RULES = [
    ("醫學健康",   lambda t, g: "Cofit" in g),
    ("喜劇・娛樂", lambda t, g: "達康" in g or "頑劣中學生" in t),
    ("語言",       lambda t, g: "大久保" in g),
    ("生活冷知識", lambda t, g: "Corn" in g),
    ("交通機車",   lambda t, g: re.search(r"機車|待轉|駕照|測速|路肩|停車|馬路|中柱|爆胎|大燈", t)),
    ("玄學",       lambda t, g: re.search(r"塔羅|占卜|風水|運勢|生肖|數字學|生命靈數|財位|命理|刮刮樂|帶財|算命", t)),
    ("心理・成長", lambda t, g: re.search(r"職場|升職", t)),
    ("語言",       lambda t, g: re.search(r"泰|韓|日文|日語|日本|英文|中文|姊姊|姐姐|單字|多益|water|口頭禪|潛台詞|讀空氣|繞口令|台語|發音", t, re.I)),
    ("喜劇・娛樂", lambda t, g: re.search(r"幽默|喜劇|搞笑|動漫|獵人|漫才|樂咖", t)),
    ("理財・房產", lambda t, g: re.search(r"理財|存股|ETF|稅|年終|退休|第一桶金|記帳|儲蓄險|紅包|投資|房|屋|租|預售|裝修|比爾蓋茲|財富|薪", t)),
    ("醫學健康",   lambda t, g: re.search(r"中醫|醫師|睡|失眠|按摩|穴|經痛|水腫|喝水|減肥|瘦|宵夜|外食|營養|打手槍|生殖|變硬|性功能|口臭|胃|健康|消脂|血糖|把脈|炸雞|燃脂", t)),
    ("心理・成長", lambda t, g: re.search(r"耳邊說書|習慣|職場|主管|升職|同事|工作|面試|兩性|撩|暈船|感情|另一半|前戲|心理|自我|無聊|學習|拒絕|演講|DIY|男生|相處|人際", t)),
]
def topic_of(title, group):
    for name, f in RULES:
        if f(title, group or ""): return name
    return "生活冷知識"
