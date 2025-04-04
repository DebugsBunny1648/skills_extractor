"""
Education Extractor - Functions for extracting education information from resumes
"""
import re

def extract_education(education_text):
    """
    Extract education information
    
    Args:
        education_text: Text from the education section
        
    Returns:
        list: List of dictionaries containing education information
    """
    if not education_text:
        return []
        
    education = []
    
    # Split into different education entries
    edu_entries = re.split(r'\n\n+', education_text)
    
    for entry in edu_entries:
        if not entry.strip():
            continue
            
        # Extract degree
        degree = _extract_degree(entry)
        
        # Extract institution
        institution = _extract_institution(entry)
        
        # Extract graduation date
        graduation_date = _extract_graduation_date(entry)
        
        # Extract GPA
        gpa = _extract_gpa(entry)
        
        # Only add if we have at least a degree or institution
        if degree or institution:
            education.append({
                'degree': degree,
                'institution': institution,
                'graduation_date': graduation_date,
                'gpa': gpa
            })
    
    return education

def _extract_degree(text):
    """Extract degree information"""
    # Common degree patterns
    degree_patterns = [
        # Full degree names
        r"(Bachelor|Master|PhD|Doctorate|Associate).+?(of|in|'s in|'s of).+?(Engineering|Science|Arts|Commerce|Business|Administration|Technology|Computer Science|Economics|Finance|Mathematics|Physics)",
        # Abbreviated degrees
        r"(B\.S\.|M\.S\.|B\.A\.|M\.A\.|B\.Tech|M\.Tech|B\.E\.|M\.E\.|Ph\.D\.|M\.B\.A\.|B\.B\.A\.).+?(Engineering|Science|Arts|Commerce|Business|Administration|Technology|Computer Science|Economics|Finance|Mathematics|Physics)",
        # Just the qualification
        r"(Bachelor|Master|PhD|Doctorate|Associate)'s degree",
        # Major without explicit degree mention
        r"Major in (Computer Science|Engineering|Business|Economics|Finance|Mathematics|Physics)"
    ]
    
    for pattern in degree_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Return the full match or just the degree part based on pattern
            if "Major in" in pattern:
                return f"Degree in {match.group(1)}"
            return match.group(0).strip()
    
    return None

def _extract_institution(text):
    """Extract institution name"""
    # Common patterns for institutions
    institution_patterns = [
        # University/College/Institute of Name
        r"(University|College|Institute|School) of [\w\s]+",
        # Name University/College/Institute
        r"[\w\s]+ (University|College|Institute|School)",
        # Common prestigious institutions
        r"(Stanford|Harvard|MIT|Yale|Princeton|Oxford|Cambridge|Berkeley|UCLA)"
    ]
    
    for pattern in institution_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    
    return None

def _extract_graduation_date(text):
    """Extract graduation date"""
    # Various date formats
    graduation_patterns = [
        # Month Year
        r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]+\d{4}",
        # Year only
        r"(Graduated|Completed|Finished|Class of|Expected|Exp)[\s:]+(\d{4})",
        # Just the year
        r"\b(20\d{2}|19\d{2})\b"
    ]
    
    for pattern in graduation_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if "Graduated|Completed|Finished|Class of|Expected|Exp" in pattern:
                return match.group(2).strip()  # Return just the year
            return match.group(0).strip()
    
    return None

def _extract_gpa(text):
    """Extract GPA information"""
    # GPA patterns
    gpa_patterns = [
        r"GPA[:\s]+(\d+\.\d+)",
        r"Grade Point Average[:\s]+(\d+\.\d+)",
        r"G\.P\.A\.?[:\s]+(\d+\.\d+)",
        r"GPA of (\d+\.\d+)",
        r"(\d+\.\d+)/4\.0"
    ]
    
    for pattern in gpa_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None