import os
from google import genai


def database_agent(project_title, requirements):
    """
    Generate comprehensive database schema design for a given project title and requirements.
    
    Args:
        project_title (str): The title/description of the software project
        requirements (str): The requirements document from requirement_agent
        
    Returns:
        str: Generated database schema design from Gemini API
    """
    # Load Gemini API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Build detailed prompt for database schema generation
    prompt = f"""
You are an expert database architect and data modeler. Design a comprehensive database schema for the following project:

Project Title: {project_title}

Requirements:
{requirements}

Please provide a detailed database schema design that includes:

1. Database Tables:
   - Table names with clear, descriptive names
   - Column names with appropriate data types (VARCHAR, INT, TEXT, DATETIME, BOOLEAN, DECIMAL, etc.)
   - Column specifications (length, constraints, default values, nullability)
   - Primary keys for each table

2. Relationships:
   - Foreign keys with references to related tables
   - Relationship types (one-to-one, one-to-many, many-to-many)
   - Cascade rules (ON DELETE, ON UPDATE) where applicable

3. Indexes:
   - Recommended indexes for performance optimization
   - Index types (single-column, composite, unique)
   - Justification for each index

4. Additional Considerations:
   - Normalization level (3NF recommended)
   - Denormalization recommendations if needed for performance
   - Data integrity constraints
   - Security considerations (sensitive data handling)

Format the output in a clear, structured manner. Use SQL-like notation or ER diagram descriptions where helpful.
Be specific about data types and constraints, avoiding generic recommendations.
"""
    
    # Call Gemini API with the prompt
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Return the response text
    return response.text