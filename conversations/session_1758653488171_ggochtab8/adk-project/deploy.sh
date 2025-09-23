#!/bin/bash
# Generated deployment script

# Script block 1
pip install ibm-watsonx-orchestrate
    ```
3.  **Orchestrate CLI Environment**: You must have an active watsonx Orchestrate environment configured. Initialize it using:
    ```bash
    orchestrate env init
    ```
4.  **Project Directory Structure**: Create the following folder structure to organize all assets for the demo. This is crucial for keeping the configuration files, tools, and mock data organized.

    ```
    onboarding_buddy_demo/
    ├── agents/
    │   ├── Onboarding_Buddy_Agent.yaml
    │   ├── IT_Support_Agent.yaml
    │   └── HR_Benefits_Agent.yaml
    ├── knowledge/
    │   └── onboarding_kb.yaml
    ├── mock_data/
    │   ├── IBM_Remote_Work_Policy.pdf
    │   ├── New_Hire_FAQ.csv
    │   └── Benefits_Guide_2024.docx
    ├── tools/
    │   ├── it_support_tools.py
    │   └── hr_benefits_tools.py
    └── requirements.txt
    ```

## Step 1: Prepare Mock Data and Knowledge Base

The Onboarding Buddy's ability to answer general questions relies on a knowledge base populated with relevant documents. We will create mock documents and a YAML configuration to define this knowledge base.

### 1.1 Create Mock Data Files

Create the three files inside the `mock_data/` directory. For the demo, you can create simple text files and save them with the correct extensions (`.pdf`, `.csv`, `.docx`).

*   **`IBM_Remote_Work_Policy.pdf` (Sample Content):**
    > IBM offers flexible remote and hybrid work arrangements. The standard dress code for client-facing video calls is business casual. For internal meetings, the dress code is relaxed. All remote work must be conducted from your registered home address.

*   **`New_Hire_FAQ.csv` (Sample Content):**
    ```csv
    Question,Answer
    "How do I get paid?","Payroll is processed bi-weekly. You can set up direct deposit in the internal HR portal."
    "Where is the main office?","The main campus is located at 123 Enterprise Drive, Armonk, NY."
    "What is the company culture like?","IBM fosters a culture of innovation, collaboration, and continuous learning."
    ```

*   **`Benefits_Guide_2024.docx` (Sample Content):**
    > **Health Plan Comparison:**
    > **PPO Plan:** Higher monthly premium, lower deductible. Offers flexibility to see specialists without a referral. Co-pays are fixed for most services.
    > **HDHP Plan:** Lower monthly premium, higher deductible. Often paired with a Health Savings Account (HSA) to save for medical expenses tax-free. You pay the full cost of services until the deductible is met.

### 1.2 Configure the Knowledge Base

The knowledge base configuration file tells Orchestrate which documents to ingest into its built-in Milvus vector database.

**File:** `knowledge/onboarding_kb.yaml`

This YAML file defines the `onboarding_knowledge_base`. It specifies the document paths and the embedding model used to create vector representations of the text, enabling semantic search. This is the core of the RAG pattern.

# Script block 2
# 1. Import the Python-based tools for both agents
echo "Importing IT Support tools..."
orchestrate tools import -f tools/it_support_tools.py

echo "Importing HR Benefits tools..."
orchestrate tools import -f tools/hr_benefits_tools.py

# 2. Import the knowledge base containing the mock onboarding documents
echo "Importing knowledge base..."
orchestrate knowledgebases import -f knowledge/onboarding_kb.yaml

# 3. Import the collaborator agents (these must exist before the supervisor can reference them)
echo "Importing collaborator agents..."
orchestrate agents import -f agents/IT_Support_Agent.yaml
orchestrate agents import -f agents/HR_Benefits_Agent.yaml

# 4. Import the main supervisor agent
echo "Importing supervisor agent..."
orchestrate agents import -f agents/Onboarding_Buddy_Agent.yaml

# 5. Start the chat interface to interact with the supervisor agent
echo "Starting chat with the Onboarding Buddy..."
orchestrate chat start --agent Onboarding_Buddy_Agent

