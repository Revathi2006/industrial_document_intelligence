
# 🏭 DocFlow Pro- **Industrial Document Intelligence Platform**

>
> An AI-powered RAG system that uploads, processes, analyzes, and chats with industrial documents.
> Supports PDF, DOCX, XLSX, CSV, PNG, JPG, JPEG, TIFF, and XML files with automatic OCR for images.

---

## 👥 Team

| Name | Role | Responsibility |
|------|------|----------------|
| **Rattish Kumar S S** | Team Lead & Backend Developer | Architecture, API, Database, Integration |
| **Revathi S** | AI/ML Engineer | Embeddings, RAG Pipeline, Copilot, Root Cause Analysis |
| **Harini S** | Full Stack Developer | Frontend UI, Knowledge Graph, Testing, Documentation |

---

## 🎯 Real-World Problems Solved

### The Problem
Industrial facilities manage **thousands of documents** — equipment manuals, inspection logs, nameplate images, maintenance records, Excel spreadsheets — scattered across folders, drives, and filing cabinets. When equipment fails, engineers waste **hours searching** for relevant information instead of fixing the problem.

### Our Solution
DocFlow Pro transforms chaotic document storage into an **intelligent, queryable knowledge base**. Upload any industrial document and instantly chat with it using AI.

### Problems We Solve

| # | Real-World Problem | How DocFlow Pro Solves It |
|---|-------------------|---------------------------|
| 1 | **Information Silos** — Documents scattered across computers, folders, and paper files | Centralized repository with drag-and-drop upload for all formats |
| 2 | **Slow Information Retrieval** — Engineers spend 30% of time searching for documents | AI Copilot answers questions in seconds with source citations |
| 3 | **Scanned Documents Unreadable** — Old manuals and nameplates are images, not text | Automatic OCR extracts text from images and scanned PDFs |
| 4 | **Equipment Failure Analysis** — No systematic way to find why equipment failed | Root Cause Analysis agent with timeline, evidence, and recommendations |
| 5 | **Lost Relationships** — Manual and inspection data are disconnected | Knowledge Graph links equipment ↔ manuals ↔ inspection logs |
| 6 | **Duplicate Documents** — Same file stored multiple times | SHA256 hash detection prevents duplicate uploads |
| 7 | **Unstructured Data** — Excel rows and CSV data hard to query individually | Smart chunking gives each data row its own searchable chunk |
| 8 | **No Source Traceability** — Answers without knowing which document they came from | Every AI answer includes document name, page, and match percentage |
| 9 | **Language Barriers** — Multi-lingual workforce in global industries | OCR and text processing support English, Tamil, Hindi, German |
| 10 | **Maintenance Knowledge Loss** — Expert technicians leave, taking knowledge with them | All documents become a permanent, searchable AI knowledge base |

---

### Industry Use Cases

#### 🏭 Manufacturing Plant
- **Before**: Engineer spends 45 minutes finding the right maintenance manual for a failed motor
- **After**: Engineer asks "How to replace bearing on MTR-AL3-001?" and gets answer in 5 seconds with exact manual page reference

#### ⚡ Power Generation
- **Before**: Inspection logs in Excel, turbine manuals in PDF, nameplate photos on phone — no connection
- **After**: Upload all files → AI links everything → "Show all documents for Turbine T-101"

#### 🏗️ Construction Equipment
- **Before**: Service records lost when technician leaves
- **After**: All service data stored and searchable — "What was the last maintenance on Excavator EX-200?"

#### 🏥 Facility Management
- **Before**: Hundreds of equipment manuals in filing cabinets
- **After**: Upload once, chat anytime — "What is the fire pump inspection schedule?"

---

## ✨ Key Advantages

### 🚀 Speed & Efficiency
| Metric | Before DocFlow | With DocFlow |
|--------|---------------|--------------|
| Find relevant document | 15-45 minutes | 5 seconds |
| Extract text from image | Manual typing (30 min) | Automatic OCR (10 sec) |
| Analyze failure patterns | Hours of manual review | Instant analysis |
| Cross-reference documents | Manually open each file | AI does it automatically |
| Onboard new engineers | Weeks of document study | Ask AI and learn instantly |

### 💰 Cost Savings
- **Reduced Downtime**: Faster troubleshooting = less equipment downtime
- **Knowledge Retention**: Expert knowledge preserved even when staff changes
- **No Duplicate Work**: SHA256 prevents storing same document twice
- **Free Tier LLM**: Groq provides free AI inference (no API costs)
- **Open Source Stack**: SQLite, Tesseract, MiniLM — no licensing fees

### 🔒 Security & Reliability
- **Local Storage**: All documents stay on your server, not in cloud
- **Duplicate Detection**: SHA256 hashing prevents redundant storage
- **Audit Trail**: Every upload, process, and deletion is logged
- **Data Persistence**: SQLite database survives server restarts

### 🎨 User Experience
- **Zero Training Needed**: Drag-and-drop interface, natural language chat
- **Multi-Format Support**: 9 file types, no conversion needed
- **Real-Time Processing**: Documents processed in seconds, not hours
- **Source Citations**: Every AI answer shows exactly which document it came from
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🧠 AI Intelligence
- **Semantic Search**: Finds content by meaning, not just keywords
- **Context-Aware**: AI understands equipment IDs, dates, and technical terms
- **Cross-Document Reasoning**: Combines info from manuals, logs, and images
- **Failure Prediction**: Identifies patterns that lead to equipment failure
- **Continuous Learning**: More documents = smarter AI

### 🔧 Technical Advantages
| Feature | Benefit |
|---------|---------|
| Modular Architecture | Easy to add new features and document types |
| REST API | Integrates with existing systems (SAP, Maximo) |
| Vector Embeddings | Fast similarity search across thousands of chunks |
| Smart Chunking | Tabular data gets row-level chunks for precise retrieval |
| Groq LLM | Free, fast, and accurate AI responses |
| OCR Pipeline | Automatic image preprocessing for better text extraction |

---

### 📊 Comparison

| Feature | Traditional DMS | Basic Chatbot | **DocFlow Pro** |
|---------|----------------|---------------|-----------------|
| Multi-format upload | ✅ | ❌ | ✅ |
| OCR for images | ❌ | ❌ | ✅ |
| AI Q&A with sources | ❌ | ❌ | ✅ |
| Knowledge Graph | ❌ | ❌ | ✅ |
| Root Cause Analysis | ❌ | ❌ | ✅ |
| Semantic Search | ❌ | ❌ | ✅ |
| Vector Embeddings | ❌ | ❌ | ✅ |
| Duplicate Detection | ❌ | ❌ | ✅ |
| Free to run | ❌ | ❌ | ✅ |
| Works offline | ✅ | ❌ | ✅ |

---

## 📑 Table of Contents

- [Real-World Problems Solved](#-real-world-problems-solved)
- [Key Advantages](#-key-advantages)
- [Overview](#overview)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Features](#features)
- [OCR Support](#ocr-support)
- [Supported File Types](#supported-file-types)
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
- [Troubleshooting](#troubleshooting)

---

## Overview

DocFlow Pro is a complete **Retrieval-Augmented Generation (RAG)** system for industrial equipment management. Upload equipment manuals, inspection logs, nameplate images, and Excel data — the system automatically extracts text (using OCR for images), generates AI-ready chunks, creates vector embeddings, and provides an intelligent chatbot that answers questions based on your documents.

### 🎯 What You Can Do

| Task | Description |
|------|-------------|
| 📤 **Upload** | Drag & drop PDF, DOCX, XLSX, CSV, Images, XML |
| 🔬 **OCR** | Automatic text extraction from images and scanned PDFs |
| 🔍 **Search** | Semantic search across all documents |
| 🤖 **Chat** | AI-powered Q&A with source citations |
| 🔗 **Graph** | Knowledge graph linking equipment to documents |
| 🔧 **Analyze** | Root cause analysis with failure timeline |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                          │
│  /dashboard (Upload)  │  /copilot-ui (Chat)  │  /rca-ui (RCA)│
└──────────────────────────┬───────────────────────────────────┘
                           │ HTTP/REST
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   FASTAPI SERVER (:8000)                      │
├──────────────────────────────────────────────────────────────┤
│  /documents/*  │  /copilot/*  │  /kg/*  │  /rca/*            │
└──────────────────────────┬───────────────────────────────────┘
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ PROCESSING  │  │   AI COPILOT    │  │  KNOWLEDGE      │
│ PIPELINE    │  │   (RAG)         │  │  GRAPH          │
│             │  │                 │  │                 │
│ • Validate  │  │ • Embed (384d)  │  │ • Entities      │
│ • Extract   │  │ • Cosine Search │  │ • Relationships │
│ • OCR       │  │ • Retrieve Top-K│  │ • Graph Queries │
│ • Clean     │  │ • Groq LLM      │  │ • Visual Links  │
│ • Metadata  │  │ • Source Cite   │  │                 │
│ • Chunk     │  │                 │  │                 │
└──────┬──────┘  └────────┬────────┘  └────────┬────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────────────┐
│                     DATA STORAGE                              │
│  📊 SQLite (doc_processor.db)  │  🧠 Embeddings (.pkl)       │
│  📁 Uploads (/uploads/)        │  📋 Logs (/logs/)           │
└──────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

| Software | Version | Required For |
|----------|---------|--------------|
| Python | 3.11+ | Backend server |
| Tesseract OCR | Latest | Image text extraction |
| Groq API Key | Free | AI Copilot |

### Installation

```powershell
# 1. Navigate to project folder
cd industrial-doc-processor

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Install Tesseract OCR for image processing
winget install UB-Mannheim.TesseractOCR

# 5. Get free Groq API key from https://console.groq.com
#    Then update copilot/copilot_api.py with your key

# 6. Start the server
python run.py
```

### Open in Browser

| URL | Page | Purpose |
|-----|------|---------|
| `http://localhost:8000/dashboard` | Upload Dashboard | Upload & manage documents |
| `http://localhost:8000/copilot-ui` | AI Copilot | Chat with your documents |
| `http://localhost:8000/rca-ui` | Root Cause Analysis | Analyze equipment failures |
| `http://localhost:8000/docs` | API Docs | Interactive Swagger UI |

---
### Output:
<img width="1897" height="950" alt="Screenshot 2026-07-22 232656" src="https://github.com/user-attachments/assets/3598eff2-5073-48fc-bc26-e188beb09cbc" />
<img width="1897" height="944" alt="Screenshot 2026-07-22 232817" src="https://github.com/user-attachments/assets/156bce43-1482-4f13-8745-b14ce4f782fb" />
<img width="1894" height="958" alt="Screenshot 2026-07-22 232940" src="https://github.com/user-attachments/assets/ba102a66-85e9-4451-9708-a0b40041327e" />
<img width="1909" height="939" alt="Screenshot 2026-07-22 233043" src="https://github.com/user-attachments/assets/7922bfb7-ede2-497e-882b-487724d488bf" />
<img width="1903" height="946" alt="Screenshot 2026-07-22 233143" src="https://github.com/user-attachments/assets/5a7182f4-feb0-42b0-9bad-0403dbd3a24a" />
<img width="1898" height="947" alt="Screenshot 2026-07-22 233233" src="https://github.com/user-attachments/assets/ac87d038-c7a6-45f0-b43a-cb7bb744b908" />
<img width="1887" height="955" alt="Screenshot 2026-07-22 233253" src="https://github.com/user-attachments/assets/8f8d7562-4d32-4426-8d93-91c218a61b14" />
<img width="1899" height="958" alt="Screenshot 2026-07-22 233353" src="https://github.com/user-attachments/assets/f69ae79a-1ec5-46f5-ba01-92e1f6273cb0" />
<img width="1904" height="960" alt="Screenshot 2026-07-22 233412" src="https://github.com/user-attachments/assets/655790a9-54c6-4f0f-81b0-5ad78e735800" />
<img width="1881" height="944" alt="Screenshot 2026-07-22 233446" src="https://github.com/user-attachments/assets/d4c2be4f-2ca0-4e27-86c1-c66f80296d2a" />
<img width="1308" height="725" alt="Screenshot 2026-07-22 233457" src="https://github.com/user-attachments/assets/e034fbd3-3e1f-42b1-a708-9b7f15646827" />
<img width="1873" height="942" alt="Screenshot 2026-07-22 233511" src="https://github.com/user-attachments/assets/69b2312b-68b0-4510-a35e-402e46846ab7" />
<img width="1884" height="943" alt="Screenshot 2026-07-22 233535" src="https://github.com/user-attachments/assets/0efddd4b-6e2c-4b9c-91ef-2e0423bb28ad" />


## Features

### 📤 Document Upload & Processing
- **Drag & drop** interface with file type badges
- **Auto-processing**: Extract → OCR → Clean → Chunk → Embed → Store (all in one step)
- **Duplicate detection** via SHA256 hashing
- **Progress tracking** with real-time status updates
- **Multi-file upload** support

### 🔬 OCR (Optical Character Recognition)
- **Automatic PDF detection**: Text-based vs scanned
- **Image preprocessing**: Grayscale, thresholding, denoising
- **Multi-language**: English, Tamil, Hindi, German
- **Confidence scoring**: Quality assessment
- **Nameplate reading**: Equipment specs from photos

### 📄 Text Extraction
PDF (PyMuPDF) | DOCX (python-docx) | XLSX/CSV (openpyxl/pandas) | Images (Tesseract OCR) | XML (ElementTree)

### 🧹 Text Cleaning
Headers/footers removal | Broken word fixing | Whitespace normalization | Watermark removal

### 🏷️ Metadata Extraction
Equipment IDs | Emails | Dates | Versions | Categories | Departments

### ✂️ Smart Chunking
500-word segments for text | Row-by-row chunks for tabular data | Page tracking

### 🧠 Vector Embeddings
MiniLM model | 384 dimensions | Cosine similarity | L2 normalized

### 🤖 AI Copilot (RAG)
Groq LLM | Top-K retrieval | Source citations | Equipment-aware

### 🔗 Knowledge Graph
Equipment ↔ Documents ↔ Categories | Graph queries | Relationship mapping

### 🔍 Root Cause Analysis
Failure timeline | Pattern detection | Root cause identification | Recommendations

### 🖥️ Modern UI
Dark theme | Responsive design | Real-time stats | Professional typography

---

## Supported File Types

| Format | Extensions | Max Size | OCR |
|--------|-----------|----------|-----|
| PDF | `.pdf` | 100 MB | ✅ Scanned |
| Word | `.docx` | 100 MB | No |
| Excel | `.xlsx` | 100 MB | No |
| CSV | `.csv` | 100 MB | No |
| PNG | `.png` | 100 MB | ✅ Yes |
| JPEG | `.jpg`, `.jpeg` | 100 MB | ✅ Yes |
| TIFF | `.tiff`, `.tif` | 100 MB | ✅ Yes |
| XML | `.xml` | 100 MB | No |

---

## Project Structure

```
industrial-doc-processor/
├── main.py, config.py, run.py, requirements.txt
├── api/           # REST API (upload, documents, search)
├── services/      # Processing (extractor, ocr, cleaner, chunker, embeddings, pipeline)
├── copilot/       # AI Copilot (retriever, copilot_api)
├── knowledge_graph/  # Knowledge Graph (graph_builder, kg_api)
├── root_cause/    # Root Cause Analysis (agent, api)
├── database/      # Models & Connection
├── index.html, copilot.html, rca.html  # UIs
├── uploads/, embeddings/, logs/  # Storage
└── doc_processor.db  # Database
```

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/upload` | Upload & process |
| GET | `/documents` | List documents |
| GET | `/documents/{id}` | Get details |
| DELETE | `/documents/{id}` | Delete |
| GET | `/documents/{id}/chunks` | View chunks |
| POST | `/copilot/chat` | AI Chat |
| GET | `/kg/query?q=` | Graph search |
| GET | `/rca/analyze/{id}` | Root cause |

---

## Processing Pipeline

```
UPLOAD → VALIDATE → EXTRACT → OCR → CLEAN → METADATA → CHUNK → EMBED → STORE → ✅
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| Database | SQLite + SQLAlchemy |
| PDF | PyMuPDF |
| OCR | Tesseract + pytesseract |
| Embeddings | Sentence-Transformers (MiniLM 384d) |
| LLM | Groq (llama-3.1-8b-instant) |
| NLP | NLTK, langdetect |
| Frontend | HTML5, CSS3, JavaScript |

---

## Commands Reference

```powershell
python run.py                    # Start server
python reindex_docs.py           # Re-generate embeddings
python view_database.py          # View database
```

---

## Troubleshooting

```powershell
# Port in use
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Tesseract missing
winget install UB-Mannheim.TesseractOCR

# Embeddings not generating
python reindex_docs.py
```

---

## 📄 License

MIT License — Free for personal and commercial use.

---

<p align="center">
  <b>DocFlow Pro v2.0.0</b><br>
  <sub>Industrial Document Intelligence Platform</sub><br>
  <br>
  <b>👥 Team</b><br>
  <sub><b>Rattish Kumar S S</b> — Team Lead & Backend Developer</sub><br>
  <sub><b>Revathi S</b> — AI/ML Engineer</sub><br>
  <sub><b>Harini S</b> — Full Stack Developer</sub><br>
  <br>

</p>
```
