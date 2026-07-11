"""
Prompt construction -- preserves notebook cells 37 and 46 exactly.
"""


def format_docs(docs) -> str:
    """Identical to cell 37's `format_docs`."""
    return "\n\n".join(doc.page_content for doc in docs)


def build_default_prompt(context: str, question: str) -> str:
    return (
        f"You are an expert customer support AI assistant specializing in analyzing consumer financial complaints.\n"
        f"Answer the user's question naturally and directly.\n"
        f"Use the retrieved information only as background knowledge.\n"
        f"Do NOT mention the context, retrieved documents, or phrases like "
        f"'Based on the provided context', 'According to the context', or "
        f"'The provided information'.\n"
        f"If the answer is not available, simply say you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )


def get_prompt(context: str, question: str, version: str = "v1") -> str:
    """
    Identical to cell 46's `get_prompt` -- used only by the prompt-engineering
    optimization experiment (v1 = baseline, v2 = role/constraint-based).
    """
    if version == "v1":
        return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    return (
        f"You are a professional Financial Complaint Analyst. "
        f"Use ONLY the provided context below to answer. "
        f"If the answer isn't in the context, say 'I do not have enough information.' "
        f"Do not invent facts.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
