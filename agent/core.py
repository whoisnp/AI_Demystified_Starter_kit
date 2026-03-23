"""
agent/core.py

Main Agent Logic
────────────────
This is the central entry point for all user interactions.
It coordinates the router (tool selection) and the LLM (language model)
to produce an appropriate response.

Flow:
  1. Receive user input
  2. Ask the router if any tool should handle it
  3. If yes → return the tool's result
  4. If no  → send the input to the LLM and return its response
"""

from agent.executor import execute_tool
from agent.router import route
from agent.llm import get_llm_response


def run_agent(user_input: str) -> str:
    """
    Process a user message and return an appropriate response.

    This function is the single interface that the UI calls.
    It handles both tool-based and LLM-based responses transparently.

    Args:
        user_input: The raw message typed by the user.

    Returns:
        A response string — either from a tool or from the LLM.
    """
    if not user_input or not user_input.strip():
        return "Please enter a message to get started!"

    # Step 1: Try routing to a specific tool
    tool_name, payload = route(user_input)

    # Step 2: Execute tool if matched
    if tool_name is not None and payload is not None:
        return execute_tool(tool_name, payload)

    # Last Step: No tool matched — send to the LLM for a general response
    try:
        return get_llm_response(user_input)
    except Exception as e:
        # Return a friendly error instead of crashing the UI
        return f"⚠️ Something went wrong while contacting the LLM: {str(e)}"
