"""
agent/router.py

Tool Router
───────────
"""

import json
from typing import Tuple, Optional
from agent.llm import get_llm_response


def route(user_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Check if the user's message matches a known tool trigger using an LLM.

    Returns:
        (tool_name, payload) or (None, None)
    """

    prompt = f"""You are an intelligent routing assistant. Your job is to classify the user's input and decide if a specific tool should handle it.

Available Tools:
1. "calculator": Use this for mathematical calculations.

Output your reply as a strictly valid JSON object with the following structure:
{{
  "tool": "tool_name_or_null",
  "payload": "extracted_payload_or_full_input_or_null"
}}

Rules:
- If a tool is needed, "tool" should be exactly one of: "calculator".
- If no tool is appropriate, set "tool" to null and "payload" to null.
- For "calculator", the "payload" should be the specific part of the user input that needs calculating.
- Return ONLY the raw JSON object.

User Input: {user_input}"""

    try:
        response = get_llm_response(prompt)

        # Clean markdown formatting if present
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

        # Handle "null" string cases
        if tool_name == "null":
            tool_name = None
        if payload == "null":
            payload = None

        if tool_name is not None:
            print(f"🔀 [ROUTER] Tool: {tool_name}, Payload: {payload}")
        else:
            print("🔀 [ROUTER] No tool matched.")

        return tool_name, payload

    except json.JSONDecodeError as e:
        print(f"🔀 [ROUTER] JSON Error: {e} | Response: {cleaned_response}")
        return None, None

    except Exception as e:
        print(f"🔀 [ROUTER] General Error: {e}")
        return None, None