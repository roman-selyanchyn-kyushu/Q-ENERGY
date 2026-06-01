#!/usr/bin/env python3
"""
Add prev/next fellow navigation buttons to all student profile pages.
Placed in the topbar, to the right of the programme mark and left of
the language toggle, so you can browse all 71 profiles in sequence.

Wraps around: last fellow → first fellow, first fellow ← last fellow.

Run from project root:
    python3 scripts_add_fellow_nav.py
"""

import re
from pathlib import Path

BASE = Path(__file__).parent

# Full ordered list of primary slugs across all cohorts (no aliases)
ALL_STUDENTS = [
    # 2021
    ('2021', 'daiki-nishimura'),   ('2021', 'haruka-mitoma'),
    ('2021', 'keitaro-maeno'),     ('2021', 'kento-komatsubara'),
    ('2021', 'likhith-manjunatha'),('2021', 'masatoshi-tashima'),
    ('2021', 'mingxu-sun'),        ('2021', 'tianhui-fan'),
    ('2021', 'timothee-redarce'),  ('2021', 'toraharu-watanabe'),
    ('2021', 'xiaofeng-shen'),     ('2021', 'yulu-chen'),
    # 2022
    ('2022', 'daisuke-yoshizawa'), ('2022', 'hyun-gyu-park'),
    ('2022', 'jacqueline-andrea-hidalgo-jim-nez'),
    ('2022', 'muhammad-irfan-maulana-kusdhany'),
    ('2022', 'qingyi-he'),         ('2022', 'ryoma-sato'),
    ('2022', 'shinichi-takeno'),   ('2022', 'sora-matsushima'),
    ('2022', 'tatsuya-hamashima'), ('2022', 'yin-kan-phua'),
    ('2022', 'yixin-chen'),        ('2022', 'zifei-nie'),
    # 2023
    ('2023', 'go-yokuhou'),        ('2023', 'hiroki-isogawa'),
    ('2023', 'kentaro-wada'),      ('2023', 'kotaro-shinozaki'),
    ('2023', 'narmandakh-khongorzul'), ('2023', 'seiya-imada'),
    ('2023', 'taisei-tomaru'),     ('2023', 'xuesong-wei'),
    ('2023', 'yusuke-oga'),        ('2023', 'yuta-takaoka'),
    ('2023', 'yutong-chen'),
    # 2024
    ('2024', 'haomin-fu'),         ('2024', 'itsuki-oyama'),
    ('2024', 'kodai-matsumoto'),   ('2024', 'ryudai-ueno'),
    ('2024', 'shen-siyu'),         ('2024', 'shogo-nakamura'),
    ('2024', 'tomomi-shoda'),      ('2024', 'xianzhe-yang'),
    ('2024', 'yuki-noguchi'),      ('2024', 'yuki-tomita'),
    ('2024', 'zhang-kaili'),
    # 2025
    ('2025', 'kohei-sawada'),      ('2025', 'nozomi-goto'),
    ('2025', 'qi-shi'),            ('2025', 'rika-iriguchi'),
    ('2025', 'ryoshi-oda'),        ('2025', 'takahiro-yamaguchi'),
    ('2025', 'wang-sheng'),        ('2025', 'yan-chenyu'),
    ('2025', 'yuki-nishimura'),    ('2025', 'zhai-xiazhe'),
    ('2025', 'zhang-jingxuan'),    ('2025', 'zhanyi-xiang'),
    # 2026
    ('2026', 'chang-s'),           ('2026', 'chen-h'),
    ('2026', 'jiang-z'),           ('2026', 'kotajima-m'),
    ('2026', 'minoda-k'),          ('2026', 'mochizuki-t'),
    ('2026', 'nakagawa-n'),        ('2026', 'omoto-s'),
    ('2026', 'sun-h'),             ('2026', 'wang-w'),
    ('2026', 'yoshida-s'),         ('2026', 'zheng-q'),
    ('2026', 'zou-z'),
]

NAV_CSS = '''
  /* Fellow navigator */
  .fellow-nav{display:flex;align-items:center;gap:4px;}
  .fnav-btn{display:inline-flex;align-items:center;gap:5px;padding:6px 12px;border:1px solid var(--line);border-radius:999px;font-family:var(--sans);font-size:11px;font-weight:600;letter-spacing:.04em;color:var(--ink-3);text-decoration:none;background:transparent;transition:background .2s,color .2s,border-color .2s;}
  .fnav-btn:hover{background:var(--paper-2);color:var(--accent);border-color:var(--accent);}
  .fnav-btn svg{width:13px;height:13px;flex-shrink:0;}
  .fnav-mobile{display:none;}
  @media(max-width:600px){.fnav-label{display:none;}.fnav-mobile{display:inline;}}
'''

SVG_LEFT  = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 12L6 8l4-4"/></svg>'
SVG_RIGHT = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4l4 4-4 4"/></svg>'

TOTAL = len(ALL_STUDENTS)


def rel_url(from_cohort, to_cohort, to_slug):
    """Relative URL from students/FROM_COHORT/slug.html to the target."""
    if from_cohort == to_cohort:
        return f'{to_slug}.html'
    return f'../{to_cohort}/{to_slug}.html'


def build_nav(from_cohort, idx):
    prev_idx = (idx - 1) % TOTAL
    next_idx = (idx + 1) % TOTAL
    prev_cohort, prev_slug = ALL_STUDENTS[prev_idx]
    next_cohort, next_slug = ALL_STUDENTS[next_idx]

    prev_url = rel_url(from_cohort, prev_cohort, prev_slug)
    next_url = rel_url(from_cohort, next_cohort, next_slug)

    position = f'{idx + 1}&thinsp;/&thinsp;{TOTAL}'
    SVG_GRID = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" '
                'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
                '<rect x="2" y="2" width="5" height="5"/>'
                '<rect x="9" y="2" width="5" height="5"/>'
                '<rect x="2" y="9" width="5" height="5"/>'
                '<rect x="9" y="9" width="5" height="5"/>'
                '</svg>')

    return (
        f'<div class="fellow-nav">'
        f'<a href="{prev_url}" class="fnav-btn" title="Previous fellow">{SVG_LEFT}</a>'
        f'<a href="../../index.html#students" class="fnav-btn" title="All Fellows">'
        f'{SVG_GRID}<span class="fnav-label">&ensp;{position}</span>'
        f'<span class="fnav-mobile">{idx + 1}</span>'
        f'</a>'
        f'<a href="{next_url}" class="fnav-btn" title="Next fellow">{SVG_RIGHT}</a>'
        f'</div>'
    )


def inject_nav(html, nav_html, css):
    # 1. Add CSS before </style>
    if '.fellow-nav' not in html:
        html = html.replace('</style>', css + '</style>', 1)

    # Remove existing nav if re-running
    html = re.sub(r'<div class="fellow-nav">.*?</div>', '', html, count=1, flags=re.DOTALL)

    # 2. Insert nav between program-mark link and lang-toggle div in topbar-inner
    pattern = re.compile(
        r'(<div class="topbar-inner">.*?)(</a>)(\s*)(<div class="lang-toggle")',
        re.DOTALL
    )
    def replacer(m):
        return m.group(1) + m.group(2) + m.group(3) + nav_html + m.group(3) + m.group(4)

    new_html, n = pattern.subn(replacer, html, count=1)
    return new_html, n > 0


def main():
    updated = skipped = 0
    for idx, (cohort, slug) in enumerate(ALL_STUDENTS):
        path = BASE / 'students' / cohort / f'{slug}.html'
        if not path.exists():
            print(f'  MISS  {cohort}/{slug}')
            skipped += 1
            continue

        html = path.read_text(encoding='utf-8')
        nav_html = build_nav(cohort, idx)
        new_html, ok = inject_nav(html, nav_html, NAV_CSS)

        if ok and new_html != html:
            path.write_text(new_html, encoding='utf-8')
            print(f'  OK    {cohort}/{slug}  [{idx+1}/{TOTAL}]')
            updated += 1
        else:
            print(f'  WARN  {cohort}/{slug} — topbar pattern not matched')
            skipped += 1

    print(f'\nUpdated {updated}  Skipped/warned {skipped}')


if __name__ == '__main__':
    main()
