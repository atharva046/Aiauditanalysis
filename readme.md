# DocInsight: AI Audit Analysis Tool

## Overview
DocInsight is an intelligent document analysis application that helps users extract insights from various file types using AI-powered analysis. The tool supports CSV, PDF, Word, TXT, and image files, providing comprehensive audit reports with automated insights.

## Features
- Multi-file type support (CSV, PDF, DOCX, TXT, PNG, JPG)
- Optical Character Recognition (OCR) for image files
- AI-powered document analysis
- Automated PDF report generation
- Numerical data extraction and analysis

## Prerequisites
- Python 3.8+
- Google Cloud account (for Gemini API)
- Tesseract OCR installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/atharva046/Aiauditanalysis.git
cd Aiauditanalysis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- On Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- On macOS: `brew install tesseract`
- On Windows: Download and install from the official Tesseract GitHub page

## Configuration
⚠️ IMPORTANT API KEY SETUP:
1. **REPLACE THE API KEY**: 
   - Open `ai_suggestions.py`
   - Replace the hardcoded Gemini API key with YOUR OWN Google AI API key
   
### Recommended API Key Management
```python
# Example of secure API key usage
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
genai.configure(api_key=api_key)
```

## Running the Application
```bash
streamlit run main.py
```

## File Structure
- `main.py`: Streamlit web application
- `file_processor.py`: File parsing and text extraction
- `report_generator.py`: PDF report generation
- `ai_suggestions.py`: AI-powered analysis using Gemini

## Usage
1. Upload a supported file type
2. View extracted content and numerical data
3. Generate a PDF audit report with AI-powered insights

## Limitations
- Maximum file size may be limited
- OCR accuracy depends on image quality
- Gemini API usage is subject to Google's terms and pricing

## Security Notes
- Never share your API key publicly
- Use environment variables or secure secret management
- Be cautious with sensitive documents

## Contributing
Contributions are welcome! Please submit pull requests or open issues on GitHub.

## License
[Specify your license, e.g., MIT License]

## Disclaimer
This tool provides automated insights and should not replace professional financial advice. Users are responsible for verifying the accuracy of generated reports.