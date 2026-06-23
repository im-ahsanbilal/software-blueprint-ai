# BlueprintAI — AI Software Architecture Assistant

An AI-powered multi-agent system that generates complete software architecture blueprints from a single project title. Built with Python, Flask, and Google Gemini API.

## What It Does

User enters a project title → 4 specialized AI agents run in sequence → complete software blueprint generated in seconds.

**Agent Pipeline:**
1. **Requirement Agent** — Generates functional and non-functional requirements
2. **Database Agent** — Designs database schema and relationships
3. **Risk Agent** — Identifies risks and mitigation strategies
4. **Roadmap Agent** — Creates phased development roadmap

Users can also refine any blueprint using natural language — "Add payment gateway support" — and all sections update automatically.

## Tech Stack

- **Backend:** Python, Flask
- **AI:** Google Gemini API (gemini-3.1-flash-lite)
- **Frontend:** HTML, CSS, Bootstrap, Markdown rendering
- **Architecture:** Multi-agent pipeline

## How to Run Locally

1. Clone the repository:

        git clone https://github.com/im-ahsanbilal/blueprintai.git
        cd blueprintai

2. Create and activate virtual environment:

        python -m venv venv
        venv\Scripts\activate

3. Install dependencies:

        pip install -r requirements.txt

4. Create a `.env` file in the root folder and add your Gemini API key:

        GEMINI_API_KEY=your_gemini_api_key_here

5. Run the app:

        python app.py

6. Open your browser and go to `http://127.0.0.1:5000`


## Author

**Muhammad Ahsan** — [GitHub](https://github.com/im-ahsanbilal) | [Portfolio](https://imahsanbilal.pythonanywhere.com)