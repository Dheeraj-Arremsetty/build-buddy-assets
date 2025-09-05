from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="station_performance_tool", description="Collects real-time performance metrics of charging stations", permission=ToolPermission.ADMIN)
def station_performance_tool(station_id: str) -> dict:
    """Gathers real-time performance data for a specified charging station.

    Args:
        station_id (str): The unique identifier of the charging station.

    Returns:
        dict: A dictionary containing performance metrics such as uptime, throughput, and error rates.
    """
    # Simulate data collection
    performance_data = {
        "station_id": station_id,
        "uptime": "99.9%",
        "throughput": "80 kWh",
        "error_rate": "0.01%"
    }
    return performance_data