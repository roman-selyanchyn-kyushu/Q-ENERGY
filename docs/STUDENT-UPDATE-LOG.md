# Student Update Log

A running record of **student-submitted content updates** applied to profile pages, so we always know what has been processed (and never re-do or lose track of a request again).

**How to use:** every time you apply a student's revision request (new photo, research text, achievements, award, etc.), add a row to the top of the table. Mark the commit hash so it's traceable. Source files for requests live in `docs/student revision requests/` (local-only, not on GitHub).

**Status key:** ✅ done & pushed · 🟡 done locally, not pushed · ⏳ received, not yet applied

| Date | Student (cohort) | What was updated | Source | Commit | Status |
|---|---|---|---|---|---|
| 2026-06-11 | Kohei Minoda (2026) | Portrait photo added; K2-SPRING + PhD research rewritten — bilingual EN/JP titles & abstracts | `K2-spring_web_Minoda_Kohei.docx` + email | `d12a595` | ✅ |
| 2026-06-10 | Niki Nakagawa (2026) | Award added | — | `12a8540` | ✅ |
| 2026-06-10 | Kohei Sawada (2025) | K2 / PhD research topics + award | — | `12a8540` | ✅ |
| 2026-06-10 | Shih-Peng Chang (2026) | Doctoral research title + abstract | — | `bc90d70` | ✅ |
| 2026-06-09 | Weifeng Wang (2026) | Research achievements | `Research achievements-WANG.docx` | `024f83e` | ✅ |
| 2026-06-08 | 2023 cohort (9 students) | Portrait photos added | — | `2e102d8` | ✅ |
| 2026-06-01 | 2026 cohort | Initial photos added | — | `8ca58b0` | ✅ |

## Pending requests (received, not yet applied)

_None outstanding._

## Notes

- This log was first assembled on 2026-06-11 by backfilling from `git log -- students/`. Earlier bulk/structural changes (supervisor-name fixes, author-format normalization, layout fixes) are tracked in git history but are **not** student-submitted content, so they are intentionally omitted here.
- For the step-by-step procedure of applying an update, see [STUDENT-UPDATE-PROCEDURE.md](STUDENT-UPDATE-PROCEDURE.md).
