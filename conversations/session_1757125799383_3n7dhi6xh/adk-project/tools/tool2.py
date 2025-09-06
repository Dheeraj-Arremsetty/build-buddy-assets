@tool(name="pattern_analyzer", description="Analyzes workflow patterns.", permission=ToolPermission.ADMIN)
def pattern_analyzer(data: dict) -> dict:
    """Analyzes workflow data to detect patterns and inefficiencies."""
    patterns = {
        "bottleneck_detected": True,
        "stage": "approval",
        "recommendation": "increase resources"
    }
    return patterns