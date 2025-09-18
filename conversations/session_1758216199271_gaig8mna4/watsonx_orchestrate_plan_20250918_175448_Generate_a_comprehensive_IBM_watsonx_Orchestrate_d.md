# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 17:54:48
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Market Intelligence Synthesizer

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Market Intelligence Synthesizer" for the client. This solution directly addresses the client's need for an on-demand market event summarizer, transforming a time-consuming manual research process into an automated, intelligent workflow. We will construct a multi-agent system where a supervisor agent intelligently orchestrates specialized collaborator agents and a knowledge base to gather, process, and synthesize external market news and internal analyst data. The final result is a powerful proof-of-concept (POC) that delivers a comprehensive brief in seconds, showcasing the strategic value of IBM watsonx Orchestrate in accelerating time-to-insight and enhancing data synthesis for critical business decisions.

## Prerequisites

Before beginning, ensure your development environment is correctly configured. This plan requires the following setup:

1.  **Python Environment**: A working Python 3.9+ installation is required to create the custom tools.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. If you haven't installed it, run:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
3.  **Active Orchestrate Environment**: You must have an active watsonx Orchestrate environment initialized. You can verify this by running `orchestrate environment list`.
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.

## Step 1: Project Setup and Mock Data Creation

First, we will establish a clean directory structure for our project and create the mock data files needed for the demonstration.

1.  **Create the Project Directory Structure**:
    Open your terminal and execute the following commands to create the necessary folders. This organization separates agents, tools, knowledge bases, and source documents, which is a best practice for managing Orchestrate projects.

    ```bash
    mkdir -p market_intelligence_poc/{agents,tools,knowledge_bases,documents}
    cd market_intelligence_poc
    ```

2.  **Create the Mock Internal Analyst Briefing (PDF)**:
    This document will serve as the proprietary data source for our knowledge base. Create a file named `documents/Internal_Analysis_NVDA_Q4.pdf`. For this demo, you can create a simple text file and save it as a PDF, or use a word processor.

    **File:** `documents/Internal_Analysis_NVDA_Q4.pdf`
    **Content:**
    ```text
    Internal Analyst Briefing: CONFIDENTIAL
    Subject: Analysis of NVIDIA (NVDA) Q4 Earnings Report
    Date: February 22, 2024
    Author: In-House Market Analysis Team

    Key Takeaways:
    - Revenue exceeded expectations by 15%, primarily driven by unprecedented demand in the Data Center segment for our AI and HPC platforms.
    - Gaming division showed a robust recovery, growing 56% year-over-year, indicating strong consumer demand for the 40-series GPUs.
    - Automotive sector revenue saw a slight dip of 4%, which we attribute to broader macroeconomic headwinds affecting vehicle production.

    Strategic Outlook (Internal Opinion):
    Our internal models project a sustained growth trajectory for the next two quarters, contingent on supply chain stability for high-end chip fabrication. We assess the primary risk factor to be increased competition in the AI accelerator market. Our recommendation is to maintain a 'Strong Buy' position, with a revised price target of $950. The public narrative is largely positive, but may underestimate the long-term competitive pressures. We should monitor competitor product announcements closely.
    ```

3.  **Create the `requirements.txt` file**:
    This file lists the Python packages our tools depend on. For this specific POC, our tools only use Python's standard library, so this file will be empty. However, creating it is a best practice for any project, as it standardizes the dependency management workflow.

    **File:** `tools/requirements.txt`
    **Content:**
    ```text
    # No external packages are required for the current version of market_tools.py.
    # This file is included as a best practice for future dependency management.
    ```

## Step 2: Develop the Specialist Tools

The specialist agents rely on tools to perform their actions. We will create two Python functions, decorated with `@tool`, to simulate fetching news and market data. These tools generate realistic synthetic data and include robust error handling, a best practice for building reliable agents.

**File:** `tools/market_tools.py`

```python
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
```

## Step 3: Define the Knowledge Base

The knowledge base provides the agent with secure, grounded access to the client's proprietary internal documents. We will configure it to use the built-in Milvus vector store and ingest our mock PDF, enabling retrieval-augmented generation (RAG).

**File:** `knowledge_bases/internal_analyst_briefs.yaml`

```yaml
spec_version: v1
kind: knowledge_base
name: InternalAnalystBriefs
description: >
   Contains proprietary internal research and analysis briefings on major market events and companies. This knowledge base is the authoritative source for our in-house analyst team's opinions, strategic outlooks, and risk assessments. Use this to answer questions about our "internal take" or "our opinion".
documents:
   - "documents/Internal_Analysis_NVDA_Q4.pdf"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 4: Define the Agent Architecture (YAML Configurations)

Now we define our three agents using YAML files. We will start with the specialist agents and finish with the supervisor agent that orchestrates them. This modular, "separation of concerns" approach is a core IBM pattern for building scalable and maintainable AI solutions.

### Specialist Agent 1: NewsHarvesterAgent

This is a focused, tool-based agent responsible for one task: fetching news. Its description is crucial, as it tells the supervisor agent *when* to use it.

**File:** `agents/news_harvester_agent.yaml`
```yaml
spec_version: v1
kind: native
name: NewsHarvesterAgent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that specializes in fetching recent news articles from public sources. Use this agent when you need to gather qualitative information, public sentiment, or news reports about a specific company and a market event.
instructions: >
  Your sole purpose is to execute the fetch_news_articles tool based on the provided company name and event. Do not attempt to analyze or summarize the news yourself. Simply retrieve and return the data.
tools:
  - fetch_news_articles
```

### Specialist Agent 2: MarketDataAgent

Similar to the news agent, this agent is focused on retrieving quantitative financial data. Its clear description allows the supervisor to delegate data-gathering tasks effectively.

**File:** `agents/market_data_agent.yaml`
```yaml
spec_version: v1
kind: native
name: MarketDataAgent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that specializes in retrieving quantitative stock market data for a given ticker symbol. Use this agent when you need objective financial metrics like stock prices (open, close, high, low) and trading volume.
instructions: >
  Your only job is to run the get_market_data tool with the stock ticker provided. Return the financial data as-is without interpretation.
tools:
  - get_market_data
```

### Supervisor Agent: MarketInsightAgent

This is the "brain" of the operation. It has no tools of its own but uses its collaborators and knowledge base to answer user requests. The `instructions` are the most critical part, defining its reasoning process for synthesizing information from multiple sources.

**File:** `agents/market_insight_agent.yaml`
```yaml
spec_version: v1
kind: native
name: MarketInsightAgent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A supervisor agent for financial market analysis. It can summarize market events by orchestrating other agents to gather public news and quantitative data. It can also consult a knowledge base of internal analyst briefings to provide a proprietary perspective.
instructions: >
    Your purpose is to provide comprehensive, synthesized summaries of market events for financial analysts.
    When a user asks for a summary of an event related to a public company, follow these steps:
    1.  **Deconstruct Request:** Identify the company name(s), stock ticker(s), and the specific market event from the user's query.
    2.  **Gather External Data:** First, delegate to the NewsHarvesterAgent to find relevant news articles. Second, delegate to the MarketDataAgent to get the stock performance data for the relevant ticker.
    3.  **Consult Internal Knowledge:** If the user explicitly mentions an "internal take," "our opinion," "internal analysis," or a similar phrase, you MUST search the InternalAnalystBriefs knowledge base for proprietary insights.
    4.  **Synthesize and Report:** Finally, combine all the gathered information (news summaries, key market data points, and internal analysis if requested) into a single, clear, and concise summary for the user. Present financial data clearly. Start with a high-level summary, then provide the supporting details.
collaborators:
  - NewsHarvesterAgent
  - MarketDataAgent
knowledge_base:
  - InternalAnalystBriefs
```

## Step 5: Deploy the Solution using the ADK CLI

With all our configuration files in place, we will now use the `orchestrate` CLI to deploy the entire solution to your active environment. The order is important: dependencies (tools, knowledge bases, collaborator agents) must be imported before the assets that rely on them.

1.  **Navigate to the project root directory**:
    Ensure your terminal is in the `market_intelligence_poc` directory.

2.  **Install Python Dependencies (Best Practice)**:
    Even though our `requirements.txt` is empty, this step is crucial in a real-world workflow.
    ```bash
    pip install -r tools/requirements.txt
    ```

3.  **Import the Tools**:
    This command registers the Python functions in `market_tools.py` as available tools in Orchestrate.
    ```bash
    orchestrate tools import -k python -f tools/market_tools.py
    ```

4.  **Import the Knowledge Base**:
    This command creates the knowledge base and begins ingesting the specified PDF document into the vector store.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/internal_analyst_briefs.yaml
    ```

5.  **Import the Specialist Agents**:
    These collaborator agents must be imported before the supervisor that orchestrates them.
    ```bash
    orchestrate agents import -f agents/news_harvester_agent.yaml
    orchestrate agents import -f agents/market_data_agent.yaml
    ```

6.  **Import the Supervisor Agent**:
    Finally, import the main agent that ties everything together.
    ```bash
    orchestrate agents import -f agents/market_insight_agent.yaml
    ```

## Step 6: Verification and Demo Scenarios

Now, let's test the complete solution by running through the client's specified demo scenarios. This validates that the agent orchestration, tool execution, and knowledge base retrieval are all functioning as designed.

1.  **Start the Orchestrate Chat**:
    Initiate the interactive chat interface to communicate with your agents.
    ```bash
    orchestrate chat start
    ```

2.  **Select the Supervisor Agent**:
    In the chat interface, you will be prompted to select an agent. Choose `MarketInsightAgent`.

3.  **Run Demo Scenarios**:

    *   **Scenario 1 (Standard Summary):** This tests the basic orchestration of both collaborator agents for external data synthesis.
        **User Prompt:**
        ```
        Give me a summary of the market event around Apple's WWDC keynote yesterday. The ticker is AAPL.
        ```
        **Expected Behavior:** The `MarketInsightAgent` will first call the `NewsHarvesterAgent` with "Apple" and "WWDC keynote". Then, it will call the `MarketDataAgent` with "AAPL". Finally, it will synthesize the news summaries and stock data into a cohesive paragraph.

    *   **Scenario 2 (Comparative Analysis):** This demonstrates the agent's ability to handle more complex, multi-step reasoning for comparative tasks.
        **User Prompt:**
        ```
        How did the market react to the latest earnings from both Google (GOOGL) and Microsoft (MSFT)?
        ```
        **Expected Behavior:** The `MarketInsightAgent` should intelligently loop through the request. It will run the news and data gathering workflow for Google, then repeat the entire process for Microsoft. The final output will be a comparative summary of the results for both companies.

    *   **Scenario 3 (Internal + External Synthesis):** This is the key scenario showcasing the full power of the solution by combining external data with internal, proprietary knowledge (RAG).
        **User Prompt:**
        ```
        What is our internal take on the Nvidia Q4 earnings, and how does it compare to public news reports? Ticker is NVDA.
        ```
        **Expected Behavior:** Because the prompt includes "internal take," the `MarketInsightAgent` will trigger all three information sources. It will call `NewsHarvesterAgent` and `MarketDataAgent` for external data, AND it will query the `InternalAnalystBriefs` knowledge base. The final answer will be a rich synthesis, contrasting the public news with the confidential internal analysis from the PDF.

## Troubleshooting

-   **`Tool not found` error during agent import**: This usually means you forgot to run `orchestrate tools import ...` before importing an agent that uses the tool. Re-run the tool import command.
-   **`Collaborator not found` error during supervisor import**: The specialist agents (`NewsHarvesterAgent`, `MarketDataAgent`) must be imported *before* the `MarketInsightAgent`. Ensure you are following the import order in Step 5.
-   **Agent is not using the correct tool/collaborator**: This is often an issue with the `description` of the tool/agent or the `instructions` in the supervisor. Ensure descriptions are clear and specific, and instructions provide unambiguous guidance on when to use each component. For example, explicitly state "Use NewsHarvesterAgent to find news."
-   **Knowledge Base returns no results**: Check that the file path in `internal_analyst_briefs.yaml` is correct relative to where you are running the command. Also, ensure the content of your PDF contains keywords from your query (e.g., "Nvidia", "internal").
-   **Tool returns an error object**: Check the terminal logs where you ran `orchestrate chat start`. The `print()` statements within the tool's `except` block will provide details on the failure.

## Best Practices

-   **Descriptive Naming and Descriptions**: The names (`MarketDataAgent`) and descriptions of agents and tools are not just for humans; they are critical inputs for the supervisor agent's LLM to decide how to route tasks. Be clear, specific, and action-oriented in your descriptions.
-   **Explicit Instructions**: The `instructions` for a supervisor agent should act as a "Standard Operating Procedure." Guide the agent's reasoning process with clear, sequential steps (e.g., "First, do X. Second, do Y. If Z happens, then do A."). This reduces ambiguity and improves performance.
-   **Modular, Single-Purpose Agents**: The specialist agents (`NewsHarvesterAgent`, `MarketDataAgent`) are effective because they do one thing well. This "separation of concerns" makes the system easier to build, test, and extend. To add a new data source (e.g., social media), you simply build a new specialist agent and add it to the supervisor's `collaborators` list.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
