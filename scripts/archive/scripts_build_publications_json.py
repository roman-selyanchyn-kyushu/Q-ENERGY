#!/usr/bin/env python3
"""
Build data/publications.json — a flat, year-sorted list of all journal papers
across all 71 student pages. Used by publications.html.

Run from project root:
    python3 scripts_build_publications_json.py
"""

import json
import re
from datetime import date
from pathlib import Path

BASE      = Path(__file__).parent
STUDENTS  = BASE / "students"
JSON_PATH = BASE / "data" / "students.json"
OUT_PATH  = BASE / "data" / "publications.json"

COHORT_DIRS = ["2021", "2022", "2023", "2024", "2025", "2026"]


def extract_papers_ol(html):
    """Return the inner content of the Research Papers <ol>, or '' if none/empty."""
    m = re.search(
        r'<div class="ach-label"><span data-lang-en="">Research Papers</span>.*?'
        r'<ol class="ach-list">(.*?)</ol>',
        html, re.DOTALL
    )
    if not m:
        return ""
    inner = m.group(1)
    return "" if "ach-soon" in inner else inner


def extract_li_items(ol_inner):
    """Split ol inner HTML into individual <li> content strings."""
    return re.findall(r"<li>(.*?)</li>", ol_inner, re.DOTALL)


def extract_year(li_html):
    """Extract 4-digit publication year from a paper <li> element."""
    text = re.sub(r"<[^>]+>", " ", li_html)
    # Primary: year in parentheses like (2025) or (2025/06)
    matches = re.findall(r"\((\d{4})(?:/\d+)?\)", text)
    if matches:
        return int(matches[-1])
    # Fallback: any 20xx year near end of text
    matches = re.findall(r"\b(20\d{2})\b", text)
    if matches:
        return int(matches[-1])
    return 0


def extract_doi(li_html):
    m = re.search(r'href="(https://doi\.org/[^"]+)"', li_html)
    if not m:
        return ""
    doi = m.group(1)
    return "" if "not yet" in doi or "未定" in doi else doi


def plain_text(li_html):
    """Strip all HTML tags for title/journal extraction."""
    return re.sub(r"<[^>]+>", "", li_html).replace("&ldquo;", "“").replace(
        "&rdquo;", "”").replace("&ndash;", "–").replace(
        "&thinsp;", " ").replace("&ensp;", " ").strip()


def load_student_meta():
    """Return dict: slug → {name_en, name_jp, cohort, programme, path}."""
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    meta = {}
    for s in data["students"]:
        meta[s["slug"]] = {
            "name_en":   s.get("name_en", ""),
            "name_jp":   s.get("name_jp", ""),
            "cohort":    s.get("cohort", 0),
            "programme": s.get("programme", ""),
        }
    return meta


def main():
    meta    = load_student_meta()
    entries = []
    skipped = []

    for cohort_dir in COHORT_DIRS:
        for html_path in sorted((STUDENTS / cohort_dir).glob("*.html")):
            slug = html_path.stem

            # Skip cohort index pages
            if slug == "index":
                continue
            # Skip alias files — these duplicate their primary; primaries are in students.json
            # Primary slugs (in JSON): mingxu-sun, hyun-gyu-park, yin-kan-phua, qingyi-he
            # Alias slugs (HTML only):  sun-mingxu, park-hyun-gyu, phua-yin-kan, he-qingyi
            ALIAS_SLUGS = {
                "sun-mingxu", "park-hyun-gyu", "phua-yin-kan", "he-qingyi"
            }
            if slug in ALIAS_SLUGS:
                continue

            student = meta.get(slug)
            if not student:
                print(f"  WARN  {slug} — not in students.json, skipping")
                continue

            html   = html_path.read_text(encoding="utf-8")
            ol_inner = extract_papers_ol(html)
            if not ol_inner:
                skipped.append(slug)
                continue

            lis = extract_li_items(ol_inner)
            for li_html in lis:
                year = extract_year(li_html)
                doi  = extract_doi(li_html)
                entries.append({
                    "year":         year,
                    "html":         li_html.strip(),
                    "doi":          doi,
                    "student_slug": slug,
                    "student_name": student["name_en"],
                    "student_name_jp": student["name_jp"],
                    "cohort":       student["cohort"],
                    "programme":    student["programme"],
                })

    # Sort: newest year first, then by cohort (older fellows first within same year)
    entries.sort(key=lambda e: (-e["year"], e["cohort"], e["student_name"]))

    # Year distribution for stats
    from collections import Counter
    year_counts = Counter(e["year"] for e in entries)

    output = {
        "generated":    str(date.today()),
        "total_papers": len(entries),
        "years":        sorted(year_counts.keys(), reverse=True),
        "year_counts":  {str(k): v for k, v in sorted(year_counts.items(), reverse=True)},
        "papers":       entries,
    }

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Also write a JS file so publications.html works via file:// without a server
    js_path = BASE / "data" / "publications-data.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated by scripts_build_publications_json.py — do not edit manually\n")
        f.write("window.PUBLICATIONS_DATA = ")
        json.dump(output, f, ensure_ascii=False)
        f.write(";\n")

    print(f"Written {OUT_PATH}")
    print(f"Written {js_path}")
    print(f"  {len(entries)} papers across {len(set(e['student_slug'] for e in entries))} students")
    print(f"  Year distribution: {dict(sorted(year_counts.items(), reverse=True))}")
    if skipped:
        print(f"  No papers (Coming soon): {', '.join(skipped)}")


if __name__ == "__main__":
    main()
