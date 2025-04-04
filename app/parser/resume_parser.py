"""
Resume Parser - Main parser class
"""
import os
import spacy
from app.parser.converter import convert_resume_to_text
from app.parser.preprocessor import preprocess_text
from app.parser.section_extractor import identify_sections
from app.parser.extractors.skills import extract_skills
from app.parser.extractors.experience import extract_experience
from app.parser.extractors.education import extract_education
from app.parser.extractors.certification import extract_certifications
from app.parser.extractors.projects import extract_projects
from app.config import NLP_MODEL

class ResumeParser:
    """Main class for parsing resumes"""
    
    def __init__(self, file_path):
        """Initialize the resume parser with a file path"""
        self.file_path = file_path
        self.nlp = spacy.load(NLP_MODEL)
        
    def parse(self):
        """Parse the resume and extract structured information"""
        try:
            # Step 1: Convert resume to text
            resume_text = convert_resume_to_text(self.file_path)
            
            # Step 2: Preprocess the text
            preprocessed_text = preprocess_text(resume_text)
            
            # Step 3: Identify sections
            sections = identify_sections(preprocessed_text)
            
            # Step 4: Extract information from each section
            resume_data = {
                'file_name': os.path.basename(self.file_path),
                'skills': extract_skills(sections.get('skills', ''), self.nlp),
                'experience': extract_experience(sections.get('experience', '')),
                'education': extract_education(sections.get('education', '')),
                'certifications': extract_certifications(sections.get('certifications', '')),
                'projects': extract_projects(sections.get('projects', ''))
            }
            
            return resume_data
            
        except Exception as e:
            print(f"Error processing resume {self.file_path}: {str(e)}")
            return None