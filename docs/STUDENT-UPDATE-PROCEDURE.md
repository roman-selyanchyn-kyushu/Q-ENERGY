# How to update student information (Q-ENERGY site)

This is the practical, step-by-step procedure for applying student-submitted
corrections to the site. It is written so it works **even on a different
computer** — keep this file in the project (it syncs via Dropbox and GitHub).

> **Golden rule:** update **one student (or even one paper) at a time** and
> re-run the build scripts. Do **not** redo everything from scratch — the build
> scripts already aggregate all students automatically.

---

## 0. Where things live (how the site is wired)

- **Source of truth = the individual student HTML pages**
  `students/<year>/<slug>.html` (e.g. `students/2026/wang-w.html`).
  These are edited by hand. Everything else is generated from them.
- **Generated data (do NOT hand-edit):**
  - `data/students.json` — built by `scripts/extract_student_data.py`
  - `data/publications.json` + `data/publications-data.js` — built by
    `scripts/build_publications_json.py` (feeds `publications.html`)
- **Homepage paper count** is hard-coded in `index.html` (~line 519) and must be
  updated by hand when the total changes.
- **Hosting:** GitHub Pages. Push to `main` and the live site
  (https://roman-selyanchyn-kyushu.github.io/Q-ENERGY/) updates in ~1 minute.

> ⚠️ The `scripts/` folder is **gitignored** (local only). It travels with the
> **Dropbox** copy of the project, but a *fresh git clone from GitHub will not
> contain the scripts*. Always work from the Dropbox-synced folder, or copy the
> `scripts/` folder over first.

---

## 1. Procedure for a student update

1. **Read the student's email and attached file** to see exactly what they want
   (add/remove/reorder papers, conferences, awards, fix names, photo, etc.).
   - `.docx` files: `pandoc` may not be installed. Unpack with the docx tools
     and read `word/document.xml` (treat `<w:tab/>` as a separator).

2. **Edit that student's HTML page** (`students/<year>/<slug>.html`), in the
   achievements section. Match the existing markup:
   `.ach-group` → `.ach-label` (EN/JP spans) → `.ach-list` → `<li>` items,
   with `.ach-authors` around the student's own name, `&ldquo;…&rdquo;` title,
   `<em>journal</em>`, and the DOI `<a>` link.

3. **Re-run the two build scripts** from the project root:
   ```bash
   python3 scripts/extract_student_data.py        # rebuilds data/students.json
   python3 scripts/build_publications_json.py      # rebuilds publications data
   ```

4. **Update the homepage count** if the unique paper total changed:
   open `index.html` (~line 519) and set the number in all three places
   (`data-ja`, `data-en`, and the visible text). The correct number is
   `total_papers` from `data/publications.json`.

5. **Verify** in a browser:
   ```bash
   python3 -m http.server 8765
   # open http://localhost:8765/  and  /publications.html
   ```
   Check the student's page, the publications list, and that nothing looks broken.

6. **Commit and push** (commit the page + the regenerated data files; do NOT
   commit the student's raw `.docx` or anything under `scripts/`):
   ```bash
   git add students/<year>/<slug>.html data/students.json data/publications.json data/publications-data.js index.html
   git commit -m "Update <Name> ..."
   git push
   ```

---

## 2. Standing editorial conventions (decided with Roman, June 2026)

- **No `[peer-reviewed]` tags** in citations — the DOI link already signals a
  journal paper. Keep meaningful notes like `[co-first author]`, `[accepted]`,
  `[submitted]`.
- **Highlight the fellow's own name** in every paper/conference entry with
  `<span class="ach-authors">…</span>`. Award entries have no author name →
  leave them plain.
- **Author-name formatting on the publications page** is normalized
  automatically to `Surname I.` style at build time (see §3). On the individual
  student pages, author names may stay as the student wrote them.
- **Do NOT bulk-rewrite author lists by hand** — the normalizer handles it.
  Only fix obviously wrong things (e.g. ALL-CAPS surnames → Title Case if a page
  still has them).
- **Translate award names** to English and keep the original Japanese in
  parentheses, e.g. `Outstanding Master's Thesis Award (優秀修士論文賞)`.
- A `Patents` achievement group is mapped to the JSON `other` bucket — expected.

---

## 3. Automatic behaviours in `build_publications_json.py` (good to know)

The publications build does three clever things so you don't have to:

1. **Merges papers co-authored by two fellows** (same DOI): the paper appears
   once, credits **both** fellows, and highlights both names. So the headline
   count is *unique* papers, which can be lower than the raw per-page total.
2. **Normalizes author names** to `Surname I.,` form (semicolons → commas,
   full names → initials, `et al.` preserved, co-first-author `*` preserved).
3. **Re-highlights** each fellow accent-insensitively and in either name order,
   so compound/surname-first names work (Hidalgo-Jiménez, Narmandakh, Phua).

### When the normalizer guesses a surname wrong

For a few names the surname/given order is genuinely ambiguous and cannot be
detected automatically (e.g. `Wang Sheng`, or `Given, Surname` order). These are
hand-corrected via a small table near the top of
`scripts/build_publications_json.py`:

```python
MANUAL_AUTHOR_OVERRIDES = {
    "<exact plain author text from the citation>": "<correct Surname I., list>",
    ...
}
```

If a newly added paper shows a wrong author name on the publications page, add
one line to that table (key = the exact author text, value = the corrected
`Surname I.,` string), then re-run `build_publications_json.py`. That's a
~30-second fix — no need to touch anything else.

> **Tip:** when adding new papers, do a quick dry check after building: open
> `publications.html` and scan the new entry's author line. Catching a bad
> surname there is trivial; fixing it after it's been live is annoying.

---

## 4. Other scripts (run from project root)

| Task | Command |
|---|---|
| Added activity photos | `python3 scripts/compress_activity_photos.py` |
| Edited a student page | `python3 scripts/extract_student_data.py` |
| Added/changed papers | `python3 scripts/build_publications_json.py` |
| Added a whole new cohort | `python3 scripts/add_fellow_nav.py` |

See `scripts/README.md` for more detail on each.
