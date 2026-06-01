#!/usr/bin/env python3
"""
Remove the "Profile metadata" section from all 2021–2025 student pages.
It is always the last <section> and contains the meta-card debug table.
The 2026 pages never had this section.
No renumbering needed — it is simply the last section.

Run from project root:
    python3 scripts_remove_metadata_section.py
"""

import re
from pathlib import Path

BASE    = Path(__file__).parent
COHORTS = ['2021', '2022', '2023', '2024', '2025']


def remove_metadata_section(html):
    """Remove the <section> block containing 'Profile metadata'."""
    pattern = re.compile(
        r'\n<section>(?P<body>(?:(?!</section>)[\s\S])*?Profile(?:(?!</section>)[\s\S])*?metadata(?:(?!</section>)[\s\S])*?)</section>',
        re.DOTALL,
    )
    new_html, n = pattern.subn('', html, count=1)
    return new_html, n > 0


def process_file(path):
    html = path.read_text(encoding='utf-8')
    original = html

    html, removed = remove_metadata_section(html)
    if not removed:
        print(f'  WARN  {path.parent.name}/{path.name} — metadata section not found')
        return

    # Count remaining sections
    body_start = html.index('<body>')
    nums = re.findall(r'§ 0(\d)', html[body_start:])

    path.write_text(html, encoding='utf-8')
    print(f'  OK    {path.parent.name}/{path.name}  ({len(nums)} sections: {", ".join("§0"+n for n in nums)})')


def main():
    total = 0
    for cohort in COHORTS:
        d = BASE / 'students' / cohort
        pages = sorted(p for p in d.glob('*.html') if p.name != 'index.html')
        print(f'\n── {cohort} ({len(pages)} pages) ──')
        for p in pages:
            process_file(p)
            total += 1
    print(f'\nProcessed {total} files. Done.')


if __name__ == '__main__':
    main()
