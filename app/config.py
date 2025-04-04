"""
Configuration settings for the resume parser
"""
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directory
DATA_DIR = os.path.join(BASE_DIR, 'app', 'data')

# NLP settings
NLP_MODEL = "en_core_web_lg"  # spaCy model to use

# Supported file types
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.txt']

# File paths for reference data
COMMON_SKILLS_FILE = os.path.join(DATA_DIR, 'common_skills.json')
JOB_TITLES_FILE = os.path.join(DATA_DIR, 'job_titles.json')

# Section identification settings
SECTION_HEADERS = {
    'experience': ['experience', 'work experience', 'employment', 'work history', 'professional experience'],
    'education': ['education', 'academic background', 'academic history', 'educational qualifications'],
    'skills': ['skills', 'technical skills', 'competencies', 'expertise', 'core competencies'],
    'certifications': ['certifications', 'certificates', 'professional certifications', 'credentials'],
    'projects': ['projects', 'personal projects', 'professional projects', 'key projects']
}