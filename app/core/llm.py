import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/chat"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")

def call_llm(prompt: str, system_prompt: str = "You are a helpful assistant.", model: str = DEFAULT_MODEL) -> str:
    """Calls the Ollama Cloud API with the given prompt and system prompt."""
    if not OLLAMA_API_KEY:
        return "Error: OLLAMA_API_KEY not found in environment."

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except Exception as e:
        return f"Error calling Ollama Cloud: {e}"
