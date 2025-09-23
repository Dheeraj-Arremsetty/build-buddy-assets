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