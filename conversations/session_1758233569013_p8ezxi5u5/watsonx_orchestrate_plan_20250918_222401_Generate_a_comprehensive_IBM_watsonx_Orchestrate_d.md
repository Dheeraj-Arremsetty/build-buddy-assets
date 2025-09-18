# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 22:24:01
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Financial Analyst Co-Pilot

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the **AI-Powered Financial Analyst Co-Pilot**, a sophisticated multi-agent system designed specifically for your organization's needs. This solution directly addresses your goal of creating an "Automated Financial Analyst Assistant" by leveraging a supervisor agent to orchestrate specialized collaborator agents for data retrieval, quantitative analysis, and qualitative insight generation. This system acts as a force multiplier for your analyst teams, automating laborious data aggregation and preliminary analysis tasks.

The final demo will showcase a tangible workflow that promises a **30-50% reduction in time spent on data collection and initial analysis**. By offloading these repetitive tasks to the AI Co-Pilot, your expert analysts can dedicate their time to high-value strategic interpretation, client advisory, and identifying nuanced market opportunities. This not only enhances the accuracy and consistency of your reports by minimizing manual data handling but also enables a scalable analysis framework, allowing you to cover a broader portfolio of companies with greater depth and speed.

## Prerequisites
Before beginning, ensure your development environment is correctly configured to support the IBM watsonx Orchestrate Agent Development Kit (ADK).

1.  **Python Environment**: A working Python 3.10+ installation is required. This ensures compatibility with the ADK and its dependencies.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. This is the core library for building, deploying, and managing agents and tools. If not already installed, run the following command in your terminal:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured and set as your current context. The ADK CLI needs to connect to your tenant to import assets. If you haven't configured it, run:
    ```bash
    orchestrate env init
    ```
    Follow the prompts to connect to your tenant using your credentials.
4.  **Project Structure**: To maintain clarity, organization, and ensure all file paths in the configurations are correct, create the following directory structure. This standardized layout is crucial for a successful deployment.
    ```
    financial_copilot_demo/
    ├── agents/
    │   ├── 01_industry_insight_agent.yaml
    │   ├── 02_market_data_agent.yaml
    │   ├── 03_quantitative_analysis_agent.yaml
    │   └── 04_financial_analyst_copilot.yaml
    ├── tools/
    │   ├── market_data_tools.py
    │   ├── quantitative_analysis_tools.py
    │   └── reporting_tools.py
    ├── knowledge_base/
    │   ├── industry_reports_kb.yaml
    │   └── documents/
    │       ├── Tech_Sector_Outlook_2024.pdf
    │       └── Financial_Ratio_Best_Practices.txt
    ├── mock_data/
    │   ├── innovate_inc_financials.json
    │   └── global_solutions_ltd_financials.json
    └── requirements.txt
    ```

## Step 1: Prepare Mock Data and Knowledge Base
The foundation of a powerful AI system is high-quality data. For this demo, we will create realistic synthetic data sources to simulate the complex information landscape a financial analyst navigates daily.

### 1.1 Create Knowledge Base Documents
These documents will populate our vector database, providing the `Industry_Insight_Agent` with the domain knowledge required to answer qualitative questions using Retrieval-Augmented Generation (RAG).

**File: `knowledge_base/documents/Financial_Ratio_Best_Practices.txt`**
```text
Best Practices in Financial Ratio Analysis - For Internal Use

This document outlines key financial ratios and industry benchmarks, particularly for the technology sector.

The Debt-to-Equity (D/E) ratio is a primary metric used to assess a company's financial leverage. It is calculated by dividing a company's total liabilities by its shareholder equity. A high D/E ratio generally means that a company has been aggressive in financing its growth with debt, which can lead to increased volatility and risk. For the technology sector, a D/E ratio below 1.5 is often considered healthy due to the fast-paced and often volatile nature of the industry. A ratio persistently above 2.0 may signal excessive risk and warrants closer investigation.

The Price-to-Earnings (P/E) ratio is another critical valuation metric, calculated as market value per share divided by earnings per share. A high P/E ratio could mean that a stock's price is high relative to earnings and possibly overvalued. Conversely, a low P/E ratio might indicate that the current stock price is low relative to earnings. The average P/E for the S&P 500 has historically hovered around 15-20. Due to high growth expectations and intangible assets, established tech companies often trade at higher P/E ratios, sometimes in the 25-40 range.
```
*(For the demo, create a dummy PDF named `Tech_Sector_Outlook_2024.pdf`. The content can be placeholder text, as the system will ingest and index it regardless to demonstrate multi-format document handling.)*

### 1.2 Create Mock Financial Data
These structured JSON files simulate the responses from internal financial databases or external APIs like Bloomberg or FactSet.

**File: `mock_data/innovate_inc_financials.json`**
```json
{
  "company_name": "Innovate Inc.",
  "ticker": "INVT",
  "report_date": "2024-09-30",
  "income_statement": {
    "revenue": 500000000,
    "cost_of_goods_sold": 200000000,
    "gross_profit": 300000000,
    "operating_expenses": 150000000,
    "net_income": 80000000
  },
  "balance_sheet": {
    "total_assets": 1200000000,
    "total_liabilities": 700000000,
    "shareholder_equity": 500000000
  }
}
```

**File: `mock_data/global_solutions_ltd_financials.json`**
```json
{
  "company_name": "Global Solutions Ltd.",
  "ticker": "GSL",
  "report_date": "2024-09-30",
  "income_statement": {
    "revenue": 850000000,
    "cost_of_goods_sold": 400000000,
    "gross_profit": 450000000,
    "operating_expenses": 250000000,
    "net_income": 120000000
  },
  "balance_sheet": {
    "total_assets": 2000000000,
    "total_liabilities": 1500000000,
    "shareholder_equity": 500000000
  }
}
```

### 1.3 Define the Knowledge Base Configuration
This YAML file configures a built-in Milvus knowledge base. It instructs Orchestrate to ingest the specified documents, process them using an embedding model, and make them searchable for the `Industry_Insight_Agent`.

**File: `knowledge_base/industry_reports_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: industry_reports_kb
description: >
  Contains analyst reports, market outlooks, and best practice guides for the technology and financial sectors. Used to answer qualitative questions about industry benchmarks, definitions, and trends.
documents:
  - "knowledge_base/documents/Tech_Sector_Outlook_2024.pdf"
  - "knowledge_base/documents/Financial_Ratio_Best_Practices.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Create Python Tools
Tools are the building blocks that give agents their abilities. We will implement them as Python functions, using the `@tool` decorator and detailed docstrings. The docstrings are critical, as they serve as the "API documentation" for the agent's Large Language Model (LLM), enabling it to understand each tool's purpose, inputs, and outputs.

### 2.1 Market Data Tools

**Business Value & Purpose**: The `Market_Data_Agent` uses these tools to perform the foundational task of data aggregation. In a real-world scenario, this step is incredibly time-consuming, requiring analysts to pull data from multiple, disparate systems. These tools automate that entire process, fetching company financials, live stock data, and relevant news with simple commands. This ensures data is fresh and consistent, while freeing up significant analyst time.

**Technical Implementation**: The tools are designed to read from our local mock JSON files, simulating API calls. They include realistic data structures and basic error handling for cases where a company's data might not be found. The `get_latest_stock_price` tool adds a random fluctuation to a base price to simulate market volatility, making the demo more dynamic. The `search_market_news` tool returns a list of dictionaries, a common format for news API responses.

**File: `tools/market_data_tools.py`**
```python
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
```

### 2.2 Quantitative Analysis Tools

**Business Value & Purpose**: These tools encapsulate the core business logic of financial analysis. By defining calculations like financial ratios in code, we ensure that every analysis is performed consistently and accurately, eliminating the risk of human error from manual spreadsheet calculations. The `summarize_income_statement` tool further adds value by translating raw numbers into a narrative summary, a key first step in drafting a report.

**Technical Implementation**: The `calculate_financial_ratios` function takes raw financial numbers as inputs and returns a structured dictionary of key metrics. It includes important error handling, such as checking for division-by-zero when calculating ratios, which makes the tool robust. The calculation for Price-to-Earnings (P/E) is a simplification for the demo but demonstrates how complex, domain-specific formulas can be encoded into a reusable tool.

**File: `tools/quantitative_analysis_tools.py`**
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="calculate_financial_ratios", permission=ToolPermission.ADMIN)
def calculate_financial_ratios(total_liabilities: float, shareholder_equity: float, net_income: float, revenue: float, stock_price: float) -> dict:
    """
    Calculates key financial ratios from raw financial data.

    Args:
        total_liabilities (float): The company's total liabilities.
        shareholder_equity (float): The company's total shareholder equity.
        net_income (float): The company's net income.
        revenue (float): The company's total revenue.
        stock_price (float): The current stock price per share.

    Returns:
        dict: A dictionary containing calculated ratios: 'debt_to_equity', 'profit_margin', and 'price_to_earnings'.
    """
    try:
        debt_to_equity = round(total_liabilities / shareholder_equity, 2) if shareholder_equity != 0 else float('inf')
        profit_margin = round((net_income / revenue) * 100, 2) if revenue != 0 else 0.0
            
        # P/E is not meaningful for negative earnings
        if net_income <= 0:
            price_to_earnings = None
        else:
            # This is a simplification; a real calculation uses Earnings Per Share (EPS)
            simulated_shares = shareholder_equity * 0.1 # Simulate share count
            eps = net_income / simulated_shares
            price_to_earnings = round(stock_price / eps, 2) if eps > 0 else None

        return {
            "debt_to_equity_ratio": debt_to_equity,
            "profit_margin_percent": profit_margin,
            "price_to_earnings_ratio": price_to_earnings
        }
    except Exception as e:
        return {"error": f"An error occurred during ratio calculation: {str(e)}"}

@tool(name="summarize_income_statement", permission=ToolPermission.ADMIN)
def summarize_income_statement(income_statement: dict) -> str:
    """
    Generates a brief, human-readable summary of a company's income statement.

    Args:
        income_statement (dict): A dictionary representing the income statement with keys like 'revenue', 'net_income', etc.

    Returns:
        str: A human-readable summary of the income statement.
    """
    revenue = income_statement.get('revenue', 0)
    gross_profit = income_statement.get('gross_profit', 0)
    net_income = income_statement.get('net_income', 0)
    
    summary = (
        f"The company generated ${revenue:,.2f} in revenue, "
        f"resulting in a gross profit of ${gross_profit:,.2f}. "
        f"After all expenses, the net income was ${net_income:,.2f}."
    )
    return summary
```

### 2.3 Reporting Tools

**Business Value & Purpose**: This tool represents the final, crucial step in the workflow: synthesis. The `Financial_Analyst_CoPilot` uses this tool to assemble the outputs from all other agents into a single, structured, and professional report. This automates the tedious task of formatting and report generation, ensuring a consistent and high-quality output every time. It's the capstone of the process, transforming disparate data points into a coherent analytical product.

**Technical Implementation**: This is a straightforward Python function that uses an f-string template to format its inputs into a clean, markdown-formatted report. It accepts all the key pieces of information generated throughout the workflow (summaries, ratios, news, insights) and structures them under clear headings. This demonstrates how an agent can use a simple tool to produce complex, formatted outputs.

**File: `tools/reporting_tools.py`**
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="generate_final_report", permission=ToolPermission.ADMIN)
def generate_final_report(company_name: str, financial_summary: str, ratio_analysis: dict, news_summary: str, qualitative_insights: str) -> str:
    """
    Compiles all gathered information into a single, formatted financial analysis report. This is the final step.

    Args:
        company_name (str): The name of the company being analyzed.
        financial_summary (str): A summary of the income statement.
        ratio_analysis (dict): A dictionary of calculated financial ratios.
        news_summary (str): A summary of recent market news.
        qualitative_insights (str): Insights from the knowledge base about industry context.

    Returns:
        str: A comprehensive, formatted report ready for the user.
    """
    
    report = f"""
# Financial Analysis Report: {company_name}

## 1. Quantitative Financial Summary
{financial_summary}

## 2. Key Financial Ratios
- **Debt-to-Equity Ratio**: {ratio_analysis.get('debt_to_equity_ratio', 'N/A')}
- **Profit Margin**: {ratio_analysis.get('profit_margin_percent', 'N/A')}%
- **Price-to-Earnings (P/E) Ratio**: {ratio_analysis.get('price_to_earnings_ratio', 'N/A')}

## 3. Qualitative Context and Industry Benchmarks
{qualitative_insights}

## 4. Recent Market News
{news_summary}

--- End of Report ---
"""
    return report
```

### 2.4 Create `requirements.txt`
This file declares any external Python libraries required by the tools. While our current tools only use standard libraries, including this file is a best practice for ensuring reproducibility and preparing for future enhancements that may require packages like `requests` or `pandas`.

**File: `requirements.txt`**
```text
# No external dependencies required for this specific mock data demo.
# Add libraries like 'requests' here if tools were to call live APIs.
```

## Step 3: Define Agent Configurations (YAML)
Agents are defined in YAML files. These configurations specify an agent's name, description, instructions, the LLM it uses, and the tools and collaborators it has access to. The `description` and `instructions` are paramount for the system's success.

### 3.1 Industry Insight Agent (RAG Specialist)
**Purpose**: This agent serves as the team's domain expert. Its role is to provide qualitative context that numbers alone cannot. By querying the knowledge base, it can explain what a financial ratio means, whether it's high or low for a specific industry, and provide context from analyst reports. This mirrors the research phase of an analyst's work.

**File: `agents/01_industry_insight_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Industry_Insight_Agent
description: >
  An expert agent that provides qualitative context on financial analysis. It answers questions about industry trends, financial metric definitions, and best practices by consulting a curated knowledge base of analyst reports and guides.

  This agent's primary function is to leverage Retrieval-Augmented Generation (RAG) to find and synthesize information from its document store. It should be used for any query that requires explanation, definition, or contextual understanding, such as "Is a 2.1 Debt-to-Equity ratio high for a tech company?" or "What are the key trends in the tech sector this year?". It does not perform calculations or access live data.
instructions: >
  Your sole purpose is to answer questions based on the provided knowledge base. When asked about financial ratios or industry benchmarks, search your documents for relevant information and provide a clear, concise answer. Cite the information from your knowledge base. Do not perform calculations or fetch live data.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools: []
collaborators: []
knowledge_base:
  - industry_reports_kb
```

### 3.2 Market Data Agent (Data Retrieval Specialist)
**Purpose**: This agent is the data gatherer. It is a specialist focused entirely on interfacing with data sources to retrieve raw financial information. Its existence as a separate agent allows for modularity; if data sources change or new ones are added, only this agent and its tools need to be updated.

**File: `agents/02_market_data_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Market_Data_Agent
description: >
  A specialist agent for fetching financial information. It can retrieve company financial statements, get the latest stock prices, and search for recent market news from various data sources. 

  This agent acts as the primary data interface for the financial analysis workflow. It should be invoked at the beginning of any analysis to gather all necessary raw data points. Its capabilities are strictly limited to data retrieval; it does not perform any analysis, calculation, or interpretation of the data it fetches.
instructions: >
  You are a data retrieval expert. Use your tools to fetch the specific data requested. 
  - Use 'fetch_company_financials' for income statements and balance sheets.
  - Use 'get_latest_stock_price' for real-time stock data.
  - Use 'search_market_news' for recent news articles.
  Return the raw data from the tools without interpretation.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - fetch_company_financials
  - get_latest_stock_price
  - search_market_news
collaborators: []
```

### 3.3 Quantitative Analysis Agent (Calculation Specialist)
**Purpose**: This agent is the "quant" on the team. It takes the raw data gathered by the `Market_Data_Agent` and transforms it into meaningful metrics and summaries. By centralizing all calculations within this agent, we ensure that financial logic is applied consistently across all analyses.

**File: `agents/03_quantitative_analysis_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Quantitative_Analysis_Agent
description: >
  A specialist agent that performs complex numerical calculations and financial modeling. It can calculate key financial ratios and generate summaries from raw financial data.

  This agent is the computational engine of the analysis team. It should be used after raw data has been collected to derive key performance indicators and metrics. It is responsible for the accuracy and consistency of all financial calculations. It does not fetch data or provide qualitative opinions, it only processes the numbers provided to it.
instructions: >
  You are a quantitative analyst. Your job is to perform calculations on the data provided to you.
  - Use the 'calculate_financial_ratios' tool when you have all the required inputs (liabilities, equity, income, revenue, stock price).
  - Use the 'summarize_income_statement' tool to create a brief text summary from income statement data.
  Provide only the results of your calculations.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - calculate_financial_ratios
  - summarize_income_statement
collaborators: []
```

### 3.4 Financial Analyst Co-Pilot (Supervisor Agent)
**Purpose**: This is the project manager and lead analyst. It interfaces with the human user, understands their high-level requests, and orchestrates the specialist agents to execute the required tasks in the correct sequence. Its instructions are the most critical, defining the entire multi-agent workflow and reasoning process.

**File: `agents/04_financial_analyst_copilot.yaml`**
```yaml
spec_version: v1
kind: native
name: Financial_Analyst_CoPilot
description: >
  An expert financial analyst assistant that orchestrates a team of specialized agents to retrieve market data, perform quantitative analysis, consult industry knowledge, and generate comprehensive financial reports. This is the primary agent for users to interact with.

  As the supervisor, it deconstructs complex user requests like "analyze company X" into a series of smaller, manageable tasks. It then delegates these tasks to the appropriate specialist agents, collects their results, and synthesizes them into a final, coherent output. Its core value lies in its ability to manage the end-to-end analytical workflow, ensuring all necessary steps are completed in the correct order.
instructions: >
  You are a supervisor agent managing a financial analysis workflow. Your goal is to break down user requests into a logical sequence of tasks and delegate them to the appropriate collaborator agent.

  Reasoning:
  - For retrieving any company financial data, stock prices, or market news, you MUST use the Market_Data_Agent.
  - For calculating financial ratios or summarizing financial statements, you MUST use the Quantitative_Analysis_Agent.
  - For questions about industry trends, definitions of financial terms, or benchmarks, you MUST consult the Industry_Insight_Agent.

  Workflow:
  1.  **Phase 1: Data Collection.** Upon receiving a request for a financial analysis, your first step is to delegate to the Market_Data_Agent to fetch all necessary raw data (financials, stock price, news).
  2.  **Phase 2: Quantitative Processing.** Once you have the raw data, pass it to the Quantitative_Analysis_Agent to perform calculations and summarizations.
  3.  **Phase 3: Qualitative Enrichment.** After calculating key ratios, consult the Industry_Insight_Agent to get qualitative context for those ratios (e.g., "is this ratio considered high?").
  4.  **Phase 4: Synthesis & Reporting.** Finally, synthesize all the information received from your collaborators (data, calculations, context, news) and use your 'generate_final_report' tool to create a single, coherent report for the user.
llm: watsonx/meta-llama/llama-3-8b-instruct
style: default
collaborators:
  - Market_Data_Agent
  - Quantitative_Analysis_Agent
  - Industry_Insight_Agent
tools:
  - generate_final_report
```

## Step 4: Import and Deploy the Solution
With all assets created, we will use the ADK CLI to deploy them to your watsonx Orchestrate environment. The order of operations is important: tools must be imported before the agents that use them, and specialist agents must be imported before the supervisor that collaborates with them.

**Run these commands from the root `financial_copilot_demo/` directory.**

### 4.1 Import All Tools
```bash
echo "Importing market data tools..."
orchestrate tools import -k python -f tools/market_data_tools.py

echo "Importing quantitative analysis tools..."
orchestrate tools import -k python -f tools/quantitative_analysis_tools.py

echo "Importing reporting tools..."
orchestrate tools import -k python -f tools/reporting_tools.py
```

### 4.2 Import the Knowledge Base
```bash
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge_base/industry_reports_kb.yaml
```
*(Note: Ingestion may take a few minutes. You can check the status with `orchestrate knowledge-bases status --name industry_reports_kb`. Wait for the status to be `Ready` before proceeding.)*

### 4.3 Import the Agents
Import the specialist agents first, followed by the supervisor agent.
```bash
echo "Importing collaborator agents..."
orchestrate agents import -f agents/01_industry_insight_agent.yaml
orchestrate agents import -f agents/02_market_data_agent.yaml
orchestrate agents import -f agents/03_quantitative_analysis_agent.yaml

echo "Importing supervisor agent..."
orchestrate agents import -f agents/04_financial_analyst_copilot.yaml
```

## Step 5: Verification and Demo Scenarios
Your multi-agent system is now live. To interact with it, start the Orchestrate chat interface from your terminal.

```bash
orchestrate chat start
```
A browser window will open with the chat interface. Select the `Financial_Analyst_CoPilot` agent from the agent list to begin the demonstration.

### Demo Scenario 1: Comprehensive Company Analysis
This showcases the full, end-to-end workflow orchestration.

*   **User Prompt:**
    > "Generate a full financial analysis for Innovate Inc. using their latest quarterly data."
*   **Expected Workflow:**
    1.  `Financial_Analyst_CoPilot` receives the request and initiates Phase 1.
    2.  It calls `Market_Data_Agent`, which uses `fetch_company_financials('Innovate Inc.')`, `get_latest_stock_price('INVT')`, and `search_market_news('Innovate Inc.')`.
    3.  Co-Pilot receives the raw data and begins Phase 2. It calls `Quantitative_Analysis_Agent` with the financial data, which uses `calculate_financial_ratios(...)` and `summarize_income_statement(...)`.
    4.  Co-Pilot receives the calculated ratios and begins Phase 3. It calls `Industry_Insight_Agent` with a prompt like: "What is a good Debt-to-Equity ratio for a tech company?".
    5.  Finally, in Phase 4, the Co-Pilot gathers all outputs and uses its `generate_final_report` tool to present a complete, formatted report to the user.

### Demo Scenario 2: Specific Metric Query
This demonstrates targeted tool use and RAG for a more focused question.

*   **User Prompt:**
    > "What is the Debt-to-Equity ratio for Global Solutions Ltd. and is that considered high for the tech sector?"
*   **Expected Workflow:**
    1.  `Financial_Analyst_CoPilot` identifies two distinct tasks.
    2.  It calls `Market_Data_Agent` to get financials for "Global Solutions Ltd."
    3.  It passes the data to `Quantitative_Analysis_Agent` to calculate the D/E ratio.
    4.  Simultaneously or sequentially, it delegates the second part of the question ("is that considered high?") to `Industry_Insight_Agent`, which queries its knowledge base.
    5.  The Co-Pilot receives both the number (e.g., 3.0) and the context (e.g., "A ratio above 2.0 may indicate excessive risk") and synthesizes them into a single, helpful answer.

### Demo Scenario 3: Market News Impact
This highlights data retrieval and the supervisor's reasoning capabilities.

*   **User Prompt:**
    > "Summarize recent news about Innovate Inc. and explain its potential impact."
*   **Expected Workflow:**
    1.  `Financial_Analyst_CoPilot` delegates the retrieval task to `Market_Data_Agent`, which uses the `search_market_news` tool.
    2.  The Co-Pilot receives the list of news articles.
    3.  It uses its own LLM reasoning capabilities (guided by its instructions) to summarize the key points from the articles and provide a brief analysis of the potential impact, demonstrating its ability to synthesize unstructured information.

## Troubleshooting

*   **`Tool not found` error**: Ensure all tools were imported successfully *before* importing the agents that use them. Double-check for typos between the tool names in the agent YAML files and the `name` parameter in the `@tool` decorators.
*   **Agent Not Routing to Collaborator**: This is often an issue with the supervisor's `instructions`. Make them as explicit as possible (e.g., "You MUST use agent X for task Y"). Also, ensure the collaborator agent `description` is clear, detailed, and accurately reflects its capabilities, as the supervisor uses this for routing decisions.
*   **Knowledge Base Not Returning Answers**: Run `orchestrate knowledge-bases status --name industry_reports_kb` to confirm ingestion is complete (`Ready: true`). Verify that the question you are asking is relevant to the content in the ingested `.txt` and `.pdf` documents.
*   **Python Errors in Tools**: If a tool fails, check the terminal where you ran `orchestrate chat start` for Python stack traces. This can help debug issues in your tool's logic or problems with reading mock data files (e.g., incorrect file paths).

## Best Practices

*   **Descriptive Naming and Descriptions**: The clarity of agent and tool descriptions is paramount. The supervisor agent's LLM relies heavily on these descriptions to make correct routing decisions. Treat them as API documentation for the AI.
*   **Atomic Tools**: Design tools to perform one specific function well. This makes them more reusable and easier for the agent to reason about. For example, `fetch_company_financials` is better than a single tool that tries to fetch all possible data types.
*   **Explicit Instructions**: For supervisor agents, be direct and explicit in your instructions about which collaborator to use for which task. A structured workflow (like the "Phases" in our example) reduces ambiguity and improves the reliability of the orchestration.
*   **Iterative Development**: Start with one agent and one tool. Test it, verify it works, and then gradually build out the complexity by adding more tools and collaborator agents. This makes troubleshooting much simpler.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
