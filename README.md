# 🤖 AI Demystified Starter Kit

A modular, beginner-friendly Python AI assistant built for the **AI Demystified Workshop**. This project is designed to grow with you — from a simple chatbot to a full agentic AI system with RAG, multi-tool workflows, and automation pipelines.

---

## 🗂️ Project Structure

```
AI_Demystified_Starter_kit/
├── app.py                    # Streamlit web UI (entry point)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
│
├── agent/
│   ├── __init__.py           # Package init (exposes run_agent)
│   ├── core.py               # Main agent logic (tool → LLM routing)
│   ├── executor.py           # Tool executor (looks up & runs tools)
│   ├── llm.py                # LLM abstraction (OpenAI / Groq)
│   └── router.py             # LLM-based tool router
│
├── tools/
│   ├── __init__.py           # Tool registry (AVAILABLE_TOOLS)
│   ├── base.py               # BaseTool abstract class
│   └── calculator.py         # Calculator tool (math expression evaluator)
│
├── rag/
│   └── pinecone_client.py    # Pinecone init stub (RAG-ready)
│
├── services/
│   └── health.py             # System health check service
│
└── config/
    └── settings.py           # Centralized environment configuration
```

---

## ⚡ Quick Start

### 1. Clone or download the project

```bash
cd AI_Demystified_Starter_kit
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment

```bash
cp .env.example .env
```

Open `.env` and fill in your API key:

```
OPENAI_API_KEY=sk-...your-key-here...
LLM_PROVIDER=openai
```

### 5. Run the app

```bash
streamlit run app.py
```

Your browser will open at **http://localhost:8501** 🚀

---

## 🔄 Switching Between OpenAI and Groq

Open your `.env` file and change the provider:

**To use OpenAI (default):**
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**To use Groq (free tier available):**
```
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...
```

Then restart the Streamlit app. No code changes needed!

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

---

## 🧪 Try It Out

| What to type | What happens |
|---|---|
| `"What is machine learning?"` | LLM answers directly |
| `"calculate 15 * 7 + 3"` | LLM router detects math → calculator tool handles it |
| `"calculate (100 / 4) - 5"` | Calculator with parentheses |

---

## 🏗️ How It Works

```
User Input
    ↓
agent/core.py (run_agent)
    ↓
agent/router.py (route)     ← asks the LLM to classify intent
    ↓
┌─────────────────────────────────────┐
│ Tool match?                         │
│  YES → agent/executor.py            │
│          → tools/calculator.py      │
│  NO  → agent/llm.py                 │
│          → OpenAI or Groq API       │
└─────────────────────────────────────┘
    ↓
Response returned to Streamlit UI
```

---

## 🔮 Future Enhancements

This project is built to evolve. Here's the planned progression:

### 📌 Version 2 — More Tools
- Add a **weather tool** (calls a weather API)
- Add a **web search tool** (Tavily integration is prepped in settings)
- Expand the LLM router to handle new tool types

### 📌 Version 3 — RAG System
- Implement `rag/pinecone_client.py` with document embedding
- Add `embed_and_upsert()` and `query()` functions
- Give the agent a long-term memory and document knowledge base

### 📌 Version 4 — Multi-Tool Agent
- Build a **trip planner** combining weather + search + maps tools
- Add conversation history and context management
- Support multi-step reasoning flows

---

## 📋 Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `LLM_PROVIDER` | ✅ | `openai` or `groq` |
| `OPENAI_API_KEY` | If using OpenAI | Your OpenAI API key |
| `OPENAI_MODEL` | Optional | Default: `gpt-4o-mini` |
| `GROQ_API_KEY` | If using Groq | Your Groq API key |
| `GROQ_MODEL` | Optional | Default: `llama-3.1-8b-instant` |
| `PINECONE_API_KEY` | Future RAG | Your Pinecone API key |
| `PINECONE_ENV` | Future RAG | Pinecone environment |
| `PINECONE_INDEX` | Future RAG | Pinecone index name |
| `TAVILY_API_KEY` | Future Search | Your Tavily API key (for web search) |

---

## 🛠️ Built With

- [Streamlit](https://streamlit.io) — Web UI
- [OpenAI Python SDK](https://github.com/openai/openai-python) — GPT models
- [Groq Python SDK](https://github.com/groq/groq-python) — Llama/Mixtral models
- [Pinecone](https://www.pinecone.io) — Vector DB (future)
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment management

---

*Built for the AI Demystified Workshop 🎓*
