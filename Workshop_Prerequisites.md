# AI Demystified Workshop: Prerequisites & Setup Guide

Welcome to the **AI Demystified Workshop**! To ensure we can dive straight into building our AI agents, we ask that you complete a few setup steps before the workshop begins.

This guide will walk you through cloning the project repository and generating the required API keys.

---

## 1. Clone the Repository & Setup the Project

First, you'll need to get the starter code onto your local machine.

### Step 1: Clone the repository
Open your terminal and run:
```bash
git clone https://github.com/whoisnp/AI_Demystified_Starter_kit.git
cd AI_Demystified_Starter_kit
```
*(Note: If you haven't installed Git, you can also download the repository as a ZIP file from GitHub and extract it).*

### Step 2: Create a virtual environment (Recommended)
It's always best practice to use a virtual environment for Python projects.
```bash
python -m venv venv
```
Activate it:
- **Mac/Linux**: `source venv/bin/activate`
- **Windows**: `venv\Scripts\activate`

### Step 3: Install the dependencies
```bash
pip install -r requirements.txt
```

---

## 2. Setting Up Your Environment Variables

The project uses a `.env` file to store your private API keys securely. 

1. In the root folder of the project, you will find a file named `.env.example`.
2. Make a copy of this file and name it `.env`.
3. Open the `.env` file in your code editor. You will fill in the values below as you acquire your API keys.

---

## 3. Obtaining Your API Keys

To power our AI agent, we will need access to Large Language Models (LLMs) and a few external tools. 

### 🌟 3.1 OpenAI API Key (Highly Recommended)
For the best and most consistent experience during this workshop, we **highly request** that you use an OpenAI API key.

1. Go to the [OpenAI Developer Platform](https://platform.openai.com/).
2. Sign up or log in to your account.
3. Navigate to the **API Keys** section (usually under your profile settings on the left sidebar).
4. Click **"Create new secret key"**. Give it a recognizable name (e.g., "AI Workshop").
5. Copy the generated key. **(You won't be able to see it again once you close the modal!)**
6. Open your `.env` file and paste the key:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-proj-...your-key-here...
   OPENAI_MODEL=gpt-4o-mini
   ```



### 3.2 Groq API Key (Alternative LLM)
If you cannot use OpenAI, we support Groq as a fast, free-tier alternative.
1. Go to [Groq Console](https://console.groq.com/).
2. Sign in and navigate to the **API Keys** tab.
3. Click "Create API Key".
4. Copy the key and add it to your `.env` file:
   ```env
   GROQ_API_KEY=gsk_...your-key-here...
   GROQ_MODEL=llama-3.1-8b-instant
   ```
*(If you use Groq instead of OpenAI, change `LLM_PROVIDER=groq` in the `.env` file).*

### 3.3 Pinecone API Key (For Vector Database / RAG)
Later in the workshop, we will build a Retrieval-Augmented Generation (RAG) system. For this, we need a Vector Database.
1. Go to [Pinecone](https://www.pinecone.io/) and create a free account.
2. Once logged in, go to the **API Keys** section in the left sidebar.
3. Copy the API key provided (or create a new one).
4. Paste it into your `.env` file:
   ```env
   PINECONE_API_KEY=pcsk_...your-key-here...
   PINECONE_ENV=dev
   PINECONE_INDEX=ai-demystified-1536
   ```

### 3.4 Tavily API Key (For Web Search Tool)
To give our AI agent the ability to search the web, we rely on the Tavily Search API.
1. Go to [Tavily](https://tavily.com/) and sign up for a free developer account.
2. Once you are in the dashboard, generate a new API key.
3. Paste it into your `.env` file:
   ```env
   TAVILY_API_KEY=tvly-...your-key-here...
   ```

---

## 4. Run the Project
Once you have your `.env` file filled out, you can test if everything is working perfectly.

Run the Streamlit application with the following command:
```bash
streamlit run app.py
```

Your browser should automatically open to **http://localhost:8501** 🚀.

See you at the workshop! If you encounter any issues during setup, don't worry—we will help you troubleshoot before we kick things off.

---

### ⚠️ Important Note Regarding OpenAI and Groq for the Workshop
Later in the workshop, we will be building a **Retrieval-Augmented Generation (RAG)** system which strictly requires an OpenAI API key for text embeddings. 

For this reason, an **OpenAI API key is absolutely necessary**. Even if you plan to use the free version of Groq for the AI answer generation (LLM response), **you will still absolutely need an OpenAI key for the text embedding portion**. While the free version of OpenAI *might* work for embeddings, it is highly likely you will quickly get a "Quota Exceeded" error.

**💡 Cost-Saving Tip (Team Sharing):**
You will need a minimum of $5 preloaded into your OpenAI account to generate an API key. Since the maximum usage per person during the workshop will only be around $1 to $2, **you can group up!** If 2 or 3 people combine to recharge $5 on a single account, you can simply generate 3 separate API keys from that one account and share them amongst yourselves to use during the workshop.
