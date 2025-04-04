"""
Experience Extractor - Functions for extracting work experience from resumes
"""
import re
import json
import os
from app.config import JOB_TITLES_FILE

def extract_experience(experience_text):
    """
    Extract work experience information
    
    Args:
        experience_text: Text from the experience section
        
    Returns:
        list: List of dictionaries containing experience information
    """
    if not experience_text:
        return []
        
    experiences = []
    
    # Load job titles list for better matching
    job_titles = _load_job_titles()
    
    # Split text into different job entries (assuming blank lines separate jobs)
    job_entries = re.split(r'\n\n+', experience_text)
    
    for entry in job_entries:
        if not entry.strip():
            continue
            
        # Extract job title
        job_title = _extract_job_title(entry, job_titles)
        
        # Extract company
        company = _extract_company(entry)
        
        # Extract dates
        dates = _extract_dates(entry)
        
        # Extract responsibilities/achievements
        responsibilities = _extract_responsibilities(entry)
        
        # Only add if we have at least job title or company
        if job_title or company:
            experiences.append({
                'job_title': job_title,
                'company': company,
                'dates': dates,
                'responsibilities': responsibilities
            })
    
    return experiences

def _extract_job_title(text, job_titles):
    """Extract job title from text"""
    # Try specific job title patterns first
    specific_pattern = '|'.join(job_titles)
    job_title_match = re.search(rf"({specific_pattern})", text, re.IGNORECASE)
    
    # If specific match found, return it
    if job_title_match:
        return job_title_match.group(1).strip()
    
    # Try general patterns
    general_patterns = [
        r"(.*?Engineer|.*?Developer|.*?Manager|.*?Director|.*?Analyst|.*?Designer|.*?Specialist|.*?Coordinator|.*?Assistant|.*?Intern)",
        r"^([A-Z][a-z]+(?: [A-Z][a-z]+)*)"  # Capitalized words at start of text
    ]
    
    for pattern in general_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    
    return None

def _extract_company(text):
    """Extract company name from text"""
    # Common patterns for company references
    company_patterns = [
        r"at\s+([\w\s,\.]+?)(?=\s+from|\s+in|\s+\(|\s*\n|\s*$)",
        r"for\s+([\w\s,\.]+?)(?=\s+from|\s+in|\s+\(|\s*\n|\s*$)",
        r"with\s+([\w\s,\.]+?)(?=\s+from|\s+in|\s+\(|\s*\n|\s*$)",
        r"@\s*([\w\s,\.]+?)(?=\s+from|\s+in|\s+\(|\s*\n|\s*$)"
    ]
    
    for pattern in company_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # Try to find company names with common suffixes
    company_suffixes = r"Inc\.|LLC|Ltd\.?|Corp\.?|Corporation|Company|GmbH"
    suffix_match = re.search(rf"([\w\s,\.]+?)\s+(?:{company_suffixes})", text)
    if suffix_match:
        return suffix_match.group(0).strip()
            
    return None

def _extract_dates(text):
    """Extract date ranges from text"""
    # Various date formats
    date_patterns = [
        # Month Year - Month Year (Jan 2020 - Dec 2021)
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4}\s*(-|–|to)\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4}",
        # Year - Year (2020 - 2021)
        r"(\d{4})\s*(-|–|to)\s*(\d{4}|Present|Current)",
        # Month Year - Present
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4}\s*(-|–|to)\s*(Present|Current)",
        # Just years in parentheses (2020-2021)
        r"\((\d{4})\s*(-|–|to)\s*(\d{4}|Present|Current)\)"
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
            
    return None

def _extract_responsibilities(text):
    """Extract job responsibilities from text"""
    responsibilities = []
    
    # Split text into lines
    lines = text.split('\n')
    
    in_bullet_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for bullet points and other list markers
        if line.startswith('•') or line.startswith('-') or line.startswith('○') or line.startswith('■'):
            responsibilities.append(line[1:].strip())
            in_bullet_list = True
        elif in_bullet_list and (line[0].islower() or line.startswith('and ')):
            # Continuation of previous bullet point
            if responsibilities:
                responsibilities[-1] += ' ' + line
        elif re.match(r'^\d+\.\s', line):
            # Numbered list
            responsibilities.append(line[line.find('.')+1:].strip())
            in_bullet_list = True
        elif in_bullet_list and re.match(r'^[A-Z]', line) and len(line.split()) > 3:
            # New sentence in bullet format but without a bullet marker
            responsibilities.append(line)
    
    return responsibilities

def _load_job_titles():
    """Load job titles from data file"""
    try:
        if os.path.exists(JOB_TITLES_FILE):
            with open(JOB_TITLES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Fallback to built-in list
            return [
                "Software Engineer", "Senior Developer", "Frontend Developer", "Backend Developer",
                "Full Stack Developer", "Data Scientist", "Product Manager", "Project Manager",
                "UX Designer", "UI Designer", "DevOps Engineer", "QA Engineer", "Test Engineer",
                "Machine Learning Engineer", "Data Analyst", "Research Scientist", "IT Specialist",
                "Network Administrator", "Systems Administrator", "Database Administrator",
                "Business Analyst", "Technical Writer", "Scrum Master", "Agile Coach",
                "CTO", "CEO", "CIO", "VP of Engineering", "Director of Technology"
            ]
    except Exception as e:
        print(f"Error loading job titles: {str(e)}")
        return []