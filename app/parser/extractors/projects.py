"""
Projects Extractor - Functions for extracting project information from resumes
"""
import re

def extract_projects(projects_text):
    """
    Extract project information
    
    Args:
        projects_text: Text from the projects section
        
    Returns:
        list: List of dictionaries containing project information
    """
    if not projects_text:
        return []
        
    projects = []
    
    # Split into different project entries
    project_entries = re.split(r'\n\n+', projects_text)
    
    for entry in project_entries:
        if not entry.strip():
            continue
            
        # Extract project title
        lines = entry.strip().split('\n')
        title = lines[0] if lines else None
        
        # Extract description, technologies, and outcomes
        description = _extract_description(entry)
        technologies = _extract_technologies(entry)
        
        # Only add if we have at least a title
        if title:
            projects.append({
                'title': title,
                'description': description,
                'technologies': technologies
            })
    
    return projects

def _extract_description(text):
    """Extract project description"""
    # Split into lines
    lines = text.strip().split('\n')
    
    # Skip the first line (title) and any technology-specific lines
    description_lines = []
    
    # Skip first line (assumed to be title)
    for line in lines[1:]:
        # Skip technology-specific lines
        if re.search(r'technologies|tech stack|tools used|built with|developed using', line, re.IGNORECASE):
            continue
        
        # Add the line to description
        description_lines.append(line.strip())
    
    # Combine lines into a single description
    description = ' '.join(description_lines)
    
    # Clean up the description
    description = re.sub(r'\s+', ' ', description).strip()
    
    return description

def _extract_technologies(text):
    """Extract technologies used in the project"""
    technologies = []
    
    # Look for explicit technology sections
    tech_patterns = [
        r"Technologies used:[\s]*([\w\s,\.]+)",
        r"Tech Stack:[\s]*([\w\s,\.]+)",
        r"Tools:[\s]*([\w\s,\.]+)",
        r"Built with:[\s]*([\w\s,\.]+)",
        r"Developed using:[\s]*([\w\s,\.]+)"
    ]
    
    for pattern in tech_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            tech_list = match.group(1)
            # Split by commas or 'and'
            techs = re.split(r',|\sand\s', tech_list)
            for tech in techs:
                clean_tech = tech.strip()
                if clean_tech and clean_tech not in technologies:
                    technologies.append(clean_tech)
    
    # If no explicit technology section, try to find common technology keywords
    if not technologies:
        common_techs = [
            "Python", "Java", "JavaScript", "TypeScript", "C\\+\\+", "C#", "PHP", "Ruby",
            "HTML", "CSS", "SQL", "React", "Angular", "Vue", "Node.js", "Express",
            "Django", "Flask", "Spring", "Laravel", "Rails", "MongoDB", "PostgreSQL",
            "MySQL", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "TensorFlow",
            "PyTorch", "Pandas", "NumPy", "Sklearn"
        ]
        
        for tech in common_techs:
            if re.search(r'\b' + re.escape(tech) + r'\b', text, re.IGNORECASE):
                technologies.append(tech)
    
    return technologies