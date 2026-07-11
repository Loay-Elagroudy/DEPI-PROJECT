"""Thin HTTP client for the FastAPI backend."""
import os
from typing import Any, Dict, List, Optional

import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 60


def _url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}{path}"


def get_health() -> Dict[str, Any]:
    resp = requests.get(_url("/api/v1/health"), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def ask_chat(question: str, k: Optional[int] = None) -> Dict[str, Any]:
    params = {"k": k} if k else {}
    resp = requests.post(_url("/api/v1/chat"), json={"question": question}, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def retrieve_documents(query: str, k: Optional[int] = None, search_type: Optional[str] = None) -> Dict[str, Any]:
    payload = {"query": query, "k": k, "search_type": search_type}
    resp = requests.post(_url("/api/v1/retrieve"), json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def get_generation_metrics() -> List[Dict[str, Any]]:
    resp = requests.get(_url("/api/v1/evaluation/generation"), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["rows"]


def get_retrieval_metrics() -> List[Dict[str, Any]]:
    resp = requests.get(_url("/api/v1/evaluation/retrieval"), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["rows"]


def run_qualitative_eval() -> Dict[str, Any]:
    resp = requests.post(_url("/api/v1/evaluation/qualitative"), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
