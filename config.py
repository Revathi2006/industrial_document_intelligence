import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Project Paths
    BASE_DIR: Path = Path(__file__).resolve().parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    EXTRACTED_DIR: Path = BASE_DIR / "extracted"
    EMBEDDINGS_DIR: Path = BASE_DIR / "embeddings"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Database - Using SQLite (No PostgreSQL needed!)
    DATABASE_URL: str = "sqlite+aiosqlite:///./doc_processor.db"
    
    # File Upload
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".docx", ".xlsx", ".csv",
        ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".xml" 
    ]
    
    # Processing
    CHUNK_SIZE: int = 500
    EMBEDDING_MODEL: str = "BAAI/bge-m3"
    EMBEDDING_DIMENSION: int = 1024
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Qdrant (optional - can skip for now)
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "documents"
    
    # Groq API Key (loaded from .env)
    GROQ_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create directories
for dir_path in [settings.UPLOAD_DIR, settings.EXTRACTED_DIR, 
                  settings.EMBEDDINGS_DIR, settings.LOGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

print(f"✅ Configuration loaded")
print(f"📁 Database: SQLite (doc_processor.db)")
print(f"📁 Upload dir: {settings.UPLOAD_DIR}")