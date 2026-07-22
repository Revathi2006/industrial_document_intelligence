from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from services.embeddings import embedding_generator

router = APIRouter()

@router.get("/search")
async def search_for_rag(
    q: str = Query(..., description="User's question"),
    top_k: int = Query(3, ge=1, le=10),
    threshold: float = Query(0.3, ge=0.0, le=1.0)
):
    """
    🔍 RAG Search - Find relevant chunks for chatbot
    Returns the most relevant text chunks with similarity scores
    """
    try:
        logger.info(f"RAG Search: '{q}'")
        
        # Search embeddings
        results = embedding_generator.search_similar(q, top_k=top_k)
        
        # Filter and format for RAG
        rag_results = []
        for r in results:
            if r['similarity_score'] >= threshold:
                rag_results.append({
                    'document_id': r['document_id'],
                    'chunk_id': r['chunk_id'],
                    'content': r['text'],  # The actual text for LLM context
                    'score': round(r['similarity_score'], 4),
                    'relevance': f"{r['similarity_score']*100:.1f}%"
                })
        
        # Format context for chatbot
        context = "\n\n---\n\n".join([r['content'] for r in rag_results])
        
        return {
            'query': q,
            'results_count': len(rag_results),
            'results': rag_results,
            'context_for_llm': context,  # Ready to feed into ChatGPT/Claude
            'stats': embedding_generator.get_stats()
        }
    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
