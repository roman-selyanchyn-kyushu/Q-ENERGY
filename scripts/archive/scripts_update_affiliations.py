#!/usr/bin/env python3
"""
Update affiliation and major/department fields in all 2021–2025 student pages:
  - Adds proper Japanese text alongside English
  - Upgrades <dd>TEXT</dd> → <dd data-lang-en="">EN</dd><dd data-lang-jp="">JP</dd>

Source: official KU roster Excel + confirmed 2026-page names.

Run from project root:
    python3 scripts_update_affiliations.py
"""

import re, openpyxl
from pathlib import Path

BASE       = Path(__file__).parent
EXCEL_PATH = Path('/Users/romanselyanchyn/Library/CloudStorage/Dropbox/00-QPIT/Q-fellowship/01-Contact list/★01_グリーンイノベーションユニット名簿_20250502更新.xlsx')
COHORTS    = ['2021', '2022', '2023', '2024', '2025']

# ── Official school name map (JP → EN) ────────────────────────────────────────
SCHOOL_MAP = {
    '経済学府':           ('Graduate School of Economics',
                          '経済学府'),
    '工学府':             ('Graduate School of Engineering',
                          '工学府'),
    '人間環境学府':        ('Graduate School of Human-Environment Studies',
                          '人間環境学府'),
    '人間環境科学府':      ('Graduate School of Human-Environment Studies',
                          '人間環境学府'),        # normalise to 人間環境学府
    '総合理工学府':        ('Interdisciplinary Graduate School of Engineering Sciences',
                          '総合理工学府'),
    '統合新領域学府':      ('Graduate School of Integrated Frontier Sciences',
                          '統合新領域学府'),
    '生物資源環境科学府':  ('Graduate School of Bioresource and Bioenvironmental Sciences',
                          '生物資源環境科学府'),
    '理学府':             ('Graduate School of Science',
                          '理学府'),
    'システム情報科学府':  ('Graduate School of Information Science and Electrical Engineering',
                          'システム情報科学府'),
}

# ── Official department name map (JP → EN) ────────────────────────────────────
DEPT_MAP = {
    # 工学府
    '水素エネルギーシステム専攻':     'Department of Hydrogen Energy Systems',
    '応用化学専攻':                   'Department of Applied Chemistry',
    '機械工学専攻':                   'Department of Mechanical Engineering',
    '土木工学専攻':                   'Department of Civil Engineering',
    '船舶海洋工学専攻':               'Department of Naval Architecture and Ocean Engineering',
    '地球資源システム工学専攻':       'Department of Earth Resources Engineering',
    '材料工学専攻':                   'Department of Materials Science and Engineering',
    # 経済学府
    '経済システム専攻':               'Department of Economic Systems',
    # 人間環境学府
    '空間システム専攻':               'Department of Spatial Systems',
    '都市共生デザイン専攻':           'Department of Urban and Environmental Design',
    '九州大学・釜山大学校都市・建築学国際連携専攻':
                                      'KU–PNU International Joint Graduate Program in Urban and Architectural Studies',
    # 総合理工学府
    '総合理工学専攻':                 'Department of Interdisciplinary Science and Engineering',
    # 統合新領域学府
    'オートモーティブサイエンス専攻': 'Department of Automotive Science',
    # 生物資源環境科学府
    '資源生物科学専攻':               'Department of Bioresource Sciences',
    '環境農学専攻':                   'Department of Agricultural and Environmental Biology',
    # 理学府
    '化学専攻':                       'Department of Chemistry',
}

# ── Parse Excel → student_id: (school_jp, dept_jp) ───────────────────────────
def normalise(s):
    """Normalise special Unicode lookalike characters used in some Excel cells."""
    if not s: return s
    # CJK Radical ⼈ (U+2F08) → 人 (U+4EBA), etc.
    return (str(s)
            .replace('⼈', '人')   # ⼈ → 人
            .replace('⽆', '水')   # ⽔ → 水  (just in case)
            .strip())


def parse_excel():
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
    mapping = {}  # student_id → (school_jp, dept_jp)

    # ── K2-SPRING sheets: col order №|unit|year|学府|専攻|学籍番号|名前 ──────
    for sname in ['K2-SPRING GI Unit_2024年度', 'K2-SPRING GI Unit_2025年度']:
        ws = wb[sname]
        for row in ws.iter_rows(values_only=True):
            if not row[0]: continue          # skip empty / header rows
            sid    = str(row[5]).strip() if row[5] else ''
            school = normalise(row[3])
            dept   = normalise(row[4])
            if not sid or sid == '学籍番号': continue
            mapping[sid] = (school, dept)

    # ── Q-ENERGY Fellowship sheet: col order None|№|名前|フリガナ|学府専攻|学籍番号 ─
    ws = wb['Q-ENERGY Fellowship_20240401']
    for row in ws.iter_rows(values_only=True):
        if not isinstance(row[1], int): continue   # skip headers (non-integer in col1)
        sid      = str(row[5]).strip() if row[5] else ''
        combined = normalise(row[4]) or ''
        if not sid: continue
        # Split combined 学府専攻 into school + dept using SCHOOL_MAP keys
        school, dept = '', ''
        for s in SCHOOL_MAP:
            if combined.startswith(s):
                school = s; dept = combined[len(s):].strip(); break
        if not school:
            school = combined   # fallback: keep combined
        if sid not in mapping:   # K2-SPRING data takes precedence (more recent)
            mapping[sid] = (school, dept)

    return mapping


# ── Match student slug to student_id via the page filename hint ───────────────
# We'll extract student_id from the HTML page (it appears in footer-meta or nowhere).
# Fallback: match by searching all HTML pages for patterns in the Excel data.
# Simpler: build a slug→id map from known data.

SLUG_TO_ID = {
    # 2021
    'daiki-nishimura':    '3ES21028T',
    'haruka-mitoma':      '3EC21102Y',
    'keitaro-maeno':      '3EC21103G',
    'kento-komatsubara':  '3TE21919T',
    'likhith-manjunatha': '3TE20810G',
    'masatoshi-tashima':  '3ES21012P',
    'mingxu-sun':         '3SC20119E',
    'tianhui-fan':        '3EC21104R',
    'timothee-redarce':   '3TE21475S',
    'toraharu-watanabe':  '3TE21722T',
    'xiaofeng-shen':      '3FS21104K',
    'yulu-chen':          '3HE21403Y',
    # 2022
    'daisuke-yoshizawa':  '3EC22104T',
    'hyun-gyu-park':      '3ES21046W',
    'jacqueline-andrea-hidalgo-jim-nez': '3FS22107G',
    'muhammad-irfan-maulana-kusdhany':   '3FS22106Y',
    'qingyi-he':          '3HE22408P',
    'ryoma-sato':         '3BE22003P',
    'shinichi-takeno':    '3ES22014E',
    'sora-matsushima':    '3EC22101N',
    'tatsuya-hamashima':  '3ES22008T',
    'yin-kan-phua':       '3TE22119W',
    'yixin-chen':         '3ES22025M',
    'zifei-nie':          '3ES22022E',
    # 2023
    'go-yokuhou':         '3TE23478S',
    'hiroki-isogawa':     '3ES23014W',
    'kentaro-wada':       '3TE23328W',
    'kotaro-shinozaki':   '3TE23785M',
    'narmandakh-khongorzul': '3FS23105N',
    'seiya-imada':        '3EC23105Y',
    'taisei-tomaru':      '3ES23016S',
    'xuesong-wei':        '3TE22327N',
    'yusuke-oga':         '3EC23103P',
    'yuta-takaoka':       '3TE23105T',
    'yutong-chen':        '3HE23401T',
    # 2024
    'haomin-fu':          '3FS24103K',
    'itsuki-oyama':       '3ES24015R',
    'kodai-matsumoto':    '3TE24123G',
    'ryudai-ueno':        '3BE24107R',
    'shen-siyu':          '3EC24105E',
    'shogo-nakamura':     '3TE24471M',
    'tomomi-shoda':       '3EC24106K',
    'xianzhe-yang':       '3HE24602T',
    'yuki-noguchi':       '3ES24022G',
    'yuki-tomita':        '3SC24106E',
    'zhang-kaili':        '3HE23006S',
    # 2025
    'kohei-sawada':       '3FS25105Y',
    'nozomi-goto':        '3TE25003P',
    'qi-shi':             '3FS25104S',
    'rika-iriguchi':      '3TE25784N',
    'ryoshi-oda':         '3ES25016M',
    'takahiro-yamaguchi': '3ES25006K',
    'wang-sheng':         '3TE24796N',
    'yan-chenyu':         '3ES24061W',
    'yuki-nishimura':     '3ES25045G',
    'zhai-xiazhe':        '3ES25019S',
    'zhang-jingxuan':     '3EC24108M',
    'zhanyi-xiang':       '3TE25473R',
}

# ── HTML update helpers ───────────────────────────────────────────────────────

def upgrade_dd(html, label_en, new_en, new_jp):
    """
    Replace:  <dl><dt data-lang-en="">LABEL</dt>...<dd>OLD</dd></dl>
    With:     <dl><dt data-lang-en="">LABEL</dt>...<dd data-lang-en="">EN</dd><dd data-lang-jp="">JP</dd></dl>
    """
    pattern = re.compile(
        r'(<dl><dt data-lang-en="">' + re.escape(label_en) +
        r'</dt><dt data-lang-jp="">[^<]+</dt>)<dd>[^<]*</dd>(</dl>)',
        re.DOTALL
    )
    replacement = (
        r'\g<1>'
        f'<dd data-lang-en="">{new_en}</dd>'
        f'<dd data-lang-jp="">{new_jp}</dd>'
        r'\g<2>'
    )
    new_html, n = pattern.subn(replacement, html, count=1)
    return new_html, n > 0


def already_bilingual(html, label_en):
    """Check if the dd is already data-lang-en format."""
    return bool(re.search(
        r'<dl><dt data-lang-en="">' + re.escape(label_en) +
        r'</dt>.*?<dd data-lang-en="">', html, re.DOTALL
    ))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    id_map = parse_excel()
    print(f'Loaded {len(id_map)} student IDs from Excel.\n')

    updated = skipped = warned = 0

    for cohort in COHORTS:
        d = BASE / 'students' / cohort
        pages = sorted(p for p in d.glob('*.html') if p.name != 'index.html')
        print(f'── {cohort} ──')

        for p in pages:
            slug = p.stem
            # Skip alias files (sun-mingxu, park-hyun-gyu, phua-yin-kan, he-qingyi)
            student_id = SLUG_TO_ID.get(slug)
            if not student_id:
                print(f'  SKIP  {slug} — no ID mapping (alias or unknown)')
                skipped += 1
                continue

            entry = id_map.get(student_id)
            if not entry:
                print(f'  WARN  {slug} ({student_id}) — not found in Excel')
                warned += 1
                continue

            school_jp, dept_jp = entry
            school_info = SCHOOL_MAP.get(school_jp)
            if not school_info:
                print(f'  WARN  {slug} — unknown school: {school_jp!r}')
                warned += 1
                continue

            school_en, school_jp_clean = school_info
            dept_en = DEPT_MAP.get(dept_jp, dept_jp)  # fallback to JP if no mapping

            html = p.read_text(encoding='utf-8')
            changed = False

            # Update Affiliation
            if not already_bilingual(html, 'Affiliation'):
                html, ok = upgrade_dd(html, 'Affiliation', school_en, school_jp_clean)
                if ok: changed = True
            else:
                # Already bilingual — just ensure EN/JP are correct
                html_new = re.sub(
                    r'(<dl><dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">[^<]+</dt>)'
                    r'<dd data-lang-en="">[^<]*</dd><dd data-lang-jp="">[^<]*</dd>(</dl>)',
                    rf'\g<1><dd data-lang-en="">{school_en}</dd><dd data-lang-jp="">{school_jp_clean}</dd>\g<2>',
                    html, count=1
                )
                if html_new != html: html = html_new; changed = True

            # Update Major / Department
            if dept_jp and not already_bilingual(html, 'Major / Department'):
                html, ok = upgrade_dd(html, 'Major / Department', dept_en, dept_jp)
                if ok: changed = True
            elif dept_jp and already_bilingual(html, 'Major / Department'):
                html_new = re.sub(
                    r'(<dl><dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">[^<]+</dt>)'
                    r'<dd data-lang-en="">[^<]*</dd><dd data-lang-jp="">[^<]*</dd>(</dl>)',
                    rf'\g<1><dd data-lang-en="">{dept_en}</dd><dd data-lang-jp="">{dept_jp}</dd>\g<2>',
                    html, count=1
                )
                if html_new != html: html = html_new; changed = True

            if changed:
                p.write_text(html, encoding='utf-8')
                print(f'  OK    {slug:<42} {school_en} / {school_jp_clean}')
                print(f'        {"":42} {dept_en} / {dept_jp}')
                updated += 1
            else:
                print(f'  SAME  {slug} — no change needed')
                skipped += 1

        print()

    print(f'Updated: {updated}  Skipped: {skipped}  Warnings: {warned}')
    print('\nRun scripts_extract_student_data.py to update JSON.')


if __name__ == '__main__':
    main()
