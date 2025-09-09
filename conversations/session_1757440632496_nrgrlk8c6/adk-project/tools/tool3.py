from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="nlp_query_processor", description="Processes natural language queries", permission=ToolPermission.ADMIN)
def nlp_query_processor(query: str) -> str:
    """Processes and responds to natural language queries."""
    return "Query processed successfully."