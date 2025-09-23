import os
from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

@tool(name="extract_text_from_file", description="Extracts raw text content from a specified file (PDF, DOCX, TXT).", permission=ToolPermission.ADMIN)
def extract_text_from_file(file_path: str) -> str:
    """
    Extracts text from various document formats.

    Args:
        file_path (str): The local path to the file (e.g., 'mock_data/HR_Policy_Guide.txt').

    Returns:
        str: The extracted text content from the file.
    """
    try:
        # This is a simplified mock for demo purposes.
        # In a real implementation, you would use libraries to parse file types.
        if not os.path.exists(file_path):
            return f"Error: File not found at path '{file_path}'"

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content

        # Example for a real implementation:
        # from pypdf import PdfReader
        # from docx import Document
        #
        # if file_path.endswith('.pdf'):
        #     reader = PdfReader(file_path)
        #     text = ""
        #     for page in reader.pages:
        #         text += page.extract_text()
        #     return text
        # elif file_path.endswith('.docx'):
        #     doc = Document(file_path)
        #     return "\\n".join([para.text for para in doc.paragraphs])
        # elif file_path.endswith('.txt'):
        #     with open(file_path, 'r') as f:
        #         return f.read()
        # else:
        #     return "Error: Unsupported file format."

    except Exception as e:
        return f"An error occurred while processing the file: {str(e)}"


@tool(name="generate_summary", description="Generates a concise summary of a given block of text.", permission=ToolPermission.ADMIN)
def generate_summary(text: str, length: str = "medium", points: int = 3) -> str:
    """
    Generates a summary of the provided text.

    Args:
        text (str): The text content to be summarized.
        length (str): The desired length of the summary ('short', 'medium', 'long').
        points (int): The number of bullet points for the summary.

    Returns:
        str: The generated summary.
    """
    # Mock logic for summarization. In a real scenario, this would call a summarization model.
    summary_intro = f"Here is a {length}, {points}-bullet point summary of the document:\n"
    
    # Simple logic to grab first few lines as a mock summary
    lines = text.strip().split('\n')
    bullet_points = [f"- {line.strip()}" for line in lines[:points] if line.strip()]
    
    if not bullet_points:
        return "Could not generate a summary from the provided text."
        
    return summary_intro + "\n".join(bullet_points)