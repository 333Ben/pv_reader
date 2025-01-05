import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re

def convert_pdf_to_images(pdf_file):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.getvalue())
    
    pdf_document = fitz.open("temp.pdf")
    images = []
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    
    pdf_document.close()
    return images

def extract_info(file):
    images = convert_pdf_to_images(file)
    
    address = ""
    budget = ""
    
    for page_num, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang='fra')
        
        if page_num == 0:  # Première page
            lines = text.split('\n')
            for line in lines[:5]:  # Chercher l'adresse dans les 5 premières lignes
                if re.search(r'\d+.*rue|avenue|boulevard', line, re.IGNORECASE):
                    address = line.strip()
                    break
        
        if not budget:
            budget_match = re.search(r'budget.*?(\d+(?:\s?\d+)*(?:,\d+)?)\s*(?:€|euros)', text, re.IGNORECASE | re.DOTALL)
            if budget_match:
                budget = budget_match.group(1).replace(" ", "")
    
    return address, budget

st.set_page_config(page_title="Analyseur de PV d'AG", layout="wide")
st.title("📄 Analyseur de PV d'AG")

uploaded_files = st.file_uploader("Choisir les PVs (PDF)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        address, budget = extract_info(uploaded_file)
        st.write(f"PV d'AG de la copropriété : {address}")
        st.write(f"Le budget de l'exercice clos est : {budget} Euros")