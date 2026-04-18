# PDF to App Multi-Agent System

This system uses a Supervisor/Orchestrator multi-agent pattern to generate complete applications from structured PDFs.

## Setup

1.  **Clone the project.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure environment:**
    Create a `.env` file based on `.env.example`:
    ```bash
    OPENROUTER_API_KEY=your_key
    GITHUB_TOKEN=your_github_personal_access_token
    OPENROUTER_MODEL=meta-llama/llama-3-8b-instruct:free
    ```

## Usage

1.  **Start the server:**
    ```bash
    python -m app.main
    ```
2.  **Generate an app:**
    Send a POST request to `/generate` with your PDF file.
    - `file`: The structured PDF.
    - `github_token` (Optional): If provided, will push the code to GitHub.

3.  **Check status:**
    GET `/status/{job_id}`

4.  **Download project:**
    GET `/download/{job_id}`

## PDF Structure Requirement
The PDF should contain:
1.  **Tech Stack:** A clear definition of the desired technologies.
2.  **Step-by-Step Prompts:** Explicit prompts for each stage of development (e.g., "Step 1: Create the database schema...", "Step 2: Implement the authentication API...").
