"""Query router for answering questions"""
import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse, Citation
from app.services.retrieval_service import RetrievalService

router = APIRouter(prefix="/query", tags=["query"])

# Initialize retrieval service
retrieval_service = None


def get_retrieval_service():
    """Get or create retrieval service instance"""
    global retrieval_service
    if retrieval_service is None:
        retrieval_service = RetrievalService(top_k=20, lambda_param=0.5)
    return retrieval_service


@router.post("", response_model=QueryResponse)
async def query_text(request: QueryRequest):
    """
    Query the vector database and generate an answer with citations.
    
    This endpoint will:
    1. Embed the query
    2. Retrieve relevant chunks from Pinecone (Phase 4) ✓
    3. Rerank chunks using Jina Reranker (Phase 5)
    4. Generate answer using LLM with citations (Phase 6)
    
    Phase 4: Retrieval with MMR
    """
    try:
        start_time = time.time()
        
        # Phase 4: Retrieve relevant chunks
        retrieval = get_retrieval_service()
        results = retrieval.retrieve(
            query=request.query,
            top_k=request.top_k or 20
        )
        
        retrieved_chunks = results["chunks"]
        
        if not retrieved_chunks:
            raise HTTPException(
                status_code=404,
                detail="No relevant chunks found in the database"
            )
        
        # Phase 4: Format chunks as citations (mock answer for now)
        citations = [
            Citation(
                citation_number=i + 1,
                text=chunk["text"],
                source=chunk["metadata"].get("source"),
                title=chunk["metadata"].get("title"),
                position=chunk["metadata"].get("position")
            )
            for i, chunk in enumerate(retrieved_chunks)
        ]
        
        # Phase 4: Generate mock answer with citations
        # Real LLM answering will be in Phase 6
        mock_answer = (
            f"Based on the retrieved chunks [1-{len(retrieved_chunks)}]: "
            f"The top-{len(retrieved_chunks)} most relevant chunks have been retrieved using MMR. "
            f"Phases 5-6 will rerank these and generate a grounded answer."
        )
        
        elapsed_time = time.time() - start_time
        
        return QueryResponse(
            answer=mock_answer,
            citations=citations,
            retrieved_chunks=len(retrieved_chunks),
            latency_ms=elapsed_time * 1000
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query: {str(e)}"
        )
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
