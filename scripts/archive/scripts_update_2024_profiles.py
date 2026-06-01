#!/usr/bin/env python3
"""
Fill 2024 student profile pages with real content.

For 2024, the doctoral research section was already scraped from the old
fellow-ship-en/ pages by Hermes. This script:
  1. Fills the K2-SPRING section (§01) — same topic as doctoral research.
  2. Updates all source URLs from fellow-ship-en/ to fellow-2024-en/.

Run from project root:
    python3 scripts_update_2024_profiles.py
"""

import re
from pathlib import Path

BASE   = Path(__file__).parent
DIR_24 = BASE / "students" / "2024"

# ── student data ──────────────────────────────────────────────────────────────
# source_url_old  : old link already embedded in the HTML
# source_url_new  : correct updated link

STUDENTS = {
    "xianzhe-yang": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/xianzhe-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/xianzhe-en/",
        "k2spring_en": "Research on the digital twin of building thermal environment utilizing digital transformation technology",
        "abstract_en": (
            "Achieving carbon neutrality by 2050 requires significant efforts in urban and "
            "architectural sectors, particularly in accelerating energy efficiency in residential "
            "and commercial buildings. This study aims to develop general-purpose software that "
            "realises a digital twin of thermal environments using Digital Transformation (DX) "
            "technology, focusing on two main objectives: development of a building energy "
            "simulation (BES) engine with detailed mathematical models and Computational Fluid "
            "Dynamics (CFD) coupling; and integration of the BES tool with architectural design "
            "platforms."
        ),
    },
    "tomomi-shoda": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/shoda-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/shoda-en/",
        "k2spring_en": "CO₂ Reduction Potential of Global Supply Chain Networks: An MRIO Approach Incorporating Maritime Network Structures",
        "abstract_en": (
            "This research focuses on the CO₂ reduction potential of global supply chain (GSC) "
            "restructuring while considering the environmental efficiency of international shipping. "
            "Some 23% of global CO₂ emissions are embodied in traded goods through GSCs. "
            "Multi-Regional Input–Output (MRIO) tables — among the most effective tools for "
            "analysing GSCs — do not currently capture transportation system data. "
            "This study proposes a new MRIO framework that incorporates maritime network "
            "structures to estimate the CO₂ reduction potential of supply chain reorganisation."
        ),
    },
    "kodai-matsumoto": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/matsumoto-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/matsumoto-en/",
        "k2spring_en": "Development of Three-Dimensional Chiral Plasmonic Meta-clusters with Circular Polarization Characteristics for Effective Utilization of Sunlight",
        "abstract_en": (
            "Circular polarisation has potential applications in improving the efficiency of solar "
            "cells and promoting plant growth. This research develops high-performance dichroic "
            "circular polarisers (DCP) and meta-surfaces to enhance circular polarised "
            "photoluminescence (CPL) of chiral chromophores. Three-dimensional helical chiral "
            "plasmonic meta-clusters are fabricated by rolling up 2D plasmonic arrays in an "
            "origami-like process, demonstrating DCP behaviour and CPL enhancement through "
            "unique electromagnetic properties of asymmetric plasmonic nanostructures."
        ),
    },
    "ryudai-ueno": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/ueno-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/ueno-en/",
        "k2spring_en": "Prediction of Future Afforestation Sites and Sustainable Forest Management in Kyushu",
        "abstract_en": (
            "Forests serve as a crucial carbon sink. In order to implement afforestation aimed at "
            "increasing carbon sequestration and to achieve sustainable forest management, it is "
            "essential to consider the impacts of climate change and population decline on forest "
            "management. This study predicts suitable areas for afforestation in the latter half "
            "of the 21st century, taking into account changes in temperature, precipitation, and "
            "population dynamics."
        ),
    },
    "shen-siyu": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/shen-siyu-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/shen-siyu-en/",
        "k2spring_en": "Environmental-economic trade-offs of membrane-based direct air capture technologies using life cycle assessment",
        "abstract_en": (
            "Climate change is primarily driven by CO₂ emissions. Achieving the Paris Agreement's "
            "target of limiting global warming to 1.5 °C requires not only reducing current "
            "emissions but also removing existing CO₂ from the atmosphere. This study explores "
            "the potential of Direct Air Capture combined with utilisation (DAC-U) at a household "
            "scale. Using Life Cycle Assessment (LCA), the research evaluates the environmental "
            "and economic feasibility of a small-scale DAC-U system that converts CO₂ into "
            "household fuel and generates carbon credits. If environmentally and economically "
            "viable, decentralised DAC-U units could provide a socially acceptable means for "
            "households to contribute to carbon neutrality."
        ),
    },
    "itsuki-oyama": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/oyama-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/oyama-en/",
        "k2spring_en": "Optimizing heat sink design in nuclear fusion reactors using topology optimisation",
        "abstract_en": (
            "Plasma-facing components (PFCs) are exposed to extreme heat loads inside a fusion "
            "reactor. In a fast-breeder reactor, reduced-activation ferritic steel (RAFS) is used "
            "around cooling systems inside PFCs, making heat sink design with consideration of "
            "RAFS thermal conductivity particularly important. This study applies topology "
            "optimisation to design an effective heat sink geometry inside the reactor, with the "
            "goal of maximising heat removal performance under fusion-relevant operating conditions."
        ),
    },
    "yuki-noguchi": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/noguchi-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/noguchi-en/",
        "k2spring_en": "Study of F82H precipitate amorphisation in a DEMO fusion reactor",
        "abstract_en": (
            "Fusion reactors are expected to be the next-generation power sources. In the "
            "conceptual design of the domestic DEMO reactor, Reduced Activation "
            "Ferritic/Martensitic Steel (F82H) is the primary candidate material for the "
            "blanket first wall. One of the precipitates in F82H — the Cr₂₃₋ₓWₓC₆ system — "
            "has been confirmed to undergo amorphisation under Fe³⁺ ion irradiation at "
            "temperatures relevant to fusion reactor operation, raising concerns regarding "
            "material degradation. This study aims to elucidate the structural changes leading "
            "to amorphisation using first-principles calculations and molecular dynamics "
            "simulation."
        ),
    },
    "haomin-fu": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/haomin-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/haomin-en/",
        "k2spring_en": "The Changing Landscape of EV Business Ecosystem: A Downstream Value Chain Analysis",
        "abstract_en": (
            "This research explores the evolving electric vehicle (EV) business ecosystem, with a "
            "focus on downstream value chain activities such as charging infrastructure, after-sales "
            "services, and mobility solutions. Unlike traditional vehicles, EVs require new digital "
            "and service-oriented capabilities that enable continuous value creation beyond the "
            "point of sale. Through a multi-case study approach, the study examines how legacy "
            "automakers, start-ups, and cross-industry entrants are reconfiguring strategies to "
            "meet changing consumer needs. The research analyses how these actors build ecosystem "
            "partnerships, manage customer engagement, and innovate in areas like battery services "
            "and platform-based mobility — providing both theoretical insights into capability "
            "transformation under technological disruption and practical guidance for building "
            "competitive, sustainable business models in the EV era."
        ),
    },
    "zhang-kaili": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/zhang-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/zhang-en/",
        "k2spring_en": "The impact mechanism of multi-scale urban built environment on health and well-being of residents",
        "abstract_en": (
            "From an interdisciplinary perspective, this study utilises multivariate data — "
            "including remote sensing imagery, street view images, vector data, and house prices — "
            "to identify the impact mechanisms of the built environment on public health outcomes "
            "(physical, mental, and social health). Machine-learning statistical models including "
            "Geographically Weighted Regression, Random Forest, and Latent Growth Curve Modelling "
            "are applied at three different scales: city, block, and community. The multi-scale "
            "analysis provides quantitative guidance for health-promoting urban planning and design."
        ),
    },
    "yuki-tomita": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/tomita-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/tomita-en/",
        "k2spring_en": "Highly Efficient Ammonia Oxidation by a Macrocyclic Molecular Catalyst",
        "abstract_en": (
            "Ammonia has attracted much attention as a new energy carrier. However, efficient "
            "catalytic ammonia oxidation to nitrogen has not been well developed, because it "
            "involves a challenging six-electron oxidation reaction. Macrocyclic metal complexes "
            "such as porphyrins and phthalocyanines have been reported as water oxidation "
            "catalysts — which involve a four-electron process — and operate via a bimolecular "
            "mechanism. This bimolecular mechanism is important for promoting ammonia oxidation "
            "efficiently, since only a three-electron oxidation of the catalyst is required. "
            "This study aims to achieve highly efficient ammonia oxidation using a novel "
            "macrocyclic molecular catalyst."
        ),
    },
    "shogo-nakamura": {
        "source_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/nakamura-en",
        "source_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2024-en/nakamura-en/",
        "k2spring_en": "Design and Evaluation of PtW-Based Catalysts for Enhancing Fuel Starvation Tolerance in PEFCs",
        "abstract_en": (
            "Polymer electrolyte fuel cells (PEFCs) have attracted attention as a core technology "
            "for utilising renewable energy and achieving a zero-emission society. This study "
            "focuses on fuel starvation at the anode, one of the major degradation factors in "
            "PEFCs. When hydrogen supply is temporarily interrupted, the anode potential rises "
            "sharply, leading to irreversible degradation such as carbon support corrosion and "
            "platinum catalyst dissolution. These phenomena significantly reduce cell performance "
            "and hinder long-term operation. The research aims to design and evaluate PtW-based "
            "catalysts with enhanced tolerance to fuel starvation conditions."
        ),
    },
}


# ── placeholder text present in every generated 2024 file ────────────────────

OLD_K2 = (
    '    <div class="research-banner">\n'
    '      <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">'
    '<path d="M6 0l1.5 4.5L12 6 7.5 7.5 6 12 4.5 7.5 0 6l4.5-1.5z"/></svg>\n'
    '      <span data-lang-en="">K2-SPRING topic &middot; Pending details</span>\n'
    '      <span data-lang-jp="">K2-SPRINGテーマ &middot; 追記予定</span>\n'
    '    </div>\n'
    '    <h3 class="research-title" data-lang-en="">To be added</h3>\n'
    '    <h3 class="research-title" data-lang-jp="">追記予定</h3>\n'
    '    <div class="research-abstract" data-lang-en="">'
    '<p class="ach-soon">K2-SPRING topic information is not available in the current public data. '
    'It will be added after Roman provides it.</p></div>\n'
    '    <div class="research-abstract" data-lang-jp="">'
    '<p class="ach-soon">K2-SPRING研究テーマは現在の公開データには含まれていません。情報提供後に追記します。</p></div>'
)


def update_file(slug, d):
    path = DIR_24 / f"{slug}.html"
    if not path.exists():
        print(f"  SKIP  {slug}.html — file not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html

    # 1. K2-SPRING section ────────────────────────────────────────────────────
    new_k2 = (
        '    <div class="research-banner">\n'
        '      <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">'
        '<path d="M6 0l1.5 4.5L12 6 7.5 7.5 6 12 4.5 7.5 0 6l4.5-1.5z"/></svg>\n'
        '      <span data-lang-en="">K2-SPRING topic &middot; 2024</span>\n'
        '      <span data-lang-jp="">K2-SPRINGテーマ &middot; 2024年度</span>\n'
        '    </div>\n'
        f'    <h3 class="research-title" data-lang-en="">{d["k2spring_en"]}</h3>\n'
        f'    <h3 class="research-title" data-lang-jp="">{d["k2spring_en"]}</h3>\n'
        f'    <div class="research-abstract" data-lang-en=""><p>{d["abstract_en"]}</p></div>\n'
        f'    <div class="research-abstract" data-lang-jp=""><p>{d["abstract_en"]}</p></div>'
    )
    html = html.replace(OLD_K2, new_k2, 1)

    # 2. Source URL — PhD card source-actions link ────────────────────────────
    html = html.replace(
        f'href="{d["source_url_old"]}"',
        f'href="{d["source_url_new"]}"'
    )
    # Also update any trailing-slash-less variant
    html = html.replace(
        f'href="{d["source_url_old"]}/"',
        f'href="{d["source_url_new"]}"'
    )

    # 3. Metadata card source URL ─────────────────────────────────────────────
    # (covered by the href replacement above since source_url_old appears there too)

    if html == original:
        print(f"  WARN  {slug}.html — no changes made (check placeholder strings)")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  OK    {slug}.html")


def main():
    print(f"Updating {len(STUDENTS)} files in {DIR_24}\n")
    for slug, d in STUDENTS.items():
        update_file(slug, d)
    print("\nDone.")


if __name__ == "__main__":
    main()
