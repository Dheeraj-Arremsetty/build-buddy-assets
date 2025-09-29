# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 15:17:34
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Field Service Co-Pilot

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building the **Field Service Co-Pilot**, an AI-powered maintenance assistant, for your client's demo. The solution is tailored to address the client's core business need: empowering field technicians with immediate, conversational access to critical information, thereby reducing repair times and improving first-time fix rates.

We will implement a multi-agent system using the supervisor/collaborator pattern within IBM watsonx Orchestrate. The **`Field_Service_CoPilot`** will act as the primary interface, intelligently routing technician queries to one of two specialized collaborator agents: the **`Manuals_Expert_Agent`**, which uses a knowledge base for RAG on technical manuals, and the **`Service_History_Agent`**, which uses a custom Python tool to query structured service logs. This plan includes all necessary code, configuration files, and commands to build and deploy this solution using the IBM watsonx Orchestrate Agent Development Kit (ADK).

## 2. Prerequisites

Before beginning, ensure your development environment is correctly configured.

*   **IBM watsonx Orchestrate ADK:** The ADK must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
*   **Python:** A recent version of Python (3.9+) is required.
*   **Orchestrate Environment:** An active watsonx Orchestrate environment must be initialized. Use the `orchestrate env init` command if you have not already done so.
*   **Project Structure:** Create the following directory structure to organize your files:

    ```sh
    field-service-copilot/
    ├── agents/
    │   ├── 01_service_history_agent.yaml
    │   ├── 02_manuals_expert_agent.yaml
    │   └── 03_field_service_copilot.yaml
    ├── tools/
    │   └── get_device_service_history.py
    ├── knowledge_base/
    │   └── manuals_kb.yaml
    ├── knowledge_base_docs/
    │   └── Z-5000_Technical_Manual.pdf
    └── requirements.txt
    ```
*   **Sample Document:** Create a placeholder PDF document named `Z-5000_Technical_Manual.pdf` inside the `knowledge_base_docs` directory. This document will be ingested into our knowledge base. For the demo, its content can be simple text describing fictitious repair procedures, such as:
    > **Section 5.1: Troubleshooting Error Code E-404**
    >
    > Error E-404 indicates a coolant system pressure failure.
    >
    > **Procedure:**
    > 1.  Power down the Z-5000 unit and disconnect from the main power supply.
    > 2.  Inspect the primary coolant intake valve (Part #PCV-101) for blockages.
    > 3.  Check the pressure sensor readings via the diagnostic port. The pressure should be between 45-55 PSI.
    > 4.  If pressure is low, refill the coolant reservoir and re-pressurize the system.
    > 5.  If the issue persists, replace the pressure sensor (Part #PS-202).

## 3. Step-by-Step Instructions

### Step 1: Create the Service History Tool

The `Service_History_Agent` requires a tool to access structured data. We will create a Python-based tool that generates realistic, synthetic service history for a given device ID. This simulates querying a CMMS or SQL database.

**Business Value:** This tool provides the agent with the ability to retrieve the complete maintenance history of a device. This is crucial for technicians to understand recurring issues, see what solutions were previously attempted, and avoid repeating ineffective repairs, directly contributing to a higher first-time fix rate and reduced MTTR.

**Technical Implementation:** The `get_device_service_history` function uses the `@tool` decorator to be recognized by the ADK. It accepts a `device_id` and returns a JSON-serializable list of dictionaries containing synthetic service records. The data is hardcoded for demo purposes but mimics the structure of a real database query result.

**File:** `tools/get_device_service_history.py`

```python
# tools/get_device_service_history.py

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# This tool generates synthetic data to simulate querying a service history database.
# In a real-world scenario, this function would connect to a SQL database,
# a REST API of a CMMS (e.g., Maximo), or another system of record.

@tool(name="get_device_service_history", permission=ToolPermission.ADMIN)
def get_device_service_history(device_id: str) -> List[Dict[str, Any]]:
    """
    Retrieves the complete maintenance and service history for a specific device based on its unique device ID.

    This tool is used to look up past repairs, reported issues, parts replaced, and technician notes.

    Args:
        device_id (str): The unique serial number or identifier for the device (e.g., "SN-98765").

    Returns:
        list[dict]: A list of service records for the device. Each record is a dictionary containing
                    details such as service date, technician, issue, actions taken, and parts replaced.
                    Returns an empty list if no history is found for the device ID.
    """
    print(f"Fetching service history for device: {device_id}")

    # Synthetic data for demonstration purposes
    history_data = {
        "SN-98765": [
            {
                "record_id": "SR-10234",
                "service_date": (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
                "technician_name": "Jane Doe",
                "issue_reported": "Device overheating and showing error code E-404.",
                "action_taken": "Cleaned primary coolant intake valve (Part #PCV-101) and refilled coolant. System pressure restored to 50 PSI. Monitored for 1 hour, no further errors.",
                "parts_replaced": [],
                "status": "Completed"
            },
            {
                "record_id": "SR-10156",
                "service_date": (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
                "technician_name": "John Smith",
                "issue_reported": "Unit making loud grinding noise during operation.",
                "action_taken": "Inspected main gear assembly. Found and replaced worn bearing.",
                "parts_replaced": ["Main Bearing Assembly (Part #MBA-305)"],
                "status": "Completed"
            }
        ],
        "SN-12345": [
            {
                "record_id": "SR-10255",
                "service_date": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                "technician_name": "Alice Johnson",
                "issue_reported": "Intermittent power failure.",
                "action_taken": "Checked power supply unit and main board connections. Reseated power connector P1. Issue could not be reproduced after fix.",
                "parts_replaced": [],
                "status": "Completed"
            }
        ]
    }

    # Return the history for the requested device_id, or an empty list if not found
    return history_data.get(device_id.strip(), [])

```

### Step 2: Create the Knowledge Base for Technical Manuals

The `Manuals_Expert_

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
