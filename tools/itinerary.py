from agent.llm import get_llm_response

def generate_itinerary(destination: str, days: int) -> str:
    print(f"🛠️ [TOOL: itinerary] Building {days}-day itinerary prompt for '{destination}'...")
    prompt = (
        f"Create a {days}-day itinerary for a trip to {destination}.\n"
        "STRICT RULES:\n"
        "- Provide a day-wise plan.\n"
        "- Maximum 3 bullet points per day.\n"
        "- No long paragraphs.\n"
        "- No filler text."
    )
    print("🛠️ [TOOL: itinerary] Requesting LLM to generate itinerary...")
    result = get_llm_response(prompt)
    print("🛠️ [TOOL: itinerary] Itinerary generation complete.")
    return result
