import hashlib
import magic
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger
import aiofiles

from config import settings

class FileValidator:
    def __init__(self):
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        self.max_file_size = settings.MAX_FILE_SIZE
    
    async def validate_file(self, file_path: Path, original_filename: str) -> Tuple[bool, str]:
        """Comprehensive file validation"""
        
        # Check extension
        ext = Path(original_filename).suffix.lower()
        if ext not in self.allowed_extensions:
            return False, f"File type '{ext}' is not supported"
        
        # Check file size
        try:
            size = file_path.stat().st_size
            if size > self.max_file_size:
                return False, f"File size ({size / (1024*1024):.2f} MB) exceeds limit"
            if size == 0:
                return False, "File is empty"
        except Exception as e:
            return False, f"Size check failed: {str(e)}"
        
        return True, "File validation passed"
    
    async def calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash"""
        sha256_hash = hashlib.sha256()
        
        try:
            async with aiofiles.open(file_path, "rb") as f:
                while chunk := await f.read(8192):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Hash calculation failed: {e}")
            raise
    
    async def check_duplicate(self, file_path: Path, db_session) -> Optional[str]:
        """Check if file already exists"""
        file_hash = await self.calculate_hash(file_path)
        
        from database.models import Document
        from sqlalchemy import select
        
        query = select(Document).where(Document.sha256_hash == file_hash)
        result = await db_session.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            return f"Duplicate found: {existing.original_filename}"
        
        return None
