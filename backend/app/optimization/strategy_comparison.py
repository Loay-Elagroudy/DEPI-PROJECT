"""Retrieval strategy (similarity vs MMR) comparison -- preserves cell 53 exactly."""
import pandas as pd

from app.evaluation.retrieval_metrics import evaluate_retrieval

STRATEGIES = ["similarity", "mmr"]


def run_strategy_comparison(vector_store, test_queries, ground_truth_ids, strategies=None) -> pd.DataFrame:
    """Identical to cell 53's loop over `strategy in ["similarity", "mmr"]`."""
    strategies = strategies or STRATEGIES
    strategy_results = []

    for strategy in strategies:
        strat_retriever = vector_store.as_retriever(search_type=strategy, search_kwargs={"k": 5})
        res = evaluate_retrieval(strat_retriever, test_queries, ground_truth_ids, k=5)
        res["strategy"] = strategy
        strategy_results.append(res)

    return pd.DataFrame(strategy_results)
