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


def run_agent(user_input: str, strict_rag: bool = False) -> str:
    """
    Process a user message and return an appropriate response.

    This function is the single interface that the UI calls.
    It handles both tool-based and LLM-based responses transparently.

    Args:
        user_input: The raw message typed by the user.
        strict_rag: If True, enforce strict handling for RAG search results.

    Returns:
        A response string — either from a tool or from the LLM.
    """
    if not user_input or not user_input.strip():
        return "Please enter a message to get started!"

    # Step 1: Try routing to a specific tool
    if strict_rag:
        tool_name, payload = "rag_search", user_input
    else:
        tool_name, payload = route(user_input)

    # Step 2: Execute tool if matched
    if tool_name is not None and payload is not None:
        # ------------logic to execute the trip_planner start-----------
        if tool_name == "trip_planner":
            print("🚀 [CORE] Executing direct Trip Planner workflow...")
            import json
            from tools.weather import get_weather
            from tools.budget import estimate_budget
            from tools.itinerary import generate_itinerary

            # Parse query
            print(
                "🚀 [CORE] Parsing user query for Trip details (days, budget, destination) using LLM..."
            )
            query = payload

            prompt = f"""Extract the trip details from the following query.
Return *only* a valid JSON object with the exact keys:
- "days": integer (number of days, default 3 if not mentioned)
- "budget": string (budget with currency, or null if not mentioned)
- "destination": string (destination city, default "Ooty" if not mentioned)

Do not include any markdown formatting or backticks.
Query: {query}"""

            days = 3
            budget = None
            destination = "Ooty"

            # Expected LLM Response format:
            # {
            #     "days": 5,
            #     "budget": "₹50,000",
            #     "destination": "Ooty"
            # }
            try:
                response = get_llm_response(prompt).strip()
                # Clean up potential markdown blocks
                if response.startswith("```json"):
                    response = response[7:]
                elif response.startswith("```"):
                    response = response[3:]
                if response.endswith("```"):
                    response = response[:-3]

                parsed = json.loads(response.strip())

                if parsed.get("days") is not None:
                    try:
                        days = int(parsed["days"])
                    except ValueError:
                        pass

                if parsed.get("budget") is not None:
                    budget = str(parsed["budget"])

                if parsed.get("destination") is not None:
                    destination = str(parsed["destination"]).title()

            except Exception as e:
                print(f"⚠️ [CORE] Error parsing trip details from LLM: {e}")

            weather = get_weather(destination, query)
            budget_result = estimate_budget(days, budget)
            itinerary = generate_itinerary(destination, days)

            print(
                "🚀 [CORE] Trip Planner workflow complete. Returning combined results."
            )
            return f"Weather:\n{weather}\n\nBudget:\n{budget_result}\n\nItinerary:\n{itinerary}"
        # ------------logic to execute the trip_planner Ends------------
        tool_output = execute_tool(tool_name, payload)

        # ------------Special handling for RAG search results to demonstrate strict vs loose RAG prompting START----------------
        print("🚀 [CORE] Step 2: Executing matched single tool...")
        # Special strict handling for RAG search
        if tool_name == "rag_search":
            if strict_rag:
                if tool_output == "NO_CONTEXT":
                    return "I don't have enough information to answer that."

                # Strict prompt
                prompt = (
                    "You are a strict RAG assistant. Answer the user's query ONLY using the provided Context.\n"
                    "If the Context answers the Query, provide the answer.\n"
                    "If the Context does NOT answer the Query, you MUST reply EXACTLY with this sentence and nothing else: "
                    "'I don't have enough information to answer that. Please ask about the AI Starter Kit, RAG, Pinecone, or the instructor.'\n"
                    "Do not use any external knowledge.\n\n"
                    f"Context:\n{tool_output}\n\n"
                    f"Query:\n{user_input}"
                )
                try:
                    return get_llm_response(prompt)
                except Exception as e:
                    return f"⚠️ Something went wrong while contacting the LLM: {str(e)}"
            else:
                # Normal (loose) prompt
                prompt = (
                    "You retrieved some context from our database. Use it if relevant.\n"
                    "If it does not contain the answer, you can use your general knowledge to answer the user.\n\n"
                    f"Context:\n{tool_output}\n\n"
                    f"Query:\n{user_input}"
                )
                try:
                    return get_llm_response(prompt)
                except Exception as e:
                    return f"⚠️ Something went wrong while contacting the LLM: {str(e)}"
                
# ------------Special handling for RAG search results to demonstrate strict vs loose RAG prompting END----------------

        return tool_output
    # Last Step: No tool matched — send to the LLM for a general response
    if strict_rag:
        return "I am in Strict RAG Mode and can only answer questions based on the provided documents. Please ask a factual question."
    try:
        return get_llm_response(user_input)
    except Exception as e:
        # Return a friendly error instead of crashing the UI
        return f"⚠️ Something went wrong while contacting the LLM: {str(e)}"
