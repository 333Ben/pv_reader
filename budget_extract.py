import pytesseract
from PIL import Image
import re
import fitz  # PyMuPDF
import os
import shutil

# Configuration de Tesseract
tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Chemin spécifique pour Mac avec Apple Silicon
if os.path.exists(tesseract_cmd):
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    tesseract_cmd = shutil.which('tesseract')
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

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
    os.remove("temp.pdf")
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
            budget_patterns = [
                r"période du \d{2}/\d{2}/\d{4}.*?pour un montant de ([\d\s,]+)\s*€",
                r"montant de ([\d\s,]+)\s*€",
                r"arrêtée? au \d{2}/\d{2}/\d{4}.*?montant de ([\d\s,]+)\s*€",
                r"budget.*?([\d\s,]+)\s*€",
                r"charges.*?([\d\s,]+)\s*€"
            ]
            
            for pattern in budget_patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    budget = match.group(1).strip()
                    budget = budget.replace(" ", "").replace(",", ".")
                    break
    
    return address, budget

def validate_pv_year(text, expected_year):
    """Vérifie si le PV correspond à l'année attendue"""
    year_patterns = [
        f"AG.*{expected_year}",
        f"exercice.*{expected_year}",
        f"{expected_year}.*exercice",
        f"décembre {expected_year}",
        f"{expected_year}",
        f"PROCES-VERBAL.*{expected_year}",
        f"Annuelle.*{expected_year}"
    ]
    
    for pattern in year_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False 