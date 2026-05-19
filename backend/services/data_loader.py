import os
import io
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes, filename: str) -> str:
    if not filename.endswith('pdf'):
        raise ValueError("Only PDFs accepted!")
    
    reader = PdfReader(io.BytesIO(file_bytes))

    return "\n".join(page.extract_text() or "" for page in reader)