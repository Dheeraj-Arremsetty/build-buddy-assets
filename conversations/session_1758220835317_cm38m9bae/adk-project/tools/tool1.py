import pandas as pd
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import List, Dict, Any

@tool(name="get_market_data", permission=ToolPermission.ADMIN)
def get_market_data(sector: str, country: str) -> List[Dict[str, Any]]:
    """
    Retrieves market data for companies in a specific sector and country. This tool provides access to S&P's proprietary market intelligence, including company names, tickers, and market capitalization.

    Args:
        sector (str): The industry sector to filter by (e.g., 'Technology', 'Finance').
        country (str): The country to filter by (e.g., 'Brazil', 'USA').

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a company with its market data. Returns an empty list if no companies match the criteria.
    """
    try:
        df = pd.read_csv('mock_market_data.csv')
        # Case-insensitive filtering
        filtered_df = df[(df['sector'].str.lower() == sector.lower()) & (df['country'].str.lower() == country.lower())]
        return filtered_df.to_dict('records')
    except FileNotFoundError:
        return [{"error": "Market data source not found."}]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {str(e)}"}]

@tool(name="get_company_esg_score", permission=ToolPermission.ADMIN)
def get_company_esg_score(company_id: str) -> Dict[str, Any]:
    """
    Retrieves the official S&P ESG score for a single company using its unique company ID. This is a certified tool that provides access to S&P's trusted ESG ratings.

    Args:
        company_id (str): The unique identifier for the company (e.g., 'C001').

    Returns:
        Dict[str, Any]: A dictionary containing the company ID and its ESG score, or an error message if the company is not found.
    """
    try:
        df = pd.read_csv('mock_esg_scores.csv')
        score_series = df[df['company_id'] == company_id]['sp_esg_score']
        if not score_series.empty:
            return {"company_id": company_id, "sp_esg_score": int(score_series.iloc[0])}
        else:
            return {"company_id": company_id, "error": "ESG score not found."}
    except FileNotFoundError:
        return {"error": "ESG data source not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}