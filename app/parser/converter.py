"""
Converter module - Functions for converting resumes to text
"""

import os
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document
from pdfminer.high_level import extract_text

# Supported extensions
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']

def convert_resume_to_text(file_input):
    """
    Convert resume files to plain text
    
    Args:
        file_input: Path to the resume file or BytesIO object
        
    Returns:
        str: Plain text content of the resume
        
    Raises:
        ValueError: If the file format is not supported
    """
    # Determine whether file_input is a file path or in-memory file-like object
    if isinstance(file_input, str):  # File path
        file_extension = os.path.splitext(file_input)[1].lower()
    elif isinstance(file_input, BytesIO):  # Stream object (e.g., from Streamlit)
        file_extension = _detect_stream_extension(file_input)
    else:
        raise ValueError("Unsupported input type. Expected file path or BytesIO object.")

    if file_extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    if file_extension == '.pdf':
        return _convert_pdf_to_text(file_input)
    
    elif file_extension in ['.docx', '.doc']:
        return _convert_doc_to_text(file_input)
    
    elif file_extension == '.txt':
        return _read_text_file(file_input)

def _convert_pdf_to_text(file_input):
    """Convert PDF file to text"""
    if isinstance(file_input, str):  # File path
        return extract_text(file_input)
    elif isinstance(file_input, BytesIO):  # Stream object
        pdf_reader = PdfReader(file_input)
        text = ''.join([page.extract_text() for page in pdf_reader.pages])
        return text
    else:
        raise ValueError("Invalid input type for PDF conversion.")

def _convert_doc_to_text(file_input):
    """Convert DOCX/DOC file to text"""
    try:
        if isinstance(file_input, str):  # File path
            import docx2txt
            return docx2txt.process(file_input)
        elif isinstance(file_input, BytesIO):  # Stream object
            document = Document(file_input)
            return '\n'.join(paragraph.text for paragraph in document.paragraphs)
        else:
            raise ValueError("Invalid input type for DOCX/DOC conversion.")
    except ImportError:
        raise ImportError("docx2txt is required for DOCX conversion. Install with: pip install docx2txt")

def _read_text_file(file_input):
    """Read plain text files"""
    if isinstance(file_input, str):  # File path
        with open(file_input, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    elif isinstance(file_input, BytesIO):  # Stream object
        file_input.seek(0)  # Ensure we're reading from the beginning
        return file_input.read().decode('utf-8', errors='ignore')
    else:
        raise ValueError("Invalid input type for text file reading.")

def _detect_stream_extension(file_stream):
    """
    Detect file extension for BytesIO object
    
    Args:
        file_stream: BytesIO object
    
    Returns:
        str: File extension (e.g., '.pdf', '.docx')
    """
    # Use filename attribute if available (e.g., from Streamlit's UploadedFile)
    if hasattr(file_stream, 'name'):
        return os.path.splitext(file_stream.name)[1].lower()
    else:
        raise ValueError("Cannot detect file extension for in-memory stream.")