#!/usr/bin/env python3
"""
Fix branding and section labels for 2021–2023 cohort pages.

These cohorts were part of the Q-ENERGY Fellowship programme, NOT K2-SPRING.
K2-SPRING only started from 2024 onwards.

Changes applied:
  2021 (12 pages):
    1. Remove the entire K2-SPRING §01 section
    2. Renumber remaining sections §02→§01, §03→§02, §04→§03, §05→§04
    3. Fix hero eyebrow label → Q-ENERGY Fellowship
    4. Fix source URLs: fellow-ship-en/fellow-2021-en/ → fellow-2021-en/

  2022 (11 pages):
    1. Fix hero eyebrow label → Q-ENERGY Fellowship
    2. Fix source URLs: fellow-ship-en/fellow-2022-en/ → fellow-2022-en/

  2023 (11 pages):
    1. Fix hero eyebrow label → Q-ENERGY Fellowship
    2. Fix source URLs: fellow-ship-en/fellow-2023-en/ → fellow-2023-en/

Run from project root:
    python3 scripts_fix_qenergy_fellowship_labels.py
"""

import re
from pathlib import Path

BASE = Path(__file__).parent

# ── The K2-SPRING §01 block present in every generated 2021 page ─────────────
K2_SECTION_2021 = (
    '<section>\n'
    '\n'
    '  <div class="section-head">\n'
    '    <div class="section-num"><span>§ 01</span></div>\n'
    '    <div>\n'
    '      <h2 class="section-title" data-lang-en="">K2-SPRING <span class="em">research topic</span></h2>\n'
    '      <h2 class="section-title" data-lang-jp="">K2-SPRING <span class="em">研究テーマ</span></h2>\n'
    '    </div>\n'
    '  </div>\n'
    '  <article class="research-primary reveal">\n'
    '    <div class="research-banner">\n'
    '      <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">'
    '<path d="M6 0l1.5 4.5L12 6 7.5 7.5 6 12 4.5 7.5 0 6l4.5-1.5z"/></svg>\n'
    '      <span data-lang-en="">K2-SPRING topic &middot; Pending details</span>\n'
    '      <span data-lang-jp="">K2-SPRINGテーマ &middot; 追記予定</span>\n'
    '    </div>\n'
    '    <h3 class="research-title" data-lang-en="">To be added</h3>\n'
    '    <h3 class="research-title" data-lang-jp="">追記予定</h3>\n'
    '    <div class="research-abstract" data-lang-en="">'
    '<p class="ach-soon">K2-SPRING topic information is not available in the current public data. '
    'It will be added after Roman provides it.</p></div>\n'
    '    <div class="research-abstract" data-lang-jp="">'
    '<p class="ach-soon">K2-SPRING研究テーマは現在の公開データには含まれていません。情報提供後に追記します。</p></div>\n'
    '  </article>\n'
    '</section>\n'
)


def fix_eyebrow(html, year):
    """Replace K2-SPRING eyebrow with Q-ENERGY Fellowship label."""
    old = (
        f'<span data-lang-en="">K2-SPRING &middot; Q-ENERGY Innovator Unit &middot; Cohort {year}</span>'
        f'<span data-lang-jp="">K2-SPRING &middot; グリーンイノベーションユニット &middot; {year}年度</span>'
    )
    new = (
        f'<span data-lang-en="">Q-ENERGY Fellowship &middot; Cohort {year}</span>'
        f'<span data-lang-jp="">Q-ENERGYフェローシップ &middot; {year}年度</span>'
    )
    return html.replace(old, new)


def fix_source_urls(html, year):
    """Remove the redundant fellow-ship-en/ prefix from source URLs."""
    old_prefix = f'https://q-pit.kyushu-u.ac.jp/fellow-ship-en/fellow-{year}-en/'
    new_prefix = f'https://q-pit.kyushu-u.ac.jp/fellow-{year}-en/'
    return html.replace(old_prefix, new_prefix)


def renumber_sections(html):
    """
    Replace §02→§01, §03→§02, §04→§03, §05→§04.
    Uses a two-pass temp-marker approach to avoid cascading replacements.
    """
    # Pass 1: replace each with a unique temp token
    html = html.replace('<span>§ 05</span>', '<span>§T05</span>')
    html = html.replace('<span>§ 04</span>', '<span>§T04</span>')
    html = html.replace('<span>§ 03</span>', '<span>§T03</span>')
    html = html.replace('<span>§ 02</span>', '<span>§T02</span>')
    # Pass 2: resolve tokens to final values
    html = html.replace('<span>§T05</span>', '<span>§ 04</span>')
    html = html.replace('<span>§T04</span>', '<span>§ 03</span>')
    html = html.replace('<span>§T03</span>', '<span>§ 02</span>')
    html = html.replace('<span>§T02</span>', '<span>§ 01</span>')
    return html


def fix_2021_page(path):
    html = path.read_text(encoding='utf-8')
    original = html

    # 1. Remove K2-SPRING section
    html = html.replace(K2_SECTION_2021, '', 1)

    # 2. Renumber remaining sections
    if html != original:  # only if section was actually found and removed
        html = renumber_sections(html)

    # 3. Fix eyebrow
    html = fix_eyebrow(html, 2021)

    # 4. Fix source URLs
    html = fix_source_urls(html, 2021)

    if html == original:
        print(f'  WARN  {path.name} — no changes made')
    else:
        path.write_text(html, encoding='utf-8')
        print(f'  OK    {path.name}')


def fix_22_23_page(path, year):
    html = path.read_text(encoding='utf-8')
    original = html

    # Fix eyebrow
    html = fix_eyebrow(html, year)

    # Fix source URLs
    html = fix_source_urls(html, year)

    if html == original:
        print(f'  WARN  {path.name} — no changes made')
    else:
        path.write_text(html, encoding='utf-8')
        print(f'  OK    {path.name}')


def main():
    # ── 2021 ──────────────────────────────────────────────────────────────────
    dir_21 = BASE / 'students' / '2021'
    pages_21 = sorted(p for p in dir_21.glob('*.html') if p.name != 'index.html')
    print(f'=== 2021 ({len(pages_21)} pages) ===')
    for p in pages_21:
        fix_2021_page(p)

    # ── 2022 ──────────────────────────────────────────────────────────────────
    dir_22 = BASE / 'students' / '2022'
    pages_22 = sorted(p for p in dir_22.glob('*.html') if p.name != 'index.html')
    print(f'\n=== 2022 ({len(pages_22)} pages) ===')
    for p in pages_22:
        fix_22_23_page(p, 2022)

    # ── 2023 ──────────────────────────────────────────────────────────────────
    dir_23 = BASE / 'students' / '2023'
    pages_23 = sorted(p for p in dir_23.glob('*.html') if p.name != 'index.html')
    print(f'\n=== 2023 ({len(pages_23)} pages) ===')
    for p in pages_23:
        fix_22_23_page(p, 2023)

    print('\nDone.')


if __name__ == '__main__':
    main()
