"""
config/settings.py

Central configuration module for the AI Demystified Starter Kit.
Loads environment variables using python-dotenv and exposes them
as simple constants for use across the project.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# --- LLM Provider ---
# Selects which LLM backend to use: "openai" or "groq"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- Pinecone (for future RAG integration) ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENV = os.getenv("PINECONE_ENV", "")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "")

# --- LLM Parameters ---
# Default model names; can be overridden via .env if needed
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# --- Tavily (for web search) ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
