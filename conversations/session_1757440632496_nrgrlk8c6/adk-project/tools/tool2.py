from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="log_parser", description="Parses printer logs for troubleshooting", permission=ToolPermission.ADMIN)
def log_parser(log_data: str) -> dict:
    """Parses logs to extract error information."""
    parsed_data = {
        "timestamp": "2025-10-05T12:00:00",
        "error_code": "016-799",
        "details": "Network timeout detected."
    }
    return parsed_data