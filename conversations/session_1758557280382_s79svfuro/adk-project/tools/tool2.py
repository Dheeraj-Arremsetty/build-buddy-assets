import json
        import random
        from datetime import datetime
        from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

        @tool(name="create_incident", permission=ToolPermission.ADMIN)
        def create_incident(description: str, severity: int = 3) -> str:
            """
            Creates a new incident ticket in ServiceNow based on a user's report.

            This tool is the primary action for formalizing an IT issue. By automating ticket creation, it ensures that all necessary information is captured consistently and that the issue is entered into the formal support queue for tracking and resolution, freeing up help desk staff from manual data entry.

            Args:
                description (str): A detailed description of the issue.
                severity (int, optional): The priority level of the incident (1=Critical, 2=High, 3=Medium). Defaults to 3.

            Returns:
                str: A JSON string confirming the creation with the new incident number.
            """
            incident_number = f"INC{random.randint(1000000, 9999999)}"
            response = {
                "result": {
                    "incident_number": incident_number,
                    "status": "New",
                    "message": "Incident created successfully."
                }
            }
            return json.dumps(response, indent=2)

        @tool(name="get_incident_status", permission=ToolPermission.ADMIN)
        def get_incident_status(incident_number: str) -> str:
            """
            Retrieves the current status, assignee, and work notes for a given ServiceNow incident number.

            This tool provides on-demand transparency into the support process. It empowers both end-users and managers to self-serve status updates, reducing the number of follow-up inquiries to the help desk and providing clear visibility into the resolution progress.

            Args:
                incident_number (str): The unique incident number (e.g., 'INC0012345').

            Returns:
                str: A JSON string with the incident's current details.
            """
            statuses = ["New", "In Progress", "On Hold", "Resolved"]
            assignees = ["WebOps Team", "Database Admins", "Network Engineering", "Jane Doe"]
            response = {
                "incident_number": incident_number,
                "status": random.choice(statuses),
                "assigned_to": random.choice(assignees),
                "last_updated": datetime.utcnow().isoformat(),
                "work_notes": "Investigation is ongoing. Engineering team is analyzing logs."
            }
            return json.dumps(response, indent=2)

        @tool(name="update_incident_with_logs", permission=ToolPermission.ADMIN)
        def update_incident_with_logs(incident_number: str, logs: str) -> str:
            """
            Updates an existing ServiceNow incident with additional information, such as performance logs.

            This tool is a critical component of the AIOps workflow, enabling the system to enrich tickets with new information as it becomes available. Attaching logs directly to the ticket ensures that engineers have all the context they need in one place, which is fundamental to accelerating resolution times.

            Args:
                incident_number (str): The incident number to update.
                logs (str): The log data to be added to the incident's work notes.

            Returns:
                str: A JSON string confirming that the incident was updated.
            """
            response = {
                "incident_number": incident_number,
                "status": "Success",
                "message": f"Successfully updated incident {incident_number} with new logs."
            }
            return json.dumps(response, indent=2)