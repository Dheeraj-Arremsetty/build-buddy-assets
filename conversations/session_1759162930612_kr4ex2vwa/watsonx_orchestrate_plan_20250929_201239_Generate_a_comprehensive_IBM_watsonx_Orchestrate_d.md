# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 20:12:39
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Comprehensive Demo for Enterprise Integration

## Overview

This execution plan provides a detailed, step-by-step guide for creating a comprehensive IBM watsonx Orchestrate demonstration tailored for a client in the enterprise sector. The demo showcases a powerful, multi-agent architecture designed to address common enterprise challenges related to fragmented employee and customer support systems. We will build a supervisor agent, the **`Empower Agent`**, which acts as a central point of contact for employees. This agent intelligently orchestrates tasks by collaborating with specialized agents: a **`Customer Care Agent`** for handling healthcare benefits and provider queries, and a **`ServiceNow Agent`** for managing IT support incidents.

The solution leverages a knowledge base for answering HR policy questions via Retrieval-Augmented Generation (RAG), and a suite of custom Python tools that simulate interactions with backend systems like healthcare databases and an IT Service Management (ITSM) platform. This plan provides all necessary code, configuration files, and CLI commands to build and run the demo, demonstrating how watsonx Orchestrate can automate complex business processes, improve operational efficiency, and enhance user experiences.

## Prerequisites

Before beginning, ensure your environment is correctly set up. This is crucial for a smooth development and deployment process.

1.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. This is the primary toolset for building, importing, and managing agents and tools.
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
2.  **Python Environment**: A Python version compatible with the ADK (e.g., Python 3.10 or later) is required. It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Orchestrate Environment Initialization**: You must have an active watsonx Orchestrate environment configured. This involves logging into your Orchestrate instance via the CLI.
    ```bash
    orchestrate login
    ```
4.  **Project Directory Structure**: A well-organized directory is essential for managing the various components of the demo. Create the following structure in your local development environment:
    ```
    /empower_demo
    |-- /agents
    |   |-- customer_care_agent.yaml
    |   |-- service_now_agent.yaml
    |   |-- empower_agent.yaml
    |-- /tools
    |   |-- customer_care_tools.py
    |   |-- servicenow_tools.py
    |-- /knowledge_base_docs
    |   |-- pto_policy.txt
    |   |-- benefits_guide.pdf  (Create a dummy PDF for this)
    |-- requirements.txt
    ```

## Step 1: Create Python Tools for Backend System Simulation

Tools are the functional components that allow agents to perform actions. We will create two sets of tools: one for customer care and another for ServiceNow, simulating interactions with real enterprise systems by generating realistic synthetic data.

### 1.1 Customer Care Tools (`customer_care_tools.py`)

These tools simulate interactions with a healthcare provider's backend systems, providing information on benefits, claims, and providers. This demonstrates how Orchestrate can connect to and retrieve data from various enterprise data sources to serve customer needs effectively.

**File:** `empower_demo/tools/customer_care_tools.py`

```python
# empower_demo/tools/customer_care_tools.py

import json
from enum import Enum
from typing import List, Optional
import requests # Although we mock, we include it to match the tutorial's structure
from pydantic import BaseModel, Field

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# --- Tool 1: search_healthcare_providers ---

class ContactInformation(BaseModel):
    phone: str
    email: str

class HealthcareSpeciality(str, Enum):
    GENERAL_MEDICINE = 'General Medicine'
    CARDIOLOGY = 'Cardiology'
    PEDIATRICS = 'Pediatrics'
    ORTHOPEDICS = 'Orthopedics'
    ENT = 'Ear, Nose and Throat'
    MULTI_SPECIALTY = 'Multi-specialty'

class HealthcareProvider(BaseModel):
    provider_id: str = Field(description="The unique identifier of the provider")
    name: str = Field(description="The provider's name")
    provider_type: str = Field(description="Type of provider, (e.g. Hospital, Clinic)")
    specialty: HealthcareSpeciality = Field(description="Medical speciality")
    address: str = Field(description="The address of the provider")
    contact: ContactInformation = Field(description="The contact information of the provider")

@tool
def search_healthcare_providers(
        location: str,
        specialty: HealthcareSpeciality = HealthcareSpeciality.GENERAL_MEDICINE
) -> List[HealthcareProvider]:
    """
    Retrieves a list of the nearest healthcare providers based on location and optional specialty.
    This tool is essential for helping users find medical care quickly and efficiently.

    Args:
        location (str): Geographic location to search providers in (city, state, zip code, etc.).
        specialty (str, optional): Medical specialty to filter providers by. Must be one of:
            "ENT", "General Medicine", "Cardiology", "Pediatrics", "Orthopedics", "Multi-specialty".

    Returns:
        list: A list of healthcare providers near the specified location for the given specialty.
    """
    print(f"Searching for {specialty} providers in {location}...")
    # Mock data generation
    providers = [
        {"provider_id": "PRV54321", "name": f"{location} General Hospital", "provider_type": "Hospital", "specialty": specialty, "address": f"123 Health St, {location}", "contact": {"phone": "555-0101", "email": "contact@lgh.com"}},
        {"provider_id": "PRV98765", "name": f"Dr. Emily Carter ({specialty})", "provider_type": "Clinic", "specialty": specialty, "address": f"456 Wellness Ave, {location}", "contact": {"phone": "555-0102", "email": "ecarter.clinic@med.com"}},
    ]
    return providers

# --- Tool 2: get_healthcare_benefits ---

class Plan(str, Enum):
    HDHP = 'HDHP'
    HDHP_Plus = 'HDHP Plus'
    PPO = 'PPO'

@tool
def get_healthcare_benefits(plan: Plan, in_network: bool = None) -> list[dict]:
    """
    Retrieves a comprehensive list of health benefits data, organized by coverage type and plan variant.
    This tool empowers users by providing transparent access to complex benefits information.

    Args:
        plan (str, optional): The plan the user is currently on. Can be one of "HDHP", "HDHP Plus", or "PPO".
        in_network (bool, optional): Whether the user wants coverage for in-network or out-of-network.

    Returns:
        list[dict]: A list of dictionaries containing detailed benefits information.
    """
    print(f"Fetching benefits for plan: {plan}")
    

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
