import re
from typing import Tuple
from enum import Enum
from loguru import logger

class DocumentType(str, Enum):
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

class DocumentClassifier:
    def __init__(self):
        self.logger = logger
        self.patterns = {
            DocumentType.SOP: [
                r'\bstandard\s+operating\s+procedure\b',
                r'\bs\.?o\.?p\.?\b',
                r'\bstandard\s+procedure\b'
            ],
            DocumentType.MAINTENANCE_MANUAL: [
                r'\bmaintenance\s+manual\b',
                r'\bservice\s+manual\b',
                r'\brepair\s+manual\b'
            ],
            DocumentType.INSPECTION_REPORT: [
                r'\binspection\s+report\b',
                r'\binspection\s+checklist\b'
            ],
            DocumentType.SAFETY_MANUAL: [
                r'\bsafety\s+manual\b',
                r'\bsafety\s+guidelines\b',
                r'\bhse\s+manual\b'
            ],
            DocumentType.INVOICE: [
                r'\binvoice\b',
                r'\btax\s+invoice\b'
            ],
            DocumentType.PURCHASE_ORDER: [
                r'\bpurchase\s+order\b',
                r'\bp\.?o\.?\s+number\b'
            ],
        }
    
    def classify(self, filename: str, content: str) -> Tuple[DocumentType, float]:
        """Classify document based on filename and content"""
        try:
            self.logger.info(f"Classifying: {filename}")
            
            # Check filename first
            filename_lower = filename.lower()
            
            for doc_type, patterns in self.patterns.items():
                for pattern in patterns:
                    if re.search(pattern, filename_lower, re.IGNORECASE):
                        self.logger.info(f"Classified as: {doc_type.value}")
                        return doc_type, 0.9
            
            # Check content
            if content:
                content_lower = content.lower()
                scores = {}
                
                for doc_type, patterns in self.patterns.items():
                    score = 0
                    for pattern in patterns:
                        matches = len(re.findall(pattern, content_lower, re.IGNORECASE))
                        score += matches
                    scores[doc_type] = score
                
                if scores:
                    best_type = max(scores, key=scores.get)
                    if scores[best_type] > 0:
                        confidence = min(scores[best_type] / 10, 1.0)
                        self.logger.info(f"Classified as: {best_type.value} (confidence: {confidence:.2f})")
                        return best_type, confidence
            
            self.logger.info("Could not classify document")
            return DocumentType.UNKNOWN, 0.0
            
        except Exception as e:
            self.logger.error(f"Classification failed: {e}")
            return DocumentType.UNKNOWN, 0.0
