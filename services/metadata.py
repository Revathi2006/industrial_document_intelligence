import re
from typing import Dict
from loguru import logger
from datetime import datetime

class MetadataExtractor:
    def __init__(self):
        self.logger = logger
    
    async def extract(self, text: str, filename: str) -> Dict:
        '''Extract metadata from document content'''
        try:
            self.logger.info("Extracting metadata")
            
            metadata = {
                'filename': filename,
                'extraction_date': datetime.now().isoformat(),
                'word_count': len(text.split()),
                'char_count': len(text),
                'has_tables': 'table' in text.lower(),
                'has_images': 'figure' in text.lower() or 'image' in text.lower(),
            }
            
            # Try to extract common patterns
            patterns = self._extract_patterns(text)
            metadata.update(patterns)
            
            self.logger.info("Metadata extraction completed")
            return metadata
            
        except Exception as e:
            self.logger.error(f"Metadata extraction failed: {e}")
            return {
                'filename': filename,
                'error': str(e)
            }
    
    def _extract_patterns(self, text: str) -> Dict:
        '''Extract specific patterns from text'''
        patterns = {}
        
        # Extract dates
        date_patterns = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
        if date_patterns:
            patterns['dates_found'] = date_patterns[:5]
        
        # Extract version numbers
        version_patterns = re.findall(r'(?:version|v)\s*(\d+\.?\d*)', text, re.IGNORECASE)
        if version_patterns:
            patterns['version'] = version_patterns[0]
        
        # Extract email addresses
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if emails:
            patterns['emails'] = emails[:3]
        
        # Extract equipment names (common in industrial docs)
        equipment_patterns = re.findall(
            r'(?:pump|motor|valve|compressor|turbine|generator|boiler|conveyor)',
            text, re.IGNORECASE
        )
        if equipment_patterns:
            patterns['equipment_mentioned'] = list(set(equipment_patterns))[:10]
        
        # Extract departments
        dept_patterns = re.findall(
            r'(?:mechanical|electrical|maintenance|production|safety|quality)\s+(?:department|dept|division)',
            text, re.IGNORECASE
        )
        if dept_patterns:
            patterns['departments'] = dept_patterns[:5]
        
        return patterns
