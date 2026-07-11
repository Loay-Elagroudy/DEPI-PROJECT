"""
Vector store builder -- preserves notebook cell 35 exactly.

Builds (or rebuilds) the Chroma vector store from the cleaned corpus using
`sentence-transformers/all-MiniLM-L6-v2` embeddings, in memory-safe batches,
freeing memory between batches. Persisted to disk so the API can load it
without rebuilding on every restart.
"""
import gc
from typing import List, Optional

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.config.settings import get_settings
from app.core.logging_config import get_logger
from app.utils.data_loader import load_documents

logger = get_logger(__name__)


def get_embeddings(model_name: Optional[str] = None) -> HuggingFaceEmbeddings:
    """Same embedding model as notebook cell 35."""
    settings = get_settings()
    return HuggingFaceEmbeddings(model_name=model_name or settings.EMBEDDING_MODEL)


def build_vector_store(
    documents: Optional[List[Document]] = None,
    persist_directory: Optional[str] = None,
    batch_size: Optional[int] = None,
) -> Chroma:
    """
    Build the Chroma vector store in fixed-size batches, exactly as in
    notebook cell 35's "Batch Embedding" loop.
    """
    settings = get_settings()
    persist_directory = persist_directory or settings.CHROMA_PERSIST_DIR
    batch_size = batch_size or settings.BATCH_SIZE

    if documents is None:
        documents = load_documents()

    logger.info("Building vector store from %s documents (batch_size=%s)", len(documents), batch_size)

    embeddings = get_embeddings()
    vector_store: Optional[Chroma] = None

    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i : i + batch_size]

        if vector_store is None:
            vector_store = Chroma.from_documents(
                documents=batch_docs,
                embedding=embeddings,
                persist_directory=persist_directory,
            )
        else:
            vector_store.add_documents(batch_docs)

        logger.info("Batch %s finished", (i // batch_size) + 1)
        del batch_docs
        gc.collect()

    logger.info("Vector store created successfully at %s", persist_directory)
    return vector_store


if __name__ == "__main__":
    # Standalone ingestion entry point:
    #   python -m app.vector_store.builder
    build_vector_store()
