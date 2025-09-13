import json
    import os
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    def _load_company_filing(company_name: str) -> dict:
        """Helper function to load mock financial data from a JSON file."""
        # Sanitize company name to create a filename
        filename = company_name.lower().replace(" ", "_").replace(".", "").replace(",", "") + ".json"
        # Construct a robust path relative to the current file's location
        filepath = os.path.join(os.path.dirname(__file__), '..', 'mock_data', 'filings', filename)

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            return {"error": f"Financial data for '{company_name}' not found."}
        except Exception as e:
            return {"error": f"An error occurred while reading the data file: {str(e)}"}

    @tool(name="get_financial_statements", permission=ToolPermission.ADMIN)
    def get_financial_statements(company_name: str) -> dict:
        """
        Retrieves key financial statement data for a specified company from internal filings.

        Args:
            company_name (str): The official name of the company (e.g., "Innovatech Solutions").

        Returns:
            dict: A dictionary containing the company's latest financial data, including revenue, net income, assets, liabilities, and EBITDA. Returns an error message if the company is not found.
        """
        return _load_company_filing(company_name)

    @tool(name="calculate_key_ratios", permission=ToolPermission.ADMIN)
    def calculate_key_ratios(company_name: str) -> dict:
        """
        Calculates standard financial ratios like Debt-to-EBITDA and Debt-to-Equity for a given company.

        Args:
            company_name (str): The official name of the company to analyze.

        Returns:
            dict: A dictionary containing the calculated ratios. Returns an error message if data is unavailable or a calculation fails.
        """
        financial_data_result = _load_company_filing(company_name)
        if "error" in financial_data_result:
            return financial_data_result

        financials = financial_data_result.get("financials", {})
        debt = financials.get("total_debt")
        ebitda = financials.get("ebitda")
        equity = financials.get("total_equity")

        if not all([isinstance(debt, (int, float)), isinstance(ebitda, (int, float)), isinstance(equity, (int, float))]):
            return {"error": "Incomplete or invalid financial data to calculate ratios."}

        try:
            debt_to_ebitda = round(debt / ebitda, 2) if ebitda != 0 else "N/A (EBITDA is zero)"
            debt_to_equity = round(debt / equity, 2) if equity != 0 else "N/A (Equity is zero)"
            
            return {
                "company_name": company_name,
                "ratios": {
                    "debt_to_ebitda": debt_to_ebitda,
                    "debt_to_equity": debt_to_equity
                }
            }
        except Exception as e:
            return {"error": f"An unexpected error occurred during calculation: {str(e)}"}
    ```

3.  **Create Market Intelligence Tools**

    **Business Value**: This tool simulates fetching real-time market data, providing a snapshot of how the market currently values a company. This is crucial for understanding investor sentiment and comparing a company's performance against its peers, adding an essential external perspective to the credit analysis.

    *File: `tools/market_tools.py`*
    ```python
    import random
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    @tool(name="get_market_performance", permission=ToolPermission.ADMIN)
    def get_market_performance(company_name: str) -> dict:
        """
        Retrieves simulated public market performance data for a given company.

        Args:
            company_name (str): The official name of the company (e.g., "Innovatech Solutions").

        Returns:
            dict: A dictionary containing the company's ticker, current stock price, market capitalization, and P/E ratio.
        """
        mock_market_data = {
            "Innovatech Solutions": {
                "ticker": "INVT",
                "stock_price": round(random.uniform(150.0, 180.0), 2),
                "market_cap_billions": round(random.uniform(90.0, 110.0), 2),
                "pe_ratio": round(random.uniform(25.0, 30.0), 1)
            },
            "Global Logistics Corp": {
                "ticker": "GLC",
                "stock_price": round(random.uniform(85.0, 100.0), 2),
                "market_cap_billions": round(random.uniform(40.0, 50.0), 2),
                "pe_ratio": round(random.uniform(15.0, 20.0), 1)
            }
        }

        if company_name in mock_market_data:
            return mock_market_data[company_name]
        else:
            return {"error": f"Market data for '{company_name}' not found."}
    ```

### Step 4.3: Define the Knowledge Base

This YAML file configures a RAG knowledge base using the built-in Milvus vector store. It will ingest our synthetic news articles, allowing the `Market_Intelligence_Agent` to perform semantic searches and answer questions based on their content, demonstrating a powerful capability for analyzing unstructured text.

*File: `knowledge_bases/market_news_kb.yaml`*