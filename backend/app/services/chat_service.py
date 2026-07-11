"""Chat service -- wraps the RAG chain (cell 37) for the /api/v1/chat endpoint."""
from app.core.logging_config import get_logger
from app.rag.chain import direct_gemini_call
from app.rag.prompts import format_docs
from app.schemas.chat import ChatResponse, SourceDocument
from app.vector_store.store import get_retriever

logger = get_logger(__name__)


def ask_question(question: str, k: int = None) -> ChatResponse:
    """
    Runs the same retrieve -> format -> generate flow as the notebook's
    `rag_chain`, but also surfaces the retrieved sources for the UI's
    "retrieved context viewer".
    """
    retriever = get_retriever(k=k)
    docs = retriever.invoke(question)
    context = format_docs(docs)
    answer = direct_gemini_call({"context": context, "question": question})

    sources = [
        SourceDocument(
            complaint_id=d.metadata.get("complaint_id", "unknown"),
            company=d.metadata.get("company", "unknown"),
            snippet=(d.page_content[:300] + "...") if len(d.page_content) > 300 else d.page_content,
        )
        for d in docs
    ]
    return ChatResponse(answer=answer, question=question, sources=sources)
