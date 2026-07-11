# Deployment Guide

## Azure App Service (Recommended)

This project is designed to be deployed on **Azure App Service** using a standard Python deployment.

For detailed deployment instructions, see:

`deployment/azure/deploy_notes.md`

### Deployment Steps

1. Create two Linux App Services using **Python 3.11**:

   * Backend (FastAPI)
   * Frontend (Streamlit)

2. Configure the required application settings (environment variables) as described in `deploy_notes.md`, especially:

   * `GOOGLE_API_KEY`

3. Configure the backend startup command to use Gunicorn with the Uvicorn worker class:

   ```bash
   deployment/azure/startup.sh
   ```

4. Deploy the application using one of the following:

   * Azure CLI (`az webapp up`)
   * GitHub Deployment Center

5. After the first deployment, build the vector database by connecting to the backend App Service through SSH and running:

   ```bash
   python -m app.vector_store.builder
   ```

6. Set the frontend's `API_BASE_URL` environment variable to the deployed backend URL.

---

## Deployment to Other Python Hosts

The application can also be deployed to any Python hosting platform that supports **Python 3.11**, such as:

* Render
* Railway
* Azure App Service
* Virtual Machines (Linux)
* Other cloud providers

### Backend

Install the dependencies from:

```text
backend/requirements.txt
```

Start the FastAPI application with:

```bash
gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind=0.0.0.0:$PORT
```

### Frontend

Start the Streamlit application with:

```bash
streamlit run streamlit_app.py \
  --server.port=$PORT \
  --server.address=0.0.0.0
```

### Initial Setup

After deploying the backend for the first time, build the persisted vector store:

```bash
python -m app.vector_store.builder
```

Once the vector store has been created, the chatbot is ready to answer user queries.
