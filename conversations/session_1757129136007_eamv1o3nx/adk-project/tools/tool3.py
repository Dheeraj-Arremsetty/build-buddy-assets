@tool(name="chart_generator", description="Generates data visualizations", permission=ToolPermission.ADMIN)
def chart_generator(data: list) -> str:
    """Generates charts from data for visualization.
    
    Args:
        data (list): Data to be visualized.

    Returns:
        str: URL or path to the generated chart.
    """
    # Simulated chart generation
    return "http://example.com/chart.png"