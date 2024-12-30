import streamlit as st
import PyPDF2
import re
from datetime import datetime

def extract_budget_info(text):
    # Recherche plus précise des budgets dans le texte du PV
    sections = text.split('\n')
    budgets = []
    years = []
    points = []
    
    for i, line in enumerate(sections):
        # Recherche des sections de budget
        if "budget prévisionnel" in line.lower():
            # Chercher le montant sur cette ligne et les 3 suivantes
            for j in range(4):
                if i+j < len(sections):
                    search_line = sections[i+j]
                    # Recherche de montants avec le symbole €
                    amount_match = re.search(r'(\d{2,3}(?:\s*\d{3})*(?:[.,]\d{2})?)\s*[€Ee]', search_line)
                    if amount_match:
                        # Chercher l'année associée
                        year_match = re.search(r'20\d{2}', search_line)
                        if year_match:
                            years.append(year_match.group())
                            budgets.append(amount_match.group(1).replace(" ", ""))
                            # Chercher le numéro du point
                            point_match = re.search(r'point\s*(\d+)', search_line, re.IGNORECASE)
                            points.append(point_match.group(1) if point_match else "N/A")

    return years, points, budgets

# Configuration de la page
st.set_page_config(page_title="Analyseur de PV d'AG", layout="wide")
st.title("Analyseur de PV d'AG")

# Zone de téléchargement multiple
uploaded_files = st.file_uploader("Choisir les PV (PDF)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.subheader("1 - Budget annuel dépenses courantes :")
    
    all_budgets = []
    for file in uploaded_files:
        # Lecture du PDF
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        # Extraction des informations
        years, points, budgets = extract_budget_info(text)
        
        # Stockage des informations
        for i in range(len(years)):
            all_budgets.append({
                'year': years[i],
                'point': points[i],
                'budget': budgets[i]
            })
    
    # Affichage des résultats triés par année
    for budget in sorted(all_budgets, key=lambda x: x['year']):
        st.write(f"{budget['year']} - point {budget['point']} - {budget['budget']} Euros")

    # Affichage du texte brut pour debug
    with st.expander("Débug - Contenu du dernier PV"):
        st.text(text)