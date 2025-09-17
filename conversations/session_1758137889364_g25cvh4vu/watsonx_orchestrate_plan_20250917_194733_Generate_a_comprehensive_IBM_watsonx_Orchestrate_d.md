# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-17 19:47:33
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox Supervisor Agent for Document Workflow Automation

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide for building and deploying a powerful watsonx Orchestrate demo tailored to Xerox. The plan directly implements the **Xerox Supervisor Agent** concept, demonstrating how watsonx Orchestrate can act as a master orchestration layer for a complex, multi-step contract management workflow. This solution showcases a "better together" story, where Orchestrate enhances and unifies a simulated ecosystem of specialized agents built with the Xerox® Agent Builder.

The core of this demo is a `Xerox_Workflow_Supervisor` agent that interprets a user's high-level request in natural language (e.g., "Onboard a new vendor"). It then intelligently decomposes the task and delegates sub-tasks to a team of specialist collaborator agents: a `Document_Generation_Agent`, a `Compliance_Check_Agent` leveraging a knowledge base (RAG), and an `Approval_Routing_Agent` that connects to external systems. This plan will build this entire multi-agent architecture from the ground up, providing all necessary code, configuration files, and deployment commands, incorporating best practices for reproducibility and performance.

## 2. Prerequisites

Before beginning, ensure your environment meets the following requirements:

*   **Python Environment**: Python 3.9 or higher is installed and accessible from your terminal.
*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured and logged in via the ADK CLI. To initialize and log in, use:
    ```bash
    orchestrate login -s <environment>
    ```
*   **Text Editor/IDE**: A code editor such as Visual Studio Code is recommended for creating and editing YAML and Python files.
*   **Project Directory**: Create a dedicated folder for this project to keep all files organized.

## 3. Step 1: Project Setup and Mock Data Creation

A well-organized project structure is crucial for managing the different components of our multi-agent system. This step involves creating the necessary directories, the synthetic data files that will fuel our demo scenarios, and a `requirements.txt` file for environment reproducibility.

First, create the following directory structure within your main project folder:

```
xerox-demo/
├── agents/
├── tools/
│   ├── document_generator/
│   └── approval_router/
├── knowledge-bases/
├── mock_data/
│   ├── policies/
│   └── templates/
└── drafts/
```

Next, create the mock data files as specified in the client demo concept.

**1. Vendor Profiles (CSV)**
Create a file named `vendors.csv` inside the `mock_data/` directory. This data will be used by the `Document_Generation_Agent`.

`mock_data/vendors.csv`:
```csv
company_name,address,contact_person,msa_type
Innovate Inc.,"123 Innovation Drive, Techville, TX 75001",Jane Doe,Standard
Global Tech,"456 Enterprise Blvd, Business City, CA 90210",John Smith,Premium
Solutions Corp,"789 Partnership Way, Synergy, FL 32801",Standard,Standard
```

**2. Contract Template (.txt)**
Create a file named `MSA_Template.txt` inside the `mock_data/templates/` directory. This template contains placeholders that our Python tool will populate.

`mock_data/templates/MSA_Template.txt`:
```
MASTER SERVICE AGREEMENT

This Master Service Agreement ("MSA") is entered into by and between Xerox Corporation and {{company_name}}.

1.  SERVICES
    Xerox shall provide services as detailed in subsequent Statements of Work ("SOW").

2.  PAYMENT TERMS
    Payment terms are Net 30 days from the date of invoice. All payments shall be made in USD.

3.  CONFIDENTIALITY
    Both parties agree to maintain the confidentiality of all proprietary information disclosed during the term of this agreement.

This is a {{msa_type}} level agreement.

Signed:

_________________________
Xerox Corporation

_________________________
{{company_name}}
```

**3. Compliance Policy Documents (.pdf)**
For the demo, we will create simple text files and save them as PDFs. Create two files inside the `mock_data/policies/` directory.

`mock_data/policies/Payment_Terms_Standard.pdf` (Create this content in a text editor and "Print to PDF"):
```
Xerox Corporate Policy: Payment Terms

Document ID: POL-FIN-001
Version: 3.0
Effective Date: 2024-01-01

Subject: Standard Client Payment Terms

All standard Master Service Agreements and Statements of Work must adhere to a "Net 30" payment term schedule. Any deviation, such as Net 60 or Net 90, requires explicit written approval from the Vice President of Finance. Contracts submitted with non-standard terms without prior approval will be rejected by the compliance department.
```

`mock_data/policies/Data_Privacy_Policy.pdf` (Create this content in a text editor and "Print to PDF"):
```
Xerox Corporate Policy: Data Privacy and Handling

Document ID: POL-SEC-005
Version: 2.1
Effective Date: 2024-03-15

Subject: Client Data Protection

All contracts must include a clause explicitly stating that client data will be handled in accordance with GDPR, CCPA, and other relevant data protection regulations. The storage of Personally Identifiable Information (PII) must be on encrypted, access-controlled servers. Any third-party data processors must be vetted and approved by the Xerox security team.
```

**4. Environment Reproducibility (`requirements.txt`)**
As a best practice, create a `requirements.txt` file in the root of your `xerox-demo/` directory. This ensures that anyone running the demo can install the exact dependencies needed.

`requirements.txt`:
```
ibm-watsonx-orchestrate
```

## 4. Step 2: Create and Import the Knowledge Base

The knowledge base is the foundation of our `Compliance_Check_Agent`. It uses Retrieval-Augmented Generation (RAG) to allow the agent to reason over the content of our internal policy documents. We will configure a built-in Milvus knowledge base and ingest our mock policy PDFs.

Create the following YAML file. Note the use of the latest recommended embedding model, `ibm/slate-125m-english-rtrvr-v2`, for optimal performance.

`knowledge-bases/xerox_legal_policy_kb.yaml`:
```yaml
spec_version: v1
kind: knowledge_base
name: xerox_legal_policy_kb
description: >
   Contains Xerox corporate policies regarding contract terms, data privacy, and payment standards. Use this to verify contract compliance against official company standards.
documents:
   - "mock_data/policies/Data_Privacy_Policy.pdf"
   - "mock_data/policies/Payment_Terms_Standard.pdf"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

**Import the Knowledge Base**
Open your terminal, navigate to the root of your `xerox-demo` directory, and run the following command:

```bash
orchestrate knowledge-bases import -f knowledge-bases/xerox_legal_policy_kb.yaml
```

## 5. Step 3: Create the Specialist Tools

Tools are the executable components that allow our agents to perform actions. We will create a Python-based tool for document generation and an OpenAPI-based tool for handling approvals, representing the two primary ways of extending watsonx Orchestrate.

### Tool 1: `create_contract_draft` (Python)

**Purpose and Business Value:** This tool automates the foundational task of drafting a contract. It represents a core Xerox capability, transforming raw data (vendor information) into a structured document based on a standard template. This eliminates manual copy-pasting, reduces errors, and ensures consistency across all generated contracts, directly accelerating the start of the contract lifecycle.

**Technical Implementation:** The Python function uses the `@tool` decorator to register it with the ADK. It reads the `vendors.csv` file to find the specified company's data, loads the `MSA_Template.txt`, replaces the placeholders (`{{company_name}}`, `{{msa_type}}`), and saves the new document to the `drafts/` directory. It includes robust error handling for missing files or companies and returns a clear confirmation message with the file path, which the agent can then use for subsequent steps.

Create the following Python file:

`tools/document_generator/create_contract_draft.py`:
```python
import os
import csv
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="create_contract_draft", permission=ToolPermission.ADMIN)
def create_contract_draft(company_name: str) -> str:
    """
    Creates a draft Master Service Agreement (MSA) for a given company using a standard template.
    It fetches company details from a central CSV file and populates the template.

    Args:
        company_name (str): The exact name of the company for the contract (e.g., 'Innovate Inc.').

    Returns:
        str: A confirmation message with the path to the saved draft document, or an error message if the company is not found.
    """
    vendor_file = 'mock_data/vendors.csv'
    template_file = 'mock_data/templates/MSA_Template.txt'
    output_dir = 'drafts'
    
    company_data = None
    try:
        with open(vendor_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['company_name'] == company_name:
                    company_data = row
                    break
        
        if not company_data:
            return f"Error: Company '{company_name}' not found in vendors list."

        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Replace placeholders
        draft_content = template_content.replace('{{company_name}}', company_data['company_name'])
        draft_content = draft_content.replace('{{msa_type}}', company_data['msa_type'])

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_name = f"{company_name.replace(' ', '_').replace('.', '')}_MSA.txt"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)
            
        return f"Successfully created draft contract at '{file_path}'"

    except FileNotFoundError as e:
        return f"Error: A required file was not found: {e.filename}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
```

### Tool 2: `submit_for_approval` (OpenAPI)

**Purpose and Business Value:** This tool demonstrates how watsonx Orchestrate can seamlessly connect to and control existing enterprise APIs and third-party services like ServiceNow or Jira. By defining a simple OpenAPI specification, we enable the `Approval_Routing_Agent` to push a completed contract into an external workflow system. This bridges the gap between document creation and business process management, creating a true end-to-end automated solution.

**Technical Implementation:** This is a mock OpenAPI 3.0 specification. It defines a single `POST` endpoint `/approvals`. The `operationId` (`submit_for_approval`) becomes the function name the agent calls. The `summary` and `description` inform the agent what the tool does. The `requestBody` specifies the required inputs (`document_path`, `submitted_by`), and the `responses` section defines the expected output, in this case, a JSON object with a `tracking_id`.

Create the following JSON file:

`tools/approval_router/approval_api.openapi.json`:
```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Mock Approval System API",
    "version": "1.0.0",
    "description": "A mock API to submit documents for approval."
  },
  "servers": [
    {
      "url": "https://mock-approval-system.com/api/v1",
      "description": "Mock Server"
    }
  ],
  "paths": {
    "/approvals": {
      "post": {
        "operationId": "submit_for_approval",
        "summary": "Submit a document for approval",
        "description": "Submits a document to the internal approval workflow system and returns a tracking ID.",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "document_path": {
                    "type": "string",
                    "description": "The file path of the document to be approved."
                  },
                  "submitted_by": {
                    "type": "string",
                    "description": "The name or ID of the user submitting the request."
                  }
                },
                "required": ["document_path", "submitted_by"]
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successfully submitted for approval.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string"
                    },
                    "tracking_id": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Invalid input provided."
          }
        }
      }
    }
  }
}
```
**Note:** The `scan_document_for_compliance` tool is implicitly handled by the `Compliance_Check_Agent` using its integrated knowledge base. The agent's instructions will guide it to perform this RAG-based check without needing a separate, explicit tool definition.

## 6. Step 4: Create the Specialist Collaborator Agents

These agents are the dedicated workers in our system. Each has a single responsibility and is equipped with the specific tools and/or knowledge needed for its job. Their well-crafted descriptions are vital for the Supervisor Agent to route tasks correctly. All agents will use the `watsonx/ibm/granite-3-8b-instruct` model for consistency with the client context.

**1. Document Generation Agent**
This agent's sole purpose is to create documents. Its description clearly states this, allowing the Supervisor to delegate any "create," "draft," or "generate" requests to it.

`agents/Document_Generation_Agent.yaml`:
```yaml
spec_version: v1
kind: native
name: Document_Generation_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent responsible for creating and drafting documents based on templates and input data.
  Use this agent for any tasks related to document generation, such as creating a new contract, MSA, or SOW.
instructions: >
  Your only job is to create contract drafts. When asked, use the create_contract_draft tool with the company name provided by the user.
  Return the full confirmation message from the tool back to the supervisor.
tools:
  - create_contract_draft
```

**2. Compliance Check Agent**
This agent is the team's legal and policy expert. It leverages its attached knowledge base to validate documents. Its description highlights its ability to check for compliance, signaling to the Supervisor that this is the go-to agent for any validation or review tasks.

`agents/Compliance_Check_Agent.yaml`:
```yaml
spec_version: v1
kind: native
name: Compliance_Check_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent that reviews documents against a knowledge base of internal Xerox policies and legal standards to ensure compliance.
  Use this agent to scan, check, verify, or validate a document for compliance with payment terms, data privacy clauses, and other corporate standards.
instructions: >
  You are a compliance officer. Your task is to use your knowledge base to check if a given document or specific clause complies with Xerox corporate policy.
  When given a document, carefully review it against the information in your knowledge base.
  If you find a violation (e.g., payment terms other than 'Net 30'), clearly state the violation and reference the policy.
  If the document is compliant, confirm that it meets all policy standards.
knowledge_base:
  - xerox_legal_policy_kb
```

**3. Approval Routing Agent**
This agent acts as the bridge to external systems. Its description focuses on submitting, routing, or sending items for approval, making it the clear choice for the final step in the workflow.

`agents/Approval_Routing_Agent.yaml`:
```yaml
spec_version: v1
kind: native
name: Approval_Routing_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialist agent that integrates with external workflow systems (e.g., ServiceNow, Jira) to manage approval routing.
  Use this agent for the final step of submitting a document for official approval.
instructions: >
  Your role is to submit documents to the approval queue. Use the submit_for_approval tool.
  You will be given a document path. Assume the user who is chatting is the one submitting.
  Relay the final confirmation message, including the tracking ID, back to the supervisor.
tools:
  - submit_for_approval
```

## 7. Step 5: Create the Supervisor Agent

The Supervisor is the brain of the operation. It doesn't perform actions itself but instead understands the user's overall goal and directs the workflow. Its `description` and `instructions` are the most critical pieces, defining the entire multi-step logic, including sequencing and exception handling.

`agents/Xerox_Workflow_Supervisor.yaml`:
```yaml
spec_version: v1
kind: native
name: Xerox_Workflow_Supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A master supervisor agent for Xerox document workflows. It understands complex requests related to contract generation, compliance, and approvals. It delegates tasks to specialist agents: Document_Generation_Agent for drafting, Compliance_Check_Agent for policy validation, and Approval_Routing_Agent for workflow submissions.
instructions: >
    You are the master orchestrator for the entire contract lifecycle. Follow these steps precisely:
    1.  **Deconstruct Request**: Understand the user's end-goal. If they ask to create and approve a contract, you must manage the full sequence.
    2.  **Step 1 - Generation**: For any request to create or draft a document, ALWAYS delegate to the `Document_Generation_Agent` first.
    3.  **Step 2 - Compliance Check**: After a document is successfully created, ALWAYS delegate to the `Compliance_Check_Agent` to verify it against corporate policies.
    4.  **Step 3 - Approval Routing**: If and ONLY IF the document is compliant, delegate to the `Approval_Routing_Agent` to submit it for final approval.
    5.  **Exception Handling**: If the `Compliance_Check_Agent` reports a violation, DO NOT proceed to the approval step. Instead, report the specific compliance failure back to the user and ask them for instructions on how to proceed (e.g., "Please advise if I should proceed with an exception or revise the terms.").
    6.  **Direct Queries**: If the user asks a specific question about compliance without asking to generate a document, route that query directly to the `Compliance_Check_Agent`.
collaborators:
  - Document_Generation_Agent
  - Compliance_Check_Agent
  - Approval_Routing_Agent
tools: []
```

## 8. Step 6: Deploy the System with ADK CLI

With all our configuration files in place, we can now deploy the entire system. The order of operations is critical to ensure that dependencies are met (e.g., agents cannot be imported before their tools exist).

Run these commands from the root of your `xerox-demo` directory in the following order:

```bash
# 1. Import all tools for the specialist agents
echo "Importing tools..."
orchestrate tools import -f tools/document_generator/create_contract_draft.py
orchestrate tools import -f tools/approval_router/approval_api.openapi.json

# 2. Import the specialist collaborator agents (Knowledge Base was already imported in Step 2)
echo "Importing specialist agents..."
orchestrate agents import -f agents/Document_Generation_Agent.yaml
orchestrate agents import -f agents/Compliance_Check_Agent.yaml
orchestrate agents import -f agents/Approval_Routing_Agent.yaml

# 3. Import the master Supervisor Agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/Xerox_Workflow_Supervisor.yaml

echo "Deployment complete! You can now test the supervisor agent."
```

## 9. Verification and Demo Scenarios

After successful deployment, you can test the entire workflow using the watsonx Orchestrate chat interface. Select the `Xerox_Workflow_Supervisor` agent to begin the conversation.

**Scenario 1: End-to-End Workflow Automation**
*   **User Prompt**: `"Generate a new Master Service Agreement for 'Innovate Inc.' and get it ready for approval."`
*   **Expected Orchestration Flow**:
    1.  `Xerox_Workflow_Supervisor` receives the prompt.
    2.  It delegates to `Document_Generation_Agent`, which calls the `create_contract_draft` tool. A file `drafts/Innovate_Inc_MSA.txt` is created.
    3.  The supervisor then delegates to `Compliance_Check_Agent`, which uses its knowledge base to confirm the "Net 30" term is compliant.
    4.  The supervisor finally delegates to `Approval_Routing_Agent`, which calls the `submit_for_approval` tool.
*   **Expected Outcome**: The Supervisor responds with a confirmation like: `"The contract for Innovate Inc. has been drafted, verified for compliance, and submitted for approval. The tracking ID is [mock_tracking_id]."`

**Scenario 2: Intelligent Exception Handling**
*   **Setup**: Manually edit `mock_data/templates/MSA_Template.txt` and change "Net 30" to "Net 90". Re-run the demo.
*   **User Prompt**: `"Draft a contract for 'Global Tech' and submit it."`
*   **Expected Orchestration Flow**:
    1.  `Xerox_Workflow_Supervisor` delegates to `Document_Generation_Agent` to create the draft with the 90-day terms.
    2.  It then delegates to `Compliance_Check_Agent`, which scans the document and its knowledge base flags that "Net 90" violates the standard "Net 30" policy.
*   **Expected Outcome**: The Supervisor stops the workflow and reports the issue to the user: `"I have drafted the contract for Global Tech, but the 90-day payment terms violate our standard Net 30 policy. Please advise if I should proceed with an exception or revise the terms."`

**Scenario 3: Direct Specialist Agent Interaction**
*   **User Prompt**: `"Is a clause requiring 'Net 60' payment terms compliant with our policies?"`
*   **Expected Orchestration Flow**: The `Xerox_Workflow_Supervisor` recognizes this is a specific compliance question and routes it directly to the `Compliance_Check_Agent`.
*   **Expected Outcome**: The `Compliance_Check_Agent` uses its knowledge base to answer: `"No, a 'Net 60' payment term is not compliant. The standard corporate policy requires 'Net 30' payment terms unless an exception is approved by the VP of Finance."`

## 10. Troubleshooting

*   **Issue: Agent Not Found During Import**
    *   **Cause**: You are trying to import the `Xerox_Workflow_Supervisor` before its collaborator agents have been successfully imported.
    *   **Solution**: Ensure you run the `orchestrate agents import` commands in the correct order: specialist agents first, then the supervisor.
*   **Issue: Tool Not Found During Agent Import**
    *   **Cause**: An agent's YAML file references a tool that has not been imported yet.
    *   **Solution**: Always import all tools using `orchestrate tools import` *before* importing any agents that depend on them.
*   **Issue: Supervisor Fails to Delegate Correctly**
    *   **Cause**: The `description` of the collaborator agents or the `instructions` in the supervisor agent are not clear enough for the LLM to understand the routing logic.
    *   **Solution**: Refine the descriptions to be more explicit about each agent's unique capability. Make the supervisor's instructions more procedural (e.g., "First, do X. Second, do Y."). Re-import the agent after making changes.
*   **Issue: File Not Found Error from `create_contract_draft` Tool**
    *   **Cause**: The CLI command is being run from a directory other than the project root (`xerox-demo`), so the relative paths (`mock_data/vendors.csv`) are incorrect.
    *   **Solution**: Always run the `orchestrate chat` command from the root directory of your project where the `mock_data` folder is located.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
