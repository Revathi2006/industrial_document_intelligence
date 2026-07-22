from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
import aiofiles
import uuid
from datetime import datetime
from typing import List
from loguru import logger

from database.connection import get_db
from database.models import Document, DocumentStatus, Chunk
from services.validator import FileValidator
from services.extractor import ContentExtractor
from services.cleaner import TextCleaner
from services.metadata import MetadataExtractor
from services.chunker import Chunker
from config import settings

router = APIRouter()
validator = FileValidator()

@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload AND automatically process documents"""
    try:
        results = []
        
        for file in files:
            logger.info(f"Processing: {file.filename}")
            
            # Save file
            file_id = str(uuid.uuid4())
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{file_id}{file_ext}"
            file_path = settings.UPLOAD_DIR / unique_filename
            
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Validate
            is_valid, msg = await validator.validate_file(file_path, file.filename)
            if not is_valid:
                file_path.unlink()
                continue
            
            # Create document
            document = Document(
                filename=unique_filename,
                original_filename=file.filename,
                file_path=str(file_path),
                file_size=file_path.stat().st_size,
                file_type=file_ext,
                mime_type=file.content_type,
                status=DocumentStatus.EXTRACTING,
                created_at=datetime.utcnow()
            )
            db.add(document)
            await db.commit()
            await db.refresh(document)
            doc_id = document.id
            
            # Extract text
            extractor = ContentExtractor()
            content = await extractor.extract(file_path)
            raw_text = content.get('text', '')
            
            if not raw_text or len(raw_text.strip()) < 10:
                document.status = DocumentStatus.FAILED
                document.error_message = "No text extracted"
                await db.commit()
                continue
            
            # Clean text
            cleaner = TextCleaner()
            cleaned_text = await cleaner.clean_text(raw_text)
            
            # Extract metadata
            metadata_extractor = MetadataExtractor()
            metadata = await metadata_extractor.extract(cleaned_text, file.filename)
            
            # Chunk text
            chunker = Chunker()
            chunks = await chunker.chunk_text(cleaned_text, doc_id)
            
            # Store chunks in database
            for i, chunk_data in enumerate(chunks):
                chunk = Chunk(
                    document_id=doc_id,
                    chunk_number=i + 1,
                    content=chunk_data['text'],
                    word_count=chunk_data.get('word_count', len(chunk_data['text'].split())),
                    page_number=chunk_data.get('page', 1),
                    section=chunk_data.get('section', f'Chunk {i+1}'),
                    chunk_metadata={'embedded': False}
                )
                db.add(chunk)
            
            # Generate embeddings (try/except so it doesn't break if model fails)
            try:
                from services.embeddings import embedding_generator
                embeddings_data = embedding_generator.generate_embeddings(chunks)
                embedding_generator.store_embeddings(doc_id, embeddings_data)
                logger.info(f"Generated {len(embeddings_data)} embeddings")
            except Exception as emb_err:
                logger.warning(f"Embedding generation skipped: {emb_err}")
            
            # Complete
            document.doc_metadata = metadata
            document.page_count = content.get('page_count', 0)
            document.word_count = len(cleaned_text.split())
            document.status = DocumentStatus.COMPLETED
            document.processing_progress = 100
            document.processed_at = datetime.utcnow()
            
            await db.commit()
            
            results.append({
                'id': doc_id,
                'filename': file.filename,
                'status': 'completed',
                'pages': document.page_count,
                'words': document.word_count,
                'chunks': len(chunks)
            })
        
        return JSONResponse(
            status_code=200,
            content={
                'message': f'Processed {len(results)} documents',
                'documents': results
            }
        )
    
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
