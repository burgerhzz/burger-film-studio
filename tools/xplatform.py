"""短影音的跨平台觀看數（來源：Strikingly 舊站短影音區的截圖，2026-11-03 人工判讀）。
yt：對應的 YouTube Shorts ID（None＝只有 IG／TikTok 版本，網站會另外新增一張卡）。
views 是截圖上的數字，平台會繼續累積，所以是「至少」。"""
XP = [
 # (平台連結, 平台, 觀看數, 對應 YouTube ID, 只在 IG/TikTok 時用的標題, 人物)
 ("https://www.instagram.com/reel/C-Kx-HWNkCP/", "IG", 1011000, "Xd3mFFdQRsw", None, "娘娘"),
 ("https://www.instagram.com/reel/C8zO42TBjhr/", "IG", 668000, "qQNVwO6P1YU", None, "娘娘"),
 ("https://www.tiktok.com/@pressplayacademy/video/7386602113339591953", "TikTok", 471400, "NooaTphrKOs", None, "娘娘"),
 ("https://www.instagram.com/reel/DBgFDqlx8ck/", "IG", 822000, "gLg6L4u7AAc", None, "達康.come"),
 ("https://www.instagram.com/reel/DAV065xJTVw/", "IG", 47000, "U8-dx4GCWCc", None, "大久保麻梨子"),
 ("https://www.instagram.com/reel/C7T75Q5PrsM/", "IG", 281000, "uVDbh-tErh4", None, None),
 ("https://www.instagram.com/reel/C3sSP49P9II/", "IG", 303000, "IaPPy04kaAY", None, None),
 ("https://www.youtube.com/shorts/R20LX9OQCPY", "YT", 130000, "R20LX9OQCPY", None, "達康.come"),
 ("https://www.instagram.com/reel/CtqrIgWLU4X/", "IG", 84000, "e3juJUlr0zQ", None, "PEETA 葛格"),
 ("https://www.instagram.com/reel/CuQxfC7rdCB/", "IG", 95000, None, "懶人必學的下飯菜：椒鹽雞丁", None),
 ("https://www.instagram.com/reel/CsSnrQUMkAk/", "IG", 464000, "CGICeydqhSI", None, None),
 ("https://www.tiktok.com/@pressplayacademy/video/7353535113528904980", "TikTok", 215600, "WHODSsr7aaQ", None, None),
 ("https://www.instagram.com/reel/C66NzTiv2f8/", "IG", 62000, None, "2 秒學會 1 個韓文：圖書館", None),
 ("https://www.instagram.com/reel/CyncQmmN4Jo/", "IG", 469000, "J49V2hl6m_4", None, None),
 ("https://www.instagram.com/reel/C63praavJGG/", "IG", 87000, None, "韓國女生的道地韓文課：不好意思，請給我＿＿", None),
 ("https://www.instagram.com/reel/C551kqjv11A/", "IG", 55000, "TIKOmghhR08", None, None),
 ("https://www.instagram.com/reel/CzYs_YPPLLF/", "IG", 246000, "Hpongm_bUa4", None, None),
 ("https://www.instagram.com/reel/C0eVSZELcH3/", "IG", 101000, "mk6cnIe4wsE", None, None),
 ("https://www.instagram.com/reel/C8eohNWvRtT/", "IG", 244000, None, "多益聽力常常聽不懂嗎？", None),
 ("https://www.instagram.com/reel/C8Mm_KfPYAo/", "IG", 138000, None, "英澳發音 vs 美加發音：water", None),
 ("https://www.instagram.com/reel/C6_YN0evpPZ/", "IG", 32000, "SKxdsLkhvgQ", None, None),
 ("https://www.instagram.com/reel/C8Ze-J4s6IH/", "IG", 295000, None, "你也是這樣背單字的嗎？", None),
 ("https://www.instagram.com/reel/C4nbBtDvFua/", "IG", 262000, "gkMFkAZbQHk", None, None),
 ("https://www.instagram.com/reel/C4dJJh6C2N2/", "IG", 212000, "YHkYJfFAHqE", None, None),
 ("https://www.instagram.com/reel/C7eQut8tMmL/", "IG", 226000, None, "那個套球要幹什麼用呢？鏤雕象牙雲龍紋套球", None),
 ("https://www.instagram.com/reel/C22PJXOvcJK/", "IG", 106000, "zqY7P_rQ5OQ", None, None),
 ("https://www.instagram.com/reel/C11w3MtPkvu/", "IG", 208000, None, "每月領著死薪水", None),
 ("https://www.instagram.com/reel/C2BckMUPdwx/", "IG", 142000, "KbXUmiABb-A", None, None),
 ("https://www.instagram.com/reel/C1CWb5xvgZB/", "IG", 115000, "_jONYn3OXFs", None, None),
 ("https://www.instagram.com/reel/C0_zA-ZPKTL/", "IG", 219000, "lzhDc8ilqBI", None, None),
 ("https://www.instagram.com/reel/C1MtXeRPaao/", "IG", 162000, "wXmOFsX_KAA", None, None),
 ("https://www.instagram.com/reel/C1E6i2oPen3/", "IG", 221000, "POjRWcVWJrg", None, None),
 ("https://www.instagram.com/reel/CpB3P7jvT1M/", "IG", 23000, "n5XDi444l8U", None, None),
 ("https://www.tiktok.com/@pressplayacademy/video/7470818994195352833", "TikTok", 32800, "9eFdy6iCR0g", None, "樂咖"),  # 11/3 她給的連結，直接讀頁面
 # ↓ 11/3 從 PressPlay TikTok 個人頁收集、逐支讀頁面比對
 ("https://www.tiktok.com/@pressplayacademy/video/7396937093252943122", "TikTok", 816300, "EMPYnNbSHKs", None, None),  # 🇹🇭在泰國我們才不這樣說！In Thai
 ("https://www.tiktok.com/@pressplayacademy/video/7386602113339591953", "TikTok", 626500, "NooaTphrKOs", None, None),  # 🇹🇭去泰國旅遊千萬別這樣點飲料！熱🐭了#
 ("https://www.tiktok.com/@pressplayacademy/video/7385124240363670791", "TikTok", 654600, "qQNVwO6P1YU", None, None),  # 🇹🇭去泰國被當盤子？那是因為你不會這件事
 ("https://www.tiktok.com/@pressplayacademy/video/7510860275218697480", "TikTok", 5781, "RueCVUBSYGc", None, None),  # 在日本說話越長越有禮貌？ \ PPA旅遊
 ("https://www.tiktok.com/@pressplayacademy/video/7470818994195352833", "TikTok", 32800, "9eFdy6iCR0g", None, None),  # 錯過飛機失去愛情？原來幽默真的可以拯救一
 ("https://www.tiktok.com/@pressplayacademy/video/7462968342513552641", "TikTok", 23100, "dHb_IL1u0xM", None, None),  # 過年知道要找誰去刮刮樂了吧！？ 🤩  還
 ("https://www.tiktok.com/@pressplayacademy/video/7418643816359398674", "TikTok", 5925, "PXtw1Y5tHOQ", None, None),  # 台🇹🇼日🇯🇵口頭禪大不同！你聽過嗎？🤩 
 ("https://www.tiktok.com/@pressplayacademy/video/7417773791364861202", "TikTok", 84700, "m6oqJrumV00", None, None),  # 日本人的潛台詞，你聽懂了嗎？😏 #日文 
 ("https://www.tiktok.com/@pressplayacademy/video/7412576769112362257", "TikTok", 6004, "B7_H-_lyIO4", None, None),  # ⚠️ 注意⚠️ 這些韓文你都念錯了！#P
 ("https://www.tiktok.com/@pressplayacademy/video/7400266033581395208", "TikTok", 99800, "z7H2Q4AH6dY", None, None),  # 🇹🇭泰語超簡單！輕鬆拿捏～ In Tha
 ("https://www.tiktok.com/@pressplayacademy/video/7400265696199937287", "TikTok", 62100, "Xd3mFFdQRsw", None, None),  # 🇹🇭泰國流行用語，讓你秒變道地泰國人！咔
 ("https://www.tiktok.com/@pressplayacademy/video/7394389840042724609", "TikTok", 301100, "Zkgf51L-kac", None, None),  # 🇹🇭去泰國旅遊要怎麼殺價？ 掌握這重點居
 ("https://www.tiktok.com/@pressplayacademy/video/7389152260116221200", "TikTok", 88200, "e5N1FtFZHSM", None, None),  # 🇹🇭泰國追星密技！學會這句話，保證回頭率
 ("https://www.tiktok.com/@pressplayacademy/video/7385123958514846994", "TikTok", 55700, "WcHa4Gy4cq8", None, None),  # 不只台灣，🇹🇭泰國也有數字迷思嗎！？🤔 
 ("https://www.tiktok.com/@pressplayacademy/video/7372111211606904072", "TikTok", 31700, "uVDbh-tErh4", None, None),  # 你是中柱派還是側柱派？ #ppa冷知識 
 ("https://www.tiktok.com/@pressplayacademy/video/7366854915068611841", "TikTok", 69200, "yyqZecPIqcU", None, None),  # 「韓國點餐」這句超實用😋想吃辣炒年糕、紫
 ("https://www.tiktok.com/@pressplayacademy/video/7363597322040741141", "TikTok", 42100, "4M9RYrqzE2k", None, None),  # 誰說國稅局只會追稅？告訴你！國稅局沒跟你
 ("https://www.tiktok.com/@pressplayacademy/video/7363596262815419669", "TikTok", 86000, "KKEpv8PJzOg", None, None),  # 📢2024報稅季來了！你知道嗎？你有機會
 ("https://www.tiktok.com/@pressplayacademy/video/7361269877459422484", "TikTok", 9668, "2yfddm7FY8s", None, None),  # 你也是起床先喝水嗎？ 小心疾病找上門(怕
 ("https://www.tiktok.com/@pressplayacademy/video/7353535113528904980", "TikTok", 216000, "WHODSsr7aaQ", None, None),  # 地震來了怎麼辦？ #地震  #地震自救 
 ("https://www.tiktok.com/@pressplayacademy/video/7345413427172510978", "TikTok", 209500, "2yfddm7FY8s", None, None),  # 你也是起床先喝水嗎？ 小心疾病找上門(怕
 ("https://www.tiktok.com/@pressplayacademy/video/7338354205075180801", "TikTok", 236200, "IaPPy04kaAY", None, None),  # 為什麼薑母鴨一定要用母鴨？ #冷知識 #
 ("https://www.tiktok.com/@pressplayacademy/video/7312296176181628161", "TikTok", 251300, "ppedZNivdX4", None, None),  # 騎士霧煞煞！有待轉標誌卻無待轉格，到底要
 ("https://www.tiktok.com/@pressplayacademy/video/7312292373134970114", "TikTok", 65200, "Lx08G5xM5UU", None, None),  # 區間測速真的能提升道路安全嗎？ ｜ #s
 ("https://www.tiktok.com/@pressplayacademy/video/7312291891100257537", "TikTok", 25000, "02Y2FysyFiI", None, None),  # 機車族看過來！騎路肩超危險，車禍機率是內
 ("https://www.tiktok.com/@pressplayacademy/video/7311982263351151873", "TikTok", 188100, "WZPrP3i4MVk", None, None),  # 台灣駕照雞腿換？他國駕照又貴又難考｜ #
 ("https://www.tiktok.com/@pressplayacademy/video/7311218917597400322", "TikTok", 93100, "lrTBq--X9is", None, None),  # 機車兩段式待轉，真的有比較安全嗎？｜ #
 ("https://www.tiktok.com/@pressplayacademy/video/7311218304931089666", "TikTok", 158400, "uva8A-lr46g", None, None),  # 台灣難停車的根本原因！人行道不能騎車，為
 ("https://www.tiktok.com/@pressplayacademy/video/7389146273309347089", "TikTok", 5194, "vmYXgzWaGQU", None, None),  # 一百萬多久可以翻倍？兩年可以變三百萬？ 
]
