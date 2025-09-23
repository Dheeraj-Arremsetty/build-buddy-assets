# tools/hr_benefits_tools.py
import random
import datetime
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="get_benefit_plan_details", permission=ToolPermission.ADMIN)
def get_benefit_plan_details(plan_type: str = "all") -> str:
    """
    Retrieves detailed information and a comparison of available health benefit plans.

    Args:
        plan_type (str, optional): The specific plan to inquire about ('PPO' or 'HDHP'). Defaults to 'all' for a comparison.

    Returns:
        str: A JSON string containing the details of the requested health plan(s).
    """
    plans = {
        "PPO": {
            "plan_name": "Premium PPO Plan",
            "monthly_premium": "$550",
            "annual_deductible": "$1,000",
            "out_of_pocket_max": "$4,000",
            "primary_care_copay": "$25",
            "specialist_copay": "$50",
            "summary": "Offers flexibility to see any doctor without a referral. Higher premiums but lower out-of-pocket costs for services."
        },
        "HDHP": {
            "plan_name": "High-Deductible Health Plan (HDHP) with HSA",
            "monthly_premium": "$250",
            "annual_deductible": "$3,000",
            "out_of_pocket_max": "$6,000",
            "primary_care_copay": "100% covered after deductible",
            "specialist_copay": "100% covered after deductible",
            "summary": "Lower premiums and the ability to contribute to a tax-advantaged Health Savings Account (HSA). You pay more upfront until the deductible is met."
        }
    }
    if plan_type.upper() in plans:
        return json.dumps({plan_type.upper(): plans[plan_type.upper()]})
    return json.dumps(plans)

@tool(name="initiate_benefits_enrollment", permission=ToolPermission.ADMIN)
def initiate_benefits_enrollment(employee_id: str, chosen_plan: str) -> str:
    """
    Initiates the benefits enrollment process for a new employee.

    Args:
        employee_id (str): The unique ID of the employee to enroll.
        chosen_plan (str): The plan the employee has chosen (e.g., 'PPO' or 'HDHP').

    Returns:
        str: A confirmation message with a reference number for the enrollment.
    """
    if chosen_plan.upper() not in ["PPO", "HDHP"]:
        return "Error: Invalid plan selected. Please choose either 'PPO' or 'HDHP'."
    
    enrollment_ref = f"ENR{random.randint(100000, 999999)}"
    print(f"Initiating enrollment for {employee_id} into {chosen_plan.upper()} plan. Reference: {enrollment_ref}")
    
    return f"Enrollment process initiated for plan '{chosen_plan.upper()}'. Your confirmation number is {enrollment_ref}. You will receive an email from HR with the next steps."