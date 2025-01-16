import streamlit as st
import plotly.graph_objects as go
from budget_extract import extract_info, validate_pv_year

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
values = [1 for _ in data]
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

# Modifier la section des colonnes pour inclure la fonctionnalité d'upload
for key, item in data.items():
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"<span class='label'>{item['label']}</span>", unsafe_allow_html=True)
    
    with col2:
        if key in ['PV_2024', 'PV_2023', 'PV_2022']:
            expected_year = key.split('_')[1]
            uploaded_file = st.file_uploader(
                "Upload PV",
                type="pdf",
                key=f"upload_{key}",
                label_visibility="collapsed"
            )
            
            if uploaded_file:
                text = ""
                address, budget = extract_info(uploaded_file)
                if validate_pv_year(text, expected_year):
                    if address:
                        st.write(f"Adresse : {address}")
                    if budget:
                        st.write(f"Budget : {budget} Euros")
                else:
                    st.error(f"Ce document ne semble pas être un PV de {expected_year}")
        else:
            st.button("Download", disabled=True, key=f"disabled_{key}", use_container_width=True)
    
    with col3:
        st.checkbox("", key=f"check_{key}")

# Mettre à jour le style CSS
st.markdown("""
<style>
.stButton button {
    background-color: #E8FFF2 !important;
    border: 1px solid #D4FFE4 !important;
    color: #2E7D32 !important;
}
.stButton button:hover {
    background-color: #D4FFE4 !important;
    border-color: #2E7D32 !important;
}
.stButton button:disabled {
    background-color: #f0f0f0 !important;
    border-color: #cccccc !important;
    color: #666666 !important;
}
.label {
    font-size: 16px;
    padding: 8px 0;
}
</style>
""", unsafe_allow_html=True)