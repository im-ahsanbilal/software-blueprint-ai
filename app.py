from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from agents.requirement_agent import requirement_agent
from agents.database_agent import database_agent
from agents.risk_agent import risk_agent
from agents.roadmap_agent import roadmap_agent
from agents.refine_agent import refine_agent

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


@app.route('/')
def index():
    """
    Home page route - renders the input form for project title.
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate blueprint route - chains through all agents to create a complete software architecture blueprint.
    Receives project_title, then calls agents sequentially: requirement -> database -> risk -> roadmap.
    """
    project_title = request.form.get('project_title')
    
    # Step 1: Generate requirements
    requirements = requirement_agent(project_title)
    
    # Step 2: Design database schema based on requirements
    database = database_agent(project_title, requirements)
    
    # Step 3: Identify potential risks
    risks = risk_agent(project_title, requirements, database)
    
    # Step 4: Create development roadmap
    roadmap = roadmap_agent(project_title, requirements, database, risks)
    
    # Render blueprint with all agent results
    return render_template('blueprint.html', 
                          project_title=project_title,
                          requirements=requirements,
                          database=database,
                          risks=risks,
                          roadmap=roadmap)


@app.route('/refine', methods=['POST'])
def refine():
    """
    Refine blueprint route - allows targeted updates to an existing blueprint.
    Receives change_request and existing blueprint data, passes to refine_agent.
    """
    change_request = request.form.get('change_request')
    project_title = request.form.get('project_title')
    requirements = request.form.get('requirements')
    database = request.form.get('database')
    risks = request.form.get('risks')
    roadmap = request.form.get('roadmap')
    
    # Call refine agent to make targeted updates
    updated_blueprint = refine_agent(
        change_request=change_request,
        project_title=project_title,
        requirements=requirements,
        database=database,
        risks=risks,
        roadmap=roadmap
    )
    
    # Render updated blueprint
    return render_template('blueprint.html', 
                          project_title=updated_blueprint.get('project_title', project_title),
                          requirements=updated_blueprint.get('requirements', requirements),
                          database=updated_blueprint.get('database', database),
                          risks=updated_blueprint.get('risks', risks),
                          roadmap=updated_blueprint.get('roadmap', roadmap))


if __name__ == '__main__':
    app.run(debug=True)
