# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-24 16:12:13
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Aviation Operations Co-Pilot

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Aviation Operations Co-Pilot" for the client, as specified in the provided demo concept. The solution is designed to address critical operational challenges in the aviation industry by enhancing maintenance efficiency, improving safety and compliance, and streamlining crew operations. We will construct a multi-agent system using the IBM watsonx Orchestrate Agent Development Kit (ADK), featuring a supervisor agent that intelligently routes tasks to specialized collaborator agents for aircraft maintenance and flight operations. This plan includes the creation of custom tools to interact with mock enterprise systems and the integration of knowledge bases populated with synthetic technical documents, demonstrating a powerful combination of Retrieval-Augmented Generation (RAG) and automated task execution.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed and configured. Refer to the official documentation for installation instructions.
*   **Python Environment**: A working Python 3.9+ environment is required.
*   **Project Directory**: Create a dedicated folder for this project to keep all files organized. The recommended structure is:
    ```
    /aviation_demo
    |-- /agents
    |-- /knowledge_bases
    |-- /mock_data
    |-- /tools
    |-- mock_api.py
    |-- requirements.txt
    ```
*   **Python Libraries**: Install the necessary Python packages. Create a file named `requirements.txt` and run `pip install -r requirements.txt`.

    **`requirements.txt`**
    ```
    requests
    Flask
    ```

## 3. Step-by-Step Implementation

This section details the creation of all components, from mock data and APIs to the final deployment of the agent architecture.

### Phase 1: Create Mock Data and Services

To simulate a realistic environment, we will first create synthetic documents and a mock API for parts inventory.

#### 1.1. Create Mock Knowledge Documents

Create the following files inside the `/mock_data` directory.

**File: `mock_data/IBM-A321X_Maintenance_Manual.pdf`**
*(Note: As a text-based model, I cannot generate a PDF. Please create a PDF document using any standard editor and paste the following text into it. The text is designed to be effectively parsed by the RAG system.)*

```text
IBM-A321X Aircraft Maintenance Manual - Section 7: Landing Gear

Document ID: AMM-A321X-LG-Rev4
Last Updated: 2024-10-01

7.1 Main Landing Gear (MLG) Assembly

7.1.1 Main Gear Axle Nut - Torque Specifications
The main gear axle nut (Part Number: HG-455B) must be torqued to precise specifications to ensure safe operation.
- **Specification:** 1500 ft-lbs (2033.7 Nm)
- **Tool:** Calibrated Torque Wrench (Model TQ-5000 or equivalent)
- **Procedure:** Apply torque in a smooth, continuous motion. Do not use impact wrenches. Verify with a secondary measurement after 5 minutes to check for seating.

7.1.2 Brake Assembly Inspection
Inspect brake wear indicators (Part Number: BRK-PIN-991) every 100 flight cycles. Minimum pin extension is 2mm. If below minimum, replace the entire brake unit assembly (Part Number: B-UNIT-78C).

7.2 Nose Landing Gear (NLG) Assembly
... (add more fictional details as needed)
```

**File: `mock_data/Crew_Operating_Handbook.txt`**

```text
Crew Operating Handbook - IBM-A321X

Section 4: Non-Normal Procedures

4.5 Go-Around Procedure (CAT II Approach)

This procedure is mandatory if visual reference is lost below 100ft RA or if the aircraft is not in a stable landing configuration.

1.  **"Go-Around, Flaps" Callout:** Pilot Flying (PF) announces the go-around.
2.  **TOGA Thrust:** Press the Take-off/Go-around (TOGA) switches. The Flight Management System (FMS) will command go-around thrust.
3.  **Pitch:** Rotate smoothly to the go-around pitch attitude as indicated by the Flight Director (FD). Target 15 degrees nose up.
4.  **Flaps:** Retract flaps one step.
5.  **"Positive Rate" Callout:** Pilot Monitoring (PM) confirms vertical speed is positive.
6.  **"Gear Up" Command:** PF commands gear retraction. PM selects gear up.
7.  **Autopilot Engagement:** Engage autopilot as soon as practicable.
8.  **Navigation:** Follow the missed approach procedure as published on the approach chart or as directed by Air Traffic Control (ATC).
```

#### 1.2. Create Mock Inventory API

This simple Flask API simulates an inventory management system. Create this file in the root of your project directory.

**File: `mock_api.py`**
```python
from flask import Flask, jsonify

app = Flask(__name__)

# Synthetic inventory database
INVENTORY_DB = {
    "HG-455B": {
        "part_number": "HG-455B",
        "description": "Main gear axle nut",
        "quantity": 12,
        "location": "ATL-Hangar 3",
        "last_updated": "2024-10-21T14:30:00Z"
    },
    "BRK-PIN-991": {
        "part_number": "BRK-PIN-991",
        "description": "Brake wear indicator pin",
        "quantity": 150,
        "location": "ATL-Hangar 2",
        "last_updated": "2024-10-20T11:00:00Z"
    },
    "B-UNIT-78C": {
        "part_number": "B-UNIT-78C",
        "description": "Brake unit assembly",
        "quantity": 4,
        "location": "DFW-Central Stores",
        "last_updated": "2024-10-21T09:15:00Z"
    }
}

@app.route('/inventory/<string:part_number>', methods=['GET'])
def get_inventory(part_number):
    """Endpoint to get inventory details for a specific part number."""
    part_details = INVENTORY_DB.get(part_number.upper())
    if part_details:
        return jsonify(part_details)
    else:
        return jsonify({"error": "Part not found"}), 404

if __name__ == '__main__':
    # Run the API on localhost port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

```
**To run the API:** Open a new terminal, navigate to your project directory, and run the command: `python mock_api.py`. Keep this terminal running throughout the demo.

### Phase 2: Create Custom Tools

Now, we will create the Python tools for the `Maintenance_Tech_Agent`. These tools enable the agent to perform actions beyond simple chat.

**File: `tools/maintenance_tools.py`**

```python
import requests
import json
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# --- Tool 1: Check Part Inventory ---

@tool
def check_part_inventory(part_number: str) -> dict:
    """
    Checks the inventory level and location for a given aircraft part number by calling the inventory API.

    Args:
        part_number (str): The unique identifier for the aircraft part, for example, 'HG-455B'.

    Returns:
        dict: The inventory details including quantity, location, and description, or an error message if not found.
    """
    api_url = f"http://127.0.0.1:5000/inventory/{part_number}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": f"Part number '{part_number}' not found in inventory."}
        else:
            return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"API connection error: {req_err}"}

# --- Tool 2: Log Maintenance Task ---

@tool
def log_maintenance_task(aircraft_id: str, task_description: str) -> dict:
    """
    Logs a completed maintenance task for a specific aircraft into the maintenance record system.

    Args:
        aircraft_id (str): The tail number or unique identifier of the aircraft, e.g., 'N505DN'.
        task_description (str): A clear and concise description of the maintenance task performed.

    Returns:
        dict: A confirmation message with a log ID and timestamp.
    """
    # In a real system, this would write to a database or a secure log file.
    # For this demo, we simulate the log entry and return a confirmation.
    log_entry = {
        "log_id": f"LOG-{int(datetime.now().timestamp())}",
        "timestamp": datetime.now().isoformat(),
        "aircraft_id": aircraft_id,
        "task_description": task_description,
        "status": "LOGGED_SUCCESSFULLY"
    }
    
    # Simulate logging by printing to the console
    print(f"MAINTENANCE LOG: {json.dumps(log_entry)}")
    
    return log_entry

```
**Business Value & Explanation:**
*   **`check_part_inventory`**: This tool provides immense value by directly connecting the conversational AI to a core operational system. Instead of a technician having to switch applications or make a phone call to check parts availability, they can ask the agent in natural language. This significantly reduces task time, minimizes errors from manual lookups, and helps get aircraft back into service faster, directly impacting on-time performance and asset utilization.
*   **`log_maintenance_task`**: Compliance and record-keeping are paramount in aviation. This tool automates the crucial step of logging completed work. By allowing technicians to log tasks conversationally, it ensures that records are created immediately and accurately, reducing the chance of forgotten or incomplete logs. This strengthens the audit trail, ensures regulatory compliance, and provides a reliable maintenance history for the aircraft.

### Phase 3: Define Knowledge Bases

We will now define the knowledge bases using YAML, linking them to the mock documents created in Phase 1.

**File: `knowledge_bases/maintenance_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: maintenance_manuals_kb
description: >
    Contains technical maintenance manuals for various aircraft including the IBM-A321X. Use this for highly specific technical questions about torque specifications, part numbers, repair procedures, and inspection criteria.
documents:
   - "./mock_data/IBM-A321X_Maintenance_Manual.pdf"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

**File: `knowledge_bases/flight_ops_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: flight_operations_kb
description: >
    Contains the Crew Operating Handbook (COH) with standard operating procedures (SOPs), checklists, and non-normal procedures like go-arounds. Use this for questions from pilots and flight crew related to in-flight operations and regulations.
documents:
   - "./mock_data/Crew_Operating_Handbook.txt"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Phase 4: Define Agents

With the tools and knowledge bases ready, we define the three agents that form our architecture.

**File: `agents/Maintenance_Tech_Agent.yaml` (Collaborator)**
```yaml
spec_version: v1
kind: native
name: Maintenance_Tech_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialized agent for aircraft maintenance technicians. It answers highly specific technical questions by querying maintenance manuals and can execute tasks like checking part inventory and logging completed maintenance work.
instructions: >
    You are an expert assistant for aircraft maintenance. 
    - When asked for technical specifications like torque values or part numbers, you MUST use the information from your knowledge base.
    - When a user wants to know the availability of a part, use the 'check_part_inventory' tool.
    - When a user confirms a task is complete, use the 'log_maintenance_task' tool to record it.
    - Be precise and factual in your responses.
tools:
  - check_part_inventory
  - log_maintenance_task
knowledge_base:
  - maintenance_manuals_kb
```

**File: `agents/Flight_Crew_Agent.yaml` (Collaborator)**
```yaml
spec_version: v1
kind: native
name: Flight_Crew_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialized agent for pilots and flight crew. It provides quick and accurate information from crew operating handbooks and regulatory documents. It handles queries about flight procedures, checklists, and operational limits.
instructions: >
    You are an expert co-pilot assistant. Your sole purpose is to provide information from the flight operations knowledge base.
    - Answer questions about procedures, such as go-arounds or emergency checklists, by citing the knowledge base directly.
    - Do not perform maintenance tasks or answer questions about parts.
    - Your responses should be clear, concise, and structured like a checklist when appropriate.
knowledge_base:
  - flight_operations_kb
```

**File: `agents/AviationOps_Supervisor.yaml` (Supervisor)**
```yaml
spec_version: v1
kind: native
name: AviationOps_Supervisor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A supervisor agent for airline operations. It acts as the primary conversational interface and routes requests to specialized agents for either aircraft maintenance or flight crew operations based on the user's intent.
instructions: >
    Your primary role is to accurately delegate tasks to the correct specialist agent. Analyze the user's request carefully.
    - If the request relates to technical repairs, maintenance procedures, tools, part numbers, or inventory, you MUST use the Maintenance_Tech_Agent.
    - If the request relates to flight procedures, checklists, pilot operations, regulations, or go-arounds, you MUST use the Flight_Crew_Agent.
    - Do not attempt to answer questions directly. Your only job is to route the request to the correct collaborator.
collaborators:
  - Maintenance_Tech_Agent
  - Flight_Crew_Agent
```

### Phase 5: Deploy and Run the Application

With all files created, we will use the ADK CLI to import and deploy the components in the correct order.

**Open a new terminal** (ensure your mock API is still running in its own terminal) and execute these commands one by one:

1.  **Import the Tools:**
    ```bash
    orchestrate tools import -f tools/maintenance_tools.py
    ```
    *Explanation: This command registers the Python functions in `maintenance_tools.py` as executable tools within the watsonx Orchestrate environment, making them available for agents to use.*

2.  **Import the Knowledge Bases:**
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/maintenance_kb.yaml
    orchestrate knowledge-bases import -f knowledge_bases/flight_ops_kb.yaml
    ```
    *Explanation: These commands upload the specified documents, process them through the embedding model, and create searchable vector indexes in the built-in Milvus database. This enables the RAG capabilities of the agents.*

3.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/Maintenance_Tech_Agent.yaml
    orchestrate agents import -f agents/Flight_Crew_Agent.yaml
    ```
    *Explanation: We import the specialized collaborator agents first. This makes them available within the platform so the supervisor agent can find and reference them upon its own import.*

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/AviationOps_Supervisor.yaml
    ```
    *Explanation: Finally, we import the supervisor agent. It will now be able to connect to its collaborators, which have already been registered in the system.*

5.  **Start the Chat Session:**
    ```bash
    orchestrate chat start --agent AviationOps_Supervisor
    ```
    *Explanation: This command initiates an interactive chat session with our main supervisor agent, allowing us to test the entire multi-agent system.*

## 4. Verification

After starting the chat session, test the three key demo scenarios outlined in the client concept.

*   **Scenario 1: Precision Knowledge Retrieval (RAG)**
    *   **User Prompt:** `What is the torque spec for the main gear axle nut on the A321X?`
    *   **Expected System Action & Response:** The `AviationOps_Supervisor` will route the query to the `Maintenance_Tech_Agent`. The agent will query the `maintenance_manuals_kb`, find the relevant text, and respond with something similar to: "The torque specification for the main gear axle nut on the IBM-A321X is 1500 ft-lbs (2033.7 Nm)."

*   **Scenario 2: Multi-Turn Conversation with Tool Use**
    *   **User Prompt 1:** `I need to check stock for landing gear bolt part number HG-455B.`
    *   **Expected System Action & Response 1:** The `Maintenance_Tech_Agent` will execute the `check_part_inventory` tool, which calls the running mock API. The agent will respond: "There are 12 units of HG-455B (Main gear axle nut) available in the ATL-Hangar 3 warehouse."
    *   **User Prompt 2:** `Great. Log the replacement of the main gear axle nut on aircraft N505DN as complete.`
    *   **Expected System Action & Response 2:** The agent will execute the `log_maintenance_task` tool and confirm: "Maintenance task 'Main gear axle nut replacement' for aircraft N505DN has been logged successfully." You should also see the log entry printed in the console where the tools are running.

*   **Scenario 3: Supervisor Agent Routing**
    *   **User Prompt:** `What are the standard go-around procedures for a CAT II approach?`
    *   **Expected System Action & Response:** The `AviationOps_Supervisor` will identify this as a flight operations query and route it to the `Flight_Crew_Agent`. That agent will query the `flight_operations_kb` and provide a structured response based on the handbook, such as:
        "Here are the go-around procedures for a CAT II approach:
        1. Announce "Go-Around, Flaps".
        2. Press TOGA switches.
        3. Rotate to the go-around pitch attitude..."

## 5. Troubleshooting

*   **Tool Not Found Error:** If an agent reports it cannot find a tool, ensure the `orchestrate tools import` command was run successfully without errors before you imported the agents. Verify the tool names in the agent's YAML file exactly match the function names in the Python file.
*   **Incorrect Agent Routing:** If the supervisor sends a query to the wrong agent (e.g., sends a flight question to maintenance), review the `description` fields in both the supervisor and collaborator YAML files. The supervisor relies heavily on these descriptions to make its decision. Make them more distinct and explicit about each agent's unique capabilities.
*   **API Connection Error from Tool:** If the `check_part_inventory` tool fails, verify that the `mock_api.py` Flask server is running in its own terminal and is accessible on `http://127.0.0.1:5000`.
*   **Knowledge Base Returns No Information:** Check that the `orchestrate knowledge-bases import` command completed successfully. Ensure the file paths in the knowledge base YAML files are correct relative to where you are running the command. For complex PDFs, retrieval may vary; ensure the text is machine-readable and not just an image.

## 6. Best Practices

*   **Descriptive Clarity for Routing:** The success of the supervisor/collaborator pattern hinges on the quality of the collaborator agents' `description` fields. Each description should be a clear, concise "advertisement" of the agent's unique skills, tools, and knowledge, enabling the supervisor to route tasks effectively.
*   **Atomic Tool Design:** Design tools to be "atomic"—each tool should perform one specific, well-defined action (e.g., `check_inventory` or `log_task`). This makes them more reusable, easier for the LLM to reason about, and simpler to maintain.
*   **Isolate Knowledge Domains:** By creating separate knowledge bases for maintenance and flight operations, we prevent "knowledge contamination." This ensures that a maintenance query only draws from technical manuals and a pilot's query only draws from the operating handbook, leading to more accurate and contextually relevant answers.
*   **Explicit Instructions:** The `instructions` field within an agent's YAML is your primary tool for controlling its behavior. Be explicit. Use phrases like "You MUST use tool X for task Y" to guide the agent's reasoning process and ensure it uses its available capabilities correctly.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
