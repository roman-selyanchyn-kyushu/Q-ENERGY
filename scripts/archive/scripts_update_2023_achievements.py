#!/usr/bin/env python3
"""
Add research achievements (papers + conference entries) to 2023 cohort HTML pages.

Data sources:
  Scopus/Isogawa.csv          → hiroki-isogawa
  Scopus/Imada.csv            → seiya-imada
  Scopus/Khongorzul.csv       → narmandakh-khongorzul
  Scopus/Oga.csv              → yusuke-oga
  Scopus/Shinozaki.csv        → kotaro-shinozaki
  Scopus/Takaoka.csv          → yuta-takaoka   (skip Erratum rows)
  Scopus/Tomaru.csv           → taisei-tomaru  (skip Erratum rows)
  Scopus/Wei.csv              → xuesong-wei
  Scopus/Yutong.csv           → yutong-chen
  Scopus/Kubota-Wada.csv      → kentaro-wada   (filter rows with "Wada K." in Authors)

  go-yokuhou: no Scopus data yet — left as "Coming soon"

Special note on Wada Kentaro (kentaro-wada):
  There are two "Wada Kentaro" in Scopus whose profiles were merged.
  Roman provided Kubota (supervisor) profile CSV instead.
  We filter Kubota CSV for rows where "Wada K." appears in the Authors column.

Run from project root:
    python3 scripts_update_2023_achievements.py
"""

import csv
import json
import re
from pathlib import Path

BASE      = Path(__file__).parent
DIR_23    = BASE / "students" / "2023"
SCOPUS    = BASE / "Scopus"
JSON_PATH = BASE / "data" / "students.json"

# ── Helpers ───────────────────────────────────────────────────────────────────

CHEM_SUBS = [
    # Order matters: longer patterns first to avoid partial replacement
    (r'\bCO2\b',  'CO<sub>2</sub>'),
    (r'\bH2O2\b', 'H<sub>2</sub>O<sub>2</sub>'),
    (r'\bH2O\b',  'H<sub>2</sub>O'),
    (r'\bCH4\b',  'CH<sub>4</sub>'),
    (r'\bC2H4\b', 'C<sub>2</sub>H<sub>4</sub>'),
    (r'\bNH3\b',  'NH<sub>3</sub>'),
    (r'\bH2S\b',  'H<sub>2</sub>S'),
    (r'\bSO2\b',  'SO<sub>2</sub>'),
    (r'\bNO2\b',  'NO<sub>2</sub>'),
    (r'\bN2O\b',  'N<sub>2</sub>O'),
    (r'\bO2\b',   'O<sub>2</sub>'),
    (r'\bN2\b',   'N<sub>2</sub>'),
    (r'\bH2\b',   'H<sub>2</sub>'),
    (r'\bLiAlO2\b', 'LiAlO<sub>2</sub>'),
    # Unicode subscripts in titles (Scopus sometimes uses these)
    ('₂', '<sub>2</sub>'),
    ('₃', '<sub>3</sub>'),
    ('₄', '<sub>4</sub>'),
    # Selective patterns within words (electrochemical formulas)
    (r'CO2reduction', 'CO<sub>2</sub> reduction'),
    (r'CO2electrolysis', 'CO<sub>2</sub> electrolysis'),
    (r'CO2Reduction', 'CO<sub>2</sub> Reduction'),
    (r'CO2Electrolysis', 'CO<sub>2</sub> Electrolysis'),
    (r'CO/H2', 'CO/H<sub>2</sub>'),
]


def apply_chem_subs(text):
    for pattern, repl in CHEM_SUBS:
        text = re.sub(pattern, repl, text)
    return text


def esc(text):
    """HTML-escape plain text (minimal — just & and quotes in title)."""
    return text.replace('&', '&amp;').replace('"', '&quot;')


def fmt_pages(vol, issue, p_start, p_end, art_no):
    """Build Vol./pages/art citation fragment."""
    parts = []
    if vol:
        if issue:
            parts.append(f'Vol. {vol}({issue})')
        else:
            parts.append(f'Vol. {vol}')
    if p_start and p_end:
        parts.append(f'pp. {p_start}–{p_end}')
    elif p_start:
        parts.append(f'p. {p_start}')
    elif art_no:
        parts.append(art_no)
    return ', '.join(parts)


def highlight(authors_str, abbrevs):
    """
    Wrap the first matching abbreviated name in <span class="ach-authors">.
    abbrevs: list of strings like ['Isogawa H.', 'Isogawa H']
    """
    for abbrev in abbrevs:
        # Match at word boundary
        escaped = re.escape(abbrev)
        if re.search(escaped, authors_str):
            return authors_str.replace(abbrev, f'<span class="ach-authors">{abbrev}</span>', 1)
    return authors_str


def read_scopus(fname):
    path = SCOPUS / fname
    if not path.exists():
        print(f"  WARN  {fname} not found — skipping")
        return []
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def fmt_paper_li(row, abbrevs, is_conference=False):
    """Format a single Scopus row as an <li> HTML string."""
    authors = highlight(row.get('Authors', '').strip(), abbrevs)
    title   = apply_chem_subs(row.get('Title', '').strip())
    journal = row.get('Source title', '').strip()
    year    = row.get('Year', '').strip()
    vol     = row.get('Volume', '').strip()
    issue   = row.get('Issue', '').strip()
    p1      = row.get('Page start', '').strip()
    p2      = row.get('Page end', '').strip()
    art     = row.get('Art. No.', '').strip()
    doi     = row.get('DOI', '').strip()

    pages_frag = fmt_pages(vol, issue, p1, p2, art)
    doi_link   = (f' <a href="https://doi.org/{doi}" target="_blank" rel="noopener">'
                  f'doi:{doi}</a>') if doi else ''

    year_part  = f' ({year})' if year else ''
    pages_part = f', {pages_frag}' if pages_frag else ''

    return (f'<li>{authors} &ldquo;{title}&rdquo; '
            f'<em>{journal}</em>{pages_part}{year_part}{doi_link}</li>')


def build_li_list(rows, abbrevs):
    """Split rows into (journal_lis, conference_lis)."""
    journal_lis = []
    conf_lis    = []
    for r in rows:
        doc_type = r.get('Document Type', '').strip().lower()
        if doc_type in ('erratum', 'retraction', 'note', 'editorial', 'letter',
                        'short survey', 'book chapter'):
            continue   # skip non-primary entries
        li = fmt_paper_li(r, abbrevs)
        if doc_type in ('conference paper', 'conference review'):
            conf_lis.append(li)
        else:
            journal_lis.append(li)
    return journal_lis, conf_lis


COMING_SOON_OL = (
    '<ol class="ach-list"><li><span class="ach-soon">'
    '<span data-lang-en="">Coming soon</span>'
    '<span data-lang-jp="">準備中</span>'
    '</span></li></ol>'
)


def build_ol(li_items):
    if not li_items:
        return COMING_SOON_OL
    inner = '\n        '.join(li_items)
    return f'<ol class="ach-list">\n        {inner}\n      </ol>'


def patch_html(html, papers_ol, conf_ol):
    """Replace the three ach-list <ol> blocks in the achievements section."""
    # There are exactly 3 ach-list groups: Papers, Conferences, Other
    # Replace the first two; leave Other/Awards as Coming Soon
    count = [0]

    def replacer(m):
        count[0] += 1
        if count[0] == 1:
            return papers_ol
        elif count[0] == 2:
            return conf_ol
        else:
            return m.group(0)  # keep Other as-is

    pattern = re.compile(re.escape(COMING_SOON_OL))
    result = pattern.sub(replacer, html)
    return result, count[0]


def update_json(students_data, slug, journals, conferences):
    """Patch achievements for a student in the loaded JSON data."""
    for s in students_data:
        if s.get('slug') == slug:
            def row_to_dict(r):
                doi = r.get('DOI', '').strip()
                return {
                    'text': (r.get('Authors', '').strip() + ' "'
                             + r.get('Title', '').strip() + '" '
                             + r.get('Source title', '').strip()
                             + (' (' + r.get('Year', '') + ')' if r.get('Year') else '')),
                    'doi': ('https://doi.org/' + doi) if doi else '',
                }
            s.setdefault('achievements', {'papers': [], 'conferences': [], 'awards': [], 'other': []})
            s['achievements']['papers']      = [row_to_dict(r) for r in journals]
            s['achievements']['conferences'] = [row_to_dict(r) for r in conferences]
            return True
    return False


def process_student(slug, csv_file, abbrevs, filter_fn=None):
    """
    Load CSV, optionally filter rows, then patch the HTML page and JSON data.
    Returns (journals, conferences) lists of raw rows.
    """
    rows = read_scopus(csv_file)
    if filter_fn:
        rows = [r for r in rows if filter_fn(r)]

    journals, conferences = [], []
    for r in rows:
        doc_type = r.get('Document Type', '').strip().lower()
        if doc_type in ('erratum', 'retraction', 'note', 'editorial', 'letter',
                        'short survey', 'book chapter'):
            continue
        if doc_type in ('conference paper', 'conference review'):
            conferences.append(r)
        else:
            journals.append(r)

    page = DIR_23 / f'{slug}.html'
    if not page.exists():
        print(f'  SKIP  {slug}.html — file not found')
        return [], []

    html     = page.read_text(encoding='utf-8')
    original = html

    papers_ol = build_ol([fmt_paper_li(r, abbrevs) for r in journals])
    conf_ol   = build_ol([fmt_paper_li(r, abbrevs) for r in conferences])

    new_html, subs = patch_html(html, papers_ol, conf_ol)
    if new_html == original:
        print(f'  WARN  {slug}.html — no changes (placeholder not found?)')
    else:
        page.write_text(new_html, encoding='utf-8')
        print(f'  OK    {slug}.html — {len(journals)} journal, {len(conferences)} conf  ({subs} sections replaced)')

    return journals, conferences


# ── Student definitions ────────────────────────────────────────────────────────

STUDENTS = [
    # (slug, csv_file, abbrevs_list, filter_fn_or_None)
    ('hiroki-isogawa',       'Isogawa.csv',     ['Isogawa H.'],             None),
    ('seiya-imada',          'Imada.csv',        ['Imada S.'],               None),
    ('narmandakh-khongorzul','Khongorzul.csv',   ['Narmandakh K.'],          None),
    ('yusuke-oga',           'Oga.csv',          ['Oga Y.'],                 None),
    ('kotaro-shinozaki',     'Shinozaki.csv',    ['Shinozaki K.'],           None),
    ('yuta-takaoka',         'Takaoka.csv',      ['Takaoka Y.'],             None),
    ('taisei-tomaru',        'Tomaru.csv',       ['Tomaru T.'],              None),
    ('xuesong-wei',          'Wei.csv',          ['Wei X.'],                 None),
    ('yutong-chen',          'Yutong.csv',       ['Chen Y.'],                None),
    # Wada: use Kubota's profile, filter for Wada K. only
    ('kentaro-wada',         'Kubota-Wada.csv',  ['Wada K.'],
     lambda r: 'Wada K.' in r.get('Authors', '') or 'Wada, Kentaro' in r.get('Author full names', '')),
]


def main():
    print(f'Updating 2023 achievements in {DIR_23}\n')

    # Load JSON
    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)
    students_data = data['students']

    results = {}
    for entry in STUDENTS:
        slug, csv_file, abbrevs, filter_fn = entry
        j, c = process_student(slug, csv_file, abbrevs, filter_fn)
        results[slug] = (j, c)
        update_json(students_data, slug, j, c)

    # Write JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('\n  JSON updated.')

    # Summary
    total_j = sum(len(j) for j, _ in results.values())
    total_c = sum(len(c) for _, c in results.values())
    print(f'\nSummary: {total_j} journal papers + {total_c} conference entries across 2023 cohort')
    print('(go-yokuhou has no Scopus data — left as Coming soon)\n')


if __name__ == '__main__':
    main()
