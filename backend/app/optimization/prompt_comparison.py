"""Prompt engineering comparison -- preserves notebook cell 46 exactly."""
import pandas as pd

from app.evaluation.generation_metrics import calculate_metrics
from app.rag.prompts import get_prompt


def run_comparison(retriever, client, gemini_model: str, eval_dataset) -> pd.DataFrame:
    """Identical to cell 46's `run_comparison`."""
    results = []
    for item in eval_dataset:
        docs = retriever.invoke(item["question"])
        context = "\n\n".join(doc.page_content for doc in docs)

        for version in ("v1", "v2"):
            full_prompt = get_prompt(context, item["question"], version)
            response = client.models.generate_content(model=gemini_model, contents=full_prompt)
            r1, rl, bleu = calculate_metrics(response.text, item["ground_truth"])
            results.append(
                {
                    "Version": version,
                    "Question": item["question"][:40] + "...",
                    "ROUGE-1": r1,
                    "ROUGE-L": rl,
                    "BLEU": bleu,
                }
            )
    return pd.DataFrame(results)
