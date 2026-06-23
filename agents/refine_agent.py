import os
import json
from google import genai


def refine_agent(change_request, project_title, requirements, database, risks, roadmap):
    """
    Apply targeted changes to an existing blueprint based on a change request.
    
    Args:
        change_request (str): The specific change/update requested by the user
        project_title (str): The title/description of the software project
        requirements (str): The current requirements document
        database (str): The current database schema design
        risks (str): The current risk assessment
        roadmap (str): The current development roadmap
        
    Returns:
        dict: Updated blueprint as a Python dictionary with keys: requirements, database, risks, roadmap
    """
    # Load Gemini API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Build detailed prompt for refinement
    prompt = f"""
You are an expert software architect. Apply the following change request to the existing blueprint and return ALL four updated sections.

Project Title: {project_title}

Change Request:
{change_request}

Current Requirements:
{requirements}

Current Database Schema:
{database}

Current Risk Assessment:
{risks}

Current Roadmap:
{roadmap}

Please analyze the change request and update the relevant sections of the blueprint. The change may affect one or multiple sections.

IMPORTANT: You must respond in valid JSON format ONLY, with no additional text before or after the JSON.
The JSON must have exactly these four keys:
- "requirements": the updated requirements text
- "database": the updated database schema text
- "risks": the updated risk assessment text
- "roadmap": the updated roadmap text

If a section does not need changes based on the request, return the original content for that section.
Ensure all sections remain comprehensive and consistent with each other.
"""
    
    # Call Gemini API with the prompt
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Parse the response as JSON
    try:
        updated_blueprint = json.loads(response.text)
        return updated_blueprint
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return original data with error note
        return {
            'requirements': requirements,
            'database': database,
            'risks': risks,
            'roadmap': roadmap,
            'error': f'Failed to parse Gemini response as JSON: {str(e)}'
        }