import os
from google import genai


def requirement_agent(project_title):
    """
    Generate comprehensive functional and non-functional requirements for a given project title.
    
    Args:
        project_title (str): The title/description of the software project
        
    Returns:
        str: Generated requirements text from Gemini API
    """
    # Load Gemini API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Build detailed prompt for requirements generation
    prompt = f"""
You are an expert software architect and requirements engineer. Generate comprehensive requirements for the following project:

Project Title: {project_title}

Please provide a detailed requirements document that includes:

1. Functional Requirements:
   - User stories and use cases
   - Core features and capabilities
   - User interactions and workflows
   - Input/output specifications
   - Business rules and constraints

2. Non-Functional Requirements:
   - Performance requirements (response time, throughput, scalability)
   - Security requirements (authentication, authorization, data protection)
   - Reliability and availability requirements
   - Usability requirements
   - Compatibility requirements (platforms, browsers, devices)
   - Maintainability and extensibility requirements

3. Technical Requirements:
   - Technology stack recommendations
   - Integration requirements (third-party services, APIs)
   - Data requirements (storage, backup, retention)

Format the output in a clear, structured manner with appropriate headings and bullet points.
Be specific and detailed, avoiding generic statements.
"""
    
    # Call Gemini API with the prompt
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Return the response text
    return response.text