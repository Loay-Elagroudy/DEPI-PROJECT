"""
Consumer Complaints RAG Chatbot -- Streamlit frontend.

Welcome / landing page. Chat, Evaluation Dashboard, and Model Info live
in `pages/` as separate multipage-app screens.
"""
import streamlit as st

from utils.api_client import get_health

st.set_page_config(
    page_title="Complaints RAG Chatbot",
    page_icon="\U0001F916",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.hero {
    padding: 2.5rem 2rem;
    border-radius: 16px;
    background: linear-gradient(135deg, #1A1D24 0%, #232733 100%);
    border: 1px solid #2E3340;
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 2.2rem; margin-bottom: 0.4rem; }
.hero p { color: #A3A9B7; font-size: 1.05rem; }
.metric-card {
    background: #1A1D24;
    border: 1px solid #2E3340;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.status-dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.status-ok { background-color: #4CAF50; }
.status-bad { background-color: #E5534B; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## \U0001F916 Complaints RAG")
    st.caption("Consumer Financial Complaints Assistant")
    st.markdown("---")
    st.page_link("streamlit_app.py", label="Welcome", icon="\U0001F3E0")
    st.page_link("pages/1_Chat.py", label="Chat", icon="\U0001F4AC")
    st.page_link("pages/2_Evaluation_Dashboard.py", label="Evaluation Dashboard", icon="\U0001F4CA")
    st.page_link("pages/3_Model_Info.py", label="Model Info", icon="\u2139\ufe0f")
    st.markdown("---")
    st.caption("Powered by Chroma + Gemini 2.5 Flash")

st.markdown(
    """
    <div class="hero">
        <h1>\U0001F916 Consumer Complaints RAG Chatbot</h1>
        <p>Ask natural-language questions about consumer financial complaints. Answers are grounded in
        real complaint records retrieved from a vector database, generated with Google Gemini.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
try:
    health = get_health()
    api_ok = True
except Exception:
    health = None
    api_ok = False

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    dot_class = "status-ok" if api_ok else "status-bad"
    st.markdown(f'<span class="status-dot {dot_class}"></span> **API Status**', unsafe_allow_html=True)
    st.write("Online" if api_ok else "Unreachable")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    ready = health.get("vector_store_ready") if health else False
    dot_class = "status-ok" if ready else "status-bad"
    st.markdown(f'<span class="status-dot {dot_class}"></span> **Vector Store**', unsafe_allow_html=True)
    st.write("Ready" if ready else "Not built yet")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("**Generation Model**", unsafe_allow_html=True)
    st.write(health.get("gemini_model") if health else "n/a")
    st.markdown("</div>", unsafe_allow_html=True)

if not api_ok:
    st.error(
        "Could not reach the backend API. Make sure it's running and that `API_BASE_URL` "
        "points to it (see the sidebar / environment variables)."
    )

st.markdown("### Get started")
st.write(
    "Head to **Chat** in the sidebar to ask a question, or check the **Evaluation Dashboard** "
    "for BLEU/ROUGE and Recall@K/MRR scores from the Milestone 2 evaluation pipeline."
)

if st.button("\U0001F4AC Go to Chat", type="primary"):
    st.switch_page("pages/1_Chat.py")
