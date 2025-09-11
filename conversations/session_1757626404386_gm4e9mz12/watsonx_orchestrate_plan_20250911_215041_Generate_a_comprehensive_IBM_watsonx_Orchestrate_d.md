# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-11 21:50:41
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Yoga SubConnect for CorePower Yoga

## 1. Overview

This execution plan provides a comprehensive, step-by-step guide to building and deploying the **"Yoga SubConnect"** proof-of-concept (POC) for CorePower Yoga using IBM watsonx Orchestrate. The solution is designed to address the critical operational challenge of managing last-minute teacher absences by automating the entire workflow of finding, contacting, and confirming substitute teachers.

This plan implements a multi-agent architecture, featuring a supervisor agent that orchestrates specialized collaborator agents. This system transforms a manual, time-consuming process into a streamlined, intelligent, and efficient workflow. The primary business values delivered are a significant reduction in administrative overhead for studio managers, minimization of class cancellations, enhanced service reliability, and an improved experience for both yoga members and instructors.

## 2. Prerequisites

Before beginning, ensure your development environment is properly configured.

*   **IBM watsonx Orchestrate ADK**: The Agent Development Kit must be installed and configured. Follow the official documentation for [Installing the watsonx Orchestrate ADK](https://developer.watson-orchestrate.ibm.com/getting_started/installing).
*   **Python**: Python 3.9 or higher is required.
*   **Project Directory Structure**: Create a root folder for the project (e.g., `cpy_orchestrate_demo`) and organize your files as follows to maintain clarity and modularity.

    ```
    cpy_orchestrate_demo/
    |-- agents/
    |   |-- sub_coordinator_agent.yaml
    |   |-- schedule_manager_agent.yaml
    |   |-- teacher_comms_agent.yaml
    |-- tools/
    |   |-- schedule_tools.py
    |   |-- comms_tools.py
    |-- knowledge_base/
    |   |-- cpy_policy_kb.yaml
    |-- data/
    |   |-- teachers.json
    |   |-- schedule.json
    |-- documents/
    |   |-- Substitute_Teacher_Policy.txt
    |   |-- Class_Format_Guide.txt
    |-- requirements.txt
    ```

*   **Python Packages**: Create a `requirements.txt` file in the root directory. While our mock tools primarily use the standard library, real-world tools often require external packages.

    **File: `requirements.txt`**
    ```
    requests
    python-dotenv
    ```
    Install the packages using the following command:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Create Mock Data and Policy Documents

First, we will create the synthetic data sources that our tools will interact with. This data simulates CorePower Yoga's operational databases and policy documents.

#### A. Create Teacher Roster (`teachers.json`)

This file contains a list of instructors, their certifications, and their availability to sub.

**File: `data/teachers.json`**
```json
[
  {
    "teacher_id": "T001",
    "name": "Sarah Johnson",
    "phone_number": "555-0101",
    "certifications": ["C2", "Yoga Sculpt"],
    "is_available_for_subbing": true
  },
  {
    "teacher_id": "T002",
    "name": "Emily White",
    "phone_number": "555-0102",
    "certifications": ["C2", "Hot Power Fusion"],
    "is_available_for_subbing": true
  },
  {
    "teacher_id": "T003",
    "name": "Michael Brown",
    "phone_number": "555-0103",
    "certifications": ["Yoga Sculpt"],
    "is_available_for_subbing": false
  },
  {
    "teacher_id": "T004",
    "name": "Jessica Green",
    "phone_number": "555-0104",
    "certifications": ["C2", "Yoga Sculpt", "Hot Power Fusion"],
    "is_available_for_subbing": true
  },
  {
    "teacher_id": "T005",
    "name": "David Black",
    "phone_number": "555-0105",
    "certifications": ["C2"],
    "is_available_for_subbing": true
  }
]
```

#### B. Create Master Class Schedule (`schedule.json`)

This file represents the weekly class schedule.

**File: `data/schedule.json`**
```json
[
  {
    "class_id": "C101",
    "studio_location": "LoDo",
    "class_name": "C2",
    "start_time": "2024-09-25T18:00:00Z",
    "assigned_teacher_id": "T001"
  },
  {
    "class_id": "C102",
    "studio_location": "LoDo",
    "class_name": "Yoga Sculpt",
    "start_time": "2024-09-25T05:30:00Z",
    "assigned_teacher_id": "T004"
  },
  {
    "class_id": "C103",
    "studio_location": "Cherry Creek",
    "class_name": "Hot Power Fusion",
    "start_time": "2024-09-26T12:00:00Z",
    "assigned_teacher_id": "T002"
  }
]
```

#### C. Create Policy Documents

These text files will populate our knowledge base for RAG queries.

**File: `documents/Substitute_Teacher_Policy.txt`**
```
CorePower Yoga Substitute Teacher Policy

Pay Rates:
- 60-minute class: $45
- 75-minute class: $55

Confirmation Procedure:
A substitute is considered confirmed once they reply 'CONFIRM' to the automated SMS notification. The schedule will be updated automatically. Studio managers will receive a final confirmation message.

Cancellation:
If a confirmed substitute needs to cancel, they must contact the studio manager directly at least 2 hours before the class start time.
```

**File: `documents/Class_Format_Guide.txt`**
```
CorePower Yoga Class Format Guide

C2: CorePower Yoga 2
Our signature Vinyasa class. This class builds on the C1 foundation and is suitable for intermediate levels. Certification Required: C2.

Yoga Sculpt:
A high-intensity workout blending Vinyasa flow with strength training using free weights. Certification Required: Yoga Sculpt.

Hot Power Fusion:
A blend of Hot Yoga and Power Vinyasa styles, practiced in a heated, humid room. Certification Required: Hot Power Fusion.
```

### Step 2: Define and Create the Knowledge Base

We will create a built-in knowledge base using watsonx Orchestrate's Milvus instance to ingest our policy documents.

**Explanation:** The `cpy_policy_kb` will enable the `SubCoordinator Agent` to answer policy-related questions directly, such as "What is the pay rate for subbing?". This demonstrates Retrieval-Augmented Generation (RAG), providing grounded, accurate answers from trusted company documents and reducing the need for managers to look up information manually.

**File: `knowledge_base/cpy_policy_kb.yaml`**
```yaml
spec_version: v1
kind: knowledge_base
name: cpy_policy_kb
description: >
   Contains official CorePower Yoga policies regarding substitute teachers,
   pay rates, class formats, and studio procedures.
documents:
   - "documents/Substitute_Teacher_Policy.txt"
   - "documents/Class_Format_Guide.txt"
vector_index:
   # Using the default model as it's robust for general text
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

### Step 3: Develop the Python Tools

Here we implement the core logic of our application. Each tool is a Python function decorated with `@tool`, containing a detailed docstring that the LLM uses to understand its purpose, arguments, and return values.

#### A. Schedule Management Tools

These tools interact with the `schedule.json` and `teachers.json` files to manage class and teacher data.

**File: `tools/schedule_tools.py`**
```python
import json
from typing import List, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# Define paths to our mock data files
TEACHERS_FILE = 'data/teachers.json'
SCHEDULE_FILE = 'data/schedule.json'

def _load_data(file_path: str) -> List[Dict]:
    """Helper function to load data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save_data(file_path: str, data: List[Dict]):
    """Helper function to save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

@tool(name="find_class_details", permission=ToolPermission.ADMIN)
def find_class_details(teacher_name: str, class_time: str, studio_location: str) -> Optional[Dict]:
    """
    Finds specific details for a class based on the original teacher, time, and location.

    This tool is essential for initiating the substitute process. It retrieves the unique class ID and required certification format, which are necessary inputs for finding a suitable substitute and updating the schedule.

    Args:
        teacher_name (str): The first name of the teacher who needs a substitute (e.g., "Sarah").
        class_time (str): The start time of the class in ISO format (e.g., "2024-09-25T18:00:00Z").
        studio_location (str): The location of the studio (e.g., "LoDo").

    Returns:
        Optional[Dict]: A dictionary containing class details ('class_id', 'class_name', 'assigned_teacher_id') or None if not found.
    """
    schedule = _load_data(SCHEDULE_FILE)
    teachers = _load_data(TEACHERS_FILE)
    
    teacher_id = None
    for teacher in teachers:
        if teacher_name.lower() in teacher['name'].lower():
            teacher_id = teacher['teacher_id']
            break
            
    if not teacher_id:
        return None

    for class_info in schedule:
        if (class_info['assigned_teacher_id'] == teacher_id and
            class_info['start_time'] == class_time and
            class_info['studio_location'].lower() == studio_location.lower()):
            return class_info
            
    return None

@tool(name="find_available_subs", permission=ToolPermission.ADMIN)
def find_available_subs(class_name: str, original_teacher_id: str) -> List[Dict]:
    """
    Finds available and certified substitute teachers for a specific class format.

    This tool automates the most critical step: intelligent matching. It filters the entire teacher roster to find instructors who hold the correct certification for the class (e.g., "Yoga Sculpt") and are marked as available, ensuring class quality is maintained.

    Args:
        class_name (str): The name/format of the class needing a sub (e.g., "C2", "Yoga Sculpt").
        original_teacher_id (str): The ID of the teacher who cannot teach the class, to exclude them from the search.

    Returns:
        List[Dict]: A list of teacher objects who are available and certified, excluding the original teacher.
    """
    teachers = _load_data(TEACHERS_FILE)
    available_subs = []
    
    for teacher in teachers:
        if (teacher['is_available_for_subbing'] and
            class_name in teacher['certifications'] and
            teacher['teacher_id'] != original_teacher_id):
            available_subs.append({
                "teacher_id": teacher["teacher_id"],
                "name": teacher["name"],
                "phone_number": teacher["phone_number"]
            })
            
    return available_subs

@tool(name="update_class_schedule", permission=ToolPermission.ADMIN)
def update_class_schedule(class_id: str, new_teacher_id: str) -> Dict:
    """
    Updates the assigned teacher for a specific class in the master schedule.

    This tool closes the loop on the workflow. Once a substitute is confirmed, this function updates the system of record (our mock schedule.json), ensuring that all studio systems are synchronized and accurate. This prevents confusion and ensures a smooth class experience.

    Args:
        class_id (str): The unique identifier of the class to update.
        new_teacher_id (str): The unique identifier of the new substitute teacher.

    Returns:
        Dict: A confirmation message indicating success or failure.
    """
    schedule = _load_data(SCHEDULE_FILE)
    class_found = False
    for class_info in schedule:
        if class_info['class_id'] == class_id:
            class_info['assigned_teacher_id'] = new_teacher_id
            class_found = True
            break
            
    if class_found:
        _save_data(SCHEDULE_FILE, schedule)
        return {"status": "Success", "message": f"Class {class_id} has been updated with new teacher {new_teacher_id}."}
    else:
        return {"status": "Error", "message": f"Class with ID {class_id} not found."}

```

#### B. Teacher Communication Tools

This tool simulates sending communications to teachers.

**File: `tools/comms_tools.py`**
```python
import json
from typing import Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="send_sms_notification", permission=ToolPermission.ADMIN)
def send_sms_notification(teacher_name: str, phone_number: str, class_details: str) -> Dict:
    """
    Sends a simulated SMS notification to a teacher to ask if they can sub for a class.

    This tool acts as the bridge to external communication systems (like Twilio). It automates the outreach process, saving managers from having to manually text or call potential substitutes. The tool simulates a confirmation, allowing the automated workflow to proceed to the final step.

    Args:
        teacher_name (str): The name of the teacher to contact.
        phone_number (str): The phone number of the teacher.
        class_details (str): A summary of the class details (e.g., "6 PM C2 class at LoDo tomorrow").

    Returns:
        Dict: A dictionary indicating the status of the notification and a simulated confirmation.
    """
    # In a real-world scenario, this would integrate with an SMS API like Twilio.
    # For this demo, we print to the console and return a success message.
    print(f"\n--- SIMULATING SMS ---")
    print(f"To: {teacher_name} ({phone_number})")
    print(f"Message: Hi {teacher_name}, can you sub the {class_details}? Reply 'CONFIRM' if yes.")
    print(f"--- SIMULATION END ---\n")
    
    # We simulate an immediate positive response for the "happy path" demo.
    return {
        "status": "Notification Sent",
        "confirmation_received": True,
        "message": f"Successfully sent sub request to {teacher_name} and received confirmation."
    }
```

### Step 4: Define the Agents using YAML

Now, we define the agents themselves. We start with the specialized collaborator agents and finish with the supervisor agent that orchestrates them.

#### A. TeacherComms Agent (Collaborator)

**Explanation:** This agent's sole responsibility is communication. By isolating this function, we create a modular system. If CorePower Yoga decides to switch from SMS to email or a mobile app for notifications, only this agent and its tool need to be updated, without affecting the scheduling logic.

**File: `agents/teacher_comms_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: teacher_comms_agent
description: >
  An agent specializing in handling outbound communications with yoga teachers. 
  Use this agent to send notifications, such as substitute teaching requests, via SMS.
instructions: >
  Your only purpose is to send notifications to teachers using the send_sms_notification tool.
  When asked to contact a teacher, use the tool with the provided details and report the result.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - send_sms_notification
```

#### B. ScheduleManager Agent (Collaborator)

**Explanation:** This agent is the single source of truth for all schedule- and roster-related operations. It abstracts the underlying data source (our JSON files, but in reality a database or scheduling API). This separation of concerns means the supervisor agent doesn't need to know *how* to find a sub, only that it can ask the `ScheduleManager` to do it.

**File: `agents/schedule_manager_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: schedule_manager_agent
description: >
  An agent that interacts with CorePower Yoga's scheduling and teacher roster data. 
  It can find details about classes, identify qualified and available substitute teachers,
  and update the class schedule with new teacher assignments.
instructions: >
  You are an expert at managing schedules.
  - Use the find_class_details tool to get the specific ID and format for a class.
  - Use the find_available_subs tool to get a list of potential substitutes for a class.
  - Use the update_class_schedule tool to assign a new teacher to a class after they have confirmed.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
tools:
  - find_class_details
  - find_available_subs
  - update_class_schedule
```

#### C. SubCoordinator Agent (Supervisor)

**Explanation:** This is the "brain" of the operation and the main entry point for the user. It interprets the user's natural language request, forms a plan, and delegates tasks to its specialized collaborators. Its instructions are crucial; they define the multi-step reasoning process (find class -> find sub -> notify sub -> update schedule). It also knows to use its knowledge base for policy questions, making it a versatile and powerful assistant for studio managers.

**File: `agents/sub_coordinator_agent.yaml`**
```yaml
spec_version: v1
kind: native
name: sub_coordinator_agent
description: >
    An agent that coordinates finding and scheduling substitute yoga teachers for CorePower Yoga.
    It uses the ScheduleManager agent to check schedules and teacher availability, and the TeacherComms
    agent to notify instructors. It can also answer questions about company subbing policies from its knowledge base.
instructions: >
    You are an expert AI assistant for CorePower Yoga studio managers. Your purpose is to find substitute teachers efficiently.

    Reasoning Workflow:
    1.  **Understand the Request**: When a manager asks for a sub, identify the original teacher's name, the class time, and the studio location.
    2.  **Get Class Details**: Use the `schedule_manager_agent` to run the `find_class_details` tool to get the precise `class_id`, `class_name`, and `original_teacher_id`. This is the first and most critical step.
    3.  **Find a Substitute**: With the class details, use the `schedule_manager_agent` again to run the `find_available_subs` tool to get a list of potential substitutes.
    4.  **Handle Scenarios**:
        - **If subs are found**: Pick the first available sub. Use the `teacher_comms_agent` to run the `send_sms_notification` tool to contact them.
        - **If the sub confirms**: Use the `schedule_manager_agent` a final time to run the `update_class_schedule` tool. Then, confirm to the manager that the process is complete.
        - **If no subs are found**: Inform the manager clearly. Suggest alternative options, like searching for teachers with a different, but similar, certification if applicable.
    5.  **Answer Policy Questions**: If the user asks a question about policies, pay rates, or procedures, use the information from your knowledge base to provide a direct and accurate answer.
llm: watsonx/ibm/granite-13b-chat-v2
style: default
collaborators:
  - schedule_manager_agent
  - teacher_comms_agent
knowledge_base:
  - cpy_policy_kb
```

### Step 5: Deploy the Solution using the ADK CLI

With all artifacts created, we deploy them to watsonx Orchestrate in a specific order to respect dependencies. Tools and knowledge bases must exist before the agents that use them can be imported. Collaborator agents must exist before the supervisor agent that calls them.

Execute these commands from the root directory of your project (`cpy_orchestrate_demo/`).

```bash
# Set the current directory for the ADK to find relative paths
export ADK_PROJECT_DIR=$(pwd)

# 1. Import the Knowledge Base
echo "Importing Knowledge Base..."
orchestrate knowledge-bases import -f knowledge_base/cpy_policy_kb.yaml

# 2. Import the Tools
echo "Importing Schedule Tools..."
orchestrate tools import -f tools/schedule_tools.py

echo "Importing Comms Tools..."
orchestrate tools import -f tools/comms_tools.py

# 3. Import the Collaborator Agents
echo "Importing TeacherComms Agent..."
orchestrate agents import -f agents/teacher_comms_agent.yaml

echo "Importing ScheduleManager Agent..."
orchestrate agents import -f agents/schedule_manager_agent.yaml

# 4. Import the Supervisor Agent
echo "Importing SubCoordinator Agent..."
orchestrate agents import -f agents/sub_coordinator_agent.yaml

# 5. Start the chat to begin testing
echo "Deployment complete. Starting chat..."
orchestrate chat start --agent sub_coordinator_agent
```

## 4. Verification and Demo Scenarios

After running `orchestrate chat start`, use the following prompts to test the three key scenarios outlined in the demo concept.

#### Scenario 1: The "Happy Path" Request

*   **User Prompt:** `I need a sub for Sarah's 6 PM C2 class at the LoDo studio tomorrow.`
    *   *(Note: The date/time in the prompt should match an entry in `schedule.json`. For the demo, you can say "for the class at 2024-09-25T18:00:00Z" to be precise.)*
*   **Expected Agent Behavior:**
    1.  `SubCoordinator Agent` delegates to `ScheduleManager Agent` to find class details for "Sarah".
    2.  `ScheduleManager Agent` finds class `C101`, a `C2` class.
    3.  `SubCoordinator Agent` asks `ScheduleManager Agent` to find available subs with a `C2` certification.
    4.  `ScheduleManager Agent` returns a list including Emily White (`T002`) and Jessica Green (`T004`).
    5.  `SubCoordinator Agent` picks the first one (Emily) and delegates to `TeacherComms Agent` to send a notification.
    6.  `TeacherComms Agent` simulates the SMS and returns a confirmation.
    7.  `SubCoordinator Agent` delegates to `ScheduleManager Agent` to update class `C101` with teacher `T002`.
*   **Expected Final Output:** `Done. Emily White will be subbing the C2 class at LoDo scheduled for 2024-09-25T18:00:00Z. The schedule has been updated.`

#### Scenario 2: The "No Availability" Escalation

*   **User Prompt:** `Find a sub for the 5:30 AM Yoga Sculpt class at LoDo today.`
*   **Expected Agent Behavior:**
    1.  The agent follows the same initial steps to identify the class (`C102`) and its requirement (`Yoga Sculpt`).
    2.  It then searches for available subs. It will find Michael Brown (`T003`) is certified but `is_available_for_subbing` is `false`. It will find Sarah (`T001`) is also certified, but let's assume she is the original teacher for this scenario to test the logic.
    3.  Finding no available and certified teachers, the agent's instructions guide it to escalate.
*   **Expected Final Output:** `I could not find any available Yoga Sculpt certified teachers for that time. Would you like me to search for teachers certified in a different format, like C2, who are available?`

#### Scenario 3: The "Policy Query" (RAG)

*   **User Prompt:** `What is the pay rate for subbing a 75-minute class?`
*   **Expected Agent Behavior:**
    1.  The `SubCoordinator Agent` recognizes this is a policy question, not a task.
    2.  It queries its attached knowledge base, `cpy_policy_kb`.
    3.  It finds the relevant text in the `Substitute_Teacher_Policy.txt` document.
*   **Expected Final Output:** `According to the policy documents, the pay rate for subbing a 75-minute class is $55.`

## 5. Troubleshooting

*   **Tool Import Fails**:
    *   **Issue**: `ModuleNotFoundError` or similar Python error during `orchestrate tools import`.
    *   **Solution**: Ensure you have run `pip install -r requirements.txt`. Verify that all Python files have the correct import statements at the top. Check for syntax errors in the Python tool files.
*   **Agent Import Fails**:
    *   **Issue**: Error message like `Collaborator "schedule_manager_agent" not found.`
    *   **Solution**: You must import agents in the correct order. Collaborators must be imported *before* the supervisor that uses them. Re-run the import commands in the sequence provided in Step 5.
*   **Agent Does Not Use the Correct Tool/Collaborator**:
    *   **Issue**: The agent seems to misunderstand the request or fails to delegate correctly.
    *   **Solution**: This is often an issue with the quality of the `description` and `instructions` in the agent's YAML file. Make them more explicit and direct. For example, instead of "manage the schedule," say "Use the `schedule_manager_agent` to find classes, find subs, and update schedules."
*   **Knowledge Base Query Fails**:
    *   **Issue**: The agent responds with "I don't know" to a policy question.
    *   **Solution**: Verify the `documents` paths in `cpy_policy_kb.yaml` are correct relative to your project root. Ensure the `knowledge_base` key is correctly configured in `sub_coordinator_agent.yaml`. You can check the status of the knowledge base ingestion with `orchestrate knowledge-bases get cpy_policy_kb`.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
