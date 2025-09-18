import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool(name="get_hr_form_link", description="Finds the URL for a specific HR document or form.")
def get_hr_form_link(form_name: str) -> str:
    """Searches the HR document directory to find a direct link to a requested form.

    Args:
        form_name (str): The name of the HR form to find, for example 'direct deposit' or 'W-4'.

    Returns:
        str: A message containing the link to the form, or a message indicating the form was not found.
    """
    try:
        with open('mock_data/hr_forms.json', 'r') as f:
            data = json.load(f)
        
        query = form_name.lower()
        
        for form in data['forms']:
            # Check against the main name and a list of keywords for better matching
            if query in form['form_name'].lower() or any(keyword in query for keyword in form['keywords']):
                return f"You can find the '{form['form_name']}' here: {form['url']}"

        return f"I'm sorry, I couldn't find a form matching '{form_name}'. Please try a different name or check the partner hub."

    except FileNotFoundError:
        return "Error: The HR forms directory could not be accessed. Please contact support."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"