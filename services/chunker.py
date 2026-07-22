import re
from typing import List, Dict
from loguru import logger

class Chunker:
    def __init__(self):
        self.logger = logger
    
    async def chunk_text(self, text: str, document_id: int, chunk_size: int = 500) -> List[Dict]:
        try:
            if not text or len(text.strip()) == 0:
                return []
            
            # Tabular data - split by rows
            if self._is_tabular(text):
                return self._chunk_by_rows(text, document_id)
            
            # Normal text
            return self._chunk_normal(text, document_id, chunk_size)
            
        except Exception as e:
            self.logger.error(f"Chunking failed: {e}")
            return []
    
    def _is_tabular(self, text: str) -> bool:
        """Check if text is tabular data"""
        lines = text.strip().split('\n')
        if len(lines) < 2:
            return False
        # Check for CSV/TSV patterns
        return ('\t' in lines[0] or ',' in lines[0] or '|' in lines[0] or 
                'Equipment_ID' in text or 'Winding_Temp' in text or
                lines[0].count('  ') > 3)
    
    def _chunk_by_rows(self, text: str, document_id: int) -> List[Dict]:
        """Each data row becomes its own chunk"""
        lines = text.strip().split('\n')
        
        # Find header (first meaningful line)
        header = ""
        data_start = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('Sheet:') and len(line) > 10:
                header = line
                data_start = i + 1
                break
        
        if not header:
            return self._chunk_normal(text, document_id, 500)
        
        chunks = []
        chunk_num = 0
        
        for line in lines[data_start:]:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            if line.startswith('Sheet:'):
                continue
            
            chunk_num += 1
            # Extract date/equipment for section name
            parts = line.split('\t') if '\t' in line else line.split(',')
            section = parts[0] if parts else f"Row {chunk_num}"
            
            chunks.append({
                'id': f'chunk_{document_id}_{chunk_num}',
                'text': f"{header}\n{line}",
                'page': chunk_num,
                'section': f"Data: {section}",
                'word_count': len(line.split())
            })
        
        self.logger.info(f"Created {len(chunks)} row chunks")
        return chunks
    
    def _chunk_normal(self, text: str, document_id: int, chunk_size: int) -> List[Dict]:
        words = text.split()
        chunks = []
        current = []
        count = 0
        num = 0
        
        for word in words:
            current.append(word)
            count += 1
            if count >= chunk_size:
                num += 1
                chunks.append({
                    'id': f'chunk_{document_id}_{num}',
                    'text': ' '.join(current),
                    'page': num,
                    'section': f'Section {num}',
                    'word_count': count
                })
                current = []
                count = 0
        
        if current:
            num += 1
            chunks.append({
                'id': f'chunk_{document_id}_{num}',
                'text': ' '.join(current),
                'page': num,
                'section': f'Section {num}',
                'word_count': count
            })
        
        self.logger.info(f"Created {len(chunks)} normal chunks")
        return chunks