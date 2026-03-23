"""
tools/__init__.py

Exports the available tools for the executor.
"""

from tools.calculator import CalculatorTool

# A simple registry mapping tool names to their classes or instances
AVAILABLE_TOOLS = {
    CalculatorTool.name: CalculatorTool(),
}
