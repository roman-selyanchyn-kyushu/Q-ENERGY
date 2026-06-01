# Q-ENERGY Student Site Remake — Progress

Updated: 2026-06-02

Safety rules:
- Do not modify the live Q-PIT/WordPress site.
- Do not modify the original FOR-HERMES folder.
- Work only in this local project folder.

Milestones:
- [x] Inventory/design plan created: `docs/INVENTORY-AND-PLAN.md`
- [x] First local static prototype created
- [x] FY2026 local student pages copied into `students/2026/`
- [x] English top page created: `index.html`
- [x] Japanese top page created: `ja/index.html`
- [x] Cohort card pages created for 2021–2026
- [x] Browser visual verification
- [x] Older cohort individual pages restyled to match 2026 profile style
- [x] Landing page remade with original structural order: recruitment, program/videos, pamphlets, student grids newest-to-oldest
- [x] Landing page top redesigned; program video reduced to summer camp only; language toggle added
- [x] Activities page completed (all 5 activities, photo sliders, bilingual)
- [x] Publications page completed (all cohorts, bilingual)
- [x] News system built (news.html index + individual pages)
- [x] Published to GitHub — https://github.com/roman-selyanchyn-kyushu/Q-ENERGY
- [ ] Roman review / final QA

Resume instruction:
Open the Dropbox folder `00-QPIT/Q-fellowship/QENERGY-STUDENT-SITE-REMAKE` on any machine.
Run `python3 -m http.server 8765` from the project root to preview locally.
Key files: `index.html` (landing), `activities.html`, `publications.html`, `news.html`,
`students/[cohort]/[slug].html` (profiles), `data/students.json` (full database), `data/news.json` (news index metadata).

GitHub repository: https://github.com/roman-selyanchyn-kyushu/Q-ENERGY (branch: main)
- Sensitive folders excluded from repo: `Scopus/`, `LIST/`, `scripts_*.py`, `.claude/`, `__pycache__/`
- `.gitignore` in place to keep future runs of those folders out
- To push updates: `git add [files] && git commit -m "message" && git push`

---

Session 2026-06-02

## GitHub publication
- Repository created: https://github.com/roman-selyanchyn-kyushu/Q-ENERGY (branch: main)
- Initial commit: full static site published from work computer.
- Sensitive folders kept out of repo: `Scopus/`, `LIST/`, `scripts_*.py`, `.claude/`, `__pycache__/` — `.gitignore` added.
- 4 commits: initial commit → remove sensitive folders → remove .claude/__pycache__ + add .gitignore → add robots.txt.
- `robots.txt` added to block search engine indexing (site is for internal/academic use, not public SEO).

---

Session 2026-06-01

## Activities page corrections
- All English text corrected throughout (Joint Seminars, Company Visits, Kyushu Energy Week, Outreach for Industry, Summer Camp).
- Key changes: seminar frequency 2–3 → 3–4 months; added doctoral thesis presentations sentence; updated company visits body; Kyushu Energy Week expanded with "University's main energy-related event" + curated presentations context; Outreach for Industry section renamed from "Decarbonization Society Workshop"; Q-DeCS link added (https://q-decs.kyushu-u.net/); Summer Camp description rewritten, past destinations list updated (added Genkai NPP, corrected Kyocera/Kyocera locations, biogas facility → "Fukuoka").
- All Japanese translations updated to match corrected English (secretary proofread pending).
- `align-items: start` → `align-items: center` on `.act-section` — text and photo now vertically centred.
- Video caption moved to immediately after summer camp description (before destinations list).

## Universal footer
- New footer text across all pages: "K2‑SPRING · Q-ENERGY Innovator Unit (coordinated by Q-PIT, Kyushu University)"
- Copyright line added everywhere: "© 2026 Q-PIT, Kyushu University. Designed & built by Roman Selyanchyn."
- Updated: `index.html`, `activities.html`, `publications.html` (two `<span>` elements).
- Updated: all 75 student profile pages (two `<div class="footer-meta">` elements) via Python script.

## News system built
- `news.html` — standalone news index page; bilingual; card list with date, category tag, lead text, thumbnail.
- `news/` folder — individual article pages (13 total).
- `data/news.json` — index metadata (slug, date, category, headlines, leads, thumbnail paths).
- 4 category tags with colour coding:
  - New Paper (blue), Award (wine/burgundy), Programme Update (green), Event (gold)
- Placeholder visuals for image-less cards: dot-grid texture + category colour wash + diamond mark.
- "News" link added to topbar on `index.html`, `activities.html`, `publications.html`.
- Cards rendered as static HTML (no fetch — works without local server).

### News pages built (13 total, newest first):
1. `phua-yin-kan-explainable-ai-polymer-design.html` — May 2026 · New Paper · J. Mater. Chem. A · graphical abstract
2. `yulu-chen-2025-best-paper-award.html` — Jan 2026 · Award · Building and Environment Best Paper
3. `digital-pamphlet-fy2024.html` — Mar 2025 · Programme Update *(HTML page still needed)*
4. `march-3-16th-joint-seminar.html` — Feb 2025 · Event
5. `energy-week-2025-poster-session.html` — Feb 2025 · Event
6. `summer-camp-2024-on-youtube.html` — Feb 2025 · Programme Update · Genkai NPP camp
7. `the-15th-joint-seminar.html` — Dec 2024 · Event
8. `research-paper-yin-kan-en.html` — Aug 2024 · New Paper · ChemElectroChem
9. `digital-pamphlet-fy2023.html` — Mar 2024 · Programme Update
10. `imada-pr-2024.html` — Feb 2024 · New Paper · J. Environmental Management
11. `summer-2023-en.html` — Dec 2023 · Event · Kagoshima (Kyocera + Yakushima)
12. `sun-mingxu-received-the-103rd-csj-annual-meeting-2023-student-presentation-award.html` — May 2023 · Award
13. `zifie-nie-research-paper.html` — Mar 2023 · New Paper · Applied Energy

---

Session 2026-05-31
- Fixed font-shrink bug on index.html when navigating back from activities.html / publications.html.
  Root cause: "← Back to home" link in footer triggered a fresh page load with a different rendering state.
  Fix: removed the link from both footers (topbar nav covers all navigation). Also added overflow-x:clip
  to html and body in assets/css/main.css as a defensive measure matching student page behaviour.
- Bilingual student names in landing page photo grid: all 71 .photo-name divs now carry data-ja / data-en
  attributes. Japanese students show kanji when JP mode is active; international students fall back to EN.
  Names sourced from data/students.json field name_jp.

---

Pending work:
- [ ] Ask Japanese secretary to verify English romanizations of all 50 supervisor names against their kanji
  (list in data/students.json, fields supervisor_name / supervisor_name_jp).
  Known fix already applied: 藤川 茂紀 → Shigenori (was wrongly Shigeki).
- [ ] Highlight exceptional papers on publications.html (Science Vol.387, Angewandte Chemie,
  Nature Communications, Annual Review of Materials Research, Astrobiology).
- [ ] Secretary proofread of all Japanese text on activities.html.
- [ ] Back-publish remaining ~15 news items from the old WordPress site (28 total, 13 done).
- [ ] Add photos to news pages when available (graphical abstracts, event photos).
- [ ] `digital-pamphlet-fy2024.html` article page still needs to be created (card exists, page missing).

---

Verification update 2026-05-24T16:03:30: homepage, Japanese page, 2026 cohort page, and sample 2026 profile opened locally. Missing local references fixed except intentional external links/placeholders.

Web extraction update 2026-05-24T16:24:16
- Scraped public English Q-PIT cohort sections.
- Downloaded public portrait images into assets/photos/2021-2025.
- Generated detail pages for public HTML profile pages in 2021-2024.
- Preserved 2025 public PDF profile links and portrait cards.
- Saved extracted data to data/public_site_extracted.json.

Style update 2026-05-24
- Generated 2026-style individual profile pages for all public cohorts 2021–2025 using `scripts_generate_2026_style_profiles.py`.
- Added individual 2025 student pages that preserve original PDF links.
- Updated 2025 cohort cards to point to local individual pages.
- Verified 71 linked individual profile pages use the 2026-style topbar/research layout.
- Verified 84 HTML files have 0 missing local references.
- Browser spot checks: `students/2024/shen-siyu.html` and `students/2025/zhang-jingxuan.html`; no console errors.

Landing remake handoff
- Main file changed: `index.html`.
- Styling added in `assets/css/main.css` under "Landing page: original public-page structure".
- Generator added: `scripts_build_landing_original_structure.py`.
- It uses `data/public_site_extracted.json`, `data/public_sections_extracted.json`, and `data/cohorts.json`.
- Current structure: recruitment → program videos → pamphlets → student grids 2026 to 2021.
- Summer-camp videos were removed from the main landing flow to match Roman's requested order: first two sections, then pamphlets, then student photos.
- Verification done: `/` opened locally, structure confirmed visually, browser console has no errors, local link check showed 0 missing refs.

Landing design revision 2026-05-24
- Roman clarified that the requested structure meant section order, not copying the old Q-PIT visual style.
- Reworked `index.html` through `scripts_build_landing_original_structure.py` with a modern hero, CTA buttons, polished cards, and cleaner typography.
- Removed fellowship introduction and fellow interview YouTube embeds from the landing page.
- Added only the Summer Camp 2024 YouTube video (`0SzLgqBV_yI`) in the program section.
- Added a main landing page language toggle button (`EN` / `日本語`) using `assets/js/main.js`; visible landing text switches Japanese/English.
- Styling is appended in `assets/css/main.css` under "Landing refresh: polished academic-program design, May 2026".
- Verification: served locally on port 8766, browser visual check confirmed modern top design, language toggle works, console has 0 JS errors, 84 HTML files have 0 missing local references, and landing checks confirm old two videos are absent and summer-camp video is present.

Summer camp video tabs update 2026-05-24
- Added four year tabs above the landing-page video thumbnail: 2025, 2024, 2023, 2022.
- Default selected year is 2025.
- Downloaded local thumbnails into `assets/video/summer-camp-2025.jpg`, `summer-camp-2024.jpg`, `summer-camp-2023.jpg`, `summer-camp-2022.jpg`.
- YouTube links used: 2025 `srLEu440lV8`, 2024 `0SzLgqBV_yI`, 2023 `qsMBEsDCcKI`, 2022 `N8owTZyTvgg`.
- Implemented switching in `assets/js/main.js`; verified each tab updates the thumbnail, caption, active state, and YouTube link. Browser console has 0 errors.

Admission hero image update 2026-05-24
- Added `assets/photos/admission.jpg` to the hero/admission section via `scripts_build_landing_original_structure.py`.
- Replaced the plain admissions text panel with a styled photo card and translucent admissions overlay.
- Added responsive CSS for `.admission-visual` and `.admission-card` in `assets/css/main.css`.
- Verification: local browser visual check confirms the photo is visible and styled well; console has 0 errors; 84 HTML files have 0 missing local references; `assets/photos/admission.jpg` exists and is referenced by `index.html`.

Uniform earlier-cohort profile update 2026-05-24T22:28:46+0900
- Updated `scripts_generate_2026_style_profiles.py` so cohorts 2021–2025 use the same 2026-style individual profile format.
- Each generated page now keeps uniform fields/sections for affiliation, major/department, supervisor, doctoral research, research achievements, profile metadata, and programme/institutional links.
- For 2021, 2024, and 2025 pages, a K2-SPRING research-topic section is included with a clear placeholder where data is not available yet.
- For 2022 and 2023 pages, the K2-SPRING topic section is intentionally omitted; pages start with Doctoral research as requested.
- Missing supervisor, major/department, 2025 PDF-only details, and achievements are kept as explicit placeholders rather than invented.
- Regenerated 58 expected detail pages: 2025=12, 2024=11, 2023=11, 2022=12, 2021=12.

2025 cohort content update 2026-05-27
- Scraped all 12 public HTML pages at `q-energy/ay-2025/[slug]/`.
- Created `scripts_update_2025_profiles.py` and ran it successfully.
- Updated all 12 `students/2025/` files: supervisor, department/affiliation, K2-SPRING topic + abstract (EN+JP where available), doctoral research title + abstract, research achievements (papers, conferences, awards).

2023 cohort bilingual content update 2026-05-27
- Scraped all 11 public pages at `fellow-2023-en/[slug]/`; also fetched Japanese variants.
- Created and ran `scripts_update_2023_profiles.py` successfully on 10 of 11 files.
- tianhui-fan.html in students/2023/ was erroneous (wrong cohort); deleted.

Q-ENERGY Fellowship branding fix 2026-05-27
- K2-SPRING only started from 2024; 2021/2022/2023 were Q-ENERGY Fellowship programme.
- Fixed eyebrow labels and removed K2-SPRING sections from 2021 pages.

2024 cohort content update 2026-05-27
- Updated all 11 `students/2024/` files: K2-SPRING topic + abstract filled.

Excel roster update 2026-05-28
- Updated JP display names, supervisor names + department (EN/JP), affiliations from official Excel.
- 59/62 files updated; 3 alias files synced.

2022 + 2021 cohort bilingual content update 2026-05-28
- JP research titles + abstracts set from public source pages.
- All "To be added" placeholders removed.

Bilingual supervisor names 2026-05-28
- All 41 unique supervisors now have EN + JP name in all 61 student pages (2021–2025).
- data/students.json regenerated with supervisor_name + supervisor_name_jp for all 70 active students.

Final state 2026-05-28
- 84 HTML files, 0 missing local references.
- 34 pages bilingual; 29 pages EN-only; 0 "To be added" titles.
