# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-23 15:54:29
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: AI-Powered Talent Acquisition Co-Pilot

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the "AI-Orchestrated Recruitment Workflow: The IBM Talent Co-Pilot" using IBM watsonx Orchestrate. The solution is designed to address the client's need to significantly enhance recruiter efficiency and improve the quality of hires. By creating a multi-agent system, we will automate high-volume, repetitive tasks such as candidate sourcing, screening, and interview scheduling.

The core of this solution is a supervisor agent that orchestrates a team of specialized collaborator agents, each responsible for a distinct phase of the recruitment lifecycle. This architecture directly implements the client's proposed demo concept, leveraging a knowledge base of IBM's hiring policies to ensure compliance and strategic alignment. The final demo will showcase a 30-50% potential reduction in time-to-fill, improved screening consistency, and a superior candidate experience, demonstrating the tangible business value of watsonx Orchestrate.

## Prerequisites
Before beginning, ensure your environment is correctly configured.

1.  **Python Environment**: A working Python 3.9+ installation is required.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed.
    ```bash
    pip install "ibm-watsonx-orchestrate[all]"
    ```
3.  **Orchestrate Environment**: You must be logged into your watsonx Orchestrate environment via the CLI.
    ```bash
    orchestrate login
    ```
4.  **Project Directory**: Create a dedicated project folder to organize all assets. This structure is critical for a clean and manageable implementation.

    ```
    talent-copilot-demo/
    ├── agents/
    │   ├── recruitment_supervisor_agent.yaml
    │   ├── candidate_sourcing_agent.yaml
    │   ├── candidate_screening_agent.yaml
    │   └── interview_scheduling_agent.yaml
    ├── tools/
    │   ├── sourcing_tools.py
    │   ├── screening_tools.py
    │   └── scheduling_tools.py
    ├── knowledge_bases/
    │   └── ibm_hiring_guidelines_kb.yaml
    ├── mock_data/
    │   └── policies/
    │       ├── IBM_Leadership_Principles.pdf
    │       └── Diversity_in_Hiring.docx
    └── requirements.txt
    ```

## Step 1: Create Mock Data and Knowledge Base
The foundation of a compelling demo is realistic data. First, we will create the mock policy documents that will populate our knowledge base.

1.  **Create Mock Policy Documents**: Inside the `mock_data/policies/` directory, create two files:
    *   `IBM_Leadership_Principles.pdf`: A PDF document containing text about IBM's leadership values, such as "Dedication to every client's success," "Innovation that matters," and "Trust and personal responsibility in all relationships."
    *   `Diversity_in_Hiring.docx`: A Word document outlining IBM's commitment to diversity, equity, and inclusion in the hiring process. Include points about unbiased screening and diverse interview panels.

2.  **Define the Knowledge Base Configuration**:
    The knowledge base will provide the `Candidate_Screening_Agent` with IBM's official hiring guidelines, enabling Retrieval-Augmented Generation (RAG) for policy-aware candidate evaluation. This ensures that screening is not only skill-based but also aligned with corporate values.

    Create the file `knowledge_bases/ibm_hiring_guidelines_kb.yaml` with the following content. This configuration points to our mock documents and uses a built-in Milvus vector store for ingestion.

    ```yaml
    # knowledge_bases/ibm_hiring_guidelines_kb.yaml
    spec_version: v1
    kind: knowledge_base 
    name: ibm_hiring_guidelines_kb
    description: >
      Contains official IBM documents regarding hiring policies, diversity and inclusion goals, 
      and core leadership competencies for candidate evaluation. This knowledge base is used to
      ensure all candidate screening is compliant and aligned with IBM's strategic goals.
    documents:
      - "mock_data/policies/IBM_Leadership_Principles.pdf"
      - "mock_data/policies/Diversity_in_Hiring.docx"
    vector_index:
      embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
    ```

## Step 2: Develop the Python Tools
Tools are the building blocks that allow agents to interact with systems and perform actions. We will create three Python files, each containing tools for a specific recruitment function.

### 2.1 Sourcing Tools
These tools simulate searching for candidates in internal and external systems.

**Business Value**: Automates the time-consuming top-of-funnel activity of finding potential candidates, allowing recruiters to focus on engagement rather than manual searches.
**Technical Implementation**: These Python functions generate realistic, synthetic candidate data, mimicking responses from an Applicant Tracking System (ATS) and external job boards.

Create the file `tools/sourcing_tools.py`:
```python
# tools/sourcing_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import List, Dict

@tool
def search_internal_ats(job_id: str) -> List[Dict]:
    """
    Searches the internal Applicant Tracking System (ATS) for candidates matching a specific job ID.

    Args:
        job_id (str): The unique identifier for the job requisition (e.g., '8921').

    Returns:
        List[Dict]: A list of candidate profiles found in the internal ATS. Each profile is a dictionary.
    """
    print(f"Searching internal ATS for job ID: {job_id}...")
    # Mock data simulating an internal ATS response
    internal_candidates = [
        {"candidate_id": "ATS_001", "name": "Jane Doe", "current_role": "Senior Consultant", "skills": ["Agile", "Project Management", "Client Relations"], "source": "Internal"},
        {"candidate_id": "ATS_002", "name": "Michael Roe", "current_role": "Cloud Engineer", "skills": ["AWS", "Azure", "CI/CD"], "source": "Internal"}
    ]
    return internal_candidates

@tool
def search_external_job_boards(keywords: str) -> List[Dict]:
    """
    Searches external job boards like LinkedIn for candidates based on keywords.

    Args:
        keywords (str): A comma-separated string of keywords to search for (e.g., 'Cloud Architect, Kubernetes, OpenShift').

    Returns:
        List[Dict]: A list of candidate profiles found on external platforms.
    """
    print(f"Searching external job boards with keywords: {keywords}...")
    # Mock data simulating an external search response
    external_candidates = [
        {"candidate_id": "EXT_101", "name": "John Smith", "current_role": "Lead Cloud Architect", "skills": ["Kubernetes", "Red Hat OpenShift", "Ansible", "Terraform"], "source": "LinkedIn"},
        {"candidate_id": "EXT_102", "name": "Priya Singh", "current_role": "Solutions Architect", "skills": ["Kubernetes", "Hybrid Cloud", "Go"], "source": "External Board"}
    ]
    return external_candidates
```

### 2.2 Screening Tools
This tool analyzes a candidate's resume against a job description.

**Business Value**: Standardizes the initial screening process, reduces unconscious bias, and quickly identifies top candidates based on objective criteria, saving significant recruiter time.
**Technical Implementation**: This function takes resume and job description text as input and returns a structured analysis, including a match score and a summary of strengths and weaknesses.

Create the file `tools/screening_tools.py`:
```python
# tools/screening_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def analyze_resume_against_jd(resume_text: str, job_description: str) -> dict:
    """
    Analyzes a candidate's resume against a job description and provides a match score.

    Args:
        resume_text (str): The full text of the candidate's resume.
        job_description (str): The full text of the job description.

    Returns:
        dict: A dictionary containing a match score, a summary of strengths, 
              and a list of potential gaps.
    """
    print(f"Analyzing resume against job description...")
    # Mock analysis logic
    score = 85
    summary = "Strong match in cloud technologies, especially Kubernetes and Red Hat OpenShift. Candidate demonstrates leadership experience in past projects."
    gaps = ["Lacks specific experience with Ansible automation.", "Project management certification not listed."]
    
    return {"score": score, "summary": summary, "gaps": gaps}
```

### 2.3 Scheduling Tools
These tools handle the logistics of setting up interviews.

**Business Value**: Eliminates the back-and-forth communication typically required for interview scheduling, accelerating the hiring process and improving the experience for both candidates and hiring managers.
**Technical Implementation**: These functions simulate checking a calendar API for availability and sending a formatted meeting invitation.

Create the file `tools/scheduling_tools.py`:
```python
# tools/scheduling_tools.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import List, Dict
import datetime

@tool
def get_interviewer_availability(interviewer_name: str) -> List[Dict]:
    """
    Checks the calendar for an interviewer's availability for the upcoming week.

    Args:
        interviewer_name (str): The name of the interviewer (e.g., 'Sarah Jenkins').

    Returns:
        List[Dict]: A list of available time slots.
    """
    print(f"Checking calendar availability for {interviewer_name}...")
    # Mock data simulating calendar API response for the next 5 business days
    today = datetime.date.today()
    availability = []
    for i in range(1, 6):
        day = today + datetime.timedelta(days=i)
        if day.weekday() < 5: # Monday to Friday
            availability.append({"date": day.strftime('%Y-%m-%d'), "time": "10:00 AM", "duration_minutes": 60})
            availability.append({"date": day.strftime('%Y-%m-%d'), "time": "02:30 PM", "duration_minutes": 45})
    return availability

@tool
def send_interview_invite(candidate_name: str, interviewer_name: str, date: str, time: str, duration: int) -> Dict:
    """
    Sends a calendar invitation for an interview.

    Args:
        candidate_name (str): The name of the candidate.
        interviewer_name (str): The name of the interviewer.
        date (str): The date of the interview (YYYY-MM-DD).
        time (str): The time of the interview (e.g., '10:00 AM').
        duration (int): The duration of the interview in minutes.

    Returns:
        Dict: A confirmation message indicating the interview was scheduled.
    """
    print(f"Sending interview invite to {candidate_name} with {interviewer_name}...")
    return {
        "status": "Success",
        "message": f"Interview scheduled for {candidate_name} with {interviewer_name} on {date} at {time} for {duration} minutes. Invitation sent."
    }
```

### 2.4 Create `requirements.txt`
This file lists any Python packages your tools depend on. For this demo, we'll include `requests` as a best practice, even though our current tools don't make live API calls.

Create the file `requirements.txt`:
```
requests
```

## Step 3: Define the Agent Configurations
With the tools and knowledge base defined, we can now configure our agents. Each agent is defined in a separate YAML file, specifying its name, description, instructions, and capabilities.

### 3.1 Candidate Sourcing Agent
This agent's sole purpose is to find candidates using the sourcing tools.

Create `agents/candidate_sourcing_agent.yaml`:
```yaml
# agents/candidate_sourcing_agent.yaml
spec_version: v1
kind: native
name: candidate_sourcing_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that specializes in finding potential job candidates. It can search both internal IBM 
  Applicant Tracking Systems (ATS) and external sources like LinkedIn to build a candidate pipeline.
instructions: >
  Your purpose is to find candidates for a given job role. Use the search_internal_ats tool to find
  candidates within IBM's systems. Use the search_external_job_boards tool to find candidates
  from outside sources. Combine the results from both tools to provide a comprehensive list.
tools:
  - search_internal_ats
  - search_external_job_boards
```

### 3.2 Candidate Screening Agent
This agent analyzes resumes and leverages the knowledge base for policy-aware evaluation.

Create `agents/candidate_screening_agent.yaml`:
```yaml
# agents/candidate_screening_agent.yaml
spec_version: v1
kind: native
name: candidate_screening_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent that screens and evaluates candidates. It analyzes resumes against job descriptions
  and uses its knowledge of IBM's hiring policies and leadership principles to ensure alignment.
instructions: >
  Your purpose is to screen candidates. Use the analyze_resume_against_jd tool to get a baseline
  match score. When asked about alignment with IBM principles or policies, you MUST use the
  knowledge base to find relevant information and incorporate it into your summary.
tools:
  - analyze_resume_against_jd
knowledge_base:
  - ibm_hiring_guidelines_kb
```

### 3.3 Interview Scheduling Agent
This agent handles all interview coordination tasks.

Create `agents/interview_scheduling_agent.yaml`:
```yaml
# agents/interview_scheduling_agent.yaml
spec_version: v1
kind: native
name: interview_scheduling_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An agent specializing in interview logistics. It can check interviewer availability on their
  calendars and send out official interview invitations to candidates and the hiring team.
instructions: >
  Your purpose is to schedule interviews. First, use the get_interviewer_availability tool to
  find open slots. After a slot is confirmed, use the send_interview_invite tool to create and
  send the calendar event.
tools:
  - get_interviewer_availability
  - send_interview_invite
```

### 3.4 Recruitment Supervisor Agent
This is the master agent that orchestrates the entire workflow. It takes high-level commands from the recruiter and delegates tasks to the appropriate collaborator agents. Its power comes from its instructions and its list of collaborators.

Create `agents/recruitment_supervisor_agent.yaml`:
```yaml
# agents/recruitment_supervisor_agent.yaml
spec_version: v1
kind: native
name: recruitment_supervisor_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
  An AI co-pilot for IBM Talent Acquisition. It orchestrates the entire recruitment workflow, 
  including sourcing, screening, and scheduling, by collaborating with specialized agents. 
  This is the primary agent for recruiters to interact with.
instructions: >
  You are an AI co-pilot for IBM recruiters. Your goal is to make the hiring process faster and more efficient.
  - When a user asks you to FIND or SOURCE candidates, you MUST delegate the task to the candidate_sourcing_agent.
  - When a user asks you to SCREEN, RANK, ANALYZE, or REVIEW a candidate or resume, you MUST delegate the task to the candidate_screening_agent.
  - When a user asks you to SCHEDULE or SETUP an interview, you MUST delegate the task to the interview_scheduling_agent.
  - Synthesize the responses from your collaborators into a clear, concise answer for the recruiter.
collaborators:
  - candidate_sourcing_agent
  - candidate_screening_agent
  - interview_scheduling_agent
```

## Step 4: Deploy the Multi-Agent System
With all assets created, we will now deploy them to watsonx Orchestrate using the ADK CLI. The order of operations is important: tools and knowledge bases must be imported before the agents that depend on them.

Execute these commands in your terminal from the root of your `talent-copilot-demo` directory.

```bash
# 1. Import all Python tools
echo "Importing Sourcing Tools..."
orchestrate tools import -f tools/sourcing_tools.py

echo "Importing Screening Tools..."
orchestrate tools import -f tools/screening_tools.py

echo "Importing Scheduling Tools..."
orchestrate tools import -f tools/scheduling_tools.py

# 2. Import the knowledge base
echo "Importing Knowledge Base..."
orchestrate knowledge_bases import -f knowledge_bases/ibm_hiring_guidelines_kb.yaml

# 3. Import the collaborator agents
echo "Importing Collaborator Agents..."
orchestrate agents import -f agents/candidate_sourcing_agent.yaml
orchestrate agents import -f agents/candidate_screening_agent.yaml
orchestrate agents import -f agents/interview_scheduling_agent.yaml

# 4. Import the supervisor agent
echo "Importing Supervisor Agent..."
orchestrate agents import -f agents/recruitment_supervisor_agent.yaml

echo "Deployment complete!"
```

## Step 5: Verification and Demo Execution
Now, you can interact with your AI Talent Co-Pilot.

1.  **Start the Chat**: Run the following command to open an interactive chat session with your deployed agents.
    ```bash
    orchestrate chat start
    ```
2.  **Select the Supervisor**: When prompted, select `recruitment_supervisor_agent` as the agent you want to chat with.
3.  **Run Demo Scenarios**: Use the following prompts to test the full workflow and showcase the system's capabilities.

    *   **Scenario 1: End-to-End Sourcing & Screening**
        *   **Prompt**: `Find and rank the top candidates for job requisition #8921 (Cloud Solutions Architect).`
        *   **Expected Behavior**: The supervisor will first delegate to the `candidate_sourcing_agent`, which will use its tools to find internal and external candidates. Then, the supervisor will delegate to the `candidate_screening_agent` to analyze and rank them. The final output will be a consolidated list of candidates with their match scores.

    *   **Scenario 2: Policy-Aware Vetting (RAG)**
        *   **Prompt**: `Review Jane Doe's resume for the Senior Consultant role. Summarize how her experience aligns with IBM's leadership principles.`
        *   **Expected Behavior**: The supervisor will delegate to the `candidate_screening_agent`. This agent will query its `ibm_hiring_guidelines_kb` to retrieve information on leadership principles and use it to provide a nuanced, policy-aware response that goes beyond simple keyword matching.

    *   **Scenario 3: Automated Scheduling**
        *   **Prompt**: `Schedule a 45-minute technical screen for John Smith with Sarah Jenkins for next week.`
        *   **Expected Behavior**: The supervisor will delegate to the `interview_scheduling_agent`. It will first call the `get_interviewer_availability` tool, present the open slots, and upon confirmation, call the `send_interview_invite` tool to simulate sending the calendar invite.

## Troubleshooting
-   **Tool Not Found Error**: If an agent reports it cannot find a tool, ensure the tool was imported successfully using `orchestrate tools import`. Also, verify the tool name in the agent's YAML file matches the function name in the Python file exactly.
-   **Agent Not Found / Collaboration Error**: If the supervisor fails to delegate, confirm that all collaborator agents were imported successfully. Check the `collaborators` list in `recruitment_supervisor_agent.yaml` for typos.
-   **Knowledge Base Not Ready**: After importing the knowledge base, ingestion can take a few moments. Use `orchestrate knowledge-bases status --name ibm_hiring_guidelines_kb` to check if the `Ready` property is `true`.
-   **Incorrect Agent Routing**: If the supervisor delegates to the wrong agent, refine the `instructions` in its YAML file. Make the routing logic more explicit (e.g., "When the user says 'find candidates', you MUST use agent X").

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
