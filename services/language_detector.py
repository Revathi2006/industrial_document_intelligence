from typing import Dict
from loguru import logger
from langdetect import detect

class LanguageDetector:
    def __init__(self):
        self.logger = logger
    
    async def detect(self, text: str) -> str:
        '''Detect language of text'''
        try:
            if len(text.strip()) < 10:
                return "unknown"
            
            language = detect(text)
            self.logger.info(f"Detected language: {language}")
            return language
        except Exception as e:
            self.logger.error(f"Language detection failed: {e}")
            return "unknown"
