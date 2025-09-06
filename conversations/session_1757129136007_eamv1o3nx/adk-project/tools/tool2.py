@tool(name="multi_source_query_tool", description="Fetches data from multiple sources", permission=ToolPermission.ADMIN)
def multi_source_query_tool(query_params: dict) -> dict:
    """Fetches data from multiple databases based on query parameters.
    
    Args:
        query_params (dict): Parameters for data retrieval.

    Returns:
        dict: Retrieved data from databases.
    """
    # Simulated data retrieval
    return {"data": [{"id": 1, "value": "Sample Data"}]}