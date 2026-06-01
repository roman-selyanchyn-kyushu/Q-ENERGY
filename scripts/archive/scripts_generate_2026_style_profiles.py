#!/usr/bin/env python3
"""Generate uniform 2026-style individual pages for public Q-ENERGY cohorts.

Rules requested by Roman:
- Earlier cohorts should use the same page format as the 2026 cohort.
- Show affiliation, major/department, supervisor, K2-SPRING topic, doctoral research,
  achievements, and programme/institutional blocks where applicable.
- If information is not available yet, keep the field in place with a clear placeholder.
- Exception: 2022 and 2023 students do not have K2-SPRING topics, only Doctoral research.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "public_site_extracted.json"
STYLE_SOURCE = ROOT / "students" / "2026" / "yoshida-s.html"
NO_K2_YEARS = {"2022", "2023"}
PLACEHOLDER = "To be added"
PLACEHOLDER_JP = "追記予定"


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "student"


def text(value: object, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def esc(s: object) -> str:
    return escape(str(s or ""))


def paragraphs(s: str, placeholder: str = "Detailed information will be added after it is provided.") -> str:
    s = text(s)
    if not s:
        return f'<p class="ach-soon">{escape(placeholder)}</p>'
    parts = [p.strip() for p in re.split(r"\n\s*\n", s) if p.strip()] or [s]
    return "".join(f"<p>{escape(p).replace(chr(10), '<br>')}</p>" for p in parts)


def split_name(name: str) -> str:
    parts = name.split()
    if len(parts) >= 2:
        return f"{escape(' '.join(parts[:-1]))} <span class=\"em\">{escape(parts[-1])}</span>"
    return escape(name)


def split_affiliation(value: str) -> tuple[str, str]:
    """Best-effort split into affiliation and major/department without inventing data."""
    value = text(value)
    if not value:
        return PLACEHOLDER, PLACEHOLDER
    lines = [ln.strip() for ln in value.splitlines() if ln.strip()]
    if len(lines) >= 2:
        return lines[0], " / ".join(lines[1:])
    # Handle common one-line forms.
    markers = [" Department of ", ", Department of ", "Department of "]
    for marker in markers:
        if marker in value and not value.startswith("Department of "):
            left, right = value.split(marker, 1)
            right = ("Department of " + right) if "Department" not in marker else marker.strip() + " " + right
            return left.strip(" ,"), right.strip()
    return value, PLACEHOLDER


def extract_css() -> str:
    html = STYLE_SOURCE.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", html, re.S)
    if not m:
        raise RuntimeError("Could not extract 2026 CSS")
    css = m.group(1)
    css += """
  .source-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px;}
  .source-pill{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border:1px solid var(--line);border-radius:999px;background:rgba(255,255,255,.5);color:var(--accent);text-decoration:none;font-family:var(--sans);font-weight:600;font-size:13px;transition:background .25s,transform .25s;}
  .source-pill:hover{background:rgba(255,255,255,.95);transform:translateY(-1px);}
  .meta-card{border:1px solid var(--line);border-radius:var(--r-lg);padding:clamp(20px,3vw,32px);background:rgba(255,255,255,.38);}
  .meta-list{display:grid;grid-template-columns:190px 1fr;gap:12px 24px;margin:0;}
  .meta-list dt{font-family:var(--sans);font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);}
  .meta-list dd{margin:0;font-family:var(--serif);font-size:16px;color:var(--ink);line-height:1.55;}
  .placeholder-note{font-family:var(--serif);font-style:italic;color:var(--ink-4);}
  @media(max-width:680px){.meta-list{grid-template-columns:1fr;gap:4px 0}.meta-list dd{margin-bottom:12px}}
"""
    return css


CSS = extract_css()
SCRIPT = """<script>
(function(){
  var html = document.documentElement;
  var toggle = document.querySelector('.lang-toggle');
  if (!toggle) return;
  var buttons = toggle.querySelectorAll('button[data-set-lang]');
  var stored = null;
  try { stored = localStorage.getItem('k2spring_lang'); } catch(e){}
  if (stored === 'jp' || stored === 'en') setLang(stored);
  function setLang(lang){
    html.setAttribute('lang', lang === 'jp' ? 'ja' : 'en');
    toggle.setAttribute('data-lang', lang);
    buttons.forEach(function(b){
      var on = b.dataset.setLang === lang;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    try { localStorage.setItem('k2spring_lang', lang); } catch(e){}
  }
  buttons.forEach(function(b){ b.addEventListener('click', function(){ setLang(b.dataset.setLang); }); });
})();
(function(){
  if (!('IntersectionObserver' in window)) return;
  var els = document.querySelectorAll('.research-primary, .phd-card, .supervisor-row, .ach-group, .meta-card');
  els.forEach(function(el){
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity .8s cubic-bezier(.2,.6,.2,1), transform .8s cubic-bezier(.2,.6,.2,1)';
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if (e.isIntersecting){ e.target.style.opacity = '1'; e.target.style.transform = 'none'; io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  els.forEach(function(el){ io.observe(el); });
})();
</script>"""


def section_head(num: int, en: str, en_em: str, jp: str, jp_em: str) -> str:
    return f"""
  <div class="section-head">
    <div class="section-num"><span>§ {num:02d}</span></div>
    <div>
      <h2 class="section-title" data-lang-en="">{esc(en)} <span class="em">{esc(en_em)}</span></h2>
      <h2 class="section-title" data-lang-jp="">{esc(jp)} <span class="em">{esc(jp_em)}</span></h2>
    </div>
  </div>"""


def k2_section(num: int) -> str:
    return f"""
<section>
{section_head(num, 'K2-SPRING', 'research topic', 'K2-SPRING', '研究テーマ')}
  <article class="research-primary reveal">
    <div class="research-banner">
      <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true"><path d="M6 0l1.5 4.5L12 6 7.5 7.5 6 12 4.5 7.5 0 6l4.5-1.5z"/></svg>
      <span data-lang-en="">K2-SPRING topic &middot; Pending details</span>
      <span data-lang-jp="">K2-SPRINGテーマ &middot; 追記予定</span>
    </div>
    <h3 class="research-title" data-lang-en="">{PLACEHOLDER}</h3>
    <h3 class="research-title" data-lang-jp="">{PLACEHOLDER_JP}</h3>
    <div class="research-abstract" data-lang-en=""><p class="ach-soon">K2-SPRING topic information is not available in the current public data. It will be added after Roman provides it.</p></div>
    <div class="research-abstract" data-lang-jp=""><p class="ach-soon">K2-SPRING研究テーマは現在の公開データには含まれていません。情報提供後に追記します。</p></div>
  </article>
</section>"""


def doctoral_section(num: int, title: str, outline: str, source: str, source_label: str, year: str) -> str:
    return f"""
<section>
{section_head(num, 'Doctoral', 'research', '博士', '研究')}
  <div class="phd-card reveal">
    <div class="phd-aside"><span data-lang-en="">Main PhD work</span><span data-lang-jp="">博士課程主研究</span></div>
    <div class="phd-body">
      <h3 data-lang-en="">{esc(title or PLACEHOLDER)}</h3>
      <h3 data-lang-jp="">{esc(title or PLACEHOLDER_JP)}</h3>
      <div data-lang-en="">{paragraphs(outline)}</div>
      <div data-lang-jp="">{paragraphs(outline, '詳細情報は提供後に追記します。')}</div>
      <div class="source-actions"><a class="source-pill" href="{esc(source)}" target="_blank" rel="noopener">{esc(source_label)}</a><a class="source-pill" href="index.html">Back to {esc(year)} cohort</a></div>
    </div>
  </div>
</section>"""


def supervisor_section(num: int) -> str:
    return f"""
<section>
{section_head(num, 'Supervisor', 'information', '指導教員', '情報')}
  <div class="supervisor-row reveal">
    <div class="sup-avatar">?</div>
    <div class="sup-info">
      <div class="role" data-lang-en="">Academic supervisor</div>
      <div class="role" data-lang-jp="">指導教員</div>
      <div class="name-line" data-lang-en="">{PLACEHOLDER}</div>
      <div class="name-line" data-lang-jp="">{PLACEHOLDER_JP}</div>
      <div class="dept" data-lang-en="">Supervisor information is not available yet.</div>
      <div class="dept" data-lang-jp="">指導教員情報は追記予定です。</div>
    </div>
  </div>
</section>"""


def achievements_section(num: int) -> str:
    return f"""
<section>
{section_head(num, 'Research', 'achievements', '研究', '業績')}
  <div class="ach-card">
    <div class="ach-group">
      <div class="ach-label"><span data-lang-en="">Research Papers</span><span data-lang-jp="">論文</span></div>
      <ol class="ach-list"><li><span class="ach-soon"><span data-lang-en="">Coming soon</span><span data-lang-jp="">準備中</span></span></li></ol>
    </div>
    <div class="ach-group">
      <div class="ach-label"><span data-lang-en="">Conference Presentations</span><span data-lang-jp="">学会発表</span></div>
      <ol class="ach-list"><li><span class="ach-soon"><span data-lang-en="">Coming soon</span><span data-lang-jp="">準備中</span></span></li></ol>
    </div>
    <div class="ach-group">
      <div class="ach-label"><span data-lang-en="">Other Achievements</span><span data-lang-jp="">その他の業績</span></div>
      <ol class="ach-list"><li><span class="ach-soon"><span data-lang-en="">Coming soon</span><span data-lang-jp="">準備中</span></span></li></ol>
    </div>
  </div>
</section>"""


def metadata_section(num: int, year: str, affiliation: str, major_dept: str, supervisor: str, source: str, source_label: str) -> str:
    items = [
        ("Cohort", year),
        ("Affiliation", affiliation),
        ("Major / Department", major_dept),
        ("Supervisor", supervisor),
        ("Source", f'<a href="{esc(source)}" target="_blank" rel="noopener">{esc(source_label)}</a>'),
        ("Data status", "Some fields are placeholders and will be updated after Roman provides the missing information."),
    ]
    dts = "".join(f"<dt>{esc(k)}</dt><dd>{v if v.startswith('<a ') else esc(v).replace(chr(10), '<br>')}</dd>" for k, v in items)
    return f"""
<section>
{section_head(num, 'Profile', 'metadata', 'プロフィール', '情報')}
  <div class="meta-card"><dl class="meta-list">{dts}</dl></div>
</section>"""


def partners_footer(year: str) -> str:
    return f"""
<section class="partners">
  <div class="partners-head" style="max-width:var(--maxw);margin:0 auto;"><span data-lang-en="">Programme &amp; institutional affiliation</span><span data-lang-jp="">プログラム・機関情報</span></div>
  <div class="partners-row" style="max-width:var(--maxw);margin:0 auto;">
    <div class="partner-wrap"><a class="partner" href="https://k-spring.kyushu-u.ac.jp" target="_blank" rel="noopener"><img src="../../assets/logos/logo-k2spring.svg" alt="K2-SPRING"></a><span class="partner-caption"><span data-lang-en="">JST SPRING programme</span><span data-lang-jp="">JSTスプリングプログラム</span></span></div>
    <div class="partner-wrap"><a class="partner" href="https://q-pit.kyushu-u.ac.jp/" target="_blank" rel="noopener"><img src="../../assets/logos/logo-qpit.png" alt="Q-PIT"></a><span class="partner-caption"><span data-lang-en="">Unit coordinator</span><span data-lang-jp="">ユニットコーディネーター</span></span></div>
    <div class="partner-wrap"><a class="partner" href="https://q-pit.kyushu-u.ac.jp/fellow-ship-en/" target="_blank" rel="noopener"><img src="../../assets/logos/logo-qenergy.png" alt="Q-Energy Innovator Unit"></a><span class="partner-caption"><span data-lang-en="">Q-Energy Innovator Unit</span><span data-lang-jp="">グリーンイノベーションユニット</span></span></div>
    <div class="partner-wrap"><a class="partner" href="https://www.kyushu-u.ac.jp/en/" target="_blank" rel="noopener"><img src="../../assets/logos/logo-kyushu.png" alt="Kyushu University" class="ku-tall"></a><span class="partner-caption"><span data-lang-en="">Host university</span><span data-lang-jp="">ホスト大学</span></span></div>
  </div>
</section>
<footer class="footer">
  <a href="index.html" class="back-link"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 12L6 8l4-4"/></svg>Back to {esc(year)} cohort</a>
  <div class="footer-meta">K2-SPRING &middot; Q-PIT &middot; Kyushu University &middot; Local prototype</div>
</footer>"""


def page_html(year: str, item: dict) -> str:
    rows = item.get("rows") or {}
    # Prefer the cohort-card name for identity. Some extracted row names are stale or
    # mismatched on older public pages, while card names/photos/links are the stable
    # navigation source.
    name = text(item.get("name"), text(rows.get("Name"), "Q-ENERGY Fellow"))
    raw_affiliation = text(rows.get("Affiliation"), "")
    affiliation, major_dept = split_affiliation(raw_affiliation)
    supervisor = PLACEHOLDER
    doctoral_title = text(rows.get("Title of the Research"), "")
    doctoral_outline = text(rows.get("Outline of Research"), "")
    source = text(item.get("source"), text(item.get("href"), "#"))
    image_local = text(item.get("image_local"))
    image_src = "../../" + image_local if image_local else "../../assets/photos/placeholder-portrait.svg"
    alt = text(item.get("alt")) or name
    source_label = "Original PDF profile" if source.lower().endswith(".pdf") else "Original public page"

    if year == "2025" and not doctoral_outline:
        doctoral_title = PLACEHOLDER
        doctoral_outline = "The public 2025 profile is currently available as a PDF link only in the extracted data. Details will be added after the missing information is provided."
    if not doctoral_title:
        doctoral_title = PLACEHOLDER

    sections = []
    n = 1
    if year not in NO_K2_YEARS:
        sections.append(k2_section(n)); n += 1
    sections.append(doctoral_section(n, doctoral_title, doctoral_outline, source, source_label, year)); n += 1
    sections.append(supervisor_section(n)); n += 1
    sections.append(achievements_section(n)); n += 1
    sections.append(metadata_section(n, year, affiliation, major_dept, supervisor, source, source_label)); n += 1

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(name)} — Q-ENERGY Fellow {esc(year)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&family=Noto+Serif+JP:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <a href="../../index.html" class="program-mark" aria-label="K2-SPRING Q-ENERGY home"><span class="dot" aria-hidden="true"></span><span>K2&#8209;SPRING</span><small data-lang-en="">Q-ENERGY Innovator Unit</small><small data-lang-jp="">グリーンイノベーションユニット</small></a>
    <div class="lang-toggle" data-lang="en" role="group" aria-label="Language"><span class="pill" aria-hidden="true"></span><button type="button" data-set-lang="en" class="is-active" aria-pressed="true">EN</button><button type="button" data-set-lang="jp" aria-pressed="false">日本語</button></div>
  </div>
</header>
<section class="hero">
  <div class="portrait-frame no-photo reveal" id="portrait">
    <img src="{esc(image_src)}" alt="{esc(alt)}" onload="this.closest('.portrait-frame').classList.remove('no-photo')" onerror="this.remove()">
    <span>Photo<br>{esc(name)}</span>
    <div class="portrait-tag"><span data-lang-en="">{esc(year)} Cohort</span><span data-lang-jp="">{esc(year)}年度</span></div>
  </div>
  <div class="hero-meta reveal">
    <div class="eyebrow"><span data-lang-en="">K2-SPRING &middot; Q-ENERGY Innovator Unit &middot; Cohort {esc(year)}</span><span data-lang-jp="">K2-SPRING &middot; グリーンイノベーションユニット &middot; {esc(year)}年度</span></div>
    <h1 class="name" data-lang-en="">{split_name(name)}</h1>
    <h1 class="name name-jp" data-lang-jp="">{esc(name)}</h1>
    <div class="hero-subline">
      <dl><dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">所属</dt><dd>{esc(affiliation).replace(chr(10), '<br>')}</dd></dl>
      <dl><dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">専攻・部局</dt><dd>{esc(major_dept).replace(chr(10), '<br>')}</dd></dl>
      <dl><dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>{esc(supervisor)}</dd></dl>
    </div>
  </div>
</section>
{''.join(sections)}
{partners_footer(year)}
{SCRIPT}
</body>
</html>
"""


def update_2025_index(items: list[dict]) -> None:
    path = ROOT / "students" / "2025" / "index.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    for item in items:
        href = text(item.get("href"))
        if href:
            html = html.replace(f'href="{href}"', f'href="{slugify(text(item.get("name")))}.html"')
    html = html.replace("PDF profile links from the public site are preserved.", "Individual pages use the 2026 profile style; original PDF links are preserved inside each page.")
    path.write_text(html, encoding="utf-8")


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    written = []
    for year in ["2025", "2024", "2023", "2022", "2021"]:
        items = data.get(year, [])
        year_dir = ROOT / "students" / year
        year_dir.mkdir(parents=True, exist_ok=True)
        for item in items:
            filename_name = text(item.get("name"), text((item.get("rows") or {}).get("Name")))
            path = year_dir / f"{slugify(filename_name)}.html"
            path.write_text(page_html(year, item), encoding="utf-8")
            written.append(path)
        if year == "2025":
            update_2025_index(items)
    print(f"Generated {len(written)} uniform 2026-style profile pages")
    print("2022/2023 generated without K2-SPRING topic sections; other years keep the K2 placeholder section.")
    for path in written[:8]:
        print(path.relative_to(ROOT))
    if len(written) > 8:
        print("...")


if __name__ == "__main__":
    main()
