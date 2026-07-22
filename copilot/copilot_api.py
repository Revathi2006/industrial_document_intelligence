from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
from copilot.retriever import Retriever
import re

router = APIRouter()
retriever = Retriever()

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-default-key")
client = Groq(api_key=GROQ_API_KEY)


class ChatRequest(BaseModel):
    question: str
    top_k: int = 3

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        context, sources = retriever.get_context(request.question, request.top_k)
        
        if not context:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "documents": []
            }
        
        prompt = f"""You are an industrial equipment expert. Answer based on context below.

Context:
{context[:3000]}

Question: {request.question}

Answer (be specific, mention document names and values):"""
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        # Get unique documents used
        docs_used = []
        seen = set()
        for s in sources:
            doc_name = s.split(' (')[0] if ' (' in s else s
            if doc_name not in seen:
                seen.add(doc_name)
                docs_used.append(s)
        
        return {
            "answer": answer,
            "sources": sources,
            "documents_used": docs_used
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)[:200]}",
            "sources": [],
            "documents_used": []
        }