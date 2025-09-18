import json
from typing import List, Dict
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="identify_risk_mentions", description="Identifies and extracts explicit mentions of risks from a financial document.", permission=ToolPermission.ADMIN)
def identify_risk_mentions(document_content: str) -> List[Dict]:
    """
    Scans document text to find sentences mentioning potential risks.

    Args:
        document_content (str): The text content of the financial document.

    Returns:
        List[Dict]: A list of dictionaries, each containing a risk type and the sentence where it was mentioned.
    """
    risks = []
    risk_keywords = {
        "SUPPLY_CHAIN": ["supply chain", "logistics"],
        "GEOPOLITICAL": ["geopolitical headwinds"],
        "MARGIN_PRESSURE": ["gross margins", "costs"]
    }
    sentences = document_content.split('.')
    for sentence in sentences:
        for risk_type, keywords in risk_keywords.items():
            for keyword in keywords:
                if keyword in sentence.lower():
                    risks.append({
                        "risk_type": risk_type,
                        "mention": sentence.strip()
                    })
    return risks

@tool(name="analyze_sentiment_by_section", description="Analyzes and scores the sentiment of different sections of a document.", permission=ToolPermission.ADMIN)
def analyze_sentiment_by_section(document_content: str) -> Dict:
    """
    Analyzes the sentiment (positive, neutral, negative) of key sections like CEO and CFO statements.

    Args:
        document_content (str): The text content of the financial document.

    Returns:
        Dict: A dictionary with sections as keys and sentiment scores as values.
    """
    sentiment_data = {
        "CEO_Statement": {"sentiment": "Neutral", "score": 0.1, "summary": "CEO highlights strong demand but notes emerging supply chain challenges."},
        "CFO_Statement": {"sentiment": "Slightly Negative", "score": -0.3, "summary": "CFO discusses increased R&D spending but expresses concern over margin pressure from logistics costs."}
    }
    # This is a mock analysis. A real tool would use an NLP model.
    if "geopolitical headwinds" in document_content and "pressure on our gross margins" in document_content:
        return sentiment_data
    else:
        return {"Overall": {"sentiment": "Positive", "score": 0.8, "summary": "No significant negative indicators found."}}

@tool(name="extract_key_topics", description="Extracts the main financial and operational topics from a document.", permission=ToolPermission.ADMIN)
def extract_key_topics(document_content: str) -> List[str]:
    """
    Identifies the primary topics discussed in the text.

    Args:
        document_content (str): The text content of the financial document.

    Returns:
        List[str]: A list of key topics identified.
    """
    topics = []
    if "Quantum Fusion processor" in document_content:
        topics.append("New Product Demand")
    if "supply chain disruptions" in document_content:
        topics.append("Supply Chain Issues")
    if "R&D spending" in document_content:
        topics.append("R&D Investment")
    if "gross margins" in document_content:
        topics.append("Margin Pressure")
    return topics if topics else ["General Business Update"]