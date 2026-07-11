"""Evaluation dashboard page -- BLEU/ROUGE + Recall@K/MRR."""
import pandas as pd
import streamlit as st

from utils.api_client import get_generation_metrics, get_retrieval_metrics

st.set_page_config(page_title="Evaluation - Complaints RAG", page_icon="\U0001F4CA", layout="wide")
st.title("\U0001F4CA Evaluation Dashboard")
st.caption("Milestone 2 evaluation results: generation quality (BLEU/ROUGE) and retrieval quality (Recall@K, MRR).")

GENERATION_NOTE = (
    "Note: BLEU and ROUGE measure lexical overlap with reference answers rather than "
    "semantic correctness. Since this chatbot is powered by an LLM, it often generates "
    "correct answers using different wording, resulting in relatively low BLEU/ROUGE "
    "scores. This is expected behavior for generative RAG systems. Overall performance "
    "should be evaluated together with retrieval metrics (Recall@K, MRR) and qualitative "
    "evaluation."
)

# Session-state keys used to cache each evaluation's results across reruns, so the
# Evaluation Summary section and the tabs can share the same data without re-invoking
# the evaluation endpoints (requirement: reuse existing data, no duplicate computation).
_GEN_KEY = "eval_generation_df"
_RET_KEY = "eval_retrieval_df"


def _generation_summary_stats(df: pd.DataFrame) -> dict:
    """Average latency / BLEU / ROUGE-1 / ROUGE-L from a generation-metrics DataFrame.

    Shared by the summary cards and the Generation Quality tab so the averages are
    only ever computed once per DataFrame, in one place.
    """
    return {
        "avg_latency": round(df["Latency(s)"].mean(), 2),
        "avg_bleu": round(df["BLEU"].mean(), 3),
        "avg_rouge1": round(df["ROUGE-1"].mean(), 3),
        "avg_rougeL": round(df["ROUGE-L"].mean(), 3),
    }


def _retrieval_summary_stats(df: pd.DataFrame) -> dict:
    """Recall@5 / MRR from a retrieval-metrics DataFrame (falls back to the largest
    available k if k=5 wasn't included in the run).
    """
    row = df[df["k"] == 5]
    if row.empty:
        row = df.sort_values("k").iloc[[-1]]
    return {
        "recall_at_5": round(float(row["Recall@K"].iloc[0]), 3),
        "mrr": round(float(row["MRR"].iloc[0]), 3),
    }


# ---------------------------------------------------------------------------
# Evaluation Summary -- compact, high-level overview built entirely from
# whatever results are already cached in session state. Nothing here triggers
# a new evaluation run; it only reads and displays data produced by the tabs
# below once their "Run ..." buttons have been used.
# ---------------------------------------------------------------------------
st.subheader("Evaluation Summary")
st.caption("Populated from the results below. Run each evaluation once to fill in its metrics here.")

gen_df = st.session_state.get(_GEN_KEY)
ret_df = st.session_state.get(_RET_KEY)

gen_stats = _generation_summary_stats(gen_df) if gen_df is not None else {}
ret_stats = _retrieval_summary_stats(ret_df) if ret_df is not None else {}

summary_row1 = st.columns(4)
summary_row1[0].metric(
    "Avg Response Latency",
    f"{gen_stats['avg_latency']}s" if gen_stats else "—",
)
summary_row1[1].metric("Avg BLEU", gen_stats.get("avg_bleu", "—"))
summary_row1[2].metric("Avg ROUGE-1", gen_stats.get("avg_rouge1", "—"))
summary_row1[3].metric("Avg ROUGE-L", gen_stats.get("avg_rougeL", "—"))

summary_row2 = st.columns(2)
summary_row2[0].metric("Recall@5", ret_stats.get("recall_at_5", "—"))
summary_row2[1].metric("MRR", ret_stats.get("mrr", "—"))

st.divider()

tab1, tab2 = st.tabs(["Generation Quality", "Retrieval Quality"])

with tab1:
    if st.button("\U0001F504 Run generation evaluation", key="gen_eval"):
        try:
            with st.spinner("Scoring generated answers against ground truth..."):
                rows = get_generation_metrics()
            st.session_state[_GEN_KEY] = pd.DataFrame(rows)
        except Exception as e:
            st.error(f"Evaluation failed: {e}")

    gen_df = st.session_state.get(_GEN_KEY)
    if gen_df is not None:
        st.dataframe(gen_df, use_container_width=True)
        stats = _generation_summary_stats(gen_df)
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg ROUGE-1", stats["avg_rouge1"])
        c2.metric("Avg ROUGE-L", stats["avg_rougeL"])
        c3.metric("Avg BLEU", stats["avg_bleu"])
        st.info(GENERATION_NOTE)

with tab2:
    st.subheader("Recall@K / MRR (k = 1, 3, 5)")
    if st.button("\U0001F504 Run retrieval evaluation", key="ret_eval"):
        try:
            with st.spinner("Scoring retriever against derived ground truth..."):
                rows = get_retrieval_metrics()
            st.session_state[_RET_KEY] = pd.DataFrame(rows)
        except Exception as e:
            st.error(f"Evaluation failed: {e}")

    ret_df = st.session_state.get(_RET_KEY)
    if ret_df is not None:
        st.dataframe(ret_df, use_container_width=True)
        st.bar_chart(ret_df.set_index("k")[["Recall@K", "MRR"]])
