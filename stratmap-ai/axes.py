WHO_AXES = [
    {"id": "geo", "label": "地域・地政学", "group": "企業・組織", "desc": "グローバル・国内・地方都市など、ターゲット地域の範囲と特性。海外展開の有無や地域固有の規制も含む。"},
    {"id": "size", "label": "企業規模", "group": "企業・組織", "desc": "大企業／中堅／SMB／スタートアップ。予算規模・意思決定速度・組織複雑性が大きく変わる。"},
    {"id": "biz", "label": "ビジネスモデル", "group": "企業・組織", "desc": "BtoB／BtoC／BtoG／プラットフォーム型。提供価値の構造と受益者が異なる。"},
    {"id": "phase", "label": "事業フェーズ", "group": "企業・組織", "desc": "創業期・成長期・成熟期・変革期。DX投資の動機と緊急度が異なる。"},
    {"id": "dx", "label": "DX成熟度", "group": "企業・組織", "desc": "DX先進企業・追随中・未着手。技術受容度と必要なアプローチが全く異なる。"},
    {"id": "reg", "label": "規制環境", "group": "企業・組織", "desc": "強規制（金融・医療・公共）から自由業種まで。コンプライアンス要件が商談構造を規定する。"},
    {"id": "dept", "label": "部署・部門", "group": "意思決定・組織", "desc": "IT・経営企画・事業部門・法務・リスクなど。ペインの種類と意思決定権限が異なる。"},
    {"id": "layer", "label": "意思決定階層", "group": "意思決定・組織", "desc": "CxO・部長・課長・担当者。各層で関心事・評価軸・アクセスルートが変わる。"},
    {"id": "budget", "label": "予算権限", "group": "意思決定・組織", "desc": "予算オーナー・承認者・影響者・ユーザーの分離度。誰が意思決定の鍵を持つか。"},
    {"id": "proc", "label": "購買プロセス", "group": "意思決定・組織", "desc": "一括購買・稟議型・サブスク更新型。営業サイクルの長さと関与者数が変わる。"},
    {"id": "style", "label": "意思決定スタイル", "group": "意思決定・組織", "desc": "トップダウン・コンセンサス・現場起点。アプローチすべき人物と順序が変わる。"},
    {"id": "urgency", "label": "課題の緊急度", "group": "課題・ニーズ", "desc": "今すぐ解決したい・中期課題・潜在課題。提案のフレーミングと優先度が変わる。"},
    {"id": "aware", "label": "課題の認識度", "group": "課題・ニーズ", "desc": "自覚あり・漠然と感じる・気づいていない。マーケティングの入口が変わる。"},
    {"id": "pain", "label": "ペイン vs ゲイン", "group": "課題・ニーズ", "desc": "痛みを除去したい型 vs 利益を最大化したい型。提案言語とROI設計が変わる。"},
    {"id": "motive", "label": "変化の動機", "group": "課題・ニーズ", "desc": "外部規制起点・競合対抗起点・内部改革起点。urgencyと合わせて提案設計を変える。"},
    {"id": "rel", "label": "既存関係", "group": "関係・文脈", "desc": "既存顧客・見込み・全く新規。必要なエビデンスと信頼構築の速度が変わる。"},
    {"id": "comp", "label": "競合状況", "group": "関係・文脈", "desc": "競合使用中・ノーベンダー・内製志向。差別化戦略と置き換えコストが変わる。"},
]

WHAT_AXES = [
    {"id": "functional", "label": "機能的価値", "group": "価値の種類", "desc": "やりたいことが、より良くできるようになるか"},
    {"id": "economic", "label": "経済的価値", "group": "価値の種類", "desc": "コスト削減・売上向上に繋がるか"},
    {"id": "emotional", "label": "感情的価値", "group": "価値の種類", "desc": "安心・快適・楽しさを感じられるか"},
    {"id": "social", "label": "社会的価値", "group": "価値の種類", "desc": "周囲からの評価・信頼・帰属に繋がるか"},
    {"id": "pain", "label": "課題解消度", "group": "価値の位置づけ", "desc": "既存のペインをどこまで取り除けるか"},
    {"id": "gain", "label": "新規ゲイン", "group": "価値の位置づけ", "desc": "今まで得られなかった新しいメリットを生むか"},
    {"id": "advantage", "label": "代替優位性", "group": "価値の位置づけ", "desc": "既存の解決策より明確に優れている点があるか"},
    {"id": "unique", "label": "独自性", "group": "価値の位置づけ", "desc": "自社にしか出せない価値か"},
    {"id": "immediate", "label": "即効性", "group": "価値の届き方", "desc": "使い始めてすぐに実感できるか"},
    {"id": "lasting", "label": "持続性", "group": "価値の届き方", "desc": "長期的に価値が続く・蓄積するか"},
    {"id": "tangible", "label": "実感しやすさ", "group": "価値の届き方", "desc": "定量的に測れる・目に見える変化があるか"},
    {"id": "spread", "label": "波及性", "group": "価値の届き方", "desc": "本人以外（チーム・組織）にも価値が広がるか"},
    {"id": "voice", "label": "顧客の声", "group": "仮説の確からしさ", "desc": "顧客自身が「欲しい」と言っているか"},
    {"id": "behavior", "label": "行動的根拠", "group": "仮説の確からしさ", "desc": "実際に顧客がお金・時間を使っている兆候があるか"},
    {"id": "validated", "label": "検証済み度", "group": "仮説の確からしさ", "desc": "MVP・PoC等で実際に確認できているか"},
    {"id": "market", "label": "市場規模感", "group": "仮説の確からしさ", "desc": "この価値を求める顧客層は十分大きいか"},
]

HOW_JOURNEY_AXES = [
    {"id": "awareness", "label": "認知", "desc": "ターゲットはどこで自社を知るか"},
    {"id": "interest", "label": "興味", "desc": "「自分ごと」だと感じさせる仕掛けがあるか"},
    {"id": "contact", "label": "初回接触", "desc": "最初の体験のハードルは十分低いか"},
    {"id": "onboard", "label": "導入", "desc": "使い始めるまでのステップは簡潔か"},
    {"id": "success", "label": "成功体験", "desc": "早期に「価値を実感する瞬間」を設計しているか"},
    {"id": "habit", "label": "習慣化", "desc": "繰り返し使う理由・仕組みがあるか"},
    {"id": "deepen", "label": "深化", "desc": "使い込むほど価値が増す設計か"},
    {"id": "advocate", "label": "推奨", "desc": "他者に勧めたくなる動機・仕組みがあるか"},
]

HOW_MECHANISM_AXES = [
    {"id": "channel", "label": "チャネル適合", "desc": "顧客が普段いる場所で届けられるか"},
    {"id": "format", "label": "提供形態", "desc": "プロダクト/サービス/ハイブリッドの形が顧客に合っているか"},
    {"id": "customize", "label": "カスタマイズ余地", "desc": "顧客ごとの事情に合わせられる柔軟性があるか"},
    {"id": "relation", "label": "関係性モデル", "desc": "セルフサーブ/伴走/コミュニティ等、関係の深さは適切か"},
    {"id": "revenue", "label": "収益モデル", "desc": "課金の仕組みが顧客の価値実感と一致しているか"},
    {"id": "pricing", "label": "価格妥当性", "desc": "価格が顧客の期待する費用対効果に見合うか"},
    {"id": "ops", "label": "運用負荷", "desc": "自社が持続的に回せるオペレーション量か"},
    {"id": "scale", "label": "拡張余地", "desc": "事業拡大時にスケールできる構造か"},
]

ALL_SECTIONS = {
    "who": {"label": "Who（想定顧客）", "axes": WHO_AXES},
    "what": {"label": "What（提供価値）", "axes": WHAT_AXES},
    "howJourney": {"label": "How - ジャーニー（顧客体験の流れ）", "axes": HOW_JOURNEY_AXES},
    "howMechanism": {"label": "How - メカニズム（届ける仕組み）", "axes": HOW_MECHANISM_AXES},
}


def get_axes_description() -> str:
    lines = []
    for section_key, section in ALL_SECTIONS.items():
        lines.append(f"\n### {section['label']} (section: \"{section_key}\")")
        for ax in section["axes"]:
            lines.append(f"- **{ax['id']}** ({ax['label']}): {ax['desc']}")
    lines.append("\n### How - クロスマトリクス (section: \"howCross\")")
    lines.append("ジャーニー軸(行) × メカニズム軸(列) の関連度。level: 0=なし, 1=弱, 2=中, 3=強")
    lines.append(f"ジャーニー軸: {', '.join(a['id'] for a in HOW_JOURNEY_AXES)}")
    lines.append(f"メカニズム軸: {', '.join(a['id'] for a in HOW_MECHANISM_AXES)}")
    return "\n".join(lines)
