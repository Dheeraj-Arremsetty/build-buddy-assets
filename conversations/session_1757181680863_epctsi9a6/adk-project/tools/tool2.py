@tool(name="document_link_provider", description="Provides links to Xerox printer manuals and troubleshooting guides", permission=ToolPermission.ADMIN)
def provide_document_link(issue: str) -> str:
    """Returns links to documentation relevant to the issue.

    Args:
        issue (str): The issue the customer is facing.

    Returns:
        str: The URL to a relevant document.
    """
    doc_links = {
        "paper jam": "http://xerox.com/manuals/paper-jam-guide.pdf",
        "error code E01": "http://xerox.com/manuals/error-e01-guide.pdf"
    }
    return doc_links.get(issue, "No documentation available for this issue.")