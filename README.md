# Q-ENERGY Student Site Remake

Local static prototype for Roman Selyanchyn / Q-PIT.

Preview locally:

```bash
cd "/Users/romanselyanchyn/Library/CloudStorage/Dropbox/00-QPIT/Q-fellowship/QENERGY-STUDENT-SITE-REMAKE"
python3 -m http.server 8765
```

Then open: http://localhost:8765/

Main files:
- `index.html` — English prototype top page
- `ja/index.html` — Japanese prototype top page
- `students/2026/` — copied local FY2026 student pages and assets
- `students/2021`–`students/2025` — prototype cohort card pages
- `assets/css/main.css` — shared prototype styling
- `docs/INVENTORY-AND-PLAN.md` — source inventory and implementation plan

Safety:
- The live Q-PIT website was not modified.
- The original `FOR-HERMES` reference folder was not modified; files were only copied into this prototype.

Current limitations:
- 2021–2025 detail pages are not fully converted yet.
- Some romanizations/Japanese names require confirmation.
- Public images are not bulk-downloaded yet; placeholders/cards are used for older cohorts.
