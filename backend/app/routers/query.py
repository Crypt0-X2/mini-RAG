"""Query router for answering questions"""
import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, Citation

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query_text(request: QueryRequest):
    """
    Query the vector database and generate an answer with citations.
    
    This endpoint will:
    1. Embed the query
    2. Retrieve relevant chunks from Pinecone
    3. Rerank chunks using Jina Reranker
    4. Generate answer using LLM with citations
    
    For Phase 1, this returns a mock response.
    """
    try:
        start_time = time.time()
        
        # For Phase 1, return a mock response
        # Real implementation will come in Phase 4-6
        
        mock_answer = (
            f"This is a mock answer to your query: '{request.query}'. "
            f"In Phase 4-6, this will retrieve relevant chunks [1], "
            f"rerank them [2], and generate a grounded answer using an LLM [3]."
        )
        
        mock_citations = [
            Citation(
                citation_number=1,
                text="Mock chunk 1: Retrieved from vector database using semantic search.",
                source="mock_source",
                title="Mock Document",
                position=0
            ),
            Citation(
                citation_number=2,
                text="Mock chunk 2: Reranked using Jina Reranker for relevance.",
                source="mock_source",
                title="Mock Document",
                position=1
            ),
            Citation(
                citation_number=3,
                text="Mock chunk 3: Used by LLM to generate grounded response.",
                source="mock_source",
                title="Mock Document",
                position=2
            )
        ]
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        return QueryResponse(
            answer=mock_answer,
            citations=mock_citations[:request.top_k],
            retrieved_chunks=min(request.top_k, 3),
            latency_ms=round(latency_ms, 2)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )
