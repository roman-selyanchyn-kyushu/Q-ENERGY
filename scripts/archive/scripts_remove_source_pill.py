#!/usr/bin/env python3
"""
Remove the "Original public page" / "Public profile page" external link pill
from all 2021–2025 student pages. The "Back to [cohort] cohort" pill is kept.
The source URL is already stored in data/students.json so no data is lost.

Run from project root:
    python3 scripts_remove_source_pill.py
"""

import re
from pathlib import Path

BASE    = Path(__file__).parent
COHORTS = ['2021', '2022', '2023', '2024', '2025']

# Matches the external q-pit source-pill <a> tag only
PATTERN = re.compile(
    r'<a class="source-pill" href="https://q-pit[^"]*"[^>]*>.*?</a>',
    re.DOTALL,
)


def process_file(path):
    html = path.read_text(encoding='utf-8')
    new_html, n = PATTERN.subn('', html, count=1)
    if n == 0:
        print(f'  SKIP  {path.parent.name}/{path.name} — no external source pill found')
        return
    path.write_text(new_html, encoding='utf-8')
    print(f'  OK    {path.parent.name}/{path.name}')


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
