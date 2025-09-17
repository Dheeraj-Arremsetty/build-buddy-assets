import os
import csv
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="create_contract_draft", permission=ToolPermission.ADMIN)
def create_contract_draft(company_name: str) -> str:
    """
    Creates a draft Master Service Agreement (MSA) for a given company using a standard template.
    It fetches company details from a central CSV file and populates the template.

    Args:
        company_name (str): The exact name of the company for the contract (e.g., 'Innovate Inc.').

    Returns:
        str: A confirmation message with the path to the saved draft document, or an error message if the company is not found.
    """
    vendor_file = 'mock_data/vendors.csv'
    template_file = 'mock_data/templates/MSA_Template.txt'
    output_dir = 'drafts'
    
    company_data = None
    try:
        with open(vendor_file, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['company_name'] == company_name:
                    company_data = row
                    break
        
        if not company_data:
            return f"Error: Company '{company_name}' not found in vendors list."

        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Replace placeholders
        draft_content = template_content.replace('{{company_name}}', company_data['company_name'])
        draft_content = draft_content.replace('{{msa_type}}', company_data['msa_type'])

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        file_name = f"{company_name.replace(' ', '_').replace('.', '')}_MSA.txt"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(draft_content)
            
        return f"Successfully created draft contract at '{file_path}'"

    except FileNotFoundError as e:
        return f"Error: A required file was not found: {e.filename}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"