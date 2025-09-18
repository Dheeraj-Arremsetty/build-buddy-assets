# tools/validation_tools.py
import re
from typing import List, Dict, Any
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(permission=ToolPermission.ADMIN)
def check_missing_values(records: List[Dict[str, Any]], column_name: str) -> List[Dict[str, Any]]:
    """
    Checks for missing or empty values in a specified column of the provided records.

    Args:
        records (List[Dict[str, Any]]): A list of records (dictionaries) to check.
        column_name (str): The name of the column to check for missing values.

    Returns:
        List[Dict[str, Any]]: A list of records that have a missing value in the specified column.
    """
    missing_records = []
    for record in records:
        if record.get(column_name) is None or str(record.get(column_name)).strip() == '':
            missing_records.append(record)
    return missing_records

@tool(permission=ToolPermission.ADMIN)
def validate_phone_number_format(phone_number: str) -> bool:
    """
    Checks if a phone number matches the standard corporate format (XXX) XXX-XXXX.

    Args:
        phone_number (str): The phone number string to validate.

    Returns:
        bool: True if the format is valid, False otherwise.
    """
    if not isinstance(phone_number, str):
        return False
    pattern = re.compile(r'^\(\d{3}\) \d{3}-\d{4}$')
    return bool(pattern.match(phone_number))

@tool(permission=ToolPermission.ADMIN)
def verify_against_rules(records: List[Dict[str, Any]], rule_description: str) -> List[Dict[str, Any]]:
    """
    Verifies records against a described data quality rule. Identifies records that violate the rule.

    Args:
        records (List[Dict[str, Any]]): The dataset to validate.
        rule_description (str): A natural language description of the rule to apply. e.g., 'Check for invalid phone number format'.

    Returns:
        List[Dict[str, Any]]: A list of records that violate the specified rule.
    """
    invalid_records = []
    if "phone number format" in rule_description.lower():
        for record in records:
            phone = record.get("PhoneNumber")
            if phone and not validate_phone_number_format(phone):
                invalid_records.append(record)
    elif "missing email" in rule_description.lower():
        return check_missing_values(records, "Email")
    # This logic can be expanded with more rules.
    else:
        return [{"error": f"Rule '{rule_description}' is not implemented."}]
        
    return invalid_records