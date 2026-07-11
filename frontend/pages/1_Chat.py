"""Chat interface page."""
import time

import streamlit as st

from utils.api_client import ask_chat

st.set_page_config(page_title="Chat - Complaints RAG", page_icon="\U0001F4AC", layout="wide")

st.markdown(
    """
    <style>
    .source-card {
        background: #1A1D24; border: 1px solid #2E3340; border-radius: 10px;
        padding: 0.8rem 1rem; margin-bottom: 0.6rem;
    }
    .source-title { color: #7EA6E0; font-weight: 600; font-size: 0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("\U0001F4AC Chat with the Complaints Assistant")

with st.sidebar:
    st.markdown("### Settings")
    top_k = st.slider("Retrieved documents (k)", min_value=1, max_value=10, value=3)
    if st.button("\U0001F5D1\ufe0f Reset conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander(f"\U0001F4DA Retrieved context ({len(message['sources'])} sources)"):
                for src in message["sources"]:
                    st.markdown(
                        f"""<div class="source-card">
                        <div class="source-title">{src['company']} &middot; Complaint #{src['complaint_id']}</div>
                        <div>{src['snippet']}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

if user_query := st.chat_input("Ask about a company, product, or complaint..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("\u258B")  # typing indicator
        try:
            with st.spinner("Searching database & generating answer..."):
                result = ask_chat(user_query, k=top_k)
            answer = result["answer"]
            sources = result.get("sources", [])
            placeholder.markdown(answer)
            if sources:
                with st.expander(f"\U0001F4DA Retrieved context ({len(sources)} sources)"):
                    for src in sources:
                        st.markdown(
                            f"""<div class="source-card">
                            <div class="source-title">{src['company']} &middot; Complaint #{src['complaint_id']}</div>
                            <div>{src['snippet']}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )
        except Exception as e:
            answer = f"\u26A0\ufe0f Error generating response: {e}"
            sources = []
            placeholder.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
