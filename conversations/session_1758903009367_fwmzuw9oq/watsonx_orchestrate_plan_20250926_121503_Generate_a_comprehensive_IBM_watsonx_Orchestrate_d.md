# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-26 12:15:03
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Barista Buddy Demo

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the "Barista Buddy" demo using IBM watsonx Orchestrate. This solution is specifically designed for the client in the coffee retail industry to address the challenges of high employee turnover, inconsistent training, and the need for immediate operational support.

The "Barista Buddy" is a multi-agent system that acts as a digital assistant for cafe staff. It streamlines new-hire onboarding, provides instant access to proprietary recipes and equipment manuals via a knowledge base, and handles basic HR inquiries. The architecture features a central **Supervisor Agent** (`Barista_Buddy_Agent`) that intelligently routes tasks to specialized **Collaborator Agents** for onboarding, operations/recipes, and HR. This plan will guide you through creating the mock data, building the knowledge base, developing the Python tools, configuring all agents, and deploying the complete solution using the IBM watsonx Orchestrate Agent Development Kit (ADK).

## 2. Prerequisites

Before you begin, ensure your development environment is set up correctly.

*   **Python:** Python 3.10 or later installed.
*   **IBM watsonx Orchestrate ADK:** The ADK must be installed and configured. If not installed, run the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate[adk]"
    ```
*   **Orchestrate Environment:** You must have an active watsonx Orchestrate environment initialized. If you haven't done so, run:
    ```bash
    orchestrate env init --name my-dev-env
    ```
    Follow the prompts to configure your environment.
*   **Project Structure:** Create the following directory structure to organize your files:
    ```
    barista_buddy_demo/
    |-- agents/
    |   |-- 1_hr_connect_agent.yaml
    |   |-- 2_onboarding_pro_agent.yaml
    |   |-- 3_recipe_and_ops_agent.yaml
    |   |-- 4_barista_buddy_agent.yaml
    |-- tools/
    |   |-- onboarding_tools.py
    |   |-- hr_tools.py
    |-- knowledge_base/
    |   |-- documents/
    |   |   |-- Barista_Recipe_Book.pdf
    |   |   |-- Espresso_Machine_Troubleshooting_Guide.pdf
    |   |   |-- Employee_Handbook.docx
    |   |-- barista_knowledge.yaml
    |-- requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Prepare Mock Data and Knowledge Base

The `Recipe_And_Ops_Agent` relies on a knowledge base for providing information on drink recipes, equipment, and company policies. We will create this using the built-in Milvus vector database provided by watsonx Orchestrate.

**A. Create Mock Documents:**

In the `barista_buddy_demo/knowledge_base/documents/` directory, create the following files with sample content. These will be ingested into the knowledge base.

*   `Barista_Recipe_Book.pdf`: A PDF containing recipes. (e.g., "Caramel Macchiato: 1 shot espresso, 2 pumps vanilla syrup, steamed milk, caramel drizzle.")
*   `Espresso_Machine_Troubleshooting_Guide.pdf`: A PDF with common issues. (e.g., "Problem: Low pressure. Solution: Check the water tank and ensure the portafilter is sealed correctly.")
*   `Employee_Handbook.docx`: A document with store policies. (e.g., "Dress Code: All employees must wear a company-provided apron and non-slip shoes.")

**B. Create the Knowledge Base Configuration File:**

This YAML file defines the knowledge base, its description, and the documents to be ingested. The description is crucial as it helps agents understand what information this knowledge base contains.

`barista_buddy_demo/knowledge_base/barista_knowledge.yaml`
```yaml
spec_version: v1
kind: knowledge_base 
name: barista_knowledge
description: >
   Contains comprehensive information for cafe operations. Use this to answer questions about drink recipes, 
   how to prepare beverages, troubleshoot coffee equipment like espresso machines, and understand general 
   store policies from the employee handbook.
documents:
   - "knowledge_base/documents/Barista_Recipe_Book.pdf"
   - "knowledge_base/documents/Espresso_Machine_Troubleshooting_Guide.pdf"
   - "knowledge_base/documents/Employee_Handbook.docx"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 2: Create Python Tools

The `Onboarding_Pro_Agent` and `HR_Connect_Agent` will use custom Python tools to perform actions and retrieve data from mock systems.

**A. Create `requirements.txt`:**

Create this file to specify the Python dependencies for your tools. For this demo, we only need the Orchestrate library itself.

`barista_buddy_demo/requirements.txt`
```text
ibm-watsonx-orchestrate
```

**B. Create Onboarding Tools:**

These tools simulate interactions with an onboarding system, providing training schedules and document access for new hires.

`barista_buddy_demo/tools/onboarding_tools.py`
```python
import json
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_training_schedule", description="Fetches the training schedule for a new barista for a given day.", permission=ToolPermission.ADMIN)
def get_training_schedule(employee_id: str, day: int) -> str:
    """
    Retrieves the new hire training schedule for a specific day.

    Args:
        employee_id (str): The unique identifier for the employee.
        day (int): The training day number (e.g., 1 for the first day).

    Returns:
        str: A JSON string representing the schedule with tasks and timings.
    """
    schedules = {
        1: [
            {"time": "09:00 AM", "task": "Welcome & Store Tour", "status": "Pending"},
            {"time": "10:00 AM", "task": "Health & Safety Video Training", "status": "Pending"},
            {"time": "12:00 PM", "task": "Lunch Break", "status": "N/A"},
            {"time": "01:00 PM", "task": "Introduction to Point-of-Sale (POS) System", "status": "Pending"},
        ],
        2: [
            {"time": "09:00 AM", "task": "Espresso Machine Basics: Grinding and Tamping", "status": "Pending"},
            {"time": "11:00 AM", "task": "Milk Steaming and Latte Art Practice", "status": "Pending"},
            {"time": "01:00 PM", "task": "Shadowing a Senior Barista on Bar", "status": "Pending"},
        ]
    }
    schedule = schedules.get(day, [])
    if not schedule:
        return json.dumps({"error": f"No schedule found for employee {employee_id} on day {day}."})
    return json.dumps({"employee_id": employee_id, "day": day, "schedule": schedule})

@tool(name="complete_onboarding_task", description="Marks a specific onboarding task as complete for a new hire.", permission=ToolPermission.ADMIN)
def complete_onboarding_task(employee_id: str, task_name: str) -> str:
    """
    Marks a new hire's onboarding task as complete in the system.

    Args:
        employee_id (str): The unique identifier for the employee.
        task_name (str): The exact name of the task to be marked as complete.

    Returns:
        str: A JSON string confirming the status update.
    """
    # In a real system, this would update a database.
    print(f"Updating task '{task_name}' for employee '{employee_id}' to 'Completed'.")
    return json.dumps({
        "employee_id": employee_id,
        "task_name": task_name,
        "new_status": "Completed",
        "timestamp": datetime.now().isoformat()
    })

@tool(name="fetch_new_hire_documents", description="Provides links to essential new hire documents like tax forms and policy acknowledgements.", permission=ToolPermission.ADMIN)
def fetch_new_hire_documents(employee_id: str) -> str:
    """
    Retrieves a list of required documents for a new hire to complete.

    Args:
        employee_id (str): The unique identifier for the employee.

    Returns:
        str: A JSON string containing a list of documents with their status and a mock link.
    """
    documents = [
        {"document_name": "W-4 Tax Form", "status": "Pending", "link": "http://mock-hr.com/docs/w4"},

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
