import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re
import plotly.graph_objects as go

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
    
    return address, budget

# Data structure for the pie chart
data = {
    'PV_2024': {
        'label': 'PV 2024',
        'status': 'incomplete',
        'hover_text': 'budget de copropriété, travaux dans l\'immeuble, disputes...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#A7D8FF'
    },
    'PV_2023': {
        'label': 'PV 2023',
        'status': 'incomplete',
        'hover_text': 'budget de copropriété, travaux dans l\'immeuble, disputes...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#BCE4FF'
    },
    'PV_2022': {
        'label': 'PV 2022',
        'status': 'incomplete',
        'hover_text': 'budget de copropriété, travaux dans l\'immeuble, disputes...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#D1EDFF'
    },
    'Plomb/Amiante/Termite': {
        'label': 'Plomb/Amiante/Termite',
        'status': 'incomplete',
        'hover_text': 'certains endroits dans l\'appartement peuvent contenir...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#98FFB3'
    },
    'Gaz/Électricité': {
        'label': 'Gaz/Électricité',
        'status': 'incomplete',
        'hover_text': 'text',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#BDFFD4'
    },
    'Carrez': {
        'label': 'Carrez',
        'status': 'incomplete',
        'hover_text': 'mesure officielle de la surface de l\'appartement, qui comprend...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#D4FFE4'
    },
    'DPE': {
        'label': 'DPE',
        'status': 'incomplete',
        'hover_text': 'text',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#E8FFF2'
    },
    'Appel de charges': {
        'label': 'Appel de charges',
        'status': 'incomplete',
        'hover_text': 'charges à payer pour...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#FFD4BC'
    },
    'Taxe foncière': {
        'label': 'Taxe foncière',
        'status': 'incomplete',
        'hover_text': 'taxe annuelle à payer en...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#FFE4D4'
    },
    'RCP': {
        'label': 'RCP',
        'status': 'incomplete',
        'hover_text': 'règlement de copropriété de l\'immeuble permet de comparer...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#FFD4E5'
    },
    'Titre': {
        'label': 'Titre',
        'status': 'incomplete',
        'hover_text': 'description de votre lot, à comparer avec...',
        'details_text': 'texte complet sur le budget de copropriété...',
        'color': '#E0D4FF'
    }
}

# Prepare data for the pie chart
labels = [data[key]['label'] for key in data]
values = [1 for _ in data]  # Assuming each section has equal weight
colors = [data[key]['color'] for key in data]
hover_texts = [data[key]['hover_text'] for key in data]

# Create the pie chart
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hovertext=hover_texts, marker=dict(colors=colors))])
fig.update_layout(
    width=400, 
    height=400, 
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False
)
fig.update_traces(
    textinfo='label+percent',
    textposition='inside',
    insidetextorientation='radial',
    hoverinfo='label+text',
    marker=dict(line=dict(color='#000000', width=2))
)

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

# Display the pie chart
st.plotly_chart(fig)

# Download section layout
st.markdown("""
<style>
.download-section {
    display: flex;
    align-items: center;
    line-height: 36px;
    margin-bottom: 12px;
}
.download-section .label {
    margin-right: 12px;
}
.download-section .button {
    background-color: #E8FFF2;
    border: 1px solid #D4FFE4;
    color: #2E7D32;
    padding: 8px 12px;
    border-radius: 6px;
    margin-right: 12px;
}
.download-section .checkbox {
    width: 18px;
    height: 18px;
    border: 2px solid #D4FFE4;
    margin-right: 12px;
}
.download-section .status-icon {
    width: 20px;
    height: 20px;
}
</style>
""", unsafe_allow_html=True)

# Example download section
st.markdown("""
<div class="download-section">
    <span class="label">PV 2024</span>
    <button class="button">Download</button>
    <input type="checkbox" class="checkbox">
    <img src="success_icon.svg" class="status-icon">
</div>
""", unsafe_allow_html=True)