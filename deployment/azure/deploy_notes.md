# Azure App Service Deployment Notes (Backend)

Primary deployment target: **Azure App Service, code deployment (no Docker)**.

## 1. Create the App Service
- Runtime stack: **Python 3.11**
- OS: Linux
- Plan: at least B2 (2 vCPU / 3.5 GB) -- sentence-transformers + Chroma need headroom.

## 2. App settings (Environment Variables)
Set these under **Configuration -> Application settings**:

| Key | Value |
|---|---|
| `GOOGLE_API_KEY` | your Gemini API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` |
| `DATA_CSV_PATH` | `/home/site/wwwroot/data/processed_corpus_5000.csv` |
| `CHROMA_PERSIST_DIR` | `/home/site/wwwroot/models/chromadb_index` |
| `MAX_ROWS` | `5000` |
| `BATCH_SIZE` | `1000` |
| `RETRIEVER_TOP_K` | `3` |
| `ENVIRONMENT` | `production` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |
| `WEBSITES_PORT` | `8000` |

Use **Persistent storage** (`WEBSITES_ENABLE_APP_SERVICE_STORAGE=true`, the default) so the
built Chroma index in `models/chromadb_index` survives restarts.

## 3. Startup command
In **Configuration -> General settings -> Startup Command**, paste the contents of
`deployment/azure/startup.sh` (or point to the file directly):

```
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --timeout 600
```

Add `gunicorn` to `backend/requirements.txt` if not already present.

## 4. Deploy
From the `backend/` directory (Azure builds from whatever is deployed as the app root):

```bash
az webapp up --name <your-app-name> --resource-group <your-rg> --runtime "PYTHON:3.11" --sku B2
```

Or connect a GitHub repo under **Deployment Center** and let Azure build on push.

## 5. Build the vector store once, post-deploy
SSH into the App Service (**Development Tools -> SSH**) and run once:

```bash
cd /home/site/wwwroot
python -m app.vector_store.builder
```

This persists the Chroma index to `CHROMA_PERSIST_DIR` so subsequent restarts load instantly.

## 6. Frontend (Streamlit)
Deploy the Streamlit app as a **second** App Service (Python 3.11), with:
- Startup command: `streamlit run streamlit_app.py --server.port=8000 --server.address=0.0.0.0`
- App setting `API_BASE_URL` = the backend App Service's URL (e.g. `https://your-backend.azurewebsites.net`)
