import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil
from pdf2docx import parse

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📑 Convertir PDF a WORD")
st.write(
    "Carga tu archivo PDF y conviertelos a WORD."
)

uploaded_files= st.file_uploader(label="Upload file",type=["pdf"],accept_multiple_files=True)

def remove_zip():
     os.remove("Descargas.zip")

def convertir_docx(files):
    temp_folder = tempfile.TemporaryDirectory()
    for file in files:
        file_name = file.name
        temp_pdf_name = os.path.join(temp_folder.name,"tempfile.pdf")
        temp_docx_name = os.path.join(temp_folder.name,f"{file_name[:-4]}.docx")
        doc = pymupdf.open(stream=file.read(),filetype="pdf")
        doc.save(temp_pdf_name)
        doc.close()
        parse(temp_pdf_name,temp_docx_name)

    for file in os.listdir(temp_folder.name):
        file_path = os.path.join(temp_folder.name,file)
        if file_path.endswith(".pdf"):
             os.remove(file_path)

    shutil.make_archive("Descargas","zip",temp_folder.name)

    with open("Descargas.zip", "rb") as fp:
            btn = st.download_button(
                label="Descargar Word.",
                data=fp,
                file_name="Descargas.zip",
                mime="application/zip",
                on_click=remove_zip)

if uploaded_files:
    if st.button("Procesar"):
        convertir_docx(uploaded_files)