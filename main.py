from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

from api.upload import router as upload_router
from api.documents import router as documents_router
from api.search import router as search_router
from copilot.copilot_api import router as copilot_router          # 👈 ADD THIS
from database.connection import init_db
from config import settings
from knowledge_graph.kg_api import router as kg_router
from root_cause.api import router as rca_router


# Add with other routers:

logger.remove()
logger.add(settings.LOGS_DIR / "app.log", rotation="500 MB", retention="10 days", level="INFO")
logger.add(sys.stdout, level="INFO")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Industrial Document Processor - Module 1")
    await init_db()
    logger.info("✅ Database initialized")
    yield
    logger.info("👋 Shutting down Module 1")

app = FastAPI(
    title="Industrial Document Processor",
    description="Smart Document Upload & Processing System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/documents", tags=["Upload"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(search_router, prefix="/documents", tags=["Search"])
app.include_router(copilot_router, prefix="/copilot", tags=["Copilot"])  # 👈 ADD THIS
app.include_router(kg_router, prefix="/kg", tags=["Knowledge Graph"])
app.include_router(rca_router, prefix="/rca", tags=["Root Cause"])
@app.get("/")
async def root():
    return {
        "module": "Module 1 - Document Processing Pipeline",
        "version": "1.0.0",
        "status": "operational",
        "dashboard": "/dashboard",
        "api_docs": "/docs"
    }

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    dashboard_path = settings.BASE_DIR / "index.html"
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)

@app.get("/copilot-ui", response_class=HTMLResponse)               # 👈 ADD THIS
async def copilot_ui():
    copilot_path = settings.BASE_DIR / "copilot.html"
    if copilot_path.exists():
        with open(copilot_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Copilot not found</h1>", status_code=404) # Add these imports at the top
from fastapi.responses import HTMLResponse

# Add these routes at the bottom of main.py
@app.get("/copilot-ui", response_class=HTMLResponse)
async def copilot_ui():
    path = settings.BASE_DIR / "copilot.html"
    return HTMLResponse(content=path.read_text(encoding='utf-8')) if path.exists() else HTMLResponse("<h1>Copilot UI not found</h1>")

@app.get("/rca-ui", response_class=HTMLResponse)
async def rca_ui():
    path = settings.BASE_DIR / "rca.html"
    return HTMLResponse(content=path.read_text(encoding='utf-8')) if path.exists() else HTMLResponse("<h1>RCA UI not found</h1>")