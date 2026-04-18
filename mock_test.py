import json
import os
from app.agents.supervisor import Supervisor

# Mock project data that would normally come from the Extraction Agent
mock_project_data = {
    "project_name": "Test App",
    "tech_stack": "HTML and Plain CSS",
    "tasks": [
        {
            "id": 1,
            "title": "Index Page",
            "prompt": "Create a simple index.html file with a 'Hello World' heading and a link to a styles.css file.",
            "dependencies": []
        },
        {
            "id": 2,
            "title": "Styles",
            "prompt": "Create a styles.css file that sets the background color of the body to lightblue.",
            "dependencies": [1]
        }
    ]
}

def test_supervisor():
    print("Starting mock test...")
    # Adjust base_dir for local test
    supervisor = Supervisor(mock_project_data, base_dir="test_workspaces")
    
    # Run the generation
    workspace_path = supervisor.run()
    print(f"Workspace created at: {workspace_path}")
    
    # Create zip
    zip_path = supervisor.create_zip(export_dir="test_exports")
    print(f"Zip created at: {zip_path}")
    
    # Verify files exist
    files = os.listdir(workspace_path)
    print(f"Files in workspace: {files}")
    
    if "index.html" in files or "styles.css" in files:
        print("Test Passed: Files generated.")
    else:
        print("Test Failed: No files generated (check if LLM actually returned anything).")

if __name__ == "__main__":
    # Note: This requires OPENROUTER_API_KEY to be set in .env
    test_supervisor()
