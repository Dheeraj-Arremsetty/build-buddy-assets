# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 15:01:42
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Comprehensive Demo Execution Plan

## Overview
This execution plan provides a detailed, step-by-step guide for creating a comprehensive IBM watsonx Orchestrate demo tailored for your client in the healthcare administration sector. The demo showcases a sophisticated, multi-agent architecture designed to automate and streamline employee support processes. The central component is the **"Empower"** agent, a supervisor agent that orchestrates tasks between two specialized collaborator agents: a `customer_care_agent` for handling healthcare benefits and claims inquiries, and a `service_now_agent` for managing IT and administrative support tickets. This solution directly addresses the client's need to reduce manual workloads, provide instant, accurate answers to employees, and create an efficient, scalable digital workforce. By integrating data retrieval (RAG), transaction processing, and inter-agent collaboration, this demo will powerfully illustrate how watsonx Orchestrate can solve complex, cross-application business process challenges.

## Prerequisites
Before beginning the implementation, ensure your development environment is correctly configured.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and up-to-date. If you haven't installed it, run the following command:
    ```bash
    pip install --upgrade ibm-watsonx-orchestrate
    ```
2.  **Python Environment**: A working Python environment (version 3.9 or higher) is required to create the custom tools.
3.  **Project Directory**: Create a dedicated project directory to organize all your files. This structure is crucial for managing agents, tools, and knowledge bases effectively.
    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir -p agents tools knowledge_base
    ```
4.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. If you have not already done so, initialize your environment and log in.
    ```bash
    # Initialize your environment (run only once)
    orchestrate env init

    # Log in to your environment
    orchestrate login
    ```
5.  **Text Editor**: A code editor like Visual Studio Code is recommended for creating and editing the YAML and Python files.

## Step 1: Create the Knowledge Base
The knowledge base will serve as the foundation for answering general employee questions, such as company policies and FAQs. This demonstrates the Retrieval-Augmented Generation (RAG) capabilities of watsonx Orchestrate, providing grounded, accurate answers from trusted company documents.

### 1.1. Create the Source Document
First, create a sample text file containing common employee questions. This file will be ingested into the built-in Milvus vector database.

**File:** `knowledge_base/employee_faq.txt`
```text
Company FAQ Document

## Remote Work Policy
Q: What is the company's policy on remote work?
A: Our company offers a hybrid work model. Employees are expected to be in the office 3 days a week (Tuesday, Wednesday, Thursday). Specific arrangements can be made with your direct manager. All remote work must be performed from your registered home address within the country.

## Expense Reports
Q: How do I submit an expense report?
A: All expense reports must be submitted through the Concur portal within 30 days of the expense date. Please include digital copies of all receipts. For expenses over $100, manager approval is required before submission.

## Onboarding Documents
Q: Where can I find my onboarding documents?
A: Your onboarding documents, including your employment contract and tax forms, are available in your Workday profile under the "Documents" section. If you cannot locate them, please file a support ticket with HR.
```

### 1.2. Create the Knowledge Base Configuration File
Next, define the knowledge base in a YAML file. This configuration tells Orchestrate how to create the knowledge base, what embedding model to use, and which documents to ingest.

**File:** `knowledge_base/empower_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base 
name: empower_employee_kb
description: >
   Contains essential information for employees, including company policies on remote work, expense reporting procedures, and guidance on accessing HR documents. Use this to answer general employee questions.
documents:
   - "knowledge_base/employee_faq.txt"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Create Python Tools
Tools are the functional building blocks that allow agents to interact with external systems and perform actions. We will create tools for both the `customer_care_agent` and the `service_now_agent`. Each tool will generate realistic synthetic data to simulate real-world API responses.

### 2.1. Create a `requirements.txt` File
This file lists any external Python libraries our tools depend on. The ADK will automatically install these when the tools are imported. For this demo, we will use the `requests` library to demonstrate a common pattern, even though our mock data is generated locally.

**File:** `tools/requirements.txt`
```text
requests
pydantic
```

### 2.2. Tools for the `customer_care_agent`
These tools simulate interactions with a healthcare benefits and claims system.

#### 2.2.1. Get Healthcare Benefits Tool
**Business Value:** This tool provides immediate, detailed information about healthcare plan benefits. It empowers employees to self-serve and compare plans, reducing the number of inquiries to the HR department. It simulates fetching data from a core HR benefits system like Workday or a third-party provider.

**File:** `tools/get_healthcare_benefits.py`
```python
# tools/get_healthcare_benefits.py
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool(permission=ToolPermission.ADMIN)
def get_healthcare_benefits(plan: Plan, in_network: bool = None) -> list[dict]:
    """Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (str): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.
            If not provided, both will be returned.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains benefit details for the specified plan.
    """
    # In a real scenario, this would make an API call. Here, we generate synthetic data.
    full_benefits_data = [
        {'Coverage': 'Annual Deductible', 'HDHP (In-Network)': '$3,000', 'HDHP (Out-of-Network)': '$6,000', 'HDHP Plus (In-Network)': '$2,000', 'HDHP Plus (Out-of-Network)': '$4,000', 'PPO (In-Network)': '$1,000', 'PPO (Out-of-Network)': '$2,000'},
        {'Coverage': 'Out-of-Pocket Maximum', 'HDHP (In-Network)': '$7,000', 'HDHP (Out-of-Network)': '$14,000', 'HDHP Plus (In-Network)': '$6,000', 'HDHP Plus (Out-of-Network)': '$12,000', 'PPO (In-Network)': '$5,000', 'PPO (Out-of-Network)': '$10,000'},
        {'Coverage': 'Primary Care Visit', 'HDHP (In-Network)': '20% after deductible', 'HDHP (Out-of-Network)': '40% after deductible', 'HDHP Plus (In-Network)': '$30 copay', 'HDHP Plus (Out-of-Network)': '40% after deductible', 'PPO (In-Network)': '$25 copay', 'PPO (Out-of-Network)': '40% after deductible'},
        {'Coverage': 'Specialist Visit', 'HDHP (In-Network)': '20% after deductible', 'HDHP (Out-of-Network)': '40% after deductible', 'HDHP Plus (In-Network)': '$50 copay', 'HDHP Plus (Out-of-Network)': '40% after deductible', 'PPO (In-Network)': '$40 copay', 'PPO (Out-of-Network)': '40% after deductible'},
        {'Coverage': 'Emergency Room', 'HDHP (In-Network)': '$250 copay then 20% after deductible', 'HDHP (Out-of-Network)': '$250 copay then 40% after deductible', 'HDHP Plus (In-Network)': '$200 copay', 'HDHP Plus (Out-of-Network)': '$200 copay then 40% after deductible', 'PPO (In-Network)': '$150 copay', 'PPO (Out-of-Network)': '$150 copay then 40% after deductible'}
    ]
    
    # Filter data based on input parameters to simulate API behavior
    plan_key_in_network = f"{plan.value} (In-Network)"
    plan_key_out_network = f"{plan.value} (Out-of-Network)"
    
    filtered_benefits = []
    for item in full_benefits_data:
        new_item = {'Coverage': item['Coverage']}
        if in_network

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
