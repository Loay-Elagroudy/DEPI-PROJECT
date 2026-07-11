# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [1.0.0] - 2026-07-10
### Added
- Production FastAPI backend wrapping the Milestone 2 RAG pipeline (Chroma + HuggingFace
  `all-MiniLM-L6-v2` embeddings + Gemini 2.5 Flash generation), preserved from the source notebook.
- Evaluation module: BLEU/ROUGE generation metrics and Recall@K/MRR retrieval metrics,
  runnable via API or standalone script (`python -m app.evaluation.run_all`).
- Optimization module: prompt engineering, embedding model, chunk size/overlap, and
  retrieval strategy (similarity vs MMR) comparisons, runnable via
  `python -m app.optimization.run_optimization`.
- Polished multipage Streamlit frontend: Welcome, Chat, Evaluation Dashboard, Model Info.
- REST API with Swagger/OpenAPI docs for chat, retrieval, evaluation, and health check.
- Pytest test suite for API endpoints, retrieval pipeline, evaluation module, and utilities.
- Azure App Service deployment support (code-based, no Docker) as the primary deployment path.
- Optional Docker / docker-compose support for local or alternative deployments.
- Full documentation set: architecture, API reference, deployment guide, installation guide.

### Notes
- No Milestone 1 (data collection/cleaning/EDA) logic is included; the app consumes the
  already-cleaned `processed_corpus_5000.csv` directly.
- No MLflow integration -- the source notebook did not use MLflow.
