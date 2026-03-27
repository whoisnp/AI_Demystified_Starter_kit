"""
agent/router.py

Tool Router
───────────
The router evaluates the user's message to decide if a tool should handle it.

Current behavior:
  Instead of executing the tool, it simply returns a tuple:
    (tool_name: str, payload: str)
  If no tool matches, it returns (None, None).
"""

import json
from agent.llm import get_llm_response


def route(user_input: str) -> tuple[str | None, str | None]:
    """
    Check if the user's message matches a known tool trigger using an LLM.

    Args:
        user_input: The raw message from the user.

    Returns:
        A tuple of (tool_name, payload).
        e.g., ("calculator", "10 + 25")
        If no tool matches, returns (None, None).
    """

    prompt = f"""You are an intelligent routing assistant. Your job is to classify the user's input and decide if a specific tool should handle it.

Available Tools:
1. "calculator": Use this for mathematical calculations.
2. "summarizer": Use this for summarizing given text or articles.
3. "search": Use this for searching the web for latest information, news, or world knowledge not covered by rag_search.
4. "trip_planner": Use this for queries related to planning trips, travel, budget, duration or destination.

Output your reply as a strictly valid JSON object with the following structure:
{{
  "tool": "tool_name_or_null",
  "payload": "extracted_payload_or_full_input_or_null"
}}

Rules:
- If a tool is needed, "tool" should be exactly one of: "calculator", "summarizer", "search", "trip_planner".
- If no tool is appropriate, set "tool" to null and "payload" to null.
- For "calculator" and "summarizer", the "payload" should be the specific part of the user input that needs processing.
- For "search", the "payload" should be the query string to search for.
- For "trip_planner", the "payload" should be the full user input.
- Return ONLY the raw JSON object. Do not include markdown formatting, backticks, or any other explanations.

User Input: {user_input}"""

    try:
        response = get_llm_response(prompt)

        # Clean up potential markdown formatting from the response
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]

        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        cleaned_response = cleaned_response.strip()

        data = json.loads(cleaned_response)

        tool_name = data.get("tool")
        payload = data.get("payload")

        # Handle string "null" just in case the LLM outputs it natively instead of actual null
        if tool_name == "null":
            tool_name = None
        if payload == "null":
            payload = None

        if tool_name is not None:
            print(
                f"🔀 [ROUTER] LLM Match found -> Tool: '{tool_name}', Payload: '{payload}'"
            )
        else:
            print("🔀 [ROUTER] LLM did not match any specific tool.")

        return tool_name, payload

    except json.JSONDecodeError as e:
        print(
            f"🔀 [ROUTER] Error parsing LLM JSON: {e} - Response was: {cleaned_response}"
        )
        return None, None
    except Exception as e:
        print(f"🔀 [ROUTER] Error during LLM routing: {e}")
        return None, None
