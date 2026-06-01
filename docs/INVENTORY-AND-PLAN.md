# Inventory and design plan — Q-PIT / Q-ENERGY student sub-site static remake

## Scope and sources inspected

Target output folder for the future prototype:

`/Users/romanselyanchyn/Library/CloudStorage/Dropbox/00-QPIT/Q-fellowship/QENERGY-STUDENT-SITE-REMAKE`

Inspected sources:

- Public English page: `https://q-pit.kyushu-u.ac.jp/fellow-ship-en/`
- Public Japanese page: `https://q-pit.kyushu-u.ac.jp/fellow-ship/`
- Local 2026 reference folder, read-only source: `2026-WEB-NEW-STUDENTS/web-pages/`
- Local protected reference folder noted but not modified: `2026-WEB-NEW-STUDENTS/FOR-HERMES/`

No public assets were downloaded during this inventory step.

## Public site structure to preserve

The current public sub-site is effectively a bilingual landing page plus linked detail/news/material pages.

### Top-level bilingual pages

- English: `https://q-pit.kyushu-u.ac.jp/fellow-ship-en/`
  - Title: `K2-SPRING, Q-ENERGY Innovator Unit`
- Japanese: `https://q-pit.kyushu-u.ac.jp/fellow-ship/`
  - Title: `九州大学 未来を拓く博士人財育成プログラム (K2-SPRING) グリーンイノベーションユニット`

### Main landing-page sections found on both public pages

- News / announcements
- Student recruitment / 学生募集
- About the program / プログラムについて
- Summer Camp 2025 / 夏合宿（2025年）
- Summer Camp 2024 / 夏合宿（2024年）
- Summer Camp 2023 / 夏合宿（2023年）
- Summer Camp 2022 / 夏合宿（2022年）
- Digital pamphlet / パンフレット
- Students in 2025 / 2025年ユニット生
- Students in 2024 / 2024年ユニット生
- Fellows in 2023 / 2023年フェロー
- Fellows in 2022 / 2022年フェロー
- Fellows in 2021 / 2021年フェロー

### Digital pamphlet links

Preserve as external links unless locally mirrored later:

- 2025: `https://q-pit.kyushu-u.ac.jp/e-book_2025/`
- 2024: `https://q-pit.kyushu-u.ac.jp/e-book_2024/`
- 2023: `https://q-pit.kyushu-u.ac.jp/e-book_2023/`
- 2022: `https://q-pit.kyushu-u.ac.jp/e-book/`

### Public image inventory observed

Important public visual assets visible from the existing pages:

- Q-PIT / Kyushu University site header/footer logos from the WordPress theme.
- Program hero image on English page: `Earth-Q-ENERGY.png`.
- Digital pamphlet banners:
  - `digital_book_bnr_2025.jpg`
  - `digital_book_bnr_2024.jpg`
  - `digital_book_bnr_2023.jpg`
  - `digital_book_bnr_2022.jpg`
- Cohort portraits:
  - 2025: 12 PNG portraits named `00-Jingxuan-ZHANG-R-new-230x300.png` through `11-Rika-IRIGUCHI-R-230x300.png` style.
  - 2024: 11 JPG portraits named `img_fellow_2024_*.jpg`.
  - 2023: 11 JPG portraits named `img_fellow_2023_*.jpg`.
  - 2022: 12 JPG portraits including `img_fellow_2022_*.jpg` and `Irfan.jpg`.
  - 2021: 12 JPG portraits named `img_fellow_2021_*.jpg`.

Recommendation: do not scrape/download all assets automatically at prototype start. First define local asset naming and permissions. For a local static mockup, link to the public image URLs or use placeholders; copy only approved assets later.

## Cohort inventory and links

### 2026 local reference cohort

Source: `2026-WEB-NEW-STUDENTS/web-pages/index.html` and individual static HTML pages.

Local pages already exist for 13 FY2026 students:

| Student | Page | Supervisor |
|---|---|---|
| Shih-Peng CHANG | `chang-s.html` | Prof. Masamichi KOHNO / 河野 正道 |
| Hao CHEN / 陳 昊 | `chen-h.html` | Prof. Haruichi KANAYA / 金谷 晴一 |
| Ziqi JIANG | `jiang-z.html` | Prof. Kyaw THU |
| Masaru KOTAJIMA / 古田島 勝 | `kotajima-m.html` | Prof. Koji NAKABAYASHI / 中林 康治 |
| Kohei MINODA / 簑田 康平 | `minoda-k.html` | Prof. Tomoaki UTSUNOMIYA / 宇都宮 智昭 |
| Takeshi MOCHIZUKI / 望月 建志 | `mochizuki-t.html` | Prof. Takahiko MIYAZAKI / 宮崎 隆彦 |
| Niki NAKAGAWA / 中川 和 | `nakagawa-n.html` | Prof. Motonori WATANABE / 渡邊 源規 |
| Shinnosuke OMOTO / 大元 紳ノ介 | `omoto-s.html` | Prof. Gen INOUE / 井上 元 |
| Haonan SUN | `sun-h.html` | Prof. Kazunari KATAYAMA / 片山 一成 |
| Weifeng WANG | `wang-w.html` | Prof. Zhenying WANG / 王 振英 |
| Shotaro YOSHIDA / 吉田 昇太郎 | `yoshida-s.html` | Prof. Susumu FUJII / 藤井 進 |
| Qingen ZHENG | `zheng-q.html` | Prof. Kosei YAMAUCHI / 山内 幸正 |
| Zeyu ZOU | `zou-z.html` | Prof. Hiroaki WATANABE / 渡邊 裕章 |

Notes from local index:

- All pages are marked done except `minoda-k.html`, which is marked pending.
- Local pages are bilingual standalone pages with an EN/JP toggle.
- Existing layout sections: topbar, hero, K2-SPRING research, doctoral research, research achievements, partner logos, footer.

Local 2026 assets available in `web-pages/assets/`:

- `logo-k2spring.png`
- `logo-k2spring.svg`
- `logo-qpit.png`
- `logo-qenergy.png`
- `logo-kyushu.png`
- Portraits currently present:
  - `chang_shih-peng.jpeg`
  - `wang_weifeng.jpeg`
- Expected portrait filenames documented in `assets/photos/README.md` for all 13 students.

### 2025 public cohort

Public page section: `Students in 2025` / `2025年ユニット生`.

Observed portraits/names from image filenames:

- Jingxuan ZHANG
- Chenyu YAN
- Takahiro YAMAGUCHI
- Ryosi/Ryoshi ODA (verify romanization)
- Xiazhe ZHAI
- Yuki NISHIMURA
- Qi SHI
- Kohei SAWADA
- Sheng WANG
- Nozomu GOTO
- Zhanyi XIANG
- Rika IRIGUCHI

### 2024 public cohort

Public page section: `Students in 2024` / `2024年ユニット生`.

Observed names:

- Xianzhe Yang / 楊 賢テツ
- Tomomi SHODA / 庄田朋申
- Kodai Matsumoto / 松本昂大
- Ryudai Ueno / 上野 竜大生
- SHEN Siyu
- Itsuki OYAMA / 小山 一輝
- Yuki NOGUCHI / 野口 湧喜
- Haomin FU
- ZHANG KAILI
- Yuki Tomita / 冨田 侑樹
- Shogo Nakamura / 中村 省吾

### 2023 public cohort

Public page section: `Fellows in 2023` / `2023年フェロー`.

Observed names:

- CHEN YUTONG / 陳 昱通
- Seiya Imada / 今田 青冶
- Yusuke Oga / 大賀 雄介
- Yuta Takaoka / 髙岡 祐太
- WEI XUESONG / イ セツショウ
- Kotaro Shinozaki / 篠崎 航太朗
- Hiroki Isogawa / 五十川 浩希
- Taisei Tomaru / 都丸 大晟
- Kentaro Wada / 和田 健太郎
- NARMANDAKH KHONGORZUL / ナルマンダフ ホンゴルゾル
- Go Yokuhou / 呉 翼峰

### 2022 public cohort

Public page section: `Fellows in 2022` / `2022年フェロー`.

Observed names:

- Sora Matsushima / 松嶋 そら
- Daisuke Yoshizawa / 吉澤 大佑
- Shinichi Takeno / 竹野 慎一
- Yixin Chen / 陳 伊新
- Zifei Nie
- Tatsuya Hamashima (JP page alt appears duplicated as Zifei Nie; verify)
- Park Hyun-Gyu (JP page alt appears duplicated as Zifei Nie; verify)
- HE QINGYI / 何 清怡
- Phua Yin Kan
- Ryoma Sato / 佐藤 稜真
- Jacqueline Andrea Hidalgo Jiménez
- Muhammad Irfan Maulana Kusdhany

### 2021 public cohort

Public page section: `Fellows in 2021` / `2021年フェロー`.

Observed names:

- Yulu Chen / 陳雨露
- Tianhui Fan
- Kento Komatsubara / 小松原 建人
- Toraharu Watanabe / 渡邊 虎春
- Timothee Redarce
- Daiki Nishimura / 西村大輝
- Keitaro Maeno / 前野 啓太郎
- Haruka Mitoma / 三苫 春香
- Sun Mingxu / 孫明旭
- Likhith Manjunatha
- Xiaofeng Shen / 沈小烽
- Masatoshi Tashima / 田島 正俊

## What to preserve in the remake

Content and information architecture:

- Bilingual EN/JP experience.
- Clear route back to program top pages and Q-PIT parent site.
- Recruitment and program overview sections.
- News/announcements list, but consider showing only recent/current items on the static homepage.
- Summer camp archive by year.
- Digital pamphlet links by year.
- Cohort sections by year, with cards for each student/fellow.
- Individual student detail pages for 2026 and future cohorts.
- Research-focused student profiles: K2-SPRING research, doctoral research, achievements.

Visual/design elements:

- Q-ENERGY / energy-transition identity: green/blue energy palette, clean academic look.
- Student portrait cards with consistent portrait ratio.
- Partner logo row: K2-SPRING, Q-PIT, Q-ENERGY, Kyushu University.
- Bilingual language toggle visible at top.
- Compact table/list option for internal checking, but public-facing design should be card-based.

Editorial rules from local 2026 guide:

- Do not guess Japanese readings or translations.
- Academic citations are not translated; only UI labels and prose sections switch language.
- Scholarships should not be included as “Other Achievements” unless explicitly awards/honours.
- Missing portraits should show a placeholder, not a broken image.

## Recommended static site structure

Recommended simple static structure for the prototype:

```text
QENERGY-STUDENT-SITE-REMAKE/
  index.html                 # language-aware landing page or English default
  ja/
    index.html               # Japanese landing page
  students/
    2026/
      index.html             # 2026 cohort grid
      chang-s.html
      chen-h.html
      ...
    2025/
      index.html             # public cohort grid, detail pages optional
    2024/
      index.html
    2023/
      index.html
    2022/
      index.html
    2021/
      index.html
  assets/
    css/
      main.css
    js/
      main.js                # minimal language toggle/filtering only if needed
    images/
      logos/
      portraits/
        2026/
        2025/
        2024/
        2023/
        2022/
        2021/
      events/
  data/
    cohorts.json             # canonical cohort/student metadata
    news.json                # optional, for generating static pages later
  docs/
    INVENTORY-AND-PLAN.md
```

Alternative if no build tooling is desired: keep plain HTML pages and shared CSS only. If repetition becomes hard to maintain, introduce a small generator later using JSON data plus templates.

## Proposed design direction

Homepage:

- Hero: “K2-SPRING / Q-ENERGY Innovator Unit” with short EN/JP program statement and CTA buttons to recruitment, program overview, and cohorts.
- Quick status cards: recruitment, program, pamphlet, latest news.
- Cohort browser: year tabs/cards for 2026, 2025, 2024, 2023, 2022, 2021.
- Event archive: summer camp cards by year with media links.
- Footer: parent Q-PIT links, Kyushu University links, contact.

Cohort pages:

- Year heading with program label: “Students in 2026” / “2026年ユニット生”.
- Responsive portrait card grid.
- Card fields: portrait, name EN/JP, affiliation, supervisor, research keyword/title, profile link.
- Add filters later only if metadata supports it: graduate school, topic, supervisor, nationality/language.

Student detail pages:

- Reuse local 2026 design, but extract shared CSS and navigation.
- Keep bilingual toggle and the existing fixed content order.
- Add breadcrumb: Home → Students → 2026 → Name.
- Add previous/next student navigation within cohort.
- Keep external supervisor/profile links where verified.

## Priority implementation plan

### Phase 1 — Static shell and information architecture

1. Create the static folder structure above.
2. Copy or adapt only approved local reference assets from `2026-WEB-NEW-STUDENTS/web-pages/assets/`.
3. Create `index.html`, `ja/index.html`, shared `assets/css/main.css`.
4. Add homepage sections matching the public page inventory.
5. Add placeholder cohort grids for 2021–2026.

### Phase 2 — 2026 cohort integration

1. Use `web-pages/index.html` as the source roster.
2. Bring in the 13 existing 2026 student pages or convert them into the new structure.
3. Normalize shared CSS and logo paths.
4. Check `minoda-k.html` pending status and either complete or mark clearly as pending.
5. Add missing portrait placeholders and document missing portrait files.

### Phase 3 — Public archive cohorts

1. Build cohort JSON/data entries for 2021–2025 from public pages.
2. Use public portrait URLs as temporary external references or download only after permission/approval.
3. Preserve external pamphlet links.
4. Add detail pages only where source content exists; otherwise link cards to public Q-PIT pages or keep cards non-clickable.

### Phase 4 — Content QA and bilingual polish

1. Verify every name and Japanese spelling against source pages or staff-provided lists.
2. Verify all supervisor links and student research titles before publishing.
3. Check mobile layout, portrait fallback, and language toggle behavior.
4. Run link checking for external URLs.
5. Prepare a short editorial workflow for adding future cohorts.

## Open issues / items needing confirmation

- Whether the remake should be only a local prototype or eventually replace/augment the WordPress public pages.
- Whether public Q-PIT images may be copied locally, or should remain externally linked in the prototype.
- Whether 2021–2025 cohorts need individual static detail pages or only cohort cards.
- Correct romanization for “Ryosi/Ryoshi ODA”.
- JP alt/name duplication observed on public Japanese page for two 2022 portraits should be verified.
- Whether the 2026 local pages should remain standalone files or be generated from a single data source.
