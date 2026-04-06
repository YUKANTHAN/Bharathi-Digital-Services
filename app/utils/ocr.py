import pytesseract
from PIL import Image
import os

# If Tesseract is not in your PATH, uncomment and set the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(file_path):
    """
    Extracts text from an image using Tesseract OCR.
    """
    try:
        if not os.path.exists(file_path):
            return "File not found"

        # Open image
        img = Image.open(file_path)
        
        # Simple OCR
        text = pytesseract.image_to_string(img)
        
        # Basic cleaning
        clean_text = " ".join(text.split())
        return clean_text if clean_text else "No textual data detected"
        
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        print(f"OCR Error: {e}")
        return f"OCR processing failed: {str(e)}"
