from app.core.llm import call_llm

SYSTEM_PROMPT_TEMPLATE = """
You are an expert developer specializing in {tech_stack}.
Your task is to implement a specific part of a project based on the following prompt.

PROJECT CONTEXT:
This is a part of the project: {project_name}

PREVIOUSLY GENERATED FILES (for context):
{context}

TASK:
{task_prompt}

INSTRUCTIONS:
- Generate ONLY the necessary code files.
- For each file, use the following format:
  FILE: path/to/file.ext
  ```
  // code here
  ```
- Do not include explanations unless specifically requested in the prompt.
- Ensure the code is production-ready and follows best practices for {tech_stack}.
"""

def generate_code_for_task(project_name: str, tech_stack: str, task_prompt: str, context: str) -> str:
    """Uses the LLM to generate code for a specific task."""
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        project_name=project_name,
        tech_stack=tech_stack,
        context=context if context else "None yet.",
        task_prompt=task_prompt
    )
    
    prompt = "Generate the code now."
    return call_llm(prompt, system_prompt=system_prompt)
