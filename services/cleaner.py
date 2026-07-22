import re
from typing import List, Dict
from loguru import logger
import nltk
from nltk.corpus import stopwords

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
        # Common patterns in industrial documents
        self.patterns_to_remove = [
            # Headers and footers
            r'^Page\s+\d+\s+of\s+\d+$',
            r'^CONFIDENTIAL$',
            r'^DRAFT$',
            r'^For Internal Use Only$',
            
            # Common watermarks
            r'CONFIDENTIAL',
            r'DRAFT',
            r'COPY',
            r'SAMPLE',
            
            # Page numbers
            r'^\d+$',
            r'^-\s*\d+\s*-$',
            
            # Repeated headers
            r'^(Company|Department|Document)\s+(Name|Title|ID):',
        ]
    
    async def clean_text(self, text: str, metadata: Dict = None) -> str:
        """
        Clean and normalize extracted text
        
        Args:
            text: Raw text to clean
            metadata: Optional metadata for context-aware cleaning
        
        Returns:
            Cleaned text
        """
        try:
            # Step 1: Remove headers and footers
            text = self._remove_headers_footers(text)
            
            # Step 2: Remove watermarks
            text = self._remove_watermarks(text)
            
            # Step 3: Remove page numbers
            text = self._remove_page_numbers(text)
            
            # Step 4: Clean whitespace
            text = self._clean_whitespace(text)
            
            # Step 5: Fix broken OCR words
            text = self._fix_broken_words(text)
            
            # Step 6: Remove repeated lines
            text = self._remove_repeated_lines(text)
            
            # Step 7: Normalize special characters
            text = self._normalize_characters(text)
            
            # Step 8: Remove empty lines
            text = self._remove_empty_lines(text)
            
            return text.strip()
        
        except Exception as e:
            logger.error(f"Text cleaning failed: {e}")
            raise
    
    def _remove_headers_footers(self, text: str) -> str:
        """Remove common header/footer patterns"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            should_keep = True
            
            for pattern in self.patterns_to_remove:
                if re.match(pattern, line.strip(), re.IGNORECASE):
                    should_keep = False
                    break
            
            if should_keep:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _remove_watermarks(self, text: str) -> str:
        """Remove watermark text"""
        watermark_patterns = [
            r'CONFIDENTIAL',
            r'DRAFT',
            r'DO NOT COPY',
            r'INTERNAL USE ONLY',
            r'PROPRIETARY'
        ]
        
        for pattern in watermark_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text
    
    def _remove_page_numbers(self, text: str) -> str:
        """Remove standalone page numbers"""
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Keep if it's not just a number
            if not re.match(r'^\d{1,4}$', stripped):
                # Keep if it's not "Page X of Y"
                if not re.match(r'^Page\s+\d+\s+of\s+\d+$', stripped, re.IGNORECASE):
                    cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _clean_whitespace(self, text: str) -> str:
        """Normalize whitespace"""
        # Remove multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove spaces at start/end of lines
        text = '\n'.join(line.strip() for line in text.split('\n'))
        
        return text
    
    def _fix_broken_words(self, text: str) -> str:
        """Fix common OCR errors and broken words"""
        # Fix hyphenated line breaks
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        
        # Fix repeated words (common OCR error)
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
        
        # Remove artifacts
        text = re.sub(r'[|]{2,}', '', text)
        
        return text
    
    def _remove_repeated_lines(self, text: str) -> str:
        """Remove consecutive duplicate lines"""
        lines = text.split('\n')
        cleaned_lines = []
        prev_line = ""
        
        for line in lines:
            stripped = line.strip()
            if stripped and stripped != prev_line:
                cleaned_lines.append(line)
            prev_line = stripped
        
        return '\n'.join(cleaned_lines)
    
    def _normalize_characters(self, text: str) -> str:
        """Normalize special characters and quotes"""
        # Replace smart quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Replace other special characters
        text = text.replace('—', '-').replace('–', '-')
        text = text.replace('…', '...')
        
        # Remove non-printable characters (keep basic set)
        text = re.sub(r'[^\x20-\x7E\n\xA0-\xFF\u0100-\u017F\u0400-\u04FF\u0600-\u06FF\u0B80-\u0BFF]', '', text)
        
        return text
    
    def _remove_empty_lines(self, text: str) -> str:
        """Remove completely empty lines"""
        lines = text.split('\n')
        return '\n'.join(line for line in lines if line.strip())