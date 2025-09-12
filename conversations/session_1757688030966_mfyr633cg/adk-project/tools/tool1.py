import json
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class OperationalStatus(str, Enum):
    OPTIMAL = "optimal"
    WARNING = "warning"
    CRITICAL = "critical"
    MAINTENANCE = "maintenance"


class AlertPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@tool(name="store_status_dashboard", permission=ToolPermission.READ_ONLY)
def store_status_dashboard(store_id: str) -> str:
    """Provides a comprehensive real-time dashboard of store operational status.
    
    This tool aggregates data from all operational domains including inventory levels,
    staffing coverage, equipment health, and training compliance to provide a holistic
    view of store operations. It helps managers and partners quickly identify areas
    requiring attention and make informed operational decisions.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        
    Returns:
        str: JSON string containing comprehensive store status including operational metrics,
             alerts, and recommendations
    """
    try:
        current_time = datetime.now()
        
        # Generate realistic store status data
        status_data = {
            "store_id": store_id,
            "timestamp": current_time.isoformat(),
            "overall_status": random.choice([OperationalStatus.OPTIMAL, OperationalStatus.WARNING]),
            "operational_metrics": {
                "inventory": {
                    "status": random.choice([OperationalStatus.OPTIMAL, OperationalStatus.WARNING]),
                    "critical_items": random.randint(0, 3),
                    "total_skus": 523,
                    "items_below_threshold": random.randint(5, 15),
                    "pending_orders": random.randint(2, 5)
                },
                "staffing": {
                    "status": OperationalStatus.OPTIMAL,
                    "current_coverage": random.randint(85, 100),
                    "partners_on_duty": random.randint(4, 8),
                    "next_shift_coverage": random.randint(90, 100),
                    "open_shift_swaps": random.randint(0, 2)
                },
                "equipment": {
                    "status": random.choice([OperationalStatus.OPTIMAL, OperationalStatus.WARNING]),
                    "machines_operational": f"{random.randint(95, 100)}%",
                    "maintenance_due": random.randint(0, 2),
                    "active_issues": random.randint(0, 1)
                },
                "training": {
                    "status": OperationalStatus.OPTIMAL,
                    "compliance_rate": f"{random.randint(92, 100)}%",
                    "certifications_expiring": random.randint(0, 3),
                    "new_partners_in_training": random.randint(0, 2)
                }
            },
            "recent_alerts": [
                {
                    "timestamp": (current_time - timedelta(hours=2)).isoformat(),
                    "type": "inventory",
                    "message": "Oat milk inventory approaching minimum threshold",
                    "priority": "medium"
                },
                {
                    "timestamp": (current_time - timedelta(hours=5)).isoformat(),
                    "type": "equipment",
                    "message": "Espresso machine #2 maintenance recommended",
                    "priority": "low"
                }
            ],
            "recommendations": [
                "Consider ordering additional oat milk for weekend demand",
                "Schedule espresso machine maintenance during slow period tomorrow",
                "Review next week's schedule for adequate morning coverage"
            ]
        }
        
        return json.dumps(status_data, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to generate store status: {str(e)}"})


@tool(name="priority_alert_generator", permission=ToolPermission.ADMIN)
def priority_alert_generator(
    store_id: str, 
    time_window_hours: int = 24, 
    min_priority: AlertPriority = AlertPriority.MEDIUM
) -> str:
    """Generates prioritized alerts for store operations requiring immediate attention.
    
    This tool analyzes operational data across all domains to identify and prioritize
    issues that could impact customer service or store operations. It uses intelligent
    algorithms to determine alert priority based on potential business impact, time
    sensitivity, and available resources. This enables partners to focus on the most
    critical issues first.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        time_window_hours (int): Number of hours to look back for alerts (default: 24)
        min_priority (AlertPriority): Minimum priority level to include (default: MEDIUM)
        
    Returns:
        str: JSON string containing prioritized alerts with recommended actions
    """
    try:
        current_time = datetime.now()
        
        # Generate realistic priority alerts
        alert_templates = [
            {
                "domain": "inventory",
                "alerts": [
                    ("Milk products critically low - 2 hours supply remaining", AlertPriority.CRITICAL),
                    ("Caramel syrup below reorder threshold", AlertPriority.HIGH),
                    ("Napkins running low, reorder recommended", AlertPriority.MEDIUM),
                    ("Seasonal cups inventory at 60%", AlertPriority.LOW)
                ]
            },
            {
                "domain": "staffing",
                "alerts": [
                    ("No shift supervisor scheduled for tomorrow morning", AlertPriority.CRITICAL),
                    ("3 partners called out for evening shift", AlertPriority.HIGH),
                    ("Next week schedule has coverage gaps", AlertPriority.MEDIUM),
                    ("Partner certification expiring in 30 days", AlertPriority.LOW)
                ]
            },
            {
                "domain": "equipment",
                "alerts": [
                    ("Espresso machine #1 showing error codes", AlertPriority.CRITICAL),
                    ("Blender #2 vibration exceeding normal range", AlertPriority.HIGH),
                    ("Ice machine efficiency dropped 20%", AlertPriority.MEDIUM),
                    ("Oven timer calibration recommended", AlertPriority.LOW)
                ]
            },
            {
                "domain": "training",
                "alerts": [
                    ("New partner hasn't completed food safety training", AlertPriority.HIGH),
                    ("5 partners missing seasonal beverage training", AlertPriority.MEDIUM),
                    ("Annual compliance training due for 3 partners", AlertPriority.MEDIUM),
                    ("New recipe cards available for download", AlertPriority.LOW)
                ]
            }
        ]
        
        # Generate alerts based on priority filter
        generated_alerts = []
        priority_values = {
            AlertPriority.LOW: 1,
            AlertPriority.MEDIUM: 2,
            AlertPriority.HIGH: 3,
            AlertPriority.CRITICAL: 4
        }
        
        min_priority_value = priority_values[min_priority]
        
        for domain_data in alert_templates:
            domain = domain_data["domain"]
            for alert_text, priority in domain_data["alerts"]:
                if priority_values[priority] >= min_priority_value and random.random() > 0.5:
                    alert_time = current_time - timedelta(
                        hours=random.randint(0, time_window_hours),
                        minutes=random.randint(0, 59)
                    )
                    
                    alert = {
                        "alert_id": f"ALT-{random.randint(10000, 99999)}",
                        "timestamp": alert_time.isoformat(),
                        "domain": domain,
                        "priority": priority,
                        "message": alert_text,
                        "impact": _get_impact_description(priority),
                        "recommended_action": _get_recommended_action(domain, priority),
                        "estimated_resolution_time": f"{random.randint(10, 120)} minutes"
                    }
                    generated_alerts.append(alert)
        
        # Sort alerts by priority and timestamp
        generated_alerts.sort(
            key=lambda x: (priority_values[x["priority"]], x["timestamp"]), 
            reverse=True
        )
        
        response = {
            "store_id": store_id,
            "generated_at": current_time.isoformat(),
            "time_window_hours": time_window_hours,
            "total_alerts": len(generated_alerts),
            "alerts_by_priority": {
                "critical": len([a for a in generated_alerts if a["priority"] == AlertPriority.CRITICAL]),
                "high": len([a for a in generated_alerts if a["priority"] == AlertPriority.HIGH]),
                "medium": len([a for a in generated_alerts if a["priority"] == AlertPriority.MEDIUM]),
                "low": len([a for a in generated_alerts if a["priority"] == AlertPriority.LOW])
            },
            "alerts": generated_alerts[:10]  # Return top 10 alerts
        }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to generate priority alerts: {str(e)}"})


def _get_impact_description(priority: AlertPriority) -> str:
    """Generate impact description based on priority.
    
    Args:
        priority (AlertPriority): The alert priority level
        
    Returns:
        str: Description of the potential impact
    """
    impacts = {
        AlertPriority.CRITICAL: "Immediate impact on customer service and operations",
        AlertPriority.HIGH: "Significant impact on operations within 2-4 hours",
        AlertPriority.MEDIUM: "Moderate impact on efficiency and service quality",
        AlertPriority.LOW: "Minor impact, preventive action recommended"
    }
    return impacts.get(priority, "Unknown impact")


def _get_recommended_action(domain: str, priority: AlertPriority) -> str:
    """Generate recommended action based on domain and priority.
    
    Args:
        domain (str): The operational domain (inventory, staffing, equipment, training)
        priority (AlertPriority): The alert priority level
        
    Returns:
        str: Recommended action to resolve the alert
    """
    if priority == AlertPriority.CRITICAL:
        return "Immediate action required - escalate to shift supervisor"
    elif priority == AlertPriority.HIGH:
        return f"Address within 1 hour - coordinate with {domain} team"
    elif priority == AlertPriority.MEDIUM:
        return f"Plan resolution within current shift"
    else:
        return "Schedule for next available opportunity"