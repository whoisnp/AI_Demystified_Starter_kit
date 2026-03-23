"""
agent/llm.py

LLM Abstraction Layer
─────────────────────
This module provides a single, unified function to call any supported
LLM provider. To add a new provider in the future, simply add a new
branch inside `get_llm_response()`.

Supported providers:
  - openai  → OpenAI Chat API (GPT models)
  - groq    → Groq API (Llama, Mixtral models)
"""

from config.settings import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    GROQ_API_KEY,
    OPENAI_MODEL,
    GROQ_MODEL,
)


def get_llm_response(prompt: str) -> str:
    """
    Send a prompt to the configured LLM and return its text response.

    Args:
        prompt: The user's message or constructed prompt string.

    Returns:
        The LLM's response as a plain string.

    Raises:
        ValueError: If the configured LLM_PROVIDER is not supported.
    """
    if LLM_PROVIDER == "openai":
        print("🧠 [LLM] Routing request to OpenAI...")
        return _call_openai(prompt)
    elif LLM_PROVIDER == "groq":
        print("🧠 [LLM] Routing request to Groq...")
        return _call_groq(prompt)
    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER: '{LLM_PROVIDER}'. "
            "Choose 'openai' or 'groq' in your .env file."
        )


def _call_openai(prompt: str) -> str:
    """
    Call the OpenAI Chat Completions API.

    Uses the model specified by OPENAI_MODEL in settings (default: gpt-4o-mini).
    """
    from openai import OpenAI
    import httpx

    if not OPENAI_API_KEY:
        return (
            "⚠️ OpenAI API key is not set. Please add OPENAI_API_KEY to your .env file."
        )

    # Providing our own http_client bypasses the library bug that tries to pass 'proxies'
    print("🧠 [LLM] Initializing OpenAI client...")
    client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())

    print(f"🧠 [LLM] Generating response using model: '{OPENAI_MODEL}'...")
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Be concise, clear, and friendly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    print(response.choices[0].message.content.strip())
    # Extract the text from the first choice
    print("🧠 [LLM] Response received from OpenAI.")
    return response.choices[0].message.content.strip()


def _call_groq(prompt: str) -> str:
    """
    Call the Groq Chat Completions API.

    Uses the model specified by GROQ_MODEL in settings (default: llama3-8b-8192).
    """
    from groq import Groq
    import httpx

    if not GROQ_API_KEY:
        return "⚠️ Groq API key is not set. Please add GROQ_API_KEY to your .env file."

    # Providing our own http_client bypasses the library bug that tries to pass 'proxies'
    print("🧠 [LLM] Initializing Groq client...")
    client = Groq(api_key=GROQ_API_KEY, http_client=httpx.Client())

    print(f"🧠 [LLM] Generating response using model: '{GROQ_MODEL}'...")
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Be concise, clear, and friendly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    print("🧠 [LLM] Response received from Groq.")
    return response.choices[0].message.content.strip()
