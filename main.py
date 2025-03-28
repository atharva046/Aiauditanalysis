import streamlit as st
from file_processor import extract_text_and_numbers
from report_generator import generate_pdf_report
from datetime import datetime

st.title("Financial Audit Review Tool with Numerical Analysis")

uploaded_file = st.file_uploader("Upload a file (CSV, PDF, Word, TXT, PNG, JPG)", 
                                type=['csv', 'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'])

if uploaded_file:
    
    file_content, df = extract_text_and_numbers(uploaded_file)
    if file_content:
        st.write("### Extracted Document Content")
        st.text(file_content[:500] + "..." if len(file_content) > 500 else file_content)
        if df is not None:
            st.write("### Numerical Data Preview")
            st.dataframe(df.head())

        
        if st.button("Generate PDF Report"):
            pdf_buffer = generate_pdf_report(file_content, df)
            st.download_button(
                label="Download Audit Report",
                data=pdf_buffer,
                file_name=f"Audit_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Failed to extract text from the uploaded file.")