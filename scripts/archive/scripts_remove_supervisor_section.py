#!/usr/bin/env python3
"""
Remove the dedicated "Supervisor information" section from all 2021–2025 student pages.
Supervisor info already lives in the top hero-subline; the extra section is redundant.

After removal, remaining section numbers are renumbered sequentially (§01, §02, …)
so there are no gaps.

Run from project root:
    python3 scripts_remove_supervisor_section.py
"""

import re
from pathlib import Path

BASE = Path(__file__).parent

COHORTS = ['2021', '2022', '2023', '2024', '2025']


def remove_supervisor_section(html):
    """
    Remove the <section> block that contains 'Supervisor information'.
    Returns (new_html, removed_flag).
    """
    # Each section starts with '<section>' and ends with '</section>'.
    # We split on section boundaries and reassemble without the supervisor section.
    # The sections in body look like:  \n<section>\n...\n</section>\n
    #
    # Strategy: find the span [start_of_<section>, end_of_</section>] that
    # contains the text "Supervisor" and remove it.

    pattern = re.compile(
        r'\n<section>(?P<body>(?:(?!</section>)[\s\S])*?Supervisor(?:(?!</section>)[\s\S])*?)</section>',
        re.DOTALL,
    )
    new_html, n = pattern.subn('', html, count=1)
    return new_html, n > 0


def renumber_sections(html):
    """
    After removal, renumber all section-num spans sequentially starting at §01.
    Replaces § 0X markers in order of appearance in the body.
    """
    body_start = html.index('<body>')

    # Collect all positions and old numbers
    positions = []
    for m in re.finditer(r'<div class="section-num"><span>§ 0(\d)</span></div>', html):
        if m.start() >= body_start:
            positions.append(m)

    if not positions:
        return html

    # Build new html character by character, replacing each marker
    result = []
    prev_end = 0
    for i, m in enumerate(positions, start=1):
        result.append(html[prev_end:m.start()])
        result.append(f'<div class="section-num"><span>§ 0{i}</span></div>')
        prev_end = m.end()
    result.append(html[prev_end:])
    return ''.join(result)


def process_file(path):
    html = path.read_text(encoding='utf-8')
    original = html

    html, removed = remove_supervisor_section(html)
    if not removed:
        print(f'  WARN  {path.parent.name}/{path.name} — supervisor section not found')
        return

    html = renumber_sections(html)

    # Count remaining sections
    body_start = html.index('<body>')
    nums = re.findall(r'§ 0(\d)', html[body_start:])

    path.write_text(html, encoding='utf-8')
    print(f'  OK    {path.parent.name}/{path.name}  ({len(nums)} sections remaining: {", ".join("§0"+n for n in nums)})')


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
