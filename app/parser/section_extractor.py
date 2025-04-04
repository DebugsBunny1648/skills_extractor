"""
Section Extractor module - Functions for identifying sections in resumes
"""
import re
from app.config import SECTION_HEADERS

def identify_sections(text):
    """
    Identify different sections in a resume
    
    Args:
        text: Preprocessed resume text
        
    Returns:
        dict: Dictionary with section names as keys and section content as values
    """
    sections = {}
    current_section = None
    current_content = []
    
    # Split text into lines
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if the line is a section header
        found_section = False
        for section, headers in SECTION_HEADERS.items():
            # Case-insensitive matching for section headers
            if _is_section_header(line, headers):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = section
                current_content = []
                found_section = True
                break
                
        if not found_section and current_section:
            current_content.append(line)
    
    # Add the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
        
    # If no sections were found, try a different approach
    if not sections:
        sections = _fallback_section_identification(text)
    
    return sections

def _is_section_header(line, headers):
    """Check if a line is a section header"""
    line_lower = line.lower()
    
    # Direct match
    if any(header == line_lower for header in headers):
        return True
    
    # Header with colon
    if any(header + ':' == line_lower for header in headers):
        return True
    
    # Header is a substring but prominent (all caps or at start of line)
    if line.isupper() and any(header in line_lower for header in headers):
        return True
        
    # More sophisticated check for headers
    for header in headers:
        pattern = r'\b' + re.escape(header) + r'\b'
        if re.search(pattern, line_lower, re.IGNORECASE):
            # Check if this is likely a header (based on formatting)
            if (line.isupper() or 
                line.istitle() or 
                line.endswith(':') or 
                len(line) < 30):  # Shorter lines are more likely to be headers
                return True
    
    return False

def _fallback_section_identification(text):
    """Fallback method if section headers aren't clearly identified"""
    sections = {}
    
    # Look for common skills
    skills_pattern = r'(?:technical skills|skills|proficiencies)[\s\S]*?(?=\n\n|\Z)'
    skills_match = re.search(skills_pattern, text, re.IGNORECASE)
    if skills_match:
        sections['skills'] = skills_match.group(0)
    
    # Look for work experience
    experience_pattern = r'(?:work experience|experience|employment)[\s\S]*?(?=\n\n|\Z)'
    experience_match = re.search(experience_pattern, text, re.IGNORECASE)
    if experience_match:
        sections['experience'] = experience_match.group(0)
    
    # Look for education
    education_pattern = r'(?:education|academic)[\s\S]*?(?=\n\n|\Z)'
    education_match = re.search(education_pattern, text, re.IGNORECASE)
    if education_match:
        sections['education'] = education_match.group(0)
    
    return sections