import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil
import streamlit_pdf_viewer as pdf_viewer

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📑 Imagen a PDF")
st.markdown("""
    1.  Carga el archivo que quieres convertir.
    2.  Se mostrará en imagen la primera página como referencia.
    3.  Se mostrará un control deslizante para seleccionar el angulo de rotación. 
    4.  Click en "Descargar PDF"..         
""")

img_uploaded = st.file_uploader(label="Cargar",type=["tif","png","jpg"],accept_multiple_files=False)


def remove_file():
    os.remove(img_uploaded.name[:-4] + ".pdf")

def convertir_image(file):
    pdf_name = file.name[:-4] + ".pdf"
    img = pymupdf.open(stream=file.read(),filetype=file.name[-3:])
    pdfbytes = img.convert_to_pdf()
    pdf = pymupdf.open("pdf", pdfbytes)
    pdf.save(f"{file.name[:-4]}.pdf")

    with open(pdf_name, "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos",
                data=fp,
                file_name=pdf_name,
                mime="application/pdf",
                on_click=remove_file)

if img_uploaded:
    if st.button("Convertir"):
        convertir_image(img_uploaded)
