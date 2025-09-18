# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 17:16:05
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered SEC Filing Risk Intelligence

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an "AI-Powered SEC Filing Risk Intelligence" demonstration using IBM watsonx Orchestrate. The solution is tailored to the client's specific need to automate the time-intensive process of analyzing SEC filings for potential risks. By creating a multi-agent system, we will demonstrate how watsonx Orchestrate can orchestrate complex workflows, integrate with document repositories using Retrieval-Augmented Generation (RAG), and execute custom actions. The final demo will showcase a seamless process: from a user's natural language request to analyze a filing, to the automated extraction and summarization of risks, and finally to the distribution of an intelligence report via email. This directly addresses the client's goal of achieving a 30-50% reduction in manual analysis effort, enabling their risk management teams to focus on strategic mitigation rather than tedious data extraction.

## Prerequisites

Before beginning the implementation, ensure your environment is correctly set up. This is crucial for the successful deployment and execution of the agents and tools.

1.  **Python Environment**: A working Python installation (version 3.10 or later) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. If not, install it using pip:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active IBM watsonx Orchestrate environment configured. Initialize it if you haven't already:
    ```bash
    orchestrate env init
    ```
4.  **Mock Data Files**: The demo relies on synthetic SEC filings. These files must be created and placed in a designated directory before running the import commands.

## Step 1: Project Structure Setup

A well-organized project structure is essential for managing the different components of the solution. Create the following directory structure in your workspace:

```
sec_risk_demo/
├── agents/
│   ├── SEC_Risk_Orchestrator_Agent.yaml
│   ├── Filing_Analysis_Agent.yaml
│   └── Risk_Reporting_Agent.yaml
├── tools/
│   └── reporting_tools.py
├── knowledge_base/
│   └── sec_filings_kb.yaml
├── mock_data/
│   ├── innovatech_ai_10k.txt
│   └── global_logistics_10k.txt
└── requirements.txt
```

## Step 2: Prepare Mock Data and Knowledge Base

The foundation of this demo is the ability to analyze documents. We will create mock SEC filing excerpts and configure a knowledge base to make them accessible to our analysis agent.

### 2.1 Create Mock SEC Filing Data

Create the two text files inside the `mock_data/` directory with the following content. This synthetic data provides a realistic basis for the RAG agent to perform its analysis.

**File: `mock_data/innovatech_ai_10k.txt`**
```text
Company: Innovatech AI Corp
Filing Type: 10-K Annual Report

Item 1A. Risk Factors

Market Risks: Our industry is characterized by rapid technological change, intense competition, and evolving industry standards. Our success depends on our ability to adapt to these changes. Failure to anticipate or respond to new developments could have a material adverse effect on our business. We face significant competition from established technology companies and numerous startups.

Regulatory Risks: We are subject to a wide range of laws and regulations, including those related to data privacy and security. Changes in these laws, such as the implementation of new AI-specific regulations, could increase our compliance costs and impact our product development. Non-compliance could result in significant fines and reputational damage.

Operational Risks: Our business relies on complex cloud infrastructure and third-party data centers. Any disruption to these services, whether from technical failures, natural disasters, or cyber-attacks, could interrupt our operations and harm our brand. We also depend on a highly skilled workforce, and the inability to attract and retain key personnel could hinder our growth.
```

**File: `mock_data/global_logistics_10k.txt`**
```text
Company: Global Logistics Inc.
Filing Type: 10-K Annual Report

Item 1A. Risk Factors

Market Risks: Our financial performance is highly dependent on global economic conditions. A downturn in international trade, increased fuel costs, or shifts in consumer spending could significantly reduce demand for our shipping and logistics services.

Regulatory Risks: The transportation industry is heavily regulated by government agencies worldwide. We are subject to complex regulations concerning safety, environmental protection, and international trade tariffs. New tariffs or trade restrictions could disrupt our supply chains and increase operational costs.

Operational Risks: Our operations are subject to risks including port closures, labor disputes, and transportation accidents. Our reliance on a global network of partners and carriers exposes us to their operational failures. Furthermore, our information technology systems are critical to managing our fleet and customer shipments; a cybersecurity breach could lead to significant financial loss and business disruption.
```

### 2.2 Configure the Knowledge Base

The knowledge base will ingest our mock documents, making them searchable for the `Filing_Analysis_Agent`. This YAML configuration uses the built-in Milvus vector store provided by watsonx Orchestrate.

**File: `knowledge_base/sec_filings_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: sec_filings_kb
description: >
  A knowledge base containing SEC 10-K filings for public companies. It is used by agents to identify, analyze, and extract stated risk factors from financial documents.
documents:
  - "mock_data/innovatech_ai_10k.txt"
  - "mock_data/global_logistics_10k.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Develop Custom Tools

The `Risk_Reporting_Agent` requires a custom tool to perform its function of sending email reports. We will create this tool using the ADK's Python `@tool` decorator.

### 3.1 Create the Reporting Tool

This Python script defines the `send_risk_report_email` tool. For this demo, the tool simulates sending an email by printing the recipient and body to the console. In a production environment, this function would contain logic to integrate with an actual email service (e.g., SendGrid, Microsoft Graph API).

**File: `tools/reporting_tools.py`**
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from pydantic import BaseModel, Field
import datetime

# Although not strictly required by Pydantic for this simple tool,
# including all imports is a best practice.
import json

@tool(name="send_risk_report_email", permission=ToolPermission.ADMIN)
def send_risk_report_email(recipient_email: str, report_summary: str) -> str:
    """
    Sends a summarized risk report to a specified email address. This tool is used by the reporting agent to distribute the final analysis.

    Args:
        recipient_email (str): The email address of the recipient (e.g., 'risk-team@example.com').
        report_summary (str): The content of the risk summary report to be included in the email body.

    Returns:
        str: A confirmation message indicating the email was sent successfully or an error occurred.
    """
    print("--- SIMULATING EMAIL DISPATCH ---")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    print(f"Recipient: {recipient_email}")
    print(f"Email Body:\n{report_summary}")
    print("---------------------------------")
    
    # Basic validation for the demo
    if not recipient_email or "@" not in recipient_email:
        return f"Error: Invalid recipient email address provided: {recipient_email}."
    if not report_summary:
        return "Error: Report summary is empty. Cannot send email."

    return f"Successfully sent risk report to {recipient_email}."

```

### 3.2 Create Requirements File

Create a `requirements.txt` file in the root directory. While our tool has no external dependencies, this file is good practice for any project.

**File: `requirements.txt`**
```text
# No external packages are required for this basic tool implementation.
# If using packages like 'requests', add them here.
```

## Step 4: Define the Agent Architecture

Now we define our three agents using YAML configuration files. This architecture implements the Supervisor/Collaborator pattern, with specialized agents for analysis and reporting.

### 4.1 `Filing_Analysis_Agent` (RAG Agent)

This agent's sole purpose is to interact with the knowledge base. Its description is critical, as it tells the supervisor agent *when* to delegate document-related tasks to it.

**File: `agents/Filing_Analysis_Agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Filing_Analysis_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent for interacting with a repository of financial documents like SEC filings. Use this agent for any task that involves searching, retrieving, reading, or extracting specific information, such as risk factors, from the sec_filings_kb knowledge base.
instructions: >
  Your only function is to answer questions based on the content within the provided knowledge base of SEC filings. Be precise and only use information from the documents. Do not invent information.
knowledge_base:
  - sec_filings_kb
```

### 4.2 `Risk_Reporting_Agent` (Execution Agent)

This agent is responsible for the final step: communication. It is equipped with the `send_risk_report_email` tool.

**File: `agents/Risk_Reporting_Agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Risk_Reporting_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An execution-focused agent that handles outbound communications. Use this agent specifically for tasks involving sending finalized reports or summaries to stakeholders via email.
instructions: >
  Your purpose is to send reports. When asked to send a report, use the send_risk_report_email tool. You must be provided with a recipient email address and the report content.
tools:
  - send_risk_report_email
```

### 4.3 `SEC_Risk_Orchestrator_Agent` (Supervisor Agent)

This is the main agent that the user interacts with. It coordinates the workflow between its collaborators, synthesizes information using its LLM, and manages the overall task. The instructions are detailed to guide its reasoning process.

**File: `agents/SEC_Risk_Orchestrator_Agent.yaml`**
```yaml
spec_version: v1
kind: native
name: SEC_Risk_Orchestrator_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A supervisor agent that manages the end-to-end analysis of SEC filings. It coordinates with collaborator agents to find risk information in documents and to send email reports. It can synthesize information from multiple sources to create comprehensive summaries.
instructions: >
  Persona:
  - You are an expert financial risk analyst assistant. Your purpose is to orchestrate the analysis of SEC filings to identify and summarize key risk factors.

  Reasoning:
  - For any user request that requires searching, reading, extracting information, or answering questions about a financial document, you MUST delegate the task to the Filing_Analysis_Agent.
  - For any user request that involves sending a completed summary or report via email, you MUST delegate the task to the Risk_Reporting_Agent.
  - If a user asks for a comparative analysis between two documents, you must first use the Filing_Analysis_Agent to get information from each document separately, then synthesize the findings into a single comparative summary yourself.
  - After generating a summary, confirm with the user if they wish to send it as a report before engaging the Risk_Reporting_Agent.
collaborators:
  - Filing_Analysis_Agent
  - Risk_Reporting_Agent
```

## Step 5: Deploy the Solution using the ADK CLI

With all configuration files in place, we will now use the `orchestrate` CLI to import the components into the watsonx Orchestrate environment. The order of these commands is important to ensure dependencies are met.

Execute these commands from the root directory of your project (`sec_risk_demo/`).

1.  **Import the Custom Tool:**
    ```bash
    orchestrate tools import -k python -f tools/reporting_tools.py
    ```

2.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge_bases import -f knowledge_base/sec_filings_kb.yaml
    ```

3.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/Filing_Analysis_Agent.yaml
    orchestrate agents import -f agents/Risk_Reporting_Agent.yaml
    ```

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/SEC_Risk_Orchestrator_Agent.yaml
    ```

## Step 6: Verification and Demo Scenarios

After successfully importing all components, you can test the solution using the Orchestrate chat interface.

**Start the Chat:**
```bash
orchestrate chat start
```
This will open a web-based chat interface. Select the `SEC_Risk_Orchestrator_Agent` to begin.

---

### **Scenario 1: End-to-End Risk Summary**

This scenario demonstrates the full, seamless workflow from request to simulated email delivery.

*   **User Prompt:**
    > "Analyze the 10-K for Innovatech AI Corp, generate a summary of the key risks, and send it to risk-management@example.com."

*   **Expected Behavior:**
    1.  The `SEC_Risk_Orchestrator_Agent` receives the request.
    2.  It delegates the analysis task to `Filing_Analysis_Agent`, which queries the knowledge base for "Innovatech AI Corp" risks.
    3.  `Filing_Analysis_Agent` returns the market, regulatory, and operational risks.
    4.  `SEC_Risk_Orchestrator_Agent` synthesizes this information into a concise summary.
    5.  It then delegates the reporting task to `Risk_Reporting_Agent`, providing the recipient email and the summary.
    6.  `Risk_Reporting_Agent` calls the `send_risk_report_email` tool.
    7.  You will see the simulated email output in your terminal, and the agent will confirm the action in the chat.

---

### **Scenario 2: Specific Risk Categorization**

This showcases the `Filing_Analysis_Agent`'s ability to perform targeted information extraction.

*   **User Prompt:**
    > "What are the primary regulatory risks mentioned in the Global Logistics Inc. filing?"

*   **Expected Behavior:**
    1.  The `SEC_Risk_Orchestrator_Agent` understands the query is about a specific document.
    2.  It delegates the task to `Filing_Analysis_Agent`.
    3.  `Filing_Analysis_Agent` searches the knowledge base for "Global Logistics Inc." and filters for "regulatory risks."
    4.  It returns the specific text about regulations in the transportation industry, safety, environment, and tariffs.
    5.  The orchestrator presents this information directly to the user.

---

### **Scenario 3: Comparative Analysis**

This highlights the supervisor agent's advanced reasoning and synthesis capabilities.

*   **User Prompt:**
    > "Compare the operational risks for Innovatech AI Corp and Global Logistics Inc. and generate a report."

*   **Expected Behavior:**
    1.  The `SEC_Risk_Orchestrator_Agent` recognizes the need for a two-step analysis.
    2.  **First Delegation:** It asks `Filing_Analysis_Agent` for the operational risks of "Innovatech AI Corp."
    3.  **Second Delegation:** It asks `Filing_Analysis_Agent` for the operational risks of "Global Logistics Inc."
    4.  **Synthesis:** The `SEC_Risk_Orchestrator_Agent` receives both sets of risks and uses its own LLM to create a new, comparative summary highlighting similarities (e.g., reliance on infrastructure/IT) and differences.
    5.  It presents the comparative report to the user in the chat.

## Troubleshooting

-   **`Agent not found` Error during Import**: This typically happens if you import a supervisor before its collaborators. Ensure you import `Filing_Analysis_Agent` and `Risk_Reporting_Agent` *before* `SEC_Risk_Orchestrator_Agent`.
-   **`Tool not found` Error during Import**: The agent's YAML file references a tool that hasn't been imported yet. Always run `orchestrate tools import` before importing agents that depend on those tools.
-   **Knowledge Base Search Fails**: Verify that the file paths in `sec_filings_kb.yaml` are correct relative to where you are running the `orchestrate` command. Ensure the `mock_data` files are not empty.
-   **Incorrect Agent Routing**: If the supervisor agent tries to answer a document question itself instead of delegating, refine the `description` of the `Filing_Analysis_Agent` to be more explicit about its capabilities. Also, strengthen the `instructions` in the `SEC_Risk_Orchestrator_Agent` to be more direct about when to delegate.

## Best Practices

-   **Descriptive Agent Descriptions**: The supervisor agent relies heavily on the `description` of its collaborators to make routing decisions. Make these descriptions clear, concise, and capability-focused. Mention the specific tasks and knowledge areas the agent handles.
-   **Explicit Instructions**: For supervisor agents, the `instructions` section is paramount. Use clear, direct language to define the rules of delegation and reasoning, as demonstrated in the `SEC_Risk_Orchestrator_Agent`.
-   **Modular and Specialized Agents**: The power of this pattern lies in creating agents with distinct, specialized roles (e.g., one for analysis, one for reporting). This makes the system easier to build, debug, and extend.
-   **Iterative Development**: Start with a single agent and a single tool. Once it's working, build out the collaborator agents and the supervisor. The ADK makes it easy to update existing agents by simply re-running the `import` command.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
