```markdown
# 🏭 DocFlow Pro

> **Industrial Document Intelligence Platform**
>
> Upload, process, analyze, and chat with your industrial documents using AI.

---

## 👥 Team

| Name | Role |
|------|------|
| 
| **Rattish Kumar S S** | Team Lead & backend |
|  **Revathi S** | AI/ML Engineer |
| **Harini S** | Full Stack Developer |

---

## 📑 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [User Interfaces](#user-interfaces)
- [Database Schema](#database-schema)
- [Processing Pipeline](#processing-pipeline)
- [AI Copilot (RAG)](#ai-copilot-rag)
- [Knowledge Graph](#knowledge-graph)
- [Root Cause Analysis](#root-cause-analysis)
- [Commands Reference](#commands-reference)
- [Tech Stack](#tech-stack)
- [Supported Formats](#supported-formats)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

DocFlow Pro is a complete **Retrieval-Augmented Generation (RAG)** system for industrial documents. Upload equipment manuals, inspection logs, nameplate images, and Excel data — the system automatically extracts text, generates AI-ready chunks, creates vector embeddings, and provides an intelligent chatbot that answers questions based on your documents.

### 🎯 What You Can Do

| Task | How |
|------|-----|
| 📤 Upload documents | Drag & drop PDF, DOCX, XLSX, CSV, images |
| 🔍 Search semantically | Find relevant content by meaning |
| 🤖 Chat with AI | Ask questions, get answers with sources |
| 🔗 Explore relationships | Knowledge graph links equipment to documents |
| 🔧 Analyze failures | Root cause analysis with timeline & recommendations |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                          │
│  /dashboard (Upload)  │  /copilot-ui (Chat)  │  /rca-ui (RCA)│
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER (:8000)                      │
│  /documents/*  │  /copilot/*  │  /kg/*  │  /rca/*            │
└──────────────────────────┬───────────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ PROCESSING  │  │   AI COPILOT    │  │  KNOWLEDGE      │
│ PIPELINE    │  │   (RAG)         │  │  GRAPH          │
│             │  │                 │  │                 │
│ • Extract   │  │ • Embeddings    │  │ • Entities      │
│ • Clean     │  │ • Cosine Search │  │ • Relationships │
│ • Chunk     │  │ • Groq LLM      │  │ • Queries       │
│ • Metadata  │  │ • Context Build │  │                 │
└──────┬──────┘  └────────┬────────┘  └────────┬────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────────────┐
│                     DATA STORAGE                              │
│  SQLite (doc_processor.db)  │  Embeddings (embeddings.pkl)   │
│  Uploads (/uploads/)        │  Logs (/logs/)                 │
└──────────────────────────────────────────────────────────────┘
```

### RAG Flow

```
User Question
     │
     ▼
Embedding Search (384d cosine similarity)
     │
     ▼
Retrieve Top-K Chunks from Database
     │
     ▼
Build Context Prompt
     │
     ▼
Groq LLM (llama-3.1-8b-instant) → Answer + Sources
```

---

## Quick Start

### Prerequisites

- **Python 3.11+** (3.13 works)
- **Tesseract OCR** (for image text extraction)
- **Groq API Key** (free from [console.groq.com](https://console.groq.com))

### Installation

```powershell
# 1. Clone or download the project
cd industrial-doc-processor

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Tesseract (for OCR)
winget install UB-Mannheim.TesseractOCR

# 5. Set Groq API key in copilot/copilot_api.py
# GROQ_API_KEY = "gsk_YOUR_KEY_HERE"

# 6. Start the server
python run.py
```

### Open in Browser

| URL | Page |
|-----|------|
| `http://localhost:8000/dashboard` | Upload & Manage |
| `http://localhost:8000/copilot-ui` | AI Chat |
| `http://localhost:8000/rca-ui` | Root Cause Analysis |
| `http://localhost:8000/docs` | API Documentation |

---

## Features

### 📤 Document Upload & Processing
- **Drag & drop** interface
- **Auto-processing**: Extract → Clean → Chunk → Embed → Store
- **Duplicate detection** via SHA256 hash
- **Progress tracking** with status updates
- **Multi-file upload** support

### 📄 Text Extraction
- **PDF**: PyMuPDF (fitz)
- **Word**: python-docx
- **Excel/CSV**: openpyxl, pandas
- **Images**: Tesseract OCR (nameplates, inspection photos)
- **XML**: ElementTree

### 🧹 Text Cleaning
- Removes headers, footers, watermarks
- Fixes broken OCR words
- Normalizes whitespace and special characters

### 🏷️ Metadata Extraction
- Equipment IDs (e.g., MTR-AL3-001)
- Email addresses
- Dates and versions
- Equipment names and categories

### ✂️ Smart Chunking
- **Normal text**: 500-word segments
- **Tabular data**: Each row becomes its own chunk with header
- Preserves page numbers and sections

### 🧠 Vector Embeddings
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Storage**: Pickle file (`embeddings.pkl`)
- **Search**: Cosine similarity

### 🤖 AI Copilot (RAG)
- **LLM**: Groq (llama-3.1-8b-instant)
- **Context retrieval**: Top-K chunks via embedding search
- **Source citations**: Shows which document and match percentage
- **Equipment-aware**: Detects equipment IDs for precise answers

### 🔗 Knowledge Graph
- Links documents ↔ equipment ↔ categories
- Query by equipment ID, category, or manufacturer
- Relationship mapping

### 🔍 Root Cause Analysis
- Analyzes inspection data for failure patterns
- Builds failure timeline
- Identifies root cause with confidence score
- Generates actionable recommendations

### 🖥️ Modern UI
- Dark theme with gradient accents
- Responsive design
- Real-time statistics
- Professional typography

---

## Project Structure

```
industrial-doc-processor/
│
├── main.py                         # FastAPI application
├── config.py                       # Settings & configuration
├── run.py                          # Server launcher
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
│
├── api/                            # REST API layer
│   ├── __init__.py
│   ├── upload.py                   # POST /documents/upload
│   ├── documents.py                # GET/DELETE /documents/{id}
│   └── search.py                   # GET /documents/search
│
├── services/                       # Processing pipeline
│   ├── __init__.py
│   ├── validator.py                # File validation
│   ├── extractor.py                # Text extraction (PDF/DOCX/OCR)
│   ├── ocr.py                      # Tesseract OCR
│   ├── cleaner.py                  # Text cleaning
│   ├── metadata.py                 # Metadata extraction
│   ├── chunker.py                  # Smart text chunking
│   ├── embeddings.py               # 384d vectors + cosine similarity
│   ├── pipeline.py                 # Processing orchestrator
│   ├── classifier.py               # Document classification
│   ├── table_extractor.py          # Table extraction
│   ├── image_extractor.py          # Image extraction
│   ├── language_detector.py        # Language detection
│   ├── storage.py                  # File storage management
│   └── upload_service.py           # Upload handling
│
├── copilot/                        # AI Copilot module
│   ├── __init__.py
│   ├── retriever.py                # Embedding search & retrieval
│   └── copilot_api.py              # Groq LLM chat endpoint
│
├── knowledge_graph/                # Knowledge graph module
│   ├── __init__.py
│   ├── graph_builder.py            # SQLite knowledge graph
│   └── kg_api.py                   # Graph API endpoints
│
├── root_cause/                     # Root cause analysis module
│   ├── __init__.py
│   ├── agent.py                    # Failure analysis agent
│   └── api.py                      # RCA API endpoints
│
├── database/                       # Database layer
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy ORM models
│   └── connection.py               # Database connection & sessions
│
├── index.html                      # Upload dashboard UI
├── copilot.html                    # AI Chat UI
├── rca.html                        # Root Cause Analysis UI
│
├── uploads/                        # Stored original files
├── embeddings/                     # Vector embeddings (.pkl)
├── extracted/                      # Extracted content
├── logs/                           # Application logs
│
├── view_database.py                # Database viewer tool
├── reindex_docs.py                 # Re-index embeddings
├── show_chunks.py                  # Chunk inspector
├── test_kg.py                      # Knowledge graph tester
└── doc_processor.db                # SQLite database
```

---

## API Reference

### Document Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/documents/upload` | Upload & auto-process documents |
| `GET` | `/documents` | List all documents (with filters) |
| `GET` | `/documents/{id}` | Get document details |
| `DELETE` | `/documents/{id}` | Delete document & all related data |
| `GET` | `/documents/{id}/status` | Get processing status |
| `GET` | `/documents/{id}/metadata` | Get extracted metadata |
| `GET` | `/documents/{id}/chunks` | Get document chunks |
| `GET` | `/documents/search?q=` | Semantic search via embeddings |

### AI Copilot

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/copilot/chat` | Chat with AI (RAG) |
| `GET` | `/copilot/health` | Health check |

**Request Body:**
```json
{
    "question": "What is the motor temperature?",
    "top_k": 3
}
```

**Response:**
```json
{
    "answer": "The winding temperature is 95°C...",
    "sources": ["Motor_Inspection_Log.csv (1 pages) - 42.6% match"],
    "documents_used": ["Motor_Inspection_Log.csv (1 pages) - 42.6% match"]
}
```

### Knowledge Graph

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/kg/query?q=` | Search graph |
| `GET` | `/kg/equipment` | List all equipment |
| `GET` | `/kg/documents` | List all documents |
| `GET` | `/kg/document/{id}/relationships` | Get document relationships |

### Root Cause Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/rca/analyze/{equipment_id}` | Full failure analysis |
| `GET` | `/rca/quick/{equipment_id}` | Quick root cause summary |

---

## Database Schema

### `documents`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| filename | VARCHAR(255) | UUID filename on disk |
| original_filename | VARCHAR(255) | Original uploaded name |
| file_path | VARCHAR(500) | Full file path |
| file_size | INTEGER | Size in bytes |
| file_type | VARCHAR(10) | Extension (.pdf, .docx, etc.) |
| sha256_hash | VARCHAR(64) | Duplicate detection hash |
| status | ENUM | uploaded/extracting/cleaning/chunking/embedding/completed/failed |
| processing_progress | FLOAT | 0.0 to 100.0 |
| doc_metadata | JSON | Extracted metadata |
| page_count | INTEGER | Number of pages |
| word_count | INTEGER | Total words |
| language | VARCHAR(10) | Detected language |
| version | VARCHAR(20) | Document version |
| created_at | TIMESTAMP | Upload timestamp |
| processed_at | TIMESTAMP | Completion timestamp |

### `chunks`
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PK | Auto-increment ID |
| document_id | INTEGER FK | References documents.id |
| chunk_number | INTEGER | Sequential chunk number |
| content | TEXT | Chunk text (500 words) |
| word_count | INTEGER | Words in chunk |
| page_number | INTEGER | Source page |
| section | VARCHAR(255) | Section name |
| qdrant_id | VARCHAR(255) | Embedding reference |
| chunk_metadata | JSON | Additional info |

---

## Processing Pipeline

```
Step 1: UPLOAD
    ↓ Save file with UUID name, check duplicates (SHA256)

Step 2: EXTRACT
    ↓ PyMuPDF (PDF) / python-docx (DOCX) / Tesseract (Images)

Step 3: CLEAN
    ↓ Remove headers, footers, watermarks, normalize text

Step 4: METADATA
    ↓ Extract equipment IDs, emails, dates, versions

Step 5: CHUNK
    ↓ Split into 500-word segments (row-by-row for tabular)

Step 6: EMBED
    ↓ Generate 384d vectors using MiniLM model

Step 7: STORE
    ↓ Save chunks to SQLite, embeddings to embeddings.pkl

Status: COMPLETED ✅
```

---

## Commands Reference

### Server
```powershell
python run.py                    # Start server
Ctrl+C                           # Stop server
```

### Embeddings
```powershell
python reindex_docs.py           # Re-generate all embeddings
```

### Database
```powershell
python view_database.py          # View all database contents
python show_chunks.py            # View chunks
```

### Testing
```powershell
# Test embeddings
python -c "from services.embeddings import embedding_generator; embedding_generator.load_from_disk(); print(embedding_generator.get_stats())"

# Test copilot search
python -c "from copilot.retriever import Retriever; r=Retriever(); c,s=r.get_context('motor',3); print(c[:500])"
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | FastAPI |
| **Server** | Uvicorn |
| **Database** | SQLite + SQLAlchemy |
| **PDF Processing** | PyMuPDF |
| **Word Processing** | python-docx |
| **Excel Processing** | openpyxl, pandas |
| **OCR** | Tesseract + pytesseract |
| **Image Processing** | OpenCV, Pillow |
| **Embeddings** | Sentence-Transformers (MiniLM 384d) |
| **Similarity** | scikit-learn (cosine) |
| **LLM** | Groq (llama-3.1-8b-instant) |
| **NLP** | NLTK, langdetect |
| **Logging** | Loguru |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## Supported Formats

| Format | Extensions | Max Size | Processor |
|--------|-----------|----------|-----------|
| PDF | `.pdf` | 100 MB | PyMuPDF |
| Word Document | `.docx` | 100 MB | python-docx |
| Excel Spreadsheet | `.xlsx` | 100 MB | openpyxl |
| CSV | `.csv` | 100 MB | pandas |
| PNG Image | `.png` | 100 MB | Tesseract OCR |
| JPEG Image | `.jpg`, `.jpeg` | 100 MB | Tesseract OCR |
| TIFF Image | `.tiff`, `.tif` | 100 MB | Tesseract OCR |
| XML | `.xml` | 100 MB | ElementTree |

---

## Troubleshooting

### Server won't start
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### PyMuPDF install fails
```powershell
pip install pymupdf --only-binary=:all:
```

### Tesseract not found
```powershell
winget install UB-Mannheim.TesseractOCR
```

### Embeddings not generating
```powershell
python reindex_docs.py
```

---

## 📄 License

MIT License - Free for personal and commercial use.

---

<p align="center">
  <b>DocFlow Pro v2.0.0</b><br>
  <sub>Industrial Document Intelligence Platform</sub><br>
  <br>
  <b>Team</b><br>
  <sub>Revathi S | Rattish Kumar S S | Harini S</sub><br>
  <br>
  <sub>Built with ❤️ for industrial equipment management</sub>
</p>
```