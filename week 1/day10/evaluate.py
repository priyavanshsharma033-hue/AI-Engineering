import requests
import math
URL="http://localhost:11434/api/embed"
MODEL = "nomic-embed-text"
documents=["Python is a beginner-friendly programming language used to build software, automate tasks, and develop AI applications.",
    "FastAPI is a Python framework used to build backend APIs. It supports HTTP methods such as GET and POST.",
    "Ollama allows developers to run large language models locally on their computers.",
    "Embeddings convert text into numerical vectors that represent aspects of its meaning.",
    "Semantic search finds documents that are similar in meaning to a question, even when the exact words differ.",
    "RAG stands for Retrieval-Augmented Generation. It retrieves relevant information and provides it to an AI model as context.",
    "Qwen2.5 is a family of language models that can generate text and answer questions."
    ]
def get_embeddings(text):
    response=requests.post(URL,json={"model":MODEL,"input":text})
    response.raise_for_status()
    return response.json()["embeddings"][0]

def cosine_similarity(v1,v2):
    dot_product=sum(a*b for a,b in zip(v1,v2))
    mag_1=math.hypot(*v1)
    mag_2=math.hypot(*v2)
    if mag_1 ==0 or mag_2 == 0:
        return 0
    return dot_product/(mag_1*mag_2)

document_embeddings=[get_embeddings(document) for document in documents]
tests = [
    ("How do I create a backend API?",
     "FastAPI is a Python framework"),

    ("How does text become a vector?",
     "Embeddings convert text"),

    ("What does RAG mean?",
     "RAG stands for Retrieval-Augmented Generation")
]

passed =0

for question,expected_text in tests:
    query_embeddings=get_embeddings(question)

    result=[]
    for document,embedding in zip(documents,document_embeddings):
        score=cosine_similarity(query_embeddings,embedding)
        result.append((score,document))

    result.sort(reverse=True,key=lambda item:item[0])
    top_result=result[:3]

    success=any(
        expected_text in document for score, document in top_result
    )

    if success:
        passed+=1

    print(f"\nQuestion: {question}")
    print(f"Expected document found in top 3: {success}")
    print(f"Top result: {result[0][1]}")
    print(f"Top similarity score: {result[0][0]:}")

    print("\n" + "=" *40)
    print(f"Evaluation:{passed}/{len(tests)}passed")
    print("=" *40)


