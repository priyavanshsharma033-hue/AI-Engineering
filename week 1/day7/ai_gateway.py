
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field

app = FastAPI(title="My AI Gateway")


class ChatRequest(BaseModel):
    prompt: str
    temperature: float = Field(default=0.7, ge=0, le=1)

@app.get("/")
def home():
    return {"message": "My AI Gateway is running!"}


@app.post("/chat")
def chat(request: ChatRequest):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:3b",
        "prompt": request.prompt,
        "stream": False,
        "options": {
            "temperature": request.temperature
        }
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()

        return {"answer": result["response"]}

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running"
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The AI took too long to respond"
        )

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Failed to get a response from the AI model"
        )