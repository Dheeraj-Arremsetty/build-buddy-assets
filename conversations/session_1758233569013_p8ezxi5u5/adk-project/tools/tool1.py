import json
import random
from datetime import datetime, timedelta

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_company_financials", permission=ToolPermission.ADMIN)
def fetch_company_financials(company_name: str) -> dict:
    """
    Retrieves the latest quarterly financial statements (Income Statement, Balance Sheet) for a given company.

    Args:
        company_name (str): The name of the company to fetch financials for (e.g., "Innovate Inc.", "Global Solutions Ltd.").

    Returns:
        dict: A dictionary containing the company's financial data. Returns an error message if the company is not found.
    """
    filename_map = {
        "innovate inc.": "mock_data/innovate_inc_financials.json",
        "global solutions ltd.": "mock_data/global_solutions_ltd_financials.json"
    }
    
    filename = filename_map.get(company_name.lower())
    
    if not filename:
        return {"error": f"Financial data not found for {company_name}."}
        
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            data["metadata"] = {"source": "Internal Financial Database", "retrieved_at": datetime.utcnow().isoformat()}
            return data
    except FileNotFoundError:
        return {"error": f"Mock data file not found: {filename}"}
    except json.JSONDecodeError:
        return {"error": f"Error decoding JSON from {filename}"}

@tool(name="get_latest_stock_price", permission=ToolPermission.ADMIN)
def get_latest_stock_price(ticker: str) -> dict:
    """
    Gets the latest stock price for a given company ticker symbol.

    Args:
        ticker (str): The stock ticker symbol (e.g., "INVT", "GSL").

    Returns:
        dict: A dictionary containing the ticker, current price, and timestamp.
    """
    price_map = {
        "INVT": 175.45,
        "GSL": 250.10
    }
    base_price = price_map.get(ticker.upper(), 100.0)
    price = round(base_price + random.uniform(-2.5, 2.5), 2)
    
    return {
        "ticker": ticker.upper(),
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {"source": "Simulated Market Feed"}
    }

@tool(name="search_market_news", permission=ToolPermission.ADMIN)
def search_market_news(company_name: str) -> list[dict]:
    """
    Searches for recent market news articles related to a specific company.

    Args:
        company_name (str): The name of the company to search news for.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a news article with a headline, source, and summary.
    """
    today = datetime.now()
    news_map = {
        "innovate inc.": [
            {
                "headline": "Innovate Inc. Exceeds Q3 Earnings Expectations on Strong Cloud Growth",
                "source": "Financial Times",
                "date": (today - timedelta(days=2)).strftime('%Y-%m-%d'),
                "summary": "Innovate Inc. reported a 15% year-over-year revenue increase, driven by significant expansion in its enterprise cloud services division. The company has raised its full-year forecast."
            },
            {
                "headline": "New AI Product Launch from Innovate Inc. Receives Positive Analyst Reviews",
                "source": "Reuters",
                "date": (today - timedelta(days=5)).strftime('%Y-%m-%d'),
                "summary": "The newly unveiled 'Cognitive Suite' is expected to capture significant market share in the AI-as-a-Service space, with analysts praising its integration capabilities."
            }
        ],
        "global solutions ltd.": [
             {
                "headline": "Global Solutions Ltd. Announces Strategic Partnership to Expand into European Markets",
                "source": "Bloomberg",
                "date": (today - timedelta(days=3)).strftime('%Y-%m-%d'),
                "summary": "The partnership with EuroLogistics aims to streamline supply chain operations and is projected to boost international revenue by 20% over the next two years."
            }
        ]
    }
    
    return news_map.get(company_name.lower(), [])