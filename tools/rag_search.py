"""
tools/rag_search.py

RAG Search Tool
───────────────
Queries the vector database (Pinecone) for relevant context.
Strictly returns NO_CONTEXT if no relevant results are found.
"""

from tools.base import BaseTool
from rag.pinecone_client import query


class RagSearchTool(BaseTool):
    name: str = "rag_search"
    description: str = "Search the knowledge base for helpful context to answer factual queries."

    def run(self, payload: str) -> str:
        """
        Query the datastore.
        
        Args:
            payload: The user's query.
            
        Returns:
            The combined text chunks or NO_CONTEXT.
        """
        print(f"🛠️ [TOOL: rag_search] Querying Pinecone vector database for: '{payload}'")
        results = query(payload, top_k=2)
        
        if not results:
            print("🛠️ [TOOL: rag_search] No relevant results found in database (returning NO_CONTEXT).")
            return "NO_CONTEXT"
            
        print(f"🛠️ [TOOL: rag_search] Found {len(results)} relevant document chunks.")
        return "\n".join(results)
