# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-19 12:04:57
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: "Empower" Employee Success Agent

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying a sophisticated, multi-agent solution within IBM watsonx Orchestrate. The demo, titled **"Empower: An agent for employee success,"** is designed to showcase the platform's core capabilities, including agent collaboration, custom tool integration, and intelligent task routing. The primary goal is to create a central "Empower" agent that acts as an intelligent front door for employee inquiries. This agent will delegate tasks to specialized collaborator agents—a **`customer_care_agent`** for handling benefits and healthcare questions, and a **`service_now_agent`** for managing IT and support incidents.

This solution directly addresses the common business challenge of fragmented employee support systems. By orchestrating interactions between different backend services (simulated via custom tools), the "Empower" agent provides a seamless, conversational experience for employees. It demonstrates how watsonx Orchestrate can automate complex workflows, reduce manual effort for HR and IT teams, and provide employees with fast, accurate answers to their questions, thereby improving overall operational efficiency and employee satisfaction.

## Prerequisites

Before beginning the implementation, ensure your development environment is correctly configured. This is crucial for the successful creation, import, and testing of the agents and tools.

1.  **Python Environment**: A working installation of Python (version 3.9 or higher) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command in your terminal:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must be logged into an active watsonx Orchestrate environment.
    *   **For SaaS Environment**: Log in using the CLI.
        ```bash
        orchestrate login
        ```
    *   **For Developer Edition**: Start the local server. You may need to provide the path to your `.env` file.
        ```bash
        orchestrate server start -e <path-to-.env-file>
        ```
4.  **Project Directory Structure**: To maintain a clean and organized project, create the following directory structure. This separation of concerns is a best practice for managing complex agent solutions.

    ```
    empower-demo/
    ├── agents/
    │   ├── customer_care_agent.yaml
    │   ├── service_now_agent.yaml
    │   └── empower_agent.yaml
    ├── tools/
    │   ├── customer_care/
    │   │   ├── get_healthcare_benefits.py
    │   │   ├── get_my_claims.py
    │   │   └── search_healthcare_providers.py
    │   └── service_now/
    │       ├── create_service_now_incident.py
    │       ├── get_my_service_now_incidents.py
    │       └── get_service_now_incident_by_number.py
    └── requirements.txt
    ```

## Step 1: Create the Tools

Tools are the building blocks of an agent's capabilities, enabling it to interact with external systems and perform actions. We will create six Python-based tools, divided into `customer_care` and `service_now` categories. Each tool will generate realistic synthetic data to simulate interactions with real enterprise platforms.

### 1.1 Customer Care Tools

These tools simulate interactions with a healthcare benefits and provider system.

#### `get_healthcare_benefits.py`

**Business Value**: This tool provides immediate, on-demand access to detailed health plan information. It empowers employees to self-serve and compare benefits, reducing the number of inquiries to the HR department. For the business, this means faster resolution times and a more informed workforce.

**Technical Implementation**: The tool uses the `requests` library to call a mock API endpoint (provided in the tutorial reference material). It accepts a `Plan` type and an optional `in_network` boolean to filter the results, demonstrating how agents can handle specific user queries. The function returns a list of dictionaries containing the benefits data, which is easily parsed and presented by the agent.

```python
# empower-demo/tools/customer_care/get_healthcare_benefits.py

from enum import Enum
import requests
from ibm_watsonx_orchestrate.agent_builder.tools import tool

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool
def get_healthcare_benefits(plan: Plan, in_network: bool = None):
    """Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO). Use this tool
    when a user asks about health plan details, coverage, or wants to compare plans.

    Args:
        plan (str, optional): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
            If not provided, all plans will be returned.
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains detailed coverage information for the specified plans.
    """
    try:
        resp = requests.get(
            'https://get-benefits-data.1sqnxi8zv3dh.us-east.codeengine.appdomain.cloud/',
            params={
                'plan': plan,
                'in_network': in_network
            }
        )
        resp.raise_for_status()
        return resp.json()['benefits']
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to retrieve healthcare benefits: {str(e)}"}
```

#### `get_my_claims.py`

**Business Value**: This tool provides employees with instant visibility into the status of their medical claims. It eliminates the need for employees to call support lines or navigate complex portals, saving time for both the employee and the claims processing department.

**Technical Implementation**: This function generates a static list of synthetic claim data. The data includes various statuses ('Processed', 'Pending', 'Rejected') and detailed information like claim IDs, amounts, and provider details. This demonstrates how an

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
