#!/usr/bin/env python3
"""Build the top landing page with the original public-page structure."""
from __future__ import annotations

import json
import re
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC_DATA = json.loads((ROOT / "data" / "public_site_extracted.json").read_text(encoding="utf-8"))
SECTIONS = json.loads((ROOT / "data" / "public_sections_extracted.json").read_text(encoding="utf-8"))
COHORTS = json.loads((ROOT / "data" / "cohorts.json").read_text(encoding="utf-8"))


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "student"


def esc(s: object) -> str:
    return escape(str(s or ""))


def download(url: str, dest: Path) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        dest.write_bytes(r.read())


def local_pamphlets() -> list[dict]:
    out = []
    for link in SECTIONS.get("Digital pamphlet", {}).get("links", []):
        year = str(link.get("text", "")).strip()
        img = link.get("img", "")
        href = link.get("href", "")
        local = f"assets/pamphlets/digital_book_bnr_{year}.jpg"
        if img:
            try:
                download(img, ROOT / local)
            except Exception as e:
                print(f"warning: could not download {img}: {e}")
                local = img
        out.append({"year": year, "href": href, "img": local, "alt": link.get("alt") or f"Digital pamphlet {year}"})
    return out


def profile_photo_2026(filename: str) -> str:
    path = ROOT / "students" / "2026" / filename
    if not path.exists():
        return "students/2026/assets/photos/placeholder-portrait.svg"
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<img src="([^"]+)" alt=', html)
    if not m:
        return "students/2026/assets/photos/placeholder-portrait.svg"
    src = m.group(1)
    if src.startswith("http") or src.startswith("/"):
        return src
    return "students/2026/" + src


def student_items(year: str) -> list[dict]:
    if year == "2026":
        items = []
        for name, filename, _supervisor in COHORTS["2026"]:
            label = name.split(" / ")[0]
            items.append({"name": label, "href": f"students/2026/{filename}", "img": profile_photo_2026(filename)})
        return items
    items = []
    for item in PUBLIC_DATA.get(year, []):
        name = item.get("name") or (item.get("rows") or {}).get("Name") or "Student"
        # Filenames were generated from item['name'] to keep cohort index links stable.
        href = f"students/{year}/{slugify(name)}.html"
        img = item.get("image_local") or ""
        img = img if img.startswith("http") else img
        items.append({"name": name, "href": href, "img": img})
    return items


def render_student_section(year: str) -> str:
    cards = []
    for item in student_items(year):
        img = item["img"]
        if img and not img.startswith("http") and not img.startswith("students/"):
            src = img
        else:
            src = img
        cards.append(f"""
        <a class="photo-person" href="{esc(item['href'])}">
          <div class="photo-box"><img src="{esc(src)}" alt="{esc(item['name'])}" loading="lazy" onerror="this.closest('.photo-box').classList.add('missing'); this.remove()"></div>
          <div class="photo-name">{esc(item['name'])}</div>
        </a>""")
    jp_label = "ユニット生" if year in {"2025", "2026"} else "フェロー"
    en_label = "Students" if year in {"2025", "2026"} else "Fellows"
    return f"""
    <section class="student-year" id="students-{esc(year)}">
      <h2 class="center-title"><span data-ja="{esc(year)}年{jp_label}" data-en="{esc(year)} {en_label}">{esc(year)}年{jp_label}</span></h2>
      <div class="photo-grid">
        {''.join(cards)}
      </div>
    </section>"""


def main() -> None:
    pamphlets = local_pamphlets()
    pamphlet_cards = "".join(f"""
      <a class="pamphlet-card" href="{esc(p['href'])}" target="_blank" rel="noopener">
        <img src="{esc(p['img'])}" alt="{esc(p['alt'])}" loading="lazy">
        <span data-ja="{esc(p['year'])}年度" data-en="FY{esc(p['year'])}">{esc(p['year'])}年度</span>
      </a>""" for p in pamphlets)

    # Roman clarified: keep the section order, but redesign the top area properly.
    # Program media should show only the summer-camp video, not fellowship/fellow interview videos.
    student_sections = "\n".join(render_student_section(y) for y in ["2026", "2025", "2024", "2023", "2022", "2021"])

    html = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Q-ENERGY Innovator Unit — Landing</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500;700&family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/main.css">
</head>
<body class="landing-structured">
<header class="top">
  <div class="topin">
    <a class="brand" href="index.html">K2-SPRING · Q-ENERGY</a>
    <nav>
      <a href="#recruitment" data-ja="学生募集" data-en="Admissions">学生募集</a>
      <a href="#program" data-ja="夏合宿" data-en="Summer camp">夏合宿</a>
      <a href="#pamphlets" data-ja="パンフレット" data-en="Pamphlets">パンフレット</a>
      <a href="#students" data-ja="ユニット生" data-en="Students">ユニット生</a>
      <button class="lang-toggle" type="button" data-lang-toggle aria-label="Switch language">EN</button>
    </nav>
  </div>
</header>
<main>
  <section class="landing-hero" id="recruitment">
    <div class="hero-copy">
      <p class="eyebrow">Kyushu University · K2-SPRING · Q-ENERGY</p>
      <h1 data-ja="未来のエネルギー研究を担う博士人材へ" data-en="For doctoral researchers shaping the future of energy">未来のエネルギー研究を担う博士人材へ</h1>
      <p class="lead" data-ja="Q-ENERGYは、脱炭素エネルギー分野の挑戦的な博士研究を支援する九州大学の人材育成ユニットです。" data-en="Q-ENERGY supports ambitious doctoral research in decarbonized energy at Kyushu University.">Q-ENERGYは、脱炭素エネルギー分野の挑戦的な博士研究を支援する九州大学の人材育成ユニットです。</p>
      <div class="hero-actions">
        <a class="btn primary" href="https://k-spring.kyushu-u.ac.jp/" target="_blank" rel="noopener" data-ja="学生募集を見る" data-en="View admissions">学生募集を見る</a>
        <a class="btn ghost" href="#students" data-ja="学生・フェローを見る" data-en="Meet students">学生・フェローを見る</a>
      </div>
    </div>
    <aside class="admission-visual" aria-label="Admissions image">
      <img src="assets/photos/admission.jpg" alt="Student writing during an admissions-related session" loading="eager">
      <div class="admission-card">
        <span class="panel-label" data-ja="学生募集" data-en="Admissions">学生募集</span>
        <p data-ja="募集要項は「九州大学 次世代研究者挑戦的研究プログラム 未来創造コース」の学生募集ページをご確認ください。" data-en="Please check the K2-SPRING Future Creation Course admissions page for application details.">募集要項は「九州大学 次世代研究者挑戦的研究プログラム 未来創造コース」の学生募集ページをご確認ください。</p>
      </div>
    </aside>
  </section>

  <section class="plain-section feature-section" id="program">
    <div class="section-kicker" data-ja="プログラムについて" data-en="Program">プログラムについて</div>
    <div class="feature-grid">
      <div>
        <h2 data-ja="夏合宿の雰囲気を動画で紹介" data-en="A look inside the Q-ENERGY summer camp">夏合宿の雰囲気を動画で紹介</h2>
        <p class="section-lead" data-ja="2025年を初期表示に、年別タブで4回分の夏合宿動画を切り替えられます。" data-en="Use the year tabs to switch between the four summer camp videos. The default view is 2025.">2025年を初期表示に、年別タブで4回分の夏合宿動画を切り替えられます。</p>
      </div>
      <article class="video-card elevated summer-video-switcher" data-summer-video>
        <div class="year-tabs" role="tablist" aria-label="Summer camp videos">
          <button class="year-tab active" type="button" data-video-year="2025" aria-selected="true">2025</button>
          <button class="year-tab" type="button" data-video-year="2024" aria-selected="false">2024</button>
          <button class="year-tab" type="button" data-video-year="2023" aria-selected="false">2023</button>
          <button class="year-tab" type="button" data-video-year="2022" aria-selected="false">2022</button>
        </div>
        <a class="video-thumb" href="https://www.youtube.com/watch?v=srLEu440lV8" target="_blank" rel="noopener" aria-label="Watch Summer camp 2025 on YouTube" data-video-link>
          <img src="assets/video/summer-camp-2025.jpg" alt="Summer camp 2025 video thumbnail" loading="lazy" data-video-image>
          <span class="play-button" aria-hidden="true"></span>
        </a>
        <div class="video-caption" data-video-caption data-ja="Summer camp 2025 on YouTube" data-en="Summer camp 2025 on YouTube">Summer camp 2025 on YouTube</div>
      </article>
    </div>
  </section>

  <section class="plain-section" id="pamphlets">
    <h2 class="center-title"><span data-ja="パンフレット" data-en="Pamphlets">パンフレット</span></h2>
    <div class="pamphlet-grid">
      {pamphlet_cards}
    </div>
  </section>

  <section class="plain-section students-wrap" id="students">
    <h2 class="section-title-modern" data-ja="学生・フェロー" data-en="Students and fellows">学生・フェロー</h2>
    {student_sections}
  </section>
</main>
<footer class="footer">
  <span>Q-ENERGY static remake prototype</span>
  <span>Landing page structure follows the original public page order.</span>
</footer>
<script src="assets/js/main.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("Wrote index.html with original-page structure")


if __name__ == "__main__":
    main()
