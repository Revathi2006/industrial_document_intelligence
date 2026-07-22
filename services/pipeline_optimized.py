import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
import time
from loguru import logger

class OptimizedPipeline:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.processing_times = {}
    
    async def process_with_timing(self, document_id: int) -> Dict:
        """Process document with performance tracking"""
        start_time = time.time()
        
        # Parallel processing where possible
        tasks = []
        
        # These can run in parallel
        tasks.extend([
            self._extract_text(document_id),
            self._classify_document(document_id),
            self._check_ocr_needed(document_id)
        ])
        
        results = await asyncio.gather(*tasks)
        
        # Sequential processing
        cleaned_text = await self._clean_text(results[0])
        
        # Parallel metadata extraction
        metadata_tasks = await asyncio.gather(
            self._extract_metadata(cleaned_text),
            self._extract_tables(cleaned_text),
            self._extract_images(document_id),
            self._detect_language(cleaned_text)
        )
        
        # Chunking and embedding
        chunks = await self._chunk_text(cleaned_text)
        embeddings = await self._generate_embeddings(chunks)
        
        # Store results
        await self._store_results(document_id, {
            'cleaned_text': cleaned_text,
            'metadata': metadata_tasks[0],
            'tables': metadata_tasks[1],
            'images': metadata_tasks[2],
            'language': metadata_tasks[3],
            'chunks': chunks,
            'embeddings': embeddings
        })
        
        elapsed = time.time() - start_time
        logger.info(f"Document {document_id} processed in {elapsed:.2f} seconds")
        
        return {
            'document_id': document_id,
            'processing_time': elapsed,
            'chunks': len(chunks),
            'embeddings': len(embeddings)
        }
    
    async def quick_upload_mode(self, file_path: str) -> Dict:
        """
        Fast mode: Store immediately, process later
        Returns in 1-2 seconds
        """
        # Quick validation only
        await self._quick_validate(file_path)
        
        # Store file
        doc_id = await self._store_document(file_path)
        
        # Queue for background processing
        await self._queue_for_processing(doc_id)
        
        return {
            'document_id': doc_id,
            'status': 'queued',
            'message': 'Document stored, processing in background'
        }