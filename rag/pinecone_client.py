"""
rag/pinecone_client.py

Pinecone Vector DB — Initialization Stub
─────────────────────────────────────────
This module sets up the Pinecone client connection.
Retrieval (RAG) is NOT implemented yet — this is a placeholder
designed to be expanded in future workshop versions.

Future steps to implement RAG:
  1. Create an index if it doesn't exist
  2. Add an `embed_and_upsert(text, metadata)` function
  3. Add a `query(prompt, top_k)` function
  4. Wire the results into the agent's context window
"""

from config.settings import PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX


def init_pinecone() -> bool:
    """
    Initialize the Pinecone client using credentials from .env.

    Returns:
        True if initialization succeeded, False otherwise.
    """
    if not PINECONE_API_KEY:
        print("Pinecone: API key not set. Skipping initialization.")
        return False

    try:
        from pinecone import Pinecone

        # Create a Pinecone client instance
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Optional: log the available indexes for confirmation
        indexes = pc.list_indexes().names()
        # print(f"Pinecone initialized. Available indexes: {list(indexes)}")

        return True

    except ImportError:
        print("Pinecone SDK not installed. Run: pip install pinecone-client")
        return False
    except Exception as e:
        print(f"Pinecone initialization failed: {e}")
        return False


# ─── REAL RAG FUNCTIONS ───────────────────────────────────────────────────

MOCK_DATABASE = [
    {
        "id": "doc1",
        "text": "The AI Demystified Starter Kit is an educational project designed to help students and developers understand how AI agents work under the hood by building simple, real-world examples.",
    },
    {
        "id": "doc2",
        "text": "RAG stands for Retrieval-Augmented Generation. Instead of relying solely on an AI's pre-trained memory, RAG first 'retrieves' relevant facts from an external database and gives them to the AI, allowing it to generate highly accurate and up-to-date answers.",
    },
    {
        "id": "doc3",
        "text": "Pinecone is a cloud-based vector database. In AI, text is converted into numbers called 'vectors' so that similar concepts are placed closer together. Pinecone stores these vectors and searches through them lightning-fast to find relevant information.",
    },
    {
        "id": "doc4",
        "text": "The instructor for this AI tutorial is a passionate AI expert who specializes in breaking down complex topics into minimal, easy-to-understand code for straightforward learning.",
    },
]

# ─── IMPLEMENTING RAG FUNCTIONS (not implemented yet) ───────────────────────────────


def get_openai_embedding(text: str) -> list[float]:
    from openai import OpenAI
    import httpx

    # Same client pattern as llm.py
    from config.settings import OPENAI_API_KEY

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set.")
    client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


def embed_and_upsert(text: str, doc_id: str, metadata: dict = None) -> None:
    """Embed text and store it in Pinecone."""
    from pinecone import Pinecone, ServerlessSpec
    from config.settings import PINECONE_API_KEY, PINECONE_INDEX

    if not PINECONE_API_KEY or not PINECONE_INDEX:
        print("Missing Pinecone credentials. Skipping upsert.")
        return

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Automatically create the index if it doesn't exist
    if not pc.has_index(PINECONE_INDEX):
        print(f"Index '{PINECONE_INDEX}' not found. Creating it now...")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=1536,  # This matches OpenAI's text-embedding-3-small
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(PINECONE_INDEX)

    embedding = get_openai_embedding(text)
    meta = metadata or {}
    meta["text"] = text

    index.upsert(vectors=[(doc_id, embedding, meta)])

def query(prompt: str, top_k: int = 3) -> list[str]:
    """Retrieve the top_k most relevant chunks for a given prompt."""
    from pinecone import Pinecone
    from config.settings import PINECONE_API_KEY, PINECONE_INDEX

    if not PINECONE_API_KEY or not PINECONE_INDEX:
        print("Missing Pinecone credentials. Returning empty context.")
        return []

    try:
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX)

        query_embedding = get_openai_embedding(prompt)

        results = index.query(
            vector=query_embedding, top_k=top_k, include_metadata=True
        )

        return [
            match.metadata["text"]
            for match in results.matches
            if "text" in match.metadata
        ]
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []

