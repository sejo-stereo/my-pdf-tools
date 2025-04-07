import streamlit as st

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.write(f"Desarrollado por José Melgarejo.")

pages = {
    "Inicio":[
        st.Page("src//00_Inicio.py",title="Inicio",icon="🏠",url_path="inicio")
    ],
    "GENERAL":
    [
        st.Page("src//01_Unir_PDF.py",title="Unir PDF",icon="🖇",url_path="unir_pdf"),
        st.Page("src//02_Separar_PDF.py",title="Separar PDF",icon="✂",url_path="separar_pdf"),
        st.Page("src//03_Convertir_PDF.py",title="PDF a WORD",icon="📑",url_path="pdf_a_word"),
        st.Page("src//04_Rotar_PDF.py",title="Rotar PDF",icon="📑",url_path="rotar_pdf"),
        st.Page("src//05_Imagen_a_pdf.py",title="PDF a Imagen",icon="📸",url_path="img_to_pdf"),
        st.Page("src//06_Proteger_PDF.py",title="Proteger PDF",icon="🔐",url_path="proteger_pdf"),
        
       
    ],
    "EN DESARROLLO":[
        st.Page("src//07_Formularios_pdf.py",title="Crear Formularios PDF",icon="🔐",url_path="crear_formularios"),
        st.Page("src//08_FirmarPDF.py",title="FIRMAR PDF",icon="🔐",url_path="firmar_pdf"),
        st.Page("src//09_Renombrar_Pdf.py",title="Renombrar PDF",icon="🔐",url_path="renombrar_pdf")
    ]
}

pg = st.navigation(pages)
pg.run()