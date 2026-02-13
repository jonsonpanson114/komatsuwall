"""
小松ウオール工業 施工事例検索
Architectural Monograph Design
"""

import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="KOMATSU WALL | 空間を、直感で見つける",
    page_icon="◻️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Design System — Architectural Monograph
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOISE_SVG = "data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E"

st.markdown(
    f"""
<style>
/* ── Typography ── */
@import url('https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@400;500;600;700;800&family=Zen+Kaku+Gothic+New:wght@300;400;500;700&display=swap');

:root {{
    --display: "Shippori Mincho", "游明朝", "YuMincho", "Hiragino Mincho ProN", serif;
    --body: "Zen Kaku Gothic New", "游ゴシック", "YuGothic", sans-serif;

    /* Warm architectural palette */
    --ink: #080808;
    --charcoal: #1a1a1a;
    --stone: #4a4a4a;
    --ash: #8a8a8a;
    --mist: #b0b0b0;
    --silk: #d8d4ce;
    --linen: #eae6df;
    --cream: #f5f2ec;
    --paper: #faf8f4;
    --white: #ffffff;

    /* Accent — warm bronze */
    --bronze: #9a7b5b;
    --bronze-light: #c4a882;
    --bronze-glow: rgba(154, 123, 91, 0.15);
}}

html, body, [class*="css"] {{
    font-family: var(--body) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}}

/* ── Streamlit chrome — hide everything ── */
#MainMenu, footer, header, .stDeployButton,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {{
    display: none !important;
    visibility: hidden !important;
}}

.stApp {{
    background: var(--paper);
}}
.stApp > header {{ background: transparent !important; }}

.main .block-container {{
    max-width: 100%;
    padding: 0;
}}

/* ── Animations ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(40px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
@keyframes slideScore {{
    from {{ width: 0; }}
}}

/* ════════════════════════════════════════════════════════
   HERO — Cinematic dark canvas with film grain
   ════════════════════════════════════════════════════════ */
.hero {{
    background: var(--ink);
    padding: 160px 40px 120px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
/* Film grain noise overlay */
.hero::after {{
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("{NOISE_SVG}");
    background-repeat: repeat;
    background-size: 256px;
    opacity: 0.035;
    pointer-events: none;
    mix-blend-mode: overlay;
}}
/* Warm radial glow */
.hero::before {{
    content: '';
    position: absolute;
    top: 35%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 1000px;
    height: 500px;
    background: radial-gradient(ellipse, rgba(154,123,91,0.07) 0%, transparent 65%);
    pointer-events: none;
}}

.hero-overline {{
    font-family: var(--body);
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--ash);
    margin: 0 0 28px;
    position: relative;
    z-index: 1;
    animation: fadeUp 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.1s both;
}}

.hero-headline {{
    font-family: var(--display);
    font-size: 76px;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0 0 24px;
    position: relative;
    z-index: 1;
    animation: fadeUp 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.3s both;
    /* Gradient text — white to warm silver */
    background: linear-gradient(160deg, #ffffff 20%, var(--silk) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.hero-subhead {{
    font-family: var(--body);
    font-size: 18px;
    font-weight: 300;
    color: var(--mist);
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.72;
    letter-spacing: 0.04em;
    position: relative;
    z-index: 1;
    animation: fadeUp 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.55s both;
}}

/* ════════════════════════════════════════════════════════
   SEARCH — Frosted glass with warm accent
   ════════════════════════════════════════════════════════ */
div[data-testid="stTextInput"] > div > div > input {{
    font-family: var(--body) !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    padding: 20px 28px !important;
    border-radius: 14px !important;
    border: 1px solid var(--silk) !important;
    background: rgba(255,255,255,0.85) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    color: var(--charcoal) !important;
    letter-spacing: 0.02em !important;
    transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06),
                0 1px 3px rgba(0,0,0,0.04) !important;
}}
div[data-testid="stTextInput"] > div > div > input::placeholder {{
    color: var(--mist) !important;
    font-weight: 300 !important;
    letter-spacing: 0.03em !important;
}}
div[data-testid="stTextInput"] > div > div > input:focus {{
    border-color: var(--bronze) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06),
                0 0 0 3px var(--bronze-glow) !important;
    outline: none !important;
}}
div[data-testid="stTextInput"] > label {{
    display: none !important;
}}

/* ════════════════════════════════════════════════════════
   CHIPS — Editorial text links
   ════════════════════════════════════════════════════════ */
div[data-testid="stButton"] > button {{
    font-family: var(--body) !important;
    background: transparent !important;
    color: var(--ash) !important;
    border: 1px solid var(--silk) !important;
    border-radius: 980px !important;
    padding: 7px 20px !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    letter-spacing: 0.04em !important;
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1) !important;
    white-space: nowrap !important;
}}
div[data-testid="stButton"] > button:hover {{
    color: var(--bronze) !important;
    border-color: var(--bronze-light) !important;
    background: rgba(154,123,91,0.04) !important;
    transform: translateY(-1px) !important;
}}
div[data-testid="stButton"] > button:active {{
    transform: scale(0.97) translateY(0) !important;
}}

/* ════════════════════════════════════════════════════════
   RESULTS HEADER
   ════════════════════════════════════════════════════════ */
.results-bar {{
    max-width: 1060px;
    margin: 56px auto 0;
    padding: 0 32px 24px;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid var(--linen);
}}
.results-bar .r-count {{
    font-family: var(--display);
    font-size: 28px;
    font-weight: 600;
    color: var(--charcoal);
    letter-spacing: -0.01em;
}}
.results-bar .r-query {{
    font-size: 14px;
    font-weight: 400;
    color: var(--ash);
    letter-spacing: 0.02em;
}}

/* ════════════════════════════════════════════════════════
   GALLERY CARDS — Cinematic editorial
   ════════════════════════════════════════════════════════ */
.card {{
    background: var(--white);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 28px;
    cursor: default;
    position: relative;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04),
                0 4px 20px rgba(0,0,0,0.05);
    transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    animation: fadeUp 0.7s cubic-bezier(0.22, 1, 0.36, 1) both;
    animation-delay: calc(var(--i, 0) * 0.07s);
}}
.card:hover {{
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.10),
                0 8px 16px rgba(0,0,0,0.06);
}}

/* Thumbnail wrapper */
.card .thumb-wrap {{
    position: relative;
    overflow: hidden;
}}
/* Cinematic gradient overlay on image */
.card .thumb-wrap::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(transparent, rgba(0,0,0,0.25));
    pointer-events: none;
    transition: opacity 0.4s;
}}
.card:hover .thumb-wrap::after {{
    opacity: 0.7;
}}

.card .thumb {{
    width: 100%;
    height: 280px;
    object-fit: cover;
    display: block;
    transition: transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}}
.card:hover .thumb {{
    transform: scale(1.06);
}}

.card .thumb-empty {{
    width: 100%;
    height: 280px;
    background: linear-gradient(145deg, var(--cream) 0%, var(--linen) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--silk);
    font-size: 13px;
    font-family: var(--body);
    letter-spacing: 0.1em;
}}

/* Score bar — thin warm gradient at image bottom */
.card .score-line {{
    position: absolute;
    bottom: 0;
    left: 0;
    height: 2px;
    z-index: 2;
    animation: slideScore 0.8s cubic-bezier(0.22, 1, 0.36, 1) 0.3s both;
}}

/* Card metadata */
.card .meta {{
    padding: 22px 24px 28px;
}}
.card .meta .name {{
    font-family: var(--display);
    font-size: 17px;
    font-weight: 600;
    color: var(--charcoal);
    margin: 0 0 6px;
    line-height: 1.4;
    letter-spacing: 0;
}}
.card .meta .match-tag {{
    display: inline-block;
    font-family: var(--body);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--bronze);
    border: 1px solid var(--bronze-light);
    padding: 2px 10px;
    border-radius: 4px;
    margin-left: 8px;
    vertical-align: middle;
}}
.card .meta .products {{
    font-family: var(--body);
    font-size: 12px;
    font-weight: 500;
    color: var(--stone);
    margin: 0 0 10px;
    line-height: 1.4;
    letter-spacing: 0.02em;
}}
.card .meta .desc {{
    font-family: var(--body);
    font-size: 13px;
    font-weight: 300;
    color: var(--ash);
    line-height: 1.7;
    margin: 0 0 18px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    letter-spacing: 0.01em;
}}

/* Animated underline link */
.card .meta .detail-link {{
    display: inline-block;
    position: relative;
    font-family: var(--body);
    font-size: 13px;
    font-weight: 500;
    color: var(--bronze);
    text-decoration: none;
    letter-spacing: 0.03em;
    padding-bottom: 2px;
    transition: color 0.3s;
}}
.card .meta .detail-link::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 1px;
    background: var(--bronze);
    transition: width 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}}
.card .meta .detail-link:hover {{
    color: var(--charcoal);
}}
.card .meta .detail-link:hover::after {{
    width: 100%;
    background: var(--charcoal);
}}

/* ════════════════════════════════════════════════════════
   EMPTY STATE
   ════════════════════════════════════════════════════════ */
.empty {{
    text-align: center;
    padding: 140px 20px;
    animation: fadeIn 0.6s ease 0.2s both;
}}
.empty h2 {{
    font-family: var(--display);
    font-size: 32px;
    font-weight: 600;
    color: var(--charcoal);
    margin: 0 0 12px;
    letter-spacing: -0.01em;
}}
.empty p {{
    font-family: var(--body);
    font-size: 16px;
    font-weight: 300;
    color: var(--ash);
    margin: 0;
    letter-spacing: 0.02em;
}}

/* ════════════════════════════════════════════════════════
   PIPELINE — Warm panel
   ════════════════════════════════════════════════════════ */
.pipeline-wrap {{
    max-width: 980px;
    margin: 64px auto 0;
    padding: 0 32px;
}}
.pipeline {{
    background: linear-gradient(160deg, var(--cream) 0%, var(--linen) 100%);
    border: 1px solid var(--silk);
    border-radius: 24px;
    padding: 56px 48px;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
/* Subtle noise on pipeline panel */
.pipeline::after {{
    content: '';
    position: absolute;
    inset: 0;
    background-image: url("{NOISE_SVG}");
    background-size: 256px;
    opacity: 0.015;
    pointer-events: none;
}}
.pipeline .p-title {{
    font-family: var(--display);
    font-size: 30px;
    font-weight: 700;
    color: var(--charcoal);
    margin: 0 0 8px;
    letter-spacing: -0.01em;
    position: relative;
    z-index: 1;
}}
.pipeline .p-sub {{
    font-family: var(--body);
    font-size: 15px;
    font-weight: 300;
    color: var(--ash);
    margin: 0 0 40px;
    letter-spacing: 0.03em;
    position: relative;
    z-index: 1;
}}
.step-card {{
    background: var(--white);
    border-radius: 16px;
    padding: 32px 24px 28px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03),
                0 4px 16px rgba(0,0,0,0.03);
    border: 1px solid rgba(0,0,0,0.03);
    transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
                box-shadow 0.4s;
}}
.step-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.06),
                0 16px 40px rgba(0,0,0,0.04);
}}
.step-card .s-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: var(--charcoal);
    color: var(--white);
    border-radius: 10px;
    font-family: var(--body);
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 16px;
}}
.step-card h4 {{
    font-family: var(--display);
    font-size: 17px;
    font-weight: 700;
    color: var(--charcoal);
    margin: 0 0 8px;
}}
.step-card p {{
    font-family: var(--body);
    font-size: 13px;
    color: var(--ash);
    margin: 0;
    line-height: 1.6;
    font-weight: 300;
    letter-spacing: 0.02em;
}}

/* ════════════════════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════════════════════ */
.site-footer {{
    max-width: 980px;
    margin: 100px auto 0;
    padding: 24px 32px 56px;
    border-top: 1px solid var(--linen);
    text-align: center;
}}
.site-footer p {{
    font-family: var(--body);
    font-size: 11px;
    font-weight: 400;
    color: var(--mist);
    margin: 0;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

/* ════════════════════════════════════════════════════════
   STREAMLIT OVERRIDES
   ════════════════════════════════════════════════════════ */
div[data-testid="stHorizontalBlock"] {{
    gap: 22px !important;
}}
div[data-testid="stSpinner"] {{
    text-align: center;
}}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Utilities ──────────────────────────────────────────


def img_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def truncate(text: str, n: int = 140) -> str:
    return text if len(text) <= n else text[:n] + "…"


# ─── Components ─────────────────────────────────────────


def render_hero():
    st.markdown(
        """
    <div class="hero">
        <p class="hero-overline">Komatsu Wall Industry</p>
        <h1 class="hero-headline">空間を、直感で見つける。</h1>
        <p class="hero-subhead">製品名でも、雰囲気でも。<br>
        イメージするだけで、理想の施工事例に出会えます。</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_search():
    query = st.text_input(
        "search",
        placeholder="明るく開放的なオフィス、木目調の温かい空間…",
        key="search_query",
        label_visibility="collapsed",
    )

    suggestions = [
        "開放的なオフィス",
        "和モダンな内装",
        "ガラスで仕切られた会議室",
        "温かみのある木目調",
        "ホテルライクなロビー",
        "明るい教室",
    ]
    cols = st.columns(len(suggestions))
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s, key=f"sg_{i}"):
                st.session_state["search_query"] = s
                st.rerun()

    return query


def render_card(r: dict, card_index: int = 0):
    path = r.get("image_path", "")
    if path and Path(path).exists():
        b64 = img_b64(path)
        thumb = (
            f'<img class="thumb" src="data:image/jpeg;base64,{b64}" alt="">'
            if b64
            else '<div class="thumb-empty"></div>'
        )
    else:
        thumb = '<div class="thumb-empty"></div>'

    dist = r.get("distance", 1.0)
    pct = max(0, int((1 - dist) * 100))

    # Score bar — warm gradient
    if pct >= 80:
        bar_bg = "linear-gradient(90deg, #9a7b5b, #c4a882)"
    elif pct >= 60:
        bar_bg = "linear-gradient(90deg, #b0b0b0, #d8d4ce)"
    else:
        bar_bg = "linear-gradient(90deg, #d8d4ce, #eae6df)"

    name = r.get("project_name", "")
    products = r.get("products", "")
    desc = truncate(r.get("description", ""), 140)
    url = r.get("url", "#")

    st.markdown(
        f"""
    <div class="card" style="--i:{card_index}">
        <div class="thumb-wrap">
            {thumb}
            <div class="score-line" style="width:{pct}%;background:{bar_bg};"></div>
        </div>
        <div class="meta">
            <p class="name">{name}<span class="match-tag">{pct}%</span></p>
            <p class="products">{products}</p>
            <p class="desc">{desc}</p>
            <a class="detail-link" href="{url}" target="_blank">さらに詳しく</a>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_results(results: list[dict], query: str):
    st.markdown(
        f"""
    <div class="results-bar">
        <span class="r-count">{len(results)}件の施工事例</span>
        <span class="r-query">「{query}」</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    card_idx = 0
    for row in range(0, len(results), 3):
        cols = st.columns(3, gap="medium")
        for i, col in enumerate(cols):
            idx = row + i
            if idx < len(results):
                with col:
                    render_card(results[idx], card_index=card_idx)
                    card_idx += 1


def render_pipeline():
    st.markdown(
        """
    <div class="pipeline-wrap">
    <div class="pipeline">
        <p class="p-title">はじめに、データを準備する。</p>
        <p class="p-sub">3つのステップで、空間検索を可能にします。</p>
    </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    cols = st.columns(3, gap="medium")
    steps = [
        ("1", "収集", "施工事例の画像とメタデータを自動取得"),
        ("2", "解析", "Gemini が画像から空間の特徴を読み解く"),
        ("3", "構築", "ベクトルインデックスとして検索可能に"),
    ]
    for i, (num, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(
                f"""
            <div class="step-card">
                <div class="s-num">{num}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("収集を開始", use_container_width=True):
            with st.spinner("施工事例を収集しています…"):
                from scraper import run_scraper

                cases = run_scraper()
                st.success(f"{len(cases)} 件を収集")
    with c2:
        if st.button("解析を開始", use_container_width=True):
            with st.spinner("Gemini で画像を解析しています…"):
                from enricher import run_enricher

                enriched = run_enricher()
                st.success(f"{len(enriched)} 件を解析")
    with c3:
        if st.button("構築を開始", use_container_width=True):
            with st.spinner("インデックスを構築しています…"):
                from search import build_index

                collection = build_index()
                st.success(f"構築完了 — {collection.count()} 件")


def render_footer():
    st.markdown(
        """
    <div class="site-footer">
        <p>Komatsu Wall &mdash; Gemini Embedding &amp; ChromaDB</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─── State ──────────────────────────────────────────────


def index_ready() -> bool:
    db = Path(__file__).parent / "data" / "chroma_db"
    if not db.exists():
        return False
    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(db))
        names = [c.name for c in client.list_collections()]
        if "komatsu_cases" in names:
            return client.get_collection("komatsu_cases").count() > 0
    except Exception:
        pass
    return False


# ─── Main ───────────────────────────────────────────────


def main():
    render_hero()
    query = render_search()

    if query:
        if index_ready():
            with st.spinner(""):
                from search import search as vector_search

                results = vector_search(query, n_results=12)
            if results:
                render_results(results, query)
            else:
                st.markdown(
                    '<div class="empty"><h2>一致する事例が見つかりませんでした。</h2>'
                    "<p>別のキーワードや表現で試してみてください。</p></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="empty"><h2>検索の準備ができていません。</h2>'
                "<p>下のパイプラインからデータを構築してください。</p></div>",
                unsafe_allow_html=True,
            )

    if not index_ready():
        render_pipeline()

    render_footer()


if __name__ == "__main__":
    main()
