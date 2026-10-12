
import requests


def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()
        return result["response"]

    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Please start Ollama."

    except requests.exceptions.Timeout:
        return "Error: The AI took too long to respond."

    except requests.exceptions.RequestException as error:
        return f"Request error: {error}"


question = input("Ask the AI something: ")

answer = ask_ai(question)

print("\nAI Response:")
print(answer)