# faq_responder.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="faq_responder", description="Handles FAQ queries", permission=ToolPermission.ADMIN)
def faq_responder(query: str) -> str:
    """Responds to FAQ queries using predefined answers.

    Args:
        query (str): The FAQ query from the customer.

    Returns:
        str: The response to the FAQ query.
    """
    faq_data = {
        "What is your return policy?": "Our return policy allows returns within 30 days of purchase.",
        "How can I track my order?": "You can track your order using the tracking number sent to your email."
    }
    return faq_data.get(query, "I'm sorry, I don't have an answer for that.")