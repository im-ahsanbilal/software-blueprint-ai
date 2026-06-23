import os
from google import genai


def roadmap_agent(project_title, requirements, database, risks):
    """
    Generate comprehensive development roadmap for a given project title, requirements, database design, and risk assessment.
    
    Args:
        project_title (str): The title/description of the software project
        requirements (str): The requirements document from requirement_agent
        database (str): The database schema design from database_agent
        risks (str): The risk assessment from risk_agent
        
    Returns:
        str: Generated development roadmap from Gemini API
    """
    # Load Gemini API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Build detailed prompt for roadmap generation
    prompt = f"""
You are an expert software architect and project manager. Create a comprehensive development roadmap for the following project:

Project Title: {project_title}

Requirements:
{requirements}

Database Schema:
{database}

Risk Assessment:
{risks}

Please provide a detailed development roadmap that includes:

1. Project Phases:
   - Phase breakdown with clear objectives
   - Phase dependencies and sequencing
   - Estimated duration for each phase
   - Deliverables for each phase

2. Development Milestones:
   - Key milestones with specific goals
   - Success criteria for each milestone
   - Timeline estimates
   - Dependencies between milestones

3. Technical Implementation Steps:
   - Architecture setup and infrastructure
   - Database implementation and migration
   - Core feature development sequence
   - Integration points and API development
   - Testing strategy (unit, integration, end-to-end)
   - Deployment and CI/CD pipeline

4. Resource Allocation:
   - Recommended team structure and roles
   - Skill requirements
   - Resource allocation per phase
   - External dependencies and third-party services

5. Risk Mitigation Timeline:
   - When to address identified risks
   - Risk monitoring checkpoints
   - Contingency planning milestones

6. Quality Gates:
   - Definition of done for each phase
   - Code review checkpoints
   - Testing requirements
   - Performance benchmarks

Format the output in a clear, structured manner with phases, timelines, and actionable steps.
Be specific about sequencing and dependencies, providing a realistic and achievable roadmap.
"""
    
    # Call Gemini API with the prompt
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Return the response text
    return response.text