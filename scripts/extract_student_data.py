#!/usr/bin/env python3
"""
Extract all student data from local HTML pages into data/students.json.

Covers cohorts 2021–2026.  Only primary slugs (linked from cohort index pages)
are processed — alias files are skipped automatically.

Output: data/students.json

Run from project root:
    python3 scripts/extract_student_data.py
"""

import json, re, html as html_lib
from pathlib import Path
from datetime import date

BASE   = Path(__file__).parent.parent
OUT    = BASE / 'data' / 'students.json'

# ── Primary slug lists (from cohort index.html links) ────────────────────────
PRIMARY = {
    '2021': [
        'daiki-nishimura','haruka-mitoma','keitaro-maeno','kento-komatsubara',
        'likhith-manjunatha','masatoshi-tashima','mingxu-sun','tianhui-fan',
        'timothee-redarce','toraharu-watanabe','xiaofeng-shen','yulu-chen',
    ],
    '2022': [
        'daisuke-yoshizawa','hyun-gyu-park','jacqueline-andrea-hidalgo-jim-nez',
        'muhammad-irfan-maulana-kusdhany','qingyi-he','ryoma-sato','shinichi-takeno',
        'sora-matsushima','tatsuya-hamashima','yin-kan-phua','yixin-chen','zifei-nie',
    ],
    '2023': [
        'go-yokuhou','hiroki-isogawa','kentaro-wada','kotaro-shinozaki',
        'narmandakh-khongorzul','seiya-imada','taisei-tomaru','xuesong-wei',
        'yusuke-oga','yuta-takaoka','yutong-chen',
    ],
    '2024': [
        'haomin-fu','itsuki-oyama','kodai-matsumoto','ryudai-ueno','shen-siyu',
        'shogo-nakamura','tomomi-shoda','xianzhe-yang','yuki-noguchi',
        'yuki-tomita','zhang-kaili',
    ],
    '2025': [
        'kohei-sawada','nozomi-goto','qi-shi','rika-iriguchi','ryoshi-oda',
        'takahiro-yamaguchi','wang-sheng','yan-chenyu','yuki-nishimura',
        'zhai-xiazhe','zhang-jingxuan','zhanyi-xiang',
    ],
    '2026': [
        'chang-s','chen-h','jiang-z','kotajima-m','minoda-k','mochizuki-t',
        'nakagawa-n','omoto-s','sun-h','wang-w','yoshida-s','zheng-q','zou-z',
    ],
}

PROGRAMME = {
    '2021': 'Q-ENERGY Fellowship',
    '2022': 'Q-ENERGY Fellowship',
    '2023': 'Q-ENERGY Fellowship',
    '2024': 'K2-SPRING',
    '2025': 'K2-SPRING',
    '2026': 'K2-SPRING',
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def strip_tags(s):
    """Remove all HTML tags and decode entities to plain text."""
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html_lib.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def get_lang(html, selector_pattern, lang='en'):
    """Extract text from a data-lang-en/jp="" element matching a pattern."""
    attr = f'data-lang-{lang}=""'
    m = re.search(selector_pattern + rf'\s+{attr}[^>]*>(.*?)</', html, re.DOTALL)
    if m:
        return strip_tags(m.group(1))
    return None


def extract_subline_field(html, field_en):
    """Extract EN <dd> value from hero-subline dl where dt contains field_en.
    Handles inline (<dl><dt…>) and multiline (<dl>\n  <dt…>) formats,
    and both plain <dd>TEXT</dd> and bilingual <dd data-lang-en="">TEXT</dd>."""
    # Match the <dl> block that contains this field label
    pattern = (
        r'<dl>[\s]*<dt data-lang-en="">' + re.escape(field_en) +
        r'</dt>.*?</dl>'
    )
    block_m = re.search(pattern, html, re.DOTALL)
    if not block_m:
        return None
    block = block_m.group(0)
    # Prefer data-lang-en dd
    en_m = re.search(r'<dd data-lang-en="">(.*?)</dd>', block, re.DOTALL)
    if en_m:
        return strip_tags(en_m.group(1)) or None
    # Fallback: plain dd
    plain_m = re.search(r'<dd>(.*?)</dd>', block, re.DOTALL)
    return strip_tags(plain_m.group(1)) if plain_m else None


def extract_supervisor(html):
    """Return (name_en, name_jp, url) from hero-subline supervisor dd."""
    m = re.search(
        r'<dt data-lang-en="">Supervisor</dt>.*?<dd>(.*?)</dd>',
        html, re.DOTALL
    )
    if not m:
        return None, None, None
    dd = m.group(1).strip()
    if 'To be added' in dd or not dd:
        return None, None, None
    # URL from first <a href>
    url_m  = re.search(r'href="([^"]+)"', dd)
    url    = url_m.group(1) if url_m else None
    # Extract EN and JP link texts separately
    en_m   = re.search(r'data-lang-en=""[^>]*>\s*(.*?)\s*</a>', dd, re.DOTALL)
    jp_m   = re.search(r'data-lang-jp=""[^>]*>\s*(.*?)\s*</a>', dd, re.DOTALL)
    name_en = strip_tags(en_m.group(1)) if en_m else None
    name_jp = strip_tags(jp_m.group(1)) if jp_m else None
    # If EN and JP are identical fall back to single value
    if name_en == name_jp:
        name_jp = None
    return name_en or None, name_jp or None, url


def extract_research_primary(section_html):
    """Extract title/abstract EN+JP from <article class='research-primary'>."""
    art = re.search(r'<article[^>]*class="research-primary[^"]*"[^>]*>(.*?)</article>',
                    section_html, re.DOTALL)
    if not art:
        return None
    body = art.group(1)
    title_en = get_lang(body, r'<h3 class="research-title"', 'en')
    title_jp = get_lang(body, r'<h3 class="research-title"', 'jp')
    abs_en_m = re.search(r'<div class="research-abstract"\s+data-lang-en="">(.*?)</div>', body, re.DOTALL)
    abs_jp_m = re.search(r'<div class="research-abstract"\s+data-lang-jp="">(.*?)</div>', body, re.DOTALL)
    abstract_en = strip_tags(abs_en_m.group(1)) if abs_en_m else None
    abstract_jp = strip_tags(abs_jp_m.group(1)) if abs_jp_m else None
    return {
        'title_en': title_en,
        'title_jp': title_jp,
        'abstract_en': abstract_en,
        'abstract_jp': abstract_jp,
    }


def extract_phd_card(section_html):
    """Extract title/abstract EN+JP from <div class='phd-body'>."""
    body_m = re.search(r'<div class="phd-body">(.*?)</div>\s*</div>', section_html, re.DOTALL)
    if not body_m:
        return None
    body = body_m.group(1)
    title_en_m = re.search(r'<h3 data-lang-en="">(.*?)</h3>', body, re.DOTALL)
    title_jp_m = re.search(r'<h3 data-lang-jp="">(.*?)</h3>', body, re.DOTALL)
    abs_en_m   = re.search(r'<div data-lang-en=""><p>(.*?)</p></div>', body, re.DOTALL)
    abs_jp_m   = re.search(r'<div data-lang-jp=""><p>(.*?)</p></div>', body, re.DOTALL)
    title_en = strip_tags(title_en_m.group(1)) if title_en_m else None
    title_jp = strip_tags(title_jp_m.group(1)) if title_jp_m else None
    abstract_en = strip_tags(abs_en_m.group(1)) if abs_en_m else None
    abstract_jp = strip_tags(abs_jp_m.group(1)) if abs_jp_m else None
    # Return None if both titles are placeholder
    if title_en in ('To be added', None) and title_jp in ('To be added', None):
        return None
    return {
        'title_en': title_en if title_en != 'To be added' else None,
        'title_jp': title_jp if title_jp != 'To be added' else None,
        'abstract_en': abstract_en,
        'abstract_jp': abstract_jp,
    }


def clean_li(li_html):
    """
    Convert a <li> inner HTML to structured dict.
    Returns {'text': str, 'doi': str|None} or None if placeholder.
    """
    # Skip "Coming soon" placeholders
    if 'ach-soon' in li_html:
        return None
    doi_m = re.search(r'href="(https?://doi\.org/[^"]+)"', li_html)
    doi = doi_m.group(1) if doi_m else None
    text = strip_tags(li_html)
    # Remove the raw DOI URL if it duplicates what's already in the text
    if doi and doi.replace('https://doi.org/', '') in text:
        text = re.sub(r'\s*https?://doi\.org/\S+', '', text).strip()
    return {'text': text, 'doi': doi} if text else None


def extract_achievements(ach_html):
    """
    Parse <div class='ach-card'> and return structured dict:
    { 'papers': [...], 'conferences': [...], 'awards': [...], 'other': [...] }
    """
    result = {'papers': [], 'conferences': [], 'awards': [], 'other': []}

    LABEL_MAP = {
        'research papers':       'papers',
        'conference presentations': 'conferences',
        'awards':                'awards',
        'fellowships':           'awards',
        'other achievements':    'other',
        'other':                 'other',
    }

    for group in re.finditer(
        r'<div class="ach-group">(.*?)</div>\s*(?=<div class="ach-group">|</div>\s*</section>|</div>\s*\n)',
        ach_html, re.DOTALL
    ):
        g = group.group(1)
        # Get EN label text
        label_m = re.search(r'<div class="ach-label">.*?data-lang-en="">(.*?)</span>', g, re.DOTALL)
        if not label_m:
            continue
        label = strip_tags(label_m.group(1)).lower()
        key = next((v for k, v in LABEL_MAP.items() if k in label), 'other')

        # Extract <li> items
        for li in re.finditer(r'<li>(.*?)</li>', g, re.DOTALL):
            item = clean_li(li.group(1))
            if item:
                result[key].append(item)

    return result


def extract_photo(html):
    """Return normalised photo path (assets/photos/...) or None."""
    m = re.search(r'<img src="([^"]*assets/photos/[^"]+)"', html)
    if m:
        # Normalise ../../assets/photos/... → assets/photos/...
        p = m.group(1)
        p = re.sub(r'^(?:\.\./)+', '', p)
        return p
    return None


def extract_source_url(html):
    """Return the public source URL (any source-pill link, or Source dd fallback)."""
    # source-pill — matches any link text (covers "Original public page",
    # "Public profile page", etc.)
    m = re.search(r'<a class="source-pill" href="(https://q-pit[^"]+)"', html)
    if m:
        return m.group(1)
    # Fallback: Source dd in meta-card (older pages before cleanup)
    m = re.search(r'<dt>Source</dt><dd><a href="(https://q-pit[^"]+)"', html)
    if m:
        return m.group(1)
    return None


# ── Main extraction ───────────────────────────────────────────────────────────

def extract_student(slug, cohort, html):
    """Return a student dict extracted from page HTML."""

    sections = list(re.finditer(r'<section>(.*?)</section>', html, re.DOTALL))

    # ── Identity ──────────────────────────────────────────────────────────────
    name_en_m = re.search(r'<h1 class="name" data-lang-en="">(.*?)</h1>', html, re.DOTALL)
    name_jp_m = re.search(r'<h1 class="name name-jp" data-lang-jp="">(.*?)</h1>', html, re.DOTALL)
    name_en = strip_tags(name_en_m.group(1)) if name_en_m else slug
    name_jp = strip_tags(name_jp_m.group(1)) if name_jp_m else None
    # JP name shouldn't duplicate EN name
    if name_jp == name_en:
        name_jp = None

    # ── Hero subline ──────────────────────────────────────────────────────────
    affiliation = extract_subline_field(html, 'Affiliation')
    dept        = extract_subline_field(html, 'Major / Department')
    sup_name, sup_name_jp, sup_url = extract_supervisor(html)

    # ── Photo ─────────────────────────────────────────────────────────────────
    photo = extract_photo(html)

    # ── Source URL ────────────────────────────────────────────────────────────
    source_url = extract_source_url(html)

    # ── K2-SPRING research (2024+) ───────────────────────────────────────────
    k2spring = None
    if int(cohort) >= 2024:
        for s in sections:
            if 'K2-SPRING' in s.group(1):
                k2spring = extract_research_primary(s.group(1))
                if k2spring is None:
                    # Fallback: try phd-body format (shouldn't happen but defensive)
                    k2spring = extract_phd_card(s.group(1))
                break

    # ── Doctoral research ────────────────────────────────────────────────────
    phd = None
    for s in sections:
        body = s.group(1)
        if 'Doctoral' in body or ('phd-body' in body and 'K2-SPRING' not in body):
            # Try research-primary first (some 2024/2025 doctoral sections use it)
            phd = extract_research_primary(body)
            if phd is None:
                phd = extract_phd_card(body)
            if phd:
                break

    # ── Achievements ─────────────────────────────────────────────────────────
    achievements = {'papers': [], 'conferences': [], 'awards': [], 'other': []}
    for s in sections:
        body = s.group(1)
        if 'ach-card' in body:
            achievements = extract_achievements(body)
            break

    return {
        'slug':             slug,
        'cohort':           int(cohort),
        'programme':        PROGRAMME[cohort],
        'name_en':          name_en,
        'name_jp':          name_jp,
        'affiliation_en':   affiliation if affiliation and affiliation != 'To be added' else None,
        'dept_en':          dept if dept and dept != 'To be added' else None,
        'supervisor_name':     sup_name,
        'supervisor_name_jp':  sup_name_jp,
        'supervisor_url':      sup_url,
        'photo':            photo,
        'source_url':       source_url,
        'k2spring':         k2spring,
        'phd':              phd,
        'achievements':     achievements,
    }


def main():
    students = []
    for cohort, slugs in sorted(PRIMARY.items()):
        print(f'\n── {cohort} ──')
        for slug in slugs:
            path = BASE / 'students' / cohort / f'{slug}.html'
            if not path.exists():
                print(f'  SKIP  {slug} — file not found')
                continue
            html = path.read_text(encoding='utf-8')
            rec  = extract_student(slug, cohort, html)
            students.append(rec)

            # Summary line
            papers_n = len(rec['achievements']['papers'])
            has_k2   = '✓k2' if rec['k2spring'] else ' --'
            has_phd  = '✓phd' if rec['phd'] else '  --'
            print(f'  OK    {slug:<45} {has_k2} {has_phd}  papers={papers_n}')

    OUT.parent.mkdir(exist_ok=True)
    payload = {
        'generated': str(date.today()),
        'total': len(students),
        'students': students,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nWrote {len(students)} records → {OUT}')

    # Quick stats
    from collections import Counter
    cohort_counts = Counter(s['cohort'] for s in students)
    paper_students = sum(1 for s in students if s['achievements']['papers'])
    total_papers   = sum(len(s['achievements']['papers']) for s in students)
    print(f'\nStats:')
    for y in sorted(cohort_counts): print(f'  {y}: {cohort_counts[y]} students')
    print(f'  Students with papers:  {paper_students}')
    print(f'  Total paper entries:   {total_papers}')


if __name__ == '__main__':
    main()
