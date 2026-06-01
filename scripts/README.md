# Scripts — Q-ENERGY Student Site

All scripts are run from the **project root folder** (not from inside `scripts/`).

---

## How to open Terminal at the project root

1. Open **Terminal** (Applications → Utilities → Terminal)
2. Type `cd ` (with a space), then drag the project folder into the Terminal window and press Enter
3. You are now in the project root — run any script below

---

## Active scripts

These are the scripts you will use regularly.

---

### 1. `compress_activity_photos.py`

**When to run:** every time you add new photos to the activities folders.

**What it does:**
- Scans `assets/photos/activities/*/` for any image files (JPG, PNG, HEIC, etc.)
- Resizes them to max 1200px wide
- Saves as JPG at quality 82% (typically 80–250 KB per photo)
- Renames files to `01.jpg`, `02.jpg`, etc. in alphabetical order
- Saves the originals safely in an `_originals/` subfolder inside each activity folder

**Where to put photos:**
```
assets/photos/activities/
  seminars/              ← Joint Seminars photos
  company-visit/         ← Company Visit photos
  energy-week/           ← Kyushu Energy Week photos
  decarbonization-workshop/  ← Decarbonization Workshop photos
  summer-camp/           ← Summer Camp photos
```
Name your files anything — the script will rename them automatically.

**How to run:**
```
python3 scripts/compress_activity_photos.py
```

**Requires:** `Pillow` — install once with: `pip3 install Pillow --break-system-packages`

---

### 2. `build_publications_json.py`

**When to run:** every time you add or change paper entries in any student HTML page.

**What it does:**
- Reads all 71 student HTML pages
- Extracts every paper from the Research Papers section
- Sorts all papers by publication year (newest first)
- Writes two output files:
  - `data/publications.json` — used when the site is served over HTTP
  - `data/publications-data.js` — used when the site is opened directly as a file (no server needed)

The `publications.html` achievements page uses these files automatically.

**How to run:**
```
python3 scripts/build_publications_json.py
```

**No extra packages required.**

---

### 3. `extract_student_data.py`

**When to run:** after editing any student HTML page — to keep `data/students.json` in sync.

**What it does:**
- Reads all 71 student HTML pages
- Extracts names, affiliations, supervisors, research topics, and achievements
- Writes `data/students.json` — the central database used across the site

**How to run:**
```
python3 scripts/extract_student_data.py
```

**No extra packages required.**

---

### 4. `add_fellow_nav.py`

**When to run:** when a new cohort of students is added (e.g. a 2027 cohort), or if the fellow navigator (‹ ⊞ N/71 ›) in the student page topbar needs updating.

**What it does:**
- Injects or updates the `‹ ⊞ N/71 ›` fellow navigator into the topbar of every student page
- The centre button (grid icon) links back to `index.html#students`
- Keeps the total count (currently 71) up to date

**How to run:**
```
python3 scripts/add_fellow_nav.py
```

**No extra packages required.**

---

## Archive scripts

The `archive/` folder contains **one-time migration scripts** that have already been run. You do not need to run these again. They are kept for reference — if you ever need to understand how the site was originally built, or need to adapt a script for a new cohort, you can find the original code here.

---

## Quick reference

| Task | Script |
|---|---|
| Added activity photos | `python3 scripts/compress_activity_photos.py` |
| Added/changed papers in student pages | `python3 scripts/build_publications_json.py` |
| Edited a student HTML page | `python3 scripts/extract_student_data.py` |
| Added a new cohort of students | `python3 scripts/add_fellow_nav.py` |
