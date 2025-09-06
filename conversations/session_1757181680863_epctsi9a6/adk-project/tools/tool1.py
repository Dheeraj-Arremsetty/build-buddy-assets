from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
import json

@tool(name="faq_responder", description="Responds to common Xerox printer FAQs", permission=ToolPermission.ADMIN)
def respond_to_faq(question: str) -> str:
    """Provides answers to common Xerox printer-related questions.

    Args:
        question (str): The customer's question.

    Returns:
        str: The response to the FAQ.
    """
    faq_db = {
        "How do I fix a paper jam?": "To fix a paper jam, open the printer cover and gently remove the jammed paper.",
        "What does error code E01 mean?": "Error code E01 indicates a paper feed issue. Please check the paper tray."
    }
    return faq_db.get(question, "I'm sorry, I don't have an answer to that question.")