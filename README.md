# 🤖 Consumer Complaints RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) application that answers natural-language
questions about consumer financial complaints (CFPB dataset), grounded in retrieved complaint
records and generated with Google Gemini.

This repository is the production build of a two-milestone research project. **Only Milestone 2
(the RAG/NLP system) is implemented here** — data collection, cleaning, and EDA (Milestone 1) are
assumed already complete and are represented solely by the cleaned input file,
`data/processed_corpus_5000.csv`.

## Screenshots

> _Add screenshots here after your first local run:_
> `docs/screenshots/welcome.png`, `docs/screenshots/chat.png`, `docs/screenshots/dashboard.png`

## Features

- **RAG pipeline**: Chroma vector store + `sentence-transformers/all-MiniLM-L6-v2` embeddings +
  Gemini 2.5 Flash generation.
- **Evaluation**: BLEU / ROUGE-1 / ROUGE-L (generation quality), Recall@K / MRR (retrieval quality).
- **Optimization experiments**: prompt engineering, embedding model, chunk size/overlap, and
  retrieval strategy (similarity vs. MMR) comparisons.
- **FastAPI backend** with Swagger/OpenAPI docs, request validation, structured error handling.
- **Streamlit frontend**: welcome page, chat with retrieved-context viewer, evaluation dashboard,
  model info page.
- **Tests**: pytest suite covering API endpoints, retrieval, evaluation, and utilities.
- **Deployment**: Azure App Service (primary, no Docker) + optional Docker/docker-compose.

## Project Structure

```
project/
├── backend/            # FastAPI app (clean architecture: api/core/config/rag/vector_store/
│                        #   evaluation/optimization/services/models/schemas/utils)
├── frontend/            # Streamlit multipage app
├── data/                 # Cleaned Milestone 1 output (processed_corpus_5000.csv)
├── models/              # Persisted Chroma vector store (generated, gitignored)
├── notebooks/            # Original research notebook (reference only)
├── tests/               # Reserved for cross-stack integration tests
├── deployment/
│   ├── azure/            # Azure App Service startup + notes (primary deployment)
│   └── docker/           # Optional Docker artifacts
├── docs/                 # Architecture, API, deployment, installation docs
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
└── LICENSE
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for a full module-by-module breakdown and its
mapping back to the original notebook cells.

## Quick Start

```bash
cp .env.example backend/.env   # set GOOGLE_API_KEY

cd backend
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab
python -m app.vector_store.builder     # builds the vector store once
uvicorn app.main:app --reload --port 8000

# in a second terminal
cd frontend
pip install -r requirements.txt
export API_BASE_URL=http://localhost:8000
streamlit run streamlit_app.py
```

Full instructions: [`docs/INSTALLATION.md`](docs/INSTALLATION.md).

## Standalone Evaluation & Optimization

Both run independently of the API, exactly as in the original notebook:

```bash
cd backend
python -m app.evaluation.run_all             # BLEU/ROUGE, Recall@K/MRR, qualitative report
python -m app.optimization.run_optimization  # prompt / embedding / chunk / strategy experiments
```

## API

Interactive docs at `/docs` once the backend is running. Reference: [`docs/API.md`](docs/API.md).

## Deployment

Primary target: **Azure App Service** (code deployment, no Docker) —
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) · [`deployment/azure/deploy_notes.md`](deployment/azure/deploy_notes.md).

Optional Docker path also documented in the same guide.

## Testing

```bash
cd backend
pytest -v
```

## What Was Preserved From the Notebook

Every RAG, retrieval, generation, evaluation, and optimization behavior in `backend/app/rag/`,
`backend/app/vector_store/`, `backend/app/evaluation/`, and `backend/app/optimization/` is the
same logic as the notebook's Milestone 2 cells — same models, same hyperparameters, same prompts,
same metrics — reorganized into typed, documented, testable modules. See
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the exact cell-to-module mapping.

## Contributing

1. Fork the repo and create a feature branch.
2. Keep RAG/evaluation/optimization logic behavior-identical unless explicitly asked to change it.
3. Add/update tests for any new backend code.
4. Open a PR describing the change and why.
