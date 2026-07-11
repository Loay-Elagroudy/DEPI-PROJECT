"""Embedding model comparison -- preserves notebook cell 48 exactly."""
from typing import List
from uuid import uuid4

import pandas as pd
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.evaluation.retrieval_metrics import evaluate_retrieval

EMBEDDING_MODELS = ["all-MiniLM-L6-v2", "all-mpnet-base-v2"]


def build_temp_retriever(docs: List[Document], embedding_model: str, search_type: str = "similarity", k: int = 5):
    """Identical to cell 48's `build_temp_retriever` (fresh, throwaway Chroma collection)."""
    emb = HuggingFaceEmbeddings(model_name=embedding_model)
    store = Chroma.from_documents(
        documents=docs,
        embedding=emb,
        collection_name=f"temp_{uuid4().hex}",
    )
    return store.as_retriever(search_type=search_type, search_kwargs={"k": k})


def run_embedding_comparison(documents_sample: List[Document], test_queries, ground_truth_ids, embedding_models=None) -> pd.DataFrame:
    """Identical to cell 48's loop over `embedding_models`."""
    embedding_models = embedding_models or EMBEDDING_MODELS
    documents_sample = documents_sample[:500]

    embedding_results = []
    for model_name in embedding_models:
        temp_retriever = build_temp_retriever(docs=documents_sample, embedding_model=model_name, k=5)
        metrics = evaluate_retrieval(temp_retriever, test_queries, ground_truth_ids, k=5)
        metrics["Embedding Model"] = model_name
        embedding_results.append(metrics)

    return pd.DataFrame(embedding_results)
