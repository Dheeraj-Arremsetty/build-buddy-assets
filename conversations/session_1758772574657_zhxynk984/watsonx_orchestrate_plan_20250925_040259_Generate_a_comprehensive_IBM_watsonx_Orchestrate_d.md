# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-25 04:02:59
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Major Incident Command Center

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Powered Major Incident Command Center" proof-of-concept (POC) using IBM watsonx Orchestrate. This plan is tailored specifically to the client's vision of creating a sophisticated, automated incident response system that integrates with their existing IT ecosystem (LogicMonitor, ServiceNow, ElasticSearch).

The core of this solution is a multi-agent architecture orchestrated by a central `supervisor_agent` that acts as an Incident Commander. This supervisor delegates specialized tasks—triage, root cause analysis, and stakeholder communication—to a team of collaborator agents. This approach directly addresses the client's key business objectives: accelerating Mean Time to Resolution (MTTR), reducing manual toil for incident response teams, improving the consistency and timeliness of stakeholder communications, and enhancing decision-making with AI-powered insights. By following this plan, we will construct a fully functional demo that showcases the power of watsonx Orchestrate to automate the end-to-end lifecycle of a major IT incident.

## Prerequisites

Before beginning the implementation, ensure your development environment is correctly configured.

1.  **Python Environment**: A working Python installation (version 3.9 or higher) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If not already installed, run the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate[all]"
    ```
3.  **Orchestrate Environment**: You must have an active IBM watsonx Orchestrate environment configured with the ADK. This involves initializing the environment and logging in.
    ```bash
    # Initialize your environment (follow the prompts)
    orchestrate env init

    # Set your newly created environment as the active one
    orchestrate env use <your_env_name>
    ```
4.  **Project Directory Structure**: To maintain organization, create the following directory structure. This plan will assume all commands are run from the root `incident_command_center` directory.
    ```
    incident_command_center/
    ├── agents/
    │   ├── supervisor_agent.yaml
    │   ├── triage_agent.yaml
    │   ├── rca_agent.yaml
    │   └── communications_agent.yaml
    ├── knowledge_bases/
    │   └── past_incident_reports_kb.yaml
    ├── tools/
    │   ├── incident_commander_tools.py
    │   ├── triage_tools.py
    │   ├── rca_tools.py
    │   └── communications_tools.py
    └── requirements.txt
    ```

## Step 1: Create Python Tools

The tools are the foundational actions that agents can perform. We will create Python-based tools using the `@tool` decorator. For this POC, the tools will generate realistic synthetic data to simulate interactions with external systems like ServiceNow, Slack, LogicMonitor, and ElasticSearch.

### 1.1 Triage and CMDB Tools

These tools are used by the `triage_agent` to enrich an incoming alert with business context from a simulated Configuration Management Database (CMDB).

**File:** `tools/triage_tools.py`

```python
# tools/triage_tools.py
import json
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Mock CMDB data source
MOCK_CMDB_DATA = {
    "prod-db-01": {
        "business_service": "Customer Billing Platform",
        "application_owner": "finance-app-owners@example.com",
        "service_tier": "Tier 1",
        "on_call_engineer": "jane.doe@example.com",
        "dependencies": ["prod-app-01", "prod-web-01"],
        "last_change_id": "CHG003456"
    },
    "prod-app-01": {
        "business_service": "Customer Billing Platform",
        "application_owner": "finance-app-owners@example.com",
        "service_tier": "Tier 1",
        "on_call_engineer": "john.smith@example.com",
        "dependencies": ["prod-db-01"],
        "last_change_id": "CHG003451"
    }
}

@tool(permission=ToolPermission.ADMIN)
def get_cmdb_details(hostname: str) -> str:
    """
    Retrieves critical business context for a given hostname from the CMDB.

    This tool queries the Configuration Management Database (CMDB) to enrich a technical alert
    with essential business information, such as the affected business service, the application
    owner, and service tier. This context is vital for assessing business impact and engaging
    the correct stakeholders during a major incident.

    Args:
        hostname (str): The hostname of the affected server (e.g., "prod-db-01").

    Returns:
        str: A JSON string containing the CMDB details for the specified hostname.
             Returns an error message if the hostname is not found.
    """
    print(f"Querying CMDB for hostname: {hostname}")
    details = MOCK_CMDB_DATA.get(hostname)
    if details:
        return json.dumps(details)
    else:
        return json.dumps({"error": f"Hostname '{hostname}' not found in CMDB."})

```

### 1.2 Root Cause Analysis (RCA) Tools

These tools are used by the `rca_agent` to gather technical data (logs and metrics) for root cause analysis.

**File:** `tools/rca_tools.py`

```python
# tools/rca_tools.py
import json
from datetime import datetime, timedelta
import random
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def query_elasticsearch_logs(hostname: str, time_window_minutes: int = 15) -> str:
    """
    Queries ElasticSearch for logs related to a specific hostname within a given time window.

    This tool simulates a search against an ElasticSearch cluster to retrieve relevant log entries
    preceding and during an incident. Access to log data is fundamental for root cause analysis,
    allowing the RCA agent to identify error messages, stack traces, and anomalous activity
    that could indicate the source of the problem.

    Args:
        hostname (str): The hostname to filter logs by (e.g., "prod-db-01").
        time_window_minutes (int): The number of minutes to look back for logs. Defaults to 15.

    Returns:
        str: A JSON string containing a list of relevant log entries.
    """
    print(f"Querying ElasticSearch for logs from '{hostname}' in the last {time_window_minutes} minutes.")
    incident_time = datetime.utcnow()
    logs = [
        {"timestamp": (incident_time - timedelta(minutes=2, seconds=2)).isoformat() + "Z", "level": "ERROR", "host": "prod-db-01", "service": "Oracle Listener", "message": "TNS-12541: TNS:no listener"},
        {"timestamp": (incident_time - timedelta(minutes=1, seconds=30)).isoformat() + "Z", "level": "INFO", "host": "prod-db-01", "service": "HealthCheck", "message": "Listener health check failed."},
        {"timestamp": (incident_time - timedelta(seconds=59)).isoformat() + "Z", "level": "ERROR", "host": "prod-app-01", "service": "BillingService", "message": "Database connection pool exhausted."},
        {"timestamp": (incident_time - timedelta(seconds=2)).isoformat() + "Z", "level": "FATAL", "host": "prod-app-01", "service": "BillingService", "message": "Cannot connect to database: ORA-12541"},
        {"timestamp": (incident_time).isoformat() + "Z", "level": "CRITICAL", "host": "prod-db-01", "service": "Oracle DB Listener", "message": "Service is down"},
    ]
    return json.dumps(logs)

@tool(permission=ToolPermission.ADMIN)
def get_logicmonitor_metrics(hostname: str, metric: str = "cpu_utilization") -> str:
    """
    Retrieves performance metrics for a specific host from LogicMonitor.

    This tool simulates a request to a monitoring platform like LogicMonitor to fetch key
    performance indicators (KPIs) such as CPU utilization, memory usage, or network I/O.
    Correlating performance metrics with log data helps the RCA agent build a more complete
    picture of the system's state and pinpoint performance bottlenecks or resource exhaustion
    as potential root causes.

    Args:
        hostname (str): The hostname to retrieve metrics for (e.g., "prod-db-01").
        metric (str): The specific metric to retrieve. Defaults to "cpu_utilization".

    Returns:
        str: A JSON string containing time-series data for the requested metric.
    """
    print(f"Retrieving LogicMonitor metric '{metric}' for host '{hostname}'.")
    now = datetime.utcnow()
    metrics_data = {
        "hostname": hostname,
        "metric": metric,
        "data_points": [
            {"timestamp": (now - timedelta(minutes=10)).isoformat() + "Z", "value": random.uniform(10.5, 15.0)},
            {"timestamp": (now - timedelta(minutes=5)).isoformat() + "Z", "value": random.uniform(12.0, 18.0)},
            {"timestamp": (now - timedelta(minutes=2)).isoformat() + "Z", "value": 98.7},
            {"timestamp": (now - timedelta(minutes=1)).isoformat() + "Z", "value": 99.1},
        ]
    }
    return json.dumps(metrics_data)
```

### 1.3 Incident Commander Tools

These tools are used by the `supervisor_agent` to manage the incident process, such as creating tickets and generating reports.

**File:** `tools/incident_commander_tools.py`

```python
# tools/incident_commander_tools.py
import json
import random
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def create_servicenow_ticket(description: str, business_service: str, severity: int = 1) -> str:
    """
    Creates a new major incident ticket in ServiceNow.

    This tool automates the first critical step of the formal incident response process:
    logging the incident in the system of record. Automating ticket creation ensures that all
    incidents are tracked, assigned, and have an auditable timeline from the very beginning,
    reducing administrative burden on the incident commander.

    Args:
        description (str): A detailed description of the incident.
        business_service (str): The primary business service impacted.
        severity (int): The severity level of the incident (e.g., 1 for Critical).

    Returns:
        str: A JSON string containing the new ServiceNow incident ticket number (e.g., "INC0012345").
    """
    ticket_number = f"INC{random.randint(10000, 99999)}"
    print(f"Creating ServiceNow ticket '{ticket_number}' for service '{business_service}' with description: {description}")
    return json.dumps({"ticket_id": ticket_number, "status": "New"})

@tool(permission=ToolPermission.ADMIN)
def create_slack_channel(incident_id: str) -> str:
    """
    Creates a dedicated Slack channel for a major incident.

    This tool automates the setup of a collaboration space for the incident response team.
    By creating a unique "war room" channel, it ensures all communications, data, and findings
    related to the incident are centralized. This improves coordination and prevents information
    silos, allowing the team to work more effectively towards resolution.

    Args:
        incident_id (str): The incident ticket number (e.g., "INC0012345") to name the channel.

    Returns:
        str: A JSON string with the name of the created Slack channel.
    """
    channel_name = f"incident-{incident_id.lower()}"
    print(f"Creating Slack channel: #{channel_name}")
    return json.dumps({"channel_name": channel_name, "status": "Created"})

@tool(permission=ToolPermission.ADMIN)
def generate_pir_draft(incident_id: str, root_cause: str, resolution_steps: str, timeline: str) -> str:
    """
    Generates a draft Post-Incident Report (PIR).

    This tool automates the often tedious process of compiling a PIR. By synthesizing key
    information gathered during the incident—such as the root cause, timeline, and resolution
    steps—it creates a structured draft report. This accelerates the post-incident learning
    process and ensures that valuable insights are captured consistently.

    Args:
        incident_id (str): The incident ticket number.
        root_cause (str): A summary of the identified root cause.
        resolution_steps (str): A summary of the steps taken to resolve the incident.
        timeline (str): A summary of the incident timeline.

    Returns:
        str: A formatted string containing the draft PIR.
    """
    pir_content = f"""
# Post-Incident Report (DRAFT)

**Incident ID:** {incident_id}
**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}

## 1. Executive Summary
A major incident was declared impacting the Customer Billing Platform. The root cause was identified and resolved, restoring service.

## 2. Incident Timeline
{timeline}

## 3. Root Cause Analysis
{root_cause}

## 4. Resolution Steps
{resolution_steps}

## 5. Next Steps
- [ ] Schedule post-mortem review.
- [ ] Identify and assign preventative action items.
"""
    return pir_content
```

### 1.4 Communications Tools

These tools are used by the `communications_agent` to send tailored updates to different stakeholder groups.

**File:** `tools/communications_tools.py`

```python
# tools/communications_tools.py
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def send_slack_message(channel: str, message: str) -> str:
    """
    Sends a message to a specified Slack channel.

    This tool provides the mechanism for delivering real-time, technical updates to the
    incident response team in their dedicated Slack channel. It is essential for keeping
    engineers and technical stakeholders informed of the latest findings, actions taken,
    and next steps, ensuring the entire response team is aligned.

    Args:
        channel (str): The Slack channel to send the message to (e.g., "incident-inc0012345").
        message (str): The message content to be sent.

    Returns:
        str: A JSON string confirming the message was sent successfully.
    """
    print(f"Sending Slack message to #{channel}:\n---\n{message}\n---")
    return json.dumps({"status": "Message sent", "channel": channel})

@tool(permission=ToolPermission.ADMIN)
def send_email_update(recipient_list: str, subject: str, body: str) -> str:
    """
    Sends an email update to a list of recipients.

    This tool is used to send high-level, business-impact-focused communications to leadership
    and non-technical stakeholders. By using a separate channel (email) and tailoring the
    message, it ensures that executives receive the information they need—business impact,
    customer impact, and ETA for resolution—without being overwhelmed by technical jargon.

    Args:
        recipient_list (str): A comma-separated list of recipient email addresses.
        subject (str): The subject line of the email.
        body (str): The HTML or plain text body of the email.

    Returns:
        str: A JSON string confirming the email was sent successfully.
    """
    print(f"Sending Email to [{recipient_list}] with subject '{subject}':\n---\n{body}\n---")
    return json.dumps({"status": "Email sent", "recipients": recipient_list.split(',')})
```

## Step 2: Create `requirements.txt`

This file ensures that any necessary third-party libraries for the tools are documented. For this POC, no external libraries are needed beyond the ADK itself, but it is best practice to include the file.

**File:** `requirements.txt`

```
# No external dependencies are required for these mock tools.
# If tools used libraries like 'requests' or 'pandas', they would be listed here.
# e.g.:
# requests
# python-dotenv
```

## Step 3: Create Knowledge Base Configuration

The `rca_agent` will leverage an external knowledge base to search for historical incident data. This YAML file defines the connection to the client's ElasticSearch instance.

**File:** `knowledge_bases/past_incident_reports_kb.yaml`

```yaml
spec_version: v1
kind: knowledge_base
name: past_incident_reports_kb
description: >
  A knowledge base containing historical post-incident reports and runbooks from past major incidents,
  stored in ElasticSearch. It is useful for identifying recurring issues, finding previous resolution
  steps, and understanding patterns in system failures.
conversational_search_tool:
  index_config:
    - elastic_search:
        # NOTE: Replace with the client's actual ElasticSearch URL for the real implementation.
        url: https://client.elasticsearch-instance.com
        index: incident-reports-index
        field_mapping:
          title: incident_id
          body: resolution_summary
          url: confluence_link
```

## Step 4: Create Agent YAML Configurations

Now we define the agents themselves. Each agent has a specific role, a set of tools, and instructions that guide its behavior and reasoning.

### 4.1 `triage_agent`

**Role:** Enriches alerts with business context.

**File:** `agents/triage_agent.yaml`

```yaml
spec_version: v1
kind: native
name: triage_agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  An IT Enrichment Specialist agent. Its sole purpose is to take a technical identifier, like a hostname,
  from an alert and enrich it with critical business context from the ServiceNow CMDB. It provides information
  like the affected business service, application owner, and service tier.
instructions: >
  Your only job is to use the get_cmdb_details tool.
  When you receive a hostname, immediately call the get_cmdb_details tool with that hostname.
  Return the full, unmodified JSON output from the tool. Do not add any conversational text.
tools:
  - get_cmdb_details
```

### 4.2 `rca_agent`

**Role:** Performs root cause analysis using logs, metrics, and historical data.

**File:** `agents/rca_agent.yaml`

```yaml
spec_version: v1
kind: native
name: rca_agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  A Root Cause Analyst agent. It investigates the technical root cause of an incident by
  correlating data from multiple sources. It can query ElasticSearch for logs, retrieve
  performance metrics from LogicMonitor, and search a knowledge base of past incidents
  to identify patterns and propose a probable root cause with a confidence score.
instructions: >
  You are an expert Root Cause Analyst. Your goal is to determine the most likely root cause of an IT incident.
  1.  When given an incident context (especially a hostname), first use the `query_elasticsearch_logs` tool to find relevant error messages around the incident time.
  2.  Next, use the `get_logicmonitor_metrics` tool to check for performance anomalies like CPU spikes or memory issues on the same host.
  3.  Search the `past_incident_reports_kb` knowledge base to see if similar incidents have occurred before.
  4.  Synthesize the information from the logs, metrics, and past incidents.
  5.  Provide a concise summary stating the "Probable root cause", a "Confidence Score" (e.g., 95%), and the key "Correlated evidence" that supports your conclusion.
tools:
  - query_elasticsearch_logs
  - get_logicmonitor_metrics
knowledge_base:
  - past_incident_reports_kb
```

### 4.3 `communications_agent`

**Role:** Manages stakeholder communications with tailored messaging.

**File:** `agents/communications_agent.yaml`

```yaml
spec_version: v1
kind: native
name: communications_agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  A Stakeholder Communications Manager agent. It is responsible for drafting and sending
  tiered communications to different audiences during a major incident. It can send detailed
  technical updates to an incident Slack channel and high-level business impact summaries
  to leadership via email.
instructions: >
  You are a communications expert. Your tone and content must match the target audience and channel.
  
  Persona 1: Technical Update for Slack
  - When asked to provide a technical update to a Slack channel, your message should be factual, concise, and include technical details.
  - Use the `send_slack_message` tool.
  - Example format: "TECHNICAL UPDATE: Investigation ongoing for INC0012345. Current finding: ORA-12541 errors found in logs for prod-db-01. RCA team is analyzing metrics."

  Persona 2: Business Update for Email
  - When asked to provide a business or leadership update via email, your message must focus on business impact.
  - Use the `send_email_update` tool.
  - Avoid technical jargon. Focus on: what is the impact on customers/business services, what is the current status, and what is the estimated time to resolution (if known).
  - Example subject: "Update: Service Disruption to Customer Billing Platform"
  - Example body: "The Customer Billing Platform is currently experiencing a service disruption. Technical teams are actively working on a resolution. The current customer impact is... We will provide another update in 30 minutes."
tools:
  - send_slack_message
  - send_email_update
```

### 4.4 `supervisor_agent`

**Role:** The central orchestrator, managing the end-to-end incident lifecycle.

**File:** `agents/supervisor_agent.yaml`

```yaml
spec_version: v1
kind: native
name: supervisor_agent
llm: watsonx/ibm/granite-13b-chat-v2
style: default
description: >
  The master Incident Commander agent that orchestrates the entire major incident response process.
  It receives the initial alert, creates official tickets and communication channels, then delegates
  specialized tasks like triage, root cause analysis, and communications to its team of collaborator agents.
  Finally, it concludes the process by generating a draft Post-Incident Report.
instructions: >
  You are the Incident Commander. Follow this sequence of operations precisely when you receive a new critical alert.
  
  Phase 1: Incident Initiation
  1.  From the initial alert, extract the hostname, service, and error message to form a description.
  2.  Delegate to the `triage_agent` with the hostname to get business context.
  3.  Using the enriched business context (especially the 'business_service'), use your `create_servicenow_ticket` tool to open a major incident.
  4.  Using the new ticket number, use your `create_slack_channel` tool to set up the war room.
  
  Phase 2: Investigation & Communication
  5.  Delegate to the `rca_agent` with the incident details (hostname, errors) to find the root cause.
  6.  While the RCA is in progress, delegate to the `communications_agent` to send an initial technical update to the new Slack channel and a business update to stakeholders.
  
  Phase 3: Resolution & Reporting
  7.  Once the `rca_agent` provides a root cause, report this finding.
  8.  After the incident is declared resolved (you will be told), use the `generate_pir_draft` tool to create the Post-Incident Report. You must provide it with the incident ID, the root cause from the rca_agent, and a summary of the timeline and resolution steps.
collaborators:
  - triage_agent
  - rca_agent
  - communications_agent
tools:
  - create_servicenow_ticket
  - create_slack_channel
  - generate_pir_draft
```

## Step 5: Import All Assets using ADK CLI

With all configuration and code files in place, you will now import them into your watsonx Orchestrate environment using the ADK CLI. **The order of operations is important**: tools and knowledge bases must be imported before the agents that depend on them. Likewise, collaborator agents must be imported before the supervisor that uses them.

```bash
# Ensure you are in the root 'incident_command_center' directory

# Step 5.1: Import all Python tools
echo "--- Importing Tools ---"
orchestrate tools import -f tools/triage_tools.py
orchestrate tools import -f tools/rca_tools.py
orchestrate tools import -f tools/communications_tools.py
orchestrate tools import -f tools/incident_commander_tools.py

# Step 5.2: Import the Knowledge Base
echo "--- Importing Knowledge Base ---"
orchestrate knowledge-bases import -f knowledge_bases/past_incident_reports_kb.yaml

# Step 5.3: Import the Collaborator Agents
echo "--- Importing Collaborator Agents ---"
orchestrate agents import -f agents/triage_agent.yaml
orchestrate agents import -f agents/rca_agent.yaml
orchestrate agents import -f agents/communications_agent.yaml

# Step 5.4: Import the Supervisor Agent (last)
echo "--- Importing Supervisor Agent ---"
orchestrate agents import -f agents/supervisor_agent.yaml

echo "--- All assets imported successfully! ---"
```

## Step 6: Verification and Demo Scenarios

After successfully importing all assets, you can begin testing and demonstrating the solution using the Orchestrate chat interface.

**Start the chat:**
```bash
orchestrate chat
```

### Scenario 1: End-to-End Incident Automation

This scenario demonstrates the full, orchestrated workflow from alert to report.

**User Prompt:**

> New critical alert received: { "timestamp": "2024-10-27T10:00:00Z", "hostname": "prod-db-01", "service": "Oracle DB Listener", "severity": "critical", "message": "Service is down" }

**Expected Orchestrate Behavior:**
1.  The `supervisor_agent` will activate.
2.  It will delegate to `triage_agent` to get CMDB details for `prod-db-01`.
3.  It will use its `create_servicenow_ticket` tool, resulting in an output like "INC12345".
4.  It will use `create_slack_channel` to create `#incident-inc12345`.
5.  It will delegate to `rca_agent`, which will query logs and metrics.
6.  `rca_agent` will respond with a probable root cause, e.g., "Oracle TNS Listener is down... Confidence: 95%".
7.  The `supervisor_agent` will then delegate communication tasks.
8.  Finally, if you prompt "The incident is resolved", it will call `generate_pir_draft`.

### Scenario 2: AI-Powered Root Cause Analysis

This scenario focuses specifically on the `rca_agent`'s capabilities.

**User Prompt (to `rca_agent` directly):**

> Investigate incident INC12345. The affected host is prod-db-01. Initial logs show ORA-12541 errors.

**Expected Orchestrate Behavior:**
1.  The `rca_agent` will execute its tools: `query_elasticsearch_logs` and `get_logicmonitor_metrics`.
2.  It will synthesize the results from the mock data (TNS error, CPU spike).
3.  It will produce a structured response: "Probable root cause: Oracle TNS Listener is down on host prod-db-01. Confidence Score: 95%. Correlated evidence: Logs show TNS-12541 errors starting at 09:59:58Z and metrics show a CPU spike to 99% on the host at the same time."

### Scenario 3: Tiered Stakeholder Communication

This scenario showcases the `communications_agent`'s persona-driven behavior.

**User Prompt (to `communications_agent`):**

> Send a technical update to the #incident-inc12345 channel about ORA-12541 errors on prod-db-01. Also, draft an email for leadership about the Customer Billing Platform outage.

**Expected Orchestrate Behavior:**
1.  The agent will call `send_slack_message` with a technical, jargon-filled message.
2.  The agent will then call `send_email_update` with a high-level, business-focused message, avoiding technical details and focusing on customer impact.

## Troubleshooting

-   **Tool Not Found Error**: If an agent fails because it cannot find a tool, ensure the tool's Python file was imported successfully using `orchestrate tools import`. Check for typos in the tool name in both the Python file (`@tool(name=...)`) and the agent's YAML file.
-   **Agent Delegation Failure**: If the `supervisor_agent` fails to delegate to a collaborator, check the descriptions of the collaborator agents. The supervisor uses these descriptions to decide which agent is best for a task. Ensure the descriptions are clear, accurate, and distinct.
-   **Incorrect LLM Behavior**: If an agent is not following instructions, try making the instructions more direct and explicit. Breaking down complex tasks into numbered steps, as done in the `supervisor_agent` instructions, can significantly improve reliability. You can also experiment with different LLMs available in your environment (`orchestrate llms list`).
-   **Context Passing Issues**: Ensure that the output of one tool or agent is in a simple format (like a JSON string) that can be easily consumed as input by the next step. Complex objects can cause context to be lost between steps.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
