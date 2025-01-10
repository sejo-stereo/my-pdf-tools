import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.write(f"Desarrollado por José Melgarejo.")

pages = {
    "GENERAL":
    [
    st.Page("src//01_Unir_PDF.py",title="UNIR PDF",icon="🖇",url_path="unir_pdf"),
    st.Page("src//02_Separar_PDF.py",title="SEPARAR PDF",icon="✂",url_path="separar_pdf"),
    st.Page("src//03_Convertir_PDF.py",title="PDF WORD",icon="📑",url_path="word_to_pdf"),
    st.Page("src//04_Rotar_PDF.py",title="ROTAR PDF",icon="📑",url_path="rotar_pdf"),
    st.Page("src//05_Imagen_a_pdf.py",title="PDF IMAGEN",icon="📸",url_path="img_to_pdf"),
    st.Page("src//06_Proteger_PDF.py",title="PROTEGER PDF",icon="🔐",url_path="proteger_pdf"),
    st.Page("src//07_Formularios_pdf.py",title="FORMULARIOS PDF",icon="🔐",url_path="crear_formularios")
    
    ],
    "PERSONALIZADOS":[]
}

pg = st.navigation(pages)
pg.run()