"""
app.py — Fault-Graph AI Streamlit Dashboard
Production-ready multi-tab diagnostic assistant for industrial HVAC assets.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

# Add project root to path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# ─── Page Config (MUST be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="Fault-Graph AI — Industrial Diagnostic Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/ishpreet7226/Fault-Graph",
        "Report a bug": "https://github.com/ishpreet7226/Fault-Graph/issues",
        "About": "Fault-Graph AI — Graph-RAG Industrial Diagnostic System v1.0",
    }
)

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fault_graph")

# ─── CSS Injection ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f1628;
    --bg-card: #141d35;
    --bg-card-hover: #1a2540;
    --accent-cyan: #00d4ff;
    --accent-blue: #4f8eff;
    --accent-purple: #8b5cf6;
    --accent-green: #10d48e;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f0f4ff;
    --text-secondary: #8892b0;
    --text-muted: #546478;
    --border-subtle: rgba(79, 142, 255, 0.15);
    --border-glow: rgba(0, 212, 255, 0.3);
    --shadow-card: 0 8px 32px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 30px rgba(0, 212, 255, 0.15);
    --gradient-hero: linear-gradient(135deg, #0a0e1a 0%, #0f1628 50%, #111827 100%);
    --gradient-card: linear-gradient(135deg, #141d35 0%, #1a2540 100%);
    --gradient-accent: linear-gradient(90deg, #00d4ff, #4f8eff);
    --gradient-danger: linear-gradient(90deg, #ef4444, #dc2626);
    --gradient-success: linear-gradient(90deg, #10d48e, #059669);
    --gradient-warning: linear-gradient(90deg, #f59e0b, #d97706);
}

/* ── Global Resets ── */
html, body, .stApp {
    background: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Tab Styling ── */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-subtle);
    padding: 4px 8px 0;
    border-radius: 12px 12px 0 0;
}

[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.3s ease !important;
    border-radius: 8px 8px 0 0 !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: var(--accent-cyan) !important;
    background: rgba(0, 212, 255, 0.08) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #4f8eff22) !important;
    border: 1px solid var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    transition: all 0.3s ease !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.15) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff44, #4f8eff44) !important;
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Primary button variant ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00d4ff, #4f8eff) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
}

/* ── Input fields ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1.5px dashed var(--border-glow) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-cyan) !important;
    box-shadow: var(--shadow-glow) !important;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
    color: var(--accent-cyan) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.8rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border-subtle) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}

/* ── Code blocks ── */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: #0a0e1a !important;
    color: var(--accent-cyan) !important;
}

/* ── JSON viewer ── */
[data-testid="stJson"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-subtle); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-blue); }
</style>
""", unsafe_allow_html=True)


# ─── Helper: Severity Color ───────────────────────────────────────────────────
def severity_color(severity: str) -> str:
    return {
        "critical": "#ef4444",
        "high": "#f59e0b",
        "medium": "#3b82f6",
        "low": "#10d48e",
        "unknown": "#8892b0",
    }.get(severity.lower(), "#8892b0")


def severity_emoji(severity: str) -> str:
    return {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🔵",
        "low": "🟢",
        "unknown": "⚫",
    }.get(severity.lower(), "⚫")


# ─── Cached Resource Loaders ──────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_graph():
    """Load the knowledge graph (cached, built once)."""
    try:
        from src.graph_builder import build_graph
        G = build_graph()
        return G
    except Exception as e:
        logger.error(f"Graph load failed: {e}")
        return None


@st.cache_resource(show_spinner=False)
def load_vector_stores():
    """Initialize ChromaDB vector stores (cached)."""
    try:
        from src.vector_store import initialize_stores
        return initialize_stores()
    except Exception as e:
        logger.error(f"Vector store init failed: {e}")
        return None, None


@st.cache_data(show_spinner=False)
def load_maintenance_logs():
    """Load raw maintenance logs JSON."""
    logs_path = ROOT_DIR / "data" / "logs" / "maintenance_logs.json"
    if logs_path.exists():
        with open(logs_path) as f:
            return json.load(f)
    return {}


# ─── Sidebar ──────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 1.2rem 0.5rem 1rem;">
            <div style="font-size:2.5rem; margin-bottom:0.3rem;">⚡</div>
            <h2 style="color:#00d4ff; font-size:1.3rem; font-weight:800; margin:0; letter-spacing:0.05em;">
                Fault-Graph AI
            </h2>
            <p style="color:#8892b0; font-size:0.72rem; margin-top:0.3rem; letter-spacing:0.08em;">
                INDUSTRIAL DIAGNOSTIC SYSTEM
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # System status indicators
        st.markdown("### 🖥 System Status")

        G = load_graph()
        if G:
            node_count = G.number_of_nodes()
            edge_count = G.number_of_edges()
            st.markdown(f"""
            <div style="background:rgba(16,212,142,0.1); border:1px solid rgba(16,212,142,0.3);
                        border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                <div style="color:#10d48e; font-size:0.75rem; font-weight:600; letter-spacing:0.08em;">
                    ● KNOWLEDGE GRAPH ONLINE
                </div>
                <div style="color:#8892b0; font-size:0.72rem; margin-top:0.3rem;">
                    {node_count} nodes · {edge_count} edges
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3);
                        border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                <div style="color:#ef4444; font-size:0.75rem; font-weight:600;">⚠ GRAPH OFFLINE</div>
            </div>
            """, unsafe_allow_html=True)

        kb_col, _ = load_vector_stores()
        if kb_col:
            try:
                doc_count = kb_col.count()
                st.markdown(f"""
                <div style="background:rgba(16,212,142,0.1); border:1px solid rgba(16,212,142,0.3);
                            border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                    <div style="color:#10d48e; font-size:0.75rem; font-weight:600; letter-spacing:0.08em;">
                        ● VECTOR STORE ONLINE
                    </div>
                    <div style="color:#8892b0; font-size:0.72rem; margin-top:0.3rem;">
                        {doc_count} KB documents indexed
                    </div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                logger.debug(f"Failed to check vector store status: {e}")

        # LLM status
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        has_google = bool(os.getenv("GOOGLE_API_KEY"))
        has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
        llm_active = has_openai or has_google or has_anthropic
        llm_label = "OPENAI" if has_openai else ("GEMINI" if has_google else ("ANTHROPIC" if has_anthropic else "NONE"))

        if llm_active:
            st.markdown(f"""
            <div style="background:rgba(16,212,142,0.1); border:1px solid rgba(16,212,142,0.3);
                        border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                <div style="color:#10d48e; font-size:0.75rem; font-weight:600; letter-spacing:0.08em;">
                    ● LLM ENGINE: {llm_label}
                </div>
                <div style="color:#8892b0; font-size:0.72rem; margin-top:0.3rem;">AI synthesis active</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3);
                        border-radius:8px; padding:0.8rem; margin-bottom:0.6rem;">
                <div style="color:#f59e0b; font-size:0.75rem; font-weight:600;">◌ LLM: TEMPLATE MODE</div>
                <div style="color:#8892b0; font-size:0.72rem; margin-top:0.3rem;">Set API key in .env to enable AI</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Quick code reference
        st.markdown("### ⚡ Error Code Reference")
        codes = {
            "E3": ("High Pressure Trip", "critical"),
            "E5": ("High Discharge Temp", "critical"),
            "U0": ("Refrigerant Loss", "critical"),
            "103": ("Prestart Temp Alert", "medium"),
            "A6": ("Fan Motor Fault", "high"),
        }
        for code, (name, sev) in codes.items():
            color = severity_color(sev)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.6rem; padding:0.4rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);">
                <span style="background:{color}22; color:{color}; border:1px solid {color}44;
                             border-radius:4px; padding:1px 8px; font-family:'JetBrains Mono',monospace;
                             font-size:0.75rem; font-weight:600; min-width:2.5rem; text-align:center;">
                    {code}
                </span>
                <span style="color:#8892b0; font-size:0.75rem;">{name}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <p style="color:#546478; font-size:0.68rem; text-align:center; line-height:1.6;">
            Fault-Graph AI v1.0<br>
            Graph-RAG Industrial Diagnostic<br>
            © 2024 Fault-Graph Systems
        </p>
        """, unsafe_allow_html=True)


# ─── Tab 1: Diagnostic Hub ────────────────────────────────────────────────────
def render_diagnostic_tab():
    # Hero header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #141d35 0%, #1a2540 100%);
                border: 1px solid rgba(0,212,255,0.2); border-radius:16px;
                padding:2rem 2.5rem; margin-bottom:1.5rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
        <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.8rem;">
            <span style="font-size:2rem;">🔍</span>
            <div>
                <h1 style="color:#00d4ff; font-size:1.8rem; font-weight:800;
                           margin:0; letter-spacing:-0.02em;">
                    Diagnostic Hub
                </h1>
                <p style="color:#8892b0; margin:0.2rem 0 0; font-size:0.9rem;">
                    Upload a panel photo or enter error details for AI-powered root cause analysis
                </p>
            </div>
        </div>
        <div style="display:flex; gap:1.5rem; flex-wrap:wrap; margin-top:1rem;">
            <div style="background:rgba(0,212,255,0.08); border:1px solid rgba(0,212,255,0.2);
                        border-radius:8px; padding:0.5rem 1rem; font-size:0.8rem; color:#00d4ff;">
                📸 OCR Panel Analysis
            </div>
            <div style="background:rgba(79,142,255,0.08); border:1px solid rgba(79,142,255,0.2);
                        border-radius:8px; padding:0.5rem 1rem; font-size:0.8rem; color:#4f8eff;">
                🕸 Knowledge Graph Lookup
            </div>
            <div style="background:rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.2);
                        border-radius:8px; padding:0.5rem 1rem; font-size:0.8rem; color:#8b5cf6;">
                🤖 AI Synthesis
            </div>
            <div style="background:rgba(16,212,142,0.08); border:1px solid rgba(16,212,142,0.2);
                        border-radius:8px; padding:0.5rem 1rem; font-size:0.8rem; color:#10d48e;">
                📋 Safety SOP Lookup
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    col_input, col_manual = st.columns([1.2, 1], gap="large")

    with col_input:
        st.markdown("""
        <h3 style="color:#f0f4ff; font-size:1.05rem; font-weight:600; margin-bottom:0.8rem;">
            📸 Image Input — Control Panel Photo
        </h3>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Upload control panel photo",
            type=["jpg", "jpeg", "png", "bmp", "tiff", "webp"],
            help="Upload a photo of the chiller control panel showing the error code",
            label_visibility="collapsed",
        )

        if uploaded_file:
            from PIL import Image
            img = Image.open(uploaded_file)
            st.image(img, caption=f"📷 {uploaded_file.name}", use_container_width=True)
            st.session_state["uploaded_image"] = uploaded_file.read()
            uploaded_file.seek(0)
            st.session_state["uploaded_image"] = uploaded_file.read()
            st.markdown("""
            <div style="background:rgba(16,212,142,0.08); border:1px solid rgba(16,212,142,0.25);
                        border-radius:8px; padding:0.6rem 1rem; font-size:0.8rem; color:#10d48e;
                        margin-top:0.5rem;">
                ✓ Image loaded — click "Run Diagnosis" to extract error code via OCR
            </div>
            """, unsafe_allow_html=True)

    with col_manual:
        st.markdown("""
        <h3 style="color:#f0f4ff; font-size:1.05rem; font-weight:600; margin-bottom:0.8rem;">
            ⌨️ Manual Input — Enter Error Details
        </h3>
        """, unsafe_allow_html=True)

        error_code_input = st.selectbox(
            "Error Code",
            options=["", "E3", "E5", "U0", "103", "A6"],
            format_func=lambda x: x if x else "— Select error code —",
            key="error_code_select",
        )

        model_input = st.selectbox(
            "Asset Model",
            options=["", "Carrier 30RAP", "York YVAA", "Carrier 30XA", "Trane RTAF", "Other"],
            format_func=lambda x: x if x else "— Select model (optional) —",
            key="model_select",
        )

        panel_text = st.text_area(
            "Panel Text / Notes (optional)",
            placeholder="Paste any text visible on the panel, or add technician notes...\n\nExample:\nALARM: E3\nHIGH PRESSURE TRIP\nDISCHARGE: 668 PSIG",
            height=140,
            key="panel_text_input",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        run_btn = st.button(
            "⚡ RUN DIAGNOSIS",
            type="primary",
            use_container_width=True,
            key="run_diagnosis_btn",
        )

    # OCR Result Preview (if image uploaded and text extracted)
    if "ocr_preview" in st.session_state and st.session_state["ocr_preview"]:
        ocr = st.session_state["ocr_preview"]
        conf_color = {"high": "#10d48e", "medium": "#f59e0b", "low": "#ef4444"}.get(
            ocr.get("confidence", "low"), "#8892b0"
        )
        st.markdown(f"""
        <div style="background:#141d35; border:1px solid rgba(0,212,255,0.2);
                    border-radius:12px; padding:1.2rem 1.5rem; margin:1rem 0;">
            <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                <span style="font-size:1.1rem;">🤖</span>
                <h4 style="color:#00d4ff; margin:0; font-size:0.95rem; font-weight:600;">
                    OCR Extraction Result
                </h4>
                <span style="background:{conf_color}22; color:{conf_color}; border:1px solid {conf_color}44;
                             border-radius:4px; padding:1px 8px; font-size:0.7rem; font-weight:700;
                             letter-spacing:0.08em; margin-left:auto;">
                    {ocr.get('confidence', 'unknown').upper()} CONFIDENCE
                </span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                <div>
                    <div style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; margin-bottom:0.2rem;">
                        DETECTED ERROR CODE
                    </div>
                    <div style="color:#ef4444; font-family:'JetBrains Mono',monospace; font-size:1.5rem; font-weight:700;">
                        {ocr.get('error_code') or '—'}
                    </div>
                </div>
                <div>
                    <div style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; margin-bottom:0.2rem;">
                        DETECTED MODEL
                    </div>
                    <div style="color:#f0f4ff; font-size:1rem; font-weight:600;">
                        {ocr.get('model') or '—'}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Run Diagnosis ──────────────────────────────────────────────────────────
    if run_btn:
        with st.spinner("⚡ Initializing diagnostic pipeline..."):
            # Ensure vector stores are ready
            load_vector_stores()

        # Determine input mode
        img_bytes = st.session_state.get("uploaded_image")
        manual_ec = error_code_input if error_code_input else None
        manual_model_val = model_input if (model_input and model_input != "Other") else None
        panel_text_val = panel_text if panel_text.strip() else None

        if not img_bytes and not manual_ec and not panel_text_val:
            st.warning("⚠️ Please upload an image or select an error code to run diagnosis.")
            return

        with st.spinner("🕸 Running knowledge graph lookup..."):
            time.sleep(0.3)

        with st.spinner("📚 Retrieving relevant knowledge base documents..."):
            time.sleep(0.2)

        with st.spinner("🤖 Synthesizing diagnostic report..."):
            try:
                from src.pipeline import run_diagnostic_pipeline
                report = run_diagnostic_pipeline(
                    image_source=img_bytes,
                    manual_text=panel_text_val,
                    manual_error_code=manual_ec,
                    manual_model=manual_model_val,
                )
                st.session_state["last_report"] = report
                st.session_state["feedback_submitted"] = False
            except Exception as e:
                st.error(f"Pipeline error: {e}")
                logger.exception("Pipeline error")
                return

    # ── Display Diagnostic Report ──────────────────────────────────────────────
    report = st.session_state.get("last_report")
    if report:
        render_diagnostic_report(report)


def render_diagnostic_report(report):
    """Render the full diagnostic result card."""
    sev_color = severity_color(report.severity)
    sev_emoji = severity_emoji(report.severity)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #141d35, #1a2540);
                border: 1px solid {sev_color}44; border-top: 3px solid {sev_color};
                border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.4);">
        <div style="display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
            <div>
                <div style="color:#546478; font-size:0.72rem; letter-spacing:0.1em; margin-bottom:0.3rem;">
                    DIAGNOSTIC REPORT
                </div>
                <h2 style="color:#f0f4ff; font-size:1.6rem; font-weight:800; margin:0; letter-spacing:-0.02em;">
                    {report.failure_name}
                </h2>
            </div>
            <div style="margin-left:auto; text-align:right;">
                <span style="background:{sev_color}22; color:{sev_color};
                             border:1.5px solid {sev_color}55; border-radius:8px;
                             padding:6px 18px; font-size:0.8rem; font-weight:700;
                             letter-spacing:0.1em;">
                    {sev_emoji} {report.severity.upper()}
                </span>
                <div style="margin-top:0.5rem; display:flex; gap:0.6rem; flex-wrap:wrap; justify-content:flex-end;">
                    {"<span style='background:rgba(0,212,255,0.1); color:#00d4ff; border:1px solid rgba(0,212,255,0.3); border-radius:4px; padding:2px 8px; font-size:0.72rem; font-family:JetBrains Mono,monospace;'>" + report.error_code + "</span>" if report.error_code else ""}
                    {"<span style='background:rgba(139,92,246,0.1); color:#8b5cf6; border:1px solid rgba(139,92,246,0.3); border-radius:4px; padding:2px 8px; font-size:0.72rem;'>" + (report.model or "") + "</span>" if report.model else ""}
                    {"<span style='background:rgba(16,212,142,0.1); color:#10d48e; border:1px solid rgba(16,212,142,0.3); border-radius:4px; padding:2px 8px; font-size:0.72rem;'>🤖 AI Synthesis</span>" if report.llm_used else "<span style='background:rgba(245,158,11,0.1); color:#f59e0b; border:1px solid rgba(245,158,11,0.3); border-radius:4px; padding:2px 8px; font-size:0.72rem;'>📋 Template Mode</span>"}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Safety Warnings (always shown first) ──────────────────────────────────
    if report.safety_warnings:
        st.markdown("""
        <div style="background:rgba(239,68,68,0.08); border:1.5px solid rgba(239,68,68,0.4);
                    border-radius:12px; padding:1.2rem 1.5rem; margin-bottom:1.2rem;">
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.8rem;">
                <span style="font-size:1.2rem;">🚨</span>
                <h3 style="color:#ef4444; margin:0; font-size:1rem; font-weight:700; letter-spacing:0.05em;">
                    SAFETY ALERTS — READ BEFORE PROCEEDING
                </h3>
            </div>
        """, unsafe_allow_html=True)
        for warning in report.safety_warnings:
            st.markdown(f"""
            <div style="color:#fca5a5; font-size:0.9rem; padding:0.4rem 0 0.4rem 1rem;
                        border-left:3px solid rgba(239,68,68,0.5); margin-bottom:0.4rem;">
                {warning}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Required SOPs ──────────────────────────────────────────────────────────
    if report.required_sops:
        sop_html = " ".join([
            f"<span style='background:rgba(239,68,68,0.1); color:#ef4444; "
            f"border:1px solid rgba(239,68,68,0.35); border-radius:6px; "
            f"padding:4px 12px; font-size:0.8rem; font-weight:600; display:inline-block; margin:3px;'>"
            f"📋 {s['name']}</span>"
            for s in report.required_sops
        ])
        st.markdown(f"""
        <div style="background:#141d35; border:1px solid rgba(239,68,68,0.2);
                    border-radius:10px; padding:0.9rem 1.2rem; margin-bottom:1rem;">
            <div style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; margin-bottom:0.5rem;">
                MANDATORY SAFETY PROCEDURES
            </div>
            {sop_html}
        </div>
        """, unsafe_allow_html=True)

    # ── Main content columns ───────────────────────────────────────────────────
    col_left, col_right = st.columns([1.1, 1], gap="large")

    with col_left:
        # Root Cause Analysis
        if report.root_cause_summary:
            st.markdown("""
            <h3 style="color:#4f8eff; font-size:1rem; font-weight:700;
                       letter-spacing:0.05em; margin-bottom:0.6rem;">
                🔍 ROOT CAUSE ANALYSIS
            </h3>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#141d35; border:1px solid rgba(79,142,255,0.2);
                        border-radius:10px; padding:1rem 1.2rem; margin-bottom:1rem;
                        color:#c5d0e8; font-size:0.88rem; line-height:1.65;">
                {report.root_cause_summary}
            </div>
            """, unsafe_allow_html=True)

        # Probable Root Causes
        if report.probable_root_causes:
            st.markdown("""
            <h4 style="color:#f0f4ff; font-size:0.9rem; font-weight:600; margin-bottom:0.6rem;">
                📊 Probable Root Causes (Priority Order)
            </h4>
            """, unsafe_allow_html=True)
            colors = ["#ef4444", "#f59e0b", "#3b82f6"]
            for i, cause in enumerate(report.probable_root_causes):
                color = colors[min(i, 2)]
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start; gap:0.8rem;
                            padding:0.7rem 1rem; background:#141d35;
                            border:1px solid {color}22; border-radius:8px; margin-bottom:0.4rem;">
                    <span style="background:{color}22; color:{color}; border:1px solid {color}44;
                                 border-radius:50%; width:22px; height:22px; min-width:22px;
                                 display:flex; align-items:center; justify-content:center;
                                 font-size:0.7rem; font-weight:700; margin-top:1px;">
                        {i+1}
                    </span>
                    <span style="color:#c5d0e8; font-size:0.87rem; line-height:1.5;">{cause}</span>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        # Key metrics
        st.markdown("""
        <h3 style="color:#4f8eff; font-size:1rem; font-weight:700;
                   letter-spacing:0.05em; margin-bottom:0.6rem;">
            📊 DIAGNOSTICS SUMMARY
        </h3>
        """, unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        with m1:
            st.metric(
                "⏱ Est. Repair Time",
                f"{report.estimated_repair_time_hours or '?'}h"
                if report.estimated_repair_time_hours else "N/A"
            )
        with m2:
            st.metric("📚 Sources Found", len(report.knowledge_sources))

        # Affected systems
        if report.affected_subsystems:
            sub_html = " ".join([
                f"<span style='background:rgba(79,142,255,0.1); color:#4f8eff; "
                f"border:1px solid rgba(79,142,255,0.25); border-radius:5px; "
                f"padding:3px 10px; font-size:0.78rem; display:inline-block; margin:2px;'>"
                f"⚙️ {s}</span>"
                for s in report.affected_subsystems
            ])
            st.markdown(f"""
            <div style="background:#141d35; border:1px solid rgba(79,142,255,0.15);
                        border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.8rem;">
                <div style="color:#546478; font-size:0.7rem; letter-spacing:0.08em; margin-bottom:0.5rem;">
                    AFFECTED SUBSYSTEMS
                </div>
                {sub_html}
            </div>
            """, unsafe_allow_html=True)

        # Required PPE
        if report.required_ppe:
            ppe_html = "".join([
                f"<div style='color:#fbbf24; font-size:0.82rem; padding:0.25rem 0;'>🧤 {p}</div>"
                for p in report.required_ppe
            ])
            st.markdown(f"""
            <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.2);
                        border-radius:10px; padding:0.8rem 1rem; margin-bottom:0.8rem;">
                <div style="color:#546478; font-size:0.7rem; letter-spacing:0.08em; margin-bottom:0.4rem;">
                    REQUIRED PPE
                </div>
                {ppe_html}
            </div>
            """, unsafe_allow_html=True)

        # Tools Required
        if report.tools_required:
            tools_html = "".join([
                f"<div style='color:#c5d0e8; font-size:0.82rem; padding:0.2rem 0;'>🔧 {t}</div>"
                for t in report.tools_required
            ])
            st.markdown(f"""
            <div style="background:#141d35; border:1px solid rgba(79,142,255,0.15);
                        border-radius:10px; padding:0.8rem 1rem;">
                <div style="color:#546478; font-size:0.7rem; letter-spacing:0.08em; margin-bottom:0.4rem;">
                    TOOLS REQUIRED
                </div>
                {tools_html}
            </div>
            """, unsafe_allow_html=True)

    # ── Step-by-Step Repair Guide ──────────────────────────────────────────────
    if report.repair_steps:
        st.markdown("""
        <h3 style="color:#10d48e; font-size:1rem; font-weight:700;
                   letter-spacing:0.05em; margin:1.5rem 0 0.8rem;">
            🔧 STEP-BY-STEP REPAIR GUIDE
        </h3>
        """, unsafe_allow_html=True)

        for i, step in enumerate(report.repair_steps):
            # Check for safety-critical steps
            is_safety = any(kw in step.lower() for kw in ["danger", "safety", "lockout", "loto", "sop"])
            step_color = "#ef4444" if is_safety else "#10d48e"
            step_bg = "rgba(239,68,68,0.05)" if is_safety else "rgba(16,212,142,0.05)"
            step_border = "rgba(239,68,68,0.25)" if is_safety else "rgba(16,212,142,0.15)"

            st.markdown(f"""
            <div style="display:flex; gap:1rem; padding:0.8rem 1.2rem;
                        background:{step_bg}; border:1px solid {step_border};
                        border-radius:10px; margin-bottom:0.5rem; align-items:flex-start;">
                <div style="background:{step_color}22; color:{step_color};
                             border:1px solid {step_color}44; border-radius:6px;
                             padding:2px 10px; font-family:'JetBrains Mono',monospace;
                             font-size:0.78rem; font-weight:700; min-width:2.5rem;
                             text-align:center; margin-top:1px;">
                    {i+1:02d}
                </div>
                <div style="color:#c5d0e8; font-size:0.88rem; line-height:1.6; flex:1;">
                    {step}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Similar Historical Cases ───────────────────────────────────────────────
    if report.similar_cases:
        st.markdown("""
        <h3 style="color:#8b5cf6; font-size:1rem; font-weight:700;
                   letter-spacing:0.05em; margin:1.5rem 0 0.8rem;">
            📂 SIMILAR HISTORICAL CASES
        </h3>
        """, unsafe_allow_html=True)

        cols = st.columns(min(len(report.similar_cases), 3))
        for i, case in enumerate(report.similar_cases[:3]):
            outcome = case.get("outcome", "")
            outcome_color = "#10d48e" if "RESOLVED" in outcome else "#f59e0b" if "PARTIAL" in outcome else "#ef4444"
            with cols[i]:
                st.markdown(f"""
                <div style="background:#141d35; border:1px solid rgba(139,92,246,0.2);
                            border-radius:12px; padding:1rem; height:100%;">
                    <div style="color:#546478; font-size:0.7rem; letter-spacing:0.08em;">
                        {case.get('log_id', '?')} · {case.get('model', '')}
                    </div>
                    <div style="background:{outcome_color}22; color:{outcome_color};
                                border-radius:4px; padding:2px 8px; font-size:0.72rem;
                                font-weight:600; display:inline-block; margin:0.4rem 0;">
                        {outcome[:30]}
                    </div>
                    <div style="color:#8892b0; font-size:0.8rem; line-height:1.5; margin-top:0.4rem;">
                        {case.get('snippet', '')[:150]}...
                    </div>
                    <div style="color:#8b5cf6; font-size:0.72rem; margin-top:0.6rem;">
                        Relevance: {case.get('relevance', 0):.0%}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Diagnosis Notes ────────────────────────────────────────────────────────
    if report.diagnosis_notes:
        st.markdown(f"""
        <div style="background:rgba(245,158,11,0.06); border:1px solid rgba(245,158,11,0.2);
                    border-radius:10px; padding:0.9rem 1.2rem; margin:1.2rem 0;">
            <div style="color:#f59e0b; font-size:0.85rem; line-height:1.5;">
                ℹ️ {report.diagnosis_notes}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Feedback Buttons ───────────────────────────────────────────────────────
    if not st.session_state.get("feedback_submitted"):
        st.markdown("""
        <h3 style="color:#f0f4ff; font-size:0.95rem; font-weight:600; margin:1.5rem 0 0.6rem;">
            📣 Was this diagnosis helpful?
        </h3>
        """, unsafe_allow_html=True)

        fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 3])
        with fb_col1:
            if st.button("✅ Resolved — Fixed it!", key="fb_resolved", use_container_width=True):
                st.session_state["feedback_submitted"] = True
                st.session_state["feedback_type"] = "resolved"
                st.success("🎉 Great! Outcome recorded as RESOLVED.")
                st.rerun()
        with fb_col2:
            if st.button("❌ Not Resolved — Still failing", key="fb_not_resolved", use_container_width=True):
                st.session_state["feedback_submitted"] = True
                st.session_state["feedback_type"] = "not_resolved"
                st.warning("⚠️ Feedback recorded. Please escalate to Level 2 support.")
                st.rerun()
    else:
        fb_type = st.session_state.get("feedback_type", "")
        if fb_type == "resolved":
            st.markdown("""
            <div style="background:rgba(16,212,142,0.1); border:1px solid rgba(16,212,142,0.3);
                        border-radius:10px; padding:1rem 1.5rem; text-align:center;">
                <div style="color:#10d48e; font-size:1rem; font-weight:600;">
                    ✅ Outcome: RESOLVED — Feedback logged to maintenance system
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3);
                        border-radius:10px; padding:1rem 1.5rem; text-align:center;">
                <div style="color:#ef4444; font-size:1rem; font-weight:600;">
                    ❌ Outcome: NOT RESOLVED — Escalate to Level 2 Engineering Support
                </div>
            </div>
            """, unsafe_allow_html=True)


# ─── Tab 2: Knowledge Graph Explorer ─────────────────────────────────────────
def render_graph_tab():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#141d35,#1a2540);
                border:1px solid rgba(139,92,246,0.2); border-radius:16px;
                padding:1.5rem 2rem; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:1rem;">
            <span style="font-size:2rem;">🕸</span>
            <div>
                <h1 style="color:#8b5cf6; font-size:1.6rem; font-weight:800; margin:0;">
                    Knowledge Graph Explorer
                </h1>
                <p style="color:#8892b0; margin:0.2rem 0 0; font-size:0.9rem;">
                    Interactive OKF knowledge graph — explore asset relationships, failure modes, and SOPs
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    G = load_graph()
    if not G:
        st.error("Knowledge graph not available. Check that OKF files are present in data/knowledge_base/")
        return

    # Graph controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
    with ctrl_col1:
        filter_type = st.multiselect(
            "Filter by Node Type",
            options=["asset", "subsystem", "component", "failure", "sop"],
            default=["asset", "subsystem", "failure", "sop"],
            key="graph_filter_type",
        )
    with ctrl_col2:
        highlight_code = st.selectbox(
            "Highlight Error Code",
            options=["None", "E3", "E5", "U0", "103", "A6"],
            key="graph_highlight_code",
        )
    with ctrl_col3:
        physics_enabled = st.toggle("Enable Physics", value=True, key="graph_physics")

    # Build agraph nodes and edges
    node_colors = {
        "asset": "#00d4ff",
        "subsystem": "#4f8eff",
        "component": "#8b5cf6",
        "failure": "#ef4444",
        "sop": "#f59e0b",
        "reference": "#546478",
        "unknown": "#546478",
    }
    node_symbols = {
        "asset": "🏭",
        "subsystem": "⚙️",
        "component": "🔩",
        "failure": "⚡",
        "sop": "📋",
    }

    nodes = []
    edges = []
    seen_nodes = set()

    # Determine highlighted nodes
    highlighted_nodes = set()
    if highlight_code and highlight_code != "None":
        from src.graph_builder import get_connected_nodes, find_failure_node
        fn = find_failure_node(highlight_code, G)
        if fn:
            highlighted_nodes.add(fn)
            for n in get_connected_nodes(fn, G, depth=2):
                highlighted_nodes.add(n["id"])

    for node_id, attrs in G.nodes(data=True):
        ntype = attrs.get("node_type", "unknown")
        if filter_type and ntype not in filter_type:
            continue

        color = node_colors.get(ntype, "#546478")
        is_highlighted = node_id in highlighted_nodes if highlighted_nodes else False
        size = 30 if ntype == "asset" else 22 if ntype in ("subsystem", "failure") else 18

        if is_highlighted:
            size += 8
            color = "#ffffff"

        label = attrs.get("name", node_id)
        # Truncate label for display
        if len(label) > 28:
            label = label[:25] + "..."

        nodes.append(Node(
            id=node_id,
            label=label,
            size=size,
            color=color,
            title=f"[{ntype.upper()}]\n{attrs.get('name', node_id)}\nSeverity: {attrs.get('severity','?')}\nCode: {attrs.get('error_code','N/A')}",
            shape="dot" if ntype not in ("asset",) else "diamond",
        ))
        seen_nodes.add(node_id)

    for src, tgt, edata in G.edges(data=True):
        if src in seen_nodes and tgt in seen_nodes:
            is_highlighted_edge = (src in highlighted_nodes and tgt in highlighted_nodes)
            edges.append(Edge(
                source=src,
                target=tgt,
                color="#00d4ff66" if is_highlighted_edge else "#4f8eff33",
                width=2 if is_highlighted_edge else 1,
            ))

    # Legend
    legend_html = "".join([
        f"<span style='background:{c}22; color:{c}; border:1px solid {c}44; "
        f"border-radius:4px; padding:2px 10px; font-size:0.72rem; margin:2px; display:inline-block;'>"
        f"{node_symbols.get(t,'●')} {t.title()}</span>"
        for t, c in node_colors.items() if t not in ("reference", "unknown")
    ])
    st.markdown(f"""
    <div style="background:#141d35; border:1px solid rgba(79,142,255,0.15);
                border-radius:10px; padding:0.7rem 1rem; margin-bottom:1rem;
                display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
        <span style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; white-space:nowrap;">
            NODE TYPES:
        </span>
        {legend_html}
        <span style="margin-left:auto; color:#8892b0; font-size:0.78rem;">
            {len(nodes)} nodes · {len(edges)} edges
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Agraph config
    config = Config(
        width="100%",
        height=550,
        directed=True,
        physics=physics_enabled,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#00d4ff",
        collapsible=False,
        node={"color": "#4f8eff"},
        link={"color": "#4f8eff33", "renderLabel": False},
    )

    if nodes:
        try:
            clicked = agraph(nodes=nodes, edges=edges, config=config)

            # Node detail panel on click
            if clicked and clicked in G.nodes:
                attrs = G.nodes[clicked]
                ntype = attrs.get("node_type", "unknown")
                color = node_colors.get(ntype, "#546478")

                st.markdown(f"""
                <div style="background:{color}11; border:1px solid {color}44;
                            border-radius:12px; padding:1.2rem 1.5rem; margin-top:1rem;">
                    <div style="display:flex; align-items:center; gap:0.8rem; margin-bottom:0.8rem;">
                        <span style="background:{color}22; color:{color}; border:1px solid {color}44;
                                     border-radius:6px; padding:3px 10px; font-size:0.75rem; font-weight:600;">
                            {ntype.upper()}
                        </span>
                        <h4 style="color:{color}; margin:0; font-size:1rem; font-weight:700;">
                            {attrs.get('name', clicked)}
                        </h4>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem;">
                        <div><span style="color:#546478; font-size:0.72rem;">Node ID:</span>
                             <span style="color:#c5d0e8; font-size:0.82rem; font-family:monospace;"> {clicked}</span>
                        </div>
                        <div><span style="color:#546478; font-size:0.72rem;">Severity:</span>
                             <span style="color:{severity_color(attrs.get('severity','unknown'))}; font-size:0.82rem;">
                                 {attrs.get('severity','?').upper()}
                             </span>
                        </div>
                        {"<div><span style='color:#546478; font-size:0.72rem;'>Error Code:</span> <span style='color:#ef4444; font-family:monospace; font-size:0.9rem; font-weight:700;'> " + str(attrs.get('error_code','')) + "</span></div>" if attrs.get('error_code') else ""}
                    </div>
                    <div style="color:#8892b0; font-size:0.82rem; margin-top:0.8rem; line-height:1.5;">
                        {attrs.get('content', '')[:300]}{"..." if len(attrs.get('content','')) > 300 else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Graph visualization error: {e}")
            st.info("Try installing streamlit-agraph: pip install streamlit-agraph")
    else:
        st.info("No nodes match the current filter. Try adjusting the filter options.")

    # Graph statistics
    st.markdown("---")
    col_stats = st.columns(4)
    with col_stats[0]:
        assets = [n for n, a in G.nodes(data=True) if a.get("node_type") == "asset"]
        st.metric("🏭 Assets", len(assets))
    with col_stats[1]:
        failures = [n for n, a in G.nodes(data=True) if a.get("node_type") == "failure"]
        st.metric("⚡ Failure Modes", len(failures))
    with col_stats[2]:
        sops = [n for n, a in G.nodes(data=True) if a.get("node_type") == "sop"]
        st.metric("📋 Safety SOPs", len(sops))
    with col_stats[3]:
        st.metric("🔗 Relationships", G.number_of_edges())


# ─── Tab 3: System Logs & Inspector ──────────────────────────────────────────
def render_logs_tab():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#141d35,#1a2540);
                border:1px solid rgba(16,212,142,0.2); border-radius:16px;
                padding:1.5rem 2rem; margin-bottom:1.5rem;">
        <div style="display:flex; align-items:center; gap:1rem;">
            <span style="font-size:2rem;">📊</span>
            <div>
                <h1 style="color:#10d48e; font-size:1.6rem; font-weight:800; margin:0;">
                    System Logs &amp; Inspector
                </h1>
                <p style="color:#8892b0; margin:0.2rem 0 0; font-size:0.9rem;">
                    View maintenance logs, knowledge base files, and vector store index status
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    log_tab, kb_tab, store_tab = st.tabs(
        ["📋 Maintenance Logs", "📚 Knowledge Base Files", "🗄 Vector Store Status"]
    )

    with log_tab:
        logs_data = load_maintenance_logs()
        logs = logs_data.get("logs", [])

        # Summary row
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Logs", len(logs))
        with col_s2:
            stories = len(set(log_item.get("story", 0) for log_item in logs))
            st.metric("Failure Stories", stories)
        with col_s3:
            resolved = len([log_item for log_item in logs if "RESOLVED" in log_item.get("outcome", "")])
            st.metric("✅ Resolved", resolved)
        with col_s4:
            critical = len([log_item for log_item in logs if log_item.get("event_type") in ("alarm", "emergency_service")])
            st.metric("🚨 Alarm Events", critical)

        # Filters
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            story_filter = st.selectbox(
                "Filter by Story",
                ["All Stories"] + [f"Story {i}" for i in range(1, stories + 1)],
                key="log_story_filter",
            )
        with fc2:
            code_filter = st.selectbox(
                "Filter by Error Code",
                ["All Codes"] + sorted(set(log_item.get("error_code", "N/A") for log_item in logs if log_item.get("error_code"))),
                key="log_code_filter",
            )
        with fc3:
            type_filter = st.selectbox(
                "Filter by Event Type",
                ["All Types"] + sorted(set(log_item.get("event_type", "") for log_item in logs)),
                key="log_type_filter",
            )

        # Filter logs
        filtered_logs = logs
        if story_filter != "All Stories":
            story_num = int(story_filter.split()[-1])
            filtered_logs = [log_item for log_item in filtered_logs if log_item.get("story") == story_num]
        if code_filter != "All Codes":
            filtered_logs = [log_item for log_item in filtered_logs if log_item.get("error_code") == code_filter]
        if type_filter != "All Types":
            filtered_logs = [log_item for log_item in filtered_logs if log_item.get("event_type") == type_filter]

        st.markdown(f"<p style='color:#8892b0; font-size:0.8rem;'>Showing {len(filtered_logs)} of {len(logs)} logs</p>",
                    unsafe_allow_html=True)

        for log in filtered_logs:
            ec = log.get("error_code")
            outcome = log.get("outcome", "")
            story = log.get("story", "?")

            outcome_color = "#10d48e" if "RESOLVED" in outcome else "#f59e0b" if "PARTIAL" in outcome or "PROGRESS" in outcome else "#ef4444"
            ec_color = severity_color("critical") if ec in ("E3", "E5", "U0") else severity_color("high") if ec == "A6" else "#3b82f6"

            with st.expander(
                f"📋 {log.get('id', '?')} | Story {story} | "
                f"{log.get('model', 'Unknown')} | {log.get('title', 'Log Entry')}"
            ):
                dc1, dc2, dc3, dc4 = st.columns(4)
                with dc1:
                    st.markdown(f"**Timestamp:** `{log.get('timestamp', 'N/A')}`")
                with dc2:
                    st.markdown(f"**Asset:** `{log.get('asset_id', 'N/A')}`")
                with dc3:
                    if ec:
                        st.markdown(f"**Error Code:** "
                                    f"<span style='color:{ec_color}; font-family:monospace; font-weight:700;'>{ec}</span>",
                                    unsafe_allow_html=True)
                    else:
                        st.markdown("**Error Code:** N/A")
                with dc4:
                    st.markdown(
                        f"**Outcome:** <span style='color:{outcome_color}; font-size:0.82rem;'>{outcome[:30]}</span>",
                        unsafe_allow_html=True
                    )

                st.markdown(f"**Site:** {log.get('site', 'N/A')}  "
                            f"**Technician:** {log.get('technician', 'N/A')}")
                st.markdown(f"**Description:** {log.get('description', '')}")
                st.markdown(f"**Resolution:** {log.get('resolution', '')}")

                # Show numeric data if present
                numeric_fields = {k: v for k, v in log.items()
                                  if isinstance(v, (int, float)) and k not in ("story", "sequence")}
                if numeric_fields:
                    with st.expander("📊 Measurement Data"):
                        st.json(numeric_fields)

    with kb_tab:
        kb_dir = ROOT_DIR / "data" / "knowledge_base"
        st.markdown(f"""
        <p style="color:#8892b0; font-size:0.85rem;">
            Knowledge base root: <code>{kb_dir}</code>
        </p>
        """, unsafe_allow_html=True)

        categories = [d for d in kb_dir.iterdir() if d.is_dir()]

        cat_tabs = st.tabs([f"📁 {c.name.title()}" for c in sorted(categories)])
        for i, cat in enumerate(sorted(categories)):
            with cat_tabs[i]:
                md_files = list(cat.glob("*.md"))
                st.markdown(f"**{len(md_files)} files** in `{cat.name}/`")

                for md_file in sorted(md_files):
                    with st.expander(f"📄 {md_file.stem}"):
                        content = md_file.read_text(encoding="utf-8")

                        # Show frontmatter metadata
                        import re
                        import yaml
                        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
                        if fm_match:
                            fm = yaml.safe_load(fm_match.group(1)) or {}
                            meta_cols = st.columns(3)
                            with meta_cols[0]:
                                st.markdown(f"**ID:** `{fm.get('id', '?')}`")
                            with meta_cols[1]:
                                st.markdown(f"**Type:** `{fm.get('type', '?')}`")
                            with meta_cols[2]:
                                sev = fm.get('severity', '?')
                                sev_c = severity_color(sev)
                                st.markdown(
                                    f"**Severity:** <span style='color:{sev_c};'>{sev.upper()}</span>",
                                    unsafe_allow_html=True
                                )

                            if fm.get("error_code"):
                                st.markdown(f"**Error Code:** `{fm['error_code']}`")

                        # Show raw markdown
                        with st.expander("View Raw Markdown"):
                            st.code(content, language="markdown")

    with store_tab:
        st.markdown("### 🗄 ChromaDB Vector Store Status")

        kb_col, logs_col = load_vector_stores()

        s1, s2 = st.columns(2)
        with s1:
            st.markdown("""
            <div style="background:#141d35; border:1px solid rgba(0,212,255,0.2);
                        border-radius:12px; padding:1.2rem; text-align:center;">
                <div style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; margin-bottom:0.5rem;">
                    KNOWLEDGE BASE COLLECTION
                </div>
            """, unsafe_allow_html=True)
            if kb_col:
                try:
                    count = kb_col.count()
                    st.metric("Documents", count)
                    st.markdown("Collection: `fault_graph_knowledge_base`")
                except Exception:
                    st.error("Collection unavailable")
            else:
                st.error("Not initialized")
            st.markdown("</div>", unsafe_allow_html=True)

        with s2:
            st.markdown("""
            <div style="background:#141d35; border:1px solid rgba(139,92,246,0.2);
                        border-radius:12px; padding:1.2rem; text-align:center;">
                <div style="color:#546478; font-size:0.72rem; letter-spacing:0.08em; margin-bottom:0.5rem;">
                    MAINTENANCE LOGS COLLECTION
                </div>
            """, unsafe_allow_html=True)
            if logs_col:
                try:
                    count = logs_col.count()
                    st.metric("Documents", count)
                    st.markdown("Collection: `fault_graph_maintenance_logs`")
                except Exception:
                    st.error("Collection unavailable")
            else:
                st.error("Not initialized")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🔄 Re-index All Data", key="reindex_btn"):
            with st.spinner("Re-indexing knowledge base and logs..."):
                try:
                    from src.vector_store import initialize_stores
                    # Clear cache and re-initialize
                    load_vector_stores.clear()
                    kb_col, logs_col = initialize_stores()
                    st.success(f"✅ Re-indexed: {kb_col.count()} KB docs + {logs_col.count()} log entries")
                except Exception as e:
                    st.error(f"Re-indexing failed: {e}")


# ─── Main App ─────────────────────────────────────────────────────────────────
def main():
    # Initialize session state
    if "last_report" not in st.session_state:
        st.session_state["last_report"] = None
    if "feedback_submitted" not in st.session_state:
        st.session_state["feedback_submitted"] = False

    # Render sidebar
    render_sidebar()

    # Warm up resources in background
    with st.spinner("Initializing Fault-Graph AI..."):
        _ = load_graph()
        kb_col, logs_col = load_vector_stores()

    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "⚡ Diagnostic Hub",
        "🕸 Knowledge Graph Explorer",
        "📊 System Logs & Inspector",
    ])

    with tab1:
        render_diagnostic_tab()

    with tab2:
        render_graph_tab()

    with tab3:
        render_logs_tab()


if __name__ == "__main__":
    main()
