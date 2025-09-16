import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_historical_stock_data", description="Fetches historical stock price and volume data for a given ticker symbol over a specified number of days.", permission=ToolPermission.ADMIN)
def get_historical_stock_data(ticker_symbol: str, days: int = 90) -> str:
    """
    Retrieves historical daily price and volume data for a financial instrument.

    This tool simulates fetching data from a market data provider, which is essential for
    calculating volatility, trend analysis, and other quantitative risk metrics.

    Args:
        ticker_symbol (str): The stock ticker symbol to fetch data for (e.g., 'TETF', 'FINCORP').
        days (int): The number of past days of historical data to retrieve. Defaults to 90.

    Returns:
        str: A JSON string representing a list of daily data points. Each point includes
             date, open, high, low, close, and volume. Returns an error message if the
             ticker is not found.
    """
    if not ticker_symbol:
        return json.dumps({"error": "Ticker symbol cannot be empty."})

    historical_data = []
    current_date = datetime.now()
    price = round(random.uniform(100, 500), 2)

    for i in range(days):
        date = (current_date - timedelta(days=i)).strftime('%Y-%m-%d')
        price_change = price * random.uniform(-0.03, 0.03)
        open_price = round(price, 2)
        close_price = round(price + price_change, 2)
        high_price = max(open_price, close_price) + round(random.uniform(0, price * 0.01), 2)
        low_price = min(open_price, close_price) - round(random.uniform(0, price * 0.01), 2)
        volume = random.randint(1_000_000, 10_000_000)
        
        historical_data.append({
            "date": date,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        })
        price = close_price
    
    return json.dumps(historical_data, indent=2)

@tool(name="get_volatility_index", description="Fetches the current value and recent trend of a major market volatility index (e.g., VIX).", permission=ToolPermission.ADMIN)
def get_volatility_index(index_name: str = "VIX") -> str:
    """
    Provides the current level of a specified market volatility index.

    High volatility indicates higher market risk and uncertainty. This tool gives a quick
    snapshot of the overall market sentiment, which is a key contextual factor for assessing
    a specific product's risk.

    Args:
        index_name (str): The name of the volatility index to fetch. Defaults to 'VIX'.

    Returns:
        str: A JSON string with the index name, current value, and a 30-day trend analysis.
    """
    current_value = round(random.uniform(12.0, 45.0), 2)
    trend_value = round(random.uniform(-5.0, 5.0), 2)
    trend_direction = "up" if trend_value > 0 else "down"

    result = {
        "index_name": index_name,
        "current_value": current_value,
        "30_day_change": trend_value,
        "trend": trend_direction,
        "assessment": "High market uncertainty" if current_value > 25 else "Moderate market stability",
        "timestamp": datetime.now().isoformat()
    }
    return json.dumps(result, indent=2)