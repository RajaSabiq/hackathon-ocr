import pytesseract
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import tempfile
import os
import logging
from typing import List, Tuple, Dict, Any
import json

from image_preprocessor import ImagePreprocessor
from models import OCRResult, BoundingBox
import config

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Advanced OCR processing with Tesseract"""
    
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        self.supported_languages = self._get_supported_languages()
        
        # Tesseract configuration for better accuracy
        self.tesseract_config = config.TESSERACT_CONFIG
        
    def _get_supported_languages(self) -> List[str]:
        """Get list of supported languages from Tesseract"""
        try:
            langs = pytesseract.get_languages(config='')
            logger.info(f"Tesseract supports {len(langs)} languages")
            return langs
        except Exception as e:
            logger.warning(f"Could not get supported languages: {str(e)}")
            return ['eng']  # Default to English
    
    def detect_language(self, image: np.ndarray) -> str:
        """Detect the primary language in the image"""
        try:
            # Use Tesseract's built-in language detection
            osd = pytesseract.image_to_osd(image, output_type=pytesseract.Output.DICT)
            
            # Try to extract language info from OSD
            # This is a simplified approach - in production, you might want more sophisticated detection
            detected_lang = 'eng'  # Default
            
            # For now, we'll use English as default but this can be enhanced
            # with proper language detection libraries like langdetect
            
            logger.info(f"Detected language: {detected_lang}")
            return detected_lang
            
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}, using English")
            return 'eng'
    
    def process_image(self, image_path: str, filename: str, page_number: int = None) -> OCRResult:
        """
        Process a single image file and extract text with confidence scores
        
        Args:
            image_path: Path to the image file
            filename: Original filename
            page_number: Page number for PDF files
            
        Returns:
            OCRResult with extracted text and metadata
        """
        try:
            logger.info(f"Processing image: {filename}")
            
            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Preprocess image
            logger.info(f"Preprocessing image: {filename}")
            processed_image = self.preprocessor.preprocess_image(image_path)
            
            # Detect language
            logger.info(f"Detecting language for: {filename}")
            language = self.detect_language(processed_image)
            
            # Extract text with confidence scores
            logger.info(f"Extracting text data for: {filename}")
            text_data = pytesseract.image_to_data(
                processed_image, 
                lang=language,
                config=self.tesseract_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract full text
            logger.info(f"Extracting full text for: {filename}")
            full_text = pytesseract.image_to_string(
                processed_image,
                lang=language,
                config=self.tesseract_config
            ).strip()
            
            # Process bounding box data
            bbox_data = self._extract_bbox_data(text_data)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(text_data)
            
            result = OCRResult(
                filename=filename,
                text=full_text,
                confidence=overall_confidence,
                language=language,
                bbox_data=bbox_data,
                page_number=page_number
            )
            
            logger.info(f"OCR completed for {filename}: {len(full_text)} characters, confidence: {overall_confidence:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {str(e)}", exc_info=True)
            raise Exception(f"OCR processing failed for {filename}: {str(e)}")
    
    def process_pdf(self, pdf_path: str, filename: str) -> List[OCRResult]:
        """
        Process a PDF file and extract text from all pages
        
        Args:
            pdf_path: Path to the PDF file
            filename: Original filename
            
        Returns:
            List of OCRResult objects, one per page
        """
        try:
            logger.info(f"Processing PDF: {filename}")
            
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=config.PDF_DPI)
            results = []
            
            for page_num, image in enumerate(images, 1):
                logger.info(f"Processing page {page_num} of {filename}")
                
                # Convert PIL image to numpy array
                image_array = np.array(image)
                
                # Preprocess image
                processed_image = self.preprocessor.preprocess_image_array(image_array)
                
                # Detect language
                language = self.detect_language(processed_image)
                
                # Extract text with confidence scores
                text_data = pytesseract.image_to_data(
                    processed_image,
                    lang=language,
                    config=self.tesseract_config,
                    output_type=pytesseract.Output.DICT
                )
                
                # Extract full text
                full_text = pytesseract.image_to_string(
                    processed_image,
                    lang=language,
                    config=self.tesseract_config
                ).strip()
                
                # Process bounding box data
                bbox_data = self._extract_bbox_data(text_data)
                
                # Calculate overall confidence
                overall_confidence = self._calculate_overall_confidence(text_data)
                
                result = OCRResult(
                    filename=f"{filename} (Page {page_num})",
                    text=full_text,
                    confidence=overall_confidence,
                    language=language,
                    bbox_data=bbox_data,
                    page_number=page_num
                )
                
                results.append(result)
                logger.info(f"Page {page_num} completed: {len(full_text)} characters, confidence: {overall_confidence:.2f}")
            
            logger.info(f"PDF processing completed: {len(results)} pages")
            return results
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            raise
    
    def _extract_bbox_data(self, text_data: Dict[str, List]) -> List[BoundingBox]:
        """Extract bounding box data from Tesseract output"""
        bbox_data = []
        
        n_boxes = len(text_data['text'])
        for i in range(n_boxes):
            text = text_data['text'][i].strip()
            confidence = float(text_data['conf'][i])
            
            # Only include text with reasonable confidence and non-empty text
            if confidence > 0 and text:
                bbox = BoundingBox(
                    text=text,
                    confidence=confidence / 100.0,  # Convert to 0-1 scale
                    bbox=[
                        int(text_data['left'][i]),
                        int(text_data['top'][i]),
                        int(text_data['width'][i]),
                        int(text_data['height'][i])
                    ]
                )
                bbox_data.append(bbox)
        
        return bbox_data
    
    def _calculate_overall_confidence(self, text_data: Dict[str, List]) -> float:
        """Calculate overall confidence score for the OCR result"""
        confidences = []
        
        for i, conf in enumerate(text_data['conf']):
            text = text_data['text'][i].strip()
            if conf > 0 and text:  # Only consider valid detections
                confidences.append(float(conf))
        
        if not confidences:
            return 0.0
        
        # Use weighted average based on text length
        total_weight = 0
        weighted_sum = 0
        
        for i, conf in enumerate(confidences):
            text_length = len(text_data['text'][i].strip())
            weight = max(1, text_length)  # Minimum weight of 1
            weighted_sum += conf * weight
            total_weight += weight
        
        overall_confidence = weighted_sum / total_weight if total_weight > 0 else 0.0
        return min(1.0, overall_confidence / 100.0)  # Convert to 0-1 scale
    
    def process_file(self, file_path: str, filename: str) -> List[OCRResult]:
        """
        Process any supported file type
        
        Args:
            file_path: Path to the file
            filename: Original filename
            
        Returns:
            List of OCRResult objects
        """
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == '.pdf':
            return self.process_pdf(file_path, filename)
        else:
            # Process as image
            result = self.process_image(file_path, filename)
            return [result]
    
    def get_tesseract_version(self) -> str:
        """Get Tesseract version for health check"""
        try:
            return pytesseract.get_tesseract_version().public
        except Exception:
            return "Unknown"