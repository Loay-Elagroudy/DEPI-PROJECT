from app.evaluation.retrieval_metrics import evaluate_retrieval, get_relevant_ids
import pandas as pd


def test_get_relevant_ids_company_filter():
    df = pd.DataFrame(
        {
            "Complaint ID": ["1", "2", "3"],
            "Company": ["WELLS FARGO BANK", "TRANSUNION LLC", "OTHER CO"],
            "Issue": ["credit card issue", "improper use", "other"],
            "narrative_clean": ["a", "b", "c"],
        }
    )
    ids = get_relevant_ids(df, {"company_contains": "WELLS FARGO"})
    assert ids == {"1"}


def test_evaluate_retrieval_perfect_recall():
    class FakeDoc:
        def __init__(self, complaint_id):
            self.metadata = {"complaint_id": complaint_id}

    class FakeRetriever:
        def invoke(self, query):
            return [FakeDoc("1"), FakeDoc("2")]

    result = evaluate_retrieval(FakeRetriever(), ["query one"], [{"1"}], k=2)
    assert result["Recall@K"] == 1.0
    assert result["MRR"] == 1.0
