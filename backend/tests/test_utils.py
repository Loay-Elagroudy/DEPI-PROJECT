import pandas as pd

from app.utils.data_loader import dataframe_to_documents


def test_dataframe_to_documents_basic():
    df = pd.DataFrame(
        {
            "Complaint ID": [1, 2],
            "Company": ["Acme Corp", "Beta Inc"],
            "rag_document": ["doc one text", "doc two text"],
        }
    )
    docs = dataframe_to_documents(df)
    assert len(docs) == 2
    assert docs[0].page_content == "doc one text"
    assert docs[0].metadata["complaint_id"] == "1"
    assert docs[0].metadata["company"] == "Acme Corp"


def test_dataframe_to_documents_drops_missing_rag_document():
    df = pd.DataFrame(
        {
            "Complaint ID": [1, 2],
            "Company": ["Acme Corp", "Beta Inc"],
            "rag_document": ["doc one text", None],
        }
    )
    docs = dataframe_to_documents(df)
    assert len(docs) == 1


def test_dataframe_to_documents_respects_max_rows():
    df = pd.DataFrame(
        {
            "Complaint ID": [1, 2, 3],
            "Company": ["A", "B", "C"],
            "rag_document": ["a", "b", "c"],
        }
    )
    docs = dataframe_to_documents(df, max_rows=2)
    assert len(docs) == 2
