import requests
import math
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI(title="My RAG API")

URL="http://localhost:11434"
E_MODEL="nomic-embed-text"
C_MODEL="qwen2.5:3b"
THRESHOLD=0.5

from pathlib import Path
KNOWLEDGE_FILE=Path(__file__).parent/"knowledge.txt"

def load_documents():
    text=KNOWLEDGE_FILE.read_text(encoding="UTF-8")

    documents=[
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]
    return documents    
documents=load_documents()
print(f"Loaded {len(documents)} documents")
for i,document in enumerate(documents,start=1):
    print(f"{i},{document}")

class QuestionRequest(BaseModel):
    question: str

def get_embeddings(text):
    response=requests.post(f"{URL}/api/embed",json={"model":E_MODEL,"input":text},timeout=120)
    response.raise_for_status()
    return response.json()["embeddings"][0]

def cosine_similarity(v1,v2):
    dot_product=sum(a*b for a,b in zip(v1,v2))

    mag_1=math.hypot(*v1)
    mag_2=math.hypot(*v2)
    if mag_1==0 or mag_2==0:
     return 0.0
    return dot_product/(mag_1*mag_2)

def Generate_answer(question,context):
   prompt=f"""
    You are an intelligent AI 
    Provide me the answer of the question from the given context
    if the given context does not have enough information about the asked question do not give any answer and tell that the sufficient information is not provided

    context:
    {context}
    question:
    {question}
    Answer:
    """
   response=requests.post(f"{URL}/api/generate",json={"model":C_MODEL,"prompt":prompt,"stream":False,"temperature":0.2},timeout=120)
   response.raise_for_status()
   return response.json()["response"]

@app.get("/")
def home():
   return {"message":"WELCOME! to my rag api","day":13}

@app.post("/ask")
def ask(request:QuestionRequest):
   question=request.question.strip()

   if not question:
      raise HTTPException(
            status_code=400,
         detail="No question was provided"
      )
   try:
      document_embeddings=[get_embeddings(document) for document in documents]
      query_embedding=get_embeddings(question)
      result=[]
      for document,embedding in zip(documents,document_embeddings):
        score=cosine_similarity(query_embedding,embedding)
        result.append((score,document))

      result.sort(reverse=True,key= lambda item:item[0])

      top_result =[(score,document)
                  for score,document in result
                  if score>=THRESHOLD][:3]
      if not top_result:
                  return {
                      "question": question,
                      "answer": (
                          "I couldn't find sufficiently relevant "
                          "information in the knowledge base."
                      ),
                      "retrieved_documents": []
                  }
      
      

      context = "\n".join(document for score,document in top_result)

      answer=Generate_answer(question,context)
      return {
          "question":question,
          "answer":answer,
          "retrieved_documents":[{
                              "text": document,
                              "similarity": round(score, 4)
                          }
                          for score, document in top_result]
      
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

@app.get("/search")
def search(question:str):
     question=question.strip()

     if not question:raise HTTPException(
          status_code=400,
          detail="question was  not provided"
     )
     try:
         document_embedding = [get_embeddings(document) for document in documents]
         query_embedding = get_embeddings(question)
         result = []
         for document, embedding in zip(documents, document_embedding):
             score = cosine_similarity(query_embedding, embedding)
             result.append({
                 "text": document,
                 "similarity": round(score, 4)
             })
         result.sort(key=lambda item: item["similarity"], reverse=True)
         relevant_results = [
             item for item in result
             if item["similarity"] >= THRESHOLD
         ][:3]

         return {
             "question": question,
             "total_results": len(relevant_results),
             "results": relevant_results
         }
     except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Check that Ollama is running."
        )

     except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Ollama timed out. Please try again."
        )

     except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail="An error occurred while communicating with Ollama."
        )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RAG API",
        "day": 13
    }
