import os
import shutil
import zipfile
from app.agents.worker_agent import generate_code_for_task

class Supervisor:
    def __init__(self, project_data: dict, base_dir: str = "workspaces"):
        self.project_name = project_data.get("project_name", "untitled_project")
        self.tech_stack = project_data.get("tech_stack", "General")
        self.tasks = project_data.get("tasks", [])
        self.base_dir = base_dir
        self.workspace_path = os.path.join(base_dir, self.project_name.replace(" ", "_").lower())
        self.context = ""

    def setup_workspace(self):
        """Creates a clean workspace for the project."""
        if os.path.exists(self.workspace_path):
            shutil.rmtree(self.workspace_path)
        os.makedirs(self.workspace_path, exist_ok=True)

    def write_generated_files(self, worker_output: str):
        """Parses worker output and writes files to the workspace."""
        lines = worker_output.splitlines()
        current_file = None
        content = []
        
        for line in lines:
            if line.startswith("FILE: "):
                # Save previous file if any
                if current_file:
                    self._save_file(current_file, "\n".join(content))
                    self.context += f"\nFile: {current_file}\nContent:\n{''.join(content[:10])}... (truncated)\n"
                
                current_file = line.replace("FILE: ", "").strip()
                content = []
            elif line.strip() == "```" or line.startswith("```"):
                continue
            elif current_file:
                content.append(line)
        
        # Save last file
        if current_file:
            self._save_file(current_file, "\n".join(content))

    def _save_file(self, rel_path: str, content: str):
        full_path = os.path.join(self.workspace_path, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)

    def run(self):
        """Executes the task queue."""
        self.setup_workspace()
        for task in self.tasks:
            print(f"Running task: {task['title']}")
            output = generate_code_for_task(
                self.project_name, 
                self.tech_stack, 
                task['prompt'], 
                self.context
            )
            self.write_generated_files(output)
        
        print("All tasks completed.")
        return self.workspace_path

    def create_zip(self, export_dir: str = "exports"):
        """Zips the workspace for download."""
        os.makedirs(export_dir, exist_ok=True)
        zip_name = f"{self.project_name.replace(' ', '_').lower()}.zip"
        zip_path = os.path.join(export_dir, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.workspace_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.workspace_path)
                    zipf.write(file_path, arcname)
        
        return zip_path
