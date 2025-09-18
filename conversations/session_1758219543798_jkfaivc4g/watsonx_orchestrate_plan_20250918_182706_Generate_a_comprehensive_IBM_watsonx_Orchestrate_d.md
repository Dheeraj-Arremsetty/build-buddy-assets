# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 18:27:06
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: CorePower Yoga AI Member Concierge

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "CorePower Yoga AI Member Concierge" using IBM watsonx Orchestrate. This solution is specifically tailored to address CorePower Yoga's business need to enhance member support by providing a 24/7, AI-powered virtual assistant. The plan implements a sophisticated multi-agent architecture, featuring a central supervisor agent that intelligently routes member inquiries to specialized collaborator agents. This approach will automate responses to common queries, streamline account management tasks, and simplify class scheduling, thereby improving operational efficiency, elevating the member experience, and increasing engagement.

The architecture consists of four main agents:
1.  **CorePower_Member_Concierge (Supervisor):** The user-facing conversational AI that understands intent and delegates tasks.
2.  **Membership_Policy_Agent:** A knowledge worker that answers policy questions using a document-based knowledge base.
3.  **Account_Management_Agent:** A transactional agent that executes member account changes using custom tools.
4.  **Class_Scheduler_Agent:** A service agent that finds and books classes by interacting with a scheduling system (simulated via tools).

This plan will guide you through creating the project structure, generating mock data, developing the necessary knowledge bases and tools, defining each agent's behavior, and deploying the entire system using the IBM watsonx Orchestrate Agent Development Kit (ADK).

## Prerequisites
Before you begin, ensure your development environment is set up with the following components. This setup is essential for building, deploying, and testing the agents and tools outlined in this plan.

*   **IBM watsonx Orchestrate ADK:** The Agent Development Kit must be installed and configured. This includes the Python library and the `orchestrate` CLI. If you haven't installed it, follow the official documentation:
    ```bash
    pip install ibm-watsonx-orchestrate
    ```
*   **Python Environment:** A working Python environment (version 3.10 or higher) is required to create the custom tools.
*   **Orchestrate Environment Initialization:** You must have an active IBM watsonx Orchestrate environment initialized. Run the following command and follow the prompts to log in:
    ```bash
    orchestrate login
    ```
*   **Text Editor or IDE:** A code editor such as Visual Studio Code is recommended for creating and editing YAML, Python, and other text files.

## Step 1: Project Setup and Mock Data Creation
A well-organized project structure is crucial for managing the various components of the solution. This step involves creating the necessary folders and the synthetic data files that will power the demo.

First, create a main project directory and the required subdirectories.

```bash
mkdir corepower-yoga-demo
cd corepower-yoga-demo
mkdir agents tools mock_data
```

Next, create the mock data files inside the `mock_data` directory.

1.  **`mock_data/Cancellation_Policy.txt`**: A plain text file outlining the membership cancellation policy.
    ```text
    CorePower Yoga Cancellation Policy

    To cancel your All Access Membership, you must provide written notice at least 14 days before your next billing date. Cancellations can be submitted through your online account portal or by contacting member support directly.

    For On Demand subscriptions, you can cancel anytime, and your access will continue until the end of the current billing period. No refunds are provided for partial months.

    There are no cancellation fees. If you freeze your membership, your billing will resume automatically at the end of the freeze period unless you cancel.
    ```

2.  **`mock_data/Membership_Tiers.txt`**: A text file describing membership options. (Using .txt for simplicity, though the plan mentions PDF. Orchestrate ingests both).
    ```text
    CorePower Yoga Membership Tiers

    1. All Access Membership:
    - Unlimited access to all in-studio classes nationwide.
    - Includes access to our full CorePower Yoga On Demand library.
    - Special discounts on retail and workshops.
    - Ability to bring one guest per month for free.

    2. On Demand Membership:
    - Unlimited access to our online library of classes.
    - Stream anytime, anywhere.
    - Does not include access to in-studio classes.
    ```

3.  **`mock_data/members.json`**: A JSON file acting as a simple member database.
    ```json
    [
      {
        "member_id": "CPY-1001",
        "name": "Alex Johnson",
        "membership_status": "Active",
        "billing_date": "2024-09-15",
        "plan_type": "All Access"
      },
      {
        "member_id": "CPY-2035",
        "name": "Maria Garcia",
        "membership_status": "Active",
        "billing_date": "2024-09-22",
        "plan_type": "On Demand"
      },
      {
        "member_id": "CPY-4778",
        "name": "David Chen",
        "membership_status": "Frozen",
        "billing_date": "2024-12-05",
        "plan_type": "All Access"
      }
    ]
    ```

## Step 2: Create the Knowledge Base
The `Membership_Policy_Agent` will use a knowledge base to answer factual questions. This component ingests the documents you created and makes them searchable.

Create a file named `corepower_kb.yaml` in the root of your project directory (`corepower-yoga-demo`).

**`corepower_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: corepower_faq_kb
description: >
  Contains official information on CorePower Yoga's membership policies, class types, cancellation rules, guest policies, and On Demand platform FAQs. Use this to answer any member questions about rules and benefits.
documents:
  - "./mock_data/Membership_Tiers.txt"
  - "./mock_data/Cancellation_Policy.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 3: Develop the Custom Python Tools
The `Account_Management_Agent` and `Class_Scheduler_Agent` require custom tools to perform actions. These are Python functions decorated with `@tool` that interact with our mock data.

1.  **Create `requirements.txt`**: In the project root, create this file. For this demo, no external libraries are needed beyond the ADK itself, but it's good practice.
    ```text
    # No external packages required for these tools
    ```

2.  **Create Account Management Tools**: Create a file named `account_tools.py` inside the `tools` directory.
    
    **`tools/account_tools.py`**
    ```python
    import json
    from datetime import datetime, timedelta
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    MEMBER_DB_PATH = './mock_data/members.json'

    def _read_db():
        """Helper function to read the member database."""
        try:
            with open(MEMBER_DB_PATH, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_db(data):
        """Helper function to write to the member database."""
        with open(MEMBER_DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    @tool(permission=ToolPermission.ADMIN)
    def freeze_membership(member_id: str, duration_months: int) -> dict:
        """
        Freezes a member's account for a specified number of months. Use this tool when a member explicitly asks to pause or freeze their membership.

        Args:
            member_id (str): The unique identifier for the member, like 'CPY-1001'.
            duration_months (int): The number of months to freeze the membership for.

        Returns:
            dict: A confirmation message with the new status and the resume date.
        """
        members = _read_db()
        member_found = False
        for member in members:
            if member['member_id'] == member_id:
                member['membership_status'] = 'Frozen'
                # Calculate resume date for confirmation
                resume_date = datetime.now() + timedelta(days=30 * duration_months)
                member['billing_date'] = resume_date.strftime('%Y-%m-%d')
                member_found = True
                break
        
        if not member_found:
            return {"status": "error", "message": f"Member with ID {member_id} not found."}

        _write_db(members)
        return {
            "status": "success",
            "message": f"Membership for {member_id} has been successfully frozen for {duration_months} months. Billing will resume on {member['billing_date']}."
        }

    @tool(permission=ToolPermission.ADMIN)
    def get_billing_info(member_id: str) -> dict:
        """
        Retrieves the next billing date and plan type for a specific member. Use this when a member asks about their billing cycle or plan details.

        Args:
            member_id (str): The unique identifier for the member, like 'CPY-1001'.

        Returns:
            dict: The member's billing information or an error message if not found.
        """
        members = _read_db()
        for member in members:
            if member['member_id'] == member_id:
                return {
                    "status": "success",
                    "member_id": member['member_id'],
                    "plan_type": member['plan_type'],
                    "next_billing_date": member['billing_date'],
                    "membership_status": member['membership_status']
                }
        return {"status": "error", "message": f"Member with ID {member_id} not found."}

    ```

3.  **Create Class Scheduler Tools**: Create a file named `scheduler_tools.py` inside the `tools` directory.
    
    **`tools/scheduler_tools.py`**
    ```python
    from datetime import datetime
    from typing import List
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    # Mock class schedule data
    mock_schedule = [
        {"class_id": "C2-0900-DEN", "class_name": "C2 - CorePower 2", "instructor": "Jenna", "time": "09:00", "location": "Denver", "spots_available": 5},
        {"class_id": "YS-1200-DEN", "class_name": "YS - Yoga Sculpt", "instructor": "Mike", "time": "12:00", "location": "Denver", "spots_available": 10},
        {"class_id": "C2-1730-DEN", "class_name": "C2 - CorePower 2", "instructor": "Chloe", "time": "17:30", "location": "Denver", "spots_available": 3},
        {"class_id": "HPF-1800-DEN", "class_name": "HPF - Hot Power Fusion", "instructor": "Sam", "time": "18:00", "location": "Denver", "spots_available": 8},
        {"class_id": "C2-1900-BOUL", "class_name": "C2 - CorePower 2", "instructor": "Leo", "time": "19:00", "location": "Boulder", "spots_available": 0},
    ]

    @tool(permission=ToolPermission.ADMIN)
    def get_class_schedule(location: str, class_type: str = None, after_time: str = None) -> List[dict]:
        """
        Searches for available yoga classes based on location, class type, and time. Use this as the first step when a member wants to find a class.

        Args:
            location (str): The city to search for classes in (e.g., 'Denver').
            class_type (str, optional): The type of class to filter by (e.g., 'C2', 'Yoga Sculpt'). Defaults to None.
            after_time (str, optional): The earliest time for the class, in 'HH:MM' format (e.g., '17:00'). Defaults to None.

        Returns:
            List[dict]: A list of available classes matching the criteria.
        """
        results = []
        for cls in mock_schedule:
            loc_match = location.lower() in cls['location'].lower()
            type_match = not class_type or class_type.lower() in cls['class_name'].lower()
            time_match = not after_time or cls['time'] >= after_time
            
            if loc_match and type_match and time_match and cls['spots_available'] > 0:
                results.append(cls)
        return results

    @tool(permission=ToolPermission.ADMIN)
    def book_class(member_id: str, class_id: str) -> dict:
        """
        Books a member into a specific class using the class ID. Use this tool after the member has selected a class from the schedule.

        Args:
            member_id (str): The unique identifier for the member, e.g., 'CPY-1001'.
            class_id (str): The unique identifier for the class, e.g., 'C2-1730-DEN'.

        Returns:
            dict: A confirmation of the booking or an error message.
        """
        for cls in mock_schedule:
            if cls['class_id'] == class_id:
                if cls['spots_available'] > 0:
                    # In a real scenario, you would decrement the spot count here.
                    return {
                        "status": "success",
                        "message": f"Booking confirmed for member {member_id} in class {cls['class_name']} with {cls['instructor']} at {cls['time']}."
                    }
                else:
                    return {"status": "error", "message": f"Sorry, class {class_id} is full."}
        return {"status": "error", "message": f"Class with ID {class_id} not found."}

    ```

## Step 4: Create the Agent Definitions (YAML)
Now, define the behavior, tools, and collaborators for each agent in separate YAML files within the `agents` directory.

1.  **`agents/membership_policy_agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: Membership_Policy_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      An expert on all CorePower Yoga policies. It answers member questions about membership tiers, cancellation rules, guest policies, and On Demand features by consulting its knowledge base.
    instructions: >
      You are an AI assistant specializing in CorePower Yoga's official policies.
      Your primary function is to provide accurate, helpful answers based ONLY on the information contained in your knowledge base.
      When a user asks a question about policies, benefits, or rules, use the knowledge base to find the answer and present it clearly.
      Do not answer questions outside of this scope.
    tools: []
    collaborators: []
    knowledge_base:
      - corepower_faq_kb
    ```

2.  **`agents/account_management_agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: Account_Management_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      Handles transactional requests related to a member's personal account. It can freeze memberships and retrieve billing information using its specialized tools.
    instructions: >
      You are an AI assistant for managing CorePower Yoga member accounts.
      - Use the `freeze_membership` tool when a user explicitly asks to pause or freeze their account. You must have the member_id and the duration in months.
      - Use the `get_billing_info` tool when a user asks about their next payment, billing date, or current plan details. You must have the member_id.
      - Always confirm actions with the user and clearly state the result from the tool.
    tools:
      - freeze_membership
      - get_billing_info
    collaborators: []
    ```

3.  **`agents/class_scheduler_agent.yaml`**
    ```yaml
    spec_version: v1
    kind: native
    name: Class_Scheduler_Agent
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      Manages all tasks related to finding and booking yoga classes. It uses tools to search the class schedule and make bookings on behalf of a member.
    instructions: >
      You are an AI assistant that helps CorePower Yoga members book classes.
      Your process is a two-step flow:
      1. First, always use the `get_class_schedule` tool to find available classes based on the user's request (location, time, class type). Present the findings to the user.
      2. After the user confirms which class they want, use the `book_class` tool with the member_id and the correct class_id from the search results to finalize the booking.
      - Do not attempt to book a class without first finding options.
    tools:
      - get_class_schedule
      - book_class
    collaborators: []
    ```

4.  **`agents/corepower_member_concierge.yaml` (Supervisor)**
    ```yaml
    spec_version: v1
    kind: native
    name: CorePower_Member_Concierge
    llm: watsonx/ibm/granite-3-8b-instruct
    style: default
    description: >
      A helpful AI assistant for CorePower Yoga members. It can answer policy questions, manage accounts, and book classes by collaborating with specialized agents. It is the primary point of contact for members.
    instructions: >
      You are the main AI assistant for CorePower Yoga members. Your primary role is to understand the user's request and route it to the correct collaborator agent. Do not perform tasks yourself.

      Reasoning:
      - For any questions about rules, policies, membership benefits, cancellation, or guests, use the `Membership_Policy_Agent`.
      - For any requests to change account status like freezing a membership, or to ask about billing, use the `Account_Management_Agent`.
      - For any requests related to finding, searching for, or booking a class, use the `Class_Scheduler_Agent`.
      
      Maintain a friendly and helpful tone. Manage the conversation and present the results from your collaborators back to the user.
    collaborators:
      - Membership_Policy_Agent
      - Account_Management_Agent
      - Class_Scheduler_Agent
    ```

## Step 5: Deploy the Solution using the ADK CLI
With all the artifacts created, you can now import them into your watsonx Orchestrate environment. Run these commands from the root of your `corepower-yoga-demo` directory. The order is important: dependencies (knowledge bases, tools) must be imported before the assets that use them (agents). Collaborator agents must be imported before the supervisor that uses them.

1.  **Import the Knowledge Base:**
    ```bash
    orchestrate knowledge-bases import -f corepower_kb.yaml
    ```
    *You can check the ingestion status with `orchestrate knowledge-bases status --name corepower_faq_kb`.*

2.  **Import the Tools:**
    ```bash
    orchestrate tools import -k python -f tools/account_tools.py
    orchestrate tools import -k python -f tools/scheduler_tools.py
    ```

3.  **Import the Collaborator Agents:**
    ```bash
    orchestrate agents import -f agents/membership_policy_agent.yaml
    orchestrate agents import -f agents/account_management_agent.yaml
    orchestrate agents import -f agents/class_scheduler_agent.yaml
    ```

4.  **Import the Supervisor Agent:**
    ```bash
    orchestrate agents import -f agents/corepower_member_concierge.yaml
    ```

## Verification
After successfully importing all components, you can test the complete solution by interacting with the supervisor agent in the chat interface.

1.  **Start the Chat:**
    ```bash
    orchestrate chat start --agent CorePower_Member_Concierge
    ```

2.  **Run Demo Scenarios:**
    *   **Scenario 1 (Knowledge Base Inquiry):**
        *   **User Prompt:** `What is the policy for bringing a guest?`
        *   **Expected Behavior:** The `CorePower_Member_Concierge` should route the request to the `Membership_Policy_Agent`. This agent will query the `corepower_faq_kb` and return an answer based on the content of `Membership_Tiers.txt` ("All Access Membership...Ability to bring one guest per month for free.").

    *   **Scenario 2 (Transactional Action):**
        *   **User Prompt:** `I'm going on vacation, please freeze my membership for 2 months. My member ID is CPY-1001.`
        *   **Expected Behavior:** The supervisor routes to the `Account_Management_Agent`. This agent calls the `freeze_membership` tool with `member_id='CPY-1001'` and `duration_months=2`. The tool updates `members.json` (changing status to 'Frozen') and returns a success message, which the agent relays to the user.

    *   **Scenario 3 (Complex, Multi-Tool Request):**
        *   **User Prompt:** `Are there any C2 classes available after 5 PM tomorrow in the Denver area?`
        *   **Expected Behavior (Part 1):** The supervisor routes to the `Class_Scheduler_Agent`. It calls the `get_class_schedule` tool with `location='Denver'` and `after_time='17:00'`. It will find the C2 class at 17:30 and present it as an option.
        *   **User Follow-up:** `Great, book me for that one. My ID is CPY-2035.`
        *   **Expected Behavior (Part 2):** The `Class_Scheduler_Agent` (still handling the conversation) then calls the `book_class` tool with `member_id='CPY-2035'` and `class_id='C2-1730-DEN'`, returning a confirmation message.

## Troubleshooting
If you encounter issues, here are common problems and their solutions:

*   **Issue: Supervisor agent doesn't route correctly or tries to answer directly.**
    *   **Cause:** The instructions in `corepower_member_concierge.yaml` may not be specific enough, or the descriptions of the collaborator agents are not distinct.
    *   **Solution:** Refine the `instructions` of the supervisor to be more explicit about which agent handles which task, as shown in the example. Ensure each collaborator's `description` clearly states its unique capability. Re-import the agent YAML file after making changes.

*   **Issue: A tool fails with an error like "File not found".**
    *   **Cause:** The Python tool script cannot find the `mock_data/members.json` file. This happens if the `orchestrate` commands are not run from the project root directory.
    *   **Solution:** Ensure your terminal's current directory is `corepower-yoga-demo` before running any `orchestrate` commands. The relative path `./mock_data/members.json` depends on this.

*   **Issue: Knowledge base isn't returning answers.**
    *   **Cause:** The documents may not have been ingested correctly, or their content doesn't match the query.
    *   **Solution:** Run `orchestrate knowledge-bases status --name corepower_faq_kb` to check if the `Ready` property is `true`. If not, wait a few minutes and check again. If it still fails, check the file paths in `corepower_kb.yaml` and re-import.

## Best Practices
Based on this implementation, here are some best practices for building robust watsonx Orchestrate solutions:

*   **Specialize Your Agents:** The supervisor/collaborator pattern is powerful. Create small, single-purpose agents (like `Account_Management_Agent`) that do one thing well. This makes them easier to build, test, and maintain.
*   **Descriptions and Docstrings are Your Prompts:** The LLM relies heavily on the `description` field in agent YAMLs and the docstrings in Python tools to understand what they do. Write them clearly and accurately, as if you were explaining their function to a new team member.
*   **Structure Instructions for Reasoning:** In the supervisor agent's `instructions`, use a `Reasoning:` block to provide explicit rules for routing. This significantly improves the model's decision-making accuracy.
*   **Idempotent Tool Design:** Whenever possible, design tools so that running them multiple times with the same input produces the same result without causing issues. For example, the `freeze_membership` tool simply sets the status to 'Frozen'; running it again on an already frozen account won't break anything.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
