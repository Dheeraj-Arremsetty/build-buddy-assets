from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="ticket_creator", description="Creates support tickets", permission=ToolPermission.ADMIN)
def ticket_creator(issue_description: str) -> dict:
    """Creates a support ticket for unresolved issues."""
    ticket = {
        "ticket_id": "TCK123456",
        "status": "Open",
        "description": issue_description
    }
    return ticket