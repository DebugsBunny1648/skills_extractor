# Resume Parser

A robust Python tool for extracting structured information from resumes in various formats.

## Features

- Extract key information from resumes including:
  - Skills
  - Work experience
  - Education
  - Certifications
  - Projects
- Support for multiple file formats (PDF, DOCX, TXT)
- Clean and modular code structure
- Configurable extraction patterns
- Command-line interface for easy usage

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/resume-parser.git
   cd resume-parser
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_lg
   ```

## Usage

### Command Line Interface

Process a single resume:
```bash
python main.py --input path/to/resume.pdf --output output_directory
```

Process all resumes in a directory:
```bash
python main.py --input path/to/resumes_directory --output output_directory
```

### Output Format

By default, the parser outputs JSON files. You can specify the output format:
```bash
python main.py --input path/to/resume.pdf --output output_directory --format txt
```

### Programmatic Usage

```python
from app.parser.resume_parser import ResumeParser

# Parse a single resume
parser = ResumeParser("path/to/resume.pdf")
results = parser.parse()

# Access extracted information
skills = results['skills']
experience = results['experience']
education = results['education']
```

## Project Structure

```
resume-parser/
│
├── app/
│   ├── parser/
│   │   ├── converter.py       # File conversion functions
│   │   ├── preprocessor.py    # Text cleaning and normalization
│   │   ├── section_extractor.py  # Section identification
│   │   ├── extractors/        # Section-specific extractors
│   │   └── utils.py           # Helper functions
│   │
│   ├── data/                  # Reference data for matching
│   └── config.py              # Configuration settings
│
├── main.py                    # Main entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Customization

### Adding New Skills

Edit the `app/data/common_skills.json` file to add new skills to the recognition database.

### Improving Section Recognition

Modify the section headers in `app/config.py` to improve section identification for your specific resume formats.

## Testing

Run the test suite:
```bash
pytest
```
