import streamlit as st

st.set_page_config(layout="wide", page_title="Architectural Design Concepts", initial_sidebar_state="expanded")

# Sidebar for theme selection
theme = st.sidebar.radio("Select Concept", ["Brutalist Concrete", "Ethereal Glass", "Midnight Monolith"])

# Mock Data
mock_results = [
    {"title": "Kioicho Office Tower", "tag": "Office", "img": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=600&q=80"},
    {"title": "Aoyama Showroom", "tag": "Commercial", "img": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=600&q=80"},
    {"title": "Ginza Gallery", "tag": "Cultural", "img": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=600&q=80"},
]

# ─── THEME 1: BRUTALIST ───
if theme == "Brutalist Concrete":
    st.markdown("""
    <style>
    .stApp { background-color: #e0e0e0; font-family: 'Courier New', monospace; }
    h1, h2, h3, p, div { color: #000 !important; }
    
    /* Hero */
    .hero {
        padding: 80px 20px;
        border-bottom: 4px solid #000;
        margin-bottom: 40px;
        background: #f4f4f4;
    }
    .hero-title {
        font-size: 64px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -2px;
        line-height: 0.9;
    }
    .hero-sub {
        font-size: 18px;
        margin-top: 20px;
        font-weight: bold;
        background: #000;
        color: #fff !important;
        display: inline-block;
        padding: 4px 12px;
    }
    
    /* Search */
    .search-container {
        border: 4px solid #000;
        background: #fff;
        padding: 10px;
        margin-bottom: 60px;
        box-shadow: 8px 8px 0px #000;
    }
    
    /* Card */
    .card {
        border: 4px solid #000;
        background: #fff;
        padding: 0;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translate(-4px, -4px);
        box-shadow: 8px 8px 0px #000;
    }
    .card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-bottom: 4px solid #000;
        filter: grayscale(100%);
    }
    .card-content { padding: 16px; }
    .card-title { font-weight: 900; font-size: 20px; text-transform: uppercase; }
    .card-tag { font-size: 12px; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="hero"><div class="hero-title">KOMATSU<br>WALL<br>ARCHIVE</div><div class="hero-sub">STRUCTURE / FUNCTION / FORM</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="search-container"><h3>SEARCH_QUERY: [ ____________________ ]</h3></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        d = mock_results[i]
        with col:
            st.markdown(f"""
            <div class="card">
                <img src="{d['img']}" class="card-img">
                <div class="card-content">
                    <div class="card-tag">#{d['tag']}</div>
                    <div class="card-title">{d['title']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── THEME 2: ETHEREAL ───
elif theme == "Ethereal Glass":
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #f8fafc, #e2e8f0);
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Hero */
    .hero {
        padding: 100px 40px;
        text-align: center;
    }
    .hero-title {
        font-family: 'Times New Roman', serif;
        font-size: 56px;
        color: #334155;
        letter-spacing: 0.05em;
        font-weight: normal;
    }
    .hero-sub {
        color: #64748b;
        font-size: 16px;
        margin-top: 16px;
        letter-spacing: 0.2em;
        text-transform: uppercase;
    }
    
    /* Search */
    .search-box {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 50px;
        padding: 20px 40px;
        margin: 0 auto 80px;
        max-width: 600px;
        box-shadow: 0 10px 40px -10px rgba(148, 163, 184, 0.2);
        color: #94a3b8;
    }
    
    /* Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid #fff;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
    }
    .glass-img {
        width: 100%;
        height: 220px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 16px;
        opacity: 0.9;
    }
    .glass-title {
        font-family: 'Times New Roman', serif;
        font-size: 20px;
        color: #1e293b;
    }
    .glass-tag {
        font-size: 11px;
        color: #94a3b8;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="hero"><div class="hero-title">Komatsu Wall</div><div class="hero-sub">Search for clarity</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="search-box">Search for products, places...</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        d = mock_results[i]
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <img src="{d['img']}" class="glass-img">
                <div class="glass-tag">{d['tag']}</div>
                <div class="glass-title">{d['title']}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── THEME 3: MIDNIGHT ───
elif theme == "Midnight Monolith":
    st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #fff; }
    
    /* Hero */
    .hero {
        padding: 120px 20px;
        border-left: 1px solid #333;
        margin-left: 20px;
    }
    .hero-title {
        font-size: 48px;
        font-weight: 300;
        letter-spacing: 0.15em;
        background: linear-gradient(90deg, #fff, #444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        color: #444;
        margin-top: 10px;
        font-family: monospace;
    }
    
    /* Search */
    .dark-search {
        border-bottom: 1px solid #333;
        padding: 10px 0;
        margin: 40px 20px 80px;
        color: #666;
        font-family: monospace;
    }
    
    /* Card */
    .dark-card {
        background: #0a0a0a;
        margin-bottom: 20px;
    }
    .dark-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        filter: brightness(0.7) contrast(1.2);
        transition: filter 0.3s;
    }
    .dark-info {
        padding: 15px 0;
        border-top: 1px solid #222;
        margin-top: -4px; /* close gap */
    }
    .dark-title {
        font-size: 16px;
        letter-spacing: 0.05em;
        color: #ddd;
    }
    .dark-tag {
        font-size: 10px;
        color: #444;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="hero"><div class="hero-title">KOMATSU<br>WALL</div><div class="hero-sub">// ARCHITECTURAL DATABASE_</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="dark-search">>> Enter keywords to search...</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    for i, col in enumerate([c1, c2, c3]):
        d = mock_results[i]
        with col:
            st.markdown(f"""
            <div class="dark-card">
                <img src="{d['img']}" class="dark-img">
                <div class="dark-info">
                    <div class="dark-tag">0{i+1} / {d['tag'].upper()}</div>
                    <div class="dark-title">{d['title']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
