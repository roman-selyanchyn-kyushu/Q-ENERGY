#!/usr/bin/env python3
"""
Fill 2021 student profile pages with real bilingual content.

Source pages:
  EN:  https://q-pit.kyushu-u.ac.jp/fellow-2021-en/[slug]-en/
  JP:  https://q-pit.kyushu-u.ac.jp/fellow-2021-en/[slug]/  (no -en suffix)

For Japanese/Chinese students: sets Japanese title + abstract in data-lang-jp fields.
masatoshi-tashima: also fills the missing EN content (was "To be added") and
                   corrects the wrong source URL.

Run from project root:
    python3 scripts_update_2021_profiles.py
"""

import re
from pathlib import Path

BASE   = Path(__file__).parent
DIR_21 = BASE / "students" / "2021"

# ── Student data ──────────────────────────────────────────────────────────────
# mode:
#   "jp_only"   — EN already in file; update only JP h3 and JP abstract div
#   "full_both" — "To be added" placeholder; replace EN and JP title + abstract,
#                 optionally fix source URL

STUDENTS = {
    "daiki-nishimura": {
        "mode": "jp_only",
        "title_jp":    "磁化プラズマにおける乱流の大域性の実験研究",
        "abstract_jp": (
            "次世代の大規模発電プラントとして期待される核融合炉を実用化するには、"
            "磁化プラズマ中の乱流輸送の物理機構を理解し、抑制することが必須である。"
            "磁化プラズマ中では、微視的な乱流揺動が巨視的な構造や流れと共存・相互作用することで"
            "大域性が発現することが明らかになっている。"
            "九州大学応用力学研究所にあるPLATOは初の乱流計測に特化したトカマク装置であり、"
            "豊富な計測ポートを有している。"
            "本研究ではトモグラフィ計測による大域乱流場観測と"
            "新たに作成する複合プローブアレイを用いて乱流輸送における大域性の役割を検証する。"
        ),
    },
    "haruka-mitoma": {
        "mode": "jp_only",
        "title_jp":    "インフォーマルセクターの生産活動を考慮したカーボンフットプリントの実証分析",
        "abstract_jp": (
            "インフォーマルセクターとは非公式な生産活動を行う主体であり、"
            "規制が不完全な状況下にあることから環境問題への寄与が懸念される。"
            "発展途上国ではその生産活動がGDPの約3分の1にも及ぶものの、"
            "統計データによってその生産活動の実態を捉えることが困難であるため"
            "どのように環境問題に寄与しているのか明らかにされていない。"
            "本研究は世界第三位のCO2排出国であるインドを対象として、"
            "限られたデータから産業連関分析の手法を用いて"
            "インフォーマルセクターの生産活動を推計することで"
            "カーボンフットプリントへの寄与を定量的に分析する。"
        ),
    },
    "keitaro-maeno": {
        "mode": "jp_only",
        "title_jp":    "グローバルサプライチェーンの再構築を通したCO2排出削減",
        "abstract_jp": (
            "自動車産業はグローバルサプライチェーン（GSC）の上流における"
            "CO2排出が大きいことがわかっている。"
            "脱炭素社会の実現に向け、COVID-19による主要国でのGSC再構築を機に、"
            "当該産業GSCのグリーン化が急務である。"
            "産業がグリーンサプライチェーンを構築するうえで重要なことは、"
            "当該産業GSCにおけるCO2排出ホットスポットを把握し、"
            "そこからのCO2排出を集中的に削減することである。"
            "そこで本研究は、CO2排出ホットスポットを解消させるような"
            "日本の自動車GSCの再構築が世界のCO2排出に与える影響を分析し、"
            "効果的なCO2排出削減策について考察する。"
        ),
    },
    "kento-komatsubara": {
        "mode": "jp_only",
        "title_jp":    "空間情報を用いた高分解能での環境持続可能性評価",
        "abstract_jp": (
            "本研究の目的は、再生可能エネルギー導入と生態系保存とのトレードオフの問題を考える"
            "材料となる定量的な指標を高解像度（250m×250m単位）で作成することである。"
            "空間情報と家庭・産業部門の顕示選好・表明選好の情報を基に、"
            "仮想評価法・コンジョイント分析・多基準意思決定分析を用いて、"
            "再生可能エネルギーと生態系に対する選好の規定要因を評価する。"
            "この評価に基づいて、再生可能エネルギーと生態系の動態予測を行い、"
            "都市の環境持続可能性評価システムの構築と評価を行う。"
        ),
    },
    # masatoshi-tashima — full update: EN was missing ("To be added") + wrong source URL
    "masatoshi-tashima": {
        "mode": "full_both",
        "title_en":    "Curved Organic Molecules as Electrode Active Material",
        "abstract_en": (
            "Na-ion batteries are expected to be a promising candidate for post-Li ion batteries "
            "due to the abundance of Na resources. "
            "However, since the ionic volume of Na is more than twice that of Li, "
            "the same materials for Li-ion batteries cannot be used for Na-ion batteries. "
            "Organic electrode materials are suitable for hosting the insertion of bulky Na ions "
            "due to their low specific gravity. "
            "In this research, I focus on organic π-conjugated materials with curvature. "
            "I have already found that sumanenetrione, which has a bowl-shaped structure, "
            "can be used as an active material for Na ion batteries. "
            "Further investigation on the storage of other metal ions and the use of "
            "other curved active materials will be conducted."
        ),
        "title_jp":    "湾曲活物質を用いた電池の創成",
        "abstract_jp": (
            "Na電池はNaの存在量が豊富であることなどから"
            "ポストLiイオン電池の有力候補と期待されている。"
            "しかしNaのイオン体積はLiの2倍以上違うため"
            "同じ材料をそのまま流用することはできない。"
            "そこでレアメタルフリーで、低比重のため嵩広いNaイオンの挿入・脱離ホストに適している"
            "有機電極材料、特に湾曲した構造を持つ物質に注目した研究を行う。"
            "すでにボウル型構造を持つスマネントリオンが"
            "Naイオン電池の活物質として使用できることを見出しているが、"
            "他の金属イオンの貯蔵や他の湾曲活物質についての検討を行う。"
        ),
        # Correct source URL (old was fellow-ship-en/fellow-2023-en/tashima-en/)
        "fix_url_old": "https://q-pit.kyushu-u.ac.jp/fellow-ship-en/fellow-2023-en/tashima-en/",
        "fix_url_new": "https://q-pit.kyushu-u.ac.jp/fellow-2021-en/tashima-en/",
    },
    "mingxu-sun": {
        "mode": "jp_only",
        "title_jp":    "電気化学二酸化炭素を付加価値化学物質に変換する",
        "abstract_jp": (
            "電気触媒によるCO2のC2+‐生成物への還元は、"
            "二酸化炭素の利用と地球温暖化の低減のための非常に魅力的な方法です。"
            "しかし、C2+‐生成物の選択性と収率は低いままです。"
            "ここでは、CO2の電気触媒還元により"
            "C2+‐生成物の選択性と収率を向上させるための"
            "触媒開発とセットアップ設計に焦点を当てています。"
        ),
    },
    "toraharu-watanabe": {
        "mode": "jp_only",
        "title_jp":    "アンモニア燃料を考慮した船舶機関室の換気制御に関する研究",
        "abstract_jp": (
            "船舶、特に国際海運からの温暖化ガス排出が大きな問題となり"
            "規制の強化が進められる中、アンモニア燃料は脱炭素を実現する"
            "次世代の船舶燃料として期待されている。"
            "一方でアンモニアはその強力な毒性により、リスク管理の面で厳重な対策が求められており、"
            "アンモニアを燃料として導入するための使用に係る規則の整備も進められている。"
            "本研究では規則整備のための評価指標を提示することを目標として、"
            "船舶機関室でアンモニアが漏洩した場合のリスクの分析、"
            "並びに漏洩を想定した場合の換気制御を数値流体計算と模型実験により最適化する。"
        ),
    },
    "xiaofeng-shen": {
        "mode": "jp_only",
        "title_jp":    "高活性化単層ナノシート色素増感型光触媒による水の完全分解",
        "abstract_jp": (
            "光触媒による水の完全分解は次世代エネルギー媒体として期待される水素の製造方法として"
            "研究されているが、現状の光-水素変換効率は1%程度である。"
            "そこで高表面積、高光子吸収効率、高色素担持量のナノシート構造に注目した。"
            "本研究ではナノシート分散・剥離剤に色素増感能を持たせた新規剥離剤の開発と、"
            "ナノシート型無機光触媒とのハイブリッド型光触媒を作製し、"
            "近赤外まで応答できる新しいシステムを開発する。"
        ),
    },
    "yulu-chen": {
        "mode": "jp_only",
        "title_jp":    "再生可能エネルギーを利用して室内温湿度を自然調節するPSEシステムの開発",
        "abstract_jp": (
            "夏季は自然に冷却・除湿し、冬季は太陽集熱する熱性能可変型PDSC外被システムの"
            "性能向上を目途に、PDSCとERV（全熱交換換気）を併用したPSE"
            "（再生可能エネルギーと全熱交換を活用したハイブリッド換気システム）の"
            "省エネルギー効果について検討する。"
            "これまでに行ったPSEの数値実験結果を基に、"
            "汎用製品化を目指して実際に民間企業とPSE機器を共同開発する。"
            "更に、実証住宅による屋外実験と数値シミュレーションによりPSEの通年に亘る"
            "効率的な運転条件や方法について検証し、最適な制御システムを設計する。"
        ),
    },
    # Skipped: likhith-manjunatha, timothee-redarce (no Japanese content available)
    # Skipped: tianhui-fan (no Japanese content on public page)
    # Note: sun-mingxu is an alias of mingxu-sun — handled separately below
}

TODO_H3_EN  = '<h3 data-lang-en="">To be added</h3>'
TODO_H3_JP  = '<h3 data-lang-jp="">To be added</h3>'
TODO_DIV_EN = '<div data-lang-en=""><p class="ach-soon">Detailed information will be added after it is provided.</p></div>'
TODO_DIV_JP = '<div data-lang-jp=""><p class="ach-soon">詳細情報は提供後に追記します。</p></div>'


def update_file(slug, d):
    path = DIR_21 / f"{slug}.html"
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

    elif mode == "full_both":
        # Replace "To be added" h3s
        html = html.replace(TODO_H3_EN, f'<h3 data-lang-en="">{d["title_en"]}</h3>', 1)
        html = html.replace(TODO_H3_JP, f'<h3 data-lang-jp="">{d["title_jp"]}</h3>', 1)
        # Replace placeholder abstract divs
        html = html.replace(
            TODO_DIV_EN,
            f'<div data-lang-en=""><p>{d["abstract_en"]}</p></div>', 1
        )
        html = html.replace(
            TODO_DIV_JP,
            f'<div data-lang-jp=""><p>{d["abstract_jp"]}</p></div>', 1
        )
        # Fix wrong source URL if specified
        if "fix_url_old" in d:
            html = html.replace(d["fix_url_old"], d["fix_url_new"])

    if html == original:
        print(f"  WARN  {slug}.html — no changes made (check placeholder strings)")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  OK    {slug}.html [{mode}]")


def main():
    print(f"Updating 2021 profiles in {DIR_21}\n")
    for slug, d in STUDENTS.items():
        update_file(slug, d)

    # Sync alias file sun-mingxu from primary mingxu-sun
    primary = DIR_21 / "mingxu-sun.html"
    alias   = DIR_21 / "sun-mingxu.html"
    if primary.exists():
        alias.write_text(primary.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"  SYNC  sun-mingxu.html ← mingxu-sun.html")

    print(f"\n  SKIP  likhith-manjunatha — no JP content available")
    print(f"  SKIP  timothee-redarce    — no JP content available")
    print(f"  SKIP  tianhui-fan         — no JP content on public page")
    print("\nDone.")


if __name__ == "__main__":
    main()
