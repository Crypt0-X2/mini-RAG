"""Ingest router for document ingestion"""
import time
import hashlib
from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse, ChunkDetail
from app.services.chunker import TextChunker

router = APIRouter(prefix="/ingest", tags=["ingest"])

# Initialize chunker with default settings
chunker = TextChunker(chunk_size=1000, chunk_overlap=120)


@router.post("", response_model=IngestResponse)
async def ingest_text(request: IngestRequest):
    """
    Ingest text and store it in the vector database.
    
    This endpoint:
    1. Chunks the input text using sentence-based chunking (1000 tokens, 12% overlap)
    2. Attaches metadata (source, title, section, position) to each chunk
    3. Will generate embeddings and store in Pinecone in Phase 3
    
    For Phase 2, this returns actual chunks with full metadata.
    """
    try:
        # Generate a document ID based on text hash
        doc_id = hashlib.md5(request.text.encode()).hexdigest()[:12]
        
        # Chunk the text with metadata
        chunks = chunker.chunk_text(
            text=request.text,
            source=request.source or "user_input",
            title=request.title,
            section=None  # Could be extracted or provided in future
        )
        
        # Convert chunks to response format
        chunk_details = [
            ChunkDetail(
                text=chunk.text,
                source=chunk.metadata.source,
                title=chunk.metadata.title,
                section=chunk.metadata.section,
                position=chunk.metadata.position,
                token_count=chunk.metadata.token_count
            )
            for chunk in chunks
        ]
        
        # TODO Phase 3: Generate embeddings and upsert to Pinecone
        # For now, we validate chunking works and return details
        
        return IngestResponse(
            success=True,
            message=f"Text chunked successfully into {len(chunks)} chunks. Embedding and storage will be added in Phase 3.",
            chunk_count=len(chunks),
            document_id=doc_id,
            chunks=chunk_details
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest text: {str(e)}"
        )
