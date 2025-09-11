#!/bin/bash
# Generated deployment script

# Script block 1
pip install -r requirements.txt
    ```

## 3. Step-by-Step Instructions

### Step 1: Create Mock Data and Policy Documents

First, we will create the synthetic data sources that our tools will interact with. This data simulates CorePower Yoga's operational databases and policy documents.

#### A. Create Teacher Roster (`teachers.json`)

This file contains a list of instructors, their certifications, and their availability to sub.

**File: `data/teachers.json`**

# Script block 2
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

