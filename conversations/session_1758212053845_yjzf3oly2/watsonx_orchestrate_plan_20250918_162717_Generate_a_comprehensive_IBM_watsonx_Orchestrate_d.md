# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 16:27:17
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Proactive Managed Print Service (MPS) Fleet Intelligence Agent

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Proactive Managed Print Service (MPS) Fleet Intelligence Agent" Proof of Concept (POC). This plan is meticulously tailored to the client's strategic goal of transforming their service model from reactive break-fix to proactive, predictive maintenance. By leveraging the IBM watsonx Orchestrate Agent Development Kit (ADK) and its powerful supervisor-collaborator pattern, we will construct a multi-agent solution that automates the entire incident lifecycle. This system will ingest real-time printer alerts, use a technical knowledge base for intelligent diagnosis, and orchestrate specialized agents to create service tickets and order necessary parts, directly demonstrating a path to significant business value.

The resulting demo will showcase a tangible solution for increasing operational efficiency by automating manual support tasks, reducing operational costs through optimized technician dispatch and inventory management, and dramatically improving customer satisfaction by minimizing device downtime. The architecture is designed to be robust, scalable, and a clear representation of modern AI-powered automation.

## Prerequisites
Before beginning, ensure your development environment is fully configured with the following components. A proper setup is crucial for the successful creation, deployment, and execution of the agents and tools outlined in this plan.

1.  **Python Environment**: A working installation of Python (version 3.10 or higher) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed. If you haven't installed it, run the following command in your terminal:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment Initialization**: You must have an active watsonx Orchestrate environment configured. If you have not done so, run the `orchestrate environment init` command and follow the prompts to connect to your instance.
4.  **Project Directory Structure**: To maintain a clean and organized project, create the following directory structure in your workspace. This structure logically separates agents, tools, knowledge base documents, and mock data assets.

    ```
    mps-fleet-intelligence-poc/
    ├── agents/
    ├── tools/
    ├── knowledge_base/
    │   └── manuals/
    └── mock_data/
    └── config.py
    └── requirements.txt
    ```

## Step 1: Project Setup and Configuration
A well-organized project with centralized configuration is easier to manage and scale. We will start by creating a configuration file for our file paths and a `requirements.txt` file for dependencies.

1.  **Create Configuration File**: Centralizing constants like file paths is a best practice. In the project root, create `config.py`.

    `config.py`
    ```python
    # Central configuration for file paths and constants
    # Mock Data Paths
    ALERTS_FILE = "mock_data/alerts.json"
    INVENTORY_FILE = "mock_data/inventory.json"
    TICKETS_LOG_FILE = "mock_data/servicenow_tickets.log"

    # Knowledge Base Document Paths
    MANUAL_VERSALINK = "knowledge_base/manuals/Xerox_VersaLink_C7000_Manual.pdf"
    MANUAL_ALTALINK = "knowledge_base/manuals/Xerox_AltaLink_B8090_Service_Guide.pdf"
    ```

2.  **Create `requirements.txt`**: This file lists any external Python packages your tools might need. For this demo, our tools are self-contained, but it's a critical best practice to include it for future expansion.

    `requirements.txt`
    ```
    # No external packages are required for these specific tools.
    # If tools used external libraries like 'requests' or 'python-dotenv',
    # they would be listed here.
    # e.g.,
    # requests
    # python-dotenv
    ```

## Step 2: Create Mock Data and Knowledge Base Assets
To simulate a real-world environment, we will create synthetic data sources. These files will be used by our custom tools to mimic interactions with external systems like a fleet monitoring service, ServiceNow, and an inventory system.

1.  **Create Expanded Mock Printer Alerts**: In the `mock_data/` directory, create `alerts.json`. This version includes a wider variety of alerts to better demonstrate the agent's ability to prioritize.

    `mock_data/alerts.json`
    ```json
    [
      {
        "alert_id": "ALERT_789101",
        "device_id": "Device-XYZ-001",
        "timestamp": "2024-08-15T09:30:00Z",
        "alert_code": "ERROR_077-901",
        "severity": "CRITICAL",
        "description": "Fuser End of Life error detected."
      },
      {
        "alert_id": "ALERT_789102",
        "device_id": "Device-ABC-002",
        "timestamp": "2024-08-15T09:32:15Z",
        "alert_code": "LOW_TONER_K",
        "severity": "WARNING",
        "description": "Black toner cartridge is low."
      },
      {
        "alert_id": "ALERT_789103",
        "device_id": "Device-BOS-005",
        "timestamp": "2024-08-14T11:05:00Z",
        "alert_code": "ERROR_016-799",
        "severity": "CRITICAL",
        "description": "Software error detected in Boston office printer."
      },
      {
        "alert_id": "ALERT_789104",
        "device_id": "Device-NYC-011",
        "timestamp": "2024-08-15T10:05:00Z",
        "alert_code": "INFO_PAPER_JAM",
        "severity": "INFO",
        "description": "Paper jam in tray 2, cleared by user."
      }
    ]
    ```

2.  **Create Mock Supply Inventory**: In `mock_data/`, create `inventory.json`.

    `mock_data/inventory.json`
    ```json
    {
      "126K35551": {
        "description": "Fuser Assembly for VersaLink C7000",
        "stock_level": 50,
        "price": 250.00
      },
      "106R03767": {
        "description": "High Capacity Black Toner for VersaLink/AltaLink",
        "stock_level": 200,
        "price": 125.50
      },
      "SW-PATCH-001": {
        "description": "Software Patch for AltaLink B8090",
        "stock_level": 999,
        "price": 0.00
      }
    }
    ```

3.  **Create Placeholder Knowledge Base Documents**: In `knowledge_base/manuals/`, create two placeholder text files and save them as PDFs.

    `knowledge_base/manuals/Xerox_VersaLink_C7000_Manual.txt`
    ```
    Xerox VersaLink C7000 Series Technical Service Manual
    Error Code Troubleshooting Guide

    Section 1: Fuser Errors
    Code: ERROR_077-901
    Description: Fuser End of Life. The fuser unit has reached its maximum operational lifespan and must be replaced to ensure print quality and prevent damage.
    Action: Replace the fuser assembly immediately.
    Required Part Number: 126K35551
    ```
    *Save this file as `Xerox_VersaLink_C7000_Manual.pdf`.*

    `knowledge_base/manuals/Xerox_AltaLink_B8090_Service_Guide.txt`
    ```
    Xerox AltaLink B8090 Service Guide

    Section 2: Supply Management
    Code: LOW_TONER_K
    Description: Low Black Toner. The black toner cartridge is nearing empty.
    Action: Order a replacement black toner cartridge.
    Required Part Number: 106R03767

    Section 3: Software Errors
    Code: ERROR_016-799
    Description: A critical software fault has occurred. A firmware patch is required.
    Action: Dispatch a technician to apply the latest software patch.
    Required Part Number: SW-PATCH-001
    ```
    *Save this file as `Xerox_AltaLink_B8090_Service_Guide.pdf`.*

## Step 3: Create and Import the Knowledge Base
The knowledge base is the "brain" of the diagnostic process, enabling the supervisor agent to understand technical error codes. We will use the built-in Milvus vector database to ingest our PDF service manuals.

**Explanation**: This knowledge base provides the agent with domain-specific expertise. When the agent encounters an error code like "ERROR_077-901," it can perform a semantic search against the manuals to find the root cause, the required corrective action, and the specific part number needed for the repair. This critical step transforms raw alert data into actionable intelligence, forming the foundation of the proactive service model.

1.  **Create the Knowledge Base Configuration File**: In the `knowledge_base/` directory, create `device_error_code_kb.yaml`.

    `knowledge_base/device_error_code_kb.yaml`
    ```yaml
    spec_version: v1
    kind: knowledge_base
    name: device_error_code_kb
    description: >
       A knowledge base containing technical service manuals and error code guides for various Xerox printer models.
       Use this to diagnose printer error codes and find required part numbers for repairs and supplies.
    documents:
       - "./knowledge_base/manuals/Xerox_VersaLink_C7000_Manual.pdf"
       - "./knowledge_base/manuals/Xerox_AltaLink_B8090_Service_Guide.pdf"
    vector_index:
       embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

2.  **Import the Knowledge Base**: Run the following command from the root of your project directory (`mps-fleet-intelligence-poc/`).

    ```bash
    orchestrate knowledgebases import -f knowledge_base/device_error_code_kb.yaml
    ```

## Step 4: Implement and Import the Tools
Tools are the functional components that allow agents to interact with systems and perform actions. We will create a suite of Python-based tools, incorporating best practices like centralized configuration and error logging.

### 4.1 ServiceNow Tools (`servicenow_tools.py`)
**Explanation**: These tools encapsulate all interactions with the ServiceNow platform. `create_service_now_incident` automates the creation of service tickets, ensuring that every detected issue is logged and tracked without human intervention. `get_my_service_now_incidents` provides a query interface for users, offering visibility into ongoing maintenance. This modular, domain-specific approach makes the ServiceNow functionality robust and reusable across other enterprise automation solutions.

1.  **Create the Python Tool File**: In the `tools/` directory, create `servicenow_tools.py`.

    `tools/servicenow_tools.py`
    ```python
    import json
    import datetime
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    # Configure basic logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="create_service_now_incident", permission=ToolPermission.ADMIN)
    def create_service_now_incident(description: str, device_id: str, priority: str, required_part: str = None) -> dict:
        """
        Creates a new service incident ticket in a mock ServiceNow system.

        Args:
            description (str): A detailed description of the incident.
            device_id (str): The unique identifier of the affected device.
            priority (str): The priority of the ticket (e.g., 'High', 'Medium', 'Low').
            required_part (str, optional): The part number required for the repair, if known.

        Returns:
            dict: A confirmation dictionary containing the new incident number and status.
        """
        try:
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Simulate ticket number generation
            with open(config.TICKETS_LOG_FILE, "a+") as f:
                f.seek(0)
                ticket_count = len(f.readlines())
                incident_number = f"INC{1001 + ticket_count:07d}"

            ticket_data = {
                "incident_number": incident_number, "timestamp": timestamp, "device_id": device_id,
                "description": description, "priority": priority, "required_part": required_part, "status": "New"
            }

            with open(config.TICKETS_LOG_FILE, "a") as f:
                f.write(json.dumps(ticket_data) + "\n")
            
            logging.info(f"Successfully created ticket {incident_number} for device {device_id}.")
            return {"status": "success", "incident_number": incident_number}
        except Exception as e:
            logging.error(f"Failed to create ServiceNow incident for device {device_id}: {e}")
            return {"status": "error", "message": str(e)}

    @tool(name="get_my_service_now_incidents", permission=ToolPermission.ADMIN)
    def get_my_service_now_incidents(location_filter: str = None) -> list[dict]:
        """
        Retrieves a list of service incidents. Can be filtered by a location string in the device ID.

        Args:
            location_filter (str, optional): A location code (e.g., 'Boston' or 'BOS') to filter incidents.

        Returns:
            list[dict]: A list of incident dictionaries matching the filter.
        """
        incidents = []
        try:
            with open(config.TICKETS_LOG_FILE, "r") as f:
                for line in f:
                    ticket = json.loads(line)
                    if location_filter and location_filter.lower() in ticket.get("device_id", "").lower():
                        incidents.append(ticket)
                    elif not location_filter:
                        incidents.append(ticket)
            return incidents
        except FileNotFoundError:
            logging.warning("ServiceNow tickets log file not found. Returning empty list.")
            return []
        except Exception as e:
            logging.error(f"Failed to retrieve incidents: {e}")
            return [{"error": f"Failed to retrieve incidents: {str(e)}"}]
    ```

### 4.2 Supply Chain Tools (`supply_chain_tools.py`)
**Explanation**: The `order_supplies` tool automates the procurement process. Once an issue is diagnosed and a required part is identified, this tool can place an order directly into the supply chain system. This eliminates costly delays, prevents human error in ordering, and enables just-in-time inventory management, directly contributing to reduced operational costs and faster service resolution.

1.  **Create the Python Tool File**: In the `tools/` directory, create `supply_chain_tools.py`.

    `tools/supply_chain_tools.py`
    ```python
    import json
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="order_supplies", permission=ToolPermission.ADMIN)
    def order_supplies(part_number: str, quantity: int) -> dict:
        """
        Orders a specific part number and quantity from the supply chain inventory system.

        Args:
            part_number (str): The unique identifier for the part or supply to order.
            quantity (int): The number of units to order.

        Returns:
            dict: A confirmation message with the order details and status.
        """
        try:
            with open(config.INVENTORY_FILE, "r") as f:
                inventory = json.load(f)

            if part_number not in inventory:
                logging.warning(f"Order failed: Part number {part_number} not found.")
                return {"status": "error", "message": f"Part number {part_number} not found."}

            if inventory[part_number]["stock_level"] < quantity:
                logging.info(f"Insufficient stock for {part_number}. Order backordered.")
                return {"status": "backordered", "message": f"Insufficient stock for {part_number}."}

            inventory[part_number]["stock_level"] -= quantity
            with open(config.INVENTORY_FILE, "w") as f:
                json.dump(inventory, f, indent=2)

            logging.info(f"Order placed for {quantity} of {part_number}.")
            return {"status": "success", "message": f"Order placed for {quantity} of {part_number}."}
        except Exception as e:
            logging.error(f"Failed to process order for part {part_number}: {e}")
            return {"status": "error", "message": str(e)}
    ```

### 4.3 Device Monitoring Tool (`device_monitor_tool.py`)
**Explanation**: This tool simulates the connection to the client's fleet management API, serving as the data ingestion point for the entire workflow. The `get_alerts` operation allows the supervisor agent to poll for new events. By filtering for actionable alerts, it ensures the system focuses only on issues that require intervention, triggering the proactive maintenance process efficiently.

1.  **Create the Python Tool File**: In `tools/`, create `device_monitor_tool.py`.

    `tools/device_monitor_tool.py`
    ```python
    import json
    import logging
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
    import config

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @tool(name="device_monitor", permission=ToolPermission.ADMIN)
    def get_alerts(min_severity: str = "WARNING") -> list[dict]:
        """
        Retrieves alerts from the printer fleet monitoring system at or above a minimum severity.

        Args:
            min_severity (str, optional): The minimum severity to fetch ('INFO', 'WARNING', 'CRITICAL'). Defaults to 'WARNING'.

        Returns:
            list[dict]: A list of active alert dictionaries.
        """
        severity_map = {"INFO": 1, "WARNING": 2, "CRITICAL": 3}
        min_level = severity_map.get(min_severity.upper(), 2)
        
        try:
            with open(config.ALERTS_FILE, "r") as f:
                all_alerts = json.load(f)
            
            filtered_alerts = [
                alert for alert in all_alerts 
                if severity_map.get(alert.get("severity", "INFO").upper(), 1) >= min_level
            ]
            return filtered_alerts
        except FileNotFoundError:
            logging.error("Alerts data file not found.")
            return [{"error": "Alerts data file not found."}]
        except Exception as e:
            logging.error(f"An error occurred while fetching alerts: {e}")
            return [{"error": f"An error occurred: {str(e)}"}]
    ```

### 4.4 Import All Tools
Run these commands from your project root to import all the tools into watsonx Orchestrate.

```bash
orchestrate tools import -k python -f tools/servicenow_tools.py
orchestrate tools import -k python -f tools/supply_chain_tools.py
orchestrate tools import -k python -f tools/device_monitor_tool.py
```

## Step 5: Implement and Import the Agents
With the tools and knowledge base in place, we define the agents. We will create two specialized collaborator agents and one supervisor agent to orchestrate the workflow, following the robust supervisor-collaborator pattern.

### 5.1 `ServiceNow_Agent` (Collaborator)
**Explanation**: A domain-specific agent dedicated to managing ServiceNow tasks. Its clear description and focused toolset allow the supervisor to reliably delegate all ticketing-related work, ensuring consistency and modularity in the architecture.

`agents/ServiceNow_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: ServiceNow_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    A specialized agent for interacting with the ServiceNow platform. Use this agent to create new service incidents,
    update existing tickets, and retrieve ticket status information. It is the sole responsible agent for all
    ServiceNow-related tasks.
instructions: >
    Your purpose is to manage service tickets in ServiceNow. When asked to create an incident, use the create_service_now_incident tool with all available details. When asked to retrieve incidents, use the get_my_service_now_incidents tool. Format your responses clearly and concisely.
collaborators: []
tools:
  - create_service_now_incident
  - get_my_service_now_incidents
```

### 5.2 `Supply_Chain_Agent` (Collaborator)
**Explanation**: This agent is responsible for all inventory and logistics operations. By encapsulating the `order_supplies` tool, it provides a clean, reliable interface for the supervisor to procure parts without needing to know the underlying details of the inventory system.

`agents/Supply_Chain_Agent.yaml`
```yaml
spec_version: v1
kind: native
name: Supply_Chain_Agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An agent that handles all inventory and supply chain logistics. Use this agent to check stock levels for parts
    or toner and to place orders for necessary supplies.
instructions: >
    You are a supply chain logistics agent. Your primary function is to order parts and supplies using the
    order_supplies tool. When you receive a request, execute the order and report the confirmation details back.
collaborators: []
tools:
  - order_supplies
```

### 5.3 `MPS_Fleet_Monitor` (Supervisor)
**Explanation**: This is the central orchestrator of the POC. Its instructions define the core business logic: ingest an alert, use the knowledge base for diagnosis, and delegate ticketing and ordering tasks to the appropriate collaborators. This pattern is a powerful and scalable design for building complex, multi-step automations.

`agents/MPS_Fleet_Monitor.yaml`
```yaml
spec_version: v1
kind: native
name: MPS_Fleet_Monitor
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    An agent that proactively monitors a fleet of printers. It can diagnose error codes using technical manuals,
    create service tickets in ServiceNow, and order replacement parts or supplies by collaborating with other specialized agents.
instructions: >
    Persona: You are a proactive Managed Print Service (MPS) Fleet Intelligence monitor.
    Context: Your goal is to minimize printer downtime by automating incident response. You only act on CRITICAL and WARNING level alerts.
    Reasoning:
    1. When a user asks you to check for alerts, use the device_monitor tool to get the latest alerts with a minimum severity of 'WARNING'.
    2. For each alert, first use the device_error_code_kb to understand the error and identify any required part numbers.
    3. If the issue requires a service call (like a hardware failure or software patch), delegate to the ServiceNow_Agent to create a 'High' priority service ticket. Include the diagnosis and required part number.
    4. If the issue is a simple supply replenishment (like toner), delegate to the ServiceNow_Agent to create a 'Low' priority tracking ticket.
    5. If a part or supply is needed, delegate to the Supply_Chain_Agent to place an order for the identified item.
    6. Always confirm all actions taken (diagnosis, ticket creation, and order placement) back to the user in a clear, consolidated summary for all processed alerts.
collaborators:
  - ServiceNow_Agent
  - Supply_Chain_Agent
tools:
  - device_monitor
knowledge_base:
  - device_error_code_kb
```

### 5.4 Import All Agents
Run these commands from your project root to import the agents in the correct order (collaborators first, then the supervisor).

```bash
# Import collaborator agents
orchestrate agents import -f agents/ServiceNow_Agent.yaml
orchestrate agents import -f agents/Supply_Chain_Agent.yaml

# Import the main supervisor agent
orchestrate agents import -f agents/MPS_Fleet_Monitor.yaml
```

## Step 6: Verification and Demo Execution
With all components deployed, you can now interact with the `MPS_Fleet_Monitor` agent to test the end-to-end workflows.

1.  **Start the Orchestrate Chat**:
    ```bash
    orchestrate chat start
    ```
    This will open a chat interface in your browser. Select the `MPS_Fleet_Monitor` agent to begin.

2.  **Run Demo Scenario 1: Proactive Fault Resolution**
    *   **User Prompt**: `"Check for new printer alerts and handle them."`
    *   **Expected Agent Actions & Response**:
        1.  The `MPS_Fleet_Monitor` agent calls its `device_monitor` tool, filtering out the 'INFO' alert. It processes the three 'CRITICAL' and 'WARNING' alerts.
        2.  For `ERROR_077-901`, it queries the KB, identifies the fuser issue, delegates to create a high-priority ticket, and delegates to order part `126K35551`.
        3.  For `LOW_TONER_K`, it queries the KB, identifies the toner issue, delegates to create a low-priority ticket, and delegates to order part `106R03767`.
        4.  For `ERROR_016-799`, it queries the KB, identifies the software issue, delegates to create a high-priority ticket, and delegates to order part `SW-PATCH-001`.
        5.  The agent will respond with a consolidated summary: *"I have processed three new alerts. For Device-XYZ-001, I detected a fuser failure, created high-priority ticket INC001001, and ordered the replacement fuser. For Device-ABC-002, I detected low toner, created ticket INC001002, and ordered a new cartridge. For Device-BOS-005, I detected a software fault, created high-priority ticket INC001003, and ordered the required patch."*

3.  **Run Demo Scenario 2: Human-in-the-Loop Query**
    *   **User Prompt**: `"What is the status of tickets for the Boston office?"`
    *   **Expected Agent Actions & Response**:
        1.  The `MPS_Fleet_Monitor` agent delegates the query to its `ServiceNow_Agent` collaborator.
        2.  The `ServiceNow_Agent` uses its `get_my_service_now_incidents` tool with the filter "Boston".
        3.  The agent will return the details for ticket `INC001003` from the log file, formatted in a readable table.

## Troubleshooting
*   **Tool Import Fails**: Check for syntax errors in your Python files. Ensure all necessary imports (including `logging` and `config`) are present and that the `@tool` decorator is used correctly.
*   **Agent Doesn't Delegate Correctly**: This is often due to unclear descriptions or instructions. Review the `description` of the collaborator agents and the `instructions` of the supervisor. Ensure the supervisor's instructions clearly state *when* and *why* it should use a specific collaborator for a specific task.
*   **File Not Found Errors**: Ensure you are running the `orchestrate` commands from the root directory of your project (`mps-fleet-intelligence-poc/`). Verify that the file paths in `config.py` are correct relative to the root.
*   **No Agent Response**: Check the terminal where you ran `orchestrate chat start` for any error logs. The enhanced logging in the tools will print detailed error messages there, helping you debug issues with file access or tool logic.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
