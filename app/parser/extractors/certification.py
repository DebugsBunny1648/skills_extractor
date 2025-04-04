"""
Certification Extractor - Functions for extracting certification information from resumes
"""
import re

def extract_certifications(certifications_text):
    """
    Extract certification information
    
    Args:
        certifications_text: Text from the certifications section
        
    Returns:
        list: List of dictionaries containing certification information
    """
    if not certifications_text:
        return []
        
    certifications = []
    
    # Split into different certification entries
    cert_entries = re.split(r'\n+', certifications_text)
    
    for entry in cert_entries:
        entry = entry.strip()
        if not entry:
            continue
            
        # Extract certification name
        cert_name = _extract_certification_name(entry)
        
        # Extract issuing authority
        authority = _extract_authority(entry)
        
        # Extract date
        date = _extract_certification_date(entry)
        
        # Extract credential ID
        credential_id = _extract_credential_id(entry)
        
        # Only add if we have at least a name
        if cert_name:
            certifications.append({
                'name': cert_name,
                'authority': authority,
                'date': date,
                'credential_id': credential_id
            })
    
    return certifications

def _extract_certification_name(text):
    """Extract certification name"""
    # If there's a comma, the first part is likely the certification name
    if ',' in text:
        return text.split(',')[0].strip()
    
    # If there are common certification keywords
    cert_keywords = [
        "Certified", "Professional", "Specialist", "Expert", "Associate", 
        "Certificate", "Certification", "Diploma", "License"
    ]
    
    for keyword in cert_keywords:
        if keyword in text:
            # Find the phrase containing the keyword
            pattern = rf"{keyword}[\w\s]+"
            match = re.search(pattern, text)
            if match:
                return match.group(0).strip()
    
    # If nothing else works, just take the first line or sentence
    first_line = text.split('\n')[0] if '\n' in text else text
    first_sentence = first_line.split('.')[0] if '.' in first_line else first_line
    
    # Limit to a reasonable length
    if len(first_sentence) > 100:
        return first_sentence[:100].strip() + "..."
    
    return first_sentence.strip()

def _extract_authority(text):
    """Extract issuing authority"""
    # Common patterns for issuing authorities
    authority_patterns = [
        r"(issued|provided|awarded|offered|certified) by\s+([\w\s]+)",
        r"from\s+([\w\s]+)",
        r"by\s+([\w\s,\.]+)(?=\s+in|\s+on|\s+\(|\s*$)",
        r"-\s+([\w\s]+)(?=\s+\d{4}|\s+certification)"
    ]
    
    for pattern in authority_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if match.group(1).lower() in ["issued", "provided", "awarded", "offered", "certified"]:
                return match.group(2).strip()
            return match.group(1).strip()
    
    # Look for common certification providers
    providers = [
        "Microsoft", "AWS", "Amazon", "Google", "Oracle", "Cisco", "CompTIA", 
        "PMI", "Scrum Alliance", "Salesforce", "Adobe", "IBM", "Apple", "SAP"
    ]
    
    for provider in providers:
        if provider in text:
            return provider
    
    return None

def _extract_certification_date(text):
    """Extract certification date"""
    # Various date formats
    date_patterns = [
        # Month Year
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4}",
        # Year only with context
        r"(Issued|Received|Completed|Earned|Certified)[\s:]+in[\s:]+(\d{4})",
        # Year only
        r"\b(20\d{2}|19\d{2})\b"
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if "Issued|Received|Completed|Earned|Certified" in pattern:
                return match.group(2).strip()  # Return just the year
            return match.group(0).strip()
    
    return None

def _extract_credential_id(text):
    """Extract credential ID"""
    # ID patterns
    id_patterns = [
        r"ID[\s:]+([A-Za-z0-9-]+)",
        r"Credential ID[\s:]+([A-Za-z0-9-]+)",
        r"Certificate ID[\s:]+([A-Za-z0-9-]+)",
        r"Certification Number[\s:]+([A-Za-z0-9-]+)",
        r"#([A-Za-z0-9-]+)"
    ]
    
    for pattern in id_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None