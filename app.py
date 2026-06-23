from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import time
from agents.requirement_agent import requirement_agent
from agents.database_agent import database_agent
from agents.risk_agent import risk_agent
from agents.roadmap_agent import roadmap_agent
from agents.refine_agent import refine_agent

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'software-blueprint-ai-secret-key')

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

AI_SERVICE_ERROR_MESSAGE = 'The AI service is currently experiencing high demand. Please try again in a few moments.'
MAX_GENERATION_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def is_retryable_gemini_error(error):
    """
    Detect Gemini API failures that are commonly temporary, including high demand,
    timeout, and rate limit responses.
    """
    error_name = error.__class__.__name__.lower()
    error_text = str(error).lower()
    retryable_markers = (
        '503',
        'unavailable',
        'high demand',
        'timeout',
        'timed out',
        'deadline',
        'rate limit',
        'ratelimit',
        'resource exhausted',
        'too many requests',
        '429',
    )
    retryable_exception_names = (
        'apierror',
        'servererror',
        'serviceunavailable',
        'resourceexhausted',
        'toomanyrequests',
        'deadlineexceeded',
        'timeout',
        'timeouterror',
    )

    return (
        isinstance(error, TimeoutError)
        or any(marker in error_text for marker in retryable_markers)
        or any(name in error_name for name in retryable_exception_names)
    )


def generate_blueprint(project_title):
    """
    Run the complete blueprint generation workflow with short retries for
    temporary Gemini API failures.
    """
    last_error = None

    for attempt in range(1, MAX_GENERATION_RETRIES + 1):
        try:
            requirements = requirement_agent(project_title)
            database = database_agent(project_title, requirements)
            risks = risk_agent(project_title, requirements, database)
            roadmap = roadmap_agent(project_title, requirements, database, risks)

            return {
                'requirements': requirements,
                'database': database,
                'risks': risks,
                'roadmap': roadmap,
            }
        except Exception as error:
            last_error = error
            if attempt < MAX_GENERATION_RETRIES and is_retryable_gemini_error(error):
                app.logger.warning(
                    'Temporary Gemini API error during blueprint generation. Retrying attempt %s of %s.',
                    attempt + 1,
                    MAX_GENERATION_RETRIES,
                    exc_info=True,
                )
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise last_error


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

    try:
        blueprint = generate_blueprint(project_title)
    except Exception:
        app.logger.exception('Blueprint generation failed.')
        flash(AI_SERVICE_ERROR_MESSAGE, 'danger')
        return redirect(url_for('index'))
    
    # Render blueprint with all agent results
    return render_template('blueprint.html', 
                          project_title=project_title,
                          requirements=blueprint['requirements'],
                          database=blueprint['database'],
                          risks=blueprint['risks'],
                          roadmap=blueprint['roadmap'])


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

    try:
        for attempt in range(1, MAX_GENERATION_RETRIES + 1):
            try:
                # Call refine agent to make targeted updates
                updated_blueprint = refine_agent(
                    change_request=change_request,
                    project_title=project_title,
                    requirements=requirements,
                    database=database,
                    risks=risks,
                    roadmap=roadmap
                )
                break
            except Exception as error:
                if attempt < MAX_GENERATION_RETRIES and is_retryable_gemini_error(error):
                    app.logger.exception(
                        'Temporary Gemini API error during blueprint refinement. Retrying attempt %s of %s.',
                        attempt + 1,
                        MAX_GENERATION_RETRIES,
                    )
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
                raise
    except Exception:
        app.logger.exception('Blueprint refinement failed.')
        flash(AI_SERVICE_ERROR_MESSAGE, 'danger')
        return redirect(url_for('index'))
    
    # Render updated blueprint
    return render_template('blueprint.html', 
                          project_title=updated_blueprint.get('project_title', project_title),
                          requirements=updated_blueprint.get('requirements', requirements),
                          database=updated_blueprint.get('database', database),
                          risks=updated_blueprint.get('risks', risks),
                          roadmap=updated_blueprint.get('roadmap', roadmap))


if __name__ == '__main__':
    app.run(debug=True)
