# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-30 15:21:38
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Nespresso AI Customer Concierge

## Overview
This execution plan details the creation of a sophisticated, multi-agent AI Customer Concierge for Nespresso using IBM watsonx Orchestrate. The solution is designed to address Nespresso's key business objectives: enhancing the premium customer experience, reducing call center volume for routine inquiries, and driving sales through personalized interactions. The core of this solution is a supervisor agent, the **Nespresso_Concierge_Agent**, which intelligently understands customer intent and delegates tasks to a team of specialized collaborator agents. These specialists handle machine troubleshooting by referencing a knowledge base of manuals, provide personalized coffee recommendations based on taste profiles, and retrieve real-time order status information. This plan provides a complete, step-by-step guide with all necessary code, configuration files, and commands to build and demonstrate this powerful proof-of-concept.

## Prerequisites
Before you begin, ensure your development environment is set up correctly. This plan requires the following components:

1.  **Python**: Ensure you have Python 3.8 or later installed.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit is essential for building and deploying agents, tools, and knowledge bases. If not installed, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **IBM watsonx Orchestrate Environment**: You must have access to an active watsonx Orchestrate environment and be logged in via the CLI. To configure your environment, use the `orchestrate env` commands.
4.  **Text Editor**: A code editor like Visual Studio Code is recommended for creating and editing Python and YAML files.
5.  **Terminal/Command Line**: You will need a terminal to execute the `orchestrate` CLI commands for importing and managing your assets.

### Project Directory Structure
To keep the project organized, create the following folder structure in your working directory. This structure separates agents, tools, and knowledge base documents, making the project scalable and easy to manage.

```
nespresso_demo/
├── agents/
│   ├── 1_order_status_agent.yaml
│   ├── 2_coffee_advisor_agent.yaml
│   ├── 3_machine_support_agent.yaml
│   └── 4_nespresso_concierge_agent.yaml
├── tools/
│   ├── order_status_tool.py
│   ├── coffee_advisor_tool.py
│   └── machine_support_tool.py
├── knowledge_base/
│   ├── machine_manuals_kb.yaml
│   └── documents/
│       ├── vertuo_manual.txt
│       └── original_manual.txt
└── requirements.txt
```

## Step 1: Create the Knowledge Base
The knowledge base will provide the `Machine_Support_Agent` with detailed product information, enabling it to answer troubleshooting questions accurately. We will create a built-in knowledge base by uploading mock product manuals.

**Business Value**: This component directly reduces the need for human intervention in common troubleshooting scenarios. By providing instant, accurate solutions from official documentation, it improves first-contact resolution and enhances customer satisfaction.

### 1.1. Create Knowledge Base Documents
In the `nespresso_demo/knowledge_base/documents/` directory, create the following two text files.

**`vertuo_manual.txt`**
```text
Nespresso Vertuo Machine Troubleshooting Guide

Issue: Red and Yellow Blinking Light
Meaning: Descaling is needed.
Solution:
1. Empty the capsule container and drip tray.
2. Fill the water tank with one unit of Nespresso descaling liquid and 0.8 liters of water.
3. Turn the machine on and press the button and lever down for 3 seconds to enter descaling mode.
4. The light will blink orange. Press the lever down to start descaling.
5. Once the cycle is complete, rinse the water tank and refill with fresh water to run a rinse cycle.

Issue: No Coffee Flow
Meaning: Water tank is empty or a capsule is blocked.
Solution:
1. Ensure the water tank is filled with potable water.
2. Check that a new capsule is correctly inserted.
3. Eject the previous capsule if necessary.
4. Run a cleaning cycle by pressing the main button 3 times rapidly.
```

**`original_manual.txt`**
```text
Nespresso Original Line Machine Troubleshooting Guide

Issue: Light blinks irregularly.
Meaning: The machine has an air bubble.
Solution:
1. Fill the water tank.
2. Lift the coffee lever.
3. Push the Lungo button and let water run through until it flows normally.

Issue: Coffee is not hot enough.
Meaning: Machine needs pre-heating or descaling.
Solution:
1. Pre-heat the cup with hot water.
2. Run a water-only cycle before inserting a capsule to pre-heat the machine.
3. If the problem persists, perform a descaling cycle as per the machine's instructions.
```

### 1.2. Create the Knowledge Base YAML Configuration
In the `nespresso_demo/knowledge_base/` directory, create the file `machine_manuals_kb.yaml`.

```yaml
# nespresso_demo/knowledge_base/machine_manuals_kb.yaml
spec_version: v1
kind: knowledge_base 
name: nespresso_machine_manuals_kb
description: >
   Contains detailed troubleshooting guides, user manuals, and step-by-step solutions for common issues related to Nespresso Vertuo and Original line coffee machines. Use this to help customers resolve problems like blinking lights, coffee flow issues, and temperature problems.
documents:
   - "knowledge_base/documents/vertuo_manual.txt"
   - "knowledge_base/documents/original_manual.txt"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 2: Develop the Python Tools
Tools are the functional components that allow agents to perform actions. We will create three Python-based tools, each generating realistic synthetic data to simulate interactions with Nespresso's backend systems.

### 2.1. Order Status Tool
**Purpose**: This tool simulates fetching real-time order status from an e-commerce or ERP system. It provides customers with immediate updates on their coffee or accessory shipments, reducing "Where is my order?" (WISMO) inquiries.

**`nespresso_demo/tools/order_status_tool.py`**
```python
# nespresso_demo/tools/order_status_tool.py
import json
import random
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_order_status", description="Retrieves the real-time status of a Nespresso order using the order number.")
def get_order_status(order_number: str) -> str:
    """
    Retrieves the detailed status of a customer's order, including current status, estimated delivery date, and items included.

    Args:
        order_number (str): The unique identifier for the customer's order, for example, 'NPX987654

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
