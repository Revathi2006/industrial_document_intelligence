import uvicorn
from config import settings

if __name__ == "__main__":
    print("🚀 Starting Industrial Document Processor...")
    print(f"📍 API will be available at: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 Documentation at: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )
