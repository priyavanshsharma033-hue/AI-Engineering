import requests
import math

URL = "http://localhost:11434/api/embed"
Model = "nomic-embed-text"

def get_Embedding(text):
    response=requests.post(URL, json={"model": Model, "input": text})
    response.raise_for_status()
    result=response.json()
    return result["embeddings"][0]

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.hypot(*v1)
    magnitude_v2 = math.hypot(*v2)
    
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0
    
    return dot_product / (magnitude_v1 * magnitude_v2)

Sentence1 = "Welcome to AIML"
Sentence2 = "Welcome to AI and Machine Learning"    
Sentence3 = "I love the weather today"

Embedding1 = get_Embedding(Sentence1)
Embedding2 = get_Embedding(Sentence2)   
Embedding3 = get_Embedding(Sentence3)

cosine_sim=cosine_similarity(Embedding1, Embedding2)
cosine_dif=cosine_similarity(Embedding1, Embedding3)

print("Sentence 1:", Sentence1)
print("Sentence 2:", Sentence2)
print("Sentence 3:", Sentence3)
print("Cosine Similarity(Sentence 1, Sentence 2) :", cosine_sim)
print("Cosine Similarity(Sentence 1, Sentence 3) :", cosine_dif)