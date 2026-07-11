# Architecture Overview

## High-level flow

```
Streamlit Frontend  --HTTP-->  FastAPI Backend  --->  Chroma Vector Store (persisted)
      |                              |
      |                              +--> Gemini 2.5 Flash (google-genai)
      |
      +--> Evaluation Dashboard --> /api/v1/evaluation/*
```

## Backend layout (`backend/app/`)

| Module | Responsibility | Notebook origin |
|---|---|---|
| `config/settings.py` | Environment-driven configuration | n/a (new) |
| `core/` | Logging, custom exceptions/handlers | n/a (new) |
| `utils/data_loader.py` | CSV -> `Document` conversion | Cell 35 (data-prep half) |
| `vector_store/builder.py` | Batch-build Chroma index | Cell 35 |
| `vector_store/store.py` | Load persisted index, build retrievers | Cell 37 |
| `rag/prompts.py` | Prompt templates | Cells 37, 46 |
| `rag/chain.py` | Gemini client + LCEL RAG chain | Cell 37 |
| `evaluation/generation_metrics.py` | BLEU/ROUGE scoring | Cell 41 |
| `evaluation/retrieval_metrics.py` | Recall@K / MRR scoring | Cell 43 |
| `evaluation/run_qualitative.py` | 9 fixed test queries -> report | Cell 39 |
| `evaluation/run_all.py` | Standalone: run all evaluation, independent of API | Cells 39/41/43/54 |
| `optimization/*_comparison.py` | Prompt / embedding / chunk / strategy experiments | Cells 46/48/51/53 |
| `optimization/run_optimization.py` | Standalone: run all experiments -> markdown report | Cell 53 |
| `services/` | Orchestration between API and rag/evaluation/optimization modules | n/a (new) |
| `api/` | FastAPI routers (chat, retrieval, evaluation, health) | n/a (new) |
| `schemas/` | Pydantic request/response models | n/a (new) |
| `main.py` | FastAPI app factory, middleware, routers | n/a (new) |

**No file in this table changes the algorithms, models, hyperparameters, or evaluation logic
from the notebook** -- they are the same code, split into importable modules and given
type hints, docstrings, and error handling.

## Frontend layout (`frontend/`)

- `streamlit_app.py` -- welcome/landing page with live API health status.
- `pages/1_Chat.py` -- chat UI with retrieved-context viewer, typing indicator, reset button.
- `pages/2_Evaluation_Dashboard.py` -- on-demand BLEU/ROUGE and Recall@K/MRR runs + charts.
- `pages/3_Model_Info.py` -- model/config summary and pipeline explanation.
- `utils/api_client.py` -- all HTTP calls to the backend, isolated from UI code.

## Why the notebook's Milestone 1 is absent

The app assumes `data/processed_corpus_5000.csv` is already the final, cleaned Milestone 1
output. There is deliberately no ingestion/cleaning/EDA code anywhere in `backend/app/` --
those steps were completed once, offline, in the notebook, and are out of scope for the
production application.
