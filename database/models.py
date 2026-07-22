from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, 
    Boolean, JSON, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class DocumentStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    VALIDATING = "validating"
    CLASSIFYING = "classifying"
    EXTRACTING = "extracting"
    OCR_PROCESSING = "ocr_processing"
    CLEANING = "cleaning"
    METADATA_EXTRACTING = "metadata_extracting"
    TABLE_EXTRACTING = "table_extracting"
    IMAGE_EXTRACTING = "image_extracting"
    LANGUAGE_DETECTING = "language_detecting"
    CHUNKING = "chunking"
    EMBEDDING = "embedding"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentType(str, enum.Enum):
    SOP = "SOP"
    MAINTENANCE_MANUAL = "Maintenance Manual"
    INSPECTION_REPORT = "Inspection Report"
    INCIDENT_REPORT = "Incident Report"
    WORK_INSTRUCTION = "Work Instruction"
    SAFETY_MANUAL = "Safety Manual"
    MACHINE_SPECIFICATION = "Machine Specification"
    CALIBRATION_REPORT = "Calibration Report"
    INVOICE = "Invoice"
    PURCHASE_ORDER = "Purchase Order"
    TECHNICAL_DRAWING = "Technical Drawing"
    UNKNOWN = "Unknown"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(10))
    mime_type = Column(String(100))
    sha256_hash = Column(String(64), unique=True, index=True)
    
    # Classification
    document_type = Column(SQLEnum(DocumentType), default=DocumentType.UNKNOWN)
    classification_confidence = Column(Float)
    
    # Status
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.UPLOADED)
    processing_progress = Column(Float, default=0.0)
    error_message = Column(Text)
    
    # Document Metadata (renamed from 'metadata' to 'doc_metadata')
    doc_metadata = Column(JSON)
    page_count = Column(Integer)
    word_count = Column(Integer)
    language = Column(String(10))
    
    # Versioning
    version = Column(String(20), default="1.0")
    is_latest = Column(Boolean, default=True)
    parent_document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True))
    
    # Relationships
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    extracted_images = relationship("ExtractedImage", back_populates="document", cascade="all, delete-orphan")
    extracted_tables = relationship("ExtractedTable", back_populates="document", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    chunk_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    word_count = Column(Integer)
    page_number = Column(Integer)
    section = Column(String(255))
    
    # Embedding reference
    embedding_id = Column(String(255))
    qdrant_id = Column(String(255), index=True)
    
    # Chunk metadata
    chunk_metadata = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    document = relationship("Document", back_populates="chunks")

class ExtractedImage(Base):
    __tablename__ = "extracted_images"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    image_path = Column(String(500), nullable=False)
    page_number = Column(Integer)
    caption = Column(Text)
    position_x = Column(Float)
    position_y = Column(Float)
    width = Column(Float)
    height = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    document = relationship("Document", back_populates="extracted_images")

class ExtractedTable(Base):
    __tablename__ = "extracted_tables"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    table_data = Column(JSON, nullable=False)
    page_number = Column(Integer)
    table_number = Column(Integer)
    caption = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    document = relationship("Document", back_populates="extracted_tables")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    action = Column(String(50), nullable=False)
    details = Column(JSON)
    user_id = Column(Integer)
    ip_address = Column(String(45))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    document = relationship("Document", back_populates="audit_logs")

class ProcessingQueue(Base):
    __tablename__ = "processing_queue"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), unique=True)
    priority = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    current_step = Column(String(50))
    step_progress = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
