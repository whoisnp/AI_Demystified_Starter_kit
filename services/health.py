"""
services/health.py

Health Check Service
─────────────────────
Validates that required API keys and configurations are present.
Returns a structured dictionary so the UI can display a readable
status panel without crashing if something is missing.

This is useful during workshop demos to immediately see what's
configured and what needs attention.
"""

from config.settings import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    GROQ_API_KEY,
    PINECONE_API_KEY,
    OPENAI_MODEL,
    GROQ_MODEL,
)
from rag.pinecone_client import init_pinecone


def get_health_status() -> dict:
    """
    Check the status of all required service configurations.

    Returns:
        A dictionary with the health state of each service. Example:
        {
            "llm_provider": "openai",
            "llm_model": "gpt-4o-mini",
            "llm_key_set": True,
            "pinecone_key_set": False,
        }
    """
    # Determine which LLM key to check based on the selected provider
    if LLM_PROVIDER == "openai":
        llm_key_set = bool(OPENAI_API_KEY)
        llm_model = OPENAI_MODEL
    elif LLM_PROVIDER == "groq":
        llm_key_set = bool(GROQ_API_KEY)
        llm_model = GROQ_MODEL
    else:
        llm_key_set = False
        llm_model = "unknown"

    return {
        "llm_provider": LLM_PROVIDER,
        "llm_model": llm_model,
        "llm_key_set": llm_key_set,
        "pinecone_key_set": init_pinecone(),
    }
