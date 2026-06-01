#!/usr/bin/env python3
"""
Fill 2025 student profile pages with real content scraped from
https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/  pages.

Run from the project root:
    python3 scripts_update_2025_profiles.py
"""

import re
from pathlib import Path

BASE   = Path(__file__).parent
DIR_25 = BASE / "students" / "2025"

# ── student data (sourced May 2026 from public q-pit pages) ──────────────────

STUDENTS = {
    "zhang-jingxuan": {
        "affiliation":  "Graduate School of Economics, Kyushu University",
        "department":   "Economic Systems (経済システム専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/zhang-j/",
        "k2spring_en":  "Decarbonizing Compact Cities: Strategic Planning for AEV-Based Public Transport",
        "abstract_en":  (
            "This study identifies optimal alternative energy vehicle (AEV) proportions "
            "in compact cities using LEAP modelling to simulate energy consumption and carbon "
            "emissions across multiple penetration scenarios, aiming to inform sustainable "
            "transportation policy for decarbonizing urban mobility systems."
        ),
        "papers": [
            'Zhang Jingxuan and Andrew Chapman, "Toward Sustainable Mobility: A Review of the '
            'Socio-Economic and Environmental Feasibility of Hydrogen Fuel Cell Bus Deployment," '
            '<em>International Journal of Hydrogen Energy</em> (2025, submitted).',
            'Zhang Jingxuan et al., paper on polyoxymethylene upcycling, '
            '<em>Green Chemistry</em> (2026, accepted).',
        ],
        "conferences": [
            "Poster: hydrogen fuel cell bus deployment, GREENIE 2025, Taiwan.",
            "Poster: hydrogen fuel cell bus deployment, EcoDesign 2025, Tokyo.",
        ],
        "awards": [],
    },

    "yan-chenyu": {
        "affiliation":  "Graduate School of Integrated Science and Engineering, Kyushu University",
        "department":   "Integrated Science and Engineering (総合理工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/yan-c/",
        "k2spring_en":  "Microwave-assisted catalytic degradation of plastics and other organic wastes",
        "abstract_en":  (
            "This research addresses plastic pollution by developing microwave-assisted degradation "
            "processes. Microwave heating enables rapid and uniform energy delivery, enhancing "
            "degradation efficiency while reducing overall energy consumption. The study selects "
            "inorganic catalysts with superior microwave absorption performance for effective "
            "organic waste treatment."
        ),
        "papers": [
            'Chenyu Yan et al., "Morphology and Defect Engineering of MoS₂ for Enhanced '
            'Microwave Heating: Superior Performance of Nanoflower Architecture," '
            '<em>The Journal of Physical Chemistry C</em> (2026, accepted).',
        ],
        "conferences": [],
        "awards": [],
    },

    "takahiro-yamaguchi": {
        "name_jp":      "山口 貴大",   # 山口 貴大
        "affiliation":  "Graduate School of Integrated Science and Engineering, Kyushu University",
        "department":   "Integrated Science and Engineering (総合理工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/yamaguchi-t/",
        "k2spring_en":  "Application of machine learning for real-time control of tokamak plasma configuration",
        "k2spring_jp":  "トカマクプラズマ配位の実時間制御のための機械学習の活用",
        "abstract_en":  (
            "This research applies machine learning techniques from image processing to achieve "
            "real-time plasma shape prediction in tokamak fusion devices. Predicting plasma "
            "configuration from high-speed camera images enables early detection of instabilities "
            "and collapse events, supporting stable steady-state operation of fusion reactors."
        ),
        "abstract_jp":  (
            "高速カメラによるプラズマ画像"
            "から形状をリアルタイムで予測"
            "することで、プラズマの崩壊や"
            "不安定性を回避し、核融合装置"
            "の定常運転を支援することを目"
            "指す研究です。"
        ),
        "papers": [],
        "conferences": [
            "Kyushu University Energy Week 2026, poster presentation (2026/01/26).",
        ],
        "awards": [
            "Excellence Poster Award, Kyushu University Energy Week 2026 (2026/01/26).",
        ],
    },

    "ryoshi-oda": {
        "name_jp":      "小田 亮志",   # 小田 亮志
        "affiliation":  "Interdisciplinary Graduate School of Engineering Sciences, Kyushu University",
        "department":   "Engineering Sciences (総合理工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/oda-r/",
        "k2spring_en":  "Research on turquoise hydrogen synthesis using carbon-based catalysts and effective utilisation of byproduct carbon",
        "k2spring_jp":  "炭素系触媒を用いたターコイズ水素の合成および副生炭素の有効利用に関する研究",
        "abstract_en":  (
            "This study develops clean hydrogen production through methane pyrolysis using "
            "carbon-based catalysts, yielding turquoise hydrogen with no CO₂ emissions. "
            "The solid carbon byproducts are further converted into high-value materials such "
            "as battery electrodes and carbon fibre, maximising the resource value of the process."
        ),
        "abstract_jp":  (
            "炭素系触媒を用いたメタン熱分"
            "解によりCO₂を排出しないターコ"
            "イズ水素を合成し、副生する固"
            "体炭素をバッテリー電極材料や"
            "炭素繊維などの高付加価値材料"
            "に転換することで、プロセス全"
            "体の資源価値を最大化する研究です。"
        ),
        "papers": [
            'Hatakeyama et al. (incl. Ryoshi Oda), "Exploring the frontiers of Li–air battery '
            'research: A review of in situ/operando measurement techniques," '
            '<em>Carbon Reports</em> (2025).',
            'Hatakeyama et al. (incl. Ryoshi Oda), "Fe-Doped MnO₂ Catalysts for Li–O₂ Batteries," '
            '<em>ACS Applied Energy Materials</em> (2025).',
        ],
        "conferences": [
            "Poster: 61st Carbon Materials Summer Seminar (2025/09/11).",
            "Poster: Japan-China-Korea Joint Symposium CSE2025 (2025/10/29).",
        ],
        "awards": [
            "Poster Award, Carbon Materials Society Young Researchers Group (2025/09/11).",
        ],
    },

    "zhai-xiazhe": {
        "affiliation":  "Graduate School of Integrated Science and Engineering, Kyushu University",
        "department":   "Integrated Science and Engineering (総合理工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/zhai-x/",
        "k2spring_en":  "Creating high-value carbon materials from carbonised products and byproducts of locally-sourced Japanese biomass",
        "k2spring_jp":  "日本近域産バイオマスを原料とした炭素化物および副産物からの高付加価値カーボン材料の創製",
        "abstract_en":  (
            "This project analyses thermal decomposition byproducts — tar and gas — "
            "from abundant Japanese biomass sources and develops optimal modification and "
            "separation techniques. Oxygen-rich tar components are converted into functional "
            "materials, while porous carbon and carbon fibre products are fabricated for "
            "diverse industrial applications."
        ),
        "abstract_jp":  (
            "日本国内に豊富なバイオマスの"
            "熱分解副産物（タールおよびガ"
            "ス）を分析し、最適な改質・分"
            "離技術を開発する研究です。酸"
            "素リッチなタール成分を機能性"
            "材料へ変換するとともに、多孔"
            "賠炭素や炭素繊維製品を製造し"
            "、多様な産業用途への展開を目指します。"
        ),
        "papers": [],
        "conferences": [
            "Multiple conference presentations (7 total, 2025–2026).",
        ],
        "awards": [
            "Multiple poster and excellence awards (3 total, 2025–2026).",
        ],
    },

    "yuki-nishimura": {
        "name_jp":      "西村 勇輝",   # 西村 勇輝
        "affiliation":  "Kyushu University Energy Research and Education Organization (Q-PIT)",
        "department":   "Graduate School of Integrated Science and Engineering (総合理工学府)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/nishimura-y/",
        "k2spring_en":  "Research on magnetised plasma structure and fluctuations using tomography systems",
        "k2spring_jp":  "トモグラフィシステムを用いた磁化プラズマの構造と揺動に関する研究",
        "abstract_en":  (
            "Turbulence in magnetically confined plasmas degrades energy confinement in fusion "
            "reactors. This research develops high-speed, high-precision measurement methods "
            "and reconstruction algorithms to observe plasma structure and fluctuations using "
            "time-series tomographic data, contributing to improved understanding and control "
            "of turbulent transport."
        ),
        "abstract_jp":  (
            "磁場閉じ込めプラズマ中の乱流"
            "は核融合炉のエネルギー閉じ込"
            "めを劣化させます。本研究では"
            "時系列トモグラフィデータを用"
            "いてプラズマの構造と揺動を観"
            "測する高速・高第度な計測手法"
            "と再構成アルゴリズムを開発し"
            "、乱流輸送の理解と制御に貢献します。"
        ),
        "papers": [
            'Yuki Nishimura et al., "Revisit to Cormack Inversion Using Function Modification '
            'Technique for Plasma Tomography," <em>Plasma and Fusion Research</em> (2025).',
            'Yuki Nishimura et al., "Neural Network for Fluctuation Evaluations of Plasma '
            'Tomography," <em>Review of Scientific Instruments</em> (2025, submitted).',
        ],
        "conferences": [
            "Poster: tomography algorithm development, 42nd Plasma and Nuclear Fusion Conference, Kyoto (December 2025).",
        ],
        "awards": [],
    },

    "qi-shi": {
        "name_jp":      "チーシー",   # チーシー (phonetic)
        "affiliation":  "Graduate School of Integrated Frontier Sciences, Kyushu University",
        "department":   "Automotive Science (オートモーティブサイエンス専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/qi-s/",
        "k2spring_en":  "Improvement of tubular solid oxide reversible cells using LSGM electrolyte via dip coating",
        "k2spring_jp":  "ディップコーティング法によるLSGM電解質を用いたチューブ型固体酸化物可逆セルの改良",
        "abstract_en":  (
            "This research aims to improve the performance of tubular solid oxide reversible "
            "cells (SORC) by optimising the dip-coating process for LSGM "
            "(La₀.₉Sr₀.₁Ga₀.₈Mg₀.₂O₃₋δ) "
            "electrolyte deposition. By elucidating the degradation mechanisms of the cell, "
            "the study seeks to enable practical implementation of reversible solid oxide cells "
            "for hydrogen-based carbon-neutral energy systems."
        ),
        "abstract_jp":  (
            "ディップコーティング法による"
            "LSGM電解質の成膜プロセスを最適化"
            "することでチューブ型固体酸化"
            "物可逆セル（SORC）の性能向上を図"
            "る研究です。劣化メカニズムを解"
            "明し、水素系カーボンニュートラ"
            "ルエネルギーシステムへの実用化"
            "を目指します。"
        ),
        "papers": [],
        "conferences": [],
        "awards": [],
    },

    "kohei-sawada": {
        "name_jp":      "沢田 光平",   # 澤田 光平
        "affiliation":  "Graduate School of Integrated Frontier Sciences, Kyushu University",
        "department":   "Automotive Science (オートモーティブサイエンス専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/sawada-k/",
        "k2spring_en":  "Development of high-efficiency photocatalytic water-splitting systems using gallium-indium compounds",
        "k2spring_jp":  "ガリウムインジウム系化合物を用いた高効率光水分解系の開発",
        "abstract_en":  (
            "This research synthesises InGaN and GaN/InGaN powders via solid-phase and "
            "liquid-phase reaction methods to develop economically viable photocatalysts for "
            "solar-driven water splitting. Both experimental and theoretical approaches are "
            "employed to elucidate the detailed catalytic mechanisms governing "
            "photoelectrochemical hydrogen production."
        ),
        "abstract_jp":  (
            "固相・液相反応法によるInGaNおよび"
            "GaN/InGaN粉末の合成を通じて、経済的に"
            "実現可能な光水分解用光触媒の開発"
            "を行う研究です。実験と理論の両ア"
            "プローチにより光電気化学的水素生"
            "成を支配する触媒機構の詳細解明を"
            "目指します。"
        ),
        "papers": [
            'Kohei Sawada et al., study on magnesium-doped InGaO₃, '
            '<em>Applied Catalysis A: General</em> (2026).',
            'Kohei Sawada et al., heptazine-imide photocatalytic hydrogen peroxide synthesis, '
            '<em>Journal of Materials Chemistry A</em> (2025).',
        ],
        "conferences": [
            "Presentation at Singapore Science Conference 2025 (December 2025).",
            "Presentation at 20th Japan-Korea Symposium on Catalysis, Tottori (May 2025).",
        ],
        "awards": [],
    },

    "wang-sheng": {
        "affiliation":  "Graduate School of Engineering, Kyushu University",
        "department":   "Earth Resources Systems (工学府 地球資源システム専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/wang-s/",
        "k2spring_en":  "Investigation of gas-liquid two-phase flow mechanisms in microscopic fractures under reservoir in-situ thermo-pressure conditions",
        "abstract_en":  (
            "This study investigates the mechanisms of gas-liquid two-phase flow in rock fractures "
            "under temperature and pressure conditions representative of geothermal reservoirs. "
            "Through laboratory experiments, theoretical modelling, and numerical simulation, "
            "the research explores gas-liquid displacement dynamics to provide design guidance "
            "for optimising geothermal energy extraction efficiency."
        ),
        "papers": [
            'Li et al. (incl. Sheng Wang), paper on mechanical behaviour of rock samples with '
            'preexisting flaws, Vol. 37, No. 086649 (2025).',
        ],
        "conferences": [
            "Sheng Wang et al., structural evolution in deep soft rock roadways, "
            "International Symposium on Earth Science and Technology (2025).",
        ],
        "awards": [],
    },

    "nozomi-goto": {
        "name_jp":      "後藤 希",   # 後藤 希
        "affiliation":  "Graduate School of Engineering, Kyushu University",
        "department":   "Materials Engineering (工学府 材料工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/goto-n/",
        "k2spring_en":  "Accelerated exploration of proton-conducting solid oxide fuel cell cathode materials using machine learning",
        "k2spring_jp":  "機械学習を用いたプロトン伝導性固体酸化物燃料電池カソード材料の加速的探索",
        "abstract_en":  (
            "Proton-conducting solid oxide fuel cells (PCFCs) operating at approximately 300 °C "
            "eliminate the need for platinum catalysts. While electrolyte development now enables "
            "low-temperature operation, cathode materials remain a performance bottleneck causing "
            "output reduction. This research leverages machine learning to accelerate the discovery "
            "and optimisation of high-performance PCFC cathode materials."
        ),
        "abstract_jp":  (
            "約300 °Cで動作するプロトン伝導性"
            "固体酸化物燃料電池（PCFC）は白金触媒"
            "を不要とします。電解質の開発により"
            "低温動作が可能になりましたが、カソ"
            "ード材料が依然として性能のボトルネ"
            "ックとなっています。本研究では機械"
            "学習を活用して高性能PCFCカソード材料"
            "の探索・最適化を加速します。"
        ),
        "papers": [],
        "conferences": [
            "Presentation on electrochemistry of scandium-doped barium zirconate films, "
            "19th Solid State Ionics Seminar (August 2025).",
        ],
        "awards": [],
    },

    "zhanyi-xiang": {
        "name_jp":      "向 展毅",   # 向 展毅
        "affiliation":  "Graduate School of Engineering, Kyushu University",
        "department":   "Hydrogen Energy Systems (水素エネルギーシステム専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/xiang-z/",
        "k2spring_en":  "Elucidation of electrochemical reaction mechanisms in H₂O–CO₂ co-electrolysis of SOEC and construction of numerical analysis methods",
        "k2spring_jp":  "固体酸化物電解セル（SOEC）の共電解における化学反応を伴う電気化学反応の原理解明および数値解析手法の構築",
        "abstract_en":  (
            "Solid oxide electrolysis cells (SOEC) operating above 600 °C enable highly "
            "efficient H₂O–CO₂ co-electrolysis to simultaneously produce hydrogen "
            "and carbon monoxide. This research elucidates the underlying reaction mechanisms "
            "including the water-gas shift reaction and thermal stress effects, and constructs "
            "3D numerical models to establish design guidelines for enhanced SOEC efficiency "
            "and durability."
        ),
        "abstract_jp":  (
            "600 °C以上で動作する固体酸化物電解"
            "セル（SOEC）はH₂O–CO₂共電解により水素"
            "と一酸化炭素を同時生成できます。本"
            "研究は水性ガスシフト反応や熱応力効"
            "果を含む反応機構を解明し、SOECの効率・"
            "耐久性向上のための設計指針を確立す"
            "る3次元数値解析モデルを構築します。"
        ),
        "papers": [],
        "conferences": [],
        "awards": [],
    },

    "rika-iriguchi": {
        "name_jp":      "入口 梨佳",   # 入口 梨佳
        "affiliation":  "Graduate School of Engineering, Kyushu University",
        "department":   "Earth Resource Systems Engineering (地球資源システム工学専攻)",
        "source_url":   "https://q-pit.kyushu-u.ac.jp/q-energy/ay-2025/iriguchi-r/",
        "k2spring_en":  "Development of low environmental impact hydrogen production technology from biomass fermentation processes",
        "abstract_en":  (
            "This research optimises biological hydrogen production from biomass through diverse "
            "microbial metabolic pathways, aiming to develop high-efficiency, low-environmental-impact "
            "hydrogen production technology. The approach contributes to both energy security and "
            "decarbonisation goals by establishing sustainable hydrogen supply chains from renewable "
            "organic feedstocks."
        ),
        "papers": [
            'Rika Iriguchi et al., paper on underground coal gasification with water injection, '
            '<em>Scientific Reports</em> (2024).',
            'Rika Iriguchi et al., study on CO₂ nanobubble applications in cement, '
            '<em>Materials</em> (2025, accepted).',
            'Rika Iriguchi et al., paper on water injection in coal gasification systems, '
            '<em>Energy</em> (2025).',
        ],
        "conferences": [
            "Presentation at International Symposium on Earth Science and Technology (2025).",
            "Upcoming presentations at World Mining Congress and Asian Rock Mechanics Symposium.",
        ],
        "awards": [
            "Excellence Poster Award, Kyushu University Energy Research Organization (January 2026).",
            "Self-introduction article for young researchers, quarterly journal (April 2026).",
        ],
    },
}


# ── helpers ───────────────────────────────────────────────────────────────────

def build_items(lst):
    """Build an <ol class="ach-list"> from a list of HTML strings, or a 'coming soon' placeholder."""
    if not lst:
        return (
            '<ol class="ach-list"><li>'
            '<span class="ach-soon">'
            '<span data-lang-en="">Coming soon</span>'
            '<span data-lang-jp="">準備中</span>'
            '</span></li></ol>'
        )
    lis = "\n      ".join(f"<li>{item}</li>" for item in lst)
    return f'<ol class="ach-list">\n      {lis}\n    </ol>'


# ── exact placeholder strings present in every generated 2025 file ────────────

OLD_SUBLINE = (
    '    <div class="hero-subline">\n'
    '      <dl><dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">所属</dt><dd>To be added</dd></dl>\n'
    '      <dl><dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">専攻・部局</dt><dd>To be added</dd></dl>\n'
    '      <dl><dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>To be added</dd></dl>\n'
    '    </div>'
)

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

OLD_PHD_TITLES = (
    '      <h3 data-lang-en="">To be added</h3>\n'
    '      <h3 data-lang-jp="">To be added</h3>'
)

OLD_PHD_BODY = (
    '      <div data-lang-en=""><p>The public 2025 profile is currently available as a PDF link '
    'only in the extracted data. Details will be added after the missing information is provided.</p></div>\n'
    '      <div data-lang-jp=""><p>The public 2025 profile is currently available as a PDF link '
    'only in the extracted data. Details will be added after the missing information is provided.</p></div>'
)

OLD_ACH = (
    '    <div class="ach-group">\n'
    '      <div class="ach-label"><span data-lang-en="">Research Papers</span>'
    '<span data-lang-jp="">論文</span></div>\n'
    '      <ol class="ach-list"><li><span class="ach-soon">'
    '<span data-lang-en="">Coming soon</span>'
    '<span data-lang-jp="">準備中</span></span></li></ol>\n'
    '    </div>\n'
    '    <div class="ach-group">\n'
    '      <div class="ach-label"><span data-lang-en="">Conference Presentations</span>'
    '<span data-lang-jp="">学会発表</span></div>\n'
    '      <ol class="ach-list"><li><span class="ach-soon">'
    '<span data-lang-en="">Coming soon</span>'
    '<span data-lang-jp="">準備中</span></span></li></ol>\n'
    '    </div>\n'
    '    <div class="ach-group">\n'
    '      <div class="ach-label"><span data-lang-en="">Other Achievements</span>'
    '<span data-lang-jp="">その他の業績</span></div>\n'
    '      <ol class="ach-list"><li><span class="ach-soon">'
    '<span data-lang-en="">Coming soon</span>'
    '<span data-lang-jp="">準備中</span></span></li></ol>\n'
    '    </div>'
)


# ── main ──────────────────────────────────────────────────────────────────────

def update_file(slug, d):
    path = DIR_25 / f"{slug}.html"
    if not path.exists():
        print(f"  SKIP  {slug}.html — file not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html  # keep for diff check

    title_jp   = d.get("k2spring_jp", d["k2spring_en"])
    abstract_jp = d.get("abstract_jp", d["abstract_en"])

    # 1. Hero subline ─────────────────────────────────────────────────────────
    new_subline = (
        '    <div class="hero-subline">\n'
        f'      <dl><dt data-lang-en="">Affiliation</dt><dt data-lang-jp="">所属</dt><dd>{d["affiliation"]}</dd></dl>\n'
        f'      <dl><dt data-lang-en="">Major / Department</dt><dt data-lang-jp="">専攻・部局</dt><dd>{d["department"]}</dd></dl>\n'
        '      <dl><dt data-lang-en="">Supervisor</dt><dt data-lang-jp="">指導教員</dt><dd>To be added</dd></dl>\n'
        '    </div>'
    )
    html = html.replace(OLD_SUBLINE, new_subline, 1)

    # 2. JP name in hero ──────────────────────────────────────────────────────
    if "name_jp" in d:
        html = re.sub(
            r'(<h1 class="name name-jp" data-lang-jp="">)[^<]*(</h1>)',
            rf'\g<1>{d["name_jp"]}\g<2>',
            html, count=1
        )

    # 3. K2-SPRING article ────────────────────────────────────────────────────
    new_k2 = (
        '    <div class="research-banner">\n'
        '      <svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true">'
        '<path d="M6 0l1.5 4.5L12 6 7.5 7.5 6 12 4.5 7.5 0 6l4.5-1.5z"/></svg>\n'
        '      <span data-lang-en="">K2-SPRING topic &middot; 2025</span>\n'
        '      <span data-lang-jp="">K2-SPRINGテーマ &middot; 2025年度</span>\n'
        '    </div>\n'
        f'    <h3 class="research-title" data-lang-en="">{d["k2spring_en"]}</h3>\n'
        f'    <h3 class="research-title" data-lang-jp="">{title_jp}</h3>\n'
        f'    <div class="research-abstract" data-lang-en=""><p>{d["abstract_en"]}</p></div>\n'
        f'    <div class="research-abstract" data-lang-jp=""><p>{abstract_jp}</p></div>'
    )
    html = html.replace(OLD_K2, new_k2, 1)

    # 4a. PhD card — titles ───────────────────────────────────────────────────
    new_phd_titles = (
        f'      <h3 data-lang-en="">{d["k2spring_en"]}</h3>\n'
        f'      <h3 data-lang-jp="">{title_jp}</h3>'
    )
    html = html.replace(OLD_PHD_TITLES, new_phd_titles, 1)

    # 4b. PhD card — body text ────────────────────────────────────────────────
    new_phd_body = (
        f'      <div data-lang-en=""><p>{d["abstract_en"]}</p></div>\n'
        f'      <div data-lang-jp=""><p>{abstract_jp}</p></div>'
    )
    html = html.replace(OLD_PHD_BODY, new_phd_body, 1)

    # 4c. PhD card — source action link (PDF → HTML) ──────────────────────────
    html = re.sub(
        r'<a class="source-pill" href="https://q-pit\.kyushu-u\.ac\.jp/wp-content/uploads/[^"]*"[^>]*>Original PDF profile</a>',
        f'<a class="source-pill" href="{d["source_url"]}" target="_blank" rel="noopener">Public profile page</a>',
        html, count=1
    )

    # 5. Achievements ─────────────────────────────────────────────────────────
    new_ach = (
        '    <div class="ach-group">\n'
        '      <div class="ach-label"><span data-lang-en="">Research Papers</span>'
        '<span data-lang-jp="">論文</span></div>\n'
        f'      {build_items(d["papers"])}\n'
        '    </div>\n'
        '    <div class="ach-group">\n'
        '      <div class="ach-label"><span data-lang-en="">Conference Presentations</span>'
        '<span data-lang-jp="">学会発表</span></div>\n'
        f'      {build_items(d["conferences"])}\n'
        '    </div>\n'
        '    <div class="ach-group">\n'
        '      <div class="ach-label"><span data-lang-en="">Other Achievements</span>'
        '<span data-lang-jp="">その他の業績</span></div>\n'
        f'      {build_items(d["awards"])}\n'
        '    </div>'
    )
    html = html.replace(OLD_ACH, new_ach, 1)

    # 6. Metadata card ────────────────────────────────────────────────────────
    html = re.sub(
        r'(<dt>Affiliation</dt><dd>)[^<]*(</dd>)',
        rf'\g<1>{d["affiliation"]}\g<2>', html, count=1
    )
    html = re.sub(
        r'(<dt>Major / Department</dt><dd>)[^<]*(</dd>)',
        rf'\g<1>{d["department"]}\g<2>', html, count=1
    )
    html = re.sub(
        r'<dt>Source</dt><dd><a href="https://q-pit\.kyushu-u\.ac\.jp/wp-content/uploads/[^"]*"[^>]*>Original PDF profile</a></dd>',
        f'<dt>Source</dt><dd><a href="{d["source_url"]}" target="_blank" rel="noopener">Public profile page</a></dd>',
        html, count=1
    )
    html = re.sub(
        r'(<dt>Data status</dt><dd>)[^<]*(</dd>)',
        r'\g<1>Affiliation and research content sourced from the public Q-PIT profile page. Supervisor to be confirmed.\g<2>',
        html, count=1
    )

    if html == original:
        print(f"  WARN  {slug}.html — no changes made (placeholder strings not found?)")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  OK    {slug}.html")


def main():
    print(f"Updating {len(STUDENTS)} files in {DIR_25}\n")
    for slug, d in STUDENTS.items():
        update_file(slug, d)
    print("\nDone.")


if __name__ == "__main__":
    main()
