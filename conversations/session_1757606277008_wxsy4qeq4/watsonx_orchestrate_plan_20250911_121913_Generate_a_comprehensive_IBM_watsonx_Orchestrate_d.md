# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-11 12:19:13
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Studio Member Concierge

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying an **AI-Powered Studio Member Concierge** using IBM watsonx Orchestrate. The plan is tailored to the client's specific business need to enhance customer service by automating responses to common member inquiries, thereby reducing the workload on human staff. The proposed solution leverages a multi-agent architecture where a supervisor agent intelligently routes requests to specialized collaborator agents. One agent will handle policy and program questions by querying a knowledge base of internal studio documents, while another will perform transactional account management tasks. This approach will deliver a 24/7 instant support channel, improve member satisfaction with consistent and accurate information, and free up staff to focus on higher-value activities like community engagement and sales, directly addressing the goal of a 30-50% reduction in manual support inquiries.

## 2. Prerequisites

Before beginning, ensure your environment is properly configured. This is crucial for the successful deployment of the agents and tools.

*   **IBM watsonx Orchestrate Account**: An active account with access to the watsonx Orchestrate platform.
*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed and configured. Follow the official documentation for installation:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Orchestrate CLI Authentication**: You must be logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```
*   **Python Environment**: A working Python environment (version 3.9 or later) is required to create the custom tools.
*   **Project Directory**: Create a dedicated project directory to organize all your files (YAML configurations, Python tools, knowledge base documents). A recommended structure is:
    ```
    studio_concierge_demo/
    ├── agents/
    │   ├── member_account_manager.yaml
    │   ├── studio_policy_expert.yaml
    │   └── studio_supervisor.yaml
    ├── tools/
    │   └── member_services.py
    ├── knowledge_base/
    │   ├── membership_policy.txt
    │   └── class_cancellation_policy.txt
    │   └── studio_kb.yaml
    └── requirements.txt
    ```

## 3. Step-by-Step Instructions

This plan is broken down into sequential steps, starting from data and knowledge creation, building tools, defining agents, and finally deploying and verifying the entire system.

### Step 1: Create the Knowledge Base and Source Documents

The foundation of the **Studio Policy Expert Agent** is a knowledge base containing the studio's official policies. We will create simple text files representing these policies and a YAML configuration to ingest them into a built-in Milvus knowledge base.

**Business Value**: This component directly addresses the need for instant, accurate answers to nuanced member questions about policies (e.g., "What is the guest pass policy?", "How do I freeze my membership?"). It ensures consistency and eliminates the need for staff to manually look up this information.

1.  **Create Source Document Files**: Inside the `knowledge_base/` directory, create the following text files with sample content.

    *   `knowledge_base/membership_policy.txt`:
        ```txt
        Membership Freeze Policy:
        Members with an active 'Unlimited' or 'Annual' membership can freeze their account for a minimum of 30 days and a maximum of 90 days per calendar year. A written request must be submitted 14 days in advance. A fee of $15 per month applies during the freeze period. 'Class Pack' memberships are not eligible for freezes.

        Guest Pass Policy:
        'Unlimited' and 'Annual' members receive 2 guest passes per month. Guest passes do not roll over. The guest must be a first-time visitor to the studio and be accompanied by the member. All guests must sign a liability waiver.
        ```
    *   `knowledge_base/class_cancellation_policy.txt`:
        ```txt
        Class Cancellation and No-Show Policy:
        To avoid losing a class credit or being charged a fee, members must cancel their class reservation at least 12 hours before the scheduled start time.
        - 'Class Pack' members who cancel late will forfeit the class credit.
        - 'Unlimited' and 'Annual' members who cancel late will be charged a $10 late cancellation fee.
        - No-shows for any membership type will result in a $20 no-show fee. Cancellations can be made through the mobile app or the studio website.
        ```

2.  **Create Knowledge Base YAML Configuration**: Create the `knowledge_base/studio_kb.yaml` file. This file tells Orchestrate to create a knowledge base named `studio_policy_kb`, ingest the specified documents, and use a default embedding model.

    ```yaml
    # knowledge_base/studio_kb.yaml
    spec_version: v1
    kind: knowledge_base
    name: studio_policy_kb
    description: >
      Contains comprehensive information about studio policies, including membership freezes, guest passes, class cancellations, and no-show fees. Use this to answer any member questions related to studio rules and procedures.
    documents:
      - "knowledge_base/membership_policy.txt"
      - "knowledge_base/class_cancellation_policy.txt"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

### Step 2: Create Transactional Tools for Account Management

The **Member Account Manager Agent** requires tools to perform actions on behalf of the user. We will create these tools in a single Python file. These tools will use realistic synthetic data to simulate interactions with a real member management system.

1.  **Create the Python Tool File**: In the `tools/` directory, create `member_services.py`.

    *   **`get_member_status` Tool**:
        **Business Value**: This tool allows the agent to retrieve real-time information about a member's account, such as their membership type and status. This is essential for answering questions like "Is my membership active?" or "What kind of plan do I have?" without human intervention.
        **Technical Implementation**: The function simulates a database lookup by searching a predefined list of member dictionaries. It takes a `member_name` as input and returns a JSON object with the member's details or an error message if the member is not found.

    *   **`update_member_contact_info` Tool**:
        **Business Value**: This tool empowers members to self-serve common administrative tasks like updating their phone number or email. This reduces the administrative burden on front-desk staff and provides a convenient, instant service for members.
        **Technical Implementation**: This function simulates updating a record in a database. It finds a member by name and updates their contact information based on the provided `phone_number` or `email`. It returns a success message confirming the update.

    *   **`get_class_schedule` Tool**:
        **Business Value**: This provides members with up-to-date information about class schedules, a very common inquiry. Automating this frees up staff from repeatedly answering the same questions and helps members plan their visits.
        **Technical Implementation**: The function simulates fetching data from a scheduling system. It takes an optional `day_of_week` parameter to filter the schedule and returns a structured list of available classes, including time, instructor, and capacity.

    *   **Complete Code for `tools/member_services.py`**:
        ```python
        # tools/member_services.py
        import json
        from datetime import datetime
        from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission
        from typing import Optional, List, Dict, Any

        # --- Synthetic Data Generation ---
        # This simulates a backend member database.
        MOCK_MEMBERS_DB = [
            {
                "member_id": "M1001",
                "name": "Alice Johnson",
                "membership_type": "Unlimited",
                "status": "Active",
                "join_date": "2023-01-15",
                "email": "alice.j@example.com",
                "phone_number": "555-0101"
            },
            {
                "member_id": "M1002",
                "name": "Bob Williams",
                "membership_type": "Class Pack",
                "status": "Active",
                "remaining_classes": 8,
                "join_date": "2023-03-22",
                "email": "bob.w@example.com",
                "phone_number": "555-0102"
            },
            {
                "member_id": "M1003",
                "name": "Charlie Brown",
                "membership_type": "Annual",
                "status": "Frozen",
                "join_date": "2022-11-10",
                "email": "charlie.b@example.com",
                "phone_number": "555-0103"
            }
        ]

        # This simulates a backend class schedule system.
        MOCK_SCHEDULE_DB = [
            {"day": "Monday", "time": "6:00 AM", "class_name": "Sunrise Yoga", "instructor": "Anna", "capacity": 15, "booked": 10},
            {"day": "Monday", "time": "5:30 PM", "class_name": "HIIT Circuit", "instructor": "David", "capacity": 20, "booked": 20},
            {"day": "Tuesday", "time": "12:00 PM", "class_name": "Lunchtime Express", "instructor": "Chloe", "capacity": 15, "booked": 5},
            {"day": "Wednesday", "time": "6:00 AM", "class_name": "Sunrise Yoga", "instructor": "Anna", "capacity": 15, "booked": 12},
            {"day": "Wednesday", "time": "6:30 PM", "class_name": "Power Pilates", "instructor": "Maria", "capacity": 18, "booked": 15},
            {"day": "Friday", "time": "5:30 PM", "class_name": "Restorative Flow", "instructor": "Anna", "capacity": 25, "booked": 22},
        ]

        @tool(name="get_member_status", permission=ToolPermission.ADMIN)
        def get_member_status(member_name: str) -> str:
            """
            Retrieves the current status and details of a studio member by their full name.

            Args:
                member_name (str): The full name of the member to look up. Case-insensitive.

            Returns:
                str: A JSON string containing the member's details if found, otherwise an error message.
            """
            print(f"Searching for member: {member_name}")
            for member in MOCK_MEMBERS_DB:
                if member["name"].lower() == member_name.lower():
                    return json.dumps(member)
            return json.dumps({"error": "Member not found. Please check the name and try again."})

        @tool(name="update_member_contact_info", permission=ToolPermission.ADMIN)
        def update_member_contact_info(member_name: str, email: Optional[str] = None, phone_number: Optional[str] = None) -> str:
            """
            Updates a member's contact information (email or phone number) in the system.

            Args:
                member_name (str): The full name of the member whose information needs to be updated.
                email (Optional

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
