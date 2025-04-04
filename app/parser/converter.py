"""
Converter module - Functions for converting resumes to text
"""
import os
from app.config import SUPPORTED_EXTENSIONS

def convert_resume_to_text(file_path):
    """
    Convert resume files to plain text
    
    Args:
        file_path: Path to the resume file
        
    Returns:
        str: Plain text content of the resume
        
    Raises:
        ValueError: If the file format is not supported
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    if file_extension == '.pdf':
        return _convert_pdf_to_text(file_path)
    
    elif file_extension in ['.docx', '.doc']:
        return _convert_doc_to_text(file_path)
    
    elif file_extension == '.txt':
        return _read_text_file(file_path)

def _convert_pdf_to_text(file_path):
    """Convert PDF file to text"""
    try:
        from pdfminer.high_level import extract_text
        return extract_text(file_path)
    except ImportError:
        raise ImportError("pdfminer.six is required for PDF conversion. Install with: pip install pdfminer.six")

def _convert_doc_to_text(file_path):
    """Convert DOCX/DOC file to text"""
    try:
        import docx2txt
        return docx2txt.process(file_path)
    except ImportError:
        raise ImportError("docx2txt is required for DOCX conversion. Install with: pip install docx2txt")

def _read_text_file(file_path):
    """Read text file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()