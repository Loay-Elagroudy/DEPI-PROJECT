"""
Application configuration.

All values are sourced from environment variables so the exact same codebase
runs unmodified locally, in Docker, and on Azure App Service. Defaults mirror
the parameters used in the original Milestone 2 notebook so behavior is
unchanged unless explicitly overridden via the environment.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    """Central application settings, loaded from environment / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App metadata ---
    APP_NAME: str = "Consumer Complaints RAG Chatbot API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production
    LOG_LEVEL: str = "INFO"

    # --- Google Gemini (Milestone 2 generation model) ---
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.1-flash-lite"

    # --- Embeddings (Milestone 2, cell 35) ---
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --- Data / vector store paths ---
    DATA_CSV_PATH: str = str(PROJECT_ROOT / "data" / "processed_corpus_5000.csv")
    CHROMA_PERSIST_DIR: str = str(PROJECT_ROOT / "models" / "chromadb_index")
    CHROMA_COLLECTION_NAME: str = "complaints_rag"

    # --- Vector store build parameters (cell 35 CONFIG block, unchanged) ---
    MAX_ROWS: Optional[int] = 5000
    BATCH_SIZE: int = 1000

    # --- Retrieval defaults (cell 37: retriever = vector_store.as_retriever(k=3)) ---
    RETRIEVER_TOP_K: int = 3
    RETRIEVER_SEARCH_TYPE: str = "similarity"

    # --- CORS ---
    CORS_ORIGINS: str = "*"

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (avoids re-parsing env on every call)."""
    return Settings()
