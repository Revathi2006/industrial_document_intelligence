from pathlib import Path
from typing import List, Dict
from loguru import logger
import fitz

class ImageExtractor:
    def __init__(self):
        self.logger = logger
    
    async def extract(self, file_path: Path) -> List[Dict]:
        '''Extract images from document'''
        self.logger.info(f"Extracting images from: {file_path}")
        images = []
        
        try:
            if file_path.suffix.lower() == '.pdf':
                doc = fitz.open(str(file_path))
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images()
                    
                    for img_index, img in enumerate(image_list):
                        images.append({
                            'page': page_num + 1,
                            'index': img_index,
                            'format': 'png'
                        })
                doc.close()
        except Exception as e:
            self.logger.error(f"Image extraction failed: {e}")
        
        return images
