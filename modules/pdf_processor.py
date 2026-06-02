import io
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file.
    
    Tries to extract standard embedded text first. If the page is empty 
    (e.g., scanned image), it falls back to OCR using pytesseract.
    
    Args:
        file_bytes: The raw bytes of the PDF file.
        
    Returns:
        Extracted text as a single string.
    """
    text_content = []
    
    try:
        # First attempt: Try extracting text directly using pdfplumber (faster, works for standard PDFs)
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                
                if page_text and page_text.strip():
                    text_content.append(page_text)
                else:
                    # Fallback to OCR for this specific page if no text was found
                    logger.info(f"Page {page_num + 1} appears to be an image. Attempting OCR...")
                    ocr_text = extract_text_via_ocr(file_bytes, page_num)
                    if ocr_text:
                        text_content.append(ocr_text)
                        
    except Exception as e:
        logger.error(f"Error during standard PDF extraction: {e}")
        # If pdfplumber fails entirely, fallback to full OCR
        logger.info("Attempting full document OCR fallback...")
        ocr_text = extract_text_via_ocr(file_bytes)
        if ocr_text:
            text_content.append(ocr_text)

    return "\n".join(text_content)


def extract_text_via_ocr(file_bytes: bytes, specific_page_num: int = None) -> str:
    """Extract text from PDF using OCR (pdf2image + pytesseract).
    
    Args:
        file_bytes: The raw bytes of the PDF file.
        specific_page_num: If provided (0-indexed), only OCR this specific page.
        
    Returns:
        Extracted text via OCR.
    """
    text_content = []
    try:
        # Convert PDF bytes to a list of PIL Images
        if specific_page_num is not None:
            # pdf2image first_page and last_page are 1-indexed
            images = convert_from_bytes(
                file_bytes, 
                first_page=specific_page_num + 1, 
                last_page=specific_page_num + 1
            )
        else:
            images = convert_from_bytes(file_bytes)
            
        for img in images:
            # Perform OCR on the image
            text = pytesseract.image_to_string(img)
            text_content.append(text)
            
    except Exception as e:
        logger.error(f"OCR Extraction failed: {e}")
        logger.warning(
            "Note: OCR requires 'tesseract' and 'poppler' to be installed on your system. "
            "Please ensure they are installed and in your system PATH."
        )
        
    return "\n".join(text_content)
