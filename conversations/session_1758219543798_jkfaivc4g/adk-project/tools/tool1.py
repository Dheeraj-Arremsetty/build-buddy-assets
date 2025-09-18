import json
    from datetime import datetime, timedelta
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    MEMBER_DB_PATH = './mock_data/members.json'

    def _read_db():
        """Helper function to read the member database."""
        try:
            with open(MEMBER_DB_PATH, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_db(data):
        """Helper function to write to the member database."""
        with open(MEMBER_DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    @tool(permission=ToolPermission.ADMIN)
    def freeze_membership(member_id: str, duration_months: int) -> dict:
        """
        Freezes a member's account for a specified number of months. Use this tool when a member explicitly asks to pause or freeze their membership.

        Args:
            member_id (str): The unique identifier for the member, like 'CPY-1001'.
            duration_months (int): The number of months to freeze the membership for.

        Returns:
            dict: A confirmation message with the new status and the resume date.
        """
        members = _read_db()
        member_found = False
        for member in members:
            if member['member_id'] == member_id:
                member['membership_status'] = 'Frozen'
                # Calculate resume date for confirmation
                resume_date = datetime.now() + timedelta(days=30 * duration_months)
                member['billing_date'] = resume_date.strftime('%Y-%m-%d')
                member_found = True
                break
        
        if not member_found:
            return {"status": "error", "message": f"Member with ID {member_id} not found."}

        _write_db(members)
        return {
            "status": "success",
            "message": f"Membership for {member_id} has been successfully frozen for {duration_months} months. Billing will resume on {member['billing_date']}."
        }

    @tool(permission=ToolPermission.ADMIN)
    def get_billing_info(member_id: str) -> dict:
        """
        Retrieves the next billing date and plan type for a specific member. Use this when a member asks about their billing cycle or plan details.

        Args:
            member_id (str): The unique identifier for the member, like 'CPY-1001'.

        Returns:
            dict: The member's billing information or an error message if not found.
        """
        members = _read_db()
        for member in members:
            if member['member_id'] == member_id:
                return {
                    "status": "success",
                    "member_id": member['member_id'],
                    "plan_type": member['plan_type'],
                    "next_billing_date": member['billing_date'],
                    "membership_status": member['membership_status']
                }
        return {"status": "error", "message": f"Member with ID {member_id} not found."}