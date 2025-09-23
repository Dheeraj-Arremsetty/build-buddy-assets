import json
import random
import string
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

USER_DATA_FILE = 'data/users.json'

def _load_users():
    """Helper function to load user data from the JSON file."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def _save_users(users):
    """Helper function to save user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@tool(permission=ToolPermission.ADMIN)
def reset_user_password(email: str) -> str:
    """
    Resets the password for a user given their email address and generates a temporary password.

    Args:
        email (str): The email address of the user who needs a password reset.

    Returns:
        str: A confirmation message including a new temporary password, or an error message if the user is not found.
    """
    users = _load_users()
    user_found = False
    for user in users:
        if user['email'].lower() == email.lower():
            user_found = True
            # In a real scenario, this would trigger a secure reset flow.
            # For the demo, we generate and return a temporary password.
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user['account_status'] = 'active' # Resetting password often implies unlocking.
            _save_users(users)
            return f"Password for {email} has been successfully reset. The temporary password is: {temp_password}. Please change it upon first login."
    
    if not user_found:
        return f"Error: User with email {email} not found in the directory."

@tool(permission=ToolPermission.ADMIN)
def unlock_user_account(email: str) -> str:
    """
    Unlocks a user's account if it is currently in a 'locked' state.

    Args:
        email (str): The email address of the user whose account needs to be unlocked.

    Returns:
        str: A confirmation message that the account has been unlocked, or a message indicating its current status.
    """
    users = _load_users()
    for user in users:
        if user['email'].lower() == email.lower():
            if user['account_status'] == 'locked':
                user['account_status'] = 'active'
                _save_users(users)
                return f"The account for {email} has been successfully unlocked."
            else:
                return f"The account for {email} is already active."
    return f"Error: User with email {email} not found in the directory."