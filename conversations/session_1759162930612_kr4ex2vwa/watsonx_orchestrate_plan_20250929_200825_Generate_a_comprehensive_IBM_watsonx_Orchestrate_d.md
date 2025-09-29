# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-29 20:08:25
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Starbucks Partner Pro Assistant

## Overview
This execution plan details the creation of the "Starbucks Partner Pro," an AI-powered onboarding and operations assistant, using IBM watsonx Orchestrate. This solution is designed specifically for Starbucks to address the challenges of rapidly training new baristas ("partners"), ensuring operational consistency, and providing immediate access to critical information. The Partner Pro will function as a multi-agent system on in-store tablets, accelerating new hire proficiency by an estimated 30-50%. It achieves this by creating a supervisor agent that intelligently routes partner queries to specialized collaborator agents—one for drink recipes and inventory, and another for company policies—delivering a seamless, conversational experience that boosts confidence and reduces errors from day one.

## Prerequisites
Before beginning, ensure your development environment is correctly configured. This involves installing the necessary software and authenticating with IBM watsonx Orchestrate.

1.  **Python Environment**: An active Python environment (version 3.10 or later) is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If not already installed, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment Configuration**: You must have an active watsonx Orchestrate environment configured. This is typically done via the `orchestrate env add` command, which connects your local ADK to your Orchestrate tenant.
4.  **Project Directory Structure**: Create a dedicated folder for the project with a clear structure to organize agents, tools, and data.
    ```bash
    mkdir starbucks-partner-pro
    cd starbucks-partner-pro
    mkdir agents tools knowledge_base_docs data
    ```

## Step 1: Create Mock Data and Knowledge Base Documents
To simulate a realistic environment, we will create mock data sources that our agents and tools will use. This includes a JSON file for drink recipes and text files for the policy knowledge base.

1.  **Create Mock Knowledge Base Documents**: Inside the `knowledge_base_docs` directory, create the following text files with sample content.

    *   `knowledge_base_docs/Barista_Basics_Handbook.txt`:
        ```text
        Barista Basics Handbook - Chapter 1: Customer Connection
        The Starbucks Experience is built on creating a personal connection with every customer. Always greet customers with a smile. Use the "LATTE" model for service recovery: Listen, Apologize, Take action, Thank, and Ensure satisfaction.

        Chapter 2: Dress Code
        Partners must wear a black, white, or gray polo shirt or a Starbucks-branded t-shirt. Dark-wash jeans or black pants are acceptable. Shoes must be non-slip and closed-toe.
        ```
    *   `knowledge_base_docs/Health_and_Safety_Manual.txt`:
        ```text
        Health and Safety Manual - Section A: Food Safety
        All partners must wash their hands for at least 20 seconds before starting work, after handling cash, and after breaks. Milk steaming wands must be purged and wiped after every use. The "danger zone" for food is between 40°F and 140°F (4°C and 60°C).

        Section B: Incident Reporting
        Any on-the-job injury, no matter how minor, must be reported to the shift supervisor immediately. An incident report form must be completed within 24 hours.
        ```

2.  **Create Mock Recipe Database**: Inside the `data` directory, create a JSON file named `drink_recipes.json`. This file will serve as our recipe database.

    *   `data/drink_recipes.json`:
        ```json
        [
          {
            "name": "Caramel Macchiato",
            "size": "Grande",
            "ingredients": [
              {"name": "Vanilla Syrup", "quantity": "3 pumps"},
              {"name": "2% Milk", "quantity": "to third line"},
              {"name": "Espresso", "quantity": "2 shots"},
              {"name": "Caramel Drizzle", "quantity": "cross-hatch pattern"}
            ],
            "steps": [
              "Pump Vanilla Syrup into the cup.",
              "Steam 2% milk.",
              "Pour steamed milk into the cup.",
              "Queue and pour 2 espresso shots over the top of the milk.",
              "Top with Caramel Drizzle in a double-circle, cross-hatch pattern."
            ]
          },
          {
            "name": "Pike Place Roast",
            "size": "Grande",
            "ingredients": [
              {"name": "Pike Place Roast Coffee Beans", "quantity": "ground for filter"},
              {"name": "Filtered Water", "quantity": "to line"}
            ],
            "steps": [
              "Ensure the coffee brewer is clean.",
              "Place a filter in the brew basket.",
              "Add the correct amount of ground Pike Place Roast coffee.",
              "Slide the brew basket into the brewer and start the brew cycle.",
              "Serve fresh. Coffee expires after 30 minutes."
            ]
          }
        ]
        ```

## Step 2: Implement the Knowledge Base
The `Policy_Guide_Agent` will use a knowledge base to answer questions from the mock documents. We define this using a YAML configuration file.

*   **Business Value**: This component provides a single source of truth for all company policies, ensuring partners receive consistent, accurate, and compliant information regarding operations, safety, and HR procedures. This reduces reliance on human trainers for simple policy questions and minimizes the risk of misinformation.

1.  **Create the Knowledge Base Configuration File**: In the root directory, create `policy_kb.yaml`.

    *   `policy_kb.yaml`:
        ```yaml
        spec_version: v1
        kind: knowledge_base 
        name: starbucks_policy_kb
        description: >
           Contains official Starbucks documentation for partner onboarding, operational procedures, health and safety guidelines, and HR policies. Use this to answer any questions about company rules or standard operating procedures.
        documents:
           - "knowledge_base_docs/Barista_Basics_Handbook.txt"
           - "knowledge_base_docs/Health_and_Safety_Manual.txt"
        vector_index:
           embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
        ```

## Step 3: Implement Custom Python Tools
The `Recipe_Expert_Agent` requires custom tools to fetch recipes and check inventory. We will implement these as Python functions decorated with `@tool`.

1.  **Create the `requirements.txt` file**: In the project root, create a `requirements.txt` file. For this demo, no external libraries are needed beyond the ADK itself, but it's good practice to have the file.
    ```text
    # requirements.txt

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
