# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 09:51:44
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

Here is a comprehensive IBM watsonx Orchestrate execution plan tailored to a specific client demo concept.

# IBM watsonx Orchestrate Demo Execution Plan for InnovateHealth

## 1. Overview

This execution plan details the creation of a comprehensive demo for **InnovateHealth**, a large healthcare institution, using IBM watsonx Orchestrate. The primary goal is to showcase how Orchestrate can create a sophisticated, multi-agent "Digital Labor" solution to automate and streamline both internal employee HR processes and external member support services. InnovateHealth currently faces challenges with fragmented support systems, leading to long resolution times for employee inquiries about HR policies (e.g., tuition reimbursement) and member questions regarding benefits, claims, and provider lookups.

The proposed solution, the **InnovateHealth Assistant**, is a hierarchical agent system. A top-level **Supervisor Agent** intelligently routes user requests to specialized **Collaborator Agents** for HR, Customer Care, and ServiceNow ticketing. This demonstrates Orchestrate's power to integrate disparate business functions, leverage both custom tools for data retrieval and knowledge bases for policy information, and create a seamless, conversational experience for users, ultimately improving efficiency and satisfaction. This plan provides all necessary code, configuration, and commands to build and deploy this solution from the ground up.

## 2. Prerequisites

Before beginning, ensure your environment is correctly configured.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and up-to-date.
    ```bash
    pip install --upgrade ibm-watsonx-orchestrate
    ```
*   **Python**: Python 3.9 or higher is required.
*   **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. Initialize it using the CLI if you haven't already.
    ```bash
    # Log in to your IBM Cloud account
    ibmcloud login
    # Initialize your Orchestrate environment
    orchestrate environment init
    ```
*   **Required Python Libraries**: Create a `requirements.txt` file in your project's root directory with the following content. These libraries are used by the custom tools.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
    Install the dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
*   **Project Structure**: Create the following directory structure to organize your assets. This structure is critical for the import commands to work correctly.
    ```
    innovatehealth-demo/
    ├── agents/
    │   ├── 01_service_now_agent.yaml
    │   ├── 02_customer_care_agent.yaml
    │   ├── 03_hr_agent.yaml
    │   └── 04_innovate_health_assistant.yaml
    ├── tools/
    │   ├── customer_care/
    │   │   ├── get_healthcare_benefits.py
    │   │   ├── get_my_claims.py
    │   │   └── search_healthcare_providers.py
    │   └── service_now/
    │       ├── create_service_now_incident.py
    │       └── get_my_service_now_incidents.py
    ├── knowledge_base/
    │   └── hr_policy_kb.yaml
    ├── knowledge_base_docs/
    │   ├── tuition_reimbursement.txt
    │   └── employee_handbook.txt
    └── requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Create Mock Knowledge Base Documents

First, we will create simple text files that will be ingested into a knowledge base. This knowledge base will be used by the `hr_agent` to provide accurate, document-grounded answers to employee questions about company policies, demonstrating the powerful RAG (Retrieval-Augmented Generation) capabilities of watsonx Orchestrate.

**File: `knowledge_base_docs/tuition_reimbursement.txt`**
```text
InnovateHealth Tuition Reimbursement Policy

Effective Date: January 1, 2024
Policy ID: IH-HR-TR-001

Eligibility:
All full-time employees who have completed at least six months of continuous service are eligible to participate in the Tuition Reimbursement Program.

Covered Expenses:
InnovateHealth will reimburse up to $5,250 per calendar year for tuition, fees, and required books for pre-approved courses at accredited institutions. Courses must be relevant to the employee's current role or a potential future role within the company.

Reimbursement Process:
1. Submit an application for course pre-approval to your manager at least 30 days before the course start date.
2. Upon successful completion of the course with a grade of 'B' or better (or 'Pass' in a Pass/Fail system), submit the reimbursement request form, proof of payment, and your final grades to the HR department within 60 days of course completion.
3. Reimbursement will be processed and included in your paycheck within two pay cycles.
```

**File: `knowledge_base_docs/employee_handbook.txt`**
```text
InnovateHealth Employee Handbook - Excerpt

Work Hours:
Standard office hours are from 9:00 AM to 5:00 PM, Monday through Friday. Flexible work arrangements may be available with manager approval.

Paid Time Off (PTO):
Full-time employees accrue PTO based on their years of service. New hires start with an accrual rate of 15 days per year.

Contact HR:
For any questions regarding company policies, please contact the HR department at hr-support@innovatehealth.com or open a ticket through the employee portal.
```

### Step 2: Create Python Tools

Next, we will create the Python tools that our agents will use to perform actions. These tools generate realistic synthetic data to simulate interactions with real backend systems like a claims database, provider directory, or a ServiceNow instance. Each tool follows the IBM ADK pattern with the `@tool` decorator and a detailed docstring that the agent's LLM uses to understand its function.

#### Customer Care Tools

**File: `tools/customer_care/get_healthcare_benefits.py`**

**Business Value**: This tool is crucial for the `customer_care_agent` to provide accurate and structured benefit details to members, reducing confusion and support calls. It directly addresses member inquiries about what their plan covers, empowering them with self-service information and improving member satisfaction.

**Technical Implementation**: The tool uses a Python dictionary to mock a database of benefits for different insurance plans (`HDHP`, `HDHP Plus`, `PPO`). It accepts a plan type and an optional network preference, filtering the data to return a structured list of dictionaries that is easily interpreted by the LLM and presented to the user.

```python
# tools/customer_care/get_healthcare_benefits.py
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
from typing import List, Dict, Optional

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool(name="get_healthcare_benefits", permission=ToolPermission.ADMIN)
def get_healthcare_benefits(plan: Plan, in_network: Optional[bool] = None) -> List[Dict]:
    """
    Retrieves a comprehensive list of health benefits data for InnovateHealth members, organized by coverage type and plan variant.

    This tool provides details such as annual deductibles, out-of-pocket maximums, and various co-pays for medical services
    under different network plans (HDHP, HDHP Plus, and PPO). It helps members understand their coverage.

    Args:
        plan (str): The specific plan to query. Must be one of "HDHP", "HDHP Plus", or "PPO".
        in_network (bool, optional): Specify whether to return coverage for in-network or out-of-network providers.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains benefit details for the specified plan.
    """
    benefits_data = {
        "HDHP": [
            {'Coverage': 'Annual Deductible', 'In-Network': '$3,000', 'Out-of-Network': '$6,000'},
            {'Coverage': 'Out-of-Pocket Max', 'In-Network': '$7,000', 'Out-of-Network': '$14,000'},
            {'Coverage': 'Primary Care Visit', 'In-Network': '100% after deductible', 'Out-of-Network': '80% after deductible'},
        ],
        "HDHP Plus": [
            {'Coverage': 'Annual Deductible', 'In-Network': '$2,000', 'Out-of-Network': '$4,000'},
            {'Coverage': 'Out-of-Pocket Max', 'In-Network': '$5,000', 'Out-of-Network': '$10,000'},
            {'Coverage': 'Primary Care Visit', 'In-Network': '$30 co-pay', 'Out-of-Network': '80% after deductible'},
        ],
        "PPO": [
            {'Coverage': 'Annual Deductible', 'In-Network': '$1,000', 'Out-of-Network': '$2,500'},
            {'Coverage': 'Out-of-Pocket Max', 'In-Network': '$4,000', 'Out-of-Network': '$8,000'},
            {'Coverage': 'Primary Care Visit', 'In-Network': '$25 co-pay',

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
