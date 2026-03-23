"""
tools/calculator.py

Calculator Tool
───────────────
A simple math expression evaluator wrapped in the standard `BaseTool` interface.
When the user asks to "calculate" something, the router extracts the expression
and passes it here as the payload.

Safety note:
  We limit eval() to only operate on numeric operations using a
  restricted scope (no builtins). This is sufficient for a workshop demo.
  In production, use a proper math parsing library like `simpleeval`.
"""

import re
from tools.base import BaseTool


class CalculatorTool(BaseTool):
    """
    Evaluates math expressions mathematically.
    """

    name = "calculator"
    description = "Evaluates simple math expressions step-by-step."

    def run(self, payload: str) -> str:
        """
        Evaluate a math expression string and return a human-readable result.

        Args:
            payload: A math expression like "10 + 25 * 3" or "(100 / 4) - 5"

        Returns:
            A formatted string with the result, or an error message.
        """
        # Sanitize: only allow digits, operators, spaces, dots, and parentheses
        cleaned = self._sanitize(payload)
        print(f"🛠️ [TOOL: calculator] Sanitized payload: '{cleaned}'")

        if not cleaned:
            print("🛠️ [TOOL: calculator] Error: Invalid math expression provided.")
            return (
                "⚠️ I couldn't find a valid math expression. "
                "Try something like: 'calculate 10 + 25 * 3'"
            )

        try:
            # eval with a restricted scope — no builtins, no variables
            print(f"🛠️ [TOOL: calculator] Evaluating: {cleaned}")
            result = eval(cleaned, {"__builtins__": {}}, {})
            print(f"🛠️ [TOOL: calculator] Result: {result}")
            return f"🧮 Result: {cleaned} = {result}"
        except ZeroDivisionError:
            print("🛠️ [TOOL: calculator] Error: Division by zero attempted.")
            return "⚠️ Division by zero is not allowed."
        except Exception as e:
            print(f"🛠️ [TOOL: calculator] Error evaluating expression: {e}")
            return (
                f"⚠️ Could not evaluate '{cleaned}'. "
                "Please use a simple math expression like: 10 + 5 * 2"
            )

    def _sanitize(self, expression: str) -> str:
        """
        Remove any characters that are not part of a valid math expression.
        """
        safe = re.sub(r"[^0-9+\-*/%.() ]", "", expression)
        return safe.strip()
