# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-22 16:17:59
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AIOps IT Help Desk for LogicMonitor

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying a powerful AIOps IT Help Desk demonstration for LogicMonitor using IBM watsonx Orchestrate. The solution, centered around the "Edwin AI Orchestrator," showcases a multi-agent architecture that intelligently routes IT help desk queries. It seamlessly integrates real-time observability data from a mocked LogicMonitor system with automated incident management in a mocked ServiceNow environment.

The core of this demonstration is a supervisor agent that delegates tasks to specialized collaborator agents—one for observability (`LogicMonitor_Observer`) and one for ITSM (`ServiceNow_Operator`). This approach directly addresses LogicMonitor's goal of creating an intelligent AIOps help desk by providing a robust orchestration layer. By following this plan, you will build a proof-of-concept that highlights significant business value, including reduced Mean Time to Resolution (MTTR), improved internal efficiency by automating manual tasks, and an enhanced self-service experience for end-users through an integrated knowledge base.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured. This setup is crucial for the successful creation and deployment of the agents and tools outlined in this plan.

*   **Python:** Version 3.10 or higher.
*   **IBM watsonx Orchestrate Agent Development Kit (ADK):** The core library for building and managing Orchestrate assets. If not already installed, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate CLI Initialization:** You must have your watsonx Orchestrate environment configured. If you haven't done so, run:
    ```bash
    orchestrate-adk env init
    ```
    Follow the prompts to connect to your watsonx Orchestrate instance.
*   **Project Directory:** Create a dedicated folder for this project to keep all files organized. We recommend the following structure:
    ```
    /logicmonitor_demo
    |-- agents/
    |   |-- edwin_ai_orchestrator.yaml
    |   |-- logicmonitor_observer.yaml
    |   |-- servicenow_operator.yaml
    |-- tools/
    |   |-- logicmonitor_tools.py
    |   |-- servicenow_tools.py
    |-- knowledge_base/
    |   |-- it_sop_kb.yaml
    |   |-- documents/
    |       |-- vpn_troubleshooting.pdf
    |       |-- app_cache_clearing.txt
    |-- requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Create the Knowledge Base and Mock Documents

The `Edwin AI Orchestrator` will use a knowledge base for self-service troubleshooting. We will create a built-in Milvus knowledge base populated with mock Standard Operating Procedure (SOP) documents.

1.  **Create the Mock SOP Documents:**
    Inside the `knowledge_base/documents/` directory, create the following files.

    *   `app_cache_clearing.txt`:
        ```text
        STANDARD OPERATING PROCEDURE: Clearing Application Cache

        1. Identify the application causing issues.
        2. Close the application completely. Ensure it is not running in the background.
        3. For Windows: Navigate to %appdata% and delete the application's folder.
        4. For macOS: Navigate to ~/Library/Caches/ and delete the application's cache folder.
        5. Relaunch the application. The cache will be rebuilt.
        6. If the issue persists, contact IT support.
        ```

    *   `vpn_troubleshooting.pdf`: For this demo, you can create a simple text file and save it as a PDF or use any existing PDF. The content is less important than the file's presence for ingestion.

2.  **Define the Knowledge Base Configuration:**
    Create the file `knowledge_base/it_sop_kb.yaml`. This YAML file defines the knowledge base, its purpose, and points to the documents to be ingested.

    *   `knowledge_base/it_sop_kb.yaml`:
        ```yaml
        spec_version: v1
        kind: knowledge_base
        name: IT_SOP_KnowledgeBase
        description: >
          Contains standard operating procedures and troubleshooting guides for common IT issues like VPN connectivity, application errors, and system performance problems. This is the first resource to consult for self-service solutions before creating a support ticket.
        documents:
          - "knowledge_base/documents/vpn_troubleshooting.pdf"
          - "knowledge_base/documents/app_cache_clearing.txt"
        vector_index:
          embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
        ```

### Step 2: Develop Python-Based Tools

Tools are the executable components that allow agents to interact with external systems. We will create two sets of tools: one for observing the LogicMonitor environment and one for operating ServiceNow. These tools will generate realistic synthetic data to simulate API responses.

1.  **Create the `requirements.txt` file:**
    This file lists the Python packages our tools depend on.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```

2.  **Create LogicMonitor Observer Tools:**
    These tools simulate fetching data from LogicMonitor's API, providing real-time observability into system health, alerts, and performance. This capability is crucial for proactive problem detection and enriching incident tickets with context.

    *   `tools/logicmonitor_tools.py`:
        ```python
        import json
        import random
        from datetime import datetime, timedelta
        from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

        @tool(name="get_device_status", permission=ToolPermission.ADMIN)
        def get_device_status(device_name: str) -> str:
            """
            Retrieves the current operational status and key performance metrics for a specific device.

            This tool simulates a call to the LogicMonitor API to get real-time health data, which is essential for immediate diagnostics when a user reports an issue. It provides the foundational data needed to determine if a system is operational or experiencing a fault.

            Args:
                device_name (str): The unique hostname of the device to check (e.g., 'web-prod-01', 'db-cluster-01').

            Returns:
                str: A JSON string containing the device status, CPU load, memory usage, and a timestamp.
            """
            statuses = ["healthy", "warning", "critical"]
            if "web" in device_name:
                status = "critical"
                cpu_load = "98%"
                memory_usage = "92%"
            else:
                status = random.choice(statuses)
                cpu_load = f"{random.randint(20, 85)}%"
                memory_usage = f"{random.randint(40, 90)}%"

            data = {
                "deviceName": device_name,
                "status": status,
                "cpu_load": cpu_load,
                "memory_usage": memory_usage,
                "timestamp": datetime.utcnow().isoformat()
            }
            return json.dumps(data, indent=2)

        @tool(name="check_active_alerts", permission=ToolPermission.ADMIN)
        def check_active_alerts(min_severity: str = "P3") -> str:
            """
            Fetches a list of all active alerts from LogicMonitor that meet a minimum severity level.

            This tool is vital for understanding the broader context of system health. It allows the AIOps agent to correlate a user's reported issue with known system-wide problems, preventing duplicate incident creation and providing immediate awareness of ongoing outages.

            Args:
                min_severity (str, optional): The minimum severity to filter by (e.g., 'P1', 'P2', 'P3'). Defaults to 'P3'.

            Returns:
                str: A JSON string containing a list of active alerts with their severity and description.
            """
            alerts = [
                {"alertId": "LM-ALERT-101", "severity": "P1", "device": "web-prod-01", "description": "High CPU utilization detected", "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat()},
                {"alertId": "LM-ALERT-102", "severity": "P2", "device": "api-gateway-01", "description": "Response time degradation", "timestamp": (datetime.utcnow() - timedelta(minutes=25)).isoformat()},
                {"alertId": "LM-ALERT-103", "severity": "P3", "device": "db-cluster-01", "description": "Disk space approaching capacity", "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat()},
            ]
            return json.dumps(alerts, indent=2)

        @tool(name="fetch_performance_logs", permission=ToolPermission.ADMIN)
        def fetch_performance_logs(device_name: str) -> str:
            """
            Retrieves the last 100 lines of performance logs for a given device from LogicMonitor.

            Access to raw logs is critical for deep-dive technical analysis. This tool automates the log collection process, ensuring that when an incident ticket is created, it is immediately enriched with the necessary data for engineers to begin root cause analysis, drastically reducing MTTR.

            Args:
                device_name (str): The unique name of the device (e.g., 'web-prod-01').

            Returns:
                str: A formatted string containing the recent performance logs.
            """
            timestamp = datetime.utcnow().isoformat()
            logs = [
                f"{timestamp} [ERROR] High CPU usage detected: 98%. Threshold exceeded.",
                f"{timestamp} [WARN] Memory pressure at 92%.",
                f"{timestamp} [INFO] Request received on /api/v1/login.",
                f"{timestamp} [ERROR] Database connection timeout on pool-3-thread-1.",
            ]
            return f"Logs for {device_name}:\n" + "\n".join(logs)
        ```

3.  **Create ServiceNow Operator Tools:**
    These tools simulate interactions with ServiceNow's ITSM platform. They automate the lifecycle of an incident ticket, from creation to status checks and updates. This automation is key to improving IT staff efficiency and providing transparent, real-time updates to users.

    *   `tools/servicenow_tools.py`:
        ```python
        import json
        import random
        from datetime import datetime
        from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

        @tool(name="create_incident", permission=ToolPermission.ADMIN)
        def create_incident(description: str, severity: int = 3) -> str:
            """
            Creates a new incident ticket in ServiceNow based on a user's report.

            This tool is the primary action for formalizing an IT issue. By automating ticket creation, it ensures that all necessary information is captured consistently and that the issue is entered into the formal support queue for tracking and resolution, freeing up help desk staff from manual data entry.

            Args:
                description (str): A detailed description of the issue.
                severity (int, optional): The priority level of the incident (1=Critical, 2=High, 3=Medium). Defaults to 3.

            Returns:
                str: A JSON string confirming the creation with the new incident number.
            """
            incident_number = f"INC{random.randint(1000000, 9999999)}"
            response = {
                "result": {
                    "incident_number": incident_number,
                    "status": "New",
                    "message": "Incident created successfully."
                }
            }
            return json.dumps(response, indent=2)

        @tool(name="get_incident_status", permission=ToolPermission.ADMIN)
        def get_incident_status(incident_number: str) -> str:
            """
            Retrieves the current status, assignee, and work notes for a given ServiceNow incident number.

            This tool provides on-demand transparency into the support process. It empowers both end-users and managers to self-serve status updates, reducing the number of follow-up inquiries to the help desk and providing clear visibility into the resolution progress.

            Args:
                incident_number (str): The unique incident number (e.g., 'INC0012345').

            Returns:
                str: A JSON string with the incident's current details.
            """
            statuses = ["New", "In Progress", "On Hold", "Resolved"]
            assignees = ["WebOps Team", "Database Admins", "Network Engineering", "Jane Doe"]
            response = {
                "incident_number": incident_number,
                "status": random.choice(statuses),
                "assigned_to": random.choice(assignees),
                "last_updated": datetime.utcnow().isoformat(),
                "work_notes": "Investigation is ongoing. Engineering team is analyzing logs."
            }
            return json.dumps(response, indent=2)

        @tool(name="update_incident_with_logs", permission=ToolPermission.ADMIN)
        def update_incident_with_logs(incident_number: str, logs: str) -> str:
            """
            Updates an existing ServiceNow incident with additional information, such as performance logs.

            This tool is a critical component of the AIOps workflow, enabling the system to enrich tickets with new information as it becomes available. Attaching logs directly to the ticket ensures that engineers have all the context they need in one place, which is fundamental to accelerating resolution times.

            Args:
                incident_number (str): The incident number to update.
                logs (str): The log data to be added to the incident's work notes.

            Returns:
                str: A JSON string confirming that the incident was updated.
            """
            response = {
                "incident_number": incident_number,
                "status": "Success",
                "message": f"Successfully updated incident {incident_number} with new logs."
            }
            return json.dumps(response, indent=2)
        ```

### Step 3: Define the Agent Configurations

With the tools and knowledge base defined, we now configure the agents. We will create two specialist collaborator agents and one supervisor agent that orchestrates them.

1.  **`LogicMonitor_Observer` Agent:**
    This agent is an expert on the LogicMonitor environment. Its sole purpose is to use the LogicMonitor tools to provide observability data. Its description is crafted so the supervisor agent understands exactly when to delegate tasks to it.

    *   `agents/logicmonitor_observer.yaml`:
        ```yaml
        spec_version: v1
        kind: native
        name: LogicMonitor_Observer
        llm: watsonx/ibm/granite-3-8b-instruct
        style: default
        description: >
          An expert agent for querying the LogicMonitor observability platform. Use this agent to get real-time information about system health, device status, active alerts, and performance logs. It is the primary source for any questions related to the current operational state of IT infrastructure.
        instructions: >
          Your purpose is to act as a direct interface to the LogicMonitor system.
          When asked for system status, alerts, or logs, use your tools to fetch the data.
          Provide the data back in a clear and concise format. Do not interpret the data, only retrieve and present it.
        tools:
          - get_device_status
          - check_active_alerts
          - fetch_performance_logs
        ```

2.  **`ServiceNow_Operator` Agent:**
    This agent is an expert on the ServiceNow platform, responsible for all ITSM functions. Its description clearly outlines its capabilities for ticket management, ensuring the supervisor agent routes all incident-related requests to it.

    *   `agents/servicenow_operator.yaml`:
        ```yaml
        spec_version: v1
        kind: native
        name: ServiceNow_Operator
        llm: watsonx/ibm/granite-3-8b-instruct
        style: default
        description: >
          An expert agent for managing IT Service Management (ITSM) tasks within ServiceNow. Use this agent for all actions related to support incidents, including creating new tickets, checking the status of existing tickets, and updating tickets with new information like logs or user comments.
        instructions: >
          Your purpose is to manage the lifecycle of ServiceNow incidents.
          Use the create_incident tool when a user needs to report a new issue.
          Use the get_incident_status tool to provide updates on existing tickets.
          Use the update_incident_with_logs tool to add context to a ticket.
        tools:
          - create_incident
          - get_incident_status
          - update_incident_with_logs
        ```

3.  **`Edwin AI Orchestrator` (Supervisor Agent):**
    This is the central agent and the primary user interface. Its instructions contain explicit reasoning logic, guiding it on how to delegate tasks to its collaborators (`LogicMonitor_Observer`, `ServiceNow_Operator`) and when to use its knowledge base. This is the core of the multi-agent pattern.

    *   `agents/edwin_ai_orchestrator.yaml`:
        ```yaml
        spec_version: v1
        kind: native
        name: edwin_ai_orchestrator
        llm: watsonx/ibm/granite-3-8b-instruct
        style: default
        description: >
          An AIOps supervisor agent for the IT Help Desk. It intelligently routes user requests by collaborating with specialized agents. It uses the LogicMonitor_Observer for observability tasks and the ServiceNow_Operator for incident management tasks. It also consults an internal knowledge base for self-service troubleshooting.
        instructions: >
          You are "Edwin AI," the lead AIOps orchestrator for the IT Help Desk. Your goal is to resolve user issues efficiently.

          Reasoning:
          1.  When a user reports a potential system issue (e.g., "website is down," "application is slow"), your FIRST step is to use the `LogicMonitor_Observer` agent to check the system's health, status, or active alerts.
          2.  If the `LogicMonitor_Observer` confirms a critical issue, use its `fetch_performance_logs` tool to get context, and then immediately use the `ServiceNow_Operator` agent to create a high-priority incident. Inform the user of the ticket number you created.
          3.  When a user asks for the status of an existing ticket, use the `ServiceNow_Operator` agent to get the ticket details.
          4.  If a user reports a common, non-critical issue (e.g., "VPN is slow," "can't connect to printer") and the `LogicMonitor_Observer` finds no system-wide alerts, your FIRST step is to consult the `IT_SOP_KnowledgeBase` for a self-service solution. Present the steps to the user. Only offer to create a ticket if the knowledge base solution does not work.
        collaborators:
          - LogicMonitor_Observer
          - ServiceNow_Operator
        knowledge_base:
          - IT_SOP_KnowledgeBase
        ```

### Step 4: Import All Assets into watsonx Orchestrate

The order of import is critical. Dependencies (knowledge bases, tools) must be imported first, followed by the collaborator agents, and finally the supervisor agent.

Execute these commands from the root of your `logicmonitor_demo` directory.

1.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f knowledge_base/it_sop_kb.yaml
    ```
    *Wait for the confirmation that the knowledge base has started processing.*

2.  **Import the Tools:**
    ```bash
    orchestrate tools import -f tools/logicmonitor_tools.py
    orchestrate tools import -f tools/servicenow_tools.py
    ```

3.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/logicmonitor_observer.yaml
    orchestrate agents import -f agents/servicenow_operator.yaml
    ```

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/edwin_ai_orchestrator.yaml
    ```

## 4. Verification and Demo Script

To verify the implementation, start the chat interface with the `edwin_ai_orchestrator` as the target agent. This allows you to interact with the entire multi-agent system through a single entry point.

**Start the Chat:**
```bash
orchestrate chat start -a edwin_ai_orchestrator
```

Now, run through the demo scenarios defined in the client concept.

**Scenario 1: Proactive Alert to Resolution**
*   **User Prompt:** `I think the main website is down. Can you check?`
*   **Expected Agent Behavior:**
    1.  `Edwin AI Orchestrator` reasons that this is a system health check and delegates to `LogicMonitor_Observer`.
    2.  `LogicMonitor_Observer` calls the `get_device_status(device_name='web-prod-01')` tool, which returns a "critical" status.
    3.  `Edwin AI Orchestrator` receives the critical status, then delegates again to `LogicMonitor_Observer` to call `fetch_performance_logs`.
    4.  `Edwin AI Orchestrator` then delegates to `ServiceNow_Operator` to call `create_incident` with the description and logs.
    5.  `ServiceNow_Operator` returns a new incident number.
*   **Expected Agent Response:** "Yes, I've confirmed a critical issue with the web server (CPU at 98%). I have created a high-priority ticket (e.g., INC1234567) and attached the relevant logs for the engineering team."

**Scenario 2: Context-Rich Incident Inquiry**
*   **User Prompt:** `What's the status of ticket INC1234567?`
*   **Expected Agent Behavior:**
    1.  `Edwin AI Orchestrator` reasons this is a ticket status request and delegates to `ServiceNow_Operator`.
    2.  `ServiceNow_Operator` calls `get_incident_status(incident_number='INC1234567')`.
    3.  (Advanced) The orchestrator could be instructed to *also* query `LogicMonitor_Observer` for the current health of the related device to provide extra context.
*   **Expected Agent Response:** "Ticket INC1234567 is currently 'In Progress' and assigned to the 'WebOps Team'. The latest note indicates they are analyzing the logs. I can also see from live monitoring that the server's CPU load has stabilized at 45%, indicating progress."

**Scenario 3: Knowledge-Based Self-Service**
*   **User Prompt:** `My VPN connection is slow.`
*   **Expected Agent Behavior:**
    1.  `Edwin AI Orchestrator` first delegates to `LogicMonitor_Observer` to run `check_active_alerts` to rule out a system-wide issue.
    2.  Finding no relevant alerts, it then queries its `IT_SOP_KnowledgeBase` with the term "VPN".
    3.  The knowledge base returns the content from `vpn_troubleshooting.pdf`.
*   **Expected Agent Response:** "I don't see any system-wide alerts related to VPN services right now. Based on our standard procedures, here are some initial steps you can try: [Presents steps from the knowledge base]. Please try these first. If the issue persists, shall I create a support ticket for you?"

## 5. Troubleshooting

*   **Error: `Collaborator '...' not found`:** This occurs if you import the supervisor agent before its collaborator agents are successfully imported. Ensure you follow the import order in Step 4. You can list existing agents with `orchestrate agents list` to verify.
*   **Error: `Tool '...' not found`:** This happens if an agent's YAML file lists a tool that has not been imported. Run the `orchestrate tools import` command for the missing tool file and then re-import the agent.
*   **Knowledge Base Not Returning Results:** After importing the knowledge base, it can take a few minutes to ingest and index the documents. Use the command `orchestrate knowledge-bases status --name IT_SOP_KnowledgeBase` and wait for the status to show `Ready: true`.
*   **Python Tool Errors:** Ensure all dependencies from `requirements.txt` are installed in your Python environment (`pip install -r requirements.txt`). Any `ImportError` in the tool's code will cause the import to fail.

## 6. Best Practices

*   **Clear Agent Descriptions:** The supervisor agent's ability to route tasks correctly depends almost entirely on the quality of the collaborator agents' descriptions. Be explicit about what each agent *does* and what systems it is an *expert* on.
*   **Specific Supervisor Instructions:** The `instructions` in the supervisor agent's YAML are its "brain." Use direct, rule-based reasoning (e.g., "If the user asks about X, use agent Y") to guide its decision-making process for reliable and predictable behavior.
*   **Modular and Specialized Agents:** Adhere to the single-responsibility principle. The `LogicMonitor_Observer` only observes; the `ServiceNow_Operator` only operates on tickets. This modularity makes the system easier to maintain, test, and extend with new capabilities.
*   **Idempotent Tools:** Design tools to be safely re-run without causing negative side effects where possible. For example, `get_incident_status` can be called multiple times, while `create_incident` should ideally be called only once per unique issue.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
