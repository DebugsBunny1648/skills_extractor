"""
Skills Extractor - Functions for extracting skills from resumes
"""
import re
import json
import os
from app.config import COMMON_SKILLS_FILE

def extract_skills(skills_text, nlp):
    """
    Extract skills from the skills section
    
    Args:
        skills_text: Text from the skills section
        nlp: Loaded spaCy NLP model
        
    Returns:
        list: List of extracted skills
    """
    if not skills_text:
        return []
        
    # Load common skills list
    common_skills = _load_common_skills()
    
    # Find skills in the text
    found_skills = []
    
    # Check for common skills
    for skill in common_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', skills_text.lower()):
            found_skills.append(skill)
    
    # Use NLP to find additional skills
    doc = nlp(skills_text)
    
    # Look for noun chunks that might be skills
    for chunk in doc.noun_chunks:
        skill_text = chunk.text.strip()
        if (len(skill_text) > 2 and 
            skill_text.lower() not in [s.lower() for s in found_skills] and
            not any(char.isdigit() for char in skill_text)):  # Filter out chunks with numbers
            found_skills.append(skill_text)
    
    # Look for skills separated by commas or bullets
    skill_candidates = re.findall(r'[•-]?\s*([A-Za-z+#]+(?:\s[A-Za-z+#]+)*)[,.]', skills_text)
    for skill in skill_candidates:
        skill = skill.strip()
        if (skill and 
            len(skill) > 2 and 
            skill.lower() not in [s.lower() for s in found_skills]):
            found_skills.append(skill)
            
    # Remove duplicates and sort
    found_skills = list(set(found_skills))
    found_skills.sort()
    
    return found_skills

def _load_common_skills():
    """Load common skills from data file"""
    try:
        if os.path.exists(COMMON_SKILLS_FILE):
            with open(COMMON_SKILLS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Fallback to built-in list
            return [
                "python", "java", "javascript", "html", "css", "react", "angular", "node.js", 
                "sql", "git", "agile", "scrum", "project management", "leadership", 
                "communication", "aws", "azure", "docker", "kubernetes", "machine learning",
                "data analysis", "excel", "powerpoint", "word", "tensorflow", "pytorch",
                "c++", "c#", "php", "ruby", "swift", "kotlin", "typescript", "rust", "golang",
                "scala", "r", "django", "flask", "spring boot", "laravel", "ruby on rails"
            ]
    except Exception as e:
        print(f"Error loading common skills: {str(e)}")
        return []