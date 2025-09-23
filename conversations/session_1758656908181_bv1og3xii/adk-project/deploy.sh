#!/bin/bash
# Generated deployment script

# Script block 1
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

# Script block 2
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

