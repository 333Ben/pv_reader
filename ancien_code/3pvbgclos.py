import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

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
            # Rechercher la section "Approbation des comptes de l'exercice"
            section_match = re.search(r"Approbation des comptes de l'exercice.*?arrêtés à la somme de\s*([\d\s,]+)\s*€", text, re.IGNORECASE | re.DOTALL)
            if section_match:
                budget = section_match.group(1).replace(" ", "").replace(",", ".")
                logging.info(f"Budget extrait: {budget}")
            else:
                logging.error("Section 'Approbation des comptes de l'exercice' non trouvée.")
    
    return address, budget

st.set_page_config(page_title="Analyse mes PV d'AG", layout="wide")
st.title("📄 Analyse mes PV d'AG")

uploaded_files = st.file_uploader("Choisir les PVs (PDF)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    first_address = None
    for uploaded_file in uploaded_files:
        address, budget = extract_info(uploaded_file)
        
        if first_address is None:
            first_address = address
            st.write(f"PV d'AG de la copropriété : {address}")
        elif address != first_address:
            st.error(f"Adresse différente détectée : {address}. Elle ne correspond pas à {first_address}.")
            continue
        
        if budget:
            st.write(f"Le budget de l'exercice clos est : {budget} Euros")
        else:
            st.error("Le budget de l'exercice clos n'a pas pu être extrait.")