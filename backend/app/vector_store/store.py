"""
Loads the persisted Chroma vector store for serving (no rebuild), and
exposes retrievers exactly as configured in notebook cell 37:

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
"""
import os
from functools import lru_cache
from typing import Optional

from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from app.config.settings import get_settings
from app.core.exceptions import VectorStoreNotReadyError
from app.core.logging_config import get_logger
from app.vector_store.builder import get_embeddings

logger = get_logger(__name__)


@lru_cache
def get_vector_store() -> Chroma:
    """Load the persisted Chroma collection built by `vector_store.builder`."""
    settings = get_settings()
    persist_directory = settings.CHROMA_PERSIST_DIR

    if not os.path.isdir(persist_directory) or not os.listdir(persist_directory):
        raise VectorStoreNotReadyError(
            f"No vector store found at '{persist_directory}'. "
            "Run `python -m app.vector_store.builder` (or the /api/v1/health "
            "startup ingestion) to build it first."
        )

    embeddings = get_embeddings()
    store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    logger.info("Vector store loaded from %s", persist_directory)
    return store


def get_retriever(k: Optional[int] = None, search_type: Optional[str] = None) -> VectorStoreRetriever:
    """
    Return a retriever. Defaults match cell 37 exactly
    (`search_kwargs={"k": 3}`, similarity search).
    """
    settings = get_settings()
    store = get_vector_store()
    k = k or settings.RETRIEVER_TOP_K
    search_type = search_type or settings.RETRIEVER_SEARCH_TYPE
    return store.as_retriever(search_type=search_type, search_kwargs={"k": k})


def vector_store_is_ready() -> bool:
    settings = get_settings()
    persist_directory = settings.CHROMA_PERSIST_DIR
    return os.path.isdir(persist_directory) and len(os.listdir(persist_directory)) > 0
