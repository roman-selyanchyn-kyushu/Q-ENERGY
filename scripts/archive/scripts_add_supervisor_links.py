#!/usr/bin/env python3
"""
Add clickable links to supervisor names in the hero-subline of 2021–2025 pages.

The link format matches the 2026 pages:
  <dd>
    <a href="https://q-pit.kyushu-u.ac.jp/teacher/[slug]/" ... data-lang-en="">NAME</a>
    <a href="https://q-pit.kyushu-u.ac.jp/teacher/[slug]/" ... data-lang-jp="">NAME</a>
  </dd>

Only updates the hero-subline dt/dd block (not the meta-card).

Run from project root:
    python3 scripts_add_supervisor_links.py
"""

import re
from pathlib import Path
from urllib.parse import quote

BASE    = Path(__file__).parent
COHORTS = ['2021', '2022', '2023', '2024', '2025']
BASE_URL = 'https://q-pit.kyushu-u.ac.jp/teacher/'


def teacher_url(name):
    """Return the Q-PIT teacher page URL for a supervisor name."""
    # Special cases for non-CJK names (confirmed URLs)
    special = {
        'Andrew Chapman':       'chapman',
        'Edalati Kaveh':        'edalati-kaveh',
        'Farzaneh Hooman':      'hooman',
        'Prasanna Divigalpitiya': 'divigalpitiya',
    }
    if name in special:
        return BASE_URL + special[name] + '/'

    # Default: replace space with hyphen, URL-encode the slug
    slug = name.replace(' ', '-')
    return BASE_URL + quote(slug, safe='') + '/'


def add_supervisor_link(html, sup_name):
    """
    Replace the hero-subline supervisor <dd>NAME</dd> with a linked version.
    The meta-card Supervisor dd is left as-is.
    """
    url = teacher_url(sup_name)
    escaped_name = re.escape(sup_name)

    # Pattern: the supervisor dl in the hero-subline (has data-lang-en on dt)
    pattern = (
        r'(<dl><dt data-lang-en="">Supervisor</dt>'
        r'<dt data-lang-jp="">指導教員</dt><dd>)'
        + escaped_name +
        r'(</dd></dl>)'
    )
    replacement = (
        r'\g<1>'
        f'<a href="{url}" target="_blank" rel="noopener" data-lang-en="">{sup_name}</a>'
        f'<a href="{url}" target="_blank" rel="noopener" data-lang-jp="">{sup_name}</a>'
        r'\g<2>'
    )
    new_html, n = re.subn(pattern, replacement, html, count=1)
    return new_html, n > 0


def process_file(path):
    html = path.read_text(encoding='utf-8')
    original = html

    # Extract current supervisor name from hero-subline
    m = re.search(
        r'<dl><dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>(.*?)</dd></dl>',
        html
    )
    if not m:
        print(f'  SKIP  {path.parent.name}/{path.name} — no supervisor dl found')
        return

    sup_name = m.group(1).strip()

    # Skip if already a link, placeholder, or empty
    if '<a ' in sup_name or not sup_name or 'To be added' in sup_name:
        print(f'  SKIP  {path.parent.name}/{path.name} — already linked or no data')
        return

    html, changed = add_supervisor_link(html, sup_name)
    if not changed:
        print(f'  WARN  {path.parent.name}/{path.name} — replacement failed for "{sup_name}"')
        return

    path.write_text(html, encoding='utf-8')
    url = teacher_url(sup_name)
    print(f'  OK    {path.parent.name}/{path.name}  → {sup_name}')


def main():
    total = 0
    for cohort in COHORTS:
        d = BASE / 'students' / cohort
        pages = sorted(p for p in d.glob('*.html') if p.name != 'index.html')
        print(f'\n── {cohort} ──')
        for p in pages:
            process_file(p)
            total += 1
    print(f'\nProcessed {total} files. Done.')


if __name__ == '__main__':
    main()
