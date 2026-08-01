# Q-ENERGY Innovator Unit — Student Site

Bilingual (Japanese / English) website introducing the fellowship students of the
**Q-ENERGY Innovator Unit / K2-SPRING** programme at Q-PIT, Kyushu University.

Each profile presents the student's research focus, supervisor, affiliation, and
achievements. The site covers six cohorts, 2021–2026.

**Programmes:** 2021–2023 — Q-ENERGY Fellowship; 2024–2026 — K2-SPRING / Q-ENERGY Innovator Unit.

## Contents

| Page | |
|---|---|
| `index.html` | Landing page — photo grid of all students |
| `students/` | Individual student profiles, by cohort |
| `activities.html` | Programme activities |
| `publications.html` | Publications by the fellows |
| `news.html`, `news/` | Programme news |

## Languages

Japanese and English are served from the same pages, switched by an in-page toggle — there
are no separate `/ja/` URLs. Your choice is remembered in the browser.

## Viewing locally

The site is plain HTML, CSS, and JavaScript with relative paths. From the repository root:

```bash
python3 -m http.server 8765
```

Then open <http://localhost:8765/>.

---

Q-PIT — Kyushu University Platform of Inter-/Transdisciplinary Energy Research.
