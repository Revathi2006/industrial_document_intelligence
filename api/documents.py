from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from datetime import datetime
from pathlib import Path
from loguru import logger

from database.connection import get_db
from database.models import Document, DocumentStatus, DocumentType, AuditLog, Chunk
from services.pipeline import ProcessingPipeline

router = APIRouter()

@router.get("")
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[DocumentStatus] = None,
    doc_type: Optional[DocumentType] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all documents with optional filters"""
    try:
        query = select(Document)
        
        if status:
            query = query.where(Document.status == status)
        if doc_type:
            query = query.where(Document.document_type == doc_type)
        
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        query = query.offset(skip).limit(limit).order_by(Document.created_at.desc())
        result = await db.execute(query)
        documents = result.scalars().all()
        
        return {
            'total': total,
            'skip': skip,
            'limit': limit,
            'documents': [
                {
                    'id': doc.id,
                    'filename': doc.original_filename,
                    'type': doc.document_type.value if doc.document_type else None,
                    'status': doc.status.value if doc.status else None,
                    'file_size': doc.file_size,
                    'page_count': doc.page_count,
                    'word_count': doc.word_count,
                    'language': doc.language,
                    'version': doc.version,
                    'created_at': doc.created_at.isoformat() if doc.created_at else None,
                    'processed_at': doc.processed_at.isoformat() if doc.processed_at else None,
                    'progress': doc.processing_progress
                }
                for doc in documents
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/process")
async def process_document(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Process a document through the extraction pipeline"""
    try:
        # Check if document exists
        query = select(Document).where(Document.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Check if already processed
        if document.status == DocumentStatus.COMPLETED:
            return {
                "message": "Document already processed",
                "document_id": document_id,
                "status": "completed"
            }
        
        # Run processing in background
        background_tasks.add_task(process_in_background, document_id)
        
        return {
            "message": "Processing started",
            "document_id": document_id,
            "status": "processing"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Process request failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_in_background(document_id: int):
    """Background processing task"""
    from database.connection import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        try:
            pipeline = ProcessingPipeline(session)
            result = await pipeline.process_document(document_id)
            logger.info(f"Document {document_id} processed: {result}")
        except Exception as e:
            logger.error(f"Processing failed for document {document_id}: {e}")

@router.get("/{document_id}")
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get document details"""
    try:
        query = select(Document).where(Document.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            'id': document.id,
            'filename': document.original_filename,
            'file_type': document.file_type,
            'file_size': document.file_size,
            'document_type': document.document_type.value if document.document_type else None,
            'status': document.status.value if document.status else None,
            'progress': document.processing_progress,
            'metadata': document.doc_metadata,
            'page_count': document.page_count,
            'word_count': document.word_count,
            'language': document.language,
            'version': document.version,
            'created_at': document.created_at.isoformat() if document.created_at else None,
            'processed_at': document.processed_at.isoformat() if document.processed_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete document"""
    try:
        query = select(Document).where(Document.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()
        
        await db.delete(document)
        await db.commit()
        
        return {"message": f"Document {document_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}/status")
async def get_document_status(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get processing status"""
    try:
        query = select(Document).where(Document.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            'id': document.id,
            'status': document.status.value if document.status else None,
            'progress': document.processing_progress,
            'error': document.error_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}/metadata")
async def get_document_metadata(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get extracted metadata"""
    try:
        query = select(Document).where(Document.id == document_id)
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            'document_id': document.id,
            'metadata': document.doc_metadata,
            'document_type': document.document_type.value if document.document_type else None,
            'language': document.language,
            'version': document.version,
            'page_count': document.page_count,
            'word_count': document.word_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}/chunks")
async def get_document_chunks(
    document_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get document chunks"""
    try:
        query = select(Chunk).where(Chunk.document_id == document_id)
        query = query.offset(skip).limit(limit).order_by(Chunk.chunk_number)
        result = await db.execute(query)
        chunks = result.scalars().all()
        
        return {
            'document_id': document_id,
            'chunks': [
                {
                    'id': chunk.id,
                    'chunk_number': chunk.chunk_number,
                    'content': chunk.content,
                    'word_count': chunk.word_count,
                    'page_number': chunk.page_number,
                    'section': chunk.section
                }
                for chunk in chunks
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
