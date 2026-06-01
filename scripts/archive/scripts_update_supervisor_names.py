#!/usr/bin/env python3
"""
Update supervisor display names in all 2021–2025 student pages so that:
  data-lang-en  →  "Prof. Firstname SURNAME"
  data-lang-jp  →  "姓 名 教授/准教授"

2026 pages already have correct bilingual names and are NOT touched.

Also regenerates data/students.json with updated supervisor fields.

Run from project root:
    python3 scripts_update_supervisor_names.py
"""

import re, json
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent

# ── Complete supervisor map: JP kanji → (EN display, JP display) ──────────────
SUPERVISOR_MAP = {
    # Resolved from Q-PIT teacher pages
    '加河 茂美':              ('Prof. Shigemi KAGAWA',           '加河 茂美 教授'),
    '馬奈木 俊介':            ('Prof. Shunsuke MANAGI',          '馬奈木 俊介 教授'),
    '松永 久生':              ('Prof. Hisao MATSUNAGA',          '松永 久生 教授'),
    '尾崎 明仁':              ('Prof. Akihito OZAKI',            '尾崎 明仁 教授'),
    '伊藤 衡平':              ('Prof. Kohei ITOH',               '伊藤 衡平 教授'),
    '住吉 大輔':              ('Prof. Daisuke SUMIYOSHI',        '住吉 大輔 教授'),
    '佐々木 一成':            ('Prof. Issei SASAKI',             '佐々木 一成 教授'),
    '加藤 幸一郎':            ('Prof. Koichiro KATO',            '加藤 幸一郎 教授'),
    '宮脇 仁':                ('Prof. Hitoshi MIYAWAKI',         '宮脇 仁 准教授'),
    '小澤 弘宜':              ('Prof. Hiroki OZAWA',             '小澤 弘宜 准教授'),
    '山内 美穂':              ('Prof. Miho YAMAUCHI',            '山内 美穂 教授'),
    '山崎 仁丈':              ('Prof. Yoshihiro YAMAZAKI',       '山崎 仁丈 教授'),
    '島田 英樹':              ('Prof. Hideki SHIMADA',           '島田 英樹 教授'),
    '林 灯':                  ('Prof. Akari HAYASHI',            '林 灯 教授'),
    '森 昌司':                ('Prof. Shoji MORI',               '森 昌司 教授'),
    '永長 久寛':              ('Prof. Hisahiro EINAGA',          '永長 久寛 教授'),
    '渡邉 賢':                ('Prof. Ken WATANABE',             '渡邉 賢 教授'),
    '石原 達己':              ('Prof. Tatsumi ISHIHARA',         '石原 達己 教授'),
    '藤井 秀道':              ('Prof. Hidemichi FUJII',          '藤井 秀道 教授'),
    '藤川 茂紀':              ('Prof. Shigenori FUJIKAWA',       '藤川 茂紀 教授'),
    '西原 正通':              ('Prof. Masamichi NISHIHARA',      '西原 正通 教授'),
    '久保田 祐信':            ('Prof. Yunoshin KUBOTA',          '久保田 祐信 教授'),
    'アルブレヒト 建':        ('Prof. Ken ALBRECHT',             'アルブレヒト 建 准教授'),
    '佐藤 宣子':              ('Prof. Noriko SATO',              '佐藤 宣子 教授'),
    # Confirmed from 2026 cross-reference
    '渡邊 源規':              ('Prof. Motonori WATANABE',        '渡邊 源規 教授'),
    '片山 一成':              ('Prof. Kazunari KATAYAMA',        '片山 一成 教授'),
    '中林 康治':              ('Prof. Koji NAKABAYASHI',         '中林 康治 教授'),
    # Resolved via hyoka / researchmap (404 on Q-PIT)
    '伊藤 一秀':              ('Prof. Kazuhide ITO',             '伊藤 一秀 教授'),
    '出射 浩':                ('Prof. Hiroshi IDEI',             '出射 浩 教授'),
    '加藤 太治':              ('Prof. Daiji KATO',               '加藤 太治 教授'),
    '小菅 佑輔':              ('Prof. Yusuke KOSUGA',            '小菅 佑輔 教授'),
    '篠田 岳思':              ('Prof. Takeshi SHINODA',          '篠田 岳思 教授'),
    '藤澤 彰英':              ('Prof. Akihide FUJISAWA',         '藤澤 彰英 教授'),
    '西島 潤':                ('Prof. Jun NISHIJIMA',            '西島 潤 教授'),
    '東江 栄':                ('Prof. Sakae AGARIE',             '東江 栄 教授'),
    '目代 武史':              ('Prof. Takefumi MOKUDAI',         '目代 武史 教授'),
    # English-named supervisors
    'Andrew Chapman':         ('Prof. Andrew CHAPMAN',           'アンドリュー・チャップマン 教授'),
    'アンドリュー・チャップマン': ('Prof. Andrew CHAPMAN',        'アンドリュー・チャップマン 教授'),
    'Edalati Kaveh':          ('Prof. Kaveh EDALATI',            'Edalati Kaveh 教授'),
    'Farzaneh Hooman':        ('Prof. Farzaneh HOOMAN',          'Farzaneh Hooman 教授'),
    'Prasanna Divigalpitiya': ('Prof. Prasanna DIVIGALPITIYA',   'Prasanna Divigalpitiya 教授'),
}


# ── HTML update ───────────────────────────────────────────────────────────────

def update_html(html):
    """
    Replace EN and JP supervisor link texts in the hero-subline.
    Returns (new_html, old_kanji_name or None).
    """
    m = re.search(
        r'(<dt data-lang-en="">Supervisor</dt>.*?<dd>)'
        r'(<a href="[^"]+" [^>]*data-lang-en=""[^>]*>)\s*(.*?)\s*(</a>)'
        r'(<a href="[^"]+" [^>]*data-lang-jp=""[^>]*>)\s*(.*?)\s*(</a></dd>)',
        html, re.DOTALL
    )
    if not m:
        return html, None

    current_en = m.group(3).strip()
    current_jp = m.group(6).strip()

    # Determine which key to look up (prefer the current_en name as key)
    lookup_key = current_en
    if lookup_key not in SUPERVISOR_MAP:
        lookup_key = current_jp  # fallback
    if lookup_key not in SUPERVISOR_MAP:
        return html, f'UNKNOWN:{current_en}'

    new_en, new_jp = SUPERVISOR_MAP[lookup_key]

    # Build replacement: keep all tag attributes, just swap inner text
    new_block = (
        m.group(1) +
        m.group(2) + new_en + m.group(4) +
        m.group(5) + new_jp + m.group(7)
    )
    return html[:m.start()] + new_block + html[m.end():], lookup_key


def process_html_files():
    COHORTS = ['2021', '2022', '2023', '2024', '2025']
    updated = 0
    skipped = 0
    unknown = []

    for cohort in COHORTS:
        d = BASE / 'students' / cohort
        pages = sorted(p for p in d.glob('*.html') if p.name != 'index.html')
        print(f'\n── {cohort} ──')
        for p in pages:
            html = p.read_text(encoding='utf-8')
            new_html, key = update_html(html)
            if key is None:
                print(f'  SKIP  {p.name} — no supervisor link (To be added / missing)')
                skipped += 1
            elif isinstance(key, str) and key.startswith('UNKNOWN:'):
                print(f'  WARN  {p.name} — {key}')
                unknown.append((cohort, p.name, key))
                skipped += 1
            elif new_html != html:
                p.write_text(new_html, encoding='utf-8')
                en, jp = SUPERVISOR_MAP[key]
                print(f'  OK    {p.name}  →  {en}  /  {jp}')
                updated += 1
            else:
                print(f'  SKIP  {p.name} — already updated')
                skipped += 1

    print(f'\nHTML: {updated} updated, {skipped} skipped')
    if unknown:
        print('Unknown supervisor keys:')
        for c, f, k in unknown:
            print(f'  {c}/{f}: {k}')
    return updated


# ── JSON update ───────────────────────────────────────────────────────────────

PRIMARY = {
    '2021': ['daiki-nishimura','haruka-mitoma','keitaro-maeno','kento-komatsubara',
             'likhith-manjunatha','masatoshi-tashima','mingxu-sun','tianhui-fan',
             'timothee-redarce','toraharu-watanabe','xiaofeng-shen','yulu-chen'],
    '2022': ['daisuke-yoshizawa','hyun-gyu-park','jacqueline-andrea-hidalgo-jim-nez',
             'muhammad-irfan-maulana-kusdhany','qingyi-he','ryoma-sato','shinichi-takeno',
             'sora-matsushima','tatsuya-hamashima','yin-kan-phua','yixin-chen','zifei-nie'],
    '2023': ['go-yokuhou','hiroki-isogawa','kentaro-wada','kotaro-shinozaki',
             'narmandakh-khongorzul','seiya-imada','taisei-tomaru','xuesong-wei',
             'yusuke-oga','yuta-takaoka','yutong-chen'],
    '2024': ['haomin-fu','itsuki-oyama','kodai-matsumoto','ryudai-ueno','shen-siyu',
             'shogo-nakamura','tomomi-shoda','xianzhe-yang','yuki-noguchi',
             'yuki-tomita','zhang-kaili'],
    '2025': ['kohei-sawada','nozomi-goto','qi-shi','rika-iriguchi','ryoshi-oda',
             'takahiro-yamaguchi','wang-sheng','yan-chenyu','yuki-nishimura',
             'zhai-xiazhe','zhang-jingxuan','zhanyi-xiang'],
    '2026': ['chang-s','chen-h','jiang-z','kotajima-m','minoda-k','mochizuki-t',
             'nakagawa-n','omoto-s','sun-h','wang-w','yoshida-s','zheng-q','zou-z'],
}

PROGRAMME = {
    '2021': 'Q-ENERGY Fellowship', '2022': 'Q-ENERGY Fellowship',
    '2023': 'Q-ENERGY Fellowship', '2024': 'K2-SPRING',
    '2025': 'K2-SPRING',           '2026': 'K2-SPRING',
}


def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    import html as html_lib
    s = html_lib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def extract_supervisor_bilingual(html):
    """Return (name_en, name_jp, url) from hero-subline supervisor dd."""
    m = re.search(r'<dt data-lang-en="">Supervisor</dt>.*?<dd>(.*?)</dd>', html, re.DOTALL)
    if not m:
        return None, None, None
    dd = m.group(1).strip()
    if 'To be added' in dd or not dd:
        return None, None, None
    url_m  = re.search(r'href="([^"]+)"', dd)
    en_m   = re.search(r'data-lang-en=""[^>]*>\s*(.*?)\s*</a>', dd, re.DOTALL)
    jp_m   = re.search(r'data-lang-jp=""[^>]*>\s*(.*?)\s*</a>', dd, re.DOTALL)
    url    = url_m.group(1) if url_m else None
    name_en = strip_tags(en_m.group(1)) if en_m else None
    name_jp = strip_tags(jp_m.group(1)) if jp_m else None
    # Dedup if still same (shouldn't happen after update but defensive)
    if name_en and name_jp and name_en == name_jp:
        name_jp = None
    return name_en, name_jp, url


def extract_student_record(slug, cohort, html):
    """Minimal re-extraction for JSON update (supervisor fields only)."""
    # Reuse the full extractor logic via import-free inline approach
    from scripts_extract_student_data import (
        extract_student
    )
    return extract_student(slug, cohort, html)


def rebuild_json():
    """Rebuild data/students.json from current HTML files with bilingual supervisor."""
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location(
        'extract', BASE / 'scripts_extract_student_data.py')
    mod  = importlib.util.load_from_spec(spec) if hasattr(importlib.util, 'load_from_spec') else None

    # Simpler: just call the extract_student function directly
    # We'll inline the extraction here to add supervisor_name_jp
    students = []
    for cohort, slugs in sorted(PRIMARY.items()):
        for slug in slugs:
            path = BASE / 'students' / cohort / f'{slug}.html'
            if not path.exists():
                continue
            html = path.read_text(encoding='utf-8')

            # Get the full record from the existing extractor
            import scripts_extract_student_data as ext
            rec = ext.extract_student(slug, cohort, html)

            # Enrich with JP supervisor name
            _, name_jp, _ = extract_supervisor_bilingual(html)
            rec['supervisor_name_jp'] = name_jp

            students.append(rec)

    out = BASE / 'data' / 'students.json'
    payload = {
        'generated': str(date.today()),
        'total': len(students),
        'students': students,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nRebuilt data/students.json — {len(students)} records')


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    print('=== Updating supervisor names in HTML pages ===')
    process_html_files()

    print('\n=== Rebuilding data/students.json ===')
    rebuild_json()

    print('\nDone.')


if __name__ == '__main__':
    main()
