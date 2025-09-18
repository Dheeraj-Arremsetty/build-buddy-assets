# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 15:07:04
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Barista Onboarding Concierge

## Overview
This execution plan provides a comprehensive, step-by-step guide to building the "AI-Powered Barista Onboarding Concierge" for Starbucks using IBM watsonx Orchestrate. This updated plan incorporates best practices and refines the implementation based on expert review. The objective is to create a multi-agent Proof of Concept (POC) that streamlines the new hire onboarding process. This solution will act as a single, intelligent point of contact for new Starbucks partners (employees), efficiently routing their diverse requests—from IT support and HR documentation to operational knowledge—to specialized agents. By automating responses to common onboarding questions, this solution directly addresses the client's goal of reducing the administrative burden on store managers and HR personnel, accelerating a new partner's time-to-productivity, and enhancing the overall onboarding experience.

The architecture leverages a Supervisor/Collaborator pattern, a core strength of watsonx Orchestrate. A central `Partner_Onboarding_Concierge` agent will intelligently delegate tasks to three specialized collaborator agents: an `IT_Support_Agent` for creating service tickets, an `HR_Forms_Agent` for retrieving document links, and a `Barista_Knowledge_Agent` for answering procedural questions using a knowledge base (Retrieval-Augmented Generation - RAG). This plan details the creation of all mock data, Python tools, knowledge bases, and agent configurations, culminating in a fully deployable and testable solution that demonstrates significant business value.

## Prerequisites
Before beginning, ensure your development environment is correctly configured. This is essential for a smooth build and deployment process.

1.  **Python Environment**: A working installation of Python 3.9 or later is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves logging in and setting the target environment using the ADK CLI.
    ```bash
    # Log in to your watsonx Orchestrate environment
    orchestrate login

    # List available environments and set your target
    orchestrate env list
    orchestrate env use <your_environment_name>
    ```
4.  **Text Editor/IDE**: A code editor like Visual Studio Code is recommended for creating and editing Python, YAML, and other configuration files.

## Step 1: Project Setup and Mock Data Creation
A well-organized project structure is key. We will first create the necessary directories and the synthetic data files that our tools and knowledge base will rely on.

**Action:** Create the following directory structure in your project folder:

```
starbucks_onboarding_poc/
├── agents/
│   ├── partner_onboarding_concierge.yaml
│   ├── it_support_agent.yaml
│   ├── hr_forms_agent.yaml
│   └── barista_knowledge_agent.yaml
├── knowledge_base/
│   ├── barista_handbook_kb.yaml
│   └── documents/
│       └── Starbucks_Recipe_Guide.pdf
├── tools/
│   ├── it_support_tool.py
│   └── hr_forms_tool.py
├── mock_data/
│   └── hr_forms.json
└── requirements.txt
```

---

### 1.1 Create Mock HR Forms Data
This JSON file will be used by the `HR_Forms_Agent`'s tool to look up links to essential documents.

**Action:** Create the file `mock_data/hr_forms.json` with the following content:

```json
{
  "forms": [
    {
      "form_name": "Direct Deposit Form",
      "keywords": ["direct deposit", "banking", "paycheck", "payment"],
      "url": "https://hr.starbucks.internal/forms/direct-deposit-dd101"
    },
    {
      "form_name": "W-4 Tax Form",
      "keywords": ["w4", "w-4", "tax", "withholding"],
      "url": "https://hr.starbucks.internal/forms/tax-w4-2024"
    },
    {
      "form_name": "I-9 Employment Eligibility Verification",
      "keywords": ["i9", "i-9", "eligibility", "employment verification"],
      "url": "https://hr.starbucks.internal/forms/i9-verification"
    },
    {
      "form_name": "Health Insurance Enrollment",
      "keywords": ["health", "medical", "insurance", "benefits"],
      "url": "https://hr.starbucks.internal/benefits/health-enrollment"
    },
    {
      "form_name": "Partner Handbook Acknowledgment",
      "keywords": ["handbook", "policy", "rules", "acknowledgment"],
      "url": "https://hr.starbucks.internal/forms/partner-handbook-ack"
    }
  ]
}
```

---

### 1.2 Create Mock Knowledge Base Document
This PDF document is the source of truth for the `Barista_Knowledge_Agent`. For this demo, we will create a text file and save it as a PDF.

**Action:** Create a new document using any word processor, paste the text below, and save it as `knowledge_base/documents/Starbucks_Recipe_Guide.pdf`.

```text
Starbucks Partner Onboarding: Recipe & Procedure Guide

**Section 1: Core Recipes**

*How to make a grande Caramel Macchiato:*
1.  Queue 2 shots of espresso.
2.  Pump 3 pumps of Vanilla Syrup into a grande-sized cup.
3.  Steam 2% milk to the appropriate temperature (150-160°F).
4.  Pour the steamed milk into the cup, holding back the foam with a spoon.
5.  Pour the espresso shots slowly over the top of the milk. The shots should "mark" the foam.
6.  Top with caramel drizzle in a crosshatch pattern, then circle the edge twice.

*How to make a tall Pumpkin Spice Latte:*
1.  Queue 1 shot of espresso.
2.  Pump 3 pumps of Pumpkin Spice Sauce into a tall-sized cup.
3.  Steam 2% milk with the sauce.
4.  Pour the steamed milk and espresso into the cup simultaneously.
5.  Top with whipped cream and pumpkin spice topping.

**Section 2: Standard Procedures**

*How to clean the espresso machine (end-of-day):*
1.  Press the "rinse" button to flush the group heads.
2.  Insert the blind filter basket into the portafilter.
3.  Add one Cafiza cleaning tablet to the blind filter.
4.  Lock the portafilter into the group head and run a 10-second brew cycle. Repeat 5 times.
5.  Remove the portafilter, rinse, and re-insert. Run another 5 10-second cycles with just water to rinse.
6.  Wipe down the machine exterior, steam wands, and drip tray.

*Procedure for handling a customer complaint:*
1.  Listen actively and empathetically to the customer's concern.
2.  Apologize for the experience, even if you are not at fault.
3.  Offer a solution. The LATTE model: Listen, Apologize, Take action, Thank, Ensure satisfaction.
4.  If needed, involve the shift supervisor for assistance.
```

---

### 1.3 Create `requirements.txt`
This file lists the Python packages our tools depend on. In this case, none are needed, but including the file is a best practice for project structure.

**Action:** Create the file `requirements.txt` with the following content:

```
# No external packages are needed for this demo's tools.
# This file is included for best practice.
```

## Step 2: Create the Knowledge Base Configuration
The `Barista_Knowledge_Agent` will use a built-in Milvus knowledge base to answer questions. This YAML file defines the knowledge base, pointing to the PDF document we just created. This demonstrates the powerful RAG pattern in watsonx Orchestrate.

**Business Value:** This component allows new hires to get instant, accurate answers to procedural questions by querying official documentation in natural language, reducing their reliance on asking managers or senior partners and ensuring operational consistency.

**Action:** Create the file `knowledge_base/barista_handbook_kb.yaml` with the following content:

```yaml
spec_version: v1
kind: knowledge_base
name: barista_handbook_kb
description: >
   Contains official Starbucks recipes for popular drinks, standard store procedures for cleaning equipment, and operational guidelines for baristas. Use this to answer any 'how-to' questions related to a barista's daily tasks.
documents:
   - "knowledge_base/documents/Starbucks_Recipe_Guide.pdf"
vector_index:
   # Using the default watsonx.ai embedding model for simplicity and performance.
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Create Python Tools
Here, we will create the Python functions that will be exposed as tools to our agents. Each tool performs a specific, discrete action and is built following production-level best practices, including proper logging and clean code.

### 3.1 IT Support Tool
**Purpose & Business Value:** The `create_it_ticket` tool simulates an integration with an IT Service Management (ITSM) system like ServiceNow. It allows the `IT_Support_Agent` to automate the creation of support tickets for common new hire issues (e.g., login problems, hardware failures). This provides immediate confirmation to the new hire and formally logs the issue for the IT department, reducing resolution time and manual data entry.

**Technical Implementation:** This Python function takes a string describing the IT issue as input. It uses the `random` library to generate a unique, synthetic ticket number prefixed with "SBX-". It then returns a formatted string confirming the ticket creation. Crucially, this updated version uses Python's `logging` module instead of `print()` for traceability in a server environment, and removes unused imports for cleaner code.

**Action:** Create the file `tools/it_support_tool.py` with the following content:

```python
import random
import logging
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@tool(name="create_it_ticket", description="Creates an IT support ticket for hardware or software issues.")
def create_it_ticket(issue_description: str) -> str:
    """Creates an IT support ticket in the internal tracking system.
    Use this for any issues related to logging in, cash register (POS) problems,
    or broken equipment.

    Args:
        issue_description (str): A clear and concise description of the IT problem the user is facing.

    Returns:
        str: A confirmation message including the newly created ticket number.
    """
    if not issue_description or not isinstance(issue_description, str):
        return "Error: A description of the issue is required to create a ticket."

    # Simulate API call to a ticketing system and generate a ticket number
    ticket_id = f"SBX-{random.randint(70000, 99999)}"
    
    # Use logging for server-side traceability instead of print()
    logging.info(f"Generated IT Ticket: {ticket_id} for issue: '{issue_description}'")

    return f"Success! I've created an IT support ticket for you. The reference number is #{ticket_id}. A technician will be in touch shortly."
```

### 3.2 HR Forms Tool
**Purpose & Business Value:** The `get_hr_form_link` tool provides a direct and efficient way for new hires to access critical HR documents. The `HR_Forms_Agent` uses this tool to search a centralized data source (our mock JSON file) for the correct form link. This eliminates the need for new hires to navigate complex internal portals or ask HR personnel for common forms, saving time for everyone and ensuring employees get the correct, up-to-date documents.

**Technical Implementation:** This Python function takes a search term (the form name) as input. It opens and reads the `mock_data/hr_forms.json` file. It then iterates through the list of forms, checking if the user's query matches the `form_name` or any of the associated `keywords` for more robust searching. If a match is found, it returns the form name and its URL. This version includes robust error handling and has been cleaned to remove unused imports.

**Action:** Create the file `tools/hr_forms_tool.py` with the following content:

```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="get_hr_form_link", description="Finds the URL for a specific HR document or form.")
def get_hr_form_link(form_name: str) -> str:
    """Searches the HR document directory to find a direct link to a requested form.

    Args:
        form_name (str): The name of the HR form to find, for example 'direct deposit' or 'W-4'.

    Returns:
        str: A message containing the link to the form, or a message indicating the form was not found.
    """
    try:
        with open('mock_data/hr_forms.json', 'r') as f:
            data = json.load(f)
        
        query = form_name.lower()
        
        for form in data['forms']:
            # Check against the main name and a list of keywords for better matching
            if query in form['form_name'].lower() or any(keyword in query for keyword in form['keywords']):
                return f"You can find the '{form['form_name']}' here: {form['url']}"

        return f"I'm sorry, I couldn't find a form matching '{form_name}'. Please try a different name or check the partner hub."

    except FileNotFoundError:
        return "Error: The HR forms directory could not be accessed. Please contact support."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
```

## Step 4: Create Agent Configurations
Now we will define our four agents in YAML. The descriptions and instructions are critical, especially for the supervisor agent, as they guide the LLM's decision-making process for routing requests.

*Note on Model Selection: For all agents, we will use `watsonx/ibm/granite-13b-chat-v2`. This model is selected for its strong balance of performance, efficiency, and reasoning capabilities, making it well-suited for both the nuanced routing decisions of the supervisor and the tool-use/RAG tasks of the collaborators.*

### 4.1 IT Support Agent (Collaborator)
**Action:** Create `agents/it_support_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: it_support_agent
description: >
  An agent specializing in IT support for Starbucks partners. Use this agent exclusively for creating IT help desk tickets for issues related to hardware (like cash registers, printers, headsets) or software (like login problems, application errors, password resets). It has a tool to directly create a ticket in the system.
instructions: >
  Your sole purpose is to create IT support tickets. When a user describes a technical problem, use the 'create_it_ticket' tool with the user's description of the problem as the input. Relay the confirmation message from the tool back to the user. Be direct and helpful.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - create_it_ticket
```

### 4.2 HR Forms Agent (Collaborator)
**Action:** Create `agents/hr_forms_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: hr_forms_agent
description: >
  An agent that assists Starbucks partners by providing direct links to Human Resources (HR) forms and documents. Use this agent when a user asks for a specific form like 'direct deposit form', 'W-4', or 'I-9'. It can search the HR directory to find the correct URL.
instructions: >
  Your goal is to provide links to HR forms. When a user asks for a form, use the 'get_hr_form_link' tool with the name of the form as the input. Return the exact response from the tool to the user. If the form is not found, relay that information clearly.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - get_hr_form_link
```

### 4.3 Barista Knowledge Agent (Collaborator)
**Action:** Create `agents/barista_knowledge_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: barista_knowledge_agent
description: >
  An expert agent on Starbucks operational procedures and drink recipes. Use this agent to answer 'how-to' questions from baristas. It has access to the official 'Barista Recipe & Procedure Guide' knowledge base, which contains step-by-step instructions for making drinks and performing standard tasks like cleaning equipment.
instructions: >
  You are a helpful knowledge expert for baristas. When a user asks a question about how to do something, search your knowledge base for the answer. Provide clear, step-by-step instructions based on the information you find in the guide. If you cannot find an answer, state that the information is not in your knowledge base.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
knowledge_base:
  - barista_handbook_kb
```

### 4.4 Partner Onboarding Concierge (Supervisor)
**Action:** Create `agents/partner_onboarding_concierge.yaml`:
```yaml
spec_version: v1
kind: native
name: partner_onboarding_concierge
description: >
  A primary contact and intelligent router for new Starbucks partners. This agent understands a new hire's request and delegates it to the correct specialist agent: IT_Support_Agent for technical issues, HR_Forms_Agent for documents, or Barista_Knowledge_Agent for recipe/procedure questions. It has no tools of its own.
instructions: >
  You are a concierge for new Starbucks employees. Your only job is to route requests. Do not attempt to answer questions yourself.
  Carefully analyze the user's request to determine their intent.

  Reasoning:
  - If the request is about a broken device, login issue, password problem, or anything technical, delegate to the 'it_support_agent'.
  - If the request is about finding a form, a document, or anything related to HR paperwork (like 'direct deposit', 'W-4', 'I-9'), delegate to the 'hr_forms_agent'.
  - If the request is a 'how-to' question about making a drink, cleaning equipment, or a store procedure, delegate to the 'barista_knowledge_agent'.
  - If the intent is unclear, ask the user for clarification.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
collaborators:
  - it_support_agent
  - hr_forms_agent
  - barista_knowledge_agent
```

## Step 5: Deployment using ADK CLI
With all artifacts created, we will now use the `orchestrate` CLI to import them into the watsonx Orchestrate platform. The order of operations is crucial: we must import dependencies (tools, knowledge bases) before the agents that use them, and we must import collaborator agents before the supervisor agent that orchestrates them.

**Action:** Open your terminal, navigate to the root of your `starbucks_onboarding_poc` project directory, and run the following commands in sequence:

1.  **Import Tools:**
    ```bash
    echo "Importing IT Support Tool..."
    orchestrate tools import -k python -f tools/it_support_tool.py

    echo "Importing HR Forms Tool..."
    orchestrate tools import -k python -f tools/hr_forms_tool.py
    ```

2.  **Import Knowledge Base:**
    ```bash
    echo "Importing Barista Handbook Knowledge Base..."
    orchestrate knowledge_bases import -f knowledge_base/barista_handbook_kb.yaml
    ```

3.  **Import Collaborator Agents:**
    ```bash
    echo "Importing IT Support Agent..."
    orchestrate agents import -f agents/it_support_agent.yaml

    echo "Importing HR Forms Agent..."
    orchestrate agents import -f agents/hr_forms_agent.yaml

    echo "Importing Barista Knowledge Agent..."
    orchestrate agents import -f agents/barista_knowledge_agent.yaml
    ```

4.  **Import Supervisor Agent:**
    ```bash
    echo "Importing Partner Onboarding Concierge (Supervisor)..."
    orchestrate agents import -f agents/partner_onboarding_concierge.yaml
    ```

## Verification
After successful deployment, you can verify the solution by interacting with the supervisor agent in the Orchestrate chat.

**Action:** Start the chat interface and test the three primary demo scenarios.

1.  **Start the Chat:**
    ```bash
    orchestrate chat start -a partner_onboarding_concierge
    ```
    This will open a chat window in your browser connected to your supervisor agent.

2.  **Test Scenario 1 (IT Automation):**
    *   **User Input:** `I can't log into the cash register.`
    *   **Expected Behavior:** The `Partner_Onboarding_Concierge` should identify this as an IT issue and delegate to the `IT_Support_Agent`. The `IT_Support_Agent` will then use its tool.
    *   **Expected Output:** `Success! I've created an IT support ticket for you. The reference number is #SBX-XXXXX. A technician will be in touch shortly.` (The ticket number will be random).

3.  **Test Scenario 2 (HR Information Retrieval):**
    *   **User Input:** `Where do I find the form for direct deposit?`
    *   **Expected Behavior:** The supervisor should route this to the `HR_Forms_Agent`.
    *   **Expected Output:** `You can find the 'Direct Deposit Form' here: https://hr.starbucks.internal/forms/direct-deposit-dd101`

4.  **Test Scenario 3 (Knowledge Base Query):**
    *   **User Input:** `What are the steps to make a grande Caramel Macchiato?`
    *   **Expected Behavior:** The supervisor should route this to the `Barista_Knowledge_Agent`, which will query the PDF in its knowledge base.
    *   **Expected Output:** A message containing the step-by-step instructions from the PDF, such as:
        `To make a grande Caramel Macchiato, follow these steps: 1. Queue 2 shots of espresso. 2. Pump 3 pumps of Vanilla Syrup into a grande-sized cup...`

## Troubleshooting
-   **Incorrect Routing:** If the supervisor agent delegates to the wrong collaborator, review the `description` and `instructions` in all agent YAML files. The supervisor relies heavily on the collaborator descriptions to make its choice. Ensure they are distinct and accurately describe each agent's capabilities.
-   **Tool Not Found:** If an agent reports it cannot find a tool, ensure the tool was imported successfully *before* the agent. Check for typos in the `tools` section of the agent's YAML file.
-   **Knowledge Base Failure:** If the `Barista_Knowledge_Agent` cannot answer questions, verify that the `barista_handbook_kb.yaml` was imported successfully and that the file path in the `documents` section is correct relative to where you are running the command. You can check the status of the knowledge base ingestion using the CLI.
-   **Python Tool Errors:** If a tool fails during execution, check the terminal where you ran the ADK commands for Python error messages. This could indicate an issue in the tool's code, like a `FileNotFoundError` for the JSON file. Ensure the mock data files are in the correct location.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
