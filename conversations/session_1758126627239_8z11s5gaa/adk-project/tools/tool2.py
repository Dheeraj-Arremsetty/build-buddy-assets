from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Dict, Any

@tool(name="create_proposal_draft", permission=ToolPermission.ADMIN)
def create_proposal_draft(customer_data: Dict[str, Any], service_info: str) -> str:
    """
    Creates a formatted draft proposal by combining customer details and service information into a template.

    This tool is used as the final step in proposal generation, assembling all gathered information
    into a coherent and professional document ready for sales review.

    Args:
        customer_data (dict): A dictionary containing customer details from Salesforce, such as 'name', 'contactPerson', and 'address'.
        service_info (str): A string containing the detailed service description, features, and terms retrieved from the Xerox Service Catalog knowledge base.

    Returns:
        str: The full text of the drafted proposal, formatted and ready for output.
    """
    try:
        # Template for the proposal document
        draft = f"""
# Proposal for: {customer_data.get('name', 'N/A')}

**Prepared for:** {customer_data.get('contactPerson', 'N/A')}
**Address:** {customer_data.get('address', 'N/A')}
**Industry:** {customer_data.get('industry', 'N/A')}

---

## 1. Proposed Services

This proposal outlines the following Xerox services tailored to meet your business needs:

{service_info}

---

## 2. Next Steps

We are confident that our solutions will deliver significant value to your organization. A Xerox sales representative will follow up within 24 hours to discuss this proposal in detail and answer any questions you may have.

Thank you for considering Xerox as your partner.
"""
        return draft.strip()
    except Exception as e:
        return f"Error generating proposal draft: {str(e)}"