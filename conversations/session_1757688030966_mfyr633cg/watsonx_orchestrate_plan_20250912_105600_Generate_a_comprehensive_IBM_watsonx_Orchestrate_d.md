# IBM watsonx Orchestrate Execution Plan

**Generated:** 2025-09-12 10:56:00
**Question:** Generate a comprehensive IBM watsonx Orchestrate demo plan for this client
**Agent:** IBM watsonx Orchestrate Planner Agent

## Execution Plan

# IBM watsonx Orchestrate Execution Plan: Starbucks Store Operations Intelligence Platform

## Overview

This comprehensive execution plan implements a multi-agent AI system designed specifically for Starbucks store operations, serving as an intelligent digital assistant for partners (employees). The platform addresses critical operational challenges by automating administrative tasks, optimizing workforce management, predicting inventory needs, and providing real-time operational support. By leveraging IBM watsonx Orchestrate's powerful agent orchestration capabilities, this solution aims to reduce administrative overhead by 30%, accelerate partner onboarding by 40%, improve inventory accuracy by 25%, and provide 24/7 intelligent support to minimize operational disruptions.

The implementation utilizes a sophisticated agent architecture with four specialized agents working collaboratively: Inventory Intelligence Agent for stock management and demand prediction, Workforce Orchestration Agent for schedule optimization and shift management, Partner Training & Support Agent for policy guidance and interactive training, and Equipment Health Monitor Agent for predictive maintenance. Each agent is equipped with domain-specific tools and knowledge bases, creating a comprehensive operational ecosystem that transforms how Starbucks stores manage their daily operations while maintaining the high standards of customer service the brand is known for.

## Prerequisites

### Environment Setup Requirements

Before beginning the implementation, ensure you have the following components properly configured:

1. **IBM watsonx Orchestrate ADK Installation**: Install version 1.7.0 or later using pip. The ADK provides the complete toolkit for building, testing, and deploying agents with their associated tools and knowledge bases. This includes the command-line interface for managing all components and the local development server for testing.
   ```bash
   pip install ibm-watsonx-orchestrate==1.7.0
   ```

2. **Python Environment**: Set up Python 3.9 or later with a virtual environment to isolate dependencies. This ensures compatibility with all required libraries and prevents conflicts with other Python projects on your system.
   ```bash
   python -m venv starbucks-wxo-env
   source starbucks-wxo-env/bin/activate  # On Windows: starbucks-wxo-env\Scripts\activate
   ```

3. **Required Python Packages**: Install all necessary dependencies for the Starbucks-specific tools. These packages enable data processing, API interactions, and synthetic data generation capabilities.
   ```bash
   pip install requests pandas numpy python-dotenv pytz timezonefinder opencv-python
   ```

4. **Directory Structure**: Create an organized project structure to maintain all components. This structure facilitates easy navigation and management of the various agents, tools, and knowledge bases.
   ```bash
   mkdir -p starbucks-operations/{agents,tools,knowledge-bases,mock-data}
   cd starbucks-operations
   ```

5. **Environment Configuration**: Set up your watsonx Orchestrate environment with proper authentication. This involves configuring your API keys and endpoint URLs for both development and production environments.
   ```bash
   orchestrate environments init
   # Follow prompts to configure your environment
   ```

6. **Create requirements.txt**: Generate a requirements file for all Python dependencies needed by the tools. This ensures consistent environment setup across different deployment scenarios.
   ```bash
   cat > requirements.txt << EOF
   requests
   pandas
   numpy
   python-dotenv
   pytz
   timezonefinder
   opencv-python
   EOF
   ```

## Step 1: Create the Supervisor Agent Configuration

The Starbucks Operations Supervisor agent serves as the central orchestrator for all store operations, intelligently routing requests to specialized agents based on the nature of the task. This supervisor agent understands the context of partner requests and delegates to the appropriate specialized agent, whether it's for inventory management, scheduling, training, or equipment maintenance. By implementing a react-style architecture with comprehensive collaborator integration, this agent ensures seamless coordination across all operational domains while maintaining conversation context and providing proactive support for complex multi-step operations.

Create the file `agents/starbucks_operations_supervisor.yaml`:

```yaml
spec_version: v1
kind: native
name: starbucks_operations_supervisor
llm: watsonx/meta-llama/llama-3-2-90b-vision-instruct
style: react
description: >
    The Starbucks Operations Supervisor is an intelligent orchestration agent that serves as the primary interface for all store operational needs. 
    This agent coordinates between inventory management, workforce scheduling, partner training, and equipment maintenance systems to provide 
    comprehensive support for Starbucks partners. It understands natural language requests and intelligently routes them to specialized agents 
    while maintaining context and ensuring seamless task completion. The supervisor has access to real-time store data, predictive analytics, 
    and can handle complex multi-step operations that span across different operational domains.
instructions: >
    You are the digital operations assistant for Starbucks partners, designed to streamline store operations and enhance partner productivity.
    
    Phase 1 - Request Analysis: When receiving a request, first analyze its nature and urgency. Identify whether it relates to inventory, 
    scheduling, training, equipment, or requires multi-domain coordination. Prioritize urgent issues like equipment failures or critical 
    inventory shortages that could impact customer service.
    
    Phase 2 - Intelligent Routing: Based on your analysis, route requests to the appropriate specialized agent:
    - Use inventory_intelligence_agent for stock levels, demand predictions, supplier orders, and inventory alerts
    - Use workforce_orchestration_agent for schedule optimization, shift swaps, coverage analysis, and compliance checking
    - Use partner_training_agent for policy questions, training modules, recipe guidance, and onboarding support
    - Use equipment_health_agent for maintenance predictions, troubleshooting, equipment status, and service tickets
    
    Phase 3 - Context Maintenance: Maintain conversation context across agent interactions. When multiple agents are involved, 
    synthesize their responses into cohesive guidance. Track task completion and follow up on pending actions.
    
    Phase 4 - Proactive Support: Identify opportunities for proactive assistance. If a partner asks about inventory, also check 
    for upcoming promotions that might affect demand. When handling shift swaps, verify compliance with labor laws and partner certifications.
    
    Phase 5 - Communication Style: Always communicate in a helpful, efficient manner using Starbucks terminology. Be concise but thorough, 
    and provide step-by-step guidance when needed. Include relevant policy references and safety reminders when applicable.
collaborators:
    - inventory_intelligence_agent
    - workforce_orchestration_agent
    - partner_training_agent
    - equipment_health_agent
tools:
    - store_status_dashboard
    - priority_alert_generator
```

## Step 2: Create Specialized Agent Configurations

### Inventory Intelligence Agent

The Inventory Intelligence Agent revolutionizes how Starbucks stores manage their complex inventory of over 500 SKUs, including coffee beans, syrups, food items, and supplies. This agent leverages predictive analytics to forecast demand based on historical sales patterns, seasonal trends, and upcoming promotions, ensuring optimal stock levels while minimizing waste. By automating the reordering process and providing real-time alerts for potential shortages, this agent enables partners to focus on customer service rather than manual inventory management, directly contributing to the 25% improvement in inventory accuracy.

Create the file `agents/inventory_intelligence_agent.yaml`:

```yaml
spec_version: v1
kind: native
name: inventory_intelligence_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    The Inventory Intelligence Agent is a sophisticated inventory management system specifically designed for Starbucks store operations. 
    It manages over 500 SKUs including coffee beans, syrups, food items, and operational supplies through real-time tracking and predictive 
    analytics. The agent uses advanced demand forecasting algorithms that consider historical sales data, seasonal patterns, local events, 
    and promotional calendars to predict inventory needs up to two weeks in advance. It automatically generates supplier orders when stock 
    levels reach predetermined thresholds and provides intelligent alerts to prevent stockouts that could impact customer service. 
    The agent also tracks product expiration dates, manages waste reduction initiatives, and optimizes storage allocation.
instructions: >
    You are the Inventory Intelligence Agent responsible for maintaining optimal stock levels across all Starbucks products and supplies.
    
    Phase 1 - Real-Time Monitoring: Continuously monitor current inventory levels across all categories. Track high-velocity items like 
    popular syrups and milk products with increased frequency. Flag any items approaching minimum stock thresholds.
    
    Phase 2 - Demand Prediction: Analyze historical sales patterns, day-of-week trends, seasonal variations, and upcoming promotions 
    to forecast demand. Consider local factors like weather patterns and community events. Generate 7-day and 14-day demand forecasts.
    
    Phase 3 - Automated Ordering: When inventory reaches reorder points, automatically generate supplier orders. Consider lead times, 
    delivery schedules, and storage capacity. Optimize order quantities to balance availability with waste reduction.
    
    Phase 4 - Alert Generation: Proactively alert partners about potential issues: critical shortages, unusual demand spikes, 
    expiring products, or delivery delays. Provide actionable recommendations for each alert.
    
    Phase 5 - Reporting: Generate daily inventory reports highlighting key metrics, predicted shortages, and optimization opportunities. 
    Track waste patterns and suggest adjustments to ordering patterns.
tools:
    - inventory_tracker
    - demand_predictor
    - supplier_integration
    - stock_alert_generator
    - expiration_monitor
    - waste_analyzer
```

### Workforce Orchestration Agent

The Workforce Orchestration Agent transforms how Starbucks manages its complex scheduling needs across 25 partners with different roles, certifications, and availability patterns. This agent goes beyond simple schedule creation by considering partner preferences, labor law compliance, skill requirements for different positions, and predicted customer traffic patterns. By automating shift swap approvals and ensuring proper coverage during peak hours, this agent significantly reduces management overhead while improving partner satisfaction through more flexible and fair scheduling practices.

Create the file `agents/workforce_orchestration_agent.yaml`:

```yaml
spec_version: v1
kind: native
name: workforce_orchestration_agent
llm: watsonx/meta-llama/llama-3-2-90b-vision-instruct
style: react
description: >
    The Workforce Orchestration Agent is an intelligent scheduling system that optimizes partner schedules while balancing business needs, 
    partner preferences, and regulatory compliance. It manages schedules for 25+ partners across various roles including baristas, shift 
    supervisors, and store managers, ensuring appropriate skill coverage during all operating hours. The agent processes shift swap requests 
    in real-time, validates coverage requirements, checks partner certifications, and ensures compliance with labor laws and company policies. 
    It also predicts staffing needs based on historical traffic patterns, local events, and seasonal trends to prevent under or overstaffing.
instructions: >
    You are the Workforce Orchestration Agent responsible for creating optimal schedules and managing workforce dynamics.
    
    Phase 1 - Schedule Optimization: Generate weekly schedules that balance partner availability, skill requirements, and predicted 
    customer traffic. Ensure each shift has appropriate coverage for baristas, shift supervisors, and specialized roles.
    
    Phase 2 - Shift Swap Processing: When partners request shift swaps, validate that both partners have required certifications, 
    the swap maintains minimum coverage levels, and complies with labor laws regarding consecutive days and maximum hours.
    
    Phase 3 - Coverage Analysis: Continuously monitor scheduled vs actual coverage. Predict potential gaps due to historical absence 
    patterns. Proactively suggest coverage solutions before issues arise.
    
    Phase 4 - Compliance Checking: Ensure all schedules comply with local labor laws, Starbucks policies, and partner contracts. 
    Flag any potential violations including excessive hours, insufficient breaks, or missing certifications.
    
    Phase 5 - Partner Communication: Provide clear, timely communication about schedule changes, approved swaps, and coverage needs. 
    Maintain fairness and transparency in all scheduling decisions.
collaborators:
    - partner_training_agent
tools:
    - schedule_optimizer
    - shift_swap_processor
    - coverage_analyzer
    - compliance_checker
    - traffic_predictor
    - partner_availability_tracker
```

### Partner Training & Support Agent

The Partner Training & Support Agent serves as an always-available knowledge resource for Starbucks partners, dramatically reducing onboarding time and improving consistency in drink preparation and policy adherence. This agent combines comprehensive policy documentation with interactive training modules and real-time recipe guidance, enabling new partners to become productive 40% faster while ensuring experienced partners can quickly reference any procedure or policy. The integration with a Milvus-based knowledge base allows for semantic search capabilities, ensuring partners find exactly what they need regardless of how they phrase their questions.

Create the file `agents/partner_training_agent.yaml`:

```yaml
spec_version: v1
kind: native
name: partner_training_agent
llm: watsonx/ibm/granite-3-8b-instruct
style: default
description: >
    The Partner Training & Support Agent is a comprehensive knowledge and training system that provides instant access to Starbucks policies, 
    procedures, recipes, and training materials. It serves both new partners during onboarding and experienced partners who need quick 
    reference to specific information. The agent uses advanced semantic search to understand natural language queries and provide relevant, 
    contextual responses from the extensive knowledge base of partner guides, recipe cards, and policy documents. It can generate 
    step-by-step instructions for any beverage, including modifications and dietary restrictions, while ensuring compliance with 
    Starbucks standards and food safety regulations.
instructions: >
    You are the Partner Training & Support Agent, providing comprehensive guidance and training support to all Starbucks partners.
    
    Phase 1 - Query Understanding: Interpret partner questions using natural language understanding. Identify whether they need 
    policy information, recipe guidance, procedural instructions, or training modules.
    
    Phase 2 - Knowledge Retrieval: Search the comprehensive knowledge base for relevant information. Prioritize official Starbucks 
    documentation and ensure all guidance aligns with current standards and policies.
    
    Phase 3 - Contextual Response: Provide clear, step-by-step instructions tailored to the partner's experience level. For recipes, 
    include quantities, temperatures, and timing. For policies, cite specific sections and explain practical applications.
    
    Phase 4 - Interactive Training: When appropriate, guide partners through interactive training scenarios. Track completion and 
    comprehension. Suggest additional resources for skill development.
    
    Phase 5 - Continuous Learning: Update responses based on new policies, seasonal beverages, and procedural changes. Track 
    common questions to identify training gaps and improvement opportunities.
tools:
    - policy_search
    - training_module_generator
    - recipe_guide
    - certification_tracker
    - onboarding_assistant
knowledge_base:
    - starbucks_operations_kb
```

### Equipment Health Monitor Agent

The Equipment Health Monitor Agent represents a breakthrough in preventive maintenance for Starbucks stores, using IoT sensor data and predictive analytics to anticipate equipment failures before they impact operations. By monitoring critical equipment like espresso machines, blenders, and ovens, this agent can detect performance degradation patterns and schedule maintenance during off-peak hours, preventing the costly disruptions that occur when equipment fails during busy periods. The integration with ServiceNow for ticket creation ensures that maintenance issues are tracked and resolved systematically, contributing to improved equipment uptime and customer satisfaction.

Create the file `agents/equipment_health_agent.yaml`:

```yaml
spec_version: v1
kind: native
name: equipment_health_agent
llm: watsonx/meta-llama/llama-3-2-90b-vision-instruct
style: react
description: >
    The Equipment Health Monitor Agent is an advanced predictive maintenance system that monitors all critical store equipment including 
    espresso machines, blenders, ovens, refrigeration units, and brewing systems. Using real-time IoT sensor data and historical 
    maintenance patterns, it predicts potential failures before they occur and provides proactive maintenance recommendations. 
    The agent offers immediate troubleshooting guidance for common issues, enabling partners to resolve minor problems without waiting 
    for technicians. It automatically creates and prioritizes service tickets in ServiceNow for issues requiring professional maintenance, 
    tracking resolution progress and maintaining comprehensive equipment history for optimal lifecycle management.
instructions: >
    You are the Equipment Health Monitor Agent responsible for maintaining optimal equipment performance and preventing service disruptions.
    
    Phase 1 - Continuous Monitoring: Track real-time sensor data from all equipment. Monitor temperature, pressure, vibration, 
    and usage patterns. Identify anomalies that indicate potential issues.
    
    Phase 2 - Predictive Analysis: Analyze patterns to predict failures before they occur. Consider equipment age, usage intensity, 
    maintenance history, and environmental factors. Generate reliability scores for each piece of equipment.
    
    Phase 3 - Troubleshooting Guidance: When issues are detected, provide immediate troubleshooting steps that partners can perform. 
    Include safety precautions and clear instructions. Escalate to professional maintenance when necessary.
    
    Phase 4 - Maintenance Scheduling: Recommend optimal maintenance windows based on equipment criticality and store traffic patterns. 
    Coordinate with workforce scheduling to ensure technical staff availability.
    
    Phase 5 - Service Integration: Automatically create ServiceNow tickets for issues requiring professional service. Track ticket 
    progress and update partners on resolution status. Maintain detailed service history for warranty and lifecycle management.
tools:
    - equipment_status_checker
    - maintenance_predictor
    - ticket_creator
    - troubleshooting_guide
    - sensor_data_analyzer
    - maintenance_scheduler
```

## Step 3: Create Comprehensive Tool Implementations

### Store Operations Dashboard Tools

These foundational tools provide real-time visibility into overall store operations, enabling the supervisor agent to quickly assess store status and generate priority alerts. The store status dashboard aggregates data from all operational domains into a unified view, while the priority alert generator ensures that critical issues receive immediate attention. These tools form the backbone of the proactive operational support system, enabling partners and managers to make informed decisions quickly and maintain optimal store performance across all operational areas.

Create the file `tools/store_operations.py`:

```python
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
```

### Inventory Management Tools

The inventory management tools form the core of the predictive inventory system, enabling Starbucks stores to maintain optimal stock levels while minimizing waste. These tools work together to track current inventory, predict future demand based on multiple factors, integrate with supplier systems for automated ordering, and generate intelligent alerts. The sophisticated demand prediction algorithm considers historical patterns, seasonal trends, promotional calendars, and even local events to ensure accuracy. The expiration monitor and waste analyzer tools help reduce product waste and improve sustainability efforts while maintaining product freshness standards.

Create the file `tools/inventory_management.py`:

```python
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission


class ProductCategory(str, Enum):
    COFFEE = "coffee"
    SYRUP = "syrup"
    DAIRY = "dairy"
    FOOD = "food"
    SUPPLIES = "supplies"
    SEASONAL = "seasonal"


class StockStatus(str, Enum):
    OPTIMAL = "optimal"
    LOW = "low"
    CRITICAL = "critical"
    OVERSTOCKED = "overstocked"
    EXPIRED = "expired"


@tool(name="inventory_tracker", permission=ToolPermission.READ_ONLY)
def inventory_tracker(store_id: str, category: Optional[ProductCategory] = None) -> str:
    """Tracks real-time inventory levels across all product categories and SKUs.
    
    This tool provides comprehensive visibility into current stock levels for over 500 SKUs
    including coffee beans, syrups, dairy products, food items, and operational supplies.
    It monitors quantities, expiration dates, and storage locations while calculating
    days of supply based on consumption patterns. This real-time tracking enables
    proactive inventory management and prevents stockouts.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        category (ProductCategory, optional): Filter results by product category
        
    Returns:
        str: JSON string containing detailed inventory status with quantities,
             expiration dates, and stock health indicators
    """
    try:
        current_time = datetime.now()
        
        # Generate realistic inventory data
        inventory_items = []
        
        # Coffee products
        coffee_products = [
            ("Pike Place Roast", "COF-001", 45, "lbs", 5, 7),
            ("Blonde Espresso", "COF-002", 38, "lbs", 5, 6),
            ("Dark Roast", "COF-003", 52, "lbs", 6, 8),
            ("Decaf Pike Place", "COF-004", 22, "lbs", 3, 5),
            ("Cold Brew Concentrate", "COF-005", 18, "gallons", 2, 4)
        ]
        
        # Syrup products
        syrup_products = [
            ("Vanilla Syrup", "SYR-001", 12, "bottles", 2, 10),
            ("Caramel Syrup", "SYR-002", 8, "bottles", 2, 7),
            ("Hazelnut Syrup", "SYR-003", 10, "bottles", 2, 8),
            ("Peppermint Syrup", "SYR-004", 15, "bottles", 1, 12),
            ("Brown Sugar Syrup", "SYR-005", 5, "bottles", 2, 6)
        ]
        
        # Dairy products
        dairy_products = [
            ("Whole Milk", "DAI-001", 25, "gallons", 1, 2),
            ("2% Milk", "DAI-002", 30, "gallons", 1, 2),
            ("Oat Milk", "DAI-003", 18, "cartons", 1, 3),
            ("Almond Milk", "DAI-004", 22, "cartons", 1, 3),
            ("Heavy Cream", "DAI-005", 8, "quarts", 1, 2)
        ]
        
        # Food products
        food_products = [
            ("Blueberry Muffin", "FOD-001", 24, "units", 1, 2),
            ("Butter Croissant", "FOD-002", 18, "units", 1, 2),
            ("Egg Bites", "FOD-003", 36, "packages", 2, 3),
            ("Protein Box", "FOD-004", 12, "units", 1, 2),
            ("Cake Pops", "FOD-005", 30, "units", 3, 5)
        ]
        
        # Supplies
        supply_products = [
            ("Venti Cups", "SUP-001", 800, "units", 100, 30),
            ("Grande Cups", "SUP-002", 1200, "units", 150, 30),
            ("Napkins", "SUP-003", 2000, "units", 200, 30),
            ("Stirrers", "SUP-004", 1500, "units", 100, 30),
            ("Cup Sleeves", "SUP-005", 1000, "units", 100, 30)
        ]
        
        all_products = [
            (ProductCategory.COFFEE, coffee_products),
            (ProductCategory.SYRUP, syrup_products),
            (ProductCategory.DAIRY, dairy_products),
            (ProductCategory.FOOD, food_products),
            (ProductCategory.SUPPLIES, supply_products)
        ]
        
        for product_category, products in all_products:
            if category and product_category != category:
                continue
                
            for name, sku, base_qty, unit, reorder_point, exp_days in products:
                # Add some randomness to quantities
                quantity = base_qty + random.randint(-5, 10)
                quantity = max(0, quantity)
                
                # Calculate stock status
                if quantity <= 0:
                    status = StockStatus.CRITICAL
                elif quantity <= reorder_point:
                    status = StockStatus.LOW
                elif quantity > reorder_point * 4:
                    status = StockStatus.OVERSTOCKED
                else:
                    status = StockStatus.OPTIMAL
                
                # Calculate expiration for perishables
                expiration_date = None
                if product_category in [ProductCategory.DAIRY, ProductCategory.FOOD]:
                    expiration_date = (current_time + timedelta(days=exp_days)).isoformat()
                
                item = {
                    "sku": sku,
                    "name": name,
                    "category": product_category,
                    "quantity": quantity,
                    "unit": unit,
                    "status": status,
                    "reorder_point": reorder_point,
                    "days_of_supply": round(quantity / (reorder_point / 2), 1) if reorder_point > 0 else 0,
                    "last_updated": current_time.isoformat(),
                    "expiration_date": expiration_date,
                    "storage_location": f"Zone {random.choice(['A', 'B', 'C'])}-{random.randint(1, 5)}"
                }
                inventory_items.append(item)
        
        # Calculate summary statistics
        summary = {
            "total_skus": len(inventory_items),
            "critical_items": len([i for i in inventory_items if i["status"] == StockStatus.CRITICAL]),
            "low_stock_items": len([i for i in inventory_items if i["status"] == StockStatus.LOW]),
            "optimal_items": len([i for i in inventory_items if i["status"] == StockStatus.OPTIMAL]),
            "overstocked_items": len([i for i in inventory_items if i["status"] == StockStatus.OVERSTOCKED])
        }
        
        response = {
            "store_id": store_id,
            "timestamp": current_time.isoformat(),
            "summary": summary,
            "inventory": inventory_items
        }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to track inventory: {str(e)}"})


@tool(name="demand_predictor", permission=ToolPermission.READ_ONLY)
def demand_predictor(
    store_id: str, 
    product_sku: str, 
    days_ahead: int = 7
) -> str:
    """Predicts future demand using AI-driven analytics based on multiple factors.
    
    This sophisticated tool analyzes historical sales data, seasonal patterns, day-of-week
    trends, weather forecasts, local events, and promotional calendars to generate accurate
    demand predictions. It uses machine learning algorithms to identify patterns and
    anomalies, enabling proactive inventory management that reduces both stockouts and waste.
    The predictions help optimize ordering quantities and timing.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        product_sku (str): The SKU of the product to predict demand for
        days_ahead (int): Number of days to predict ahead (default: 7)
        
    Returns:
        str: JSON string containing daily demand predictions with confidence intervals
             and factors influencing the forecast
    """
    try:
        current_time = datetime.now()
        
        # Simulate historical average based on product type
        sku_prefix = product_sku.split('-')[0]
        base_demands = {
            "COF": 8.5,  # Coffee products
            "SYR": 2.3,  # Syrups
            "DAI": 12.7, # Dairy
            "FOD": 15.2, # Food
            "SUP": 85.3  # Supplies
        }
        
        base_daily_demand = base_demands.get(sku_prefix, 10.0)
        
        # Generate daily predictions
        predictions = []
        
        for day in range(days_ahead):
            prediction_date = current_time + timedelta(days=day)
            day_of_week = prediction_date.strftime("%A")
            
            # Apply day of week multipliers
            dow_multipliers = {
                "Monday": 1.2,
                "Tuesday": 0.9,
                "Wednesday": 0.95,
                "Thursday": 1.0,
                "Friday": 1.3,
                "Saturday": 1.4,
                "Sunday": 1.1
            }
            
            dow_multiplier = dow_multipliers.get(day_of_week, 1.0)
            
            # Seasonal factors
            month = prediction_date.month
            seasonal_multiplier = 1.0
            if month in [11, 12, 1]:  # Holiday season
                seasonal_multiplier = 1.3
            elif month in [6, 7, 8]:  # Summer
                seasonal_multiplier = 1.15
            
            # Weather impact (simulated)
            weather_impact = random.uniform(0.9, 1.1)
            
            # Special events (simulated)
            event_multiplier = 1.0
            event_name = None
            if random.random() > 0.85:  # 15% chance of special event
                event_multiplier = random.uniform(1.2, 1.5)
                event_name = random.choice([
                    "Local Festival", "Sports Event", "Concert", 
                    "Conference", "Holiday Weekend"
                ])
            
            # Calculate predicted demand
            predicted_demand = (
                base_daily_demand * 
                dow_multiplier * 
                seasonal_multiplier * 
                weather_impact * 
                event_multiplier
            )
            
            # Add some random variation
            predicted_demand *= random.uniform(0.85, 1.15)
            
            # Calculate confidence interval
            confidence_lower = predicted_demand * 0.85
            confidence_upper = predicted_demand * 1.15
            
            prediction = {
                "date": prediction_date.strftime("%Y-%m-%d"),
                "day_of_week": day_of_week,
                "predicted_quantity": round(predicted_demand, 1),
                "confidence_interval": {
                    "lower": round(confidence_lower, 1),
                    "upper": round(confidence_upper, 1)
                },
                "factors": {
                    "base_demand": round(base_daily_demand, 1),
                    "day_of_week_impact": f"{round((dow_multiplier - 1) * 100, 1)}%",
                    "seasonal_impact": f"{round((seasonal_multiplier - 1) * 100, 1)}%",
                    "weather_impact": f"{round((weather_impact - 1) * 100, 1)}%",
                    "special_event": event_name
                }
            }
            predictions.append(prediction)
        
        # Calculate aggregated statistics
        total_predicted = sum(p["predicted_quantity"] for p in predictions)
        avg_daily = total_predicted / days_ahead if days_ahead > 0 else 0
        peak_day = max(predictions, key=lambda x: x["predicted_quantity"]) if predictions else None
        
        response = {
            "store_id": store_id,
            "product_sku": product_sku,
            "prediction_generated": current_time.isoformat(),
            "prediction_period": f"{days_ahead} days",
            "summary": {
                "total_predicted_demand": round(total_predicted, 1),
                "average_daily_demand": round(avg_daily, 1),
                "peak_demand_day": peak_day["date"] if peak_day else None,
                "peak_demand_quantity": peak_day["predicted_quantity"] if peak_day else 0
            },
            "daily_predictions": predictions,
            "recommendation": _generate_ordering_recommendation(total_predicted, days_ahead)
        }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to predict demand: {str(e)}"})


@tool(name="supplier_integration", permission=ToolPermission.ADMIN)
def supplier_integration(
    store_id: str,
    supplier_id: str,
    order_items: List[Dict[str, Any]]
) -> str:
    """Integrates with supplier systems to automate ordering and track deliveries.
    
    This tool provides seamless integration with Starbucks' supplier network, enabling
    automated order placement based on inventory levels and demand predictions. It handles
    order validation, submission, confirmation, and tracking while maintaining compliance
    with procurement policies. The integration reduces manual ordering errors and ensures
    timely replenishment of all products.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        supplier_id (str): The supplier identifier (e.g., "SUP-DAIRY", "SUP-COFFEE")
        order_items (List[Dict]): List of items to order with SKU and quantity
        
    Returns:
        str: JSON string containing order confirmation details, expected delivery,
             and tracking information
    """
    try:
        current_time = datetime.now()
        
        # Validate supplier
        suppliers = {
            "SUP-DAIRY": "Fresh Dairy Distributors Inc.",
            "SUP-COFFEE": "Starbucks Roasting Plant",
            "SUP-FOOD": "Artisan Food Partners",
            "SUP-SUPPLIES": "Restaurant Supply Co.",
            "SUP-SYRUP": "Flavor Systems International"
        }
        
        supplier_name = suppliers.get(supplier_id, "Unknown Supplier")
        
        # Process order items
        processed_items = []
        total_amount = 0
        
        for item in order_items:
            # Simulate pricing
            unit_price = random.uniform(5.0, 50.0)
            quantity = item.get("quantity", 1)
            line_total = unit_price * quantity
            total_amount += line_total
            
            processed_item = {
                "sku": item.get("sku"),
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "line_total": round(line_total, 2),
                "availability": random.choice(["in_stock", "in_stock", "in_stock", "limited"])
            }
            processed_items.append(processed_item)
        
        # Generate order details
        order_number = f"ORD-{random.randint(100000, 999999)}"
        
        # Calculate delivery date based on supplier
        delivery_days = {
            "SUP-DAIRY": 1,
            "SUP-COFFEE": 2,
            "SUP-FOOD": 1,
            "SUP-SUPPLIES": 3,
            "SUP-SYRUP": 2
        }
        
        delivery_date = current_time + timedelta(days=delivery_days.get(supplier_id, 2))
        
        response = {
            "order_confirmation": {
                "order_number": order_number,
                "store_id": store_id,
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "order_date": current_time.isoformat(),
                "status": "confirmed",
                "total_items": len(processed_items),
                "total_amount": round(total_amount, 2),
                "currency": "USD"
            },
            "order_items": processed_items,
            "delivery_information": {
                "expected_delivery": delivery_date.isoformat(),
                "delivery_window": "8:00 AM - 12:00 PM",
                "delivery_method": "Standard Truck",
                "tracking_number": f"TRK-{random.randint(10000000, 99999999)}",
                "special_instructions": "Deliver to back entrance, refrigerated items first"
            },
            "payment_terms": {
                "method": "Net 30",
                "account_number": f"****{random.randint(1000, 9999)}"
            }
        }
        
        return json.dumps(response, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to process supplier order: {str(e)}"})


@tool(name="stock_alert_generator", permission=ToolPermission.READ_ONLY)
def stock_alert_generator(store_id: str, threshold_days: int = 3) -> str:
    """Generates intelligent alerts for inventory items requiring attention.
    
    This tool continuously monitors inventory levels against dynamic thresholds and
    generates prioritized alerts for items that need immediate attention. It considers
    factors like lead time, demand variability, and business criticality to ensure
    partners are notified of potential stockouts before they impact operations.
    The alerts include specific action recommendations.
    
    Args:
        store_id (str): The unique identifier of the Starbucks store
        threshold_days (int): Alert when days of supply falls below this (default: 3)
        
    Returns:
        str: JSON string containing prioritized inventory alerts with recommended actions
    """
    try:
        current_time = datetime.now()
        
        # Generate realistic alerts
        alerts = []
        
        # Critical alerts
        critical_items = [
            {
                "sku": "DAI-003",
                "name": "Oat Milk",
                "current_quantity": 3,
                "unit": "cartons",
                "days_of_supply": 0.5,
                "daily_usage": 6,
                "reason": "High demand item with very low stock"
            },
            {

---
*Plan generated by IBM watsonx Orchestrate Planner Agent*
