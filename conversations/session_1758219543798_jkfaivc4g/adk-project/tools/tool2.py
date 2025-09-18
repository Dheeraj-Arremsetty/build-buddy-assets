from datetime import datetime
    from typing import List
    from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

    # Mock class schedule data
    mock_schedule = [
        {"class_id": "C2-0900-DEN", "class_name": "C2 - CorePower 2", "instructor": "Jenna", "time": "09:00", "location": "Denver", "spots_available": 5},
        {"class_id": "YS-1200-DEN", "class_name": "YS - Yoga Sculpt", "instructor": "Mike", "time": "12:00", "location": "Denver", "spots_available": 10},
        {"class_id": "C2-1730-DEN", "class_name": "C2 - CorePower 2", "instructor": "Chloe", "time": "17:30", "location": "Denver", "spots_available": 3},
        {"class_id": "HPF-1800-DEN", "class_name": "HPF - Hot Power Fusion", "instructor": "Sam", "time": "18:00", "location": "Denver", "spots_available": 8},
        {"class_id": "C2-1900-BOUL", "class_name": "C2 - CorePower 2", "instructor": "Leo", "time": "19:00", "location": "Boulder", "spots_available": 0},
    ]

    @tool(permission=ToolPermission.ADMIN)
    def get_class_schedule(location: str, class_type: str = None, after_time: str = None) -> List[dict]:
        """
        Searches for available yoga classes based on location, class type, and time. Use this as the first step when a member wants to find a class.

        Args:
            location (str): The city to search for classes in (e.g., 'Denver').
            class_type (str, optional): The type of class to filter by (e.g., 'C2', 'Yoga Sculpt'). Defaults to None.
            after_time (str, optional): The earliest time for the class, in 'HH:MM' format (e.g., '17:00'). Defaults to None.

        Returns:
            List[dict]: A list of available classes matching the criteria.
        """
        results = []
        for cls in mock_schedule:
            loc_match = location.lower() in cls['location'].lower()
            type_match = not class_type or class_type.lower() in cls['class_name'].lower()
            time_match = not after_time or cls['time'] >= after_time
            
            if loc_match and type_match and time_match and cls['spots_available'] > 0:
                results.append(cls)
        return results

    @tool(permission=ToolPermission.ADMIN)
    def book_class(member_id: str, class_id: str) -> dict:
        """
        Books a member into a specific class using the class ID. Use this tool after the member has selected a class from the schedule.

        Args:
            member_id (str): The unique identifier for the member, e.g., 'CPY-1001'.
            class_id (str): The unique identifier for the class, e.g., 'C2-1730-DEN'.

        Returns:
            dict: A confirmation of the booking or an error message.
        """
        for cls in mock_schedule:
            if cls['class_id'] == class_id:
                if cls['spots_available'] > 0:
                    # In a real scenario, you would decrement the spot count here.
                    return {
                        "status": "success",
                        "message": f"Booking confirmed for member {member_id} in class {cls['class_name']} with {cls['instructor']} at {cls['time']}."
                    }
                else:
                    return {"status": "error", "message": f"Sorry, class {class_id} is full."}
        return {"status": "error", "message": f"Class with ID {class_id} not found."}