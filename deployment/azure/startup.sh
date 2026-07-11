#!/bin/bash
# Azure App Service startup command (code deployment, no Docker).
# Set this exact line as the "Startup Command" in
# Azure Portal -> App Service -> Configuration -> General settings.

python -m nltk.downloader punkt punkt_tab -d /home/nltk_data
gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 --timeout 600
