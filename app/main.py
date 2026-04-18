import os
import uuid
from typing import Optional
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.utils.pdf_parser import extract_text_from_pdf
from app.agents.extraction_agent import extract_tasks_from_text
from app.agents.supervisor import Supervisor
from app.utils.github_helper import push_to_github

app = FastAPI(title="PDF to App Multi-Agent System")

# Mount frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def get_frontend():
    return FileResponse("frontend/index.html")

# In-memory status tracking
job_status = {}

class ProjectStatus(BaseModel):
    job_id: str
    status: str
    workspace_path: Optional[str] = None
    zip_path: Optional[str] = None
    github_url: Optional[str] = None

@app.post("/generate", response_model=dict)
async def generate_app(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    github_token: Optional[str] = None
):
    job_id = str(uuid.uuid4())
    job_status[job_id] = {"status": "Starting..."}
    
    # Save PDF temporarily
    temp_pdf_path = f"temp_{job_id}.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(await file.read())
        
    background_tasks.add_task(run_pipeline, job_id, temp_pdf_path, github_token)
    
    return {"job_id": job_id, "message": "Project generation started in the background."}

@app.get("/status/{job_id}", response_model=dict)
async def get_status(job_id: str):
    if job_id not in job_status:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_status[job_id]

@app.get("/download/{job_id}")
async def download_zip(job_id: str):
    if job_id not in job_status or "zip_path" not in job_status[job_id]:
        raise HTTPException(status_code=404, detail="Zip file not ready or job not found")
    
    return FileResponse(
        job_status[job_id]["zip_path"], 
        media_type='application/zip', 
        filename=os.path.basename(job_status[job_id]["zip_path"])
    )

async def run_pipeline(job_id: str, pdf_path: str, github_token: str):
    try:
        # 1. Extraction
        job_status[job_id]["status"] = "Extracting text from PDF..."
        text = extract_text_from_pdf(pdf_path)
        
        job_status[job_id]["status"] = "Parsing tasks with AI..."
        project_data = extract_tasks_from_text(text)
        
        if "error" in project_data:
            job_status[job_id]["status"] = f"Failed: {project_data['error']}"
            return

        # 2. Orchestration
        job_status[job_id]["status"] = f"Generating code for {project_data['project_name']}..."
        supervisor = Supervisor(project_data)
        workspace_path = supervisor.run()
        job_status[job_id]["workspace_path"] = workspace_path
        
        # 3. Zip Generation
        job_status[job_id]["status"] = "Creating zip archive..."
        zip_path = supervisor.create_zip()
        job_status[job_id]["zip_path"] = zip_path
        
        # 4. GitHub Push (Optional)
        if github_token:
            job_status[job_id]["status"] = "Pushing to GitHub..."
            github_result = push_to_github(
                workspace_path, 
                project_data['project_name'].replace(" ", "-").lower(), 
                github_token
            )
            job_status[job_id]["github_url"] = github_result
            
        job_status[job_id]["status"] = "Completed"
        
    except Exception as e:
        job_status[job_id]["status"] = f"Error: {str(e)}"
    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
