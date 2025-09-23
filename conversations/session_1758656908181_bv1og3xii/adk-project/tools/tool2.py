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