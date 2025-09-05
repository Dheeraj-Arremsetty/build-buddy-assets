@tool(name="pricing_recommender", description="Recommends dynamic pricing based on demand forecasting", permission=ToolPermission.ADMIN)
def pricing_recommender(demand_data: dict) -> dict:
    """Recommends pricing adjustments based on demand data.

    Args:
        demand_data (dict): A dictionary containing demand metrics.

    Returns:
        dict: A dictionary containing pricing recommendations.
    """
    # Simulate pricing recommendation
    pricing_recommendation = {
        "recommended_price": "0.30 per kWh",
        "reason": "High demand observed"
    }
    return pricing_recommendation