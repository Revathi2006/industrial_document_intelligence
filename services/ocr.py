import pytesseract
from PIL import Image
import fitz
from pathlib import Path
from typing import Dict, List, Tuple
from loguru import logger
import cv2
import numpy as np

class OCRProcessor:
    def __init__(self):
        self.confidence_threshold = 0.6
        
    async def process_document(self, file_path: Path, page_images: List = None) -> Dict:
        """
        Process document with OCR if needed
        
        Args:
            file_path: Path to the document
            page_images: Optional list of pre-extracted page images
        
        Returns:
            Dictionary with OCR results
        """
        try:
            if file_path.suffix.lower() == '.pdf':
                return await self._process_pdf(file_path)
            else:
                return await self._process_image(file_path)
        
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            raise
    
    async def _process_pdf(self, pdf_path: Path) -> Dict:
        """Process PDF pages with OCR"""
        doc = fitz.open(str(pdf_path))
        ocr_results = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert page to image
            pix = page.get_pixmap(dpi=300)
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], img_data)
            
            # Preprocess image
            img_processed = self._preprocess_image(img)
            
            # Perform OCR
            ocr_result = await self._perform_ocr(img_processed)
            ocr_result['page'] = page_num + 1
            ocr_results.append(ocr_result)
        
        doc.close()
        
        return {
            'pages': ocr_results,
            'full_text': '\n'.join([r['text'] for r in ocr_results]),
            'average_confidence': sum(r['confidence'] for r in ocr_results) / len(ocr_results) if ocr_results else 0
        }
    
    async def _process_image(self, image_path: Path) -> Dict:
        """Process single image with OCR"""
        img = Image.open(str(image_path))
        img_processed = self._preprocess_image(img)
        
        ocr_result = await self._perform_ocr(img_processed)
        
        return {
            'pages': [ocr_result],
            'full_text': ocr_result['text'],
            'average_confidence': ocr_result['confidence']
        }
    
    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """Preprocess image for better OCR"""
        # Convert to numpy array
        img_array = np.array(img)
        
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        # Convert back to PIL Image
        return Image.fromarray(denoised)
    
    async def _perform_ocr(self, img: Image.Image) -> Dict:
        """Perform OCR on image"""
        try:
            # Get OCR data with confidence scores
            ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            
            # Extract text
            text = ' '.join([word for word in ocr_data['text'] if word.strip()])
            
            # Calculate confidence
            confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) / 100 if confidences else 0
            
            # Extract word-level information
            words = []
            for i in range(len(ocr_data['text'])):
                if ocr_data['text'][i].strip():
                    words.append({
                        'text': ocr_data['text'][i],
                        'confidence': int(ocr_data['conf'][i]) / 100,
                        'bbox': {
                            'x': ocr_data['left'][i],
                            'y': ocr_data['top'][i],
                            'w': ocr_data['width'][i],
                            'h': ocr_data['height'][i]
                        }
                    })
            
            return {
                'text': text,
                'confidence': avg_confidence,
                'words': words,
                'word_count': len(words)
            }
        
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            raise
    
    async def detect_text_type(self, pdf_path: Path) -> str:
        """Detect if PDF is text-based or scanned"""
        doc = fitz.open(str(pdf_path))
        
        # Check first few pages
        total_text = ""
        pages_to_check = min(5, len(doc))
        
        for i in range(pages_to_check):
            page = doc[i]
            total_text += page.get_text()
        
        doc.close()
        
        # If very little text is extractable, it's likely scanned
        if len(total_text.strip()) < 100:
            return "scanned"
        
        return "text"