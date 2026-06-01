#!/usr/bin/env python3
"""
Update achievements sections in all 2024 student pages from Excel report data.

Sources: /Users/romanselyanchyn/Library/CloudStorage/Dropbox/Roman sensei/Report for 2024/*.xlsx

Sections updated:
  - Research Papers      ← academic papers + peer-reviewed proceedings
  - Conference Presentations ← conference oral/poster presentations
  - Awards               ← awards (replaces "Other Achievements" label if awards exist)

Run from project root:
    python3 scripts_update_2024_achievements.py
"""

import re, json, openpyxl
from pathlib import Path
from datetime import datetime

BASE   = Path(__file__).parent
FOLDER = Path('/Users/romanselyanchyn/Library/CloudStorage/Dropbox/Roman sensei/Report for 2024')

FILE_TO_SLUG = {
    '3BE24107R_上野竜大生_研究業績報告書.xlsx':              'ryudai-ueno',
    '3EC24105E_SHEN Siyu_研究業績報告書.xlsx':               'shen-siyu',
    '3EC24106K_庄田朋申_研究業績報告書.xlsx':                'tomomi-shoda',
    '3ES24015R_小山一輝_研究業績報告書.xlsx':                'itsuki-oyama',
    '3ES24022G_野口湧喜_研究業績報告書.xlsx':                'yuki-noguchi',
    '3FS24103K_FU HAOMIN_Research Achievements Report.xlsx': 'haomin-fu',
    '3HE23006S_ZHANG KAILI_research_achievement_report.xlsx':'zhang-kaili',
    '3HE24602T_楊賢テツ_研究業績報告書.xlsx':                'xianzhe-yang',
    '3SC24106E_冨田侑樹_研究業績報告書.xlsx':                'yuki-tomita',
    '3TE24123G_松本昂大_研究業績報告書.xlsx':                'kodai-matsumoto',
    '3TE24471M_中村省吾_研究業績報告書.xlsx':                'shogo-nakamura',
}

# ── Excel parsing ─────────────────────────────────────────────────────────────

def fmt_date(v):
    if isinstance(v, datetime): return v.strftime('%Y/%m/%d')
    return str(v).strip() if v else ''

def clean(v):
    s = str(v).strip() if v is not None else ''
    return s

def is_example(authors):
    """Skip template / example rows."""
    skip = ('n/a', 'e.g.', 'kyudai', 'motooka', '九大', '元岡')
    return not authors or any(s in authors.lower() for s in skip)

def parse_excel(path):
    wb   = openpyxl.load_workbook(path, data_only=True)
    ws   = wb.active
    rows = [r for r in ws.iter_rows(values_only=True) if any(c is not None for c in r)]

    data = {'papers': [], 'proceedings': [], 'conferences': [], 'awards': []}
    mode = None

    for row in rows:
        c0 = row[0]; c1 = row[1]
        c2 = row[2] if len(row) > 2 else None

        if c0 == 1 and c1 and '学術論文' in str(c1):
            mode = 'papers'; continue
        if c1 == '（2）' and c2 and '国際会議' in str(c2):
            mode = 'proceedings'; continue
        if c0 == 2: mode = 'conferences'; continue
        if c0 == 3: mode = 'awards'; continue
        if c0 == 4: mode = None; continue   # Others section — skip

        if not isinstance(c1, int) or c1 < 1: continue
        authors = clean(c2)
        if is_example(authors): continue
        title = clean(row[3]) if len(row) > 3 else ''
        if not title: continue

        if mode == 'papers':
            data['papers'].append({
                'authors': authors,
                'title':   title,
                'journal': clean(row[4]) if len(row) > 4 else '',
                'status':  clean(row[5]) if len(row) > 5 else '',
                'date':    fmt_date(row[6]) if len(row) > 6 else '',
                'doi':     clean(row[9]) if len(row) > 9 else '',
                'if':      clean(row[10]) if len(row) > 10 else '',
            })
        elif mode == 'proceedings':
            data['proceedings'].append({
                'authors':    authors,
                'title':      title,
                'conference': clean(row[4]) if len(row) > 4 else '',
                'country':    clean(row[6]) if len(row) > 6 else '',
                'date':       fmt_date(row[8]) if len(row) > 8 else '',
            })
        elif mode == 'conferences':
            data['conferences'].append({
                'authors':    authors,
                'title':      title,
                'conference': clean(row[4]) if len(row) > 4 else '',
                'venue':      clean(row[6]) if len(row) > 6 else '',
                'date':       fmt_date(row[8]) if len(row) > 8 else '',
                'type':       clean(row[9]) if len(row) > 9 else '',
                'format':     clean(row[10]) if len(row) > 10 else '',
            })
        elif mode == 'awards':
            data['awards'].append({
                'awardees': authors,
                'title':    title,
                'award':    clean(row[4]) if len(row) > 4 else '',
                'org':      clean(row[5]) if len(row) > 5 else '',
                'date':     fmt_date(row[6]) if len(row) > 6 else '',
            })

    return data


# ── HTML formatting ───────────────────────────────────────────────────────────

def esc(s):
    """HTML-escape plain text."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def doi_link(doi):
    if not doi: return ''
    url = doi if doi.startswith('http') else f'https://doi.org/{doi}'
    short = doi.replace('https://doi.org/', '').replace('http://doi.org/', '')
    return f' <a href="{url}" target="_blank" rel="noopener">doi:{esc(short)}</a>'

def fmt_paper_li(p):
    parts = [esc(p['authors']) + '.']
    parts.append(f' &ldquo;{esc(p["title"])}&rdquo;')
    if p['journal']:
        parts.append(f' <em>{esc(p["journal"])}</em>')
    if p['date']:
        year = p['date'][:4]
        parts.append(f' ({year})')
    if p['status'] and p['status'] not in ('published',):
        parts.append(f' [{esc(p["status"])}]')
    parts.append(doi_link(p['doi']))
    return ''.join(parts)

def fmt_proc_li(p):
    parts = [esc(p['authors']) + '.']
    parts.append(f' &ldquo;{esc(p["title"])}&rdquo;')
    if p['conference']:
        parts.append(f' <em>{esc(p["conference"])}</em>')
    if p['country']:
        parts.append(f', {esc(p["country"])}')
    if p['date']:
        parts.append(f' ({p["date"][:7]})')
    parts.append(' [proceedings]')
    return ''.join(parts)

def fmt_conf_li(c):
    parts = [esc(c['authors']) + '.']
    parts.append(f' &ldquo;{esc(c["title"])}&rdquo;')
    if c['conference']:
        parts.append(f' <em>{esc(c["conference"])}</em>')
    if c['venue']:
        parts.append(f', {esc(c["venue"])}')
    if c['date']:
        parts.append(f' ({c["date"][:7]})')
    flags = []
    if 'International' in c.get('type','') or '国際' in c.get('type',''):
        flags.append('international')
    if 'Oral' in c.get('format','') or '口頭' in c.get('format',''):
        flags.append('oral')
    elif 'Poster' in c.get('format','') or 'ポスター' in c.get('format',''):
        flags.append('poster')
    if flags:
        parts.append(f' [{", ".join(flags)}]')
    return ''.join(parts)

def fmt_award_li(a):
    parts = []
    if a['award']:
        parts.append(f'<em>{esc(a["award"])}</em>')
    if a['org']:
        parts.append(esc(a['org']))
    if a['date']:
        parts.append(f'({a["date"][:7]})')
    parts.append(f'&mdash; &ldquo;{esc(a["title"])}&rdquo;')
    return ' '.join(parts)

def soon_li():
    return '<li><span class="ach-soon"><span data-lang-en="">Coming soon</span><span data-lang-jp="">準備中</span></span></li>'

def build_ach_card(data):
    """Build the full <div class="ach-card"> replacement."""
    all_papers = data['papers'] + data['proceedings']
    all_confs  = data['conferences']
    all_awards = data['awards']

    def make_group(label_en, label_jp, items_html):
        li_block = '\n        '.join(f'<li>{li}</li>' for li in items_html) if items_html else soon_li()
        return (
            f'  <div class="ach-group">\n'
            f'    <div class="ach-label"><span data-lang-en="">{label_en}</span>'
            f'<span data-lang-jp="">{label_jp}</span></div>\n'
            f'    <ol class="ach-list">{li_block}</ol>\n'
            f'  </div>'
        )

    paper_lis = [fmt_paper_li(p) for p in data['papers']] + \
                [fmt_proc_li(p) for p in data['proceedings']]
    conf_lis  = [fmt_conf_li(c) for c in all_confs]
    award_lis = [fmt_award_li(a) for a in all_awards]

    groups = [
        make_group('Research Papers', '論文', paper_lis),
        make_group('Conference Presentations', '学会発表', conf_lis),
        make_group('Awards', '受賞', award_lis),
    ]
    return '<div class="ach-card">\n' + '\n'.join(groups) + '\n</div>'


# ── HTML update ───────────────────────────────────────────────────────────────

ACH_CARD_RE = re.compile(
    r'<div class="ach-card">.*?</div>\s*\n?\s*</div>\s*\n?\s*</section>',
    re.DOTALL
)
# Simpler: just replace the ach-card div
ACH_CARD_RE2 = re.compile(r'<div class="ach-card">.*?(?=\n</section>|\n\n)', re.DOTALL)


def update_page(slug, data):
    path = BASE / 'students' / '2024' / f'{slug}.html'
    if not path.exists():
        print(f'  ERROR  {slug} — file not found'); return

    html = path.read_text(encoding='utf-8')

    # Find the ach-card block
    m = re.search(r'<div class="ach-card">.*?</div>\s*\n\s*</section>', html, re.DOTALL)
    if not m:
        print(f'  WARN   {slug} — ach-card not found'); return

    new_card = build_ach_card(data)
    new_html = html[:m.start()] + new_card + '\n</section>' + html[m.end():]
    path.write_text(new_html, encoding='utf-8')

    n_papers = len(data['papers']) + len(data['proceedings'])
    n_confs  = len(data['conferences'])
    n_awards = len(data['awards'])
    print(f'  OK     {slug}  papers={n_papers} confs={n_confs} awards={n_awards}')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('Parsing Excel files and updating 2024 student pages...\n')
    for fname, slug in sorted(FILE_TO_SLUG.items(), key=lambda x: x[1]):
        fpath = FOLDER / fname
        if not fpath.exists():
            print(f'  MISS   {fname}'); continue
        data = parse_excel(fpath)
        update_page(slug, data)

    print('\nDone. Re-run scripts_extract_student_data.py to update students.json.')


if __name__ == '__main__':
    main()
