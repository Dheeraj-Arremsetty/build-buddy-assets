from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="diagnostic_questionnaire", description="Gathers detailed information about printer issues", permission=ToolPermission.ADMIN)
def diagnostic_questionnaire(input: str) -> dict:
    """Collects user responses to diagnose printer issues."""
    # Simulate data collection
    return {"questionnaire": "Detailed diagnostic data"}