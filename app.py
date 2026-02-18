"""
小松ウオール工業 施工事例検索
Architectural Monograph Design
"""

import base64
import io
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
HERO_IMAGE = str(DATA_DIR / "images" / "3460_0.jpg")  # mosaic glass corridor

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
    """
<style>
/* ── Typography ── */
@import url('https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@400;500;600;700;900&family=Zen+Kaku+Gothic+New:wght@300;400;500;700&display=swap');

:root {
    --display: "Times New Roman", "Zen Old Mincho", serif;
    --body: "Helvetica Neue", "Zen Kaku Gothic New", sans-serif;

    /* Ethereal Glass Palette */
    --ink: #1e293b;       /* Dark Slate */
    --charcoal: #334155;  /* Slate */
    --stone: #64748b;     /* Light Slate */
    --ash: #94a3b8;       /* Blue Grey */
    --mist: #cbd5e1;      /* Light Blue Grey */
    --silk: #e2e8f0;      /* Very Light Blue Grey */
    --linen: #f1f5f9;     
    --cream: #f8fafc;
    --white: #ffffff;
    
    /* Glass Effect */
    --glass-bg: rgba(255, 255, 255, 0.65);
    --glass-border: rgba(255, 255, 255, 0.4);
    --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
    --blur: blur(12px);

    /* Accent — Soft Blue/Silver */
    --accent: #60a5fa;
    --accent-light: #bfdbfe;
    --accent-glow: rgba(96, 165, 250, 0.15);
}

html, body, [class*="css"] {
    font-family: var(--body) !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
    color: var(--charcoal);
}

/* ── Streamlit chrome — hide everything ── */
#MainMenu, footer, header, .stDeployButton,
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

.stApp {
    background: radial-gradient(circle at top left, #f8fafc, #e2e8f0);
    background-attachment: fixed;
}
.stApp > header { background: transparent !important; }

.main .block-container {
    max-width: 100%;
    padding: 0;
}

/* ── Animations ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* ════════════════════════════════════════════════════════
   HERO — Ethereal, Air, Light
   ════════════════════════════════════════════════════════ */
.hero {
    padding: 160px 40px 100px;
    text-align: center;
    position: relative;
    overflow: hidden;
    background: transparent;
}

.hero-overline {
    font-family: var(--body);
    font-size: 13px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ash);
    margin: 0 0 24px;
    position: relative;
    z-index: 5;
    animation: fadeUp 1.0s cubic-bezier(0.2, 1, 0.3, 1) 0.1s both;
}

.hero-headline {
    font-family: var(--display);
    font-size: 80px;
    font-weight: 400; /* Lighter weight for elegance */
    letter-spacing: -0.01em;
    line-height: 1.1;
    margin: 0 0 24px;
    position: relative;
    z-index: 5;
    color: var(--charcoal);
    animation: fadeUp 1.0s cubic-bezier(0.2, 1, 0.3, 1) 0.2s both;
    text-shadow: 0 10px 30px rgba(100,116,139,0.1);
}

.hero-subhead {
    font-family: var(--body);
    font-size: 16px;
    font-weight: 400;
    color: var(--stone);
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.8;
    letter-spacing: 0.05em;
    position: relative;
    z-index: 5;
    animation: fadeUp 1.0s cubic-bezier(0.2, 1, 0.3, 1) 0.3s both;
}

/* ════════════════════════════════════════════════════════
   SEARCH — Floating Glass Capsule
   ════════════════════════════════════════════════════════ */
div[data-testid="stTextInput"] {
    max-width: 680px;
    margin: 0 auto;
}
div[data-testid="stTextInput"] > div > div > input {
    font-family: var(--body) !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 18px 32px !important;
    border-radius: 50px !important; /* Capsule */
    border: 1px solid var(--glass-border) !important;
    background: var(--glass-bg) !important;
    backdrop-filter: var(--blur) !important;
    -webkit-backdrop-filter: var(--blur) !important;
    color: var(--charcoal) !important;
    letter-spacing: 0.03em !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--glass-shadow), 
                0 4px 12px rgba(0,0,0,0.02) !important;
}
div[data-testid="stTextInput"] > div > div > input::placeholder {
    color: var(--ash) !important;
    font-weight: 300 !important;
}
div[data-testid="stTextInput"] > div > div > input:focus {
    background: rgba(255,255,255,0.85) !important;
    border-color: var(--white) !important;
    box-shadow: var(--glass-shadow),
                0 0 0 4px var(--accent-glow) !important;
    outline: none !important;
    transform: translateY(-2px);
}
div[data-testid="stTextInput"] > label {
    display: none !important;
}

/* ════════════════════════════════════════════════════════
   CHIPS — Minimalist Pills
   ════════════════════════════════════════════════════════ */
div[data-testid="stButton"] > button {
    font-family: var(--body) !important;
    background: rgba(255,255,255,0.4) !important;
    color: var(--stone) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 30px !important;
    padding: 6px 18px !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s ease !important;
    backdrop-filter: blur(4px);
}
div[data-testid="stButton"] > button:hover {
    color: var(--ink) !important;
    background: rgba(255,255,255,0.8) !important;
    border-color: var(--white) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active {
    transform: scale(0.98) translateY(0) !important;
}

/* ════════════════════════════════════════════════════════
   RESULTS HEADER
   ════════════════════════════════════════════════════════ */
.results-bar {
    max-width: 1100px;
    margin: 40px auto 0;
    padding: 0 32px 20px;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.3); /* Subtle divider */
}
.results-bar .r-count {
    font-family: var(--display);
    font-size: 24px;
    font-weight: 400;
    color: var(--charcoal);
}
.results-bar .r-query {
    font-size: 13px;
    color: var(--ash);
    font-weight: 300;
}

/* ════════════════════════════════════════════════════════
   GALLERY CARDS — Glassmorphism
   ════════════════════════════════════════════════════════ */
.card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 32px;
    cursor: default;
    position: relative;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 
                0 2px 4px -1px rgba(0, 0, 0, 0.02);
    transition: all 0.4s cubic-bezier(0.2, 1, 0.3, 1);
    animation: fadeUp 0.8s cubic-bezier(0.2, 1, 0.3, 1) both;
}
.card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.8);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 
                0 10px 10px -5px rgba(0, 0, 0, 0.02);
    border-color: rgba(255, 255, 255, 0.9);
}

.card .thumb-wrap {
    position: relative;
    overflow: hidden;
    margin: 8px 8px 0; /* Padding around image */
    border-radius: 16px;
}
.card .thumb {
    width: 100%;
    height: 240px;
    object-fit: cover;
    display: block;
    transition: transform 0.6s ease;
}
.card:hover .thumb {
    transform: scale(1.04);
}
.card .thumb-empty {
    width: 100%;
    height: 240px;
    background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
}

/* Score bar */
.card .score-line {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 3px;
    z-index: 2;
    background: linear-gradient(90deg, #93c5fd, #60a5fa);
    opacity: 0.8;
}

/* Metadata */
.card .meta {
    padding: 20px 24px 24px;
}
.card .meta .name {
    font-family: var(--display);
    font-size: 18px;
    font-weight: 500;
    color: var(--ink);
    margin: 0 0 6px;
    line-height: 1.3;
}
.card .meta .match-tag {
    display: inline-block;
    font-family: var(--body);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.05em;
    color: var(--accent);
    background: rgba(96, 165, 250, 0.1);
    padding: 3px 8px;
    border-radius: 12px;
    margin-left: 8px;
    vertical-align: middle;
}
.card .meta .products {
    font-family: var(--body);
    font-size: 11px;
    font-weight: 500;
    color: var(--stone);
    margin: 0 0 12px;
    letter-spacing: 0.02em;
}
.card .meta .desc {
    font-family: var(--body);
    font-size: 13px;
    font-weight: 400;
    color: var(--stone);
    line-height: 1.6;
    margin: 0 0 16px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Link */
.card .meta .detail-link {
    font-family: var(--body);
    font-size: 12px;
    font-weight: 600;
    color: var(--accent);
    text-decoration: none;
    letter-spacing: 0.02em;
    transition: all 0.2s;
}
.card .meta .detail-link:hover {
    color: var(--charcoal);
}

/* ════════════════════════════════════════════════════════
   PIPELINE — Minimal Glass
   ════════════════════════════════════════════════════════ */
.pipeline-wrap {
    max-width: 900px;
    margin: 64px auto 0;
    padding: 0 32px;
}
.pipeline {
    padding: 40px 0;
    text-align: center;
}
.pipeline .p-title {
    font-family: var(--display);
    font-size: 26px;
    font-weight: 400;
    color: var(--charcoal);
    margin: 0 0 8px;
}
.pipeline .p-sub {
    font-family: var(--body);
    font-size: 14px;
    font-weight: 300;
    color: var(--stone);
    margin: 0 0 40px;
}
.step-card {
    background: rgba(255,255,255,0.4);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 16px;
    padding: 24px 16px;
    text-align: center;
    transition: all 0.3s ease;
}
.step-card:hover {
    background: rgba(255,255,255,0.8);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
}
.step-card .s-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--silk);
    color: var(--stone);
    border-radius: 50%;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 12px;
}
.step-card h4 {
    font-family: var(--display);
    font-size: 16px;
    font-weight: 500;
    color: var(--charcoal);
    margin: 0 0 6px;
}
.step-card p {
    font-size: 12px;
    color: var(--ash);
    margin: 0;
    line-height: 1.5;
}

/* ════════════════════════════════════════════════════════
   FOOTER
   ════════════════════════════════════════════════════════ */
.site-footer {
    max-width: 900px;
    margin: 80px auto 0;
    padding: 24px 32px 40px;
    border-top: 1px solid rgba(255,255,255,0.3);
    text-align: center;
}
.site-footer p {
    font-family: var(--display);
    font-size: 12px;
    color: var(--ash);
    font-style: italic;
    opacity: 0.7;
}

/* ════════════════════════════════════════════════════════
   STREAMLIT OVERRIDES
   ════════════════════════════════════════════════════════ */
div[data-testid="stHorizontalBlock"] {
    gap: 16px !important;
}
div[data-testid="stSpinner"] {
    text-align: center;
    color: var(--stone) !important;
}
/* ════════════════════════════════════════════════════════
   DETAIL VIEW — Refined
   ════════════════════════════════════════════════════════ */
.detail-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
    margin-bottom: 60px;
    animation: fadeUp 0.6s cubic-bezier(0.2, 1, 0.3, 1) both;
}

.detail-title {
    font-family: var(--display);
    font-size: 36px;
    font-weight: 500;
    color: var(--ink);
    margin: 0 0 16px;
    line-height: 1.2;
}

.detail-meta {
    font-family: var(--body);
    font-size: 14px;
    color: var(--stone);
    margin-bottom: 32px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
}

.product-badge {
    display: inline-block;
    padding: 4px 12px;
    background: var(--linen);
    color: var(--charcoal);
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.02em;
    border: 1px solid var(--silk);
}
.location-badge {
    display: inline-block;
    color: var(--ash);
    font-weight: 500;
    margin-right: 8px;
}

.detail-desc {
    font-family: var(--body);
    font-size: 16px;
    line-height: 1.9;
    color: var(--charcoal);
    margin-top: 32px;
    padding-top: 32px;
    border-top: 1px solid var(--silk);
}

.gallery-label {
    font-family: var(--body);
    font-size: 12px;
    color: var(--ash);
    margin-bottom: 4px;
    display: block;
}


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


@st.cache_data
def hero_img_b64(path: str, width: int = 1600) -> str:
    """Resize hero image for lightweight base64 embedding."""
    try:
        img = Image.open(path)
        ratio = width / img.width
        img = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=82, optimize=True)
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""


def truncate(text: str, n: int = 140) -> str:
    return text if len(text) <= n else text[:n] + "…"


# ─── Components ─────────────────────────────────────────


def render_hero():
    # Ethereal design relies on CSS background gradient, no heavy hero image
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



def fix_path(path: str) -> str:
    """
    Fix absolute Windows paths to relative Linux-friendly paths for Streamlit Cloud.
    Converts 'c:\\Users\\...\\data\\images\\xxx.jpg' -> 'data/images/xxx.jpg'
    """
    if not path:
        return ""
    
    # Standardize separators
    p = path.replace("\\", "/")
    
    # If it contains 'data/images', slice from there
    if "data/images" in p:
        return p[p.find("data/images"):]
        
    # Fallback: if it's already a filename or relative
    return p

def render_card(r: dict, card_index: int = 0):
    raw_path = r.get("image_path", "")
    path = fix_path(raw_path)
    
    # Debug info (optional, remove in prod if noisy)
    # st.write(f"Fixed: {path}")

    if path and Path(path).exists():
        b64 = img_b64(path)
        thumb = (
            f'<img class="thumb" src="data:image/jpeg;base64,{b64}" alt="">'
            if b64
            else '<div class="thumb-empty"></div>'
        )
    else:
        # Check if we can find it in 'data/images' by filename
        filename = Path(raw_path).name
        alt_path = f"data/images/{filename}"
        if Path(alt_path).exists():
             b64 = img_b64(alt_path)
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
    # URL link removed in favor of in-app detail view

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
        <span class="r-query">{query}</span>
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
                r = results[idx]
                case_id = r.get("case_id")
                
                with col:
                    render_card(r, card_index=card_idx)
                    
                    # 詳細ボタン (カードの下に配置)
                    # Unique key is essential here
                    if st.button("詳細を見る", key=f"det_btn_{idx}_{case_id}", use_container_width=True):
                        st.session_state["selected_case_id"] = case_id
                        st.rerun()
                    
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
    db = Path(__file__).parent / "data" / "chroma_db_v2"
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


# ─── Data Loading ───────────────────────────────────────

@st.cache_data
def load_filter_options():
    """raw_data.json からフィルタリング用の選択肢を作成する"""
    raw_path = Path(__file__).parent / "data" / "raw_data.json"
    locations = set()
    products = set()
    
    if raw_path.exists():
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if item.get("location"):
                        locations.add(item["location"])
                    for p in item.get("products", []):
                        products.add(p)
        except Exception:
            pass
            
    return sorted(list(locations)), sorted(list(products))


@st.cache_data
def load_case_map():
    """enriched_data.json を読み込んで case_id をキーにした辞書を返す"""
    path = Path(__file__).parent / "data" / "enriched_data.json"
    if not path.exists():
        # enriched がなければ raw_data で代用 (画像はあるはず)
        path = Path(__file__).parent / "data" / "raw_data.json"
    
    mapping = {}
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    mapping[item["case_id"]] = item
        except Exception:
            pass
    return mapping


def render_detail_view(case_id: str):
    case_map = load_case_map()
    case = case_map.get(case_id)
    
    if not case:
        st.error("事例データの読み込みに失敗しました。")
        if st.button("戻る"):
            del st.session_state["selected_case_id"]
            st.rerun()
        return

    # Back button
    if st.button("← 検索結果に戻る", key="back_btn"):
        del st.session_state["selected_case_id"]
        st.rerun()

    # Data preparation
    project_name = case.get('project_name', 'Untitled Project')
    location = case.get('location', '')
    products = case.get('products', [])
    
    # HTML Construction for the Card
    
    # Badges HTML
    badges_html = ""
    for p in products:
        badges_html += f'<span class="product-badge">{p}</span>'
    
    # Location HTML
    loc_html = f'<span class="location-badge">{location}</span>' if location else ""

    # Description
    descriptions = case.get("descriptions", [])
    desc_text = descriptions[0].get("description", "") if descriptions else ""
    
    # Start of Card
    st.markdown(f"""
    <div class="detail-card">
        <h1 class="detail-title">{project_name}</h1>
        <div class="detail-meta">
            {loc_html}
            {badges_html}
        </div>
    """, unsafe_allow_html=True)

    # Main Image (First one)
    image_paths = case.get("local_image_paths", [])
    if image_paths:
        raw_main = image_paths[0]
        main_img_path = fix_path(raw_main)
        
        if Path(main_img_path).exists():
            st.image(main_img_path, use_container_width=True)
            
            # Show products for main image (refined)
            if descriptions:
                main_prods = descriptions[0].get("refined_products", [])
                if main_prods:
                    p_str = ", ".join(main_prods)
                    st.markdown(f'<span class="gallery-label">写っている製品: {p_str}</span>', unsafe_allow_html=True)
        else:
             # Fallback check
             fname = Path(raw_main).name
             alt_main = f"data/images/{fname}"
             if Path(alt_main).exists():
                 st.image(alt_main, use_container_width=True)

    # Description Text
    if desc_text:
        st.markdown(f'<div class="detail-desc">{desc_text}</div>', unsafe_allow_html=True)

    # Close Card div
    st.markdown("</div>", unsafe_allow_html=True)

    # Gallery
    if len(image_paths) > 1:
        st.markdown("### Gallery")
        cols = st.columns(3)
        for i, raw_path in enumerate(image_paths[1:]): # Skip first one
            idx = i + 1 
            path = fix_path(raw_path)
            
            # Fallback path logic
            if not Path(path).exists():
                path = f"data/images/{Path(raw_path).name}"

            with cols[i % 3]:
                if Path(path).exists():
                    st.image(path, use_container_width=True)
                    
                    if idx < len(descriptions):
                        g_prods = descriptions[idx].get("refined_products", [])
                        if g_prods:
                             st.markdown(f"<span class='gallery-label'>製品: {', '.join(g_prods)}</span>", unsafe_allow_html=True)
                        else:
                             st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Similar Search Button
    st.markdown("### この事例にピンときたら")
    if st.button("🔍 この事例に似た案件を探す (More Like This)", type="primary", use_container_width=True):
        st.session_state["similar_query_id"] = case_id
        del st.session_state["selected_case_id"] # 詳細ビューを閉じる
        st.rerun()


# ─── Main ───────────────────────────────────────────────


def main():
    # Session State Initialization
    if "selected_case_id" not in st.session_state:
        st.session_state["selected_case_id"] = None
    if "similar_query_id" not in st.session_state:
        st.session_state["similar_query_id"] = None
    if "search_query" not in st.session_state: # Ensure search_query is initialized
        st.session_state["search_query"] = ""

    # Detail View Rendering
    if st.session_state["selected_case_id"]:
        render_detail_view(st.session_state["selected_case_id"])
        render_footer()
        return

    render_hero()
    
    # 類似検索モードの場合は検索バーに値を入れない、あるいは特別な表示にする
    initial_query = ""
    if st.session_state.get("search_query"):
        initial_query = st.session_state["search_query"]
        
    query = st.text_input(
        "search",
        value=initial_query,
        placeholder="明るく開放的なオフィス、木目調の温かい空間…",
        key="search_input", # keyを変更してsession_stateの競合を避ける
        label_visibility="collapsed",
    )
    
    # 検索バーの下にサジェスト (類似検索時は表示しない？いや、してもいい)
    if not st.session_state["similar_query_id"]:
        render_suggestions()

    # フィルタリングUI
    locations, products = load_filter_options()
    
    with st.expander("詳細検索 (絞り込み)", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            sel_locations = st.multiselect("場所", locations, placeholder="場所を選択...")
        with c2:
            sel_products = st.multiselect("製品", products, placeholder="製品名を選択...")

    # Search Logic
    results = []
    mode_title = ""

    if st.session_state["similar_query_id"]:
        if index_ready():
            with st.spinner("類似案件を探しています..."):
                from search import get_similar_by_id
                # 類似検索実行
                sim_id = st.session_state["similar_query_id"]
                results = get_similar_by_id(sim_id, n_results=100)
                
                # ケースマップからプロジェクト名を取得して表示
                case_map = load_case_map()
                original_case = case_map.get(sim_id)
                p_name = original_case.get("project_name", "選択した事例") if original_case else "選択した事例"
                mode_title = f"「{p_name}」に似た事例"
                
                if query and query != initial_query: # ユーザーが何か入力したら類似検索モード解除
                    st.session_state["similar_query_id"] = None
                    st.session_state["search_query"] = query
                    st.rerun()

    elif query:
        if index_ready():
            with st.spinner(""):
                from search import search as vector_search
                results = vector_search(query, n_results=300)
                mode_title = f"「{query}」"
    
    else:
        # Query is empty: Show ALL items (or a large shuffle)
        if index_ready():
             from search import get_all_items
             results = get_all_items(n_results=300)
             mode_title = "すべての施工事例"

    # Filtering (共通)
    if results:
         # Python側でフィルタリング
        filtered_results = []
        for r in results:
            # 場所フィルタ
            if sel_locations and r.get("location") not in sel_locations:
                continue
            
            # 製品フィルタ
            if sel_products:
                r_prods = r.get("products", "").split("、")
                if not any(sp in r_prods for sp in sel_products):
                    continue
                    
            filtered_results.append(r)
        
        # 上位表示 (全件表示のためスライス制限を解除)
        display_results = filtered_results # Removed [:12] limit
        
        if display_results:
            render_results(display_results, mode_title)
        else:
            st.markdown(
                '<div class="empty"><h2>一致する事例が見つかりませんでした。</h2>'
                "<p>別のキーワードや表現で試してみてください。</p></div>",
                unsafe_allow_html=True,
            )

    elif not index_ready():
        render_pipeline()

    render_footer()


def set_search(query):
    st.session_state["search_query"] = query
    st.session_state["search_input"] = query

def render_suggestions():
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
            st.button(s, key=f"sg_{i}", on_click=set_search, args=(s,))


if __name__ == "__main__":
    main()
