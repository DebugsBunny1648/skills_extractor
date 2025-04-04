"""
Utils module - Helper functions for resume parsing
"""
import os
import re

def is_valid_file_extension(file_path, supported_extensions):
    """
    Check if the file has a supported extension
    
    Args:
        file_path: Path to the file
        supported_extensions: List of supported extensions
        
    Returns:
        bool: True if the file has a supported extension, False otherwise
    """
    _, ext = os.path.splitext(file_path)
    return ext.lower() in supported_extensions

def clean_text(text):
    """
    Remove unwanted characters and normalize whitespace
    
    Args:
        text: Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
        
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere with parsing
    text = re.sub(r'[^\w\s.,;:()-]', '', text)
    
    return text.strip()

def extract_contact_info(text):
    """
    Extract contact information from resume text
    
    Args:
        text: Resume text
        
    Returns:
        dict: Dictionary containing contact information
    """
    contact_info = {
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info['email'] = email_match.group(0)
    
    # Phone number patterns
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US/Canada: 123-456-7890
        r'\b\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'  # International: +1-123-456-7890
    ]
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group(0)
            break
    
    # LinkedIn profile
    linkedin_patterns = [
        r'linkedin\.com/in/[\w-]+',
        r'linkedin:\s*([\w-]+)'
    ]
    for pattern in linkedin_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contact_info['linkedin'] = match.group(0)
            break
    
    # GitHub profile
    github_patterns = [
        r'github\.com/[\w-]+',
        r'github:\s*([\w-]+)'
    ]
    for pattern in github_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            contact_info['github'] = match.group(0)
            break
    
    return contact_info