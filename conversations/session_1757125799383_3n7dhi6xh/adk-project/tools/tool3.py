@tool(name="alert_generator", description="Generates workflow alerts.", permission=ToolPermission.ADMIN)
def alert_generator(issue: str, severity: str) -> str:
    """Generates alerts based on detected workflow issues."""
    alert = f"ALERT: {issue} detected with severity {severity}."
    return alert