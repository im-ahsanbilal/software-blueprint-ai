import os
from google import genai


def risk_agent(project_title, requirements, database):
    """
    Generate comprehensive risk assessment for a given project title, requirements, and database design.
    
    Args:
        project_title (str): The title/description of the software project
        requirements (str): The requirements document from requirement_agent
        database (str): The database schema design from database_agent
        
    Returns:
        str: Generated risk assessment from Gemini API
    """
    # Load Gemini API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Build detailed prompt for risk assessment generation
    prompt = f"""
You are an expert risk analyst and project manager. Conduct a comprehensive risk assessment for the following project:

Project Title: {project_title}

Requirements:
{requirements}

Database Schema:
{database}

Please provide a detailed risk assessment that includes:

1. Technical Risks:
   - Security vulnerabilities (authentication, authorization, data encryption, injection attacks)
   - Scalability issues (performance bottlenecks, load handling, resource constraints)
   - Integration risks (third-party API dependencies, service availability, version compatibility)
   - Technology stack risks (obsolescence, learning curve, community support)
   - Infrastructure risks (cloud provider dependencies, backup/recovery, disaster recovery)

2. Business Risks:
   - Timeline risks (unrealistic deadlines, scope creep, dependency delays)
   - Budget risks (cost overruns, resource allocation, unexpected expenses)
   - Market risks (competition, changing requirements, user adoption)
   - Regulatory and compliance risks (GDPR, HIPAA, industry-specific regulations)
   - Stakeholder risks (changing priorities, lack of buy-in, communication gaps)

3. Data Risks:
   - Data loss risks (backup failures, accidental deletion, corruption)
   - Data integrity risks (inconsistent data, migration errors, synchronization issues)
   - Privacy concerns (PII handling, data breaches, unauthorized access)
   - Data migration risks (legacy system integration, data quality, downtime)

4. Mitigation Strategies:
   - Specific actionable steps for each identified risk
   - Prevention measures
   - Contingency plans
   - Monitoring and early warning indicators

5. Risk Severity Levels:
   - High: Critical risks that could derail the project
   - Medium: Significant risks requiring attention
   - Low: Minor risks with minimal impact

Format the output in a clear, structured manner with risk categories, individual risks, severity levels, and corresponding mitigation strategies.
Be specific and practical, avoiding generic advice.
"""
    
    # Call Gemini API with the prompt
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt
    )
    
    # Return the response text
    return response.text