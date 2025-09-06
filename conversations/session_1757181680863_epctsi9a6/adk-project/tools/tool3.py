@tool(name="contact_info_provider", description="Provides contact information for Xerox customer support", permission=ToolPermission.ADMIN)
def provide_contact_info() -> str:
    """Returns contact information for further customer support.

    Returns:
        str: The contact information.
    """
    contact_info = "For further support, please contact Xerox Customer Support at 1-800-555-0199 or support@xerox.com."
    return contact_info