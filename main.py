#!/usr/bin/env python3
"""
Resume Parser - Main entry point
"""
import os
import json
import argparse
from app.parser.resume_parser import ResumeParser

def main():
    """Main function to run the resume parser"""
    parser = argparse.ArgumentParser(description='Parse resumes and extract structured information')
    parser.add_argument('--input', '-i', required=True, help='Input file or directory containing resumes')
    parser.add_argument('--output', '-o', default='output', help='Output directory for parsed results')
    parser.add_argument('--format', '-f', choices=['json', 'txt'], default='json', help='Output format')
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Check if input is a file or directory
    if os.path.isfile(args.input):
        process_single_file(args.input, args.output, args.format)
    elif os.path.isdir(args.input):
        process_directory(args.input, args.output, args.format)
    else:
        print(f"Error: {args.input} is not a valid file or directory")

def process_single_file(file_path, output_dir, output_format):
    """Process a single resume file"""
    try:
        print(f"Processing: {file_path}")
        resume_parser = ResumeParser(file_path)
        parsed_data = resume_parser.parse()
        
        if parsed_data:
            # Generate output file name
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file = os.path.join(output_dir, f"{base_name}.{output_format}")
            
            # Save result
            if output_format == 'json':
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(parsed_data, f, indent=4)
            else:  # txt format
                write_txt_output(parsed_data, output_file)
                
            print(f"Successfully processed: {file_path}")
            print(f"Output saved to: {output_file}")
        else:
            print(f"Failed to parse: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

def process_directory(dir_path, output_dir, output_format):
    """Process all resume files in a directory"""
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt']
    
    for root, _, files in os.walk(dir_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                file_path = os.path.join(root, file)
                process_single_file(file_path, output_dir, output_format)

def write_txt_output(parsed_data, output_file):
    """Write parsed data to a text file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== RESUME PARSING RESULTS ===\n\n")
        
        # Write skills
        f.write("SKILLS:\n")
        for skill in parsed_data.get('skills', []):
            f.write(f"- {skill}\n")
        f.write("\n")
        
        # Write experience
        f.write("EXPERIENCE:\n")
        for exp in parsed_data.get('experience', []):
            f.write(f"- {exp.get('job_title', 'N/A')} at {exp.get('company', 'N/A')}, {exp.get('dates', 'N/A')}\n")
            for resp in exp.get('responsibilities', []):
                f.write(f"  • {resp}\n")
        f.write("\n")
        
        # Write education
        f.write("EDUCATION:\n")
        for edu in parsed_data.get('education', []):
            f.write(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}, {edu.get('graduation_date', 'N/A')}\n")
            if edu.get('gpa'):
                f.write(f"  GPA: {edu.get('gpa')}\n")
        f.write("\n")
        
        # Write certifications
        f.write("CERTIFICATIONS:\n")
        for cert in parsed_data.get('certifications', []):
            f.write(f"- {cert.get('name', 'N/A')}")
            if cert.get('authority'):
                f.write(f", {cert.get('authority')}")
            if cert.get('date'):
                f.write(f", {cert.get('date')}")
            f.write("\n")
        f.write("\n")
        
        # Write projects
        f.write("PROJECTS:\n")
        for proj in parsed_data.get('projects', []):
            f.write(f"- {proj.get('title', 'N/A')}\n")
            f.write(f"  {proj.get('description', 'N/A')}\n")
            if proj.get('technologies'):
                f.write(f"  Technologies: {', '.join(proj.get('technologies'))}\n")
        f.write("\n")

if __name__ == "__main__":
    main()