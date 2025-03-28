from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import pytesseract
from PIL import Image
import re

def extract_text_and_numbers(uploaded_file):
    
    text = ""
    df = None
    
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        text = df.to_string()
    elif uploaded_file.name.endswith('.pdf'):
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif uploaded_file.name.endswith('.docx'):
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif uploaded_file.name.endswith('.txt'):
        text = uploaded_file.read().decode('utf-8')
    elif uploaded_file.name.endswith(('.png', '.jpg', '.jpeg')):
        image = Image.open(uploaded_file)
        text = pytesseract.image_to_string(image)

  
    if df is None and text:
        numbers = re.findall(r'-?\d+\.?\d*', text)  
        if numbers:
            df = pd.DataFrame({'Extracted_Numbers': [float(n) for n in numbers]})

    return text, df