import streamlit as st
import time
from pipeline import research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NEXUS // Research Agent",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #050a0f;
    color: #c8d8e8;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, #00ffe120 0%, transparent 60%),
        radial-gradient(ellipse 60% 30% at 80% 100%, #ff00c820 0%, transparent 50%),
        #050a0f;
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; }

/* ── Scanline overlay ── */
.stApp::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,200,0.015) 2px,
        rgba(0,255,200,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── Hero header ── */
.nexus-header {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}

.nexus-logo {
    font-family: 'Orbitron', monospace;
    font-size: 4.5rem;
    font-weight: 900;
    letter-spacing: 0.3em;
    background: linear-gradient(135deg, #00ffe1 0%, #00b4ff 40%, #ff00c8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    filter: drop-shadow(0 0 30px #00ffe180);
    animation: flicker 6s infinite;
}

@keyframes flicker {
    0%, 95%, 100% { opacity: 1; }
    96% { opacity: 0.85; }
    97% { opacity: 1; }
    98% { opacity: 0.9; }
}

.nexus-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.4em;
    color: #00ffe180;
    margin-top: 0.5rem;
    text-transform: uppercase;
}

.nexus-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00ffe1, #ff00c8, transparent);
    margin: 1.5rem auto;
    max-width: 600px;
    opacity: 0.6;
}

/* ── Input panel ── */
.input-panel {
    background: rgba(0, 20, 35, 0.85);
    border: 1px solid #00ffe130;
    border-radius: 4px;
    padding: 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.input-panel::before {
    content: '';
    position: absolute; top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00ffe1, #ff00c8);
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input {
    background: rgba(0,255,225,0.04) !important;
    border: 1px solid #00ffe150 !important;
    border-radius: 2px !important;
    color: #45047a !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    caret-color: #00ffe1;
    padding: 0.75rem 1rem !important;
    letter-spacing: 0.05em;
}
.stTextInput > div > div > input:focus {
    border-color: #00ffe1 !important;
    box-shadow: 0 0 0 2px #00ffe120, 0 0 20px #00ffe130 !important;
}
.stTextInput label {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.25em !important;
    color: #00ffe1a0 !important;
    text-transform: uppercase;
}

/* ── Button ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #00ffe1 !important;
    color: #00ffe1 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase;
    padding: 0.8rem 2.5rem !important;
    border-radius: 2px !important;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
    width: 100%;
}
.stButton > button:hover {
    background: rgba(0,255,225,0.08) !important;
    box-shadow: 0 0 30px #00ffe140, inset 0 0 20px #00ffe110 !important;
    border-color: #00ffe1 !important;
    color: #ffffff !important;
}
.stButton > button:active {
    background: rgba(0,255,225,0.15) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(0, 12, 25, 0.9);
    border: 1px solid #1a3a5c;
    border-radius: 3px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.4s, box-shadow 0.4s;
}
.step-card.active {
    border-color: #00ffe1;
    box-shadow: 0 0 25px #00ffe120, inset 0 0 30px #00ffe108;
}
.step-card.done {
    border-color: #00ffe150;
    box-shadow: 0 0 10px #00ffe110;
}
.step-card.error {
    border-color: #ff00c8;
    box-shadow: 0 0 15px #ff00c830;
}

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.step-num {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    color: #00ffe1;
    letter-spacing: 0.15em;
    opacity: 0.7;
}
.step-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.1em;
}
.step-status {
    margin-left: auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #ffffff40; }
.status-running  { color: #00ffe1; animation: pulse 1s infinite; }
.status-done     { color: #00ffe1; }
.status-error    { color: #ff00c8; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Progress bar override ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00ffe1, #00b4ff, #ff00c8) !important;
}

/* ── Expander overrides ── */
.streamlit-expanderHeader {
    background: rgba(0,255,225,0.04) !important;
    border: 1px solid #00ffe120 !important;
    border-radius: 2px !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: #00ffe1 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
}
.streamlit-expanderContent {
    background: rgba(0,8,18,0.95) !important;
    border: 1px solid #00ffe115 !important;
    border-top: none !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #a0c8d8 !important;
    line-height: 1.7;
}

/* ── Final report card ── */
.report-card {
    background: rgba(0, 10, 20, 0.95);
    border: 1px solid #ff00c860;
    border-radius: 3px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: 0 0 40px #ff00c820;
    position: relative;
}
.report-card::before {
    content: 'FINAL REPORT';
    position: absolute;
    top: -0.7rem; left: 1.5rem;
    background: #050a0f;
    padding: 0 0.75rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: #ff00c8;
}
.report-card::after {
    content: '';
    position: absolute; top: 0; right: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #ff00c8, #00ffe1);
}

/* ── Feedback card ── */
.feedback-card {
    background: rgba(0, 10, 20, 0.95);
    border: 1px solid #00b4ff50;
    border-radius: 3px;
    padding: 2rem;
    margin-top: 1.5rem;
    box-shadow: 0 0 30px #00b4ff15;
    position: relative;
}
.feedback-card::before {
    content: 'CRITIC ANALYSIS';
    position: absolute;
    top: -0.7rem; left: 1.5rem;
    background: #050a0f;
    padding: 0 0.75rem;
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: #00b4ff;
}

/* ── Metric boxes ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}
.metric-box {
    flex: 1;
    background: rgba(0,255,225,0.04);
    border: 1px solid #00ffe120;
    border-radius: 2px;
    padding: 1rem;
    text-align: center;
}
.metric-val {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00ffe1;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: #ffffff50;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

/* ── Glitch on label ── */
.glitch {
    position: relative;
}
.glitch::after {
    content: attr(data-text);
    position: absolute; top: 0; left: 2px;
    background: linear-gradient(135deg, #00ffe1, #00b4ff, #ff00c8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: glitch 4s infinite;
    opacity: 0.5;
}
@keyframes glitch {
    0%,90%,100% { clip-path: none; transform: none; }
    91% { clip-path: inset(20% 0 60% 0); transform: translate(-2px); }
    92% { clip-path: inset(60% 0 10% 0); transform: translate(2px); }
    93% { clip-path: none; transform: none; }
}

/* ── Corner decorations ── */
.corner-dec {
    position: relative;
    padding: 1rem;
}
.corner-dec::before, .corner-dec::after {
    content: '';
    position: absolute;
    width: 12px; height: 12px;
}
.corner-dec::before {
    top: 0; left: 0;
    border-top: 2px solid #00ffe1;
    border-left: 2px solid #00ffe1;
}
.corner-dec::after {
    bottom: 0; right: 0;
    border-bottom: 2px solid #ff00c8;
    border-right: 2px solid #ff00c8;
}

/* ── Content text ── */
.content-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    color: #9ab8c8;
    line-height: 1.8;
    white-space: pre-wrap;
    word-wrap: break-word;
}

/* ── Section label ── */
.section-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: #00ffe180;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #00ffe130, transparent);
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False
if "state" not in st.session_state:
    st.session_state.state = {}
if "run_time" not in st.session_state:
    st.session_state.run_time = 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nexus-header">
    <div class="nexus-logo glitch" data-text="NEXUS">NEXUS</div>
    <div class="nexus-sub">// Multi-Agent Research Intelligence System //</div>
    <div class="nexus-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Input Panel ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-panel corner-dec">', unsafe_allow_html=True)
st.markdown('<div class="section-label">⬡ Target Acquisition</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    topic = st.text_input(
        "RESEARCH TARGET",
        placeholder="e.g. Quantum computing breakthroughs 2025...",
        label_visibility="visible"
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⬡ INITIATE", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Pipeline Steps Display ────────────────────────────────────────────────────
STEPS = [
    ("01", "SEARCH AGENT",  "Scanning web for intelligence..."),
    ("02", "READER AGENT",  "Scraping & extracting deep content..."),
    ("03", "WRITER AGENT",  "Synthesizing research report..."),
    ("04", "CRITIC AGENT",  "Evaluating report quality..."),
]

def render_step(idx, num, title, desc, status="waiting", content=None):
    card_class = {"waiting": "", "running": "active", "done": "done", "error": "error"}[status]
    status_label = {
        "waiting": '<span class="step-status status-waiting">[ STANDBY ]</span>',
        "running": '<span class="step-status status-running">[ PROCESSING ]</span>',
        "done":    '<span class="step-status status-done">[ COMPLETE ]</span>',
        "error":   '<span class="step-status status-error">[ ERROR ]</span>',
    }[status]

    html = f"""
    <div class="step-card {card_class}">
        <div class="step-header">
            <span class="step-num">STEP {num}</span>
            <span class="step-title">{title}</span>
            {status_label}
        </div>
        <div style="font-size:0.78rem;color:#ffffff40;font-family:'Share Tech Mono',monospace;letter-spacing:0.05em;">
            {desc}
        </div>
    </div>
    """
    return html

# ── Render static pipeline grid when idle ────────────────────────────────────
if not st.session_state.pipeline_done:
    st.markdown('<div class="section-label">⬡ Pipeline Architecture</div>', unsafe_allow_html=True)
    for i, (num, title, desc) in enumerate(STEPS):
        st.markdown(render_step(i, num, title, desc, "waiting"), unsafe_allow_html=True)

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.pipeline_done = False
    st.session_state.state = {}

    st.markdown('<div class="section-label">⬡ Pipeline Execution</div>', unsafe_allow_html=True)

    step_placeholders = []
    for i, (num, title, desc) in enumerate(STEPS):
        ph = st.empty()
        ph.markdown(render_step(i, num, title, desc, "waiting"), unsafe_allow_html=True)
        step_placeholders.append(ph)

    progress_ph = st.empty()
    progress_ph.progress(0)
    log_ph = st.empty()

    result_state = {}
    error_msg = None
    start_time = time.time()

    try:
        # ── Step 1: Search ──────────────────────────────────────────────────
        step_placeholders[0].markdown(render_step(0, *STEPS[0], "running"), unsafe_allow_html=True)
        log_ph.markdown('<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#00ffe180;">▶ Activating search agent...</p>', unsafe_allow_html=True)
        progress_ph.progress(5)

        from agents import search_agent
        sa = search_agent()
        sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})
        result_state["search_results"] = sr['messages'][-1].content

        step_placeholders[0].markdown(render_step(0, *STEPS[0], "done"), unsafe_allow_html=True)
        progress_ph.progress(25)

        # ── Step 2: Reader ──────────────────────────────────────────────────
        step_placeholders[1].markdown(render_step(1, *STEPS[1], "running"), unsafe_allow_html=True)
        log_ph.markdown('<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#00ffe180;">▶ Reader agent scraping target URL...</p>', unsafe_allow_html=True)

        from agents import reader_agent
        ra = reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"Based on the following search results about '{topic}',"
            f"Pick the most relevant URL and scrape it for deeper content. \n\n"
            f"Search Results: \n{result_state['search_results'][:800]}")]})
        result_state["scraped_content"] = rr['messages'][-1].content

        step_placeholders[1].markdown(render_step(1, *STEPS[1], "done"), unsafe_allow_html=True)
        progress_ph.progress(50)

        # ── Step 3: Writer ──────────────────────────────────────────────────
        step_placeholders[2].markdown(render_step(2, *STEPS[2], "running"), unsafe_allow_html=True)
        log_ph.markdown('<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#00ffe180;">▶ Writer agent synthesizing report...</p>', unsafe_allow_html=True)

        from agents import writer_chain
        combined = [
            f"SEARCH RESULTS: \n {result_state['search_results']} \n\n"
            f"DETAILED SEARCH RESULTS SCRAPED: \n {result_state['scraped_content']}"
        ]
        result_state["report"] = writer_chain.invoke({"topic": topic, "research": combined})

        step_placeholders[2].markdown(render_step(2, *STEPS[2], "done"), unsafe_allow_html=True)
        progress_ph.progress(75)

        # ── Step 4: Critic ──────────────────────────────────────────────────
        step_placeholders[3].markdown(render_step(3, *STEPS[3], "running"), unsafe_allow_html=True)
        log_ph.markdown('<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#00ffe180;">▶ Critic agent evaluating output...</p>', unsafe_allow_html=True)

        from agents import critic_chain
        result_state["feedback"] = critic_chain.invoke({"report": result_state["report"]})

        step_placeholders[3].markdown(render_step(3, *STEPS[3], "done"), unsafe_allow_html=True)
        progress_ph.progress(100)
        log_ph.markdown('<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#00ffe1;">✓ Pipeline complete.</p>', unsafe_allow_html=True)

        st.session_state.state = result_state
        st.session_state.pipeline_done = True
        st.session_state.run_time = round(time.time() - start_time, 1)

    except Exception as e:
        error_msg = str(e)
        log_ph.markdown(f'<p style="font-family:Share Tech Mono;font-size:0.75rem;color:#ff00c8;">✗ ERROR: {error_msg}</p>', unsafe_allow_html=True)
        progress_ph.progress(0)

elif run_btn and not topic.strip():
    st.markdown('<p style="font-family:Share Tech Mono;font-size:0.8rem;color:#ff00c8;margin-top:0.5rem;">⚠ No target specified. Enter a research topic.</p>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.pipeline_done and st.session_state.state:
    s = st.session_state.state

    # Metrics
    word_count = len(str(s.get("report", "")).split())
    search_len = len(str(s.get("search_results", "")))
    scraped_len = len(str(s.get("scraped_content", "")))

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-box">
            <div class="metric-val">{st.session_state.run_time}s</div>
            <div class="metric-label">Execution Time</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{word_count}</div>
            <div class="metric-label">Report Words</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{search_len:,}</div>
            <div class="metric-label">Search Chars</div>
        </div>
        <div class="metric-box">
            <div class="metric-val">{scraped_len:,}</div>
            <div class="metric-label">Scraped Chars</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Raw data expanders
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("⬡ SEARCH AGENT OUTPUT"):
            st.markdown(f'<div class="content-text">{s.get("search_results", "—")}</div>', unsafe_allow_html=True)
    with col2:
        with st.expander("⬡ READER AGENT OUTPUT"):
            st.markdown(f'<div class="content-text">{s.get("scraped_content", "—")}</div>', unsafe_allow_html=True)

    # Final report
    st.markdown(f"""
    <div class="report-card">
        <div class="content-text">{s.get("report", "—")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Critic feedback
    st.markdown(f"""
    <div class="feedback-card">
        <div class="content-text">{s.get("feedback", "—")}</div>
    </div>
    """, unsafe_allow_html=True)

    # Reset
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬡ NEW RESEARCH TARGET"):
        st.session_state.pipeline_done = False
        st.session_state.state = {}
        st.rerun()