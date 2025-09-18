import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="fetch_sec_filing", description="Fetches the content of a public SEC filing or earnings call transcript for a given company ticker.", permission=ToolPermission.ADMIN)
def fetch_sec_filing(company_ticker: str) -> str:
    """
    Retrieves the full text content of the latest financial filing for a company.

    Args:
        company_ticker (str): The stock ticker symbol for the company (e.g., 'QCI' for QuantumChip Inc.).

    Returns:
        str: The full text content of the document.
    """
    if company_ticker.upper() == "QCI":
        try:
            with open('mock_data/QuantumChip_earnings_transcript.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Error: Mock data file not found for QCI."
    return f"Error: No document found for ticker {company_ticker}."

@tool(name="transcribe_earnings_call", description="Transcribes the audio of a company's earnings call from a provided source URL.", permission=ToolPermission.ADMIN)
def transcribe_earnings_call(company_ticker: str, audio_source_url: str) -> str:
    """
    Processes an audio source and returns the transcribed text of an earnings call.

    Args:
        company_ticker (str): The stock ticker symbol of the company.
        audio_source_url (str): The URL to the audio recording of the earnings call.

    Returns:
        str: The transcribed text of the earnings call.
    """
    # In a real implementation, this would call a speech-to-text service.
    # For the demo, we return the same mock data.
    print(f"Simulating transcription for {company_ticker} from {audio_source_url}...")
    if company_ticker.upper() == "QCI":
        try:
            with open('mock_data/QuantumChip_earnings_transcript.txt', 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "Error: Mock data file not found for QCI."
    return f"Error: Transcription failed for ticker {company_ticker}."