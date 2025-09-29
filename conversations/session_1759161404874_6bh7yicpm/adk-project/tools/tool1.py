# tools/data_harvester_tools.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_market_data", description="Fetches the latest market price and volume for a given stock ticker.", permission=ToolPermission.ADMIN)
def fetch_market_data(ticker: str) -> str:
    """
    Retrieves the latest market data, including price, volume, and day's high/low for a specific financial instrument.

    Args:
        ticker (str): The stock ticker symbol to fetch data for (e.g., 'IBM', 'GOOGL').

    Returns:
        str: A JSON string containing the market data for the requested ticker.
    """
    try:
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker symbol must be a non-empty string.")

        # Synthetic data generation
        base_price = random.uniform(100.0, 500.0)
        market_data = {
            "ticker": ticker.upper(),
            "price": round(base_price, 2),
            "volume": random.randint(500000, 10000000),
            "day_high": round(base_price * 1.02, 2),
            "day_low": round(base_price * 0.98, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        return json.dumps(market_data)
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch market data: {str(e)}"})

@tool(name="get_client_portfolio", description="Retrieves the current investment portfolio holdings for a given client ID.", permission=ToolPermission.ADMIN)
def get_client_portfolio(client_id: str) -> str:
    """
    Fetches the complete list of assets currently held in a client's portfolio, including quantities and acquisition dates.

    Args:
        client_id (str): The unique identifier for the client.

    Returns:
        str: A JSON string containing a list of the client's portfolio holdings.
    """
    try:
        if not client_id:
            raise ValueError("Client ID cannot be empty.")
            
        # Synthetic data generation
        holdings = [
            {"ticker": "IBM", "quantity": 200, "acquisition_date": (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')},
            {"ticker": "MSFT", "quantity": 150, "acquisition_date": (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')},
            {"ticker": "TSLA", "quantity": 50, "acquisition_date": (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')}
        ]
        portfolio = {
            "client_id": client_id,
            "retrieved_at": datetime.utcnow().isoformat(),
            "holdings": holdings
        }
        return json.dumps(portfolio)
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve portfolio for client {client_id}: {str(e)}"})

@tool(name="get_instrument_details", description="Gets detailed information about a financial instrument, such as its asset class and risk rating.", permission=ToolPermission.ADMIN)
def get_instrument_details(ticker: str) -> str:
    """
    Provides detailed information about a financial instrument, including its name, asset class, sector, and internal risk rating.

    Args:
        ticker (str): The stock ticker symbol for the instrument.

    Returns:
        str: A JSON string containing detailed information about the instrument.
    """
    try:
        instrument_map = {
            "IBM": {"name": "International Business Machines Corp", "asset_class": "Equity", "sector": "Technology", "risk_rating": "Medium"},
            "MSFT": {"name": "Microsoft Corporation", "asset_class": "Equity", "sector": "Technology", "risk_rating": "Low"},
            "TSLA": {"name": "Tesla, Inc.", "asset_class": "Equity", "sector": "Consumer Discretionary", "risk_rating": "High"},
            "GOOGL": {"name": "Alphabet Inc.", "asset_class": "Equity", "sector": "Communication Services", "risk_rating": "Low"}
        }
        details = instrument_map.get(ticker.upper(), {"name": "Unknown Instrument", "asset_class": "Unknown", "sector": "Unknown", "risk_rating": "Unrated"})
        details["ticker"] = ticker.upper()
        return json.dumps(details)
    except Exception as e:
        return json.dumps({"error": f"Failed to get instrument details: {str(e)}"})