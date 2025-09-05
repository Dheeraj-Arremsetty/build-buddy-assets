# doc_search_tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="doc_search_tool", description="Searches for developer documentation based on query")
def doc_search_tool(query: str) -> dict:
    """Searches for documentation matching the given query.

    Args:
        query (str): The search query for documentation.

    Returns:
        dict: A dictionary containing document titles and URLs.
    """
    # Mock implementation with synthetic data
    documents = {
        "query": query,
        "results": [
            {"title": "API Documentation", "url": "https://developer.apple.com/api-docs"},
            {"title": "User Guide", "url": "https://developer.apple.com/user-guide"}
        ]
    }
    return documents