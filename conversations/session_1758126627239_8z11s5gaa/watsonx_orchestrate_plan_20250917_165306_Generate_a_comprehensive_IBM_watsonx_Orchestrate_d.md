# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 16:53:06
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Sales Co-pilot

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Xerox Sales Co-pilot," an AI-powered proposal automation solution using IBM watsonx Orchestrate. The plan is tailored specifically for the Xerox demo concept, which aims to accelerate the sales cycle for complex, services-led offerings. By leveraging a multi-agent architecture, this solution automates the manual, time-consuming process of creating sales proposals. It intelligently orchestrates data retrieval from a mock Salesforce instance and content generation from an internal service catalog, enabling the Xerox sales team to produce accurate, customer-specific documents in minutes instead of hours.

The core of this solution is a supervisor agent that delegates tasks to specialized collaborator agents: one for fetching customer data and another for generating proposal content using a knowledge base. This design pattern showcases the power of watsonx Orchestrate to integrate with enterprise systems, reason over unstructured content using Retrieval-Augmented Generation (RAG), and execute custom business logic, directly addressing Xerox's strategic goal of enhancing sales velocity and productivity.

## Prerequisites
Before beginning, ensure your environment is set up with the following components. This setup is crucial for the successful creation, deployment, and testing of the agent ecosystem.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. This is the primary tool for building, importing, and managing agents, tools, and knowledge bases.
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
2.  **Python Environment**: A Python 3.9+ environment is required to run the mock Salesforce API and execute the Python-based tool.
3.  **Project Directory**: Create a dedicated project directory to organize all configuration files, tools, and mock data.
    ```bash
    mkdir xerox_sales_copilot
    cd xerox_sales_copilot
    mkdir agents tools mock_docs
    ```
4.  **Python Libraries**: Install the necessary Python libraries for the mock API.
    ```bash
    pip install Flask
    ```
5.  **`requirements.txt` file**: Create a `requirements.txt` file in the root of your project directory for dependency management.
    ```text
    # requirements.txt
    ibm-watsonx-orchestrate
    Flask
    ```

## Step 1: Create Mock Data and Services

To simulate a real-world enterprise environment, we will create mock service documents for the knowledge base and a mock Salesforce REST API for customer data retrieval.

### 1.1. Create Mock Service Catalog Documents
These documents will be ingested into a watsonx Orchestrate knowledge base, allowing the `Proposal_Generation_Agent` to perform semantic searches for service details.

**File: `mock_docs/Managed_Print_Services.pdf`**
(Create a simple PDF document with the following text)
> **Xerox Managed Print Services (MPS)**
> Our comprehensive MPS solution streamlines print operations, reduces costs, and enhances document security.
> **Features:**
> -   Automated supply replenishment
> -   Proactive device monitoring and maintenance
> -   Fleet optimization and right-sizing
> -   Secure print release and access control
> **Pricing Tiers:**
> -   Standard: $50/user/month
> -   Premium: $75/user/month (includes advanced security)

**File: `mock_docs/IT_Outsourcing_Solutions.txt`**
> **Xerox IT Outsourcing (ITO) Solutions**
> We provide end-to-end IT management, allowing you to focus on your core business.
> **Services Offered:**
> -   24/7 Help Desk and Technical Support
> -   Network Infrastructure Management
> -   Cloud Services and Migration
> -   Cybersecurity and Compliance
> **Standard Terms:** 12-month minimum contract.

**File: `mock_docs/Digital_Transformation_Services.txt`**
> **Xerox Digital Transformation Services**
> Accelerate your digital journey with our expert consulting and implementation services.
> **Capabilities:**
> -   Workflow Automation and Process Re-engineering
> -   Document Digitization and Management
> -   Custom Application Development
> -   Data Analytics and Business Intelligence

### 1.2. Create the Mock Salesforce API
This simple Flask application will simulate a Salesforce REST API, serving customer data. This is essential for demonstrating the `Salesforce_Data_Agent`'s ability to connect to external systems via OpenAPI.

**File: `tools/mock_salesforce_api.py`**
```python
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Realistic synthetic customer data
mock_db = {
    "Global Tech Inc.": {
        "id": "acc001",
        "name": "Global Tech Inc.",
        "contactPerson": "Jane Doe",
        "address": "123 Tech Park, Silicon Valley, CA 94001",
        "industry": "Technology",
    },
    "Innovate Solutions": {
        "id": "acc002",
        "name": "Innovate Solutions",
        "contactPerson": "John Smith",
        "address": "456 Innovation Dr, Boston, MA 02101",
        "industry": "Consulting",
    },
    "Creative Designs": {
        "id": "acc003",
        "name": "Creative Designs",
        "contactPerson": "Emily White",
        "address": "789 Art Ave, New York, NY 10001",
        "industry": "Marketing",
    }
}

mock_history = {
    "acc001": [
        {"date": "2024-05-20", "activity": "Closed Won - Printer Fleet Upgrade", "amount": 75000},
        {"date": "2024-02-10", "activity": "Support Ticket #4521 Resolved", "amount": 0}
    ],
    "acc002": [
        {"date": "2024-06-01", "activity": "Initial Consultation - IT Services", "amount": 0}
    ],
    "acc003": [
         {"date": "2023-11-15", "activity": "Contract Signed - Marketing Automation", "amount": 50000}
    ]
}

@app.route('/customers', methods=['GET'])
def get_customer_details():
    customer_name = request.args.get('name')
    if not customer_name:
        return jsonify({"error": "Customer name is required"}), 400
    
    customer_data = mock_db.get(customer_name)
    
    if customer_data:
        return jsonify(customer_data)
    else:
        return jsonify({"error": f"Customer '{customer_name}' not found"}), 404

@app.route('/history', methods=['GET'])
def get_account_history():
    customer_name = request.args.get('name')
    if not customer_name:
        return jsonify({"error": "Customer name is required"}), 400
    
    customer_data = mock_db.get(customer_name)
    if not customer_data:
        return jsonify({"error": f"Customer '{customer_name}' not found"}), 404
        
    account_id = customer_data.get('id')
    history = mock_history.get(account_id, [])
    
    return jsonify({"history": history})

if __name__ == '__main__':
    # Run on port 5003 to avoid conflicts with Orchestrate services
    app.run(port=5003, debug=True)
```
**To run the API, open a new terminal, navigate to the `tools` directory, and run:**
```bash
python mock_salesforce_api.py
```
Leave this terminal running in the background.

## Step 2: Create and Import the Knowledge Base
The knowledge base is a critical component that stores unstructured information about Xerox's services. It enables the `Proposal_Generation_Agent` to find and use the most relevant service descriptions for a proposal, demonstrating a powerful RAG pattern.

**File: `xerox_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: Xerox_Service_Catalog
description: >
   Contains detailed descriptions, features, pricing, and standard terms for all Xerox services-led offerings, including Managed Print Services, IT Outsourcing, and Digital Transformation.
documents:
   - "./mock_docs/Managed_Print_Services.pdf"
   - "./mock_docs/IT_Outsourcing_Solutions.txt"
   - "./mock_docs/Digital_Transformation_Services.txt"
vector_index:
   # Uses the default, powerful embedding model provided by watsonx Orchestrate
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

**Import the Knowledge Base using the ADK CLI:**
```bash
orchestrate knowledge-bases import -f xerox_kb.yaml
```

## Step 3: Create the Tools
Tools are the building blocks that allow agents to perform actions. We will create two distinct tools: an OpenAPI-based tool for structured API calls and a Python-based tool for custom document generation logic.

### 3.1. Salesforce Data Tools (OpenAPI)
This OpenAPI specification defines how the `Salesforce_Data_Agent` can interact with our mock API. This pattern is ideal for integrating with any existing enterprise system that exposes a REST API, providing a robust and scalable integration method.

**File: `tools/salesforce_api.openapi.yaml`**
```yaml
openapi: 3.0.0
info:
  title: Mock Salesforce API
  version: 1.0.0
servers:
  - url: http://127.0.0.1:5003
paths:
  /customers:
    get:
      operationId: get_customer_details
      summary: Get Customer Details
      description: Retrieves key customer details like contact person, address, and industry from Salesforce by account name.
      parameters:
        - name: name
          in: query
          required: true
          schema:
            type: string
          description: The full account name of the customer.
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
  /history:
    get:
      operationId: get_account_history
      summary: Get Account History
      description: Retrieves the recent activity and transaction history for a customer by their account name.
      parameters:
        - name: name
          in: query
          required: true
          schema:
            type: string
          description: The full account name of the customer.
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
```

### 3.2. Proposal Generation Tool (Python)
This Python tool encapsulates the custom logic for generating a proposal draft. It takes structured customer data and unstructured service information and combines them into a formatted document. This pattern is perfect for tasks that require complex logic, data manipulation, or custom formatting that goes beyond a simple API call.

**File: `tools/proposal_tool.py`**
```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import Dict, Any

@tool(name="create_proposal_draft", permission=ToolPermission.ADMIN)
def create_proposal_draft(customer_data: Dict[str, Any], service_info: str) -> str:
    """
    Creates a formatted draft proposal by combining customer details and service information into a template.

    This tool is used as the final step in proposal generation, assembling all gathered information
    into a coherent and professional document ready for sales review.

    Args:
        customer_data (dict): A dictionary containing customer details from Salesforce, such as 'name', 'contactPerson', and 'address'.
        service_info (str): A string containing the detailed service description, features, and terms retrieved from the Xerox Service Catalog knowledge base.

    Returns:
        str: The full text of the drafted proposal, formatted and ready for output.
    """
    try:
        # Template for the proposal document
        draft = f"""
# Proposal for: {customer_data.get('name', 'N/A')}

**Prepared for:** {customer_data.get('contactPerson', 'N/A')}
**Address:** {customer_data.get('address', 'N/A')}
**Industry:** {customer_data.get('industry', 'N/A')}

---

## 1. Proposed Services

This proposal outlines the following Xerox services tailored to meet your business needs:

{service_info}

---

## 2. Next Steps

We are confident that our solutions will deliver significant value to your organization. A Xerox sales representative will follow up within 24 hours to discuss this proposal in detail and answer any questions you may have.

Thank you for considering Xerox as your partner.
"""
        return draft.strip()
    except Exception as e:
        return f"Error generating proposal draft: {str(e)}"

```

## Step 4: Import the Tools
With the tool definitions created, import them into watsonx Orchestrate so they can be assigned to agents.

**Import the OpenAPI Tool:**
```bash
orchestrate tools import -f tools/salesforce_api.openapi.yaml
```

**Import the Python Tool:**
```bash
orchestrate tools import -k python -f tools/proposal_tool.py
```

## Step 5: Create Agent Definitions
Now we define the three agents that form our architecture. The collaborator agents are specialized workers, and the supervisor agent is the manager that orchestrates their efforts.

### 5.1. Salesforce Data Agent (Collaborator)
This agent's sole purpose is to interact with the Salesforce API. Its description is crafted to clearly state its capabilities, so the supervisor knows exactly when to delegate customer data requests to it.

**File: `agents/salesforce_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Salesforce_Data_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An agent that specializes in connecting to and retrieving customer information from the Salesforce CRM system. Use this agent to get customer details like address and contact person, or to look up account history.
instructions: >
    Your only function is to use your tools to retrieve data from Salesforce.
    - Use the 'get_customer_details' tool when asked for general information about a customer account.
    - Use the 'get_account_history' tool when asked for past activities or transactions.
    - Do not attempt to answer questions about anything other than Salesforce data.
collaborators: []
tools:
  - get_customer_details
  - get_account_history
```

### 5.2. Proposal Generation Agent (Collaborator)
This agent is responsible for the creative and assembly work. It uses the knowledge base to find service information and the Python tool to build the final document. Its description highlights its ability to work with the service catalog and draft documents.

**File: `agents/proposal_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: Proposal_Generation_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An agent responsible for drafting sales proposals and contracts. It can search the Xerox_Service_Catalog knowledge base to find detailed information about services and then use its tools to assemble a final document.
instructions: >
    Your goal is to create proposal documents.
    1. First, you MUST search the 'Xerox_Service_Catalog' knowledge base to find information about the services requested by the user.
    2. Once you have the service information, use the 'create_proposal_draft' tool to combine it with the provided customer data to generate the final document.
    3. Present the output from the 'create_proposal_draft' tool as your final answer.
collaborators: []
tools:
  - create_proposal_draft
knowledge_base:
  - Xerox_Service_Catalog
```

### 5.3. Xerox Sales Co-pilot (Supervisor)
This is the master orchestrator. It has no tools of its own; its power comes from its ability to understand a user's request and intelligently route tasks to the correct collaborator. The instructions are critical here, as they form the reasoning framework for its decision-making process.

**File: `agents/xerox_sales_copilot.yaml`**
```yaml
spec_version: v1
kind: native
name: Xerox_Sales_Co-pilot
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A master sales assistant that creates comprehensive proposals and contracts for the Xerox sales team. It orchestrates work between a Salesforce agent for customer data and a Proposal agent for document creation and service information retrieval.
instructions: >
    You are the Xerox Sales Co-pilot. Your primary goal is to help the Xerox sales team create proposals efficiently. Follow this reasoning process:
    
    Phase 1: Information Gathering
    - When a user asks for a proposal for a specific customer, your FIRST step is ALWAYS to use the 'Salesforce_Data_Agent' to retrieve that customer's details.
    
    Phase 2: Content Generation
    - Once you have the customer data, your SECOND step is to delegate the task of finding service information and drafting the document to the 'Proposal_Generation_Agent'.
    - You must pass the customer data you retrieved in Phase 1 to the 'Proposal_Generation_Agent' so it can create the full draft.
    
    Phase 3: Clarification
    - If the user's request is ambiguous (e.g., they don't specify which service to include), ask for clarification before proceeding with Phase 1.
collaborators:
  - Salesforce_Data_Agent
  - Proposal_Generation_Agent
```

## Step 6: Import the Agents
Import the agents in the correct order: dependencies (collaborators) first, then the supervisor that depends on them.

```bash
# Import Collaborator Agents
orchestrate agents import -f agents/salesforce_agent.yaml
orchestrate agents import -f agents/proposal_agent.yaml

# Import the Supervisor Agent
orchestrate agents import -f agents/xerox_sales_copilot.yaml
```

## Step 7: Verification and Demo
Now, test the complete solution by interacting with the `Xerox_Sales_Co-pilot` in the Orchestrate chat.

**Start the chat interface:**
```bash
orchestrate chat start
```
This will open a chat window in your browser. Make sure to select `Xerox_Sales_Co-pilot` from the agent dropdown list.

### Demo Scenario 1: Standard Proposal Generation
**User Prompt:**
> "Draft a proposal for 'Global Tech Inc.' for your Managed Print Services."

**Expected Behavior:**
1.  The `Xerox_Sales_Co-pilot` receives the request.
2.  It calls the `Salesforce_Data_Agent`, which uses the `get_customer_details` tool to fetch data for "Global Tech Inc." from the mock API.
3.  The supervisor then passes this customer data to the `Proposal_Generation_Agent`.
4.  The `Proposal_Generation_Agent` searches the `Xerox_Service_Catalog` knowledge base for "Managed Print Services".
5.  It then uses the `create_proposal_draft` tool, combining the customer data and service info.
6.  The final, formatted proposal is displayed in the chat.

### Demo Scenario 2: Multi-Service Contract Creation
**User Prompt:**
> "Create a contract for 'Innovate Solutions' that includes both IT Outsourcing and Digital Transformation Services. Make sure to include their address from Salesforce."

**Expected Behavior:**
1.  The `Xerox_Sales_Co-pilot` initiates the process by calling the `Salesforce_Data_Agent` for "Innovate Solutions".
2.  It then calls the `Proposal_Generation_Agent`.
3.  The `Proposal_Generation_Agent` queries the knowledge base for *both* "IT Outsourcing" and "Digital Transformation Services" and synthesizes the information.
4.  The `create_proposal_draft` tool is called to assemble the final, more complex document.
5.  The final contract draft is returned to the user.

### Demo Scenario 3: Conversational Clarification
**User Prompt:**
> "I need a proposal for 'Creative Designs'."

**Expected Behavior:**
1.  The `Xerox_Sales_Co-pilot` recognizes that a key piece of information (the service) is missing.
2.  Based on its instructions, instead of calling a collaborator, it will respond directly to the user with a clarifying question, such as: *"I can help with that. Which Xerox services are you proposing for Creative Designs?"* This demonstrates the agent's reasoning and conversational capabilities.

## Troubleshooting
-   **Tool Import Fails**: Ensure the mock Salesforce API (`mock_salesforce_api.py`) is running in a separate terminal before you import the OpenAPI tool. Check that the URL (`http://127.0.0.1:5003`) in the `salesforce_api.openapi.yaml` file is correct.
-   **Agent Not Found Error**: When importing the supervisor, ensure you have successfully imported the collaborator agents first. Agent names are case-sensitive and must match exactly between the collaborator list and the agent's `name` field.
-   **Knowledge Base Not Working**: Verify that the file paths in `xerox_kb.yaml` are correct relative to where you are running the `orchestrate` command. Use `orchestrate knowledge-bases status --name Xerox_Service_Catalog` to check if it was ingested correctly.
-   **Agent Doesn't Follow Instructions**: If the supervisor fails to delegate correctly, review the `instructions` in its YAML file. They need to be clear, explicit, and directive. Small changes in wording can significantly impact the LLM's reasoning. Ensure the collaborator `description` fields are also clear and accurate.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
