"""
agent/executor.py

Tool Executor
─────────────
Responsible for executing a tool given its name and a payload.
It looks up the requested tool from the registry in `tools/__init__.py`
and calls its standard `run()` method.
"""

from tools import AVAILABLE_TOOLS


def execute_tool(tool_name: str, payload: str) -> str:
    """
    Execute a registered tool by name.

    Args:
        tool_name: The unique string name of the tool (e.g., "calculator").
        payload: The input extracted by the router for the tool to process.

    Returns:
        The result string from the tool execution.
    """
    print(
        f"\n⚙️ [EXECUTOR] Preparing to run tool: '{tool_name}' with payload: '{payload}'"
    )
    tool = AVAILABLE_TOOLS.get(tool_name)

    if not tool:
        print(f"⚙️ [EXECUTOR] Error: Tool '{tool_name}' not found in registry.")
        return f"⚠️ Tool Error: Unrecognized tool '{tool_name}'."

    try:
        # Every tool guarantees a run(payload: str) -> str interface
        print(f"⚙️ [EXECUTOR] ⏳ Executing '{tool_name}.run()'...")
        result = tool.run(payload)
        print(f"⚙️ [EXECUTOR] ✅ Tool '{tool_name}' execution completed successfully.")
        return result
    except Exception as e:
        print(f"⚙️ [EXECUTOR] ❌ Execution failed for '{tool_name}'. Error: {e}")
        return f"⚠️ Tool Execution Error in '{tool_name}': {str(e)}"
