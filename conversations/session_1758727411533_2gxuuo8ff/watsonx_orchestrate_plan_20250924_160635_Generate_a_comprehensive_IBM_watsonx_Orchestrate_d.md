# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-24 16:06:35
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Delta AeroAssist

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **Delta AeroAssist** proof-of-concept for Delta Airlines using IBM watsonx Orchestrate. The plan is tailored to address Delta's core business challenges of minimizing Aircraft on Ground (AOG) time, enhancing safety and compliance, and improving crew efficiency. We will construct a multi-agent system featuring a supervisor agent that intelligently routes tasks to specialized agents for maintenance and flight crew operations. These specialized agents will leverage Retrieval-Augmented Generation (RAG) to provide sourced answers from technical manuals and use custom tools to automate key operational tasks, demonstrating a direct path to significant business value.

## Prerequisites

Before starting, ensure your development environment is correctly configured.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
2.  **Python Environment**: A working Python environment (version 3.10 or higher) is required.
3.  **IBM Cloud Account**: An active IBM Cloud account is needed to access watsonx.ai models.
4.  **Environment Initialization**: You must have an active watsonx Orchestrate environment initialized using the ADK CLI.
    ```bash
    # Set up your environment (follow interactive prompts)
    orchestrate env add
    
    # Set the current environment as active
    orchestrate env use <your_env_name>
    ```
5.  **Mock Data Files**: The demo relies on synthetic documents. Create a directory named `mock_data` and place the following (empty or mock-content) files inside it. For a realistic demo, populate them with relevant sample text.
    *   `mock_data/A321_AMM.pdf`: A mock Aircraft Maintenance Manual for the Airbus A321.
    *   `mock_data/A321_FCOM.pdf`: A mock Flight Crew Operating Manual for the Airbus A321.
    *   `mock_data/Safety_Compliance_Regs.txt`: A text file with mock FAA regulations.

## Step 1: Create the Knowledge Bases

First, we will define the knowledge bases that will provide the specialized agents with grounded, factual information from Delta's operational documents. This is the foundation of the RAG pattern, enabling agents to answer questions with high accuracy and provide citations.

### 1.1 Maintenance Manuals Knowledge Base

This knowledge base will ingest the Aircraft Maintenance Manual (AMM) and compliance documents, making them searchable for the `Maintenance_Technician_Agent`.

Create a file named `maintenance_kb.yaml`:
```yaml
spec_version: v1
kind: knowledge_base 
name: Maintenance_Manuals_KB
description: >
   Contains technical specifications, troubleshooting procedures, and fault code references from the Airbus A321 Aircraft Maintenance Manual (AMM) and safety compliance regulations. Used by the Maintenance Technician Agent.
documents:
   - "mock_data/A321_AMM.pdf"
   - "mock_data/Safety_Compliance_Regs.txt"
vector_index:
   # Uses the default and recommended watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### 1.2 Flight Operations Knowledge Base

This knowledge base will ingest the Flight Crew Operating Manual (FCOM), providing the `Flight_Crew_Agent` with access to standard procedures and checklists.

Create a file named `flight_ops_kb.yaml`:
```yaml
spec_version: v1
kind: knowledge_base 
name: Flight_Operations_KB
description: >
   Contains flight operating manuals (FCOM), emergency procedures, and safety checklists for the Airbus A321. Used by the Flight Crew Agent for pre-flight and in-flight procedure verification.
documents:
   - "mock_data/A321_FCOM.pdf"
   - "mock_data/Safety_Compliance_Regs.txt"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Develop Python Tools

Next, we will create the custom Python tools that allow the agents to perform actions, such as logging maintenance issues or retrieving specific procedures. These tools bridge the gap between conversational AI and backend operational systems.

### 2.1 Maintenance Tool (`log_maintenance_issue`)

**Business Value:** This tool automates the critical first step in the maintenance process. By allowing a technician to log an issue via natural language, it reduces administrative overhead, minimizes data entry errors, and ensures that issues are tracked immediately, accelerating the repair lifecycle and reducing AOG time.

**Technical Implementation:** The tool uses Python's `Enum` to enforce structured input for priority levels, ensuring data consistency. It simulates a call to a maintenance ticketing system (like ServiceNow or a custom backend) and returns a unique ticket ID, providing immediate confirmation to the user.

Create a file named `maintenance_tools.py`:
```python
# maintenance_tools.py
import random
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Priority(str, Enum):
    """Enumeration for maintenance issue priority levels."""
    P1 = 'Priority 1 (Critical - AOG)'
    P2 = 'Priority 2 (High)'
    P3 = 'Priority 3 (Medium)'
    P4 = 'Priority 4 (Low)'

@tool(name="log_maintenance_issue", permission=ToolPermission.ADMIN)
def log_maintenance_issue(description: str, priority: Priority, aircraft_tail_number: str) -> str:
    """
    Creates a new maintenance issue ticket in the central tracking system.

    Args:
        description (str): A detailed description of the maintenance issue observed.
        priority (Priority): The priority level of the issue, e.g., 'Priority 1 (Critical - AOG)'.
        aircraft_tail_number (str): The tail number of the aircraft requiring maintenance, e.g., 'N301DN'.

    Returns:
        str: A confirmation message with the newly created ticket number.
    """
    # In a real-world scenario, this function would make an API call to a system like ServiceNow or JIRA.
    # For this demo, we simulate the API call and generate a mock ticket number.
    print(f"Connecting to maintenance backend...")
    ticket_id = f"MX-{random.randint(10000, 99999)}"
    print(f"Creating ticket {ticket_id} for aircraft {aircraft_tail_number} with priority {priority.value} and description: '{description}'")
    
    # Return a user-friendly confirmation message
    return f"Successfully created maintenance ticket {ticket_id} for aircraft {aircraft_tail_number}."

```

### 2.2 Flight Crew Tool (`get_preflight_procedure`)

**Business Value:** This tool provides flight crews with instant, unambiguous access to critical procedures. It eliminates the need to manually search through lengthy PDF manuals during high-pressure pre-flight or irregular operations. This enhances safety, ensures procedural compliance, and improves on-time performance by speeding up checklist verification.

**Technical Implementation:** This tool simulates a lookup in a structured database or API that houses standardized operational procedures. It takes a procedure name as an input and returns a detailed, step-by-step checklist in a clear, readable format. The data is structured to be easily parsed and displayed by the agent.

Create a file named `flight_crew_tools.py`:
```python
# flight_crew_tools.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock database of pre-flight procedures
PROCEDURE_DATABASE = {
    "de-icing_communications_check": {
        "name": "De-Icing Communications Check",
        "source": "FCOM Vol 2, Section 5.3, Page 12",
        "steps": [
            "1. Establish communication with de-icing crew on designated frequency.",
            "2. Confirm aircraft type and tail number.",
            "3. State the required de-icing fluid type (e.g., Type I, Type IV).",
            "4. Verbally confirm critical surfaces to be treated (wings, tail, stabilizers).",
            "5. Receive confirmation from de-icing crew that procedure is understood.",
            "6. Await 'De-icing complete' call before continuing pre-flight."
        ]
    },
    "cold_weather_engine_start": {
        "name": "Cold Weather Engine Start Procedure (OAT < 0°C)",
        "source": "FCOM Vol 1, Section 3.2, Page 45",
        "steps": [
            "1. Verify engine oil quantity is within limits.",
            "2. Ensure APU bleed is ON.",
            "3. Set Engine Start selectors to IGN/START.",
            "4. Monitor N2 rotation; must be at least 20% before introducing fuel.",
            "5. At 20% N2, move Engine Master Switch to ON.",
            "6. Monitor EGT, N1, and oil pressure for normal parameters during start sequence."
        ]
    }
}

@tool(name="get_preflight_procedure", permission=ToolPermission.ADMIN)
def get_preflight_procedure(procedure_name: str) -> str:
    """
    Retrieves a specific, step-by-step pre-flight procedure from the operations manual.

    Args:
        procedure_name (str): The standardized name of the procedure to retrieve, e.g., 'de-icing_communications_check' or 'cold_weather_engine_start'.

    Returns:
        str: A JSON string containing the detailed procedure steps and source reference, or a message if not found.
    """
    # Normalize the input to handle variations
    lookup_key = procedure_name.lower().replace(" ", "_")
    
    procedure = PROCEDURE_DATABASE.get(lookup_key)
    
    if procedure:
        return json.dumps(procedure, indent=2)
    else:
        return json.dumps({"error": "Procedure not found.", "available_procedures": list(PROCEDURE_DATABASE.keys())})

```

## Step 3: Define the Agents

Now we will define the three agents that form the core of the AeroAssist architecture. We will use the supervisor agent pattern, where a primary agent routes tasks to specialized collaborators based on their descriptions.

### 3.1 Maintenance Technician Agent

This is a specialized agent for ground crews. It uses the `Maintenance_Manuals_KB` for RAG and the `log_maintenance_issue` tool for actions.

Create a file named `maintenance_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: Maintenance_Technician_Agent
llm: watsonx/ibm/granite-13b-chat-v2 # Using a powerful model for technical reasoning
style: default
description: >
    An expert agent for aircraft maintenance technicians. Use this agent for troubleshooting technical issues, understanding fault codes from manuals, and logging maintenance work orders into the system. It has access to detailed Aircraft Maintenance Manuals (AMM) and safety regulations.
instructions: >
    Persona: You are an expert AI assistant for certified Delta maintenance technicians. Be precise, technical, and direct.
    
    Reasoning:
    - When asked to troubleshoot an issue or look up a fault code, use your knowledge base.
    - When answering from your knowledge base, ALWAYS cite the source document and page number if available.
    - When a user asks to log, create, or file an issue, use the 'log_maintenance_issue' tool.
    - Before using the tool, ensure you have a clear description, a priority level, and the aircraft tail number from the user. If any are missing, ask for them.
    - After using the tool, confirm the ticket number back to the user.
collaborators: []
tools:
  - log_maintenance_issue
knowledge_base:
  - Maintenance_Manuals_KB
```

### 3.2 Flight Crew Agent

This is a specialized agent for pilots and flight attendants. It uses the `Flight_Operations_KB` for RAG and the `get_preflight_procedure` tool for specific lookups.

Create a file named `flight_crew_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: Flight_Crew_Agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
    An expert assistant for Delta flight crews (pilots and flight attendants). Use this agent to get quick access to flight operating manuals (FCOM), verify standard operating procedures, check emergency protocols, and review crew compliance regulations like rest requirements.
instructions: >
    Persona: You are a reliable co-pilot assistant. Your responses must be clear, concise, and adhere strictly to official procedures. Safety is the top priority.
    
    Reasoning:
    - For general questions about procedures or regulations, search your knowledge base. Always cite the source document and section.
    - If a user asks for the exact steps of a specific, named procedure like 'de-icing check', use the 'get_preflight_procedure' tool for the most accurate, structured checklist.
    - Do not provide advice or opinions; only provide information from your official knowledge base or tools.
collaborators: []
tools:
  - get_preflight_procedure
knowledge_base:
  - Flight_Operations_KB
```

### 3.3 AeroAssist Supervisor Agent

This is the main entry point for the user. It has no tools or knowledge of its own. Its sole purpose is to understand the user's intent and delegate the task to the correct collaborator agent based on their `description`.

Create a file named `supervisor_agent.yaml`:
```yaml
spec_version: v1
kind: native
name: AeroAssist_Supervisor
llm: watsonx/meta-llama/llama-3-70b-instruct # A large model is best for complex routing
style: default
description: >
    The primary assistant for Delta Airlines operations, named AeroAssist. It acts as an intelligent supervisor that routes user requests to specialized agents for either maintenance tasks or flight crew procedures.
instructions: >
    Persona: You are AeroAssist, the central AI for Delta operations. Your primary role is to understand who can best help the user and delegate the task.
    
    Context:
    - You have two specialized assistants available: Maintenance_Technician_Agent and Flight_Crew_Agent.
    - The Maintenance_Technician_Agent handles technical troubleshooting, fault codes, and logging repair tickets.
    - The Flight_Crew_Agent handles flight procedures, checklists, and crew regulations.
    
    Reasoning:
    - Analyze the user's request to determine if it relates to maintenance or flight operations.
    - If the request involves fixing the aircraft, technical manuals (AMM), or logging issues, delegate to the 'Maintenance_Technician_Agent'.
    - If the request involves flying the aircraft, operating procedures (FCOM), checklists, or crew rules, delegate to the 'Flight_Crew_Agent'.
    - Do not attempt to answer questions yourself. Always delegate to the appropriate collaborator.
collaborators:
  - Maintenance_Technician_Agent
  - Flight_Crew_Agent
tools: []
knowledge_base: []
```

## Step 4: Create `requirements.txt`

To ensure all dependencies for the Python tools are available, create a `requirements.txt` file. For this demo, no external libraries are needed beyond the ADK itself, but it's a best practice to have this file.

Create a file named `requirements.txt`:
```text
# No external dependencies required for these specific tools.
# If tools used libraries like 'requests' or 'pandas', they would be listed here.
# e.g.
# requests
```

## Step 5: Deploy the Solution with ADK CLI

With all configuration files created, we will now use the ADK CLI to import and deploy the components to your watsonx Orchestrate environment. **The order of operations is important**: import knowledge bases and tools first, then the collaborator agents, and finally the supervisor agent.

Open your terminal in the project's root directory and run the following commands sequentially:

```bash
# 1. Import the Knowledge Bases
echo "Importing Knowledge Bases..."
orchestrate knowledge-bases import -f maintenance_kb.yaml
orchestrate knowledge-bases import -f flight_ops_kb.yaml

# 2. Import the Python Tools
echo "Importing Tools..."
orchestrate tools import -f maintenance_tools.py
orchestrate tools import -f flight_crew_tools.py

# 3. Import the Collaborator Agents
echo "Importing Collaborator Agents..."
orchestrate agents import -f maintenance_agent.yaml
orchestrate agents import -f flight_crew_agent.yaml

# 4. Import the Supervisor Agent
echo "Importing Supervisor Agent..."
orchestrate agents import -f supervisor_agent.yaml

echo "Deployment complete. You can now start the chat."
```

## Verification Steps

To verify the solution and perform the client demo, start the interactive chat with the `AeroAssist_Supervisor` agent.

```bash
orchestrate chat start --agent AeroAssist_Supervisor
```

Now, run through the three demo scenarios outlined in the client context.

### Scenario 1: Maintenance Troubleshooting & Action

*   **User Prompt:** `What are the possible causes for hydraulic system pressure low alert on an A321, fault code 29-11-00?`
*   **Expected Behavior:**
    1.  `AeroAssist_Supervisor` receives the prompt.
    2.  It identifies keywords like "hydraulic system," "fault code," and "causes," matching the description of the `Maintenance_Technician_Agent`.
    3.  It delegates the task to the `Maintenance_Technician_Agent`.
    4.  The `Maintenance_Technician_Agent` queries the `Maintenance_Manuals_KB`.
    5.  It returns a sourced answer from the mock `A321_AMM.pdf`.
*   **Follow-up User Prompt:** `Log a priority 1 issue for aircraft N301DN regarding a suspected leak in the green hydraulic line.`
*   **Expected Behavior:**
    1.  The conversation continues with the `Maintenance_Technician_Agent`.
    2.  The agent identifies the intent to "Log an issue" and recognizes the need for the `log_maintenance_issue` tool.
    3.  It invokes the tool with the provided description, priority, and tail number.
    4.  The tool executes, and the agent returns the confirmation message: `Successfully created maintenance ticket MX-##### for aircraft N301DN.`

### Scenario 2: Pre-Flight Procedure Verification

*   **User Prompt:** `What are the exact steps for the de-icing communications check?`
*   **Expected Behavior:**
    1.  `AeroAssist_Supervisor` receives the prompt.
    2.  It identifies keywords like "steps," "pre-flight," and "communications check," matching the description of the `Flight_Crew_Agent`.
    3.  It delegates the task.
    4.  The `Flight_Crew_Agent` recognizes the request for "exact steps" and invokes the `get_preflight_procedure` tool.
    5.  The agent returns the structured, step-by-step procedure from the tool's mock database, citing the FCOM source.

### Scenario 3: Intelligent Routing

*   **User Prompt:** `What are the crew rest requirements for a 14-hour international flight?`
*   **Expected Behavior:**
    1.  `AeroAssist_Supervisor` receives the prompt.
    2.  It sees the keywords "crew rest requirements," which strongly aligns with the `Flight_Crew_Agent`'s description ("...review crew compliance regulations like rest requirements").
    3.  It correctly routes the query to the `Flight_Crew_Agent`.
    4.  The `Flight_Crew_Agent` queries its `Flight_Operations_KB` using the `Safety_Compliance_Regs.txt` document and provides a sourced answer.

## Troubleshooting

*   **Agent Routing Failure:** If the supervisor fails to route correctly, review and enhance the `description` fields for the collaborator agents. The supervisor relies entirely on these descriptions for its routing logic. Make them more distinct and keyword-rich.
*   **Tool Not Found:** If an agent reports it cannot find a tool, ensure the `orchestrate tools import` command ran successfully. Use `orchestrate tools list` to verify the tool is present in the environment. Also, check that the tool's name in the agent's YAML file matches the `@tool(name=...)` decorator in the Python code exactly.
*   **Poor RAG Results:** If the knowledge base answers are inaccurate or not sourced, check the quality of the mock documents. For dense PDFs like technical manuals, ensure the text is extractable and well-structured. The default `ibm/slate-125m-english-rtrvr-v2` embedding model is robust, but document quality is paramount.
*   **Tool Execution Error:** If a tool fails during execution, check the terminal where the ADK is running for Python stack traces. This could indicate a bug in the tool's logic or an issue with simulated data.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
