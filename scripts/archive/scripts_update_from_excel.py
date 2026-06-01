#!/usr/bin/env python3
"""
Comprehensive update from Excel roster
★01_グリーンイノベーションユニット名簿_20250502更新.xlsx

Applies to ALL cohorts 2021–2025:
  1. Japanese display name (h1 name-jp field) — where correct kanji known
  2. Supervisor name in hero-subline, supervisor section, and meta-card
  3. Supervisor department/org in supervisor section
  4. Affiliation + Major/Department in hero-subline and meta-card (2021 & 2022 only)

Run from project root:
    python3 scripts_update_from_excel.py
"""

from pathlib import Path
import re

BASE = Path(__file__).parent

# ── Organisation English translations ─────────────────────────────────────────
ORG_EN = {
    "経済学研究院":                      "Faculty of Economics",
    "工学研究院":                        "Faculty of Engineering",
    "総合理工学研究院":                   "Faculty of Engineering Sciences",
    "先導物質化学研究所":                  "Institute for Materials Chemistry and Engineering",
    "人間環境学研究院":                   "Faculty of Human-Environment Studies",
    "人間環境科学研究院":                  "Faculty of Human-Environment Studies",
    "エネルギー研究教育機構":               "Institute for Energy Research and Education",
    "カーボンニュートラル・エネルギー国際研究所": "I²CNER / International Institute for Carbon-Neutral Energy Research",
    "次世代燃料電池産学連携研究センター":       "Next-Generation Fuel Cell Research Center",
    "農学研究院":                        "Faculty of Agriculture",
    "理学研究院":                        "Faculty of Science",
    "応用力学研究所":                     "Research Institute for Applied Mechanics",
}

TITLE_EN = {"教授": "Professor", "准教授": "Associate Professor"}


def sup_display(sup_name, sup_org_jp, sup_title_jp):
    """Format dept-line strings for EN and JP supervisor section."""
    org_en = ORG_EN.get(sup_org_jp, sup_org_jp)
    title_en = TITLE_EN.get(sup_title_jp, "")
    if title_en and sup_org_jp:
        dept_en = f"{title_en}, {org_en}"
        dept_jp = f"{sup_title_jp}、{sup_org_jp}"
    elif sup_org_jp:
        dept_en = org_en
        dept_jp = sup_org_jp
    else:
        dept_en = dept_jp = ""
    return dept_en, dept_jp


# ── Student data ──────────────────────────────────────────────────────────────
# Keys: slug (filename without .html)
# Values: dict with:
#   name_jp           — correct Japanese/kanji name (None = keep as-is)
#   name_en_current   — string currently in JP name field to replace (None = skip)
#   affiliation_en    — English affiliation (None = skip / already filled)
#   dept_en           — English major/department (None = skip)
#   sup_name          — supervisor display name (None = no supervisor data)
#   sup_org_jp        — supervisor's institute JP (None = no data)
#   sup_title_jp      — 教授 / 准教授 / None
#   cohort            — used to select correct students/ subdirectory

STUDENTS = {

    # ── 2021 ─────────────────────────────────────────────────────────────────
    "2021/daiki-nishimura": {
        "name_jp": "西村 大輝",    "name_en_current": "Daiki Nishimura",
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": None, "sup_org_jp": None, "sup_title_jp": None,
    },
    "2021/haruka-mitoma": {
        "name_jp": "三苫 春香",    "name_en_current": "Haruka Mitoma",
        "affiliation_en": "Graduate School of Economics",
        "dept_en": "Department of Economic Systems",
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2021/keitaro-maeno": {
        "name_jp": "前野 啓太郎",   "name_en_current": "Keitaro Maeno",
        "affiliation_en": "Graduate School of Economics",
        "dept_en": "Department of Economic Systems",
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2021/kento-komatsubara": {
        "name_jp": "小松原 建人",   "name_en_current": "Kento Komatsubara",
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Civil and Structural Engineering",
        "sup_name": "馬奈木 俊介", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2021/likhith-manjunatha": {
        "name_jp": None,          "name_en_current": None,   # keep English name
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Hydrogen Energy Systems",
        "sup_name": "林 灯", "sup_org_jp": "エネルギー研究教育機構", "sup_title_jp": "教授",
    },
    "2021/masatoshi-tashima": {
        "name_jp": "田島 正俊",    "name_en_current": "Masatoshi Tashima",
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "アルブレヒト 建", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": "准教授",
    },
    "2021/mingxu-sun": {
        "name_jp": None,          "name_en_current": None,   # no kanji in roster
        "affiliation_en": "Graduate School of Science",
        "dept_en": "Department of Chemistry",
        "sup_name": "山内 美穂", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": "教授",
    },
    "2021/sun-mingxu": {          # duplicate file — same data
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Science",
        "dept_en": "Department of Chemistry",
        "sup_name": "山内 美穂", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": "教授",
    },
    "2021/tianhui-fan": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Economics",
        "dept_en": "Department of Economic Systems",
        "sup_name": "アンドリュー・チャップマン",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": "准教授",
    },
    "2021/timothee-redarce": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Hydrogen Energy Systems",
        "sup_name": "松永 久生", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2021/toraharu-watanabe": {
        "name_jp": "渡邊 虎春",    "name_en_current": "Toraharu Watanabe",
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Naval Architecture and Ocean Engineering",
        "sup_name": "篠田 岳思", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2021/xiaofeng-shen": {
        "name_jp": "沈 小烽",     "name_en_current": "Xiaofeng Shen",
        "affiliation_en": "Graduate School of Integrated Frontier Sciences",
        "dept_en": "Department of Automotive Science",
        "sup_name": "渡邊 源規",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": "准教授",
    },
    "2021/yulu-chen": {
        "name_jp": "陳 雨露",     "name_en_current": "Yulu Chen",
        "affiliation_en": "Graduate School of Human-Environment Studies",
        "dept_en": "Department of Spatial Systems",
        "sup_name": "尾崎 明仁", "sup_org_jp": "人間環境学研究院", "sup_title_jp": "教授",
    },

    # ── 2022 ─────────────────────────────────────────────────────────────────
    "2022/daisuke-yoshizawa": {
        "name_jp": "吉澤 大佑",    "name_en_current": "Daisuke Yoshizawa",
        "affiliation_en": "Graduate School of Economics",
        "dept_en": "Department of Economic Systems",
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2022/he-qingyi": {
        "name_jp": "何 清怡",     "name_en_current": "HE QINGYI",
        "affiliation_en": "Graduate School of Human-Environment Studies",
        "dept_en": "Department of Spatial Systems",
        "sup_name": "住吉 大輔", "sup_org_jp": "人間環境学研究院", "sup_title_jp": "教授",
    },
    "2022/qingyi-he": {           # duplicate file
        "name_jp": "何 清怡",     "name_en_current": "Qingyi He",
        "affiliation_en": "Graduate School of Human-Environment Studies",
        "dept_en": "Department of Spatial Systems",
        "sup_name": "住吉 大輔", "sup_org_jp": "人間環境学研究院", "sup_title_jp": "教授",
    },
    "2022/hyun-gyu-park": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "伊藤 一秀", "sup_org_jp": "総合理工学研究院", "sup_title_jp": "教授",
    },
    "2022/park-hyun-gyu": {       # duplicate file
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "伊藤 一秀", "sup_org_jp": "総合理工学研究院", "sup_title_jp": "教授",
    },
    "2022/jacqueline-andrea-hidalgo-jim-nez": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Integrated Frontier Sciences",
        "dept_en": "Department of Automotive Science",
        "sup_name": "Edalati Kaveh",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": "准教授",
    },
    "2022/muhammad-irfan-maulana-kusdhany": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Integrated Frontier Sciences",
        "dept_en": "Department of Automotive Science",
        "sup_name": "西原 正通", "sup_org_jp": "次世代燃料電池産学連携研究センター", "sup_title_jp": "教授",
    },
    "2022/phua-yin-kan": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Applied Chemistry",
        "sup_name": "加藤 幸一郎", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2022/yin-kan-phua": {        # duplicate file
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Engineering",
        "dept_en": "Department of Applied Chemistry",
        "sup_name": "加藤 幸一郎", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2022/ryoma-sato": {
        "name_jp": "佐藤 稜真",    "name_en_current": "Ryoma Sato",
        "affiliation_en": "Graduate School of Bioresource and Bioenvironmental Sciences",
        "dept_en": "Department of Bioresource Sciences",
        "sup_name": "東江 栄", "sup_org_jp": "農学研究院", "sup_title_jp": "教授",
    },
    "2022/shinichi-takeno": {
        "name_jp": "竹野 慎一",    "name_en_current": "Shinichi Takeno",
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "渡邉 賢", "sup_org_jp": "総合理工学研究院", "sup_title_jp": "准教授",
    },
    "2022/sora-matsushima": {
        "name_jp": "松嶋 そら",    "name_en_current": "Sora Matsushima",
        "affiliation_en": "Graduate School of Economics",
        "dept_en": "Department of Economic Systems",
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2022/tatsuya-hamashima": {
        "name_jp": "濱島 達也",    "name_en_current": "Tatsuya Hamashima",
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "永長 久寛", "sup_org_jp": "総合理工学研究院", "sup_title_jp": "教授",
    },
    "2022/yixin-chen": {
        "name_jp": "陳 伊新",     "name_en_current": "Yixin Chen",
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "アルブレヒト 建", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": "准教授",
    },
    "2022/zifei-nie": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": "Graduate School of Integrated Science and Engineering",
        "dept_en": "Interdisciplinary Graduate Program in Engineering Sciences",
        "sup_name": "Farzaneh Hooman",
        "sup_org_jp": "総合理工学研究院", "sup_title_jp": "准教授",
    },

    # ── 2023 — affiliation/dept already filled; only supervisor + name fixes ──
    "2023/go-yokuhou": {
        "name_jp": None,          "name_en_current": None,   # already 呉 翼峰
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "伊藤 衡平", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2023/hiroki-isogawa": {
        "name_jp": None,          "name_en_current": None,   # already 五十川 浩希
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "片山 一成", "sup_org_jp": "総合理工学研究院", "sup_title_jp": "准教授",
    },
    "2023/kentaro-wada": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "久保田 祐信",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": "教授",
    },
    "2023/kotaro-shinozaki": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "西島 潤", "sup_org_jp": "工学研究院", "sup_title_jp": "准教授",
    },
    "2023/narmandakh-khongorzul": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "石原 達己", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2023/seiya-imada": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2023/taisei-tomaru": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        # Supervisor changed per 2025 sheet — using most recent
        "sup_name": "中林 康治", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": None,
    },
    "2023/xuesong-wei": {
        "name_jp": "韋 雪淞",     "name_en_current": "イ セツショウ",  # fix from katakana
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "森 昌司", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2023/yusuke-oga": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2023/yuta-takaoka": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "石原 達己", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2023/yutong-chen": {
        "name_jp": "陳 昱通",     "name_en_current": "陳 雨露",  # correct the earlier mistake
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "住吉 大輔", "sup_org_jp": "人間環境学研究院", "sup_title_jp": "教授",
    },

    # ── 2024 — affiliation/dept filled; supervisor + JP names needed ──────────
    "2024/haomin-fu": {
        "name_jp": "付 昊旻",     "name_en_current": "Haomin FU",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "目代 武史", "sup_org_jp": "経済学研究院", "sup_title_jp": None,
    },
    "2024/itsuki-oyama": {
        "name_jp": "小山 一輝",   "name_en_current": "Itsuki Oyama",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "小菅 佑輔", "sup_org_jp": "総合理工学研究院", "sup_title_jp": None,
    },
    "2024/kodai-matsumoto": {
        "name_jp": "松本 昂大",   "name_en_current": "Kodai Matsumoto",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "藤川 茂紀",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": "教授",
    },
    "2024/ryudai-ueno": {
        "name_jp": "上野 竜大生",  "name_en_current": "Ryudai Ueno",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "佐藤 宣子", "sup_org_jp": "農学研究院", "sup_title_jp": None,
    },
    "2024/shen-siyu": {
        "name_jp": "沈 思語",     "name_en_current": "SHEN Siyu",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "藤井 秀道", "sup_org_jp": "経済学研究院", "sup_title_jp": None,
    },
    "2024/shogo-nakamura": {
        "name_jp": "中村 省吾",   "name_en_current": "Shogo Nakamura",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "佐々木 一成", "sup_org_jp": "工学研究院", "sup_title_jp": "教授",
    },
    "2024/tomomi-shoda": {
        "name_jp": "庄田 朋申",   "name_en_current": "Tomomi Shoda",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "加河 茂美", "sup_org_jp": "経済学研究院", "sup_title_jp": "教授",
    },
    "2024/xianzhe-yang": {
        "name_jp": "楊 賢哲",    "name_en_current": "Xianzhe Yang",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "尾崎 明仁", "sup_org_jp": "人間環境科学研究院", "sup_title_jp": "教授",
    },
    "2024/yuki-noguchi": {
        "name_jp": "野口 湧喜",   "name_en_current": "Yuki Noguchi",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "加藤 太治", "sup_org_jp": "総合理工学研究院", "sup_title_jp": None,
    },
    "2024/yuki-tomita": {
        "name_jp": "冨田 侑樹",   "name_en_current": "Yuki Tomita",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "小澤 弘宜", "sup_org_jp": "理学研究院", "sup_title_jp": "教授",
    },
    "2024/zhang-kaili": {
        "name_jp": None,          "name_en_current": None,   # no kanji in roster
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "Prasanna Divigalpitiya",
        "sup_org_jp": "人間環境科学研究院", "sup_title_jp": None,
    },

    # ── 2025 — only supervisor + a few name fixes ─────────────────────────────
    "2025/kohei-sawada": {
        "name_jp": "澤田 光平",   "name_en_current": "沢田 光平",  # simplified→traditional
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "渡邊 源規",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": None,
    },
    "2025/nozomi-goto": {
        "name_jp": None,          "name_en_current": None,   # already 後藤 希
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "山崎 仁丈", "sup_org_jp": "エネルギー研究教育機構", "sup_title_jp": None,
    },
    "2025/qi-shi": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "渡邊 源規",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": None,
    },
    "2025/rika-iriguchi": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "島田 英樹", "sup_org_jp": "工学研究院", "sup_title_jp": None,
    },
    "2025/ryoshi-oda": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "中林 康治", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": None,
    },
    "2025/takahiro-yamaguchi": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "出射 浩", "sup_org_jp": "応用力学研究所", "sup_title_jp": None,
    },
    "2025/wang-sheng": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "島田 英樹", "sup_org_jp": "工学研究院", "sup_title_jp": None,
    },
    "2025/yan-chenyu": {
        "name_jp": "厳 晨雨",     "name_en_current": "Yan Chenyu",
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "永長 久寛", "sup_org_jp": "総合理工学研究院", "sup_title_jp": None,
    },
    "2025/yuki-nishimura": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "藤澤 彰英", "sup_org_jp": "総合理工学研究院", "sup_title_jp": None,
    },
    "2025/zhai-xiazhe": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "宮脇 仁", "sup_org_jp": "先導物質化学研究所", "sup_title_jp": None,
    },
    "2025/zhang-jingxuan": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "Andrew Chapman",
        "sup_org_jp": "カーボンニュートラル・エネルギー国際研究所", "sup_title_jp": None,
    },
    "2025/zhanyi-xiang": {
        "name_jp": None,          "name_en_current": None,
        "affiliation_en": None,   "dept_en": None,
        "sup_name": "伊藤 衡平", "sup_org_jp": "工学研究院", "sup_title_jp": None,
    },
}


def update_file(key, d):
    cohort, slug = key.split("/", 1)
    path = BASE / "students" / cohort / f"{slug}.html"
    if not path.exists():
        print(f"  MISS  {key}.html — file not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html

    # ── 1. Japanese display name ──────────────────────────────────────────────
    if d.get("name_jp") and d.get("name_en_current"):
        old_tag = f'<h1 class="name name-jp" data-lang-jp="">{d["name_en_current"]}</h1>'
        new_tag = f'<h1 class="name name-jp" data-lang-jp="">{d["name_jp"]}</h1>'
        html = html.replace(old_tag, new_tag, 1)

    # ── 2. Hero-subline affiliation/department (2021 & 2022 only) ────────────
    if d.get("affiliation_en"):
        html = html.replace(
            '<dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">所属</dt><dd>To be added</dd>',
            f'<dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">所属</dt><dd>{d["affiliation_en"]}</dd>',
            1
        )
    if d.get("dept_en"):
        html = html.replace(
            '<dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">専攻・部局</dt><dd>To be added</dd>',
            f'<dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">専攻・部局</dt><dd>{d["dept_en"]}</dd>',
            1
        )
    # ── 2b. Meta-card affiliation/department (2021 & 2022 only) ─────────────
    if d.get("affiliation_en"):
        html = html.replace(
            '<dt>Affiliation</dt><dd>To be added</dd>',
            f'<dt>Affiliation</dt><dd>{d["affiliation_en"]}</dd>',
            1
        )
    if d.get("dept_en"):
        html = html.replace(
            '<dt>Major / Department</dt><dd>To be added</dd>',
            f'<dt>Major / Department</dt><dd>{d["dept_en"]}</dd>',
            1
        )

    # ── 3. Supervisor in hero-subline ─────────────────────────────────────────
    if d.get("sup_name"):
        html = html.replace(
            '<dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>To be added</dd>',
            f'<dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>{d["sup_name"]}</dd>',
            1
        )

    # ── 4. Supervisor section (name-line + dept + avatar) ─────────────────────
    if d.get("sup_name"):
        dept_en, dept_jp = sup_display(d["sup_name"], d.get("sup_org_jp"), d.get("sup_title_jp"))
        initial = d["sup_name"][0] if d["sup_name"] else "?"

        html = html.replace(
            '<div class="name-line" data-lang-en="">To be added</div>',
            f'<div class="name-line" data-lang-en="">{d["sup_name"]}</div>', 1
        )
        html = html.replace(
            '<div class="name-line" data-lang-jp="">追記予定</div>',
            f'<div class="name-line" data-lang-jp="">{d["sup_name"]}</div>', 1
        )
        if dept_en:
            html = html.replace(
                '<div class="dept" data-lang-en="">Supervisor information is not available yet.</div>',
                f'<div class="dept" data-lang-en="">{dept_en}</div>', 1
            )
        if dept_jp:
            html = html.replace(
                '<div class="dept" data-lang-jp="">指導教員情報は追記予定です。</div>',
                f'<div class="dept" data-lang-jp="">{dept_jp}</div>', 1
            )
        html = html.replace(
            '<div class="sup-avatar">?</div>',
            f'<div class="sup-avatar">{initial}</div>', 1
        )

    # ── 5. Meta-card supervisor ───────────────────────────────────────────────
    if d.get("sup_name"):
        html = html.replace(
            '<dt>Supervisor</dt><dd>To be added</dd>',
            f'<dt>Supervisor</dt><dd>{d["sup_name"]}</dd>', 1
        )

    if html == original:
        print(f"  WARN  {key} — no changes made")
    else:
        path.write_text(html, encoding="utf-8")
        changes = []
        if d.get("name_jp"):       changes.append("name")
        if d.get("affiliation_en"): changes.append("affiliation")
        if d.get("sup_name"):      changes.append("supervisor")
        print(f"  OK    {key}  [{', '.join(changes)}]")


def main():
    print(f"Updating {len(STUDENTS)} student files from Excel data\n")
    current_cohort = None
    for key, d in STUDENTS.items():
        cohort = key.split("/")[0]
        if cohort != current_cohort:
            print(f"\n── {cohort} ──")
            current_cohort = cohort
        update_file(key, d)
    print("\nDone.")


if __name__ == "__main__":
    main()
