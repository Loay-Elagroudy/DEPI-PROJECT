# API Reference

Base URL (local): `http://localhost:8000`
Interactive docs: `GET /docs` (Swagger UI), `GET /redoc` (ReDoc), `GET /openapi.json`

All endpoints are versioned under `/api/v1`.

## Health

### `GET /api/v1/health`
Returns service status, vector store readiness, and configured models.

```json
{
  "status": "ok",
  "vector_store_ready": true,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "gemini_model": "gemini-2.5-flash",
  "google_api_key_configured": true,
  "version": "1.0.0"
}
```

## Chat

### `POST /api/v1/chat`
Runs the full RAG pipeline (retrieve -> format context -> generate with Gemini).

Request:
```json
{ "question": "What issue was filed against Wells Fargo about credit cards?" }
```
Optional query param: `?k=5` overrides top-K retrieval.

Response:
```json
{
  "answer": "...",
  "question": "...",
  "sources": [
    { "complaint_id": "6079679", "company": "TRANSUNION INTERMEDIATE HOLDINGS, INC.", "snippet": "..." }
  ]
}
```

## Retrieval

### `POST /api/v1/retrieve`
Runs retrieval only, no generation. Useful for debugging the retriever independently.

Request:
```json
{ "query": "identity theft credit card", "k": 5, "search_type": "similarity" }
```

## Evaluation

### `GET /api/v1/evaluation/generation`
Runs the BLEU/ROUGE generation-quality evaluation (cell 41) and returns per-question scores.

### `GET /api/v1/evaluation/retrieval`
Runs the Recall@K / MRR retrieval-quality evaluation (cell 43) for k = 1, 3, 5.

### `POST /api/v1/evaluation/qualitative`
Runs the 9 fixed test queries (cell 39) through the live RAG chain and saves
`evaluation_report.txt`.

### `GET /api/v1/evaluation/summary`
Combined generation + retrieval metrics in one call.

## Errors

Errors follow a consistent shape:
```json
{ "error": "VectorStoreNotReadyError", "message": "Vector store is not ready. Build it first via the ingestion step." }
```

| Status | Meaning |
|---|---|
| 422 | Request validation failed (Pydantic) |
| 502 | Gemini generation call failed |
| 503 | Vector store not built/loaded |
| 500 | Unexpected server error |
