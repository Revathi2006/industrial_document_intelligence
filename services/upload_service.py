from pathlib import Path
import aiofiles
import uuid
from loguru import logger
from config import settings

class UploadService:
    def __init__(self):
        self.logger = logger
    
    async def save_uploaded_file(self, file_content: bytes, original_filename: str) -> Path:
        """Save uploaded file to disk"""
        try:
            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_ext = Path(original_filename).suffix.lower()
            unique_filename = f"{file_id}{file_ext}"
            file_path = settings.UPLOAD_DIR / unique_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
            
            self.logger.info(f"Saved file: {unique_filename}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Failed to save file: {e}")
            raise
    
    async def delete_file(self, file_path: Path):
        """Delete a file"""
        try:
            if file_path.exists():
                file_path.unlink()
                self.logger.info(f"Deleted file: {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
