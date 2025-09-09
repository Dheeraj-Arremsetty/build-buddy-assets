from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="context_preserver", description="Preserves issue context for escalation", permission=ToolPermission.ADMIN)
def context_preserver(issue_id: str) -> dict:
    """Preserves context details for issue escalation."""
    context_data = {
        "issue_id": issue_id,
        "context": "Detailed context for the issue."
    }
    return context_data