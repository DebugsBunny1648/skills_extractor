#!/usr/bin/env python3
"""
Resume Parser - Streamlit version
"""
import os
import json
import streamlit as st
from app.parser.resume_parser import ResumeParser
from io import BytesIO
st.title("📄 Resume Parser")

import tempfile

def process_resume(uploaded_file, output_format='json'):
    """Process a single uploaded resume file"""
    try:
        # Create a temporary file to save the uploaded resume
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name  # Get the temp file path

        # Pass the temporary file path to ResumeParser
        resume_parser = ResumeParser(temp_file_path)
        parsed_data = resume_parser.parse()

        # Cleanup temp file
        os.remove(temp_file_path)

        if parsed_data:
            st.success("✅ Resume parsed successfully!")
            if output_format == 'json':
                st.subheader("Parsed Data (JSON Format)")
                st.json(parsed_data)
                json_str = json.dumps(parsed_data, indent=4)
                st.download_button("Download JSON", json_str, file_name="parsed_resume.json", mime="application/json")
            else:
                st.subheader("Parsed Data (Text Format)")
                txt_output = generate_txt_output(parsed_data)
                st.text(txt_output)
                st.download_button("Download TXT", txt_output, file_name="parsed_resume.txt", mime="text/plain")
        else:
            st.error("❌ Failed to parse resume.")

    except Exception as e:
        st.error(f"⚠️ Error while processing resume: {str(e)}")


def generate_txt_output(parsed_data):
    """Return parsed data in text format"""
    lines = ["=== RESUME PARSING RESULTS ===\n"]

    lines.append("SKILLS:")
    for skill in parsed_data.get('skills', []):
        lines.append(f"- {skill}")
    lines.append("")

    lines.append("EXPERIENCE:")
    for exp in parsed_data.get('experience', []):
        lines.append(f"- {exp.get('job_title', 'N/A')} at {exp.get('company', 'N/A')}, {exp.get('dates', 'N/A')}")
        for resp in exp.get('responsibilities', []):
            lines.append(f"  • {resp}")
    lines.append("")

    lines.append("EDUCATION:")
    for edu in parsed_data.get('education', []):
        lines.append(f"- {edu.get('degree', 'N/A')} from {edu.get('institution', 'N/A')}, {edu.get('graduation_date', 'N/A')}")
        if edu.get('gpa'):
            lines.append(f"  GPA: {edu.get('gpa')}")
    lines.append("")

    lines.append("CERTIFICATIONS:")
    for cert in parsed_data.get('certifications', []):
        line = f"- {cert.get('name', 'N/A')}"
        if cert.get('authority'):
            line += f", {cert.get('authority')}"
        if cert.get('date'):
            line += f", {cert.get('date')}"
        lines.append(line)
    lines.append("")

    lines.append("PROJECTS:")
    for proj in parsed_data.get('projects', []):
        lines.append(f"- {proj.get('title', 'N/A')}")
        lines.append(f"  {proj.get('description', 'N/A')}")
        if proj.get('technologies'):
            lines.append(f"  Technologies: {', '.join(proj.get('technologies'))}")
    lines.append("")

    return "\n".join(lines)

# Streamlit UI
uploaded_file = st.file_uploader("📤 Upload your resume", type=['pdf', 'docx', 'doc', 'txt'])

output_format = st.radio("Choose Output Format", ['json', 'txt'])

if st.button("🚀 Parse Resume") and uploaded_file is not None:
    process_resume(uploaded_file, output_format)
elif uploaded_file is None:
    st.info("👆 Please upload a resume file to begin.")