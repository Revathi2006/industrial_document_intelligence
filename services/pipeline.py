from typing import Dict
from pathlib import Path
from datetime import datetime
from loguru import logger

from .validator import FileValidator
from .extractor import ContentExtractor
from .ocr import OCRProcessor
from .cleaner import TextCleaner
from .metadata import MetadataExtractor
from .chunker import Chunker
from .embeddings import EmbeddingGenerator
from database.models import Document, DocumentStatus, AuditLog

class ProcessingPipeline:
    def __init__(self, db_session):
        self.db_session = db_session
        self.validator = FileValidator()
        self.extractor = ContentExtractor()
        self.ocr = OCRProcessor()
        self.cleaner = TextCleaner()
        self.metadata_extractor = MetadataExtractor()
        self.chunker = Chunker()
        self.embedding_generator = EmbeddingGenerator()
    
    async def process_document(self, document_id: int) -> Dict:
        """Main processing pipeline"""
        try:
            logger.info(f"Starting pipeline for document {document_id}")
            
            # Get document
            from sqlalchemy import select
            query = select(Document).where(Document.id == document_id)
            result = await self.db_session.execute(query)
            document = result.scalar_one_or_none()
            
            if not document:
                raise ValueError(f"Document {document_id} not found")
            
            # Update status
            document.status = DocumentStatus.QUEUED
            document.processing_progress = 5
            await self.db_session.commit()
            
            # Extract content
            document.status = DocumentStatus.EXTRACTING
            document.processing_progress = 20
            await self.db_session.commit()
            
            content = await self.extractor.extract(Path(document.file_path))
            
            # Clean text
            document.status = DocumentStatus.CLEANING
            document.processing_progress = 40
            await self.db_session.commit()
            
            cleaned_text = await self.cleaner.clean_text(content.get('text', ''))
            
            # Extract metadata
            document.status = DocumentStatus.METADATA_EXTRACTING
            document.processing_progress = 60
            await self.db_session.commit()
            
            metadata = await self.metadata_extractor.extract(cleaned_text, document.original_filename)
            
            # Generate chunks
            document.status = DocumentStatus.CHUNKING
            document.processing_progress = 80
            await self.db_session.commit()
            
            chunks = await self.chunker.chunk_text(cleaned_text, document_id)
            
            # Update document - use doc_metadata instead of metadata
            document.doc_metadata = metadata
            document.page_count = content.get('page_count', 0)
            document.word_count = len(cleaned_text.split())
            document.status = DocumentStatus.COMPLETED
            document.processing_progress = 100
            document.processed_at = datetime.utcnow()
            
            await self.db_session.commit()
            
            logger.info(f"✅ Document {document_id} processed successfully")
            
            return {
                'status': 'completed',
                'document_id': document_id,
                'chunks_count': len(chunks),
                'word_count': document.word_count
            }
        
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            if document:
                document.status = DocumentStatus.FAILED
                document.error_message = str(e)
                await self.db_session.commit()
            raise
