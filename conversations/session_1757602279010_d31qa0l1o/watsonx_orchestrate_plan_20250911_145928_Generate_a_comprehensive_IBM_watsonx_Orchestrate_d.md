# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-11 14:59:28
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: CorePower AI Wellness Concierge

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **CorePower AI Wellness Concierge**, a sophisticated multi-agent solution using IBM watsonx Orchestrate. This plan is tailored specifically to CorePower's goal of creating an AI Wellness Advisor. The solution will enhance the member experience by providing instant, 24/7 answers to inquiries, improve operational efficiency by automating routine tasks, and ensure brand consistency by grounding responses in official CorePower documentation.

The architecture leverages a powerful **supervisor agent pattern**. The primary `Member_Concierge_Agent` intelligently analyzes member requests and routes them to one of two specialized collaborator agents: the `Wellness_Advisor_Agent`, which uses a knowledge base for conversational Q&A on wellness topics, and the `Class_Scheduler_Agent`, which uses custom Python tools to handle transactional requests like checking class schedules and member details. This modular design demonstrates a scalable and robust AI system capable of handling diverse and complex user interactions.

## Prerequisites

Before beginning, ensure your environment is properly configured. This is essential for a smooth development and deployment process.

1.  **Python Environment**: An installation of Python 3.10 or higher is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If you haven't installed it, run the following command:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate Environment**: You must have an active watsonx Orchestrate environment configured. This involves initializing the ADK and logging in. If this is your first time, follow the official documentation to run `orchestrate login` and `orchestrate env create`.
4.  **Project Directory Structure**: To organize all assets for this demo, create the following directory structure in your local development environment:

    ```
    corepower_demo/
    ├── agents/
    │   ├── member_concierge_agent.yaml
    │   ├── wellness_advisor_agent.yaml
    │   └── class_scheduler_agent.yaml
    ├── tools/
    │   └── corepower_tools.py
    ├── knowledge_base/
    │   └── corepower_kb.yaml
    ├── mock_data/
    │   ├── Class_Descriptions.pdf
    │   ├── Wellness_and_Nutrition_Guide.pdf
    │   ├── Membership_FAQs.txt
    │   ├── class_schedule.json
    │   └── member_profiles.json
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Project Files

The foundation of this demo is realistic, domain-specific data that simulates CorePower's operational environment. We will create the necessary data files that our knowledge base and tools will use.

1.  **Create Mock Knowledge Base Documents**:
    *   Create two PDF files, `Class_Descriptions.pdf` and `Wellness_and_Nutrition_Guide.pdf`, with relevant content about CorePower's offerings.
    *   In the `mock_data/` directory, create `Membership_FAQs.txt` with the following content:

    ```txt
    # mock_data/Membership_FAQs.txt

    Q: What is the All Access membership?
    A: The All Access membership grants you unlimited access to all CorePower Yoga studios nationwide, including all class formats and online content.

    Q: How do I freeze my membership?
    A: You can freeze your membership for up to 90 days by contacting our support team through the member portal. A small monthly freeze fee applies.

    Q: What is the cancellation policy?
    A: We require a 30-day written notice for all membership cancellations. Please submit your request via the online member portal to ensure it is processed correctly.
    ```

2.  **Create Mock JSON Data for Tools**:
    *   In the `mock_data/` directory, create `class_schedule.json`:

    ```json
    // mock_data/class_schedule.json
    [
      {"class_id": "YS101", "class_name": "Yoga Sculpt", "studio": "Downtown", "instructor": "Alex Ray", "start_time": "2024-10-28T18:00:00Z", "duration_minutes": 60, "day": "tomorrow"},
      {"class_id": "C2-102", "class_name": "C2 CorePower Yoga", "studio": "Downtown", "instructor": "Maria Garcia", "start_time": "2024-10-28T09:00:00Z", "duration_minutes": 60, "day": "tomorrow"},
      {"class_id": "HPF-103", "class_name": "Hot Power Fusion", "studio": "Northside", "instructor": "Sam Chen", "start_time": "2024-10-27T19:00:00Z", "duration_minutes": 75, "day": "today"},
      {"class_id": "C2-104", "class_name": "C2 CorePower Yoga", "studio": "Northside", "instructor": "Emily White", "start_time": "2024-10-27T17:30:00Z", "duration_minutes": 60, "day": "today"}
    ]
    ```

    *   In the `mock_data/` directory, create `member_profiles.json`:

    ```json
    // mock_data/member_profiles.json
    [
      {"member_id": "CP7890", "name": "Jane Doe", "membership_level": "All Access", "join_date": "2023-01-15", "next_billing_date": "2024-11-01"},
      {"member_id": "CP1234", "name": "John Smith", "membership_level": "Studio Pass", "join_date": "2024-03-20", "next_billing_date": "2024-11-20"}
    ]
    ```

3.  **Create the `requirements.txt` file**:
    *   This file lists the Python dependencies for our tools. In this case, we only need the `requests` library for demonstrating a common pattern, though our local implementation doesn't strictly require it.

    ```txt
    # requirements.txt
    requests
    ```

## Step 2: Create the Knowledge Base Configuration

The `Wellness_Advisor_Agent` will use a knowledge base to provide accurate, brand-consistent answers. This is achieved through Retrieval-Augmented Generation (RAG), where the agent retrieves information from CorePower's documents before generating a response.

Create the file `knowledge_base/corepower_kb.yaml` with the following configuration. This file defines a built-in Milvus knowledge base that will ingest the documents we created.

```yaml
# knowledge_base/corepower_kb.yaml

spec_version: v1
kind: knowledge_base
name: corepower_wellness_kb
description: >
  Contains official CorePower documents covering class descriptions, wellness and nutrition guides, and frequently asked questions about memberships. Use this to answer any general questions about CorePower's offerings and policies.
documents:
  - "./mock_data/Class_Descriptions.pdf"
  - "./mock_data/Wellness_and_Nutrition_Guide.pdf"
  - "./mock_data/Membership_FAQs.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2 # Using the default watsonx.ai model
```

## Step 3: Create the Custom Python Tools

The `Class_Scheduler_Agent` requires tools to perform specific, transactional tasks. We will create two Python functions decorated with `@tool`, which allows watsonx Orchestrate to recognize and use them.

Create the file `tools/corepower_tools.py` and add the following Python code.

### Tool 1: `get_class_schedule`

**Business Value:** This tool automates the process of retrieving class schedules, a common member inquiry. By providing instant, accurate schedule information, it enhances the member experience and reduces the repetitive workload on studio staff, allowing them to focus on in-person interactions and higher-value activities.

**Technical Implementation:** The tool accepts a studio location and a day as input. For this demo, it reads from a local `class_schedule.json` file and filters the results to find matching classes. In a production environment, this function would be modified to make a secure API call to CorePower's backend scheduling system.

### Tool 2: `get_member_details`

**Business Value:** This tool provides a secure way to look up member-specific information, such as membership level and join date. This capability is foundational for building more personalized AI interactions, such as offering tailored promotions or proactively addressing billing questions, thereby increasing member satisfaction and loyalty.

**Technical Implementation:** The tool takes a unique `member_id` as input to ensure data privacy. It queries the `member_profiles.json` file to find the corresponding member's record. This simulates a secure lookup in a CRM or member management system via an authenticated API call.

```python
# tools/corepower_tools.py

import json
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_class_schedule", permission=ToolPermission.ADMIN)
def get_class_schedule(studio_location: str, day: str) -> list[dict]:
    """
    Retrieves the class schedule for a specific CorePower studio location and a given day.

    Args:
        studio_location (str): The CorePower studio location to search for (e.g., "Downtown", "Northside").
        day (str): The desired day for the schedule. Can be "today" or "tomorrow".

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a class with its name, instructor, and start time. Returns an empty list if no classes are found.
    """
    try:
        with open('mock_data/class_schedule.json', 'r') as f:
            all_classes = json.load(f)

        # Simple filter logic based on studio and day
        # In a real scenario, this would involve more complex date handling
        filtered_classes = [
            cls for cls in all_classes
            if cls['studio'].lower() == studio_location.lower() and cls['day'].lower() == day.lower()
        ]
        
        if not filtered_classes:
            return [{"status": "No classes found for the specified criteria."}]
            
        return filtered_classes
    except FileNotFoundError:
        return [{"error": "Schedule data file not found."}]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {str(e)}"}]


@tool(name="get_member_details", permission=ToolPermission.ADMIN)
def get_member_details(member_id: str) -> dict:
    """
    Retrieves detailed information for a specific member using their unique member ID.

    Args:
        member_id (str): The unique identifier for the member (e.g., "CP7890").

    Returns:
        dict: A dictionary containing the member's details, including name, membership level, and join date. Returns an error message if the member is not found.
    """
    try:
        with open('mock_data/member_profiles.json', 'r') as f:
            all_members = json.load(f)

        member_details = next((member for member in all_members if member['member_id'] == member_id), None)

        if member_details:
            return member_details
        else:
            return {"error": f"Member with ID '{member_id}' not found."}
    except FileNotFoundError:
        return {"error": "Member profiles data file not found."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

```

## Step 4: Create the Agent YAML Configurations

With the knowledge base and tools defined, we can now configure our three agents. Each agent is defined in a separate YAML file, specifying its name, description, instructions, and relationship to other components.

1.  **`Wellness_Advisor_Agent` (Collaborator)**: This agent is a specialist in answering questions using the `corepower_wellness_kb`.

    ```yaml
    # agents/wellness_advisor_agent.yaml

    spec_version: v1
    kind: native
    name: Wellness_Advisor_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert agent that answers member questions about CorePower's class types, wellness benefits, nutrition, and membership policies by consulting the official company knowledge base.
    instructions: >
      Your sole purpose is to answer user questions based on the information contained in the corepower_wellness_kb.
      Do not answer questions outside of this scope. If the knowledge base does not contain the answer, state that you do not have that information.
      Always provide comprehensive and helpful answers grounded in the provided documents.
    tools: []
    collaborators: []
    knowledge_base:
      - corepower_wellness_kb
    ```

2.  **`Class_Scheduler_Agent` (Collaborator)**: This agent is a specialist in handling transactional requests using its custom tools.

    ```yaml
    # agents/class_scheduler_agent.yaml

    spec_version: v1
    kind: native
    name: Class_Scheduler_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A transactional agent that handles specific tasks related to class schedules and member accounts. It can look up class times for specific studios and retrieve member profile details.
    instructions: >
      Your purpose is to execute specific tasks using your available tools.
      - Use the get_class_schedule tool when a user asks for the class schedule for a specific location and day.
      - Use the get_member_details tool when a user provides a member ID and asks for their account information.
      - If the user's request cannot be fulfilled by one of your tools, state that you cannot perform that action.
    tools:
      - get_class_schedule
      - get_member_details
    collaborators: []
    ```

3.  **`Member_Concierge_Agent` (Supervisor)**: This is the primary, user-facing agent. Its main role is to understand the user's intent and delegate the task to the correct collaborator.

    ```yaml
    # agents/member_concierge_agent.yaml

    spec_version: v1
    kind: native
    name: Member_Concierge_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A helpful AI concierge for CorePower members. It acts as the primary point of contact, understanding member inquiries and routing them to the appropriate specialist agent for resolution. It can handle questions about wellness, classes, schedules, and member accounts.
    instructions: >
      You are the main AI assistant for CorePower members. Your primary role is to understand the user's intent and delegate the task to the correct specialist agent.
      
      Reasoning:
      - If the user asks a general, knowledge-based question about wellness, the benefits of a class, nutrition advice, or membership policies, use the Wellness_Advisor_Agent.
      - If the user asks for a specific, transactional piece of information like a class time, a schedule for a studio, or details about their account, use the Class_Scheduler_Agent.
      - For complex requests that have multiple parts, break down the request and use the appropriate agent for each part.
    collaborators:
      - Wellness_Advisor_Agent
      - Class_Scheduler_Agent
    tools: []
    ```

## Step 5: Deployment and Import Sequence

Now we will use the ADK's command-line interface (CLI) to import all our created assets into watsonx Orchestrate. The order of operations is crucial: dependencies like knowledge bases and tools must be imported before the agents that use them.

Open your terminal, navigate to the root `corepower_demo/` directory, and run the following commands in sequence:

1.  **Import the Knowledge Base**:
    ```bash
    orchestrate knowledge-bases import -f knowledge_base/corepower_kb.yaml
    ```

2.  **Import the Custom Tools**:
    ```bash
    orchestrate tools import -f tools/corepower_tools.py
    ```

3.  **Import the Collaborator Agents**:
    ```bash
    orchestrate agents import -f agents/wellness_advisor_agent.yaml
    orchestrate agents import -f agents/class_scheduler_agent.yaml
    ```

4.  **Import the Supervisor Agent**:
    ```bash
    orchestrate agents import -f agents/member_concierge_agent.yaml
    ```

## Step 6: Verification and Testing

With all components deployed, you can now interact with the `Member_Concierge_Agent` to test the full solution. The supervisor agent will handle the routing logic based on your prompts.

1.  **Start the Chat Interface**: Launch the interactive chat, specifying the supervisor agent as the entry point.
    ```bash
    orchestrate chat start --agent Member_Concierge_Agent
    ```

2.  **Execute Demo Scenarios**: Test the system using the predefined scenarios from the demo concept.

    *   **Scenario 1 (Knowledge Base Query)**: Test the `Wellness_Advisor_Agent`.
        *   **User Prompt**: `What are the benefits of Yoga Sculpt and what should I bring to my first class?`
        *   **Expected Outcome**: The `Member_Concierge_Agent` should route this to the `Wellness_Advisor_Agent`. The response will be a comprehensive, conversational answer generated from the content in your mock PDF documents.

    *   **Scenario 2 (Tool-Based Query)**: Test the `Class_Scheduler_Agent`.
        *   **User Prompt**: `Show me the schedule for the Downtown studio tomorrow.`
        *   **Expected Outcome**: The `Member_Concierge_Agent` should route this to the `Class_Scheduler_Agent`. The agent will invoke the `get_class_schedule` tool, which will read the `class_schedule.json` file and return a formatted list of the two matching classes for the Downtown studio.

    *   **Scenario 3 (Complex, Multi-Step Reasoning)**: Test the supervisor's ability to handle complex queries.
        *   **User Prompt**: `I'm new to yoga. Can you recommend a good class for beginners and then tell me when it's offered at the Northside studio today?`
        *   **Expected Outcome**: This demonstrates the power of the supervisor. It should first route the recommendation part to the `Wellness_Advisor_Agent` (which might suggest 'C2 CorePower Yoga' based on the knowledge base). Then, it should route the scheduling part to the `Class_Scheduler_Agent` to look up the 'C2' schedule at the 'Northside' studio, returning the specific class time.

## Troubleshooting

If you encounter issues, here are some common problems and their solutions:

*   **`ImportError` or `ModuleNotFoundError`**: This usually means a required Python package is missing. Ensure you have created and installed the dependencies from `requirements.txt` (`pip install -r requirements.txt`).
*   **`FileNotFoundError` during Tool Execution**: The Python tool cannot find the mock data files (`.json`). Verify that you are running the `orchestrate chat start` command from the root `corepower_demo/` directory and that the file paths in the Python code are correct relative to that directory.
*   **Agent Routing Incorrectly**: If the supervisor agent sends a request to the wrong collaborator, review the `description` and `instructions` in all three agent YAML files. The supervisor heavily relies on the collaborator descriptions to make routing decisions. Ensure they are distinct and accurately reflect each agent's capabilities.
*   **Knowledge Base Not Returning Answers**: After importing the knowledge base, it may take a few minutes to ingest and index the documents. If it's not working, use `orchestrate knowledge-bases get --name corepower_wellness_kb` to check its status. Ensure the status is `Ready`.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
