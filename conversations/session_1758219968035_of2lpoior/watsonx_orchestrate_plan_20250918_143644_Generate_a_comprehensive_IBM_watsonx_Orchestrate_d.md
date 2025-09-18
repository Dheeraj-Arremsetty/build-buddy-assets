# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-18 14:36:44
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Studio Concierge AI

## Overview
This execution plan provides a comprehensive, step-by-step guide to building and deploying the **Studio Concierge AI**, an intelligent, multi-agent virtual assistant for a fitness and wellness studio client. The solution is designed to automate member services by intelligently handling inquiries and performing account actions. By leveraging a supervisor-collaborator agent architecture, the Studio Concierge AI will significantly reduce staff workload, provide 24/7 member support, and ensure consistent, accurate information delivery, positioning the studio as a modern, tech-forward brand.

This revised and complete plan addresses all components of the proposed architecture. The architecture consists of a primary `StudioConciergeAgent` (Supervisor) that triages user requests and delegates them to two specialized collaborator agents: the `PolicyAndScheduleAgent`, which answers informational questions using a knowledge base of studio documents, and the `MemberServicesAgent`, which executes transactional tasks like class bookings and profile updates using a set of custom tools. This plan details the creation of all required components, from knowledge base documents and Python tools to the agent YAML configurations, and provides complete code and commands for a successful implementation.

## Prerequisites
Before beginning, ensure your development environment is properly configured. This plan assumes you have a foundational understanding of Python and YAML.

1.  **Python and pip**: Ensure Python (version 3.9 or later) and its package manager, pip, are installed on your system.
2.  **IBM watsonx Orchestrate ADK**: The Agent Development Kit (ADK) must be installed. If not, install it using the following command:
    ```bash
    pip install "ibm-watsonx-orchestrate"
    ```
3.  **ADK Environment**: An active ADK environment must be configured. If you haven't done so, initialize your environment. This typically involves running `orchestrate init` and following the prompts to connect to your watsonx Orchestrate instance.
4.  **Text Editor/IDE**: A code editor such as Visual Studio Code is recommended for creating and editing Python and YAML files.

## Step 1: Project Setup and Knowledge Base Documents
First, we will establish a clean project structure and create the source documents for our knowledge base. This ensures the `PolicyAndScheduleAgent` has accurate, studio-approved information to answer member questions.

1.  Create a main project directory named `studio_concierge_project`.
2.  Inside this directory, create the following subdirectories: `agents`, `tools`, and `knowledge_base_docs`.
3.  Inside the `knowledge_base_docs` directory, create the following text files with the content below. These documents will serve as the foundation for our informational agent.

**File: `knowledge_base_docs/studio_policies.txt`**
```text
Studio Policies and Member Guidelines

Membership Cancellation Policy:
To cancel a membership, members must provide a written 30-day notice. An early termination fee of $150 applies if the cancellation occurs within the first 6 months of the contract. All requests should be emailed to billing@studiowellness.com.

Class Booking and Cancellation:
Members can book classes up to 7 days in advance via the app or our AI assistant. Cancellations must be made at least 4 hours before the class starts to avoid a $15 late cancellation fee. No-shows will be charged a $25 fee.

Guest Policy:
Members can bring a guest for a drop-in fee of $25 per class. The same guest is limited to 2 visits per month. All guests must sign a liability waiver upon arrival.
```

**File: `knowledge_base_docs/class_schedule.txt`**
```text
Weekly Class Schedule

Monday:
- 6:00 AM: Sunrise Vinyasa Yoga
- 12:00 PM: Midday HIIT Blast
- 6:00 PM: Powerlifting Foundations

Wednesday:
- 7:00 AM: Morning Zen Meditation
- 12:00 PM: Lunchtime Core Crusher
- 5:30 PM: Restorative Yoga

Friday:
- 6:00 AM: Full Body Strength Circuit
- 12:00 PM: Express Spin
- 6:00 PM: Wind Down Yin Yoga

Saturday:
- 9:00 AM: Weekend Warrior Bootcamp
- 11:00 AM: Advanced Pilates
```

**File: `knowledge_base_docs/faqs.txt`**
```text
Frequently Asked Questions (FAQs)

Q: Do you offer personal training?
A: Yes, we have a team of certified personal trainers. You can book a consultation through the front desk or our mobile app to get started.

Q: What amenities are included with membership?
A: All memberships include full access to our gym floor, all group classes, locker rooms with showers, and towel service.

Q: Is there parking available?
A: We offer validated parking for up to 2 hours in the adjacent parking garage. Please bring your parking ticket to the front desk for validation.
```

## Step 2: Create and Import the Knowledge Base
With the source documents ready, we will define a knowledge base in watsonx Orchestrate. This component will be used by the `PolicyAndScheduleAgent` to perform Retrieval-Augmented Generation (RAG), providing grounded answers from the studio's official documents.

1.  Inside the main `studio_concierge_project` directory, create a file named `studio_knowledge_base.yaml`.

**File: `studio_knowledge_base.yaml`**
```yaml
spec_version: v1
kind: knowledge_base 
name: studio_docs_kb
description: >
   Contains official studio information regarding class schedules, membership policies (cancellation, booking), guest rules, and frequently asked questions about amenities and services like personal training.
documents:
   - "knowledge_base_docs/studio_policies.txt"
   - "knowledge_base_docs/class_schedule.txt"
   - "knowledge_base_docs/faqs.txt"
vector_index:
   embeddings_model_name: ibm/slate-125m-english-rtrvr-v2
```

2.  Now, import this knowledge base into your watsonx Orchestrate environment using the ADK CLI. Run this command from the root of your `studio_concierge_project` directory.

```bash
orchestrate knowledge-bases import -f studio_knowledge_base.yaml
```
You should see a confirmation message that the knowledge base `studio_docs_kb` was successfully imported and the documents are being processed.

## Step 3: Create Python Tools for Member Services
Next, we will implement the tools required by the `MemberServicesAgent` to perform actions on behalf of the user. These tools simulate interactions with a studio's backend system, handling tasks like booking classes, canceling bookings, and updating member profiles. Each tool generates realistic synthetic data to provide a dynamic and convincing demo experience.

1.  Inside the `tools` directory, create a Python file named `member_tools.py`.

**File: `tools/member_tools.py`**
```python
import json
import random
import string
from datetime import datetime, timedelta
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

# --- Synthetic Data Store ---
# In a real application, this data would come from a database or API.
MEMBER_PROFILES = {
    "M-1001": {"name": "Alex Johnson", "email": "alex.j@email.com", "phone": "555-123-4567", "membership_level": "Premium"},
    "M-1002": {"name": "Brenda Smith", "email": "brenda.s@email.com", "phone": "555-987-6543", "membership_level": "Basic"},
}

CLASS_SCHEDULE = [
    "Sunrise Vinyasa Yoga", "Midday HIIT Blast", "Powerlifting Foundations

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
