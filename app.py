import streamlit as st
import pdfplumber
import re

def analyze_pdf_structure(text):
    st.markdown("### 🔍 Texte brut extrait du PDF :")
    st.code(text, language='text')
    
    st.markdown("### 📝 Lignes numérotées :")
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():
            st.code(f"Ligne {i+1}: {line}")
            if 'budget' in line.lower() or '€' in line:
                st.info(f"🔎 Ligne importante : {line}")

st.set_page_config(page_title="Analyseur de PV d'AG - Debug", layout="wide")
st.title("📄 Analyseur de PV d'AG - Mode Debug")

# D'abord, installer pdfplumber
st.markdown("### 1. Installation de pdfplumber")
import subprocess
try:
    import pdfplumber
except ImportError:
    st.info("Installation de pdfplumber...")
    subprocess.check_call(["pip", "install", "pdfplumber"])
    import pdfplumber
    st.success("pdfplumber installé !")

uploaded_files = st.file_uploader("Choisir les PV (PDF)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.markdown(f"## 📁 Analyse du fichier : {file.name}")
        
        # Lecture du PDF avec pdfplumber
        with pdfplumber.open(file) as pdf:
            st.markdown(f"**Nombre de pages :** {len(pdf.pages)}")
            
            # Extraire et analyser le texte page par page
            for i, page in enumerate(pdf.pages):
                st.markdown(f"### 📃 Page {i+1}")
                text = page.extract_text()
                if text and text.strip():
                    analyze_pdf_structure(text)
                else:
                    st.warning(f"⚠️ Page {i+1} : Aucun texte extrait")