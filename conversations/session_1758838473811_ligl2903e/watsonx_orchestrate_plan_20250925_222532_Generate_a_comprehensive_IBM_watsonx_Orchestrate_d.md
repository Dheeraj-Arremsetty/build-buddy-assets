# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-25 22:25:32
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Contract Lifecycle Automation Suite

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Contract Lifecycle Automation Suite" for the client. The solution directly addresses the client's strategic goal of transforming their manual contract management process into an intelligent, automated workflow. By leveraging a multi-agent architecture within IBM watsonx Orchestrate, this system will significantly reduce contract cycle times, minimize legal risks through AI-powered analysis, and enhance operational efficiency by seamlessly integrating with core business systems like Box, Salesforce, and DocuSign.

The plan details the creation of a supervisor agent, the `Contract Lifecycle Supervisor`, which intelligently orchestrates three specialized collaborator agents: the `Document Manager Agent` for secure content handling, the `Contract Intelligence Agent` for deep document analysis using watsonx.ai and a legal knowledge base, and the `Workflow Execution Agent` for actions in external platforms. This document provides all necessary code, configuration files, and CLI commands to build a fully functional Proof of Concept (POC) that demonstrates the power and flexibility of watsonx Orchestrate for complex enterprise automation.

## Prerequisites
Before beginning, ensure your development environment is set up with the following components. This setup is crucial for using the Agent Development Kit (ADK) and deploying the solution.

1.  **Python Environment**: A working installation of Python (version 3.10 or higher) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment Configuration**: You must have an active watsonx Orchestrate environment configured with the ADK. This is typically done via the `orchestrate env add` command, pointing to your tenant credentials.
4.  **Mock Data Files**: You will need to create the mock documents specified in the client demo concept. These files are essential for populating the knowledge base and for the agents to process during the demo scenarios.
5.  **External API Specifications (for production)**: While this plan uses mock OpenAPI specifications for demonstration, a real-world implementation would require the official OpenAPI (or Swagger) specifications for Salesforce and DocuSign to ensure accurate tool creation.

## Step 1: Project Structure and Mock Data Setup
A well-organized project structure is key to managing the different components of your solution. We will also create the necessary mock data files that will be used by our agents and knowledge base.

### 1.1. Create the Project Directory Structure
Create the following folders in your project's root directory:
```
/contract-lifecycle-poc
|-- /agents
|-- /tools
|-- /openapi
|-- /knowledge-bases
|-- /mock_data
|-- requirements.txt
```

### 1.2. Create Mock Contract and Knowledge Base Documents
Inside the `/mock_data` folder, create the following (placeholder) PDF files. For the demo, the content of the `.pdf` files can be simple text, but the file names are important.

1.  **`Standard_MSA_Template.pdf`**: A standard Master Services Agreement.
2.  **`High_Risk_Vendor_Agreement.pdf`**: An agreement containing non-standard clauses.
3.  **`Simple_NDA.pdf`**: A straightforward Non-Disclosure Agreement.
4.  **`Legal_Risk_Definitions.pdf`**: This document will form our knowledge base. Create a PDF with the following text to simulate legal definitions:
    *   **Unlimited Liability**: A clause where one party assumes unlimited financial responsibility for damages, which is considered a high-risk term.
    *   **Non-standard Indemnification**: Clauses that deviate from company policy on holding harmless, exposing the company to unforeseen legal costs.
    *   **Auto-renewal**: Contract terms that automatically renew without explicit consent, potentially locking the company into unfavorable long-term agreements.

## Step 2: Create the Knowledge Base
The `Contract Intelligence Agent` will use a knowledge base to identify risks. This is a core component of the RAG (Retrieval-Augmented Generation) pattern.

### 2.1. Define the Knowledge Base YAML
Create a file named `legal_risk_kb.yaml` inside the `/knowledge-bases` folder. This configuration ingests our `Legal_Risk_Definitions.pdf` into a built-in Milvus vector database.

**File: `/knowledge-bases/legal_risk_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: legal_risk_kb
description: >
   Contains definitions and examples of high-risk legal clauses and non-standard terms 
   to aid in contract review. This knowledge base is the primary source of truth for the
   Contract Intelligence Agent when identifying potential contractual risks.
documents:
   - "mock_data/Legal_Risk_Definitions.pdf"
vector_index:
   # Using the default embedding model for simplicity
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Create the Tools
Tools are the building blocks that allow agents to perform actions. We will create Python-based tools for custom logic (Box, AI analysis) and define mock OpenAPI specifications for external services (Salesforce, DocuSign).

### 3.1. Create Python Tools
#### Document Manager Tools (Box Integration)
This set of tools simulates interactions with the Box content cloud, enabling the `Document Manager Agent` to fetch, upload, and list contracts. It demonstrates secure and programmatic access to an enterprise content management system.

**File: `/tools/box_tools.py`**
```python
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="list_pending_contracts", description="Lists all contracts from Box that are in the 'Pending Review' folder.", permission=ToolPermission.ADMIN)
def list_pending_contracts() -> str:
    """
    Retrieves a list of contract documents awaiting review from a specific folder in Box.

    Returns:
        str: A JSON string representing a list of pending contracts with their metadata.
    """
    # --- SYNTHETIC DATA GENERATION ---
    mock_contracts = [
        {"id": "box-doc-112233", "name": "High_Risk_Vendor_Agreement.pdf", "status": "Pending Review", "uploaded_by": "sales.ops@example.com", "timestamp": (datetime.now() - timedelta(days=1)).isoformat()},
        {"id": "box-doc-445566", "name": "Standard_MSA_Template.pdf", "status": "Pending Review", "uploaded_by": "legal.team@example.com", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()},
        {"id": "box-doc-778899", "name": "Simple_NDA.pdf", "status": "Pending Review", "uploaded_by": "hr@example.com", "timestamp": (datetime.now() - timedelta(days=3)).isoformat()}
    ]
    return json.dumps(mock_contracts, indent=2)

@tool(name="fetch_contract_from_box", description="Fetches the content of a specific contract document from Box by its name.", permission=ToolPermission.ADMIN)
def fetch_contract_from_box(document_name: str) -> str:
    """
    Simulates downloading a contract document from Box.

    Args:
        document_name (str): The filename of the contract to fetch (e.g., 'High_Risk_Vendor_Agreement.pdf').

    Returns:
        str: A JSON string containing mock content and metadata of the fetched document.
    """
    # --- SYNTHETIC DATA GENERATION ---
    mock_content = {
        "Standard_MSA_Template.pdf": "This is a standard Master Services Agreement...",
        "High_Risk_Vendor_Agreement.pdf": "This agreement contains a clause stating: The vendor assumes unlimited liability...",
        "Simple_NDA.pdf": "This is a simple Non-Disclosure Agreement..."
    }
    
    if document_name in mock_content:
        return json.dumps({
            "document_name": document_name,
            "content": mock_content[document_name],
            "fetch_status": "Success",
            "timestamp": datetime.now().isoformat()
        })
    else:
        return json.dumps({
            "document_name": document_name,
            "content": None,
            "fetch_status": "Error: Document not found",
            "timestamp": datetime.now().isoformat()
        })

@tool(name="upload_signed_contract_to_box", description="Uploads a signed contract to the 'Executed Agreements' folder in Box.", permission=ToolPermission.ADMIN)
def upload_signed_contract_to_box(document_name: str, salesforce_opportunity_id: str) -> str:
    """
    Simulates uploading a signed contract document to a specific folder in Box.

    Args:
        document_name (str): The filename of the signed contract.
        salesforce_opportunity_id (str): The related Salesforce Opportunity ID for metadata tagging.

    Returns:
        str: A JSON string confirming the upload status and providing a mock Box URL.
    """
    # --- SYNTHETIC DATA GENERATION ---
    new_doc_id = f"box-doc-{random.randint(100000, 999999)}"
    return json.dumps({
        "document_name": document_name,
        "upload_status": "Success",
        "destination_folder": "/Executed Agreements/",
        "box_url": f"https://app.box.com/file/{new_doc_id}",
        "metadata_tags": {"salesforce_opportunity_id": salesforce_opportunity_id},
        "timestamp": datetime.now().isoformat()
    })
```

#### Contract Intelligence Tools (AI Analysis)
These tools simulate calls to watsonx.ai foundation models. They form the core of the `Contract Intelligence Agent`, enabling it to summarize, extract key information, and identify risks by leveraging the knowledge base. This showcases the direct business value of applying generative AI to complex legal documents.

**File: `/tools/contract_intelligence_tools.py`**
```python
import json
from datetime import datetime
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="summarize_contract", description="Generates a concise summary of a contract document using an AI model.", permission=ToolPermission.ADMIN)
def summarize_contract(contract_text: str) -> str:
    """
    Simulates a call to a watsonx.ai model to summarize the provided contract text.

    Args:
        contract_text (str): The full text of the contract to be summarized.

    Returns:
        str: A JSON string containing a bulleted summary of the contract.
    """
    # --- SYNTHETIC DATA GENERATION ---
    summary_points = [
        "Parties Involved: Client Corp and Vendor Inc.",
        "Effective Date: " + datetime.now().strftime('%Y-%m-%d'),
        "Term: 24 months from effective date.",
        "Key Services: Cloud data processing and analytics.",
        "Payment Terms: Net 30 days upon receipt of invoice."
    ]
    return json.dumps({"summary": summary_points, "model_used": "simulated/granite-3-8b-instruct"})

@tool(name="extract_key_clauses", description="Extracts specific key clauses from a contract, such as payment terms, termination conditions, and liability limits.", permission=ToolPermission.ADMIN)
def extract_key_clauses(contract_text: str) -> str:
    """
    Simulates a call to a watsonx.ai model to extract structured data from contract text.

    Args:
        contract_text (str): The full text of the contract.

    Returns:
        str: A JSON string containing the extracted clauses.
    """
    # --- SYNTHETIC DATA GENERATION ---
    clauses = {
        "payment_terms": "Payments are due within 30 days of the invoice date.",
        "termination_clause": "Either party may terminate with 60 days written notice.",
        "governing_law": "State of New York",
        "confidentiality": "Standard mutual confidentiality obligations apply for 5 years post-termination."
    }
    if "unlimited liability" in contract_text.lower():
        clauses["liability"] = "Vendor assumes unlimited liability for data breaches."
    else:
        clauses["liability"] = "Liability is capped at the total contract value for the preceding 12 months."
        
    return json.dumps(clauses, indent=2)

@tool(name="identify_contractual_risks", description="Analyzes a contract against a knowledge base of legal risks to identify non-standard or high-risk clauses.", permission=ToolPermission.ADMIN)
def identify_contractual_risks(contract_text: str) -> str:
    """
    Simulates using RAG to identify risks. In a real scenario, this tool would query the 
    'legal_risk_kb' knowledge base. Here, we simulate the outcome.

    Args:
        contract_text (str): The full text of the contract to analyze.

    Returns:
        str: A JSON string listing identified risks with severity levels.
    """
    # --- SYNTHETIC DATA GENERATION ---
    risks = []
    if "unlimited liability" in contract_text.lower():
        risks.append({
            "risk_type": "Unlimited Liability",
            "severity": "High",
            "recommendation": "Requires immediate legal review. Propose capping liability.",
            "source_in_kb": "Definition of 'Unlimited Liability' found in knowledge base."
        })
    if not risks:
        risks.append({
            "risk_type": "Standard Terms",
            "severity": "Low",
            "recommendation": "Contract appears to follow standard templates. Safe to proceed.",
            "source_in_kb": "N/A"
        })
        
    return json.dumps({"risk_analysis": risks, "timestamp": datetime.now().isoformat()})
```

### 3.2. Create OpenAPI-based Tools (Mock Specifications)
This demonstrates how watsonx Orchestrate can rapidly integrate with external SaaS platforms like Salesforce and DocuSign by importing their OpenAPI specifications. For this demo, we create simplified, mock YAML files that represent the structure Orchestrate expects.

#### DocuSign API Mock
**File: `/openapi/docusign_api.yaml`**
```yaml
servers:
  - url: https://demo.docusign.net/restapi
paths:
  /v2.1/accounts/{accountId}/envelopes:
    post:
      operationId: send_for_signature_docusign
      summary: Send a contract for electronic signature
      description: Creates a DocuSign envelope and sends it to the specified recipients for signature.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                emailSubject:
                  type: string
                documentBase64:
                  type: string
                recipients:
                  type: object
      responses:
        '201':
          description: Envelope sent successfully.
```

#### Salesforce API Mock
**File: `/openapi/salesforce_api.yaml`**
```yaml
servers:
  - url: https://my-salesforce-instance.my.salesforce.com
paths:
  /services/data/v58.0/sobjects/Opportunity/{Id}:
    patch:
      operationId: update_salesforce_opportunity
      summary: Update a Salesforce Opportunity
      description: Updates the stage or other fields of a Salesforce Opportunity record.
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                StageName:
                  type: string
                Contract_Status__c:
                  type: string
      responses:
        '204':
          description: Opportunity updated successfully.
  /services/data/v58.0/sobjects/Account/{Id}:
    get:
      operationId: get_salesforce_account_details
      summary: Get Salesforce Account Details
      description: Retrieves details for a specific Account in Salesforce, such as name and billing address.
      responses:
        '200':
          description: Account details retrieved.
```

### 3.3. Create `requirements.txt`
This file ensures that any necessary libraries for our Python tools are available in the environment. For these tools, no external libraries are needed, but it's a best practice to include the file.

**File: `requirements.txt`**
```
# No external dependencies required for these mock tools.
# In a real scenario, this would include:
# requests
# python-box
# simple-salesforce
```

## Step 4: Create the Agent Definitions
With our tools and knowledge base defined, we now create the YAML definitions for our four agents. These files configure each agent's identity, instructions, capabilities (tools), and relationships (collaborators).

#### Document Manager Agent
**File: `/agents/document_manager_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: document_manager_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent specializing in secure document handling with the Box content cloud. Use this agent for any tasks related to fetching, uploading, or listing contract documents. It is the sole interface for interacting with our corporate document repository.
instructions: >
  Your purpose is to manage documents in Box.
  Reasoning:
  - Use the 'list_pending_contracts' tool when a user asks to see which contracts are ready for review.
  - Use the 'fetch_contract_from_box' tool when another agent or user needs the content of a specific document.
  - Use the 'upload_signed_contract_to_box' tool to archive executed agreements.
tools:
  - list_pending_contracts
  - fetch_contract_from_box
  - upload_signed_contract_to_box
```

#### Contract Intelligence Agent
**File: `/agents/contract_intelligence_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: contract_intelligence_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An expert agent for analyzing legal contracts. Use this agent to summarize documents, 
  extract key clauses like payment terms and termination dates, and identify potential risks 
  by cross-referencing with our legal knowledge base.
instructions: >
  Your purpose is to provide deep insights into legal documents.
  Reasoning:
  - Use the 'summarize_contract' tool when a user asks for a high-level overview.
  - Use the 'extract_key_clauses' tool to pull specific data points from a contract.
  - Use the 'identify_contractual_risks' tool when a user asks for analysis or review. Always consult the knowledge base when identifying risks.
tools:
  - summarize_contract
  - extract_key_clauses
  - identify_contractual_risks
knowledge_base:
  - legal_risk_kb
```

#### Workflow Execution Agent
**File: `/agents/workflow_execution_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: workflow_execution_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that integrates with external business platforms to execute actions. Use this agent for tasks like sending a contract for signature via DocuSign or updating an opportunity status in Salesforce.
instructions: >
  Your purpose is to execute actions in external systems like Salesforce and DocuSign.
  Reasoning:
  - Use the 'send_for_signature_docusign' tool to initiate the e-signature process for an approved contract.
  - Use the 'update_salesforce_opportunity' tool to change the stage of an opportunity, for example, to 'Closed Won' after a contract is signed.
  - Use the 'get_salesforce_account_details' tool when you need information about a client from Salesforce.
tools:
  - send_for_signature_docusign
  - update_salesforce_opportunity
  - get_salesforce_account_details
```

#### Contract Lifecycle Supervisor (Supervisor Agent)
**File: `/agents/contract_lifecycle_supervisor.yaml`**
```yaml
spec_version: v1
kind: native
name: contract_lifecycle_supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  The primary agent for managing the end-to-end contract lifecycle. I interpret user requests and orchestrate my team of specialist agents—Document Manager, Contract Intelligence, and Workflow Execution—to automate contract processing from initial review to final signature and archiving.
instructions: >
  You are the supervisor for contract lifecycle management. Your goal is to understand the user's intent and delegate tasks to the appropriate collaborator agent. You do not run tools directly.

  Reasoning for Delegation:
  - For any request involving finding, retrieving, or storing documents in Box, delegate to the 'document_manager_agent'.
  - For any request requiring analysis, summarization, clause extraction, or risk identification of a contract's text, delegate to the 'contract_intelligence_agent'.
  - For any request to perform an action in an external system like sending for signature (DocuSign) or updating a sales record (Salesforce), delegate to the 'workflow_execution_agent'.
  
  Example Workflow:
  If a user says "Analyze and process the new vendor agreement", you must first use the 'document_manager_agent' to fetch it, then the 'contract_intelligence_agent' to analyze it, and finally, if approved, the 'workflow_execution_agent' to send it for signature.
collaborators:
  - document_manager_agent
  - contract_intelligence_agent
  - workflow_execution_agent
```

## Step 5: Import All Assets using the ADK CLI
Now, we will use the `orchestrate` CLI to import all the knowledge bases, tools, and agents into your watsonx Orchestrate environment. Run these commands from the root directory of your project (`/contract-lifecycle-poc`).

```bash
# 1. Import the Knowledge Base
echo "Importing knowledge base..."
orchestrate knowledge-bases import -f knowledge-bases/legal_risk_kb.yaml

# 2. Import the Python Tools
echo "Importing Python tools..."
orchestrate tools import -f tools/box_tools.py
orchestrate tools import -f tools/contract_intelligence_tools.py

# 3. Import the OpenAPI Tools
echo "Importing OpenAPI tools..."
orchestrate tools import -f openapi/docusign_api.yaml
orchestrate tools import -f openapi/salesforce_api.yaml

# 4. Import the Collaborator Agents
echo "Importing collaborator agents..."
orchestrate agents import -f agents/document_manager_agent.yaml
orchestrate agents import -f agents/contract_intelligence_agent.yaml
orchestrate agents import -f agents/workflow_execution_agent.yaml

# 5. Import the Supervisor Agent (last)
echo "Importing supervisor agent..."
orchestrate agents import -f agents/contract_lifecycle_supervisor.yaml

echo "All assets imported successfully!"
```

## Verification
After importing all assets, you can verify the setup by running the demo scenarios in the watsonx Orchestrate chat interface. Select the `Contract Lifecycle Supervisor` agent to start.

*   **Scenario 1: The "Happy Path" Automation**
    *   **User Prompt:** `"Process the standard MSA for the 'Globex Corp' opportunity."`
    *   **Expected Behavior:** The Supervisor should delegate to the `Document Manager` to fetch `Standard_MSA_Template.pdf`. Then, it should delegate to the `Contract Intelligence Agent`, which will use its `identify_contractual_risks` tool and report low risk. Finally, the Supervisor should ask if it should proceed, then delegate to the `Workflow Execution Agent` to (simulate) sending via DocuSign and updating Salesforce.

*   **Scenario 2: AI-Powered Risk Detection**
    *   **User Prompt:** `"Analyze the new vendor agreement from 'Risky Ventures'."` (Assume this maps to `High_Risk_Vendor_Agreement.pdf`)
    *   **Expected Behavior:** The Supervisor will orchestrate fetching the document. The `Contract Intelligence Agent` will analyze the text, and its `identify_contractual_risks` tool will detect the "unlimited liability" clause. The agent's response should be grounded by the knowledge base, flagging the high-risk term and recommending legal review, as described in the client concept.

*   **Scenario 3: On-Demand Contract Summarization**
    *   **User Prompt:** `"Give me a summary of the executed contract for the 'Cyberdyne Systems' deal."`
    *   **Expected Behavior:** The Supervisor should delegate to the `Document Manager` to find the contract and then to the `Contract Intelligence Agent` to use the `summarize_contract` tool, returning a concise, bulleted summary to the user.

## Troubleshooting
*   **Agent Not Found During Import**: If an agent import fails because a collaborator is not found, ensure you import the collaborator agents *before* the supervisor agent that depends on them.
*   **Supervisor Fails to Delegate**: If the supervisor agent tries to execute a tool directly or chooses the wrong collaborator, review its `description` and `instructions`. The descriptions of the collaborator agents are critical for the supervisor's routing logic. Ensure they clearly state the agent's unique capabilities.
*   **Tool Import Fails**: For Python tools, check for syntax errors and ensure the `@tool` decorator is correctly applied with a name and description. For OpenAPI tools, validate the YAML syntax and ensure `operationId` is unique and present for each path.
*   **Knowledge Base Not Working**: After importing the knowledge base, it can take a few minutes to ingest the documents. If the `Contract Intelligence Agent` isn't providing grounded answers, check the status of the knowledge base ingestion process.

## Best Practices
*   **Descriptive Naming and Descriptions**: The supervisor's ability to route tasks correctly depends heavily on the quality of the collaborator agents' `name` and `description` fields. Make them unique and explicit about the agent's function.
*   **Clear Instructions for Reasoning**: The `instructions` block, especially the "Reasoning" section, is crucial for guiding the agent's behavior. Be explicit about which tools or collaborators to use for specific scenarios.
*   **Separation of Concerns**: The agent architecture in this demo follows a key best practice: separating concerns. The `Document Manager` only handles files, the `Intelligence Agent` only handles analysis, and the `Workflow Agent` only handles external actions. This makes the system modular, scalable, and easier to maintain.
*   **Start Simple, Then Iterate**: Begin with a core workflow and verify it works end-to-end. Then, incrementally add more complex tools, collaborators, and logic. This iterative approach simplifies debugging and ensures a stable foundation.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
