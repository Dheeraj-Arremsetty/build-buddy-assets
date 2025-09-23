# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 14:59:32
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: "IBM Onboarding Buddy" Demo

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "IBM Onboarding Buddy," a multi-agent AI solution for a client's new hire onboarding process. The plan directly implements the client-provided demo concept, which aims to streamline onboarding by providing a single, intelligent point of contact for new employees. The solution leverages a supervisor agent to handle user interactions, a knowledge base for answering policy questions (RAG), and specialized collaborator agents for automating IT and HR tasks. This approach directly addresses the client's business need to reduce new hire time-to-productivity, decrease the manual workload on support teams, and deliver a modern, consistent onboarding experience.

## Prerequisites

Before beginning, ensure your development environment is set up correctly. This plan requires the following:

1.  **Python 3.9+**: The IBM watsonx Orchestrate Agent Development Kit (ADK) is a Python library.
2.  **IBM watsonx Orchestrate ADK**: The core library for building agents and tools. If not installed, run:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate CLI Environment**: You must have an active watsonx Orchestrate environment configured. Initialize it using:
    ```bash
    orchestrate env init
    ```
4.  **Project Directory Structure**: Create the following folder structure to organize all assets for the demo. This is crucial for keeping the configuration files, tools, and mock data organized.

    ```
    onboarding_buddy_demo/
    ├── agents/
    │   ├── Onboarding_Buddy_Agent.yaml
    │   ├── IT_Support_Agent.yaml
    │   └── HR_Benefits_Agent.yaml
    ├── knowledge/
    │   └── onboarding_kb.yaml
    ├── mock_data/
    │   ├── IBM_Remote_Work_Policy.pdf
    │   ├── New_Hire_FAQ.csv
    │   └── Benefits_Guide_2024.docx
    ├── tools/
    │   ├── it_support_tools.py
    │   └── hr_benefits_tools.py
    └── requirements.txt
    ```

## Step 1: Prepare Mock Data and Knowledge Base

The Onboarding Buddy's ability to answer general questions relies on a knowledge base populated with relevant documents. We will create mock documents and a YAML configuration to define this knowledge base.

### 1.1 Create Mock Data Files

Create the three files inside the `mock_data/` directory. For the demo, you can create simple text files and save them with the correct extensions (`.pdf`, `.csv`, `.docx`).

*   **`IBM_Remote_Work_Policy.pdf` (Sample Content):**
    > IBM offers flexible remote and hybrid work arrangements. The standard dress code for client-facing video calls is business casual. For internal meetings, the dress code is relaxed. All remote work must be conducted from your registered home address.

*   **`New_Hire_FAQ.csv` (Sample Content):**
    ```csv
    Question,Answer
    "How do I get paid?","Payroll is processed bi-weekly. You can set up direct deposit in the internal HR portal."
    "Where is the main office?","The main campus is located at 123 Enterprise Drive, Armonk, NY."
    "What is the company culture like?","IBM fosters a culture of innovation, collaboration, and continuous learning."
    ```

*   **`Benefits_Guide_2024.docx` (Sample Content):**
    > **Health Plan Comparison:**
    > **PPO Plan:** Higher monthly premium, lower deductible. Offers flexibility to see specialists without a referral. Co-pays are fixed for most services.
    > **HDHP Plan:** Lower monthly premium, higher deductible. Often paired with a Health Savings Account (HSA) to save for medical expenses tax-free. You pay the full cost of services until the deductible is met.

### 1.2 Configure the Knowledge Base

The knowledge base configuration file tells Orchestrate which documents to ingest into its built-in Milvus vector database.

**File:** `knowledge/onboarding_kb.yaml`

This YAML file defines the `onboarding_knowledge_base`. It specifies the document paths and the embedding model used to create vector representations of the text, enabling semantic search. This is the core of the RAG pattern.

```yaml
# knowledge/onboarding_kb.yaml
spec_version: v1
kind: knowledge_base
name: onboarding_knowledge_base
description: >
  Contains essential documents for new IBM employees, including company policies, FAQs, and benefits guides.
documents:
  - "mock_data/IBM_Remote_Work_Policy.pdf"
  - "mock_data/New_Hire_FAQ.csv"
  - "mock_data/Benefits_Guide_2024.docx"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Develop Python Tools

Tools are the executable components that allow agents to perform actions. We will create Python-based tools for the IT and HR collaborator agents, ensuring they generate realistic synthetic data.

### 2.1 Create IT Support Tools

**File:** `tools/it_support_tools.py`

This file contains functions for creating and checking IT support tickets. These tools simulate interaction with a service management system like ServiceNow. The `create_it_ticket` tool provides immediate confirmation with a unique ticket ID, a crucial feature for user experience. The `check_ticket_status` tool allows for follow-up, making the agent a persistent assistant.

```python
# tools/it_support_tools.py
import random
import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock database to store ticket information
MOCK_TICKET_DB = {}

@tool(name="create_it_ticket", permission=ToolPermission.ADMIN)
def create_it_ticket(issue_summary: str, employee_id: str) -> str:
    """
    Creates a new IT support ticket in the system for requests like hardware or software.

    Args:
        issue_summary (str): A brief, clear description of the IT issue or request (e.g., 'Request corporate laptop').
        employee_id (str): The unique ID of the employee making the request.

    Returns:
        str: The confirmation message including the new ticket number.
    """
    ticket_number = f"INC{random.randint(10000, 99999)}"
    creation_time = datetime.datetime.now().isoformat()
    
    MOCK_TICKET_DB[ticket_number] = {
        "employee_id": employee_id,
        "summary": issue_summary,
        "status": "New",
        "created_at": creation_time,
        "updated_at": creation_time
    }
    
    print(f"Creating ticket {ticket_number} for {employee_id} with summary: {issue_summary}")
    return f"Successfully created IT ticket {ticket_number} for your request: '{issue_summary}'."

@tool(name="check_ticket_status", permission=ToolPermission.ADMIN)
def check_ticket_status(ticket_number: str) -> str:
    """
    Checks the status of an existing IT support ticket.

    Args:
        ticket_number (str): The unique ticket number to check (e.g., 'INC12345').

    Returns:
        str: A message describing the current status of the ticket, or an error if not found.
    """
    if ticket_number in MOCK_TICKET_DB:
        ticket_data = MOCK_TICKET_DB[ticket_number]
        # Simulate status change for demo purposes
        if random.random() > 0.5 and ticket_data["status"] == "New":
            ticket_data["status"] = "In Progress"
            ticket_data["updated_at"] = datetime.datetime.now().isoformat()

        return f"Ticket {ticket_number} ('{ticket_data['summary']}') is currently in status: '{ticket_data['status']}'. Last updated: {ticket_data['updated_at']}."
    else:
        return f"Error: Ticket {ticket_number} not found in the system."
```

### 2.2 Create HR Benefits Tools

**File:** `tools/hr_benefits_tools.py`

This file contains functions for retrieving benefit plan details and initiating enrollment. The `get_benefit_plan_details` tool is essential for empowering new hires to make informed decisions by providing structured, comparable data. The `initiate_benefits_enrollment` tool automates the first step of a critical onboarding process, reducing administrative burden and accelerating the employee's setup.

```python
# tools/hr_benefits_tools.py
import random
import datetime
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_benefit_plan_details", permission=ToolPermission.ADMIN)
def get_benefit_plan_details(plan_type: str = "all") -> str:
    """
    Retrieves detailed information and a comparison of available health benefit plans.

    Args:
        plan_type (str, optional): The specific plan to inquire about ('PPO' or 'HDHP'). Defaults to 'all' for a comparison.

    Returns:
        str: A JSON string containing the details of the requested health plan(s).
    """
    plans = {
        "PPO": {
            "plan_name": "Premium PPO Plan",
            "monthly_premium": "$550",
            "annual_deductible": "$1,000",
            "out_of_pocket_max": "$4,000",
            "primary_care_copay": "$25",
            "specialist_copay": "$50",
            "summary": "Offers flexibility to see any doctor without a referral. Higher premiums but lower out-of-pocket costs for services."
        },
        "HDHP": {
            "plan_name": "High-Deductible Health Plan (HDHP) with HSA",
            "monthly_premium": "$250",
            "annual_deductible": "$3,000",
            "out_of_pocket_max": "$6,000",
            "primary_care_copay": "100% covered after deductible",
            "specialist_copay": "100% covered after deductible",
            "summary": "Lower premiums and the ability to contribute to a tax-advantaged Health Savings Account (HSA). You pay more upfront until the deductible is met."
        }
    }
    if plan_type.upper() in plans:
        return json.dumps({plan_type.upper(): plans[plan_type.upper()]})
    return json.dumps(plans)

@tool(name="initiate_benefits_enrollment", permission=ToolPermission.ADMIN)
def initiate_benefits_enrollment(employee_id: str, chosen_plan: str) -> str:
    """
    Initiates the benefits enrollment process for a new employee.

    Args:
        employee_id (str): The unique ID of the employee to enroll.
        chosen_plan (str): The plan the employee has chosen (e.g., 'PPO' or 'HDHP').

    Returns:
        str: A confirmation message with a reference number for the enrollment.
    """
    if chosen_plan.upper() not in ["PPO", "HDHP"]:
        return "Error: Invalid plan selected. Please choose either 'PPO' or 'HDHP'."
    
    enrollment_ref = f"ENR{random.randint(100000, 999999)}"
    print(f"Initiating enrollment for {employee_id} into {chosen_plan.upper()} plan. Reference: {enrollment_ref}")
    
    return f"Enrollment process initiated for plan '{chosen_plan.upper()}'. Your confirmation number is {enrollment_ref}. You will receive an email from HR with the next steps."
```

### 2.3 Create `requirements.txt`

This file lists any Python packages required by the tools. While our current tools only use standard libraries, it is a best practice to include this file. Real-world tools often use libraries like `requests` for API calls.

**File:** `requirements.txt`
```
# No external packages are required for these specific mock tools.
# If tools made API calls, you would add packages here, e.g.:
# requests
# python-dotenv
```

## Step 3: Configure Agents

With the tools defined, we now configure the agents. We will create two collaborator agents for specific tasks and one supervisor agent to orchestrate the work.

### 3.1 Configure the `IT_Support_Agent` (Collaborator)

**File:** `agents/IT_Support_Agent.yaml`

This agent is a specialist. Its description and instructions are tightly focused on IT tasks. This allows the supervisor agent to confidently delegate requests like "I need a laptop" to this agent.

```yaml
spec_version: v1
kind: native
name: IT_Support_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A specialized agent for handling IT support tasks for new employees. Use this agent to create and manage IT tickets for hardware requests (laptops, monitors), software access, and system setup issues.
instructions: >
  Your purpose is to resolve IT-related onboarding tasks.
  - When a user needs to request hardware or software, use the `create_it_ticket` tool.
  - If a user asks for the status of an existing request, use the `check_ticket_status` tool, but you must have a ticket number.
  - Be direct and provide the ticket number or status information clearly.
tools:
  - create_it_ticket
  - check_ticket_status
```

### 3.2 Configure the `HR_Benefits_Agent` (Collaborator)

**File:** `agents/HR_Benefits_Agent.yaml`

This agent is an expert on HR benefits. Its description clearly states its capabilities, enabling the supervisor to route complex questions about health plans to it for an accurate, tool-driven response.

```yaml
spec_version: v1
kind: native
name: HR_Benefits_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An expert agent focused on IBM's employee benefits programs. This agent can provide detailed comparisons of health plans (PPO vs. HDHP) and can start the benefits enrollment process for new hires.
instructions: >
  You are an HR benefits specialist.
  - For questions comparing health plans, use the `get_benefit_plan_details` tool to provide accurate, structured information. Format the JSON output into a user-friendly table or comparison list.
  - If a user decides on a plan and wants to enroll, use the `initiate_benefits_enrollment` tool.
  - Always be helpful and guide the new hire through their benefits options.
tools:
  - get_benefit_plan_details
  - initiate_benefits_enrollment
```

### 3.3 Configure the `Onboarding_Buddy_Agent` (Supervisor)

**File:** `agents/Onboarding_Buddy_Agent.yaml`

This is the main, user-facing agent. Its instructions define its core logic: first, try to answer questions using its knowledge base (RAG). If the user's request requires an action (like creating a ticket or enrolling in benefits), it must delegate the task to the appropriate collaborator. This supervisor pattern is key to building scalable and maintainable multi-agent systems.

```yaml
spec_version: v1
kind: native
name: Onboarding_Buddy_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  A friendly and helpful AI assistant for new IBM employees. Answers questions about company policies, culture, and benefits using the onboarding knowledge base. Collaborates with IT and HR agents to complete tasks.
instructions: >
  Your primary goal is to assist new hires. First, try to answer questions using your knowledge base. If a user needs to perform an action related to IT (like getting a laptop or software), delegate to the `IT_Support_Agent`. If a user has a detailed question about health plans or wants to enroll in benefits, delegate to the `HR_Benefits_Agent`.
collaborators:
  - IT_Support_Agent
  - HR_Benefits_Agent
knowledge_base:
  - onboarding_knowledge_base
```

## Step 4: Deploy and Run the Solution

With all assets created, deploy them to watsonx Orchestrate using the ADK CLI. The order of operations is critical: dependencies like tools and knowledge bases must be imported before the agents that use them.

Execute these commands from the root `onboarding_buddy_demo/` directory.

```bash
# 1. Import the Python-based tools for both agents
echo "Importing IT Support tools..."
orchestrate tools import -f tools/it_support_tools.py

echo "Importing HR Benefits tools..."
orchestrate tools import -f tools/hr_benefits_tools.py

# 2. Import the knowledge base containing the mock onboarding documents
echo "Importing knowledge base..."
orchestrate knowledgebases import -f knowledge/onboarding_kb.yaml

# 3. Import the collaborator agents (these must exist before the supervisor can reference them)
echo "Importing collaborator agents..."
orchestrate agents import -f agents/IT_Support_Agent.yaml
orchestrate agents import -f agents/HR_Benefits_Agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/Onboarding_Buddy_Agent.yaml

# 5. Start the chat interface to interact with the supervisor agent
echo "Starting chat with the Onboarding Buddy..."
orchestrate chat start --agent Onboarding_Buddy_Agent
```

## Verification

After starting the chat, test the three core demo scenarios outlined in the client concept to verify that the RAG and agent delegation patterns are working correctly.

*   **Scenario 1: Simple Knowledge Retrieval (RAG)**
    *   **User Input:** `What is IBM's dress code policy?`
    *   **Expected Behavior:** The `Onboarding_Buddy_Agent` should query its `onboarding_knowledge_base`, find the relevant information in the `IBM_Remote_Work_Policy.pdf` document, and generate a natural language answer like: "The standard dress code for client-facing video calls is business casual. For internal meetings, the dress code is more relaxed."

*   **Scenario 2: Task Orchestration & Collaboration (IT)**
    *   **User Input:** `I need to request my corporate laptop.`
    *   **Expected Behavior:** The `Onboarding_Buddy_Agent` will recognize this as an IT task and delegate to the `IT_Support_Agent`. The IT agent will call the `create_it_ticket` tool. The final response to the user should be: "I've created IT ticket #INC... for your laptop request. You will receive updates shortly."

*   **Scenario 3: Complex Inquiry & Collaboration (HR)**
    *   **User Input:** `Can you explain the differences between the PPO and HDHP health plans?`
    *   **Expected Behavior:** The `Onboarding_Buddy_Agent` will route this request to the `HR_Benefits_Agent`. The HR agent will use its `get_benefit_plan_details` tool to retrieve the structured data and present a clear comparison, likely formatted as a markdown table or a list, summarizing the differences in premiums, deductibles, and coverage.

## Troubleshooting

*   **Agent Not Found Error:** If you get an error that a collaborator agent is not found when importing the supervisor, ensure you have imported the collaborator agents (`IT_Support_Agent`, `HR_Benefits_Agent`) *before* the `Onboarding_Buddy_Agent`.
*   **Tool Not Found Error:** If an agent fails to use a tool, double-check that the tool names in the agent's YAML file exactly match the `name` parameter in the `@tool` decorator in the Python files.
*   **Incorrect Agent Delegation:** If the supervisor agent tries to answer an IT/HR question itself instead of delegating, refine the `instructions` in the `Onboarding_Buddy_Agent.yaml`. Make the delegation logic more explicit, e.g., "If the user mentions 'laptop', 'software', or 'ticket', you MUST use the `IT_Support_Agent`."
*   **Knowledge Base Not Working:** If the agent can't answer questions from the documents, verify the file paths in `onboarding_kb.yaml` are correct relative to where you are running the `orchestrate` command. Re-import the knowledge base if you make changes to the source documents.

## Best Practices

*   **Clear Agent Descriptions**: The supervisor agent relies heavily on the collaborator agents' `description` fields to decide where to route a task. Write clear, concise, and keyword-rich descriptions that accurately reflect each agent's capabilities.
*   **Explicit Instructions**: For supervisor agents, provide explicit instructions on when to delegate to a specific collaborator. Use clear trigger phrases or scenarios to guide the LLM's reasoning process.
*   **Modular Tool Design**: Keep Python files for tools organized by domain (e.g., `it_support_tools.py`, `hr_benefits_tools.py`). This makes the solution easier to maintain and scale as you add more capabilities.
*   **Idempotent Tools**: Design tools to be safely re-run without causing negative side effects. For example, if a `create_it_ticket` tool were called twice for the same request, it should ideally identify the duplicate rather than creating a second ticket.
*   **State Management**: For more complex interactions (like a multi-step process), consider how to manage state. While our example is stateless, real-world applications might require tools to read from and write to an external database or cache to track progress.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
