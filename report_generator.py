from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
from ai_suggestions import get_ai_suggestions
from datetime import datetime, timedelta

def generate_pdf_report(results, df=None):
    """Generate a simple PDF audit report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

   
    story.append(Paragraph("Financial Audit Report", styles['Title']))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 12))

    
    data = get_ai_suggestions(results, df)
    print(f"Data received from get_ai_suggestions: {repr(data)}")

    
    for section, header in [('overview', 'Overview'), ('insights', 'Key Insights'), 
                            ('risks', 'Risk Assessment'), ('suggestions', 'Suggestions'), 
                            ('notes', 'Notes')]:
        if section in data:
            story.append(Paragraph(header, styles['Heading2']))
            section_text = str(data[section])  
            print(f"Adding {header} to PDF: {repr(section_text)}")
            story.append(Paragraph(section_text, styles['Normal']))
            story.append(Spacer(1, 12))

    
    print("Building PDF with story content:", [str(item) for item in story])
    doc.build(story)

    buffer.seek(0)
    return buffer