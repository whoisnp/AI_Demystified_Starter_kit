"""
tools/summarizer.py

Summarizer Tool
───────────────
Uses the LLM backend to summarize a given text payload.
This demonstrates how a tool can internally rely on the main AI core.
"""

from tools.base import BaseTool
from agent.llm import get_llm_response


class SummarizerTool(BaseTool):
    """
    Summarizes long pieces of text using the LLM.
    """
    name = "summarizer"
    description = "Summarizes long text into a concise overview."

    def run(self, payload: str) -> str:
        """
        Ask the LLM to summarize the payload.

        Args:
            payload: The text to be summarized.

        Returns:
            The summary string from the LLM.
        """
        print(f"🛠️ [TOOL: summarizer] Starting summarization for text of length {len(payload)}")
        if not payload.strip():
            print("🛠️ [TOOL: summarizer] Error: Empty payload received.")
            return "⚠️ Please provide some text to summarize."

        prompt = (
            "Please provide a concise but comprehensive summary "
            f"of the following text:\n\n{payload}"
        )

        try:
            print("🛠️ [TOOL: summarizer] Contacting LLM for summary...")
            summary = get_llm_response(prompt)
            print("🛠️ [TOOL: summarizer] Summary generation complete.")
            return f"📝 **Summary:**\n\n{summary}"
        except Exception as e:
            print(f"🛠️ [TOOL: summarizer] Error during generation: {e}")
            return f"⚠️ Could not summarize the text: {str(e)}"
