# 🤖 AI Demystified Starter Kit: Code & Structure Guide

Welcome to the AI Demystified Starter Kit! This document explains the codebase simply so you can understand what each part does and how it all connects.

---

## 📁 Folder Structure Explained

Here is a quick overview of what each file and folder does in the project:

- **`app.py`**: The main entry point. This runs the Streamlit web interface (the UI) where you chat with the agent.
- **`requirements.txt`**: A list of all the Python packages needed to run this project (like Streamlit, OpenAI, Groq, etc.).
- **`.env` & `.env.example`**: These files store your secret API keys safely. `.env.example` is the template, and `.env` is where you actually put your keys (never commit `.env` to GitHub!).
- **`config/`**: Holds configuration settings.
- **`agent/`**: The "brain" of our AI. It contains the logic for routing messages, talking to the LLM (Large Language Model), and running tools.
- **`tools/`**: The "hands" of our AI. This folder contains specific actions the AI can take, like using a calculator.
- **`services/`**: Small helper services, like checking if your API keys are set up correctly.
- **`rag/`**: Setup for "Retrieval-Augmented Generation", which is how we will give the AI long-term memory in the future using a database called Pinecone.

---

## 🧩 Deep Dive into the Code

Let's look at how each specific part of the code works and *why* it is designed this way.

### 1. `app.py` (The User Interface)
This is a Streamlit application. 
- **What it does**: It creates the webpage. It displays the chat history, provides a text box for your input, and shows a sidebar with a system health check.
- **How it works**: When you hit Enter, it takes your message and passes it to `run_agent(user_input)` (located in the `agent` folder). Once the agent replies, `app.py` displays the text on the screen.

### 2. `config/settings.py` (Central Configuration)
- **Why it's here**: Instead of reading from the `.env` file in every single script, we load the API keys and settings *once* in this file.
- **How it works**: It uses `dotenv` to pull your `OPENAI_API_KEY`, `GROQ_API_KEY`, and preferred `LLM_PROVIDER` into simple variables. Every other file imports from here, keeping things clean.

### 3. The `agent/` Folder (The Brain)
This is where the magic happens. We split this into multiple files so it's easy to read and maintain:
- **`core.py`**: The boss. It takes the user's message, asks the `router` what to do, and then hands the job to either a `tool` or the `llm`. 
- **`router.py`**: The traffic cop. It privately asks the LLM: *"Does this user's message require a tool like a calculator?"* It returns the tool's name if yes, or nothing if no.
- **`executor.py`**: The doer. If the router picks a tool, this script finds the tool and runs it with the user's data.
- **`llm.py`**: The conversationalist. If no tool is needed, this script sends your message to OpenAI or Groq to get a standard chat response. It's built to easily let you switch between different AI providers.

### 4. The `tools/` Folder (The Actions)
An AI gets much smarter when it can use tools.
- **`base.py`**: This is a blueprint (an Abstract Class). It forces every tool we build to have a standard `name`, `description`, and a `run()` function. This ensures the `executor` always knows exactly how to trigger any tool.
- **`calculator.py`**: An actual tool built from the blueprint. If a user asks a math question, the router sends the math expression to this file, which strictly evaluates the numbers and returns the answer.

### 5. `services/health.py` (System Status)
- **What it does**: It checks if your keys (like OpenAI or Pinecone) are properly loaded.
- **Why it's helpful**: Instead of the app crashing on startup because you forgot an API key, this service safely checks your environment and shows a friendly ✅ or ❌ in the Streamlit sidebar.

### 6. `rag/pinecone_client.py` (Future Memory)
- **What it does**: Right now, it's just a connection setup for Pinecone (a vector database). 
- **Why it's here**: By default, LLMs cannot read large documents or remember previous sessions well. In the future, we will use this database to search through heavy text documents and feed only the relevant pieces to the AI—a process called RAG (Retrieval-Augmented Generation).

---

## 🚀 How a Message Flows (The Big Picture)

1. You type `"calculate 10 + 25"` in **`app.py`**.
2. The message goes to **`agent/core.py`**.
3. **`core.py`** asks **`router.py`**: *"Does this need a tool?"*
4. **`router.py`** sees it's math and says: *"Yes, use the `calculator` tool with the payload `10 + 25`"*.
5. **`core.py`** tells **`executor.py`** to run the calculator.
6. **`tools/calculator.py`** does the math and returns `"35"`.
7. The answer goes all the way back to **`app.py`** and appears on your screen!

*If you had typed a normal question like "What is AI?", the router would say "No tool needed," and `core.py` would just ask `llm.py` to generate a chat response instead.*
