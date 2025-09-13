# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 23:52:25
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watxsonx Orchestrate Execution Plan: Dynamic Market Event Intelligence Orchestrator

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **Dynamic Market Event Intelligence Orchestrator**, a multi-agent solution for a financial services client. This plan directly addresses the client's core business need for rapid, data-driven market analysis by automating the initial research and synthesis phases of impact assessment. The solution leverages a supervisor agent to orchestrate a team of specialized collaborator agents that gather financial data, analyze historical precedents via a knowledge base (RAG), and aggregate breaking news. This improved version incorporates enhanced reasoning, more robust instructions, and expanded mock data to fully realize the client's demo scenarios, accelerating time-to-insight, enhancing analyst productivity, and ensuring a consistent, scalable analytical framework for reacting to market volatility.

## Prerequisites

Before beginning, ensure your development environment is set up with the following components. This setup is crucial for building, deploying, and testing the watsonx Orchestrate agents and tools.

1.  **Python 3.9+**: The IBM watsonx Orchestrate Agent Development Kit (ADK) is a Python library and requires a modern version of Python.
2.  **pip**: The Python package installer is required to install the ADK and other dependencies.
3.  **IBM watsonx Orchestrate ADK**: The core toolkit for building agents. Install it using the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
4.  **IBM watsonx Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured with the ADK. Follow the official documentation to run `orchestrate env init` and connect to your instance.
5.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and managing Python and YAML files.
6.  **Mock API Dependencies**: The tools will interact with a local mock API. Install the required packages:
    ```bash
    pip install Flask requests
    ```

## Step 1: Establish Project Structure and Mock Data Sources

A well-organized project structure is essential for managing the various components of this multi-agent system. We will also create the mock data sources that the agents' tools will interact with, simulating a real-world environment and covering all specified demo scenarios.

### 1.1. Create the Directory Structure

Create the following folder structure in your project's root directory. This separates agents, tools, knowledge base documents, and the mock API.

```
market_intelligence_orchestrator/
├── mock_api/
│   └── app.py
├── agents/
│   ├── impact_assessment_supervisor_agent.yaml
│   ├── financial_data_agent.yaml
│   ├── historical_precedent_agent.yaml
│   └── news_aggregator_agent.yaml
├── tools/
│   ├── financial_tools.py
│   └── news_tools.py
├── knowledge_base/
│   ├── historical_market_events_kb.yaml
│   └── documents/
│       ├── 2025_AI_Chip_Shock.txt
│       ├── 2026_Logistics_Freeze.txt
│       ├── 1990s_Trade_Disputes.txt
│       └── Suez_Canal_Blockage_2021.txt
└── requirements.txt
```

### 1.2. Create Mock Historical Event Documents

Populate the text files in the `knowledge_base/documents/` directory with the following content. These documents will be ingested into our knowledge base to power the RAG pattern for the `Historical Precedent Agent`.

**File: `knowledge_base/documents/2025_AI_Chip_Shock.txt`**
```
Event Title: The 2025 AI Chip Supply Shock
Date: June 15, 2025
Summary: A major fire at a leading semiconductor fabrication plant in Taiwan led to a global shortage of advanced AI accelerator chips.
Impact: The event caused a 30% spike in GPU prices within two weeks. Companies heavily reliant on AI, such as cloud computing providers and autonomous vehicle manufacturers, saw their stock prices drop by an average of 15%. The event highlighted the fragility of the semiconductor supply chain and accelerated investment in geographically diverse manufacturing facilities. The market took approximately 18 months to stabilize.
Key Sectors Affected: Semiconductors, Cloud Computing, Automotive, AI Research.
```

**File: `knowledge_base/documents/2026_Logistics_Freeze.txt`**
```
Event Title: Impact of the Global Logistics Freeze of 2026
Date: March 3, 2026
Summary: A coordinated cyberattack on major global shipping port management systems caused a near-total shutdown of maritime logistics for 72 hours.
Impact: The freeze led to immediate disruptions in supply chains worldwide, affecting retail, manufacturing, and technology sectors. Retail companies faced inventory shortages, leading to a 10% decline in quarterly revenue. Shipping and logistics stocks fell by 20-25% in the immediate aftermath. The event served as a catalyst for increased cybersecurity spending in the logistics industry and a push towards more resilient, decentralized supply chain models.
Key Sectors Affected: Global Shipping, Retail, Manufacturing, Cybersecurity.
```

**File: `knowledge_base/documents/1990s_Trade_Disputes.txt`**
```
Event Title: Analysis of the 1990s Automotive Trade Disputes
Date: Circa 1993-1995
Summary: A series of trade disputes between the United States and Japan over automotive imports resulted in the threat and brief imposition of significant tariffs.
Impact: European and American automotive manufacturers experienced a short-term competitive advantage. Japanese auto stocks saw temporary dips of 5-8% following tariff announcements. The disputes ultimately led to negotiated agreements for Japanese automakers to increase production within the United States, altering the global manufacturing landscape. The long-term impact was a more integrated global automotive supply chain but with increased political risk factors.
Key Sectors Affected: Automotive, Manufacturing, International Trade.
```

**File: `knowledge_base/documents/Suez_Canal_Blockage_2021.txt`**
```
Event Title: Precedent Analysis: The 2021 Suez Canal Blockage
Date: March 23, 2021
Summary: The container ship 'Ever Given' ran aground in the Suez Canal, blocking the critical waterway for six days and disrupting global trade.
Impact: The blockage was estimated to hold up $9.6 billion in trade each day. Global shipping and logistics companies faced significant delays and rerouting costs. Retail and manufacturing sectors experienced supply chain disruptions, impacting inventory levels and production schedules. The event exposed vulnerabilities in global supply chains concentrated around key choke points, leading to increased interest in alternative shipping routes and more sophisticated supply chain risk management strategies.
Key Sectors Affected: Global Shipping, Retail, Energy, Manufacturing.
```

### 1.3. Create the Mock APIs

Create a simple Flask application to serve as the mock endpoint for financial and news data. This version is expanded to cover all three client demo scenarios.

**File: `mock_api/app.py`**
```python
from flask import Flask, jsonify, request
import datetime

app = Flask(__name__)

# Mock S&P Financials API Data
mock_financial_data = {
    "QLI": { "companyName": "QuantumLeap Inc.", "ticker": "QLI", "marketCap": "950B USD", "peRatio": 35.2, "eps": 8.75, "52WeekHigh": 350.12, "52WeekLow": 210.45, "analystRating": "Strong Buy" },
    "AUTX": { "companyName": "AutoNoma GMBH", "ticker": "AUTX", "marketCap": "450B EUR", "peRatio": 18.5, "eps": 4.20, "52WeekHigh": 150.80, "52WeekLow": 95.25, "analystRating": "Hold" },
    "SHIP": { "companyName": "Global Maritime Logistics", "ticker": "SHIP", "marketCap": "120B USD", "peRatio": 12.1, "eps": 2.50, "52WeekHigh": 75.00, "52WeekLow": 45.00, "analystRating": "Buy" },
    "RETL": { "companyName": "Worldwide Retail Corp", "ticker": "RETL", "marketCap": "300B USD", "peRatio": 22.8, "eps": 5.10, "52WeekHigh": 210.00, "52WeekLow": 150.00, "analystRating": "Hold" }
}

# Mock Sector Performance API Data
mock_sector_data = {
    "Semiconductors": { "sector": "Semiconductors", "ytdPerformance": "+22.5%", "dailyChange": "+1.8%", "keyDrivers": ["AI demand", "Data center growth"], "outlook": "Positive" },
    "Automotive": { "sector": "European Automotive", "ytdPerformance": "-5.2%", "dailyChange": "-2.1%", "keyDrivers": ["EV transition", "Trade tariffs", "Supply chain costs"], "outlook": "Neutral to Negative" },
    "Shipping": { "sector": "Global Shipping", "ytdPerformance": "+8.0%", "dailyChange": "-3.5%", "keyDrivers": ["Global trade volume", "Fuel costs", "Port congestion"], "outlook": "Volatile" }
}

# Mock News Feed API Data
mock_news_data = {
    "quantumleap inc.": [
        { "headline": "QuantumLeap Inc. Unveils Fusion-Powered Processor, Stock Soars 30%", "source": "TechCrunch", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "The tech giant announced a breakthrough in processor technology that promises to revolutionize computing." },
        { "headline": "Regulators to Scrutinize QuantumLeap's New Technology", "source": "Wall Street Journal", "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(hours=1)).isoformat() + "Z", "summary": "Global regulatory bodies have expressed concerns over the potential monopolistic implications." }
    ],
    "trade tariffs": [
        { "headline": "New Trans-Atlantic Trade Tariffs Announced, Targeting Automotive and Luxury Goods", "source": "Reuters", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "Governments have imposed new tariffs, escalating trade tensions and rattling the European automotive industry." }
    ],
    "suez canal blockage": [
        { "headline": "BREAKING: Container Ship Blocks Suez Canal, Global Shipping Grinds to a Halt", "source": "Associated Press", "timestamp": datetime.datetime.utcnow().isoformat() + "Z", "summary": "A massive container ship has become wedged across the Suez Canal, causing a major traffic jam of vessels." }
    ]
}

@app.route('/financials/<ticker>', methods=['GET'])
def get_financials(ticker):
    data = mock_financial_data.get(ticker.upper())
    if data: return jsonify(data)
    return jsonify({"error": "Ticker not found"}), 404

@app.route('/sector/<sector_name>', methods=['GET'])
def get_sector_performance(sector_name):
    for key, value in mock_sector_data.items():
        if sector_name.lower() in key.lower():
            return jsonify(value)
    return jsonify({"error": "Sector not found"}), 404

@app.route('/news', methods=['GET'])
def get_news():
    query = request.args.get('q', '').lower()
    for key, articles in mock_news_data.items():
        if query in key:
            return jsonify({"articles": articles})
    return jsonify({"articles": []})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
```

### 1.4. Create `requirements.txt`

This file lists the Python dependencies for the project.

**File: `requirements.txt`**
```
requests
Flask
python-dotenv
ibm-watsonx-orchestrate
```

## Step 2: Develop Python Tools

The tools are the functional building blocks of our agents, performing specific actions like querying APIs. Each tool is a Python function decorated with `@tool` and includes a detailed docstring that the agent's LLM uses to understand its purpose, arguments, and return value. This ensures the supervisor can delegate tasks accurately.

### 2.1. Financial Data Tools

These tools are responsible for fetching company and sector financial data from our mock API. They provide the quantitative data needed for the impact assessment. The business value lies in their ability to instantly retrieve standardized financial metrics, eliminating manual data lookup and ensuring consistency in the data used for analysis.

**File: `tools/financial_tools.py`**
```python
import requests
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define the base URL for the mock API
BASE_URL = "http://127.0.0.1:5001"

@tool(permission=ToolPermission.ADMIN)
def get_company_financials(company_ticker: str) -> str:
    """
    Retrieves key financial data for a given company ticker from the internal S&P mock database.
    This includes market cap, P/E ratio, EPS, and analyst ratings.

    Args:
        company_ticker (str): The stock ticker symbol for the company (e.g., 'QLI').

    Returns:
        str: A JSON string containing the company's financial data or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/financials/{company_ticker}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})

@tool(permission=ToolPermission.ADMIN)
def get_sector_performance(sector_name: str) -> str:
    """
    Retrieves performance data for a specific market sector from the internal S&P mock database.
    This includes YTD performance, daily change, key drivers, and outlook.

    Args:
        sector_name (str): The name of the market sector to query (e.g., 'Semiconductors', 'Automotive').

    Returns:
        str: A JSON string containing the sector's performance data or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/sector/{sector_name}")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})
```

### 2.2. News Aggregation Tool

This tool fetches recent news articles related to a market event, providing crucial qualitative context for the analysis. Its business value comes from providing immediate, near real-time context on a developing situation, allowing analysts to understand the market narrative and public sentiment that quantitative data alone cannot capture.

**File: `tools/news_tools.py`**
```python
import requests
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define the base URL for the mock API
BASE_URL = "http://127.0.0.1:5001"

@tool(permission=ToolPermission.ADMIN)
def fetch_market_news(query: str) -> str:
    """
    Gathers the latest news articles and press releases related to a specific market event or company.

    Args:
        query (str): The search term for the news, such as a company name or event description (e.g., 'QuantumLeap Inc.', 'trade tariffs').

    Returns:
        str: A JSON string containing a list of relevant news articles or an error message.
    """
    try:
        response = requests.get(f"{BASE_URL}/news", params={"q": query})
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"API call failed: {str(e)}"})
```

## Step 3: Configure Knowledge Base and Agents

With the tools defined, we now configure the knowledge base and the agents. The agent definitions are created in YAML files, specifying their name, description, instructions, tools, and collaborators. These configurations are the blueprint for the AI's behavior.

### 3.1. Knowledge Base Configuration

This YAML file defines the knowledge base that the `Historical Precedent Agent` will use. It points to the document corpus we created, enabling powerful RAG capabilities to ground the agent's responses in factual historical data.

**File: `knowledge_base/historical_market_events_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: historical_market_events_kb
description: >
  A knowledge base containing detailed reports and analyses of significant historical market events, their causes, and their impact on various sectors. Use this to find historical analogues for current events.
documents:
  - "knowledge_base/documents/2025_AI_Chip_Shock.txt"
  - "knowledge_base/documents/2026_Logistics_Freeze.txt"
  - "knowledge_base/documents/1990s_Trade_Disputes.txt"
  - "knowledge_base/documents/Suez_Canal_Blockage_2021.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### 3.2. Collaborator Agent Configurations

These are the specialized agents that perform specific tasks. Their descriptions are crucial, as the supervisor agent uses them to decide which collaborator to delegate a task to.

**File: `agents/financial_data_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: financial_data_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent for retrieving real-time and historical financial data. It can query for specific company financials using a ticker symbol and get performance data for entire market sectors. Use this agent for any task requiring quantitative financial metrics like market cap, P/E ratio, or sector performance.
instructions: >
  Your sole purpose is to execute financial data retrieval tools.
  - Use the get_company_financials tool when asked for data about a specific company.
  - Use the get_sector_performance tool when asked for data about a market sector.
  - Return only the direct output from the tools. Do not add any conversational text.
tools:
  - get_company_financials
  - get_sector_performance
```

**File: `agents/news_aggregator_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: news_aggregator_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that gathers the latest news articles and press releases from various sources. It is used to get immediate context on a developing market event. Use this agent to understand the narrative and public sentiment surrounding an event.
instructions: >
  Your purpose is to fetch news. Use the fetch_market_news tool with a relevant query based on the user's request. Return only the direct output from the tool.
tools:
  - fetch_market_news
```

**File: `agents/historical_precedent_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: historical_precedent_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An expert agent that searches a curated knowledge base of past market events to find historical analogues. It provides context on how similar events impacted markets in the past. Use this agent to answer questions about historical context or precedents.
instructions: >
  You are an expert in financial history. When a user asks about a past event or a historical comparison, search your knowledge base for the most relevant information and provide a concise summary of the findings.
knowledge_base:
  - historical_market_events_kb
```

### 3.3. Supervisor Agent Configuration

This is the central orchestrator. Its instructions are the most critical part, defining the multi-step reasoning process for generating the final report by delegating tasks to its collaborators and synthesizing their responses. This enhanced version includes logic for handling ambiguity and a more structured, multi-phase approach to report generation.

**File: `agents/impact_assessment_supervisor_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: impact_assessment_supervisor_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An expert financial analysis agent that assesses the impact of market events. It orchestrates data gathering from financial databases, historical analysis from a knowledge base, and news aggregation from external feeds to produce comprehensive preliminary reports for financial analysts.
instructions: >
  Your purpose is to generate a preliminary market event impact report. You must follow a strict, multi-phase process:

  Phase 1: Request Validation & Clarification
  - First, analyze the user's request. If the request is ambiguous about the specific company, ticker, or market sector, you MUST ask for clarification before proceeding. For example, if they mention a company but not a ticker, ask for the ticker.

  Phase 2: Orchestration & Data Collection
  - Once the request is clear, orchestrate your collaborators in a logical sequence.
  - Step 2.1: Delegate to the News Aggregator Agent to get the latest context and headlines. This is always the first data-gathering step.
  - Step 2.2: Based on the event details, delegate to the Financial Data Agent to retrieve relevant company and/or sector performance data.
  - Step 2.3: Concurrently, delegate to the Historical Precedent Agent to find similar past events and their outcomes from its knowledge base.

  Phase 3: Synthesis & Analysis
  - After receiving responses from all collaborators, synthesize the information. Do not just list the outputs. Integrate the findings to form a cohesive analysis.

  Phase 4: Report Generation
  - Format the synthesized information into a single, structured report. The report MUST have the following sections in markdown format:
      ## Preliminary Impact Assessment
      ### 1. Event Summary
      [Briefly describe the event based on the news.]
      ### 2. Key Financial Data
      [Present the data from the Financial Data Agent in a clean format.]
      ### 3. Historical Context & Precedent
      [Summarize the findings from the Historical Precedent Agent, drawing parallels to the current event.]
      ### 4. Preliminary Outlook
      [Provide a brief, synthesized outlook based on all available information.]
collaborators:
  - financial_data_agent      # For retrieving quantitative financial metrics.
  - news_aggregator_agent     # For gathering qualitative context and market sentiment.
  - historical_precedent_agent # For RAG-based analysis of similar past events.
```

## Step 4: Deploy and Run the Solution

Now we will deploy all the components to watsonx Orchestrate using the ADK CLI. The order of operations is critical: tools and knowledge bases must be imported before the agents that depend on them.

### 4.1. Start the Mock API

In a separate terminal, navigate to the project root and start the Flask server. This server must be running for the tools to function correctly.

```bash
# Navigate to the project root directory
cd market_intelligence_orchestrator

# Start the mock API server
python mock_api/app.py
```
You should see output indicating the server is running on `http://127.0.0.1:5001/`.

### 4.2. Import Components with the ADK CLI

In a new terminal, navigate to the project root (`market_intelligence_orchestrator/`) and run the following commands in sequence.

1.  **Import the Tools**:
    ```bash
    orchestrate tools import -f tools/financial_tools.py
    orchestrate tools import -f tools/news_tools.py
    ```

2.  **Import the Knowledge Base**: This step may take a few minutes as the documents are ingested and indexed.
    ```bash
    orchestrate knowledge-bases import -f knowledge_base/historical_market_events_kb.yaml
    ```
    You can check the status with `orchestrate knowledge-bases status --name historical_market_events_kb`. Wait until the status is `Ready`.

3.  **Import the Collaborator Agents**:
    ```bash
    orchestrate agents import -f agents/financial_data_agent.yaml
    orchestrate agents import -f agents/news_aggregator_agent.yaml
    orchestrate agents import -f agents/historical_precedent_agent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/impact_assessment_supervisor_agent.yaml
    ```

## Step 5: Verification and Demo Execution

With all components deployed, you can now interact with the supervisor agent to test the complete workflow and demonstrate its value to the client.

1.  **Start the Chat Interface**:
    ```bash
    orchestrate chat start
    ```
    This will open the watsonx Orchestrate chat in your browser.

2.  **Select the Supervisor Agent**: In the chat UI, ensure you are interacting with the `impact_assessment_supervisor_agent`.

3.  **Run Demo Scenarios**: Use the prompts from the client concept to test the system.

    *   **Scenario 1 (Technology Breakthrough):**
        > "Generate an impact assessment on the semiconductor sector following QuantumLeap Inc.'s announcement of a new fusion-powered processor."

    *   **Scenario 2 (Geopolitical Event):**
        > "What is the preliminary impact of the new trade tariffs on the European automotive industry?"

    *   **Scenario 3 (Supply Chain Disruption):**
        > "Draft a report on the impact of the Suez Canal blockage on global shipping and retail companies."

**Expected Behavior:**
You will see the supervisor agent's thought process in the chat. It will first call the `News Aggregator Agent`, then the `Financial Data Agent`, and the `Historical Precedent Agent`. Finally, it will synthesize their responses into a single, well-structured markdown report as defined in its instructions. If a query is ambiguous, it should first ask for clarification before proceeding.

## Troubleshooting

-   **Tool Not Found Error**: Ensure you have successfully run `orchestrate tools import` for all tool files *before* importing the agents. Verify the tool names in the agent YAML files match the function names in the Python files.
-   **Collaborator Not Found**: Ensure you have imported all collaborator agents *before* importing the supervisor agent. Check for typos in the `collaborators` list in the supervisor's YAML.
-   **API Connection Errors**: Verify that the mock Flask API server is running in a separate terminal and is accessible at `http://127.0.0.1:5001`. Check for any firewall issues blocking local connections.
-   **Knowledge Base Not Ready**: The `orchestrate knowledge-bases import` command can take time. Use `orchestrate knowledge-bases status --name historical_market_events_kb` to confirm the status is "Ready" before testing the `Historical Precedent Agent`.
-   **Incorrect Agent Behavior**: If the supervisor isn't following the steps, review its `instructions` in the YAML file. The clarity and specificity of these instructions are paramount for guiding the LLM's reasoning process. The enhanced, multi-phase instructions in this plan are designed to mitigate this risk.
-   **Agent Fails to Ask for Clarification**: If the agent proceeds with an ambiguous query, its instructions may need to be even more forceful. Try capitalizing keywords like "MUST" or rephrasing the clarification rule to be the absolute first step it considers.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
