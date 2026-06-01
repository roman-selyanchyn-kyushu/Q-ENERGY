#!/usr/bin/env python3
"""
Repair the section numbers in 2021 pages that were all collapsed to §01
by the cascading-replacement bug.

After the previous script removed the K2-SPRING §01 section and
mis-renumbered, all four remaining sections read §01.
They should read §01, §02, §03, §04 in order of appearance.

Run from project root:
    python3 scripts_fix_section_numbers_2021.py
"""

import re
from pathlib import Path

DIR_21 = Path(__file__).parent / 'students' / '2021'

# Counter is per-file; each occurrence of section-num in the <body> gets
# the next sequential number.
MARKER = '<div class="section-num"><span>§ 01</span></div>'


def fix_file(path):
    html = path.read_text(encoding='utf-8')
    original = html

    # Count how many real section markers exist in the body
    # (CSS lines contain different text, so we count exactly)
    count = html.count(MARKER)
    if count == 0:
        print(f'  SKIP  {path.name} — no §01 markers found')
        return
    if count == 1:
        print(f'  SKIP  {path.name} — only one §01 marker, already correct')
        return

    # Replace occurrences 2, 3, 4 … with §02, §03, §04 …
    # We leave the first occurrence as §01.
    section_num = [1]  # mutable counter

    def replacer(m):
        section_num[0] += 1
        return f'<div class="section-num"><span>§ 0{section_num[0]}</span></div>'

    # Replace all but the first occurrence
    new_html = html
    first_pos = new_html.find(MARKER)
    # Build result: keep everything up to and including first match unchanged,
    # then replace subsequent matches.
    prefix = new_html[:first_pos + len(MARKER)]
    suffix = new_html[first_pos + len(MARKER):]

    suffix = re.sub(
        r'<div class="section-num"><span>§ 01</span></div>',
        replacer,
        suffix
    )
    new_html = prefix + suffix

    if new_html == original:
        print(f'  WARN  {path.name} — no changes made')
    else:
        path.write_text(new_html, encoding='utf-8')
        # Count final section numbers
        nums = re.findall(r'§ 0\d', new_html[new_html.index('<body>'):])
        print(f'  OK    {path.name}  ({len(nums)} sections: {", ".join(nums)})')


def main():
    pages = sorted(p for p in DIR_21.glob('*.html') if p.name != 'index.html')
    print(f'Repairing {len(pages)} 2021 pages in {DIR_21}\n')
    for p in pages:
        fix_file(p)
    print('\nDone.')


if __name__ == '__main__':
    main()
