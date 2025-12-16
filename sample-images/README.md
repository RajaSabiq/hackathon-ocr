# Sample Test Images

This directory contains sample images for testing the OCR application. You can use these files to test different scenarios:

## Test Scenarios

### 1. Clean Printed Text
- **receipt.jpg**: Clean receipt with printed text
- **business-card.png**: Business card with contact information
- **invoice.pdf**: Multi-page invoice document

### 2. Challenging Cases
- **handwritten.jpg**: Handwritten note (lower accuracy expected)
- **skewed-document.jpg**: Rotated/skewed document
- **low-quality.jpg**: Blurry or low-resolution image
- **multi-language.png**: Document with multiple languages

### 3. Different Formats
- **document.pdf**: Multi-page PDF document
- **screenshot.png**: Screenshot of text
- **photo-text.jpg**: Photo containing text

## Usage

1. Start the OCR application
2. Drag and drop any of these sample files
3. Compare results with expected text content
4. Test batch upload by selecting multiple files

## Expected Results

The OCR system should handle:
- ✅ High accuracy on clean printed text (>90% confidence)
- ✅ Reasonable accuracy on business cards and receipts
- ✅ Multi-page PDF processing
- ✅ Automatic language detection
- ⚠️ Lower accuracy on handwritten text (expected)
- ⚠️ Preprocessing should improve skewed images

## Adding Your Own Test Images

You can add your own test images to this directory. Supported formats:
- PNG, JPG, JPEG, WEBP (up to 10MB)
- PDF (single or multi-page, up to 10MB)

For best results:
- Use high-resolution images (300+ DPI)
- Ensure good contrast between text and background
- Avoid excessive skew or rotation
- Use well-lit photos without shadows