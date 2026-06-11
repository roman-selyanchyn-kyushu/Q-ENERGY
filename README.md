# Q-ENERGY Innovator Unit — Student Site

Bilingual (Japanese / English) static website profiling the fellowship students of the
**Q-ENERGY Innovator Unit / K2-SPRING** programme at Q-PIT, Kyushu University. Each profile
presents the student's research focus, supervisor, affiliation, and achievements, across
six cohorts (2021–2026).

Pure HTML/CSS/JS — no build step, no framework, all paths relative. Published via GitHub Pages.

**Programmes:** 2021–2023 = Q-ENERGY Fellowship; 2024–2026 = K2-SPRING / Q-ENERGY Innovator Unit.

## Preview locally

From the repository root:

```bash
python3 -m http.server 8765
```

Then open <http://localhost:8765/>.

## Structure

| Path | What it is |
|---|---|
| `index.html` | Landing page (photo grid of all students, with JP/EN toggle) |
| `students/2021`–`students/2026/` | Individual student profile pages — 71 students across six cohorts |
| `activities.html` | Programme activities (photo sliders) |
| `publications.html` | Aggregated publications list |
| `news.html`, `news/` | News index + individual article pages |
| `assets/css/main.css` | Landing-page styles (student pages are self-contained) |
| `assets/js/main.js` | Landing-page language toggle + video switcher |
| `assets/logos/`, `assets/photos/` | Logos and web-sized portraits |
| `data/` | `students.json`, `news.json`, etc. |

**Bilingual mechanism:** an in-page toggle (no separate `/ja/` pages). Student pages swap
`data-lang-en` / `data-lang-jp` elements via CSS; the landing page swaps `data-en` / `data-ja`
text in JS. Preference is stored in `localStorage` (`k2spring_lang`).
