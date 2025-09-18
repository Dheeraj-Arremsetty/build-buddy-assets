# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 18:58:34
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: S&P Global Market Intelligence Agent Factory

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building the **S&P Global Market Intelligence Agent Factory** demo using IBM watsonx Orchestrate. The plan is tailored to S&P Global's strategic goal of transforming from a data provider into a high-value, AI-native service platform.

The core of this demo is a multi-agent architecture that showcases how S&P Global can productize its proprietary data. We will build a secure, S&P-managed "Data Steward" agent that exposes certified data access tools. Clients can then use this trusted agent as a building block (a collaborator) to construct their own custom supervisor agents for complex financial analysis, without needing to write complex code or manage data connections. This directly addresses the client's objective to create a new, monetizable product offering, increase data stickiness, and empower non-technical financial analysts.

## 2. Prerequisites

Before starting, ensure your environment is correctly configured.

*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured.
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
*   **Python Environment:** A working Python environment (3.9 or higher) is required.
*   **Required Python Libraries:** The tools in this demo rely on the `pandas` library for data manipulation.
    ```bash
    pip install pandas
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized and set as your current context.
    ```bash
    # Example for initializing a local developer environment
    orchestrate server start -e .env
    orchestrate env init --name local-dev --url http://127.0.0.1:8000
    orchestrate env set local-dev
    ```

## 3. Step-by-Step Instructions

### Step 1: Project Setup and Mock Data Creation

First, we will set up our project directory and create the synthetic data files that will simulate S&P Global's proprietary Snowflake database. This approach allows for a self-contained and easily demonstrable proof-of-concept.

1.  **Create the Project Directory:**
    ```bash
    mkdir sp_global_demo
    cd sp_global_demo
    ```

2.  **Create Mock Market Data (`mock_market_data.csv`):** This file contains foundational company information. The data is specifically designed to have multiple companies in the "Technology" sector in "Brazil" to satisfy the demo query.

    Create a file named `mock_market_data.csv` with the following content:
    ```csv
    company_id,company_name,ticker,sector,country,market_cap_usd
    C001,QuantumLeap Tech,QLEAP,Technology,Brazil,15000000000
    C002,VerdeSol Energy,VSOL,Renewables,Brazil,8000000000
    C003,Brasilia Digital,BDIG,Technology,Brazil,25000000000
    C004,Amazonas Logistics,ALOG,Logistics,Brazil,12000000000
    C005,Rio Banking Corp,RBCB,Finance,Brazil,35000000000
    C006,InovaMed Devices,IMD,Healthcare,Brazil,7500000000
    C007,Sao Paulo Software,SPS,Technology,Brazil,9000000000
    C008,Global Steel Inc,GSI,Industrials,USA,85000000000
    C009,NextGen AI,NGAI,Technology,USA,120000000000
    C010,EuroPharma,EUPH,Healthcare,Germany,95000000000
    C011,Apex Fintech,APEX,Finance,USA,60000000000
    C012,Digital Horizon,DHOR,Technology,Brazil,22000000000
    ```

3.  **Create Mock ESG Scores (`mock_esg_scores.csv`):** This file maps company IDs to their S&P ESG scores. The scores for the Brazilian tech companies are varied, with several scoring above the demo's threshold of 75.

    Create a file named `mock_esg_scores.csv` with the following content:
    ```csv
    company_id,sp_esg_score
    C001,82
    C002,78
    C003,91
    C004,65
    C005,72
    C006,85
    C007,74
    C008,55
    C009,88
    C010,92
    C011,68
    C012,79
    ```

4.  **Create Python Dependencies File (`requirements.txt`):** This file lists the necessary Python packages for our tools.

    Create a file named `requirements.txt` with the following content:
    ```text
    pandas
    ```

### Step 2: Develop S&P Global's Certified Data Tools

This is the core of S&P's value proposition in the demo. We create Python functions decorated with `@tool` that act as secure, governed gateways to the mock data. The `permission=ToolPermission.ADMIN` setting signifies that only S&P administrators can create or modify these foundational data connections, ensuring data integrity and governance.

Create a Python file named `sp_tools.py` and add the following code:

```python
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

```

### Step 3: Define the Agent Architecture with YAML

Now we define our two agents using YAML configuration files. This step implements the powerful **Supervisor/Collaborator pattern**.

1.  **Create the S&P Data Steward Agent (Collaborator):** This agent is S&P's product. It is a secure gateway that knows how to use the certified tools. Its `description` is critical, as it allows other agents (like the client's supervisor agent) to understand its capabilities.

    Create a file named `sp_data_steward_agent.yaml`:
    ```yaml
    spec_version: v1
    kind: native
    name: SP_Data_Steward_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        A secure agent that provides access to S&P Global's proprietary data.
        It has tools to retrieve company market data, including market capitalization, sector, and country,
        as well as official S&P ESG scores for companies. Use this agent for any requests related to S&P market or ESG data.
    instructions: >
        You are a data retrieval service. When called upon by another agent, use your tools to fetch the requested
        market or ESG data accurately and return it directly. Do not interpret, analyze, or summarize the data. Your sole purpose is to execute your tools based on the inputs provided.
    collaborators: []
    tools:
      - get_market_data
      - get_company_esg_score
    ```

2.  **Create the Emerging Market Opportunity Agent (Supervisor):** This is the agent the client (a financial analyst) builds. It has no tools of its own. Its power comes from its ability to orchestrate and reason over the capabilities of its collaborator, the `SP_Data_Steward_Agent`. The `instructions` guide its multi-step logic to answer the complex query.

    Create a file named `emerging_market_agent.yaml`:
    ```yaml
    spec_version: v1
    kind: native
    name: Emerging_Market_Opportunity_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
        An agent for financial analysts to identify investment opportunities in emerging markets
        based on market capitalization and ESG performance, using certified S&P Global data.
    instructions: >
        Your goal is to answer complex financial queries by orchestrating data retrieval and synthesis.
        To do this, you must use the SP_Data_Steward_Agent collaborator.

        Follow these steps precisely:
        1.  First, call the `get_market_data` tool from the SP_Data_Steward_Agent to retrieve a list of companies based on the user's criteria (e.g., sector, country).
        2.  Next, for each company in the list you received, call the `get_company_esg_score` tool from the SP_Data_Steward_Agent to get its ESG score.
        3.  Then, filter this list of companies to keep only those that meet the ESG threshold mentioned by the user.
        4.  Finally, sort the remaining companies by market capitalization in descending order and return the top results as requested by the user in a clear, formatted list.
    collaborators:
      - SP_Data_Steward_Agent
    tools: []
    ```

### Step 4: Import Assets into watsonx Orchestrate

With all the configuration files and tools created, we now import them into watsonx Orchestrate using the ADK's CLI. The order of operations is critical: tools must be imported first, followed by the collaborator agent, and finally the supervisor agent that depends on the collaborator.

Execute these commands from your terminal within the `sp_global_demo` directory:

1.  **Import the Certified Tools (S&P Developer Persona):**
    ```bash
    orchestrate tools import -f sp_tools.py
    ```
    *Output should confirm that `get_market_data` and `get_company_esg_score` were successfully imported.*

2.  **Import the Data Steward Agent (S&P Developer Persona):**
    ```bash
    orchestrate agents import -f sp_data_steward_agent.yaml
    ```
    *Output should confirm `SP_Data_Steward_Agent` was successfully imported.*

3.  **Import the Client's Custom Agent (Financial Analyst Persona):**
    ```bash
    orchestrate agents import -f emerging_market_agent.yaml
    ```
    *Output should confirm `Emerging_Market_Opportunity_Agent` was successfully imported.*

## 4. Verification and Demo Execution

Now, you will play the role of the financial analyst interacting with the custom agent they just built.

1.  **Start the Chat Session:** Launch an interactive chat with the supervisor agent.

    ```bash
    orchestrate chat start --agent Emerging_Market_Opportunity_Agent
    ```

2.  **Execute the Core Business Query:** Once the chat interface is running, enter the key prompt:

    ```text
    Find the top 3 companies in the Brazilian technology sector by market cap that have an S&P ESG score above 75.
    ```

3.  **Observe the Reasoning and Final Output:**
    watsonx Orchestrate will display the agent's thought process. You should see it:
    *   Recognize the need for market and ESG data.
    *   Delegate the task to the `SP_Data_Steward_Agent`.
    *   Invoke the `get_market_data` tool with `sector='Technology'` and `country='Brazil'`.
    *   Invoke the `get_company_esg_score` tool for each resulting company.
    *   Filter, sort, and synthesize the final answer.

    **Expected Output:** The agent should return a clear, concise list similar to this:

    ```text
    Here are the top 3 companies in the Brazilian technology sector with an S&P ESG score above 75, ranked by market cap:

    1.  **Brasilia Digital (BDIG)** - Market Cap: $25,000,000,000, ESG Score: 91
    2.  **Digital Horizon (DHOR)** - Market Cap: $22,000,000,000, ESG Score: 79
    3.  **QuantumLeap Tech (QLEAP)** - Market Cap: $15,000,000,000, ESG Score: 82
    ```

## 5. Troubleshooting

*   **Error: `Collaborator 'SP_Data_Steward_Agent' not found`:** This occurs if you import `emerging_market_agent.yaml` before `sp_data_steward_agent.yaml`. Ensure the collaborator agent is imported first. Re-run the import command for the supervisor agent.
*   **Error: `Tool 'get_market_data' not found`:** This means the tool was not correctly associated with the `SP_Data_Steward_Agent`. Verify that the `orchestrate tools import` command ran successfully and that the tool names in `sp_data_steward_agent.yaml` exactly match the `name` attribute in the `@tool` decorators.
*   **Agent doesn't call the collaborator:** If the supervisor agent tries to answer without using the collaborator, its `description` and `instructions` may not be clear enough. Ensure the supervisor's instructions explicitly state to "use the SP_Data_Steward_Agent". Also, check that the collaborator's `description` clearly states its capabilities regarding market and ESG data.
*   **Python Tool Errors (e.g., `FileNotFoundError`):** Ensure the `mock_market_data.csv` and `mock_esg_scores.csv` files are in the same directory where you are running the `orchestrate` commands.

## 6. Best Practices

*   **Descriptive Clarity:** The success of the supervisor/collaborator pattern hinges on the quality of the `description` and `instructions` fields. The supervisor agent uses the collaborator's description to discover its capabilities. Be explicit and comprehensive.
*   **Secure Tooling:** The use of `permission=ToolPermission.ADMIN` is a powerful pattern for creating a governed data access layer. It establishes a clear separation of concerns between the data provider (S&P) and the data consumer (the client analyst).
*   **Atomic Tools:** Design tools to be atomic and single-purpose (e.g., one tool to get market data, another to get ESG scores). This makes them more reusable and easier for the supervisor agent to chain together in complex workflows.
*   **Error Handling in Tools:** Always include robust error handling (like `try...except` blocks) in your Python tools. This prevents the agent from failing on unexpected issues and allows it to report problems back to the user gracefully.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
