from typing import List, Dict
from loguru import logger

class TableExtractor:
    def __init__(self):
        self.logger = logger
    
    async def extract(self, text: str) -> List[Dict]:
        '''Extract tables from text'''
        self.logger.info("Extracting tables")
        # Simple table detection - look for structured data
        tables = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if '|' in line or '\t' in line:
                tables.append({
                    'page': i + 1,
                    'data': line,
                    'type': 'text_table'
                })
        
        return tables
