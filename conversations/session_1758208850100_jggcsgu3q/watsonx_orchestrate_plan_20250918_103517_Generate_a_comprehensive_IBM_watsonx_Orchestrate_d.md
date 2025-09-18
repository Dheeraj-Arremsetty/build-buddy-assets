# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 10:35:17
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered ESG Intelligence Engine

## Overview

This execution plan provides a comprehensive, step-by-step guide for building and demonstrating an **AI-Powered ESG Intelligence Engine** using IBM watsonx Orchestrate. This solution is specifically tailored to the client's need to automate the analysis of corporate Environmental, Social, and Governance (ESG) reports. The plan details the creation of a sophisticated multi-agent system that transforms dense, unstructured PDF reports into an interactive, conversational knowledge source.

The core business value is the dramatic acceleration of the financial analyst's workflow. By leveraging a supervisor agent to orchestrate tasks between a specialized document analysis agent (using Retrieval-Augmented Generation - RAG) and a content formatting agent, this demo will showcase how watsonx Orchestrate can reduce research time from hours to seconds, improve the accuracy of data extraction, and enable analysts to deliver rapid, source-verified insights to their clients.

## Prerequisites

Before beginning, ensure your environment is correctly configured.

1.  **IBM watsonx Orchestrate ADK:** The Agent Development Kit (ADK) must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
2.  **Python Environment:** A working Python environment (3.9 or higher) is required to create custom tools.
3.  **Project Directory Structure:** Create a dedicated directory for the project to keep all assets organized.

    ```bash
    mkdir esg_intelligence_engine
    cd esg_intelligence_engine
    mkdir agents
    mkdir tools
    mkdir mock_data
    ```

4.  **Required Python Packages:** Create a `requirements.txt` file in the root directory. For this project, no external libraries are needed for the tool itself, but it's a best practice to have the file.

    **File: `requirements.txt`**
    ```
    # No external packages are required for this specific tool,
    # but this file should be present for future scalability.
    # If using packages like 'requests' or 'pandas', add them here.
    ```

## Step 1: Prepare Mock Data and Knowledge Base

The foundation of the RAG pattern is a high-quality knowledge base. We will create synthetic ESG reports in PDF format and define a knowledge base configuration to ingest them.

### 1.1 Create Synthetic ESG Reports

Create three separate PDF documents with plausible but fictional ESG data. Place these files in the `mock_data/` directory.

*   `mock_data/Global_Innovations_ESG_2023.pdf`
*   `mock_data/EcoSolutions_ESG_2023.pdf`
*   `mock_data/FutureForward_Corp_ESG_2023.pdf`

**Example Content for `Global_Innovations_ESG_2023.pdf`:**

> **Global Innovations Inc. - 2023 ESG Report**
>
> **Section 1: Water Stewardship**
> Global Innovations Inc. is committed to responsible water management. Our primary goal is to achieve a 25% reduction in total water consumption across all manufacturing facilities by 2030, against a 2022 baseline.
>
> **Section 2: Carbon Emissions Targets**
> We have set an ambitious target to reduce our Scope 1 and Scope 2 greenhouse gas emissions by 40% by 2035. In 2023, our Scope 1 emissions were 150,000 metric tons of CO2 equivalent.
>
> **Section 3: Board Diversity Policies**
> Our board of directors reflects our commitment to diversity. We have a policy to maintain at least 40% female representation and 20% representation from underrepresented ethnic groups on our board.

*(Create similar distinct content for EcoSolutions Ltd. and FutureForward Corp.)*

### 1.2 Create the Knowledge Base YAML Configuration

This file tells Orchestrate to ingest the specified PDFs into a built-in Milvus vector database, using the default IBM Slate embedding model.

**File: `esg_knowledge_base.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: Corporate_ESG_Reports_KB
description: >
   Contains official PDF sustainability and ESG reports for publicly traded companies including Global Innovations Inc., EcoSolutions Ltd., and FutureForward Corp. 
   Use this to answer questions about environmental goals (like water usage and carbon emissions), social policies, and governance structures (like board diversity).
documents:
   - "mock_data/Global_Innovations_ESG_2023.pdf"
   - "mock_data/EcoSolutions_ESG_2023.pdf"
   - "mock_data/FutureForward_Corp_ESG_2023.pdf"
vector_index:
   # Using the default high-performance IBM model for document retrieval
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Create the Custom Formatting Tool

The `ESG_Briefing_Generator` agent requires a custom tool to format raw text into a professional briefing note. We will create this using a Python file with the `@tool` decorator.

### Business Value & Explanation

The `format_esg_summary` tool provides a crucial "last-mile" service. While the RAG agent is excellent at *finding* information, this tool ensures the information is *presented* in a structured, client-ready format. This adds significant value by standardizing the output, reducing the manual effort for analysts to clean up raw text, and ensuring consistency in client deliverables. It demonstrates how Orchestrate can seamlessly blend AI-driven retrieval with deterministic, rule-based formatting.

**File: `tools/esg_briefing_tool.py`**
```python
# tools/esg_briefing_tool.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission
import datetime

@tool(name="format_esg_summary", permission=ToolPermission.ADMIN)
def format_esg_summary(raw_text: str, company_name: str, topic: str) -> str:
    """
    Formats raw text about a company's ESG policy into a structured briefing note.
    This tool is ideal for taking unstructured paragraphs and presenting them in a professional,
    easy-to-read markdown format suitable for client reports or internal summaries.

    Args:
        raw_text (str): The unstructured text retrieved from the ESG report. This is typically the direct output from a knowledge base search.
        company_name (str): The name of the company being analyzed (e.g., 'EcoSolutions Ltd.').
        topic (str): The specific ESG topic (e.g., 'Carbon Emissions Targets', 'Board Diversity').

    Returns:
        str: A professionally formatted markdown string for the briefing note, including a header, key findings, and a footer.
    """
    try:
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        
        header = f"## ESG Briefing Note: {company_name} - {topic}\n"
        header += f"**Date:** {current_date}\n\n"
        
        body = f"**Key Findings:**\n> {raw_text.strip()}\n\n"
        
        footer = "---\n*Generated by watsonx Orchestrate ESG Intelligence Engine.*"
        
        return header + body + footer
    except Exception as e:
        # Basic error handling
        return f"Error formatting summary: {str(e)}"

```

## Step 3: Define the Agent Architecture

We will now define the three agents as described in the client concept. Each agent has a specific role, and their descriptions and instructions are critical for the supervisor agent to route tasks correctly.

### 3.1 `ESG_Report_Analyst` (RAG Agent)

This agent is the specialist for querying the knowledge base. Its sole purpose is to find accurate information within the ESG reports.

**File: `agents/ESG_Report_Analyst.yaml`**
```yaml
spec_version: v1
kind: native
name: ESG_Report_Analyst
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An expert agent that specializes in searching and retrieving specific data points from a knowledge base of corporate ESG reports. 
    Use this agent to answer direct questions about environmental policies, social metrics, and governance details. 
    It reads PDF documents to find precise, factual information.
instructions: >
    Your sole purpose is to answer questions using the provided Corporate_ESG_Reports_KB knowledge base.
    1. Carefully analyze the user's query to identify the company name and the specific ESG topic.
    2. Search the knowledge base for the most relevant information.
    3. Provide a concise, factual answer based ONLY on the information retrieved from the documents.
    4. Do not infer information or answer from general knowledge. If the information is not in the documents, state that clearly.
collaborators: []
tools: []
knowledge_base:
  - Corporate_ESG_Reports_KB
```

### 3.2 `ESG_Briefing_Generator` (Formatting Agent)

This agent uses the custom tool we created to format text. Its description clearly states its capability, allowing the supervisor to delegate formatting tasks to it.

**File: `agents/ESG_Briefing_Generator.yaml`**
```yaml
spec_version: v1
kind: native
name: ESG_Briefing_Generator
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialist agent that takes raw text and formats it into a professional, structured briefing note or summary. 
    Use this agent when a user asks for the output to be presented in a formal document, note, or summary format.
instructions: >
    Your purpose is to create well-structured briefing notes.
    1. You will receive raw text, a company name, and a topic.
    2. Use the 'format_esg_summary' tool to structure this information.
    3. Present the formatted output from the tool directly to the user.
collaborators: []
tools:
  - format_esg_summary
knowledge_base: []
```

### 3.3 `ESG_Inquiry_Supervisor` (Supervisor Agent)

This is the user-facing agent. It interprets the user's intent and orchestrates the workflow between its collaborators. The instructions are key to its reasoning process.

**File: `agents/ESG_Inquiry_Supervisor.yaml`**
```yaml
spec_version: v1
kind: native
name: ESG_Inquiry_Supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A supervisor agent for financial analysts. It understands natural language questions about Environmental, Social, and Governance (ESG) policies. 
    It collaborates with other specialist agents to find specific data in ESG reports and to format that data into professional briefings. 
    This is the primary agent to interact with for all ESG-related inquiries.
instructions: >
    You are an AI assistant for financial analysts specializing in ESG research. Your goal is to provide accurate and well-formatted answers.

    Reasoning Steps:
    1.  **Analyze Intent:** First, determine the user's primary goal. Are they asking for a specific piece of data, or do they want a formatted output like a "briefing note", "summary", or "report"?

    2.  **Data Retrieval:** For ANY question that requires information from an ESG report, you MUST first delegate the task to the `ESG_Report_Analyst` agent. This agent is the expert at finding factual data.

    3.  **Formatting Logic:**
        - If the user's request explicitly contains keywords like "format", "briefing note", "summary", "note for a client", or "formal brief", you must perform a two-step process:
            a. First, use the `ESG_Report_Analyst` to get the raw data.
            b. Second, pass the raw data you received from the analyst to the `ESG_Briefing_Generator` agent to format it correctly.
        - If the user's request is a direct question without any formatting keywords, simply use the `ESG_Report_Analyst` and return its answer directly.
collaborators:
  - ESG_Report_Analyst
  - ESG_Briefing_Generator
tools: []
knowledge_base: []
```

## Step 4: Import Assets and Run the Demo

With all configuration files in place, use the ADK CLI to import the components into watsonx Orchestrate in the correct order.

### Import Commands

Execute these commands from the root of your `esg_intelligence_engine` directory.

1.  **Import the Knowledge Base:** This process will start the ingestion of the PDFs. It may take a few minutes.
    ```bash
    orchestrate knowledge-bases import -f esg_knowledge_base.yaml
    ```

2.  **Import the Custom Tool:** Make the formatting tool available to agents.
    ```bash
    orchestrate tools import -f tools/esg_briefing_tool.py
    ```

3.  **Import the Agents:** Import the collaborator agents first, followed by the supervisor.
    ```bash
    # Import the specialist agents
    orchestrate agents import -f agents/ESG_Report_Analyst.yaml
    orchestrate agents import -f agents/ESG_Briefing_Generator.yaml

    # Import the main supervisor agent
    orchestrate agents import -f agents/ESG_Inquiry_Supervisor.yaml
    ```

4.  **Start the Chat:** Launch the interactive chat interface to begin the demo.
    ```bash
    orchestrate chat start
    ```

## Verification: Demo Scenarios

Once the chat is running, select the `ESG_Inquiry_Supervisor` agent and use the following prompts to demonstrate the defined scenarios.

#### Scenario 1: Specific Data Point Retrieval
This tests the supervisor's ability to route a simple query to the RAG agent.

*   **User Query:**
    > "What are Global Innovations Inc.'s goals for water usage reduction?"

*   **Expected Behavior:**
    1.  The `ESG_Inquiry_Supervisor` receives the query.
    2.  It determines the need for data retrieval and delegates to `ESG_Report_Analyst`.
    3.  `ESG_Report_Analyst` searches `Corporate_ESG_Reports_KB`, finds the relevant text in the `Global_Innovations_ESG_2023.pdf`.
    4.  It returns a concise answer like: "Global Innovations Inc.'s goal is to achieve a 25% reduction in total water consumption across all manufacturing facilities by 2030, against a 2022 baseline."

#### Scenario 2: Comparative Analysis
This showcases the LLM's ability to synthesize information retrieved from multiple documents via the RAG agent.

*   **User Query:**
    > "Compare the board diversity policies of EcoSolutions and FutureForward Corp."

*   **Expected Behavior:**
    1.  `ESG_Inquiry_Supervisor` delegates to `ESG_Report_Analyst`.
    2.  `ESG_Report_Analyst` queries the knowledge base, retrieving the board diversity sections from both the `EcoSolutions` and `FutureForward` PDFs.
    3.  The agent's LLM synthesizes the retrieved contexts into a comparative summary, highlighting the key policies and targets of each company.

#### Scenario 3: Formatted Briefing Generation
This demonstrates the full, multi-step orchestration power of the supervisor agent.

*   **User Query:**
    > "Generate a formal briefing note on EcoSolutions' carbon emissions targets for a client."

*   **Expected Behavior:**
    1.  `ESG_Inquiry_Supervisor` detects the keywords "formal briefing note".
    2.  **Step 1:** It first calls `ESG_Report_Analyst` with the core question: "What are EcoSolutions' carbon emissions targets?".
    3.  `ESG_Report_Analyst` retrieves the relevant data and returns the raw text.
    4.  **Step 2:** The supervisor takes this raw text and calls `ESG_Briefing_Generator`, passing the text, company name ("EcoSolutions"), and topic ("Carbon Emissions Targets").
    5.  `ESG_Briefing_Generator` executes its `format_esg_summary` tool.
    6.  The final, beautifully formatted markdown output is returned to the user.

## Troubleshooting

*   **Issue:** Agent cannot find information that is known to be in the PDF.
    *   **Solution:** The knowledge base may still be indexing. Run `orchestrate knowledge-bases status --name Corporate_ESG_Reports_KB` to check if the `Ready` property is true. PDF parsing can also be complex; ensure the text in the PDF is selectable and not just an image.
*   **Issue:** Supervisor agent fails to delegate to the correct collaborator.
    *   **Solution:** This is almost always an issue with the `description` or `instructions`. Ensure the descriptions of the collaborator agents are extremely clear and distinct. Refine the supervisor's instructions to be more explicit about the routing logic, as shown in the examples.
*   **Issue:** Tool import fails with an error.
    *   **Solution:** Check the Python code for syntax errors. Ensure all required imports are at the top of the file and that the function is correctly decorated with `@tool`.
*   **Issue:** The RAG agent provides an answer but it's not from the document (hallucination).
    *   **Solution:** The instructions for the `ESG_Report_Analyst` are critical here. The prompt "Provide a concise, factual answer based ONLY on the information retrieved from the documents" helps mitigate this. Using a high-quality, instruction-tuned model like `ibm/granite-3-8b-instruct` also improves factuality.

## Best Practices

*   **Descriptive Naming:** Use clear, descriptive names for agents, tools, and knowledge bases (e.g., `Corporate_ESG_Reports_KB` instead of `kb1`). This is crucial for maintainability and for the supervisor's ability to reason.
*   **Atomicity of Agents:** Design agents to be specialists in one area. The `ESG_Report_Analyst` only does retrieval. The `ESG_Briefing_Generator` only does formatting. This makes the system more robust and easier to debug.
*   **Instructional Clarity:** The quality of the `instructions` in the supervisor's YAML directly impacts its performance. Use clear, direct language and provide explicit reasoning steps for how it should choose between collaborators.
*   **Source Citation:** For a production system, enhance the `ESG_Report_Analyst` instructions to include the source document name in its response. This builds trust and allows for easy verification by the analyst.
*   **Iterative Development:** Start with a simple, single-agent RAG setup. Once that works, add the formatting tool and agent. Finally, add the supervisor on top. This layered approach simplifies development and testing.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
