import os
import httpx
from tools.base import BaseTool

class SearchTool(BaseTool):
    """Tool to search the web using Tavily API."""
    name: str = "search"
    description: str = "Searches the web for latest information, news, or world knowledge."

    def run(self, payload: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Tavily API key not configured. Mock result for: " + payload
            
        try:
            response = httpx.post(
                "https://api.tavily.com/search",
                json={"api_key": api_key, "query": payload, "search_depth": "basic", "max_results": 3},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            if not results:
                return "No results found."
            
            formatted_results = []
            for r in results:
                title = r.get('title', 'No Title')
                content = r.get('content', 'No Content')
                formatted_results.append(f"- {title}: {content}")
            return "\n".join(formatted_results)
        except Exception as e:
            return f"Search failed: {str(e)}"
