from pathlib import Path
from typing import Dict
from loguru import logger
import shutil
from config import settings

class StorageManager:
    def __init__(self):
        self.logger = logger
    
    async def store_processed_files(self, document, results: Dict):
        '''Store processed files'''
        try:
            doc_id = document.id
            self.logger.info(f"Storing files for document {doc_id}")
            
            # Create document-specific directory
            doc_dir = settings.EXTRACTED_DIR / str(doc_id)
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Store extracted text
            text_path = doc_dir / "extracted_text.txt"
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(results.get('cleaned_text', ''))
            
            self.logger.info(f"Files stored for document {doc_id}")
        except Exception as e:
            self.logger.error(f"Storage failed: {e}")
            raise
