@tool(name="solution_finder", description="Finds solutions for identified printer issues", permission=ToolPermission.ADMIN)
def solution_finder(issue_id: str) -> dict:
    """Retrieves solutions for given issue."""
    # Simulate solution retrieval
    return {"solution": "Step-by-step solution for issue"}