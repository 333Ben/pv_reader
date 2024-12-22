import streamlit as st
import PyPDF2
import io

# Configuration de la page
st.set_page_config(
    page_title="Lecteur de PV",
    layout="wide"
)

# Titre de l'application
st.title("Lecteur de PV d'AG")

# Upload de fichier PDF
uploaded_file = st.file_uploader("Choisir un PV (PDF)", type="pdf")

if uploaded_file is not None:
    # Lecture du PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Affichage du contenu
    with st.expander("Contenu du PV", expanded=True):
        st.write(text)
    
    # Questions prédéfinies
    st.subheader("Questions sur le PV")
    questions = [
        "Quelle est la date de l'AG ?",
        "Combien de participants étaient présents ?",
        "Quelles sont les principales décisions prises ?"
    ]
    
    for question in questions:
        st.text_input(question)

# Footer
st.markdown("---")
st.markdown("*Ce projet est en cours de développement*")