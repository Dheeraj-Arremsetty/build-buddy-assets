from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="faq_resolver", description="Resolves frequently asked questions", permission=ToolPermission.ADMIN)
def faq_resolver(question: str) -> str:
    """Provides answers to frequently asked questions."""
    faq_database = {
        "How to fix error 016-799?": "Check network cables and settings.",
    }
    return faq_database.get(question, "No answer found.")