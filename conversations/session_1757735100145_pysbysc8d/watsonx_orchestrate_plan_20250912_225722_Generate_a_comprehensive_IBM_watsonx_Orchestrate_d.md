# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 22:57:22
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: S&P Global Credit Intelligence Co-Pilot

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying the **S&P Global Credit Intelligence Co-Pilot**, a sophisticated multi-agent system using IBM watsonx Orchestrate. This solution is specifically designed to address S&P Global's core business need of accelerating the preliminary stages of credit risk assessment. By automating the laborious data gathering and synthesis process, the Co-Pilot empowers S&P Global analysts to focus on high-value strategic analysis and judgment, aiming for a **30-50% reduction in preliminary research time**.

The Co-Pilot leverages a supervisor-collaborator agent architecture, a powerful pattern recommended by IBM. A primary `Credit_Risk_Synthesizer_Agent` orchestrates two specialized agents: a `Financial_Data_Agent` for quantitative analysis of corporate filings and a `Market_Intelligence_Agent` for qualitative analysis of market data and news sentiment. This plan details the creation of all agents, their underlying Python tools, a Retrieval-Augmented Generation (RAG) knowledge base, and the mock data required to simulate a realistic credit analysis workflow, culminating in a powerful and compelling client demonstration. This updated plan incorporates best practices for code reusability and maintainability.

## 2. Prerequisites

Before beginning, ensure your development environment is correctly configured according to IBM watsonx Orchestrate standards.

*   **IBM watsonx Orchestrate Account**: An active account with access to the watsonx Orchestrate service.
*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured.
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Python**: Python 3.10 or later is required.
*   **Environment Initialization**: Your ADK environment must be initialized and connected to your watsonx Orchestrate instance. This command will guide you through logging in and selecting your environment.
    ```bash
    orchestrate env init
    ```
*   **Project Directory**: A dedicated folder to organize all project files.

## 3. Project Directory Structure

To maintain a clean and manageable project, create the following directory structure. This organization separates agents, tools, knowledge bases, and mock data, aligning with ADK best practices.

```
spg_copilot_demo/
├── agents/
│   ├── Credit_Risk_Synthesizer_Agent.yaml
│   ├── Financial_Data_Agent.yaml
│   └── Market_Intelligence_Agent.yaml
├── tools/
│   ├── financial_tools.py
│   └── market_tools.py
├── knowledge_bases/
│   └── market_news_kb.yaml
├── mock_data/
│   ├── filings/
│   │   ├── innovatech_solutions.json
│   │   └── global_logistics_corp.json
│   └── news/
│       ├── innovatech_product_launch.txt
│       └── globallogistics_disruption.txt
└── requirements.txt
```

## 4. Step-by-Step Implementation

### Step 4.1: Create Mock Data Sources

This step involves creating realistic synthetic data that our tools will use to simulate interactions with financial data providers and news sources. This self-contained data ensures the demo is reliable and requires no external API access.

1.  **Create Mock Corporate Filings (JSON)**: These files represent simplified annual reports containing key financial metrics.

    *File: `mock_data/filings/innovatech_solutions.json`*
    ```json
    {
      "company_name": "Innovatech Solutions",
      "ticker": "INVT",
      "report_date": "2023-12-31",
      "currency": "USD",
      "financials": {
        "revenue": 5200000000,
        "net_income": 850000000,
        "total_assets": 12000000000,
        "total_liabilities": 4500000000,
        "total_equity": 7500000000,
        "total_debt": 2100000000,
        "ebitda": 1400000000
      }
    }
    ```

    *File: `mock_data/filings/global_logistics_corp.json`*
    ```json
    {
      "company_name": "Global Logistics Corp",
      "ticker": "GLC",
      "report_date": "2023-12-31",
      "currency": "USD",
      "financials": {
        "revenue": 12300000000,
        "net_income": 450000000,
        "total_assets": 18000000000,
        "total_liabilities": 11000000000,
        "total_equity": 7000000000,
        "total_debt": 8500000000,
        "ebitda": 1800000000
      }
    }
    ```

2.  **Create Synthetic News Articles (TXT)**: These files will be ingested into our knowledge base to power the RAG capabilities of the `Market_Intelligence_Agent`.

    *File: `mock_data/news/innovatech_product_launch.txt`*
    ```
    Headline: Innovatech Solutions Launches Breakthrough AI Platform 'Nexus'
    Date: 2024-05-10
    
    Innovatech Solutions today announced the launch of 'Nexus', a groundbreaking generative AI platform poised to disrupt the enterprise software market. Analysts predict the launch could significantly boost revenue streams and market share over the next fiscal year. CEO Jane Doe stated, "Nexus represents a quantum leap in enterprise intelligence, and we are confident in its strong market adoption." The company's stock surged 15% on the news.
    ```

    *File: `mock_data/news/globallogistics_disruption.txt`*
    ```
    Headline: Global Logistics Corp Faces Major Supply Chain Disruption After Port Strike
    Date: 2024-05-15

    Global Logistics Corp is currently grappling with significant operational headwinds following a major strike at a key international shipping port. The disruption is expected to impact Q2 earnings and has raised concerns about the company's short-term liquidity and ability to meet delivery commitments. The company has stated it is exploring alternative routes, but analysts remain cautious, downgrading the stock from 'Buy' to 'Hold'. The full financial impact is expected to be detailed in the next earnings call.
    ```

### Step 4.2: Develop Python Tools

Here, we create the Python functions that our agents will use to perform actions. Each tool is defined with the `@tool` decorator and includes a detailed docstring, which is critical for the agent's LLM to understand its function, arguments, and return values.

1.  **Create `requirements.txt`**: This file lists Python dependencies. Since our tools only use standard libraries (`json`, `os`, `random`), this file will be empty. Including it is a best practice for project structure.
    *File: `requirements.txt`*
    ```
    # No external packages are required for this demo's tools.
    ```

2.  **Create Financial Data Tools**

    **Business Value**: These tools automate the extraction and calculation of fundamental financial metrics, which are the bedrock of any credit analysis. They replace manual data entry and calculation from filings, reducing human error and freeing up analyst time for more strategic work. This improved version uses a helper function to avoid code duplication, making the tools more maintainable.

    *File: `tools/financial_tools.py`*
    ```python
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
```yaml
spec_version: v1
kind: knowledge_base
name: market_news_kb
description: >
  A knowledge base containing recent news articles, press releases, and market analysis for major public companies. Used to assess qualitative risk and market sentiment.
documents:
  - "mock_data/news/innovatech_product_launch.txt"
  - "mock_data/news/globallogistics_disruption.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 4.4: Define the Agent Architecture (YAML)

We will now define our three agents in separate YAML files. The descriptions and instructions are meticulously crafted to guide the LLM's reasoning, ensuring correct tool usage and collaborator routing. We will use `watsonx/ibm/granite-13b-chat-v2` for all agents to ensure consistent, high-quality reasoning capabilities.

1.  **Financial Data Agent**

    **Role**: This is a specialist agent focused on quantitative tasks. It uses its tools to fetch structured financial data and perform calculations, acting as a reliable source of hard numbers for the supervisor. Its narrow focus ensures accuracy and predictability.

    *File: `agents/Financial_Data_Agent.yaml`*
    ```yaml
    spec_version: v1
    kind: native
    name: Financial_Data_Agent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
      An expert agent for processing structured quantitative data. It extracts key metrics from corporate financial statements and calculates standard financial ratios like Debt-to-EBITDA and Debt-to-Equity.
    instructions: >
      Your sole purpose is to handle quantitative financial data.
      - When asked for financial statements or specific metrics like revenue or EBITDA, use the `get_financial_statements` tool.
      - When asked to calculate financial ratios, use the `calculate_key_ratios` tool.
      - Present the data clearly and concisely. Do not provide opinions or analysis.
    tools:
      - get_financial_statements
      - calculate_key_ratios
    ```

2.  **Market Intelligence Agent**

    **Role**: This agent specializes in unstructured, external data. It combines a tool for market data with a knowledge base of news articles to provide a qualitative view of a company's market position, recent developments, and overall sentiment.

    *File: `agents/Market_Intelligence_Agent.yaml`*
    ```yaml
    spec_version: v1
    kind: native
    name: Market_Intelligence_Agent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
      A specialist agent for gathering unstructured, external data. It provides public market data (stock price, market cap) and analyzes relevant news articles from its knowledge base to gauge market sentiment and identify qualitative risks.
    instructions: >
      You are an expert in market intelligence.
      - For requests about stock price, P/E ratio, or market capitalization, use the `get_market_performance` tool.
      - For questions about recent news, events, sentiment, or qualitative risks, search the `market_news_kb` knowledge base.
      - Summarize findings from the knowledge base into a coherent narrative.
    tools:
      - get_market_performance
    knowledge_base:
      - market_news_kb
    ```

3.  **Credit Risk Synthesizer Agent (Supervisor)**

    **Role**: This is the primary, user-facing agent. It acts as an orchestrator, breaking down a complex user request ("generate a credit report") into sub-tasks, delegating them to the appropriate specialist collaborator agents, and then synthesizing their responses into a final, structured report for the analyst.

    *File: `agents/Credit_Risk_Synthesizer_Agent.yaml`*
    ```yaml
    spec_version: v1
    kind: native
    name: Credit_Risk_Synthesizer_Agent
    llm: watsonx/ibm/granite-13b-chat-v2
    style: default
    description: >
      An expert AI assistant for S&P Global that orchestrates data gathering and analysis to create preliminary credit risk reports. It uses a Financial Data Agent for quantitative metrics and a Market Intelligence Agent for market data and news sentiment.
    instructions: >
      You are a master credit risk analyst co-pilot. Your job is to orchestrate collaborator agents to build a comprehensive preliminary credit report.

      Reasoning Strategy:
      1.  For any request related to financial statements, financial ratios, debt, or EBITDA, you MUST delegate the task to the `Financial_Data_Agent`.
      2.  For any request related to market performance, stock price, news, or market sentiment, you MUST delegate the task to the `Market_Intelligence_Agent`.
      3.  If a user asks for a comprehensive or full credit risk report, you must perform the following steps in order:
          a. Call the `Financial_Data_Agent` to get key financial ratios.
          b. Call the `Market_Intelligence_Agent` to get market performance data.
          c. Call the `Market_Intelligence_Agent` again to summarize recent news and sentiment.
          d. Synthesize all the collected information into a final report with three distinct sections: "Financial Health Analysis", "Market Position", and "Qualitative Risk Factors".
      4.  Always present the final synthesized report in a clean, well-formatted markdown structure.
    collaborators:
      - Financial_Data_Agent
      - Market_Intelligence_Agent
    ```

### Step 4.5: Deploy the Co-Pilot to watsonx Orchestrate

This is the final step where we use the ADK CLI to import all our assets into the watsonx Orchestrate platform. The order of operations is critical: dependencies (tools, knowledge bases) must be imported before the assets that use them (agents).

Execute these commands from the root of your `spg_copilot_demo` directory.

1.  **Import Python Tools**:
    ```bash
    # Import the financial tools
    orchestrate tools import -f tools/financial_tools.py

    # Import the market intelligence tools
    orchestrate tools import -f tools/market_tools.py
    ```

2.  **Import the Knowledge Base**:
    ```bash
    # Import and ingest documents for the news knowledge base
    orchestrate knowledge-bases import -f knowledge_bases/market_news_kb.yaml
    ```

3.  **Import Collaborator Agents**:
    ```bash
    # Import the specialist agents first as they are dependencies for the supervisor
    orchestrate agents import -f agents/Financial_Data_Agent.yaml
    orchestrate agents import -f agents/Market_Intelligence_Agent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    # Finally, import the main agent that orchestrates the others
    orchestrate agents import -f agents/Credit_Risk_Synthesizer_Agent.yaml
    ```

## 5. Verification and Demo Scenarios

After deploying all assets, you can interact with the `Credit_Risk_Synthesizer_Agent` in the watsonx Orchestrate chat interface. Use the following scenarios to verify its functionality and demonstrate its value to the client.

*   **Scenario 1: Comprehensive Report Generation**
    *   **User Prompt**: `"Generate a preliminary credit risk report for Innovatech Solutions."`
    *   **Expected Behavior**:
        1.  The `Credit_Risk_Synthesizer_Agent` receives the request.
        2.  It delegates to `Financial_Data_Agent` to get key ratios.
        3.  It delegates to `Market_Intelligence_Agent` to get market performance.
        4.  It delegates to `Market_Intelligence_Agent` to search the `market_news_kb`.
        5.  It synthesizes the results into a structured report with sections for Financial Health, Market Position, and Qualitative Risk Factors, including the positive news about the 'Nexus' platform launch.

*   **Scenario 2: Specific Quantitative Query**
    *   **User Prompt**: `"What is the debt-to-EBITDA ratio for Global Logistics Corp?"`
    *   **Expected Behavior**:
        1.  The `Credit_Risk_Synthesizer_Agent` identifies this as a quantitative question.
        2.  It correctly routes the request directly to the `Financial_Data_Agent`.
        3.  The `Financial_Data_Agent` uses its `calculate_key_ratios` tool.
        4.  The agent returns the direct answer (e.g., "The debt-to-EBITDA ratio for Global Logistics Corp is 4.72.").

*   **Scenario 3: Qualitative News & Sentiment Analysis**
    *   **User Prompt**: `"Summarize recent news and market sentiment for Global Logistics Corp."`
    *   **Expected Behavior**:
        1.  The `Credit_Risk_Synthesizer_Agent` identifies this as a qualitative request.
        2.  It routes the request to the `Market_Intelligence_Agent`.
        3.  The `Market_Intelligence_Agent` uses its `market_news_kb` to find the relevant article about the port strike.
        4.  It returns a summary highlighting the supply chain disruption, expected impact on earnings, and cautious analyst sentiment.

## 6. Troubleshooting

*   **Issue: Tool Import Fails with `ModuleNotFoundError`**:
    *   **Solution**: Ensure you have installed all dependencies listed in `requirements.txt` (`pip install -r requirements.txt`). In this case, the file is empty, so this error is unlikely. Verify that the Python file containing the tool has no syntax errors.
*   **Issue: Agent Does Not Route to the Correct Collaborator**:
    *   **Solution**: This is almost always an issue with the `description` of the collaborator agents or the `instructions` of the supervisor agent. Make them more explicit. For example, explicitly state in the supervisor's instructions: "For any task involving financial ratios, ALWAYS use the `Financial_Data_Agent`."
*   **Issue: Knowledge Base Returns No Results**:
    *   **Solution**: Verify the file paths in the `market_news_kb.yaml` are correct relative to where you are running the `orchestrate` command. Check the logs during the `knowledge-bases import` command for any ingestion errors. Ensure your query uses keywords present in the documents.
*   **Issue: `FileNotFoundError` in Python Tool**:
    *   **Solution**: The tool's logic for finding mock data files is sensitive to the current working directory. The provided code (`os.path.join(os.path.dirname(__file__), '..', ...`) is robust, but ensure your directory structure exactly matches the one specified in this plan.

## 7. Best Practices

*   **Descriptive Clarity is Key**: The performance of a supervisor-collaborator model is highly dependent on the quality of the `description` and `instructions` fields. Be explicit, unambiguous, and task-oriented in your writing.
*   **Modular and Atomic Tools**: Design tools to perform one specific task well (e.g., `get_financial_statements` vs. a single tool that does fetching and calculation). This makes them more reusable, testable, and easier for the LLM to reason about.
*   **Code Reusability**: As demonstrated in `financial_tools.py`, use helper functions to encapsulate common logic (like loading data files). This reduces code duplication and improves maintainability.
*   **Hierarchical Design**: For complex workflows, the supervisor-collaborator pattern is highly effective. The supervisor should only be responsible for orchestration and synthesis, while specialist agents handle the execution of specific tasks.
*   **Iterative Refinement**: Start with a basic agent structure and test it. Use the chat interaction to identify where reasoning fails, then refine the instructions or descriptions and re-import the agent. The `orchestrate agents import` command can be used to update an existing agent in place, speeding up the development cycle.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
