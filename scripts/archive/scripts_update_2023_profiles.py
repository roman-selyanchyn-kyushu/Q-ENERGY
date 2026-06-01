#!/usr/bin/env python3
"""
Fill 2023 student profile pages with real bilingual content.

Source pages: https://q-pit.kyushu-u.ac.jp/fellow-2023-en/[slug]/

For each student this script:
  1. Sets the Japanese display name (h1 name-jp field).
  2. Replaces the English-only doctoral research title in the JP field
     with the Japanese title from the source page.
  3. Replaces the English-only doctoral research abstract in the JP field
     with the Japanese abstract from the source page.

Narmandakh Khongorzul is skipped because no Japanese content is available
on the public page (non-Japanese student with only English profile).

Run from project root:
    python3 scripts_update_2023_profiles.py
"""

import re
from pathlib import Path

BASE   = Path(__file__).parent
DIR_23 = BASE / "students" / "2023"

# ── Student data ──────────────────────────────────────────────────────────────
# name_en_current : exact string currently in the JP h1 name field (will be
#                   replaced with the Japanese name)
# name_jp         : Japanese name from the public profile page
# title_jp        : Japanese research title
# abstract_jp     : Japanese research abstract (verbatim from source page)

STUDENTS = {
    "go-yokuhou": {
        "name_en_current": "Go Yokuhou",
        "name_jp": "呉 翼峰",
        "title_jp": "MH合金システムの速度律速因子の探求と設計指針の構築",
        "abstract_jp": (
            "本研究は、水素社会実現に向けた安全かつ効率的な水素貯蔵方法の開発を目指しています。"
            "水素吸蔵合金（MH合金）を利用した場合、表面反応から内部拡散、相変化に至る各プロセスを"
            "総合的に解析し、システムの速度律速因子を明確化します。その上で、固相拡散、気相拡散、"
            "伝熱の時間スケールを最適化することで、充放出時間の短縮を実現します。"
        ),
    },
    "hiroki-isogawa": {
        "name_en_current": "Hiroki Isogawa",
        "name_jp": "五十川 浩希",
        "title_jp": "トリチウム閉じ込め技術開発に向けた、Liロッド模擬試験体のトリチウム透過挙動解析",
        "abstract_jp": (
            "次世代エネルギー源として期待されている核融合炉では、燃料にトリチウムが使用されるが、"
            "天然に存在するリチウム量は極めて少ないため、高温ガス炉を用いたトリチウムの生産が"
            "検討されている。しかし、未だ高温環境下での材料中のトリチウム滞留挙動はわかっておらず、"
            "安全性の観点からもこれらの解明は必須となる。本研究では、高温ガス炉炉心を模擬した"
            "試験体を用いて、実際にトリチウム透過実験を行う。また、実験結果を化学工学的視点から"
            "解析することでトリチウム透過挙動をモデル化し、トリチウム基礎移動現象の解明を目指す。"
        ),
    },
    "kentaro-wada": {
        "name_en_current": "Kentaro Wada",
        "name_jp": "和田 健太郎",
        "title_jp": (
            "高温水素利用機器の安全性を確実にするための"
            "水素中クリープ寿命低下の機構解明に関する研究"
        ),
        "abstract_jp": (
            "SOECによる水素製造やSOFCによる水素発電などの先進高温水素利用技術は"
            "2050年のカーボンニュートラル実現に大きな役割が期待されている．"
            "これらの機器の構造部材は「高温」＋「水素」という極めて過酷な環境に曝される．"
            "高温で負荷を受ける部材の設計にはクリープ強度の考慮が必要不可欠であるが，"
            "クリープ変形に及ぼす水素の影響は十分に明らかになっていない．"
            "本研究では水素がクリープ寿命を低下させる機構の解明を目指す．"
            "国際共同の分野横断研究として熱力学による Defactant theory に基礎をおく"
            "ドイツ・ゲッチンゲン大学の Professor Kirchheim らと共同研究を実施する．"
        ),
    },
    "kotaro-shinozaki": {
        "name_en_current": "Kotaro Shinozaki",
        "name_jp": "篠崎 航太朗",
        "title_jp": "地熱発電の社会受容性に関する数理社会学的分析と制度提案",
        "abstract_jp": (
            "日本は世界第３位の地熱資源量を有しているが、実際の設備容量では世界第１０位であり、"
            "地熱開発はあまり進んでいない。開発の阻害要因として、温泉関係者からの反対という"
            "社会的課題が存在する。この研究では、ゲーム理論やAgent-Based Simulationといった"
            "数理社会学の手法を活用し、合意形成の状況を分析することで、地熱発電の社会受容性向上に"
            "資する知見や制度提案を目指す。"
        ),
    },
    # narmandakh-khongorzul — no Japanese content available, skipped
    "seiya-imada": {
        "name_en_current": "Seiya Imada",
        "name_jp": "今田 青冶",
        "title_jp": "日本の木造住宅のカーボンフットプリント分析",
        "abstract_jp": (
            "世界の建設活動とそれに伴う電力消費によるCO₂排出量は全体の19%を占めている。"
            "日本の住宅部門のCO₂排出削減策の多くは、サプライチェーンからのCO₂排出量削減に"
            "焦点を当てられていない。サプライチェーンを通じたCO₂排出削減のためには、"
            "サプライチェーン構造におけるCO₂排出ホットスポットの特定が必要である。"
            "そこで、本研究は日本の戸建て住宅の９割を占める木造住宅のサプライチェーン構造の"
            "推計を行い、サプライチェーン構造に存在するCO₂排出ホットスポットの特定を行う。"
        ),
    },
    "taisei-tomaru": {
        "name_en_current": "Taisei Tomaru",
        "name_jp": "都丸 大晟",
        "title_jp": "座礁資源を利用した高機能炭素繊維の製造に関する研究",
        "abstract_jp": (
            "座礁資源とは環境・社会の変化により価値を損失した資源を指し、"
            "例えばエチレン製造時に排出される重質残渣油「エチレンボトムオイル（EO）」が挙げられる。"
            "これは現在、ボイラー燃料として用いられており、大量のCO₂排出の原因となっている。"
            "そこで本研究では座礁資源の1つとしてEOに着目し、EOの有効利用・高付加価値化を試みる。"
            "EO由来の高機能炭素繊維を製造することで潜在的なCO₂排出源の削除と"
            "革新的な脱炭素社会の構築に貢献する。"
            "高機能炭素繊維の製造にはこれまでにない新たな製造方法を提案し、"
            "安価かつ高収率な製造を目指す。"
        ),
    },
    "xuesong-wei": {
        "name_en_current": "Xuesong Wei",
        "name_jp": "イ セツショウ",
        "title_jp": "沸騰と水電解のアナロジーに基づく水電解性能の飛躍的な向上",
        "abstract_jp": (
            "風力・太陽光発電が再生可能エネルギーとしての大量導入が急務だが、"
            "需要と供給に時空間的なズレが生じることで、余剰電力を水素に変換して貯蔵する"
            "水電解技術の高性能化が重要である。過去に我々は沸騰と水電解のアナロジーを基づき、"
            "沸騰超高熱流束冷却に成功したハニカム多孔体を用い、水電解電極面の気液流れを"
            "制御することでその性能を大幅に向上させた。今後我々は自己組織化現象により"
            "微細構造が制御されるハニカム多孔電極の作成技術を開発し、"
            "電解性能向上メカニズムをミクロスケールで解明を行い、理論モデルの構築を検討する。"
        ),
    },
    "yusuke-oga": {
        "name_en_current": "Yusuke Oga",
        "name_jp": "大賀 雄介",
        "title_jp": "環境・観光分析用産業連関分析を用いた旅行者のカーボンフットプリント分析",
        "abstract_jp": (
            "日本の観光需要は今後長期的に増加し、観光によるCO₂排出量も増加することが予想される。"
            "本研究は、新たな環境・観光分析用の産業連関分析フレームワークを開発し、"
            "国籍別訪日外客1人あたりのカーボンフットプリントと"
            "訪問地別国内旅行1人あたりのカーボンフットプリントを推計する。"
            "得られた結果から、CO₂負荷の大きい旅行者や産業部門の特定、"
            "需要サイドの政策提言（例えば、入国炭素税やカーボンラベル制度の政策提言）と"
            "供給サイドの政策提言（例えば、CO₂負荷の大きい産業に対する炭素補助金の支給）などを行う。"
        ),
    },
    "yuta-takaoka": {
        "name_en_current": "Yuta Takaoka",
        "name_jp": "髙岡 祐太",
        "title_jp": "マルチカーボン生成を目指した電気化学CO₂還元触媒の検討",
        "abstract_jp": (
            "カーボンニュートラルの観点から，排出量が最も多い温室効果ガスであるCO₂の再利用が"
            "求められている．再利用には多くのエネルギーを必要とすることから，"
            "より効率的な変換技術が求められている．近年，再生可能エネルギーを用いる"
            "電気化学CO₂還元（CO₂RR）が注目されている．CO₂RRは常温・常圧という温和な条件で"
            "効率的に反応を進行させることができる．しかしながら，CO₂RRには選択性の向上・"
            "過電圧の低減のために電極触媒が必要である．我々は，この電極触媒の構造や複合化によって，"
            "より高いエネルギー密度の生成物へと変換を試みる．"
        ),
    },
    "yutong-chen": {
        "name_en_current": "Yutong Chen",
        "name_jp": "陳 雨露",
        "title_jp": "再生可能エネルギーを利用して室内温湿度を自然調節するPSEシステムの開発",
        "abstract_jp": (
            "夏季は自然に冷却・除湿し、冬季は太陽集熱する熱性能可変型PDSC外被システムの"
            "性能向上を目途に、PDSCとERV（全熱交換換気）を併用したPSE"
            "（再生可能エネルギーと全熱交換を活用したハイブリッド換気システム）の"
            "省エネルギー効果について検討する。これまでに行ったPSEの数値実験結果を基に、"
            "汎用製品化を目指して実際に民間企業とPSE機器を共同開発する。更に、"
            "実証住宅による屋外実験と数値シミュレーションによりPSEの通年に亘る"
            "効率的な運転条件や方法について検証し、最適な制御システムを設計する。"
        ),
    },
}


def update_file(slug, d):
    path = DIR_23 / f"{slug}.html"
    if not path.exists():
        print(f"  SKIP  {slug}.html — file not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html

    # 1. Japanese display name ─────────────────────────────────────────────────
    old_name_tag = (
        f'<h1 class="name name-jp" data-lang-jp="">{d["name_en_current"]}</h1>'
    )
    new_name_tag = (
        f'<h1 class="name name-jp" data-lang-jp="">{d["name_jp"]}</h1>'
    )
    html = html.replace(old_name_tag, new_name_tag, 1)

    # 2. Japanese doctoral research title (h3 inside phd-body) ────────────────
    # The phd-body section has exactly one <h3 data-lang-jp=""> element.
    html = re.sub(
        r'(<div class="phd-body">.*?<h3 data-lang-jp="">)(.*?)(</h3>)',
        lambda m: m.group(1) + d["title_jp"] + m.group(3),
        html,
        flags=re.DOTALL,
        count=1,
    )

    # 3. Japanese doctoral research abstract (div data-lang-jp inside phd-body)
    # Pattern is unique: <div data-lang-jp=""><p>…</p></div> in phd-body only.
    html = re.sub(
        r'(<div data-lang-jp=""><p>)(.*?)(</p></div>)',
        lambda m: m.group(1) + d["abstract_jp"] + m.group(3),
        html,
        flags=re.DOTALL,
        count=1,
    )

    if html == original:
        print(f"  WARN  {slug}.html — no changes made (check placeholder strings)")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"  OK    {slug}.html")


def main():
    print(f"Updating {len(STUDENTS)} files in {DIR_23}\n")
    for slug, d in STUDENTS.items():
        update_file(slug, d)
    print(f"\n  SKIP  narmandakh-khongorzul.html — no Japanese content available")
    print("\nDone.")


if __name__ == "__main__":
    main()
