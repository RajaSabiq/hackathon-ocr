import cv2
import numpy as np
from PIL import Image, ImageEnhance
import logging
import config

logger = logging.getLogger(__name__)

class ImagePreprocessor:
    """Advanced image preprocessing for OCR optimization"""
    
    def __init__(self):
        self.max_dimension = config.MAX_IMAGE_DIMENSION
        self.min_dimension = config.MIN_IMAGE_DIMENSION
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Apply comprehensive preprocessing pipeline to optimize image for OCR
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            logger.info(f"Original image shape: {image.shape}")
            
            # Step 1: Resize if needed
            image = self._resize_image(image)
            
            # Step 2: Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Step 3: Noise reduction
            denoised = self._denoise_image(gray)
            
            # Step 4: Deskew/rotation correction
            deskewed = self._deskew_image(denoised)
            
            # Step 5: Enhance contrast
            enhanced = self._enhance_contrast(deskewed)
            
            # Step 6: Binarization (adaptive thresholding)
            binary = self._binarize_image(enhanced)
            
            logger.info(f"Preprocessed image shape: {binary.shape}")
            return binary
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {str(e)}")
            raise
    
    def _resize_image(self, image: np.ndarray) -> np.ndarray:
        """Resize image to optimal dimensions for OCR"""
        height, width = image.shape[:2]
        
        # Calculate scaling factor
        max_dim = max(height, width)
        min_dim = min(height, width)
        
        if max_dim > self.max_dimension:
            scale = self.max_dimension / max_dim
        elif min_dim < self.min_dimension:
            scale = self.min_dimension / min_dim
        else:
            return image  # No resizing needed
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        logger.info(f"Resized from {width}x{height} to {new_width}x{new_height}")
        
        return resized
    
    def _denoise_image(self, image: np.ndarray) -> np.ndarray:
        """Remove noise from the image"""
        # Apply Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
        return denoised
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """Correct skew/rotation in the image"""
        try:
            # Find edges
            edges = cv2.Canny(image, 50, 150, apertureSize=3)
            
            # Find lines using Hough transform
            lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
            
            if lines is not None and len(lines) > 0:
                # Calculate average angle
                angles = []
                for rho, theta in lines[:20]:  # Use first 20 lines
                    angle = theta * 180 / np.pi
                    if angle < 45:
                        angles.append(angle)
                    elif angle > 135:
                        angles.append(angle - 180)
                
                if angles:
                    median_angle = np.median(angles)
                    
                    # Only rotate if angle is significant
                    if abs(median_angle) > 0.5:
                        logger.info(f"Deskewing by {median_angle:.2f} degrees")
                        
                        # Rotate image
                        height, width = image.shape
                        center = (width // 2, height // 2)
                        rotation_matrix = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                        
                        # Calculate new dimensions
                        cos_angle = abs(rotation_matrix[0, 0])
                        sin_angle = abs(rotation_matrix[0, 1])
                        new_width = int((height * sin_angle) + (width * cos_angle))
                        new_height = int((height * cos_angle) + (width * sin_angle))
                        
                        # Adjust rotation matrix for new dimensions
                        rotation_matrix[0, 2] += (new_width / 2) - center[0]
                        rotation_matrix[1, 2] += (new_height / 2) - center[1]
                        
                        rotated = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), 
                                               flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                        return rotated
            
            return image
            
        except Exception as e:
            logger.warning(f"Deskewing failed: {str(e)}, using original image")
            return image
    
    def _enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Enhance image contrast using CLAHE"""
        # Create CLAHE object
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        return enhanced
    
    def _binarize_image(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding for binarization"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Apply adaptive threshold
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def preprocess_pil_image(self, pil_image: Image.Image) -> np.ndarray:
        """Preprocess PIL Image object"""
        # Convert PIL to OpenCV format
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Apply preprocessing pipeline
        return self.preprocess_image_array(opencv_image)
    
    def preprocess_image_array(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image array directly"""
        try:
            # Step 1: Resize if needed
            image = self._resize_image(image)
            
            # Step 2: Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Step 3: Noise reduction
            denoised = self._denoise_image(gray)
            
            # Step 4: Deskew/rotation correction
            deskewed = self._deskew_image(denoised)
            
            # Step 5: Enhance contrast
            enhanced = self._enhance_contrast(deskewed)
            
            # Step 6: Binarization
            binary = self._binarize_image(enhanced)
            
            return binary
            
        except Exception as e:
            logger.error(f"Error preprocessing image array: {str(e)}")
            raise