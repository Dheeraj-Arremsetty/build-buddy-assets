# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 19:49:53
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Xerox SMB IT Help Desk Assistant

## Overview

This execution plan provides a comprehensive, step-by-step guide to building and demonstrating the "Xerox SMB IT Help Desk Assistant," a multi-agent Proof of Concept (POC) on IBM watsonx Orchestrate. The solution is tailored to Xerox's goal of creating a new, scalable, subscription-based AI service for its Small and Medium-sized Business (SMB) clients. By implementing a sophisticated **Supervisor/Collaborator pattern**, this demo will showcase an automated IT help desk that intelligently handles common employee support requests, including password resets, software provisioning, and network troubleshooting. This plan directly addresses the client's proposed architecture, mock data strategy, and business objectives, providing a tangible example of how Xerox can reduce IT operational costs for their customers, improve employee productivity with 24/7 support, and establish a new high-margin revenue stream.

## Prerequisites

Before beginning, ensure your environment is set up with the following components. This setup is crucial for developing, deploying, and demonstrating the solution.

1.  **Python Environment**: An installation of Python 3.9 or higher is required.
2.  **IBM watsonx Orchestrate Agent Development Kit (ADK)**: The ADK must be installed and configured. If you haven't installed it, run the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
3.  **Orchestrate CLI Login**: You must be logged into your watsonx Orchestrate environment via the CLI. If you are not logged in, run:
    ```bash
    orchestrate login
    ```
4.  **Project Directory Structure**: Create a dedicated folder for this project to keep all artifacts organized. Use the following structure:
    ```
    xerox-it-demo/
    ├── agents/
    │   ├── it_help_desk_supervisor.yaml
    │   ├── network_troubleshooter_agent.yaml
    │   ├── software_provisioning_agent.yaml
    │   └── user_access_agent.yaml
    ├── data/
    │   ├── software.json
    │   └── users.json
    ├── knowledge_bases/
    │   └── network_kb.yaml
    ├── knowledge_docs/
    │   ├── vpn_guide.txt
    │   └── wifi_setup.txt
    ├── tools/
    │   ├── software_provisioning_tools.py
    │   └── user_access_tools.py
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Knowledge Base Documents

This step involves creating the synthetic data sources that the agents' tools will interact with. This approach allows for a self-contained, repeatable demo without dependencies on live systems.

### 1.1. Mock User Directory

Create a file named `data/users.json`. This file simulates a simple user database for the `User_Access_Agent` to manage.

**File:** `data/users.json`
```json
[
  {
    "employee_id": "XRX-1001",
    "email": "jane.doe@smb-client.com",
    "account_status": "locked"
  },
  {
    "employee_id": "XRX-1002",
    "email": "john.smith@smb-client.com",
    "account_status": "active"
  },
  {
    "employee_id": "XRX-1003",
    "email": "sara.jones@smb-client.com",
    "account_status": "active"
  }
]
```

### 1.2. Mock Software Catalog

Create a file named `data/software.json`. This file acts as a software asset management database for the `Software_Provisioning_Agent`.

**File:** `data/software.json`
```json
[
  {
    "software_name": "Microsoft Visio",
    "total_licenses": 25,
    "used_licenses": 24
  },
  {
    "software_name": "Adobe Photoshop",
    "total_licenses": 10,
    "used_licenses": 10
  },
  {
    "software_name": "Autodesk AutoCAD",
    "total_licenses": 5,
    "used_licenses": 3
  }
]
```

### 1.3. IT Troubleshooting Guides (Knowledge Documents)

These plain text files will populate our knowledge base, enabling the `Network_Troubleshooter_Agent` to perform Retrieval-Augmented Generation (RAG).

**File:** `knowledge_docs/wifi_setup.txt`
```
How to fix Office Wi-Fi Connection Issues

If you are unable to connect to the "SMB-Office-WIFI" network, please follow these steps carefully.

Step 1: Forget the Network
- On Windows: Go to Settings > Network & Internet > Wi-Fi > Manage known networks. Select "SMB-Office-WIFI" and click "Forget".
- On macOS: Go to System Preferences > Network > Wi-Fi > Advanced. Select "SMB-Office-WIFI" from the list and click the minus (-) button to remove it.

Step 2: Reconnect to the Network
- Find the "SMB-Office-WIFI" network in your list of available networks.
- Click to connect. You will be prompted for the password.
- The current password is: "SecurePassword123!"

Step 3: Check IP Address
- If you are connected but have no internet, ensure you have a valid IP address. Open a command prompt (cmd on Windows, Terminal on macOS) and type "ipconfig" (Windows) or "ifconfig" (macOS). If your IP address starts with 169.254, the connection failed to get an address. Try disconnecting and reconnecting.

Step 4: Contact Support
- If these steps do not resolve your issue, please create a support ticket.
```

**File:** `knowledge_docs/vpn_guide.txt`
```
Connecting to the Corporate VPN

All employees must use the "GlobalProtect VPN" client to access internal resources when working remotely.

Installation:
- The GlobalProtect client is pre-installed on all company-issued laptops. If you cannot find it, please request a software installation.

Connection Steps:
1. Open the GlobalProtect application.
2. The portal address should be pre-configured as "vpn.smb-client.com". If it is empty, please enter this address.
3. Click "Connect".
4. You will be prompted to enter your company email and password.
5. Complete the multi-factor authentication (MFA) prompt on your mobile device.
6. Once connected, the status icon will show a green shield.

Common Issues:
- "Connection Failed": This often means an incorrect password or a problem with your internet connection. Please verify your credentials and ensure you are connected to the internet.
- "MFA Prompt Not Received": Check your authenticator app on your phone. If you still do not see a prompt, try restarting the app or your phone.
```

## Step 2: Develop Python Tools

Here, we create the Python functions that provide the "skills" for our agents. Each tool is decorated with `@tool` and includes a detailed docstring, which is critical for the agent to understand its purpose, arguments, and return values.

### 2.1. User Access Management Tools

These tools manage password resets and account unlocking by interacting with the `users.json` file.

**Business Value**: Automating these high-frequency, low-complexity tasks provides immediate value to Xerox's SMB clients by offering instant resolution to employees, reducing downtime, and freeing up IT staff from repetitive work.

**File:** `tools/user_access_tools.py`
```python
import json
import random
import string
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

USER_DATA_FILE = 'data/users.json'

def _load_users():
    """Helper function to load user data from the JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def _save_users(users):
    """Helper function to save user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@tool(permission=ToolPermission.ADMIN)
def reset_user_password(email: str) -> str:
    """
    Resets the password for a user given their email address and generates a temporary password.

    Args:
        email (str): The email address of the user who needs a password reset.

    Returns:
        str: A confirmation message including a new temporary password, or an error message if the user is not found.
    """
    users = _load_users()
    user_found = False
    for user in users:
        if user['email'].lower() == email.lower():
            user_found = True
            # In a real scenario, this would trigger a secure reset flow.
            # For the demo, we generate and return a temporary password.
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user['account_status'] = 'active' # Resetting password often implies unlocking.
            _save_users(users)
            return f"Password for {email} has been successfully reset. The temporary password is: {temp_password}. Please change it upon first login."
    
    if not user_found:
        return f"Error: User with email {email} not found in the directory."

@tool(permission=ToolPermission.ADMIN)
def unlock_user_account(email: str) -> str:
    """
    Unlocks a user's account if it is currently in a 'locked' state.

    Args:
        email (str): The email address of the user whose account needs to be unlocked.

    Returns:
        str: A confirmation message that the account has been unlocked, or a message indicating its current status.
    """
    users = _load_users()
    for user in users:
        if user['email'].lower() == email.lower():
            if user['account_status'] == 'locked':
                user['account_status'] = 'active'
                _save_users(users)
                return f"The account for {email} has been successfully unlocked."
            else:
                return f"The account for {email} is already active."
    return f"Error: User with email {email} not found in the directory."
```

### 2.2. Software Provisioning Tools

These tools check license availability and simulate a software installation request by interacting with `software.json`.

**Business Value**: This automates the software request lifecycle. For SMBs, this provides a streamlined, auditable process for managing costly software licenses, preventing over-provisioning, and ensuring employees get the tools they need quickly.

**File:** `tools/software_provisioning_tools.py`
```python
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

SOFTWARE_CATALOG_FILE = 'data/software.json'

def _load_software_catalog():
    """Helper function to load software data from the JSON file."""
    try:
        with open(SOFTWARE_CATALOG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@tool(permission=ToolPermission.ADMIN)
def check_license_availability(software_name: str) -> str:
    """
    Checks if there are available licenses for a given piece of software in the catalog.

    Args:
        software_name (str): The name of the software to check (e.g., 'Microsoft Visio').

    Returns:
        str: A message indicating whether licenses are available, not available, or if the software is not found.
    """
    catalog = _load_software_catalog()
    for software in catalog:
        if software['software_name'].lower() == software_name.lower():
            available_licenses = software['total_licenses'] - software['used_licenses']
            if available_licenses > 0:
                return f"Yes, there are {available_licenses} licenses available for {software_name}."
            else:
                return f"No, there are currently no available licenses for {software_name}."
    return f"Software named '{software_name}' was not found in the catalog."

@tool(permission=ToolPermission.ADMIN)
def request_software_install(software_name: str, user_email: str) -> str:
    """
    Submits a request for a software installation after checking for license availability. If a license is available, it simulates creating a service ticket.

    Args:
        software_name (str): The name of the software being requested.
        user_email (str): The email of the user requesting the software.

    Returns:
        str: A confirmation message with a ticket number if the request is successful, or an error message if no licenses are available.
    """
    catalog = _load_software_catalog()
    software_found = False
    for software in catalog:
        if software['software_name'].lower() == software_name.lower():
            software_found = True
            available_licenses = software['total_licenses'] - software['used_licenses']
            if available_licenses > 0:
                # Simulate ticket creation
                ticket_id = f"INC{random.randint(10000, 99999)}"
                # In a real system, we would decrement the license count here.
                # For the demo, we won't modify the file to keep it repeatable.
                return f"Request approved. A support ticket ({ticket_id}) has been created to install {software_name} for {user_email}. The IT team will be in touch shortly."
            else:
                return f"Request denied for {software_name}. No licenses are currently available. Please contact IT for alternatives."
    
    if not software_found:
        return f"Cannot process request. Software '{software_name}' is not in our catalog."
```

## Step 3: Define the Knowledge Base

This YAML file defines the knowledge base that the `Network_Troubleshooter_Agent` will use. It points to the text documents we created, which will be ingested into the built-in Milvus vector database.

**File:** `knowledge_bases/network_kb.yaml`
```yaml
spec_version: v1
kind: knowledge_base
name: network_troubleshooting_kb
description: >
  Contains technical guides, standard operating procedures, and FAQs for solving common employee network connectivity issues. This includes problems with office Wi-Fi, corporate VPN access, and general internet connectivity.
documents:
  - "knowledge_docs/wifi_setup.txt"
  - "knowledge_docs/vpn_guide.txt"
vector_index:
  embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

## Step 4: Define the Agent Configurations

We will now define each agent in its own YAML file. The descriptions and instructions are written carefully to ensure the Supervisor agent can accurately route tasks.

### 4.1. Network Troubleshooter Agent (RAG Collaborator)

This agent specializes in answering questions by searching its knowledge base. It doesn't use any custom Python tools.

**File:** `agents/network_troubleshooter_agent.yaml`
```yaml
spec_version: v1
kind: native
name: Network_Troubleshooter_Agent
description: >
  A specialist agent that provides first-line support for common network connectivity issues. Use this agent for user questions about connecting to office Wi-Fi, accessing the corporate VPN, or general internet problems. It leverages a knowledge base of troubleshooting guides to provide step-by-step instructions.
instructions: >
  Your sole purpose is to answer user questions about network problems by consulting your knowledge base.
  When a user describes a network issue (e.g., "can't connect to wifi", "vpn not working"), search your knowledge base for relevant documents.
  Synthesize the information from the documents into a clear, concise, step-by-step answer for the user.
  If you cannot find a relevant answer in your knowledge base, state that you do not have the information and recommend they contact the IT help desk directly. Do not attempt to answer from general knowledge.
llm: watsonx/ibm/granite-3-8b-instruct
style: default
knowledge_base:
  - network_troubleshooting_kb
```

### 4.2. Software Provisioning Agent (Tool-based Collaborator)

This agent uses the software provisioning tools to handle software requests.

**File:** `agents/software_provisioning_agent.yaml`
```yaml
spec_version: v1
kind: native
name: Software_Provisioning_Agent
description: >
  A specialist agent for managing the entire software request lifecycle. Use this agent for tasks related to requesting new software installations and checking for license availability. It can interact with the software asset catalog to validate requests.
instructions: >
  You are an assistant for software asset management.
  - If the user wants to know if a software is available, use the `check_license_availability` tool.
  - If a user wants to install or request software, first use the `check_license_availability` tool. If a license is available, then use the `request_software_install` tool to create a ticket. You will need to ask the user for their email address if it is not provided.
  - Always report the outcome of the tool back to the user, whether it's a success with a ticket number or a denial due to lack of licenses.
llm: watsonx/ibm/granite-3-8b-instruct
style: default
tools:
  - check_license_availability
  - request_software_install
```

### 4.3. User Access Agent (Tool-based Collaborator)

This agent uses the user access tools to handle account lockouts and password resets.

**File:** `agents/user_access_agent.yaml`
```yaml
spec_version: v1
kind: native
name: User_Access_Agent
description: >
  A specialist agent focused exclusively on managing user accounts and access credentials. Use this agent for requests to reset a user's password or to unlock a user's account. It securely handles these sensitive operations.
instructions: >
  You are a security assistant for user account management.
  - When a user says they are locked out or need their password reset, you must determine which action to take.
  - For password reset requests, use the `reset_user_password` tool.
  - For account unlock requests, use the `unlock_user_account` tool.
  - You must have the user's email address to perform any action. If it is not provided in the initial request, you must ask the user for it before calling a tool.
  - Clearly communicate the result of the action to the user.
llm: watsonx/ibm/granite-3-8b-instruct
style: default
tools:
  - reset_user_password
  - unlock_user_account
```

### 4.4. IT Help Desk Supervisor (Supervisor Agent)

This is the main, user-facing agent. It has no tools or knowledge bases of its own; its power comes from its ability to delegate tasks to its collaborators.

**File:** `agents/it_help_desk_supervisor.yaml`
```yaml
spec_version: v1
kind: native
name: IT_Help_Desk_Supervisor
description: >
  A primary, user-facing IT Help Desk supervisor agent. It assists employees by understanding their IT support needs and routing their requests to the appropriate specialist agent. It can coordinate help for password resets, software requests, and network troubleshooting.
instructions: >
  You are the central coordinator for an IT help desk. Your primary job is to understand the user's request and delegate it to the correct specialist agent from your list of collaborators.
  - Read the user's request carefully to determine their intent.
  - Review the descriptions of your collaborator agents to decide which one is best suited for the task.
  - If the request is about passwords or being locked out, delegate to the 'User_Access_Agent'.
  - If the request is about installing software or checking licenses, delegate to the 'Software_Provisioning_Agent'.
  - If the request is about Wi-Fi, VPN, or internet problems, delegate to the 'Network_Troubleshooter_Agent'.
  - Do not attempt to answer the question or perform the task yourself. Your only role is to route the request to the correct collaborator.
llm: watsonx/ibm/granite-3-8b-instruct
style: default
collaborators:
  - User_Access_Agent
  - Software_Provisioning_Agent
  - Network_Troubleshooter_Agent
```

## Step 5: Create `requirements.txt`

This file lists the Python packages required for the tools. While our current tools only use the standard library, it's a best practice to include this file. We add `requests` as an example of a common dependency for real-world tools that call APIs.

**File:** `requirements.txt`
```
requests
```

## Step 6: Deployment and Execution Sequence

Follow this precise sequence of CLI commands to import all artifacts into your watsonx Orchestrate environment. The order is crucial: dependencies (tools, knowledge bases) must be imported before the assets that use them (agents).

```bash
# Navigate to the root of your project directory
cd /path/to/xerox-it-demo

# Step 1: Import all Python-based tools
echo "Importing User Access tools..."
orchestrate tools import -f tools/user_access_tools.py

echo "Importing Software Provisioning tools..."
orchestrate tools import -f tools/software_provisioning_tools.py

# Step 2: Import the knowledge base
echo "Importing Network Troubleshooting knowledge base..."
orchestrate knowledge-bases import -f knowledge_bases/network_kb.yaml

# Step 3: Import the collaborator agents (these must exist before the supervisor)
echo "Importing Network Troubleshooter agent..."
orchestrate agents import -f agents/network_troubleshooter_agent.yaml

echo "Importing Software Provisioning agent..."
orchestrate agents import -f agents/software_provisioning_agent.yaml

echo "Importing User Access agent..."
orchestrate agents import -f agents/user_access_agent.yaml

# Step 4: Import the supervisor agent last
echo "Importing IT Help Desk Supervisor agent..."
orchestrate agents import -f agents/it_help_desk_supervisor.yaml

# Step 5: Start the interactive chat to begin the demo
echo "All assets imported. Starting chat with the Supervisor agent..."
orchestrate chat start --agent IT_Help_Desk_Supervisor
```

## Verification and Demo Scenarios

After running `orchestrate chat start`, you can test the complete solution using the following scenarios directly from the client demo concept.

### Scenario 1: Password Reset

*   **User Input:** `I'm locked out of my account, my email is jane.doe@smb-client.com.`
*   **Expected Behavior:**
    1.  The `IT_Help_Desk_Supervisor` receives the prompt. Based on the keywords "locked out" and its collaborator descriptions, it correctly routes the task to the `User_Access_Agent`.
    2.  The `User_Access_Agent` receives the task and determines the user's intent is to reset their password.
    3.  It calls the `reset_user_password` tool with the email `jane.doe@smb-client.com`.
    4.  The tool updates the `data/users.json` file, changing the status for Jane Doe from "locked" to "active".
    5.  The tool returns a success message with a temporary password.
*   **Expected AI Output:** `Password for jane.doe@smb-client.com has been successfully reset. The temporary password is: [Generated 10-character password]. Please change it upon first login.`

### Scenario 2: Software Request

*   **User Input:** `I need to install Microsoft Visio.`
*   **Expected Behavior:**
    1.  The `IT_Help_Desk_Supervisor` routes the request to the `Software_Provisioning_Agent`.
    2.  The `Software_Provisioning_Agent`'s instructions guide it to first ask for the user's email.
    3.  **User provides email:** `My email is john.smith@smb-client.com`
    4.  The agent calls the `request_software_install` tool with "Microsoft Visio" and the user's email.
    5.  The tool checks `data/software.json`, finds that licenses are available (25 total - 24 used = 1 available), and simulates creating a ticket.
*   **Expected AI Output:** `Request approved. A support ticket (INCXXXXX) has been created to install Microsoft Visio for john.smith@smb-client.com. The IT team will be in touch shortly.`

### Scenario 3: Network Troubleshooting (RAG)

*   **User Input:** `My laptop won't connect to the office Wi-Fi.`
*   **Expected Behavior:**
    1.  The `IT_Help_Desk_Supervisor` identifies the request as a network issue and routes it to the `Network_Troubleshooter_Agent`.
    2.  The `Network_Troubleshooter_Agent` does not use tools. Instead, it performs a semantic search against its knowledge base (`network_troubleshooting_kb`).
    3.  It finds the `wifi_setup.txt` document to be the most relevant.
    4.  It synthesizes the content of the document into a helpful, conversational response.
*   **Expected AI Output:** `I can help with that. If you are unable to connect to the "SMB-Office-WIFI" network, please try these steps: First, "forget" the network from your device's Wi-Fi settings. Then, try to reconnect and enter the password "SecurePassword123!" when prompted. If that doesn't work, please let me know.`

## Troubleshooting

*   **Incorrect Agent Routing**: If the Supervisor sends a task to the wrong agent, review the `description` fields in the collaborator agent YAML files. The Supervisor relies heavily on these descriptions. Make them more distinct and keyword-rich. For example, ensure "password" and "account" are prominent in the `User_Access_Agent`'s description.
*   **Tool Not Found Error**: This usually means the tool was not imported successfully before the agent that uses it. Re-run the `orchestrate tools import -f <file>` command for the missing tool and then re-import the agent.
*   **Python Tool Errors**: If a tool fails during execution, check the terminal where you ran `orchestrate chat start` for Python tracebacks. Common issues include incorrect file paths to the JSON data files or bugs in the tool's logic. Ensure the `data` directory is in the same root folder where you run the commands.
*   **Knowledge Base Not Working**: If the `Network_Troubleshooter_Agent` responds with "I don't know," check the status of the knowledge base with `orchestrate knowledge-bases status --name network_troubleshooting_kb`. The status should be "Ready". If not, there may have been an issue during ingestion. Try removing and re-importing it.

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
