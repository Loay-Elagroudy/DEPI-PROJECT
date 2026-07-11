from typing import Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    vector_store_ready: bool
    embedding_model: str
    gemini_model: str
    google_api_key_configured: bool
    version: str
