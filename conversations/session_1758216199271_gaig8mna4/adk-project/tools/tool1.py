# tools/market_tools.py
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def fetch_news_articles(company_name: str, event: str) -> list[dict]:
    """
    Fetches a list of recent news articles for a given company and market event. 
    This tool is essential for gathering unstructured, real-time public sentiment and factual reporting surrounding a key business event. It allows the supervisor agent to incorporate qualitative context into its final summary, providing a narrative to complement hard data.

    Args:
        company_name (str): The name of the company (e.g., 'Nvidia', 'Apple').
        event (str): The specific market event (e.g., 'Q4 earnings report', 'WWDC keynote').

    Returns:
        list[dict]: A list of articles, each with a title, source, summary, and publication date, or an error object if retrieval fails.
    """
    try:
        print(f"Fetching news for {company_name} regarding {event}...")
        # Mock data implementation returns a hardcoded list of realistic articles
        base_date = datetime.now()
        articles = [
            {
                "title": f"{company_name} Shatters Expectations with Strong {event} Results",
                "source": "Reuters",
                "published_date": (base_date - timedelta(days=1)).isoformat(),
                "summary": f"Analysts are overwhelmingly positive after {company_name} reported revenue figures that significantly beat Wall Street forecasts, driven by high demand in its core sectors."
            },
            {
                "title": f"Is {company_name}'s Growth Sustainable After Stellar {event}?",
                "source": "Bloomberg",
                "published_date": (base_date - timedelta(hours=12)).isoformat(),
                "summary": f"While the latest {event} was impressive, some experts raise questions about future growth, citing increased market competition and potential supply chain constraints."
            },
            {
                "title": f"Market Reacts: {company_name} Stock Surges Post-{event} Announcement",
                "source": "The Wall Street Journal",
                "published_date": (base_date - timedelta(hours=8)).isoformat(),
                "summary": f"Shares of {company_name} jumped over 8% in after-hours trading following the company's highly anticipated {event}, signaling strong investor confidence."
            }
        ]
        return articles
    except Exception as e:
        print(f"An error occurred in fetch_news_articles: {e}")
        return [{"error": "Failed to fetch news articles.", "details": str(e)}]


@tool(permission=ToolPermission.ADMIN)
def get_market_data(ticker: str) -> dict:
    """
    Retrieves key quantitative market data points for a specific stock ticker.
    This tool provides the essential structured financial data needed to objectively assess market reaction. By supplying concrete numbers like price changes and trading volume, it complements the qualitative news data, enabling a holistic and data-driven analysis.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'NVDA', 'AAPL').

    Returns:
        dict: A dictionary with key stock data points like opening_price, closing_price, day_high, day_low, and trading_volume, or an error object if retrieval fails.
    """
    try:
        print(f"Getting market data for ticker: {ticker}...")
        # Mock data implementation returns a hardcoded dictionary of realistic financial data
        base_price = random.uniform(150.0, 800.0)
        closing_price = base_price * random.uniform(1.02, 1.09) # Simulate a positive reaction
        market_data = {
            "ticker": ticker,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "opening_price": round(base_price, 2),
            "closing_price": round(closing_price, 2),
            "day_high": round(closing_price * 1.03, 2),
            "day_low": round(base_price * 0.98, 2),
            "trading_volume": random.randint(50_000_000, 150_000_000)
        }
        return market_data
    except Exception as e:
        print(f"An error occurred in get_market_data: {e}")
        return {"error": "Failed to retrieve market data.", "details": str(e)}