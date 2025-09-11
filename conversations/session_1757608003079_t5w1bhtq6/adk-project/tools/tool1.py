import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import List, Dict

@tool(name="fetch_market_data", description="Fetches the latest market data for a given list of stock tickers.")
def fetch_market_data(tickers: List[str]) -> str:
    """
    Simulates fetching the latest market data including price, volume, and day's high/low for a specified list of stock tickers.

    Args:
        tickers (List[str]): A list of stock market tickers to fetch data for (e.g., ['IBM', 'GOOG', 'MSFT']).

    Returns:
        str: A JSON string representing a list of dictionaries, where each dictionary contains market data for a ticker.
    """
    market_data = []
    for ticker in tickers:
        base_price = random.uniform(100.0, 500.0)
        market_data.append({
            "ticker": ticker,
            "price": round(base_price + random.uniform(-5.0, 5.0), 2),
            "volume": random.randint(1_000_000, 20_000_000),
            "day_high": round(base_price + random.uniform(2.0, 8.0), 2),
            "day_low": round(base_price - random.uniform(2.0, 8.0), 2),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat(),
            "metadata": {
                "source": "Simulated Market Feed",
                "quality_score": round(random.uniform(0.95, 0.99), 2)
            }
        })
    return json.dumps(market_data, indent=2)

@tool(name="get_economic_indicators", description="Retrieves key economic indicators relevant to market analysis.")
def get_economic_indicators() -> str:
    """
    Simulates retrieving major economic indicators like CPI, interest rates, and unemployment rates.

    Returns:
        str: A JSON string containing a dictionary of key economic indicators.
    """
    indicators = {
        "consumer_price_index": {
            "value": round(random.uniform(2.5, 4.0), 2),
            "unit": "%",
            "change_mom": round(random.uniform(-0.2, 0.2), 2),
            "last_updated": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        },
        "federal_interest_rate": {
            "value": round(random.uniform(4.5, 5.5), 2),
            "unit": "%",
            "change_bps": random.choice([0, 25, -25]),
            "last_updated": (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        },
        "unemployment_rate": {
            "value": round(random.uniform(3.5, 4.5), 2),
            "unit": "%",
            "last_updated": (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')
        }
    }
    return json.dumps(indicators, indent=2)