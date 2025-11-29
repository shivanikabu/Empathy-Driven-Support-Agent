import io
import PyPDF2
from typing import List, Tuple

class DocumentProcessor:
    """Service for processing PDF documents"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Tuple[bool, str, List[str]]:
        """
        Extract text from PDF and split into paragraphs
        Returns: (success, message, paragraphs)
        """
        try:
            pdf_bytes = pdf_file.read()
            pdf_file_obj = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
            
            num_pages = len(pdf_reader.pages)
            content = ""
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n\n"
            
            if not content or len(content) < 50:
                return False, "No readable text found in PDF", []
            
            # Split into paragraphs
            content = '\n\n'.join([line.strip() for line in content.split('\n') if line.strip()])
            paragraphs = content.split('\n\n')
            
            # Clean and filter paragraphs
            valid_paragraphs = []
            for para in paragraphs:
                para = para.strip()
                if len(para) >= 50:  # Minimum paragraph length
                    para = ' '.join(para.split())  # Clean whitespace
                    valid_paragraphs.append(para)
            
            return True, f"Extracted {len(valid_paragraphs)} paragraphs", valid_paragraphs
            
        except Exception as e:
            return False, f"PDF processing error: {str(e)}", []
