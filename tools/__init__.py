"""
tools/__init__.py

Exports the available tools for the executor.
"""

from tools.calculator import CalculatorTool
from tools.search import SearchTool
from tools.summarizer import SummarizerTool

# A simple registry mapping tool names to their classes or instances
AVAILABLE_TOOLS = {
    CalculatorTool.name: CalculatorTool(),
    SummarizerTool.name: SummarizerTool(),
    SearchTool.name: SearchTool(),
}
