import google.generativeai as genai
import pandas as pd
from PIL import Image
import pytesseract
import os
import re


genai.configure(api_key="AIzaSyBC9XxLf3Jwz5O_1KdJn-TY4UG4t4ctfcM")

def extract_text_from_image(file_path_or_binary):
    """Extract text from an image using OCR."""
    try:
        if isinstance(file_path_or_binary, str) and os.path.exists(file_path_or_binary):
            image = Image.open(file_path_or_binary)
        else:
            image = Image.open(file_path_or_binary)
        text = pytesseract.image_to_string(image)
        extracted = text.strip() if text else ""
        print(f"OCR extracted text: {repr(extracted)}")
        return extracted
    except Exception as e:
        print(f"OCR failed: {str(e)}")
        return ""

def get_ai_suggestions(document_text, df=None):
    """Generate audit report content using Gemini API."""
    print(f"Input type: {type(document_text)}")
    
   
    if isinstance(document_text, (str, bytes)) and (
        (isinstance(document_text, str) and document_text.lower().endswith(('.png', '.jpg', '.jpeg'))) or
        isinstance(document_text, bytes)
    ):
        extracted_text = extract_text_from_image(document_text)
        if not extracted_text:
            print("No text extracted from image")
            return {'overview': 'Error: Failed to extract text from image using OCR'}
    else:
        extracted_text = str(document_text)
        print(f"Input text: {repr(extracted_text[:100])}...")

  
    numerical_summary = ""
    if df is not None and not df.empty:
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if numeric_cols.size > 0:
            summary = f"Columns: {', '.join(numeric_cols)}\nTotal Rows: {len(df)}\nSum: {df[numeric_cols].sum().to_string()}"
            numerical_summary = f"\n\nNumerical Data Summary:\n{summary}"
            print(f"Numerical summary: {numerical_summary}")

   
    truncated_text = extracted_text[:10000]
    full_input = f"{truncated_text}{numerical_summary}"
    
    prompt = (
        "Analyze the following document and numerical data (if provided) and generate a comprehensive audit report. "
        "Ensure each section has detailed, meaningful content. If no specific insights are found, provide general observations. "
        "Include these sections:\n"
        "1. Overview: Comprehensive summary of the document's purpose and key points.\n"
        "2. Insights: Significant findings, trends, or patterns in the data.\n"
        "3. Risks: Potential issues, anomalies, or areas of concern.\n"
        "4. Suggestions: Actionable recommendations based on the analysis.\n"
        "5. Notes: Additional context, methodology, or limitations.\n"
        "Format the response with clear section headers like 'Overview:', 'Insights:', etc. "
        "Write in a professional, analytical tone.\n\n"
        f"{full_input}"
    )
    print(f"Prompt sent to Gemini: {repr(prompt[:200])}...")

    
    content = None
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=2000, 
                temperature=0.7
            )
        )
        content = response.text.strip()
        print(f"Gemini raw response length: {len(content)}")
        print(f"Gemini raw response: {repr(content[:500])}...")
    except Exception as e:
        error_msg = f"Gemini API failed: {str(e)}"
        print(error_msg)
        return {'overview': error_msg}

    
    results = {}
    section_patterns = [
        ('overview', r'Overview:(.*?)(?=Insights:|$)', 'No overview available.'),
        ('insights', r'Insights:(.*?)(?=Risks:|$)', 'No specific insights found.'),
        ('risks', r'Risks:(.*?)(?=Suggestions:|$)', 'No significant risks identified.'),
        ('suggestions', r'Suggestions:(.*?)(?=Notes:|$)', 'No recommendations at this time.'),
        ('notes', r'Notes:(.*)', 'No additional notes.')
    ]

    for section, pattern, default_text in section_patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1).strip()
            results[section] = section_content if section_content else default_text
        else:
            results[section] = default_text


    if not any(results.values()):
        results['overview'] = 'Unable to generate analysis. Please review the original document.'

    print("Final results:")
    for section, content in results.items():
        print(f"{section.capitalize()}: {repr(content)}")

    return results