import requests
url = "http://localhost:11434/api/embed"

data={
    "model": "nomic-embed-text",
    "input": "Welcome to AIML"
}

response=requests.post(url,json=data)
response.raise_for_status()
result=response.json()
embedding=result["embeddings"][0]


print("Text:", data["input"])
print("No. of values:", len(embedding))
print("First 10 values:", embedding[:10])