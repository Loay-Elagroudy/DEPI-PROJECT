"""
Loads the already-cleaned Milestone 1 corpus and turns rows into LangChain
``Document`` objects.

This mirrors the "Prepare Data" and "Sample Documents" blocks of notebook
cell 35 exactly (same columns, same metadata keys). It intentionally does
NOT re-clean or re-derive `rag_document` -- that is Milestone 1's job and is
assumed already done in the CSV.
"""
from typing import List, Optional

import pandas as pd
from langchain_core.documents import Document

from app.config.settings import get_settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


def load_processed_corpus(csv_path: Optional[str] = None) -> pd.DataFrame:
    """Load the cleaned Milestone 1 output CSV (`processed_corpus_5000.csv`)."""
    settings = get_settings()
    path = csv_path or settings.DATA_CSV_PATH
    df = pd.read_csv(path)
    logger.info("Loaded processed corpus: %s rows from %s", len(df), path)
    return df


def dataframe_to_documents(df: pd.DataFrame, max_rows: Optional[int] = None) -> List[Document]:
    """
    Convert corpus rows into Documents, identical to notebook cell 35:

        df_processed = df.dropna(subset=["rag_document"]).copy()
        if MAX_ROWS is not None:
            df_processed = df_processed.head(MAX_ROWS)
        ... Document(page_content=row["rag_document"],
                     metadata={"complaint_id": ..., "company": ...})
    """
    df_processed = df.dropna(subset=["rag_document"]).copy()
    if max_rows is not None:
        df_processed = df_processed.head(max_rows)

    documents = [
        Document(
            page_content=row["rag_document"],
            metadata={
                "complaint_id": str(row["Complaint ID"]),
                "company": str(row["Company"]),
            },
        )
        for _, row in df_processed.iterrows()
    ]
    return documents


def load_documents(csv_path: Optional[str] = None, max_rows: Optional[int] = None) -> List[Document]:
    """Convenience wrapper: CSV path -> list[Document]."""
    settings = get_settings()
    df = load_processed_corpus(csv_path)
    effective_max_rows = settings.MAX_ROWS if max_rows is None else max_rows
    return dataframe_to_documents(df, max_rows=effective_max_rows)


def load_dataframe_for_ground_truth(csv_path: Optional[str] = None, max_rows: Optional[int] = None) -> pd.DataFrame:
    """
    Return the same `df_processed` slice used to build the vector store, for
    use by the retrieval-evaluation ground-truth filters (cell 43), which
    query `Company` / `Issue` / `narrative_clean` / `Complaint ID` columns.
    """
    settings = get_settings()
    df = load_processed_corpus(csv_path)
    df_processed = df.dropna(subset=["rag_document"]).copy()
    effective_max_rows = settings.MAX_ROWS if max_rows is None else max_rows
    if effective_max_rows is not None:
        df_processed = df_processed.head(effective_max_rows)
    return df_processed
