import requests
import math
URL="http://localhost:11434/api/embed"
Model="nomic-embed-text"
documents=[
    "Python is a high-level programming language.",
    "Java is a popular programming language.",  
    "JavaScript is widely used for web development.",
    "C++ is a powerful programming language.",
    "Ruby is known for its simplicity and productivity.",
    "Go is a statically typed programming language.",]
def get_embedding(text):
    response=requests.post(URL,json={"model":Model,"input":text})
    response.raise_for_status()
    result=response.json()
    return result["embeddings"][0]
def cosine_similarity(v1,v2):
    dot_product=sum(a*b for a,b in zip(v1,v2))
    magnitude_v1=math.hypot(*v1)
    magnitude_v2=math.hypot(*v2)
    if magnitude_v1==0 or magnitude_v2==0:
        return 0
    return dot_product/(magnitude_v1*magnitude_v2)  

document_embeddings=[get_embedding(doc) for doc in documents]

query=input("Enter your query: ")
query_embedding=get_embedding(query)

results=[]
for doc,embedding in zip(documents,document_embeddings):
    similarity=cosine_similarity(query_embedding,embedding)
    results.append((doc,similarity))

results.sort(key=lambda x:x[1],reverse=True)

for score,doc in results:
        print(f"Document: {doc}\nSimilarity Score: {score:}\n")