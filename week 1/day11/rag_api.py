from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import math

app = FastAPI(title="My RAG Api")

URL = "http://localhost:11434"
CHAT_MODEL = "qwen2.5:3b"
E_MODEL = "nomic-embed-text"
THRESHOLD = 0.5


documents = [
    "Python is a beginner-friendly programming language used to build software, automate tasks, and develop AI applications.",
    "FastAPI is a Python framework used to build backend APIs. It supports HTTP methods such as GET and POST.",
    "Ollama allows developers to run large language models locally on their computers.",
    "Embeddings convert text into numerical vectors that represent aspects of their meaning.",
    "Semantic search finds documents that are similar in meaning to a question, even when the exact words differ.",
    "RAG stands for Retrieval-Augmented Generation. It retrieves relevant information and provides it to an AI model as context.",
    "Qwen2.5 is a family of language models that can generate text and answer questions."
]


class QuestionRequest(BaseModel):
    question: str


def get_embeddings(text):
    response = requests.post(
        f"{URL}/api/embed",
        json={
            "model": E_MODEL,
            "input": text
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["embeddings"][0]


def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def generate_answer(question, context):
    prompt = f"""
Answer the question using the context below.
If the context is insufficient, say so.
Do not invent facts unsupported by the context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        f"{URL}/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]


@app.get("/")
def home():
    return {
        "message": "My RAG Api is running",
        "day": 11
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="No question was provided"
        )

    try:
        document_embeddings = [
            get_embeddings(document)
            for document in documents
        ]

        query_embeddings = get_embeddings(question)

        result = []

        for document, embedding in zip(
            documents, document_embeddings
        ):
            score = cosine_similarity(
                query_embeddings,
                embedding
            )

            result.append((score, document))

        result.sort(
            reverse=True,
            key=lambda item: item[0]
        )

        top_results = [
            (score, document)
            for score, document in result
            if score >= THRESHOLD
        ][:3]

        if not top_results:
            return {
                "question": question,
                "answer": (
                    "I couldn't find sufficiently relevant "
                    "information in the knowledge base."
                ),
                "retrieved_documents": []
            }

        context = "\n".join(
            document
            for score, document in top_results
        )

        answer = generate_answer(question, context)

        return {
            "question": question,
            "answer": answer,
            "retrieved_documents": [
                {
                    "text": document,
                    "similarity": round(score, 4)
                }
                for score, document in top_results
            ]
        }

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama"
        )

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond"
        )

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Ollama could not process the request"
        )