# Analyseur de Documents Immobiliers

## Description
Application web développée avec Streamlit pour analyser les documents légaux nécessaires lors d'une transaction immobilière.

## Fonctionnalités
- Lecture et analyse de documents PDF
- Extraction d'informations clés
- Visualisation interactive (pie chart)
- Interface utilisateur intuitive

## Installation
1. Cloner le repository
```bash
git clone [votre-url-repo]
```

2. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

3. Installer Tesseract OCR
- Windows : Installer depuis https://github.com/UB-Mannheim/tesseract/wiki
- Mac : `brew install tesseract`
- Linux : `sudo apt-get install tesseract-ocr`

## Technologies utilisées
- Python 3.x
- Streamlit
- Plotly
- PyMuPDF
- Tesseract OCR

## Structure du projet
```
project/
│
├── app.py                # Point d'entrée principal
├── requirements.txt      # Dépendances
├── .gitignore           # Fichiers à ignorer
│
├── src/                 # Code source
│   ├── pdf_reader.py    # Lecture des PDF
│   ├── data_extract.py  # Extraction des données
│   └── visualization.py # Visualisations
│
└── tests/              # Tests unitaires
    └── test_pdf.py
```

## Développement
- IDE : Cursor
- Version Python : 3.x
- Auteur : 333Ben