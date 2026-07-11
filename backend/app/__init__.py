"""
App package init.

Disables ChromaDB's anonymized telemetry *before* chromadb/langchain_chroma
get imported anywhere else in the app. This must live here (not in
config/settings.py) because Python fully executes this file before
resolving any `app.<submodule>` import, guaranteeing the env var is set
before chromadb's telemetry client is constructed.

This silences the noisy (harmless) posthog errors:
    "Failed to send telemetry event ...: capture() takes 1 positional
    argument but 3 were given"
which come from a version mismatch between chromadb's bundled telemetry
code and newer posthog releases -- see chroma-core/chroma#4966.
"""
import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "FALSE")
