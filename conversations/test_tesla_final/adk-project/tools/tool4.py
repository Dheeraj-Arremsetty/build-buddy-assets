@tool(name="wait_time_predictor", description="Predicts customer wait times at charging stations", permission=ToolPermission.ADMIN)
def wait_time_predictor(station_id: str, current_queue_length: int) -> str:
    """Estimates wait time for customers based on the current queue length.

    Args:
        station_id (str): The unique identifier of the charging station.
        current_queue_length (int): The current number of customers in queue.

    Returns:
        str: An estimated wait time message.
    """
    # Simulate wait time prediction
    wait_time = current_queue_length * 5  # assuming 5 minutes per customer
    return f"Estimated wait time at station {station_id} is {wait_time} minutes."