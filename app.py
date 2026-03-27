"""
app.py

Streamlit UI — AI Demystified Starter Kit
──────────────────────────────────────────
This is the main entry point for the web application.
Run it with: streamlit run app.py

The UI consists of:
  - A sidebar with a system health check panel
  - A main chat area with persistent message history
  - A text input to send messages to the agent
"""

import streamlit as st
from agent.core import run_agent
from services.health import get_health_status

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Demystified",
    page_icon="🤖",
    layout="centered",
)

# ── Sidebar: Health Check ─────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔧 System Status")
    st.caption("Checks that your API keys and config are loaded correctly.")
    st.divider()

    health = get_health_status()

    # LLM Provider info
    st.markdown(f"**Provider:** `{health['llm_provider'].upper()}`")
    st.markdown(f"**Model:** `{health['llm_model']}`")

    # LLM key status
    if health["llm_key_set"]:
        st.success(f"✅ LLM API Key is set")
    else:
        st.error(f"❌ LLM API Key is missing")
        st.caption(
            f"Set `{'OPENAI_API_KEY' if health['llm_provider'] == 'openai' else 'GROQ_API_KEY'}` "
            "in your `.env` file."
        )

    st.divider()

    # Pinecone key status
    if health["pinecone_key_set"]:
        st.success("✅ Pinecone Key is set")
    else:
        st.warning("⚠️ Pinecone Key not set")
        st.caption("Not required yet — needed for future RAG features.")

    st.divider()
    st.caption("💡 Tip: Type **'calculate 10 + 25'** to trigger the calculator tool!")

# --------------------------STRICT RAG MODE TOGGLE (DEMO PURPOSES) START-----------------------------
    st.divider()
    st.session_state.strict_rag_mode = st.toggle(
        "🔒 Strict RAG Mode (Demo)",
        value=False,
        help="When enabled, the agent will only use the RAG system and will not fallback to general knowledge.",
    )
# --------------------------STRICT RAG MODE TOGGLE (DEMO PURPOSES) END-----------------------------

# ── Main Chat Interface ───────────────────────────────────────────────────────
st.title("🤖 AI Demystified")
st.caption("A simple AI assistant powered by OpenAI or Groq — your choice.")

st.divider()

# Initialize chat history in session state (persists across reruns)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hi! I'm your AI assistant. Ask me anything, "
                "or try typing **'calculate 15 * 7'** to see the tool router in action!"
            ),
        }
    ]

# Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat Input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Type your message here...")

if user_input:
    # 1. Show the user's message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Get the agent's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            strict_mode = st.session_state.get("strict_rag_mode", False)
            response = run_agent(user_input, strict_rag=strict_mode)
        st.markdown(response)

    # 3. Save the assistant's response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
