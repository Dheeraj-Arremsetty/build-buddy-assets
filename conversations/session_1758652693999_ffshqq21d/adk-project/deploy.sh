#!/bin/bash
# Generated deployment script

# Script block 1
pip install "ibm-watsonx-orchestrate"
    ```
*   **Orchestrate Environment:** You must have an active IBM watsonx Orchestrate environment initialized. This can be a local Developer Edition for rapid prototyping or a SaaS environment for a more production-like setup.
*   **Project Directory Structure:** A well-organized directory is essential for managing the various artifacts (agents, tools, documents). Create a root folder for the project and then the following subdirectories. This structure is mandatory for the file paths in the configuration files to work correctly.

    ```
    employee_lifecycle_demo/
    ├── agents/
    │   ├── IT_ServiceNow_Agent.yaml
    │   ├── Identity_Okta_Agent.yaml
    │   ├── LMS_Enrollment_Agent.yaml
    │   └── EmployeeLifecycle_Supervisor.yaml
    ├── tools/
    │   ├── it_tools.py
    │   ├── identity_tools.py
    │   └── lms_tools.py
    ├── knowledge_bases/
    │   └── hr_policy_kb.yaml
    ├── documents/
    │   └── HR_Onboarding_Policy.pdf
    └── requirements.txt
    ```

## 3. Step-by-Step Implementation

This section provides the detailed steps, complete code, and configuration files needed to build the entire demo from the ground up.

### Step 3.1: Create Project Structure and Mock Data

Begin by setting up the project directory as detailed above. Then, create the necessary mock data files and dependencies that will power the demo.

1.  **Create `requirements.txt`:** In the root of your `employee_lifecycle_demo` directory, create this file. It will manage the Python dependencies for our tools.
    ```text
    # requirements.txt
    requests
    python-dotenv
    ```
2.  **Create `documents/HR_Onboarding_Policy.pdf`:** Create a PDF document containing the following text. This document serves as the "source of truth" for the knowledge base, allowing the supervisor agent to answer policy questions directly.
    ```text
    HR Onboarding and Hardware Policy - v4.0

    Section 1: Standard Hardware Packages by Role

    1.1 Software Engineer:
       - Laptop: 16-inch MacBook Pro M3 (or equivalent high-performance laptop)
       - Monitor: 32-inch 4K Display
       - Peripherals: Mechanical Keyboard, Ergonomic Mouse
       - Access: Full Admin rights on local machine.

    1.2 Marketing Manager:
       - Laptop: 13-inch MacBook Air
       - Monitor: 27-inch external monitor
       - Peripherals: Standard Wireless Keyboard and Mouse
       - Access: Standard user rights.

    1.3 Sales Representative:
       - Laptop: 14-inch Lenovo ThinkPad
       - Monitor: None (Portable monitor available upon request)
       - Peripherals: High-Quality Wireless Headset

    Section 2: Required Training Courses

    2.1 All New Hires (Mandatory within first 30 days):
        - "New Hire Security Awareness Training" (Course ID: SEC101)
        - "Corporate Code of Conduct" (Course ID: CND101)

    2.2 Engineering Department:
        - "Introduction to Engineering Practices" (Course ID: ENG201)

    2.3 Sales Department:
        - "CRM Best Practices and Usage" (Course ID: SLS201)
    ```
3.  **Install Dependencies:** Open your terminal, navigate to the project's root directory, and run the following command to install the required packages.
    ```bash
    pip install -r requirements.txt
    ```

### Step 3.2: Develop Python Tools

Here, we will create the Python tools that our collaborator agents will use to perform actions. These tools simulate interactions with external enterprise systems by generating realistic, structured synthetic data. Each tool's docstring is critically important, as it serves as the description the LLM uses to understand the tool's function, arguments, and return value.

#### **IT ServiceNow Tools (`tools/it_tools.py`)**

This module contains tools for managing IT service requests, simulating a ServiceNow environment. The `IT_ServiceNow_Agent` will use these to provision hardware and track support tickets. This demonstrates how Orchestrate can automate core IT helpdesk functions, reducing manual effort and ensuring consistency. The tools generate structured JSON data, which is a best practice for providing predictable, parsable output to the agent.

# Script block 2
orchestrate tools import -k python -f tools/it_tools.py
    orchestrate tools import -k python -f tools/identity_tools.py
    orchestrate tools import -k python -f tools/lms_tools.py
    ```

2.  **Import the knowledge base:** This command initiates the ingestion process for the PDF document.
    ```bash
    orchestrate knowledge-bases import -f knowledge_bases/hr_policy_kb.yaml
    ```

3.  **Import the collaborator agents:** This registers the specialized agents and links them to their respective tools.
    ```bash
    orchestrate agents import -f agents/IT_ServiceNow_Agent.yaml
    orchestrate agents import -f agents/Identity_Okta_Agent.yaml
    orchestrate agents import -f agents/LMS_Enrollment_Agent.yaml
    ```

4.  **Import the supervisor agent:** This final step registers the main agent and links it to its collaborators and knowledge base.
    ```bash
    orchestrate agents import -f agents/EmployeeLifecycle_Supervisor.yaml
    ```

## 4. Verification and Demo Scenarios

After successfully importing all assets, start the interactive chat to test the demo scenarios and verify the end-to-end functionality.

**Start the chat environment:**

