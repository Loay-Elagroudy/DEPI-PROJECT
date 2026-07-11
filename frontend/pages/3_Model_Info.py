"""Model / system information page."""
import streamlit as st

from utils.api_client import get_health

st.set_page_config(page_title="Model Info - Complaints RAG", page_icon="\u2139\ufe0f", layout="wide")
st.title("\u2139\ufe0f Model Information")

try:
    health = get_health()
except Exception as e:
    st.error(f"Could not reach the backend API: {e}")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Retrieval")
    st.write(f"**Embedding model:** `{health['embedding_model']}`")
    st.write("**Vector store:** Chroma (persisted, batch-built)")
    store_ready_label = "\u2705 Yes" if health["vector_store_ready"] else "\u274C No"
    st.write(f"**Vector store ready:** {store_ready_label}")

with col2:
    st.markdown("### Generation")
    st.write(f"**Model:** `{health['gemini_model']}`")
    key_configured_label = "\u2705 Yes" if health["google_api_key_configured"] else "\u274C No"
    st.write(f"**API key configured:** {key_configured_label}")
    st.write(f"**API version:** {health['version']}")

st.markdown("---")
st.markdown("### Pipeline Overview")
st.markdown(
    """
1. **Retrieval** -- the question is embedded and matched against complaint documents in Chroma
   (similarity search, top-k configurable).
2. **Context assembly** -- retrieved complaint records are concatenated into a single context block.
3. **Generation** -- Gemini generates a grounded answer from the context + question, instructed to
   say "I don't know" when the context doesn't contain the answer.
4. **Evaluation** -- generation is scored with ROUGE-1/L and smoothed BLEU against curated ground
   truth; retrieval is scored with Recall@K and MRR against programmatically derived relevance labels.
5. **Optimization** -- prompt wording, embedding model, chunk size/overlap, and retrieval strategy
   (similarity vs. MMR) were compared experimentally; results are in `optimization_experiments_report.md`.
    """
)
