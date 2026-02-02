"""Ingest router for document ingestion"""
import time
import hashlib
from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
async def ingest_text(request: IngestRequest):
    """
    Ingest text and store it in the vector database.
    
    This endpoint will:
    1. Chunk the input text
    2. Generate embeddings for each chunk
    3. Store chunks in Pinecone vector database
    
    For Phase 1, this returns a mock response.
    """
    try:
        # For Phase 1, we're just validating the endpoint works
        # Real implementation will come in Phase 2-3
        
        # Generate a simple document ID based on text hash
        doc_id = hashlib.md5(request.text.encode()).hexdigest()[:12]
        
        # Mock chunk count (will be real in Phase 2)
        # Rough estimate: 1 chunk per ~750 characters (assuming ~1000 tokens with overhead)
        estimated_chunks = max(1, len(request.text) // 750)
        
        return IngestResponse(
            success=True,
            message=f"Text ingested successfully. Ready for processing in Phase 2-3.",
            chunk_count=estimated_chunks,
            document_id=doc_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest text: {str(e)}"
        )
