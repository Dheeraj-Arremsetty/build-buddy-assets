# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-16 10:16:06
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: "Empower" Agent for Employee Success

## Overview
This execution plan provides a comprehensive, step-by-step guide for building a sophisticated, multi-agent demonstration for your healthcare institution client using IBM watsonx Orchestrate. The demo, centered around the **"Empower" agent**, is designed to showcase how Orchestrate can serve as a central hub for employee success, seamlessly integrating HR, benefits, and IT support functions.

The proposed architecture features a supervisor agent ("Empower") that intelligently delegates tasks to specialized collaborator agents: a **`customer_care_agent`** for handling healthcare benefits and claims, and a **`service_now_agent`** for managing IT and HR support incidents. This layered approach demonstrates Orchestrate's powerful reasoning and routing capabilities, providing a single, conversational interface for complex, multi-domain employee inquiries. The plan includes the creation of all necessary agents, tools with realistic synthetic data, and a knowledge base to create a fully functional and compelling demonstration tailored to the client's specific business needs.

## Prerequisites
Before beginning, ensure your development environment is properly configured.

1.  **IBM watsonx Orchestrate ADK:** The Agent Development Kit (ADK) must be installed and configured.
    ```bash
    pip install "ibm-watsonx-orchestrate[all]"
    ```
2.  **Python Environment:** A working Python environment (version 3.10 or later) is required to create the custom tools.
3.  **Orchestrate Environment:** You must have an active watsonx Orchestrate environment configured. Use the following command to set up and activate your environment.
    ```bash
    # Configure your environment (run once)
    orchestrate env add
    
    # Activate your environment for the current session
    orchestrate env use <your_environment_name>
    ```
4.  **Project Directory:** Create a dedicated directory to organize all demo assets.
    ```bash
    mkdir empower-demo
    cd empower-demo
    mkdir agents tools knowledge_docs
    ```

---

## Step 1: Create the Knowledge Base for Company Policies

To enable the "Empower" agent to answer general policy and procedure questions, we will create a knowledge base from internal documents. This demonstrates Retrieval-Augmented Generation (RAG), allowing the agent to provide accurate answers based on trusted company sources.

### 1.1. Create Mock Documents
First, create mock FAQ and benefits documents inside the `knowledge_docs` directory.

**File: `knowledge_docs/employee_faq.txt`**
```text
Employee Frequently Asked Questions (FAQ)

Q: What is the company policy on Paid Time Off (PTO)?
A: Full-time employees accrue 15 days of PTO per year for the first 5 years of service. After 5 years, this increases to 20 days per year. PTO requests should be submitted through the Workday portal at least two weeks in advance.

Q: How do I reset my network password?
A: If you need to reset your password, please open a ticket with the IT help desk. You can say "I need to create a ticket to reset my password" to get started.

Q: Where can I find details about my health benefits?
A: You can ask about your specific health plan benefits, check the status of a claim, or find a healthcare provider in your network. Just ask a question like "What are the benefits for the PPO plan?" or "Find me a cardiologist in Boston".
```

### 1.2. Create Knowledge Base Configuration
Next, create the YAML configuration file that defines the knowledge base and points to the documents.

**File: `empower_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: empower_company_policies_kb
description: >
   Contains comprehensive information about company policies, employee benefits, IT procedures, and frequently asked questions (FAQs). Use this to answer general employee inquiries about internal processes.
documents:
   - "knowledge_docs/employee_faq.txt"
vector_index:
   # Using the default watsonx.ai embedding model
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### 1.3. Import the Knowledge Base
Use the ADK CLI to import the knowledge base into your Orchestrate environment.

```bash
orchestrate knowledge-bases import -f empower_kb.yaml
```

---

## Step 2: Create Custom Python Tools

The core functionality of the collaborator agents is provided by custom tools. We will create six Python tools that generate realistic, synthetic data for healthcare and ServiceNow scenarios.

### Tool 1: Get Healthcare Benefits (`get_healthcare_benefits.py`)

**Business Value:** This tool empowers employees to self-serve information about their healthcare plans, reducing the burden on HR staff. It provides clear, structured data on deductibles, co-pays, and coverage, helping employees make informed decisions about their healthcare.

**Technical Implementation:** The tool simulates a request to an internal benefits API. It defines a `Plan` enum for valid inputs and returns a list of dictionaries containing detailed benefits information for different plans, which the agent can then format for the user.

**File: `tools/get_healthcare_benefits.py`**
```python
import json
from enum import Enum
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool(name="get_healthcare_benefits", permission=ToolPermission.ADMIN)
def get_healthcare_benefits(plan: Plan) -> str:
    """
    Retrieves a comprehensive list of health benefits data for a specific plan variant.

    This data includes details such as annual deductibles, out-of-pocket maximums, and various co-pays or
    percentages for medical services under different network plans (HDHP, HDHP Plus, and PPO).

    Args:
        plan (str): The plan the user is asking about. Must be one of "HDHP", "HDHP Plus", or "PPO".

    Returns:
        str: A JSON string representing a list of dictionaries with benefit details for the requested plan.
    """
    benefits_data = {
        "HDHP": [
            {"Coverage": "Annual Deductible", "In-Network": "$3,000", "Out-of-Network": "$6,000"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$6,000", "Out-of-Network": "$12,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "100% after deductible", "Out-of-Network": "70% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "90% after deductible", "Out-of-Network": "60% after deductible"},
        ],
        "HDHP Plus": [
            {"Coverage": "Annual Deductible", "In-Network": "$2,000", "Out-of-Network": "$4,000"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$5,000", "Out-of-Network": "$10,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "$40 Copay", "Out-of-Network": "70% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "$60 Copay", "Out-of-Network": "60% after deductible"},
        ],
        "PPO": [
            {"Coverage": "Annual Deductible", "In-Network": "$1,000", "Out-of-Network": "$2,500"},
            {"Coverage": "Out-of-Pocket Max", "In-Network": "$4,000", "Out-of-Network": "$8,000"},
            {"Coverage": "Primary Care Visit", "In-Network": "$25 Copay", "Out-of-Network": "80% after deductible"},
            {"Coverage": "Specialist Visit", "In-Network": "$50 Copay", "Out-of-Network": "70% after deductible"},
        ]
    }
    
    result = benefits_data.get(plan, [])
    return json.dumps(result)

```
**Import Command:**
```bash
orchestrate tools import -k python -f tools/get_healthcare_benefits.py
```

### Tool 2: Get My Claims (`get_my_claims.py`)

**Business Value:** This tool provides employees with immediate access to the status of their medical claims, answering common questions like "Was my claim approved?" without needing to call the insurance provider or HR. This transparency improves employee satisfaction and reduces administrative overhead.

**Technical Implementation:**

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
