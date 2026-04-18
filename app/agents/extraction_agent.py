import json
from app.core.llm import call_llm

SYSTEM_PROMPT = """
You are an expert software architect. Your task is to analyze a document containing app requirements and step-by-step prompts.
Extract the target tech stack and convert the step-by-step instructions into a JSON task queue.

The output MUST be a valid JSON object with the following structure:
{
  "project_name": "Name of the project",
  "tech_stack": "Description of the tech stack",
  "tasks": [
    {
      "id": 1,
      "title": "Short title of the task",
      "prompt": "The full detailed prompt for this step",
      "dependencies": []
    }
  ]
}
Only output the JSON. Do not include any other text.
"""

def extract_tasks_from_text(text: str) -> dict:
    """Uses the LLM to parse extracted PDF text into a structured task queue."""
    prompt = f"Analyze the following text and extract the project structure:\n\n{text}"
    response = call_llm(prompt, system_prompt=SYSTEM_PROMPT)
    
    try:
        # Clean response in case LLM adds markdown formatting
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
            
        return json.loads(response)
    except Exception as e:
        print(f"Error parsing Extraction Agent response: {e}")
        return {"error": "Failed to parse tasks", "raw_response": response}
