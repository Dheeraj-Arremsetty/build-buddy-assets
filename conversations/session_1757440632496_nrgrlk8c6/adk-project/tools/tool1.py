from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="error_code_analyzer", description="Analyzes printer error codes", permission=ToolPermission.ADMIN)
def error_code_analyzer(error_code: str) -> str:
    """Diagnoses issues based on printer error codes."""
    error_mapping = {
        "016-799": "Network connectivity issue. Check network cables and settings.",
    }
    return error_mapping.get(error_code, "Unknown error code.")