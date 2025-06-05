from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

OLLAMA_HOST = "http://ollama:11434"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/query")
def query_model(request: PromptRequest):
    payload = {
        "model": "llama3",
        "prompt": request.prompt,
        "stream": True  # enable streaming response
    }

    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                try:
                    json_data = json.loads(data) if "response" in data else {}
                    full_response += json_data.get("response", "")
                except Exception:
                    pass  # skip malformed lines

        return {"response": full_response.strip()}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
