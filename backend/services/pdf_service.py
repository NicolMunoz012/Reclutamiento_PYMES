"""
PDF Service - Extract text from PDF files
"""
from PyPDF2 import PdfReader
from io import BytesIO
from typing import Optional


class PDFService:
    """Service for PDF text extraction"""
    
    @staticmethod
    async def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            Extracted text from PDF
        """
        try:
            pdf_file = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_file)
            
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # Clean up text
            text = text.strip()
            
            if not text:
                return "No se pudo extraer texto del PDF"
            
            return text
            
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return f"Error al procesar PDF: {str(e)}"


# Singleton instance
pdf_service = PDFService()
