"""
Preprocessor module - Functions for cleaning and normalizing text
"""
import re

def preprocess_text(text):
    """
    Clean and normalize text
    
    Args:
        text: Raw text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
        
    # Convert to lowercase
    # text = text.lower()  # Optional - may lose information about proper nouns
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)
    
    # Remove special characters (optional, be careful with this)
    # text = re.sub(r'[^\w\s.,;:()-]', '', text)
    
    # Handle bullet points and dashes
    text = text.replace('•', '\n• ')
    text = text.replace('◦', '\n◦ ')
    text = text.replace('○', '\n○ ')
    text = text.replace('■', '\n■ ')
    text = text.replace('●', '\n● ')
    
    # Handle common section header variations
    text = re.sub(r'WORK\s+EXPERIENCE', 'EXPERIENCE', text, flags=re.IGNORECASE)
    text = re.sub(r'PROFESSIONAL\s+EXPERIENCE', 'EXPERIENCE', text, flags=re.IGNORECASE)
    text = re.sub(r'ACADEMIC\s+BACKGROUND', 'EDUCATION', text, flags=re.IGNORECASE)
    text = re.sub(r'EDUCATIONAL\s+QUALIFICATIONS', 'EDUCATION', text, flags=re.IGNORECASE)
    text = re.sub(r'TECHNICAL\s+SKILLS', 'SKILLS', text, flags=re.IGNORECASE)
    text = re.sub(r'CORE\s+COMPETENCIES', 'SKILLS', text, flags=re.IGNORECASE)
    text = re.sub(r'PROFESSIONAL\s+CERTIFICATIONS', 'CERTIFICATIONS', text, flags=re.IGNORECASE)
    text = re.sub(r'PERSONAL\s+PROJECTS', 'PROJECTS', text, flags=re.IGNORECASE)
    
    return text.strip()