from tools.search import SearchTool


def get_weather(location: str, query: str) -> str:
    print(f"🛠️ [TOOL: weather] Fetching weather for '{location}' (query: '{query}')...")
    query_lower = query.lower()
    if any(word in query_lower for word in ["today", "now", "current"]):
        print("🛠️ [TOOL: weather] Detected real-time keyword, triggering web_search...")
        return SearchTool().run(f"current weather in {location}")
    else:
        print("🛠️ [TOOL: weather] Returning static mock weather.")
        return "Sunny, 28°C"
