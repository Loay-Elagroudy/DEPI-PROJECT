# Installation Guide

## Prerequisites
- Python 3.11+
- A Google Gemini API key (for generation)
- ~2 GB free disk (embedding model + Chroma index)

## 1. Clone and configure
```bash
git clone <your-repo-url>
cd <repo>
cp .env.example backend/.env
# edit backend/.env and set GOOGLE_API_KEY
```

## 2. Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab   # needed for BLEU tokenization
```

### Build the vector store (one-time, or whenever the corpus changes)
```bash
python -m app.vector_store.builder
```
This reads `data/processed_corpus_5000.csv` and writes a persisted Chroma index to
`models/chromadb_index/`.

### Run the API
```bash
uvicorn app.main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` for interactive API docs.

## 3. Frontend setup
```bash
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_BASE_URL=http://localhost:8000   # Windows: set API_BASE_URL=...
streamlit run streamlit_app.py
```
Visit `http://localhost:8501`.

## 4. Run tests
```bash
cd backend
pytest -v
```

## 5. Run evaluation / optimization independently of the API
```bash
cd backend
python -m app.evaluation.run_all          # BLEU/ROUGE + Recall@K/MRR + qualitative report
python -m app.optimization.run_optimization # prompt/embedding/chunk/strategy experiments
```
