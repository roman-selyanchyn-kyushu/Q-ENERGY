#!/usr/bin/env python3
"""
Fill 2022 student profile pages with real bilingual content.

Source pages:
  EN:  https://q-pit.kyushu-u.ac.jp/fellow-2022-en/[slug]-en/
  JP:  https://q-pit.kyushu-u.ac.jp/fellow-2022-en/[slug]/  (no -en suffix)

For Japanese/Chinese students: sets Japanese title + abstract in data-lang-jp fields.
For he-qingyi: replaces placeholder phd-body (only JP available; JP used in both fields).
For zifei-nie: replaces "To be added" placeholder with EN content (no JP available).

Run from project root:
    python3 scripts_update_2022_profiles.py
"""

import re
from pathlib import Path

BASE   = Path(__file__).parent
DIR_22 = BASE / "students" / "2022"

# ── Student data ──────────────────────────────────────────────────────────────
# title_jp / abstract_jp  — Japanese research content to place in data-lang-jp
# title_en_new / abstract_en_new — only set when replacing a full placeholder
# mode:
#   "jp_only"    — EN title/abstract already in file; update only JP h3 and div
#   "full_jp"    — file has placeholder phd-body; replace with JP in both fields
#   "full_en"    — file has placeholder phd-body; replace with EN in both fields

STUDENTS = {
    "daisuke-yoshizawa": {
        "mode": "jp_only",
        "title_jp":    "カーシェアリング普及のCO2排出削減効果",
        "abstract_jp": (
            "脱炭素化に向けて車の使い方の変革も大切であるが、"
            "車の使い方を大きく変えるカーシェアリングサービスが環境に与える影響についての研究は少ない。"
            "カーシェアリングサービスが普及した際に日本のCO2排出量がどのように変化するのか分析し、"
            "温暖化緩和政策に繋がる提言を行う。"
            "本研究では、乗用車のストック･フローモデルを応用し、"
            "カーシェアリングサービスが拡大した際のCO2排出量の変化を包括的に分析できるフレームワークの開発を行うとともに、"
            "そのカーシェアリングサービスの普及シナリオがCO2削減に果たす役割について定量分析する。"
        ),
    },
    "tatsuya-hamashima": {
        "mode": "jp_only",
        "title_jp":    "高効率な反応を可能にするマイクロ波援用DRMシステムの開発と反応メカニズムの解明",
        "abstract_jp": (
            "脱炭素技術として注目されるメタンドライリフォーミング(DRM)は"
            "反応の省エネルギー化と触媒活性の低下の要因となる炭素の抑制が課題である。"
            "そこで省エネルギーな加熱方法であるマイクロ波加熱に着目し、"
            "La-Ce-Ni系触媒が優れた活性を示すことを明らかにした。"
            "しかし、さらなる省エネルギー化と高耐久性を有する触媒の開発のため"
            "詳細な反応メカニズムの解明が求められる。"
            "本研究においては、La-Ce-Ni系触媒を対象とし、"
            "ラマン分光分析、放射光測定、電子顕微鏡観察を駆使した活性向上メカニズムの解明から、"
            "マイクロ波援用DRMに必要な基盤技術を確立する。"
        ),
    },
    "sora-matsushima": {
        "mode": "jp_only",
        "title_jp":    "住宅ストックの動態を考慮した包括的LCA評価フレームワークの開発と実証分析",
        "abstract_jp": (
            "わが国の住宅・建築物分野の関わる部門からのCO2排出量は、"
            "全体のおよそ4割を占めるといわれている。"
            "様々な策が講じられている中で、住宅の長寿命化による建築時CO2削減と使用時の増加、"
            "省エネ住宅の普及による建築時CO2の増加と使用時の削減という"
            "二律背反の関係については未だに詳細な分析がなされていない。"
            "本研究は建物総体としての寿命・ストックの築年数別の構成を考慮し"
            "日本の住宅全体のライフサイクルCO2排出量の推計を行い、"
            "長寿命化や省エネ住宅の普及で発生するトレードオフ関係を"
            "シナリオ分析によって調査する。"
        ),
    },
    "shinichi-takeno": {
        "mode": "jp_only",
        "title_jp":    "新規電子・Liイオン混合伝導性酸化物の探索とその電池応用",
        "abstract_jp": (
            "脱炭素社会を実現するうえで、優れた蓄電池の開発は重要な研究課題となっている。"
            "Liイオン電池は、高いエネルギー密度から今後も蓄電池の中核を担うと考えられ、"
            "さらに、酸化物系固体電解質を用いた全固体電池は、"
            "究極の二次電池として期待されている。"
            "本研究では、高いLiイオン伝導性が報告されているペロブスカイト型酸化物に着目し、"
            "Li系全固体電池のキーマテリアルの一つである優れた電子・Liイオン混合導電体の探索を行い、"
            "高い電子伝導性と高いLiイオン伝導性を両立する材料の設計指針を確立し、"
            "その電池応用を試みる。"
        ),
    },
    "yixin-chen": {
        "mode": "jp_only",
        "title_jp":    "水素化物負極を用いた高容量全固体電池の構築",
        "abstract_jp": (
            "これまで、Mg(BH4)2、Ca(BH4)2、MgH2といった高容量負極材料に"
            "Liイオンを挿入すると固体電解質が自己生成することを明らかにしている。"
            "MgH2はLi挿入によりLiHとMgを生成するが、"
            "LiHのLiイオン伝導度は低いにも関わらず、"
            "固体電解質の自己生成により優れた全固体電池負極として利用できる。"
            "本研究では、生成するLi塩のイオン伝導性や、"
            "充放電中の電極合材中の反応物・生成物・炭素の3次元分布を明らかにすることで、"
            "自己生成固体電解質を用いた負極の電池特性を決定する要因を解明する。"
        ),
    },
    # he-qingyi — only JP available; use JP in both EN and JP fields
    "he-qingyi": {
        "mode": "full_jp",
        "title_jp": "人間の省エネ意識と省エネ行動の関係分析に基づく建物エネルギーシミュレーションツールの開発",
        "abstract_jp": (
            "本研究の目的は、将来の建物のエネルギーシミュレーションにおいて、"
            "人間の意識や行動の変化が及ぼす影響をシミュレートするためのツールを開発することである。"
            "本研究ではまず、アンケートと検証実験により、"
            "人間の環境心理と行動の関係の数理モデルを作る。"
            "そして、異なる人々に、環境意識を高めて省エネ行動を誘発するための異なる手段を設定する。"
            "これをもとに人間の行動をモデル化し、エネルギー消費のシミュレーションと組み合わせる。"
            "最後に、人間の意識や行動がエネルギー消費に与える影響を"
            "分析するシミュレーションツールを開発する。"
        ),
    },
    # zifei-nie — only EN available; use EN in both fields
    "zifei-nie": {
        "mode": "full_en",
        "title_en": (
            "Toward Safer, Smarter, and Decarbonized Mobility: "
            "Personalized Energy-efficient Driving for Intelligent Vehicles"
        ),
        "abstract_en": (
            "Analyzing the energy consumption for road vehicles and the corresponding driving behaviors "
            "are critical tasks for the realization of public traffic with a low energy cost and high efficiency. "
            "Especially, intelligent and connected vehicular technologies potentiate the energy-saving driving "
            "with ubiquitous and sensible traffic information. "
            "In this research, we try to utilize the advanced optimal control algorithm to optimize the driving "
            "decision and control output from vehicle powertrain so that the relationship between vehicle driving, "
            "road condition, traffic situation and powertrain efficiency can be fully matched to realize the "
            "energy-efficient driving. "
            "Meanwhile, the personalized driving styles are expected to be incorporated into the automated driving "
            "control system to quantitatively evaluate the impact from driving style on energy consumption. "
            "Ultimately, a human-oriented, safer, smarter and decarbonized energy-efficient autonomous driving "
            "system is expected to be developed for the next-generation mobility."
        ),
    },
}

# Placeholder strings used in the "full replacement" modes
PLACEHOLDER_PHD_BODY = (
    '<div class="phd-body"><h3 data-lang-en="">Extracted from public Q-PIT information</h3>'
    '<h3 data-lang-jp="">Q-PIT公開情報から抽出</h3>'
    '<p data-lang-en="">This local prototype page uses the same visual system as the 2026 cohort profiles '
    'while preserving the public source link and extracted content.</p>'
    '<p data-lang-jp="">This local prototype page uses the same visual system as the 2026 cohort profiles '
    'while preserving the public source link and extracted content.</p></div>'
)

TODO_H3_EN  = '<h3 data-lang-en="">To be added</h3>'
TODO_H3_JP  = '<h3 data-lang-jp="">To be added</h3>'
TODO_DIV_EN = '<div data-lang-en=""><p class="ach-soon">Detailed information will be added after it is provided.</p></div>'
TODO_DIV_JP = '<div data-lang-jp=""><p class="ach-soon">詳細情報は提供後に追記します。</p></div>'


def make_phd_body(title_en, abstract_en, title_jp, abstract_jp, source_url):
    """Build a complete phd-body block with source-actions link."""
    return (
        f'<div class="phd-body">'
        f'\n      <h3 data-lang-en="">{title_en}</h3>'
        f'\n      <h3 data-lang-jp="">{title_jp}</h3>'
        f'\n      <div data-lang-en=""><p>{abstract_en}</p></div>'
        f'\n      <div data-lang-jp=""><p>{abstract_jp}</p></div>'
        f'\n      <div class="source-actions">'
        f'<a class="source-pill" href="{source_url}" target="_blank" rel="noopener">Original public page</a>'
        f'<a class="source-pill" href="index.html">Back to 2022 cohort</a></div>'
        f'\n    '
        f'</div>'
    )


def get_source_url(html):
    m = re.search(r'href="(https://q-pit\.kyushu-u\.ac\.jp/fellow-2022[^"]+)"[^>]*>Original public page', html)
    return m.group(1) if m else "https://q-pit.kyushu-u.ac.jp/fellow-2022-en/"


def update_file(slug, d):
    path = DIR_22 / f"{slug}.html"
    if not path.exists():
        print(f"  SKIP  {slug}.html — file not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html
    mode = d["mode"]

    if mode == "jp_only":
        # Update JP h3 inside phd-body
        html = re.sub(
            r'(<div class="phd-body">.*?<h3 data-lang-jp="">)(.*?)(</h3>)',
            lambda m: m.group(1) + d["title_jp"] + m.group(3),
            html, flags=re.DOTALL, count=1,
        )
        # Update JP abstract div inside phd-body
        html = re.sub(
            r'(<div data-lang-jp=""><p>)(.*?)(</p></div>)',
            lambda m: m.group(1) + d["abstract_jp"] + m.group(3),
            html, flags=re.DOTALL, count=1,
        )

    elif mode == "full_jp":
        # Replace placeholder phd-body block entirely
        title_jp    = d["title_jp"]
        abstract_jp = d["abstract_jp"]
        src = get_source_url(html)
        new_block = make_phd_body(title_jp, abstract_jp, title_jp, abstract_jp, src)
        html = html.replace(PLACEHOLDER_PHD_BODY, new_block, 1)

    elif mode == "full_en":
        title_en    = d["title_en"]
        abstract_en = d["abstract_en"]
        # Replace "To be added" h3s
        html = html.replace(TODO_H3_EN, f'<h3 data-lang-en="">{title_en}</h3>', 1)
        html = html.replace(TODO_H3_JP, f'<h3 data-lang-jp="">{title_en}</h3>', 1)
        # Replace placeholder divs
        html = html.replace(TODO_DIV_EN, f'<div data-lang-en=""><p>{abstract_en}</p></div>', 1)
        html = html.replace(TODO_DIV_JP, f'<div data-lang-jp=""><p>{abstract_en}</p></div>', 1)

    if html == original:
        print(f"  WARN  {slug}.html — no changes made (check placeholder strings)")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  OK    {slug}.html [{mode}]")


def main():
    print(f"Updating 2022 profiles in {DIR_22}\n")
    for slug, d in STUDENTS.items():
        update_file(slug, d)

    # Sync alias files from their primaries where applicable
    pairs = [("qingyi-he", "he-qingyi")]  # primary ← alias (alias updated above)
    # Also re-sync the other alias files that were already synced:
    print("\n  INFO  Alias files (park-hyun-gyu, yin-kan-phua) already synced earlier.")
    print("\nDone.")


if __name__ == "__main__":
    main()
