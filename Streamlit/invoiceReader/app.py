import streamlit as st
import PyPDF2
import re

def extract_information(text):
    # Define regular expressions to match the desired patterns
    ean_code_pattern = re.search(r'EAN-code\s(\d+)', text)
    periode_pattern = re.search(r'Periode\s\d{2}/\d{2}/\d{4}\s-\s\d{2}/\d{2}/\d{4}', text)
    total_pattern = re.search(r'Totaal\s+€\s+([\d.,]+)\s+€\s+([\d.,]+)\s+€\s+([\d.,]+)', text)

    # Extract matched patterns or groups
    ean_code = ean_code_pattern.group(1) if ean_code_pattern else None
    periode = periode_pattern.group(0) if periode_pattern else None
    total = total_pattern.groups() if total_pattern else None

    # Split text by lines and filter for lines starting with 'Injectie'
    lines = text.split('\n')
    invoice_items = [line.strip() for line in lines if line.startswith('Injectie')]

    return ean_code, periode, invoice_items, total

def main():
    st.title("Invoice Information Extraction")

    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ""
        for page_num in range(len(pdf_reader.pages)):
          page = pdf_reader.pages[page_num]
          pdf_text += page.extract_text()

        ean_code, periode, invoice_items, total = extract_information(pdf_text)

        st.header("Extracted Information:")
        st.write(f"EAN-code: {ean_code}")
        st.write(f"Periode: {periode}")
        st.write("Invoice Items:")
        for item in invoice_items:
            st.write(item)
        st.write(f"Total: Hoeveelheid: {total[0]}€, Tarief Eenheid: {total[1]}, € Bedrag: {total[2]}€" if total else None)

if __name__ == "__main__":
    main()
