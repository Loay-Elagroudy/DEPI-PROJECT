"""Retrieval service -- exposes the retriever (cell 37 config) directly, for debugging/inspection."""
from app.schemas.retrieval import RetrievalResponse, RetrievedDocument
from app.vector_store.store import get_retriever


def retrieve(query: str, k: int = None, search_type: str = None) -> RetrievalResponse:
    retriever = get_retriever(k=k, search_type=search_type)
    docs = retriever.invoke(query)
    results = [
        RetrievedDocument(
            complaint_id=d.metadata.get("complaint_id", "unknown"),
            company=d.metadata.get("company", "unknown"),
            content=d.page_content,
        )
        for d in docs
    ]
    return RetrievalResponse(query=query, results=results)
