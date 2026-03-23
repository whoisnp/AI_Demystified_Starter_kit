"""
tools/base.py

Standard Tool Interface
───────────────────────
Defines the base structure that all tools must follow.
This ensures the agent can interact with any tool uniformly,
without needing hardcoded logic for each individual tool.
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Abstract base class for all tools in the AI Starter Kit.

    Every tool must provide:
      - name: A unique string identifier for the tool (used by the router)
      - description: A brief explanation of what the tool does
      - run(payload: str) -> str: The function that executes the tool's logic
    """

    name: str = "unnamed_tool"
    description: str = "No description provided."

    @abstractmethod
    def run(self, payload: str) -> str:
        """
        Execute the tool's core logic using the specific payload.

        Args:
            payload: The extracted text that the tool should operate on.
                     (e.g., the math expression for a calculator, or the
                      text body for a summarizer).

        Returns:
            A string containing the tool's output or result.
        """
        pass
