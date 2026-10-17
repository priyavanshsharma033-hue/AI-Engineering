import requests
import math
URL = "http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"
documents = [
    "Python is a beginner-friendly programming language used to build software, automate tasks, and develop AI applications.",
    "FastAPI is a Python framework used to build backend APIs. It supports HTTP methods such as GET and POST.",
    "Ollama allows developers to run large language models locally on their computers.",
    "Embeddings convert text into numerical vectors that represent aspects of its meaning.",
    "Semantic search finds documents that are similar in meaning to a question, even when the exact words differ.",
    "RAG stands for Retrieval-Augmented Generation. It retrieves relevant information and provides it to an AI model as context.",
    "Qwen2.5 is a family of language models that can generate text and answer questions."
]

def get_embeddings(text):
    response = requests.post(URL, json={"model": MODEL, "input": text},timeout=120)
    response.raise_for_status()
    return response.json()["embeddings"][0]
def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.hypot(*vec1)
    magnitude2 = math.hypot(*vec2)
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    return dot_product / (magnitude1 * magnitude2)

def generate_answer(query, context):
    url = "http://localhost:11434/api/generate"

    prompt = f"""
You are a helpful AI assistant.
Answer the question using the context below.
If the context does not contain enough information,
say that you do not have enough information.

Context:
{context}

Question:
{query}

Answer:
"""

    response = requests.post(
        url,
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]


Documents_embeddings = [get_embeddings(doc) for doc in documents]

query=input("Enter your query: ")
query_embedding = get_embeddings(query)

results=[]
for document,embedding in zip(documents,Documents_embeddings):
    score=cosine_similarity(query_embedding,embedding)
    results.append((score, document))

    results.sort(key=lambda item: item[0], reverse=True)



top_results = results[:3]

context = "\n".join(
    document for score, document in top_results
)

print("\nRetrieved context:")
print(context)

print("\nGenerating answer...")

answer = generate_answer(query, context)

print("\nAI Answer:")
print(answer)
    

