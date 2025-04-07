import streamlit as st
import zipfile
from pdf2docx import Converter
import io
from pathlib import Path

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def convertir_docx2(files):
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            docx_buffer = io.BytesIO()
            file_name = Path(file.name).stem 
            
            cv = Converter(stream=file.read())
            cv.convert(docx_buffer)
            cv.close()
            docx_buffer.seek(0) 
            zip_file.writestr(f"{file_name}.docx", docx_buffer.getvalue())
    
    zip_buffer.seek(0)

     # Boton para descargar el zip
    st.download_button(
        label="Descargar ZIP",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )

st.title("📑 PDF a WORD")
st.markdown("""
    1.  Carga los archivos PDF para convertir a WORD.
    2.  Click en el botón "Procesar" para convertir los archivos PDF a WORD.
    3.  Click en el boton "Descargar ZIP" para obtener un archivo ZIP con los WORDs convertidos.           
""")

uploaded_files= st.file_uploader(label="Cargar archivos PDF",type=["pdf"],accept_multiple_files=True)

if uploaded_files:
    if st.button("Convertir a WORD"):
        convertir_docx2(uploaded_files)