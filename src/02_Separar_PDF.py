import streamlit as st
import pymupdf
import tempfile
import os
import shutil

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("✂ Separar PDF",anchor=False)
st.write(
    "Carga tu archivo PDF y procesa para separarlos."
)

rename_flag = False
uploaded_file= st.file_uploader(label="Upload file",type=["pdf"],accept_multiple_files=False)
number_pages_split = st.number_input(label="Ingrese cantidad de páginas",min_value=1,step=1)

def remove_zip():
     os.remove("Descargas.zip")

def separar_pdf(uploaded_file):
    try:
        remove_zip()
    except:
         pass
    temp_folder = tempfile.TemporaryDirectory()
    doc = pymupdf.open(stream=uploaded_file.read(),filetype="pdf")
    npages = len(doc)
    for i in range(0,npages,number_pages_split):
        start_page = i
        end_page = i + number_pages_split
        temp_doc = pymupdf.open()
        temp_doc.insert_pdf(doc,from_page=start_page,to_page=end_page -1)
        if end_page + 1 > npages:
             end_page = npages
        temp_doc.save(os.path.join(temp_folder.name,f"{uploaded_file.name}_{start_page+1}_{end_page}.pdf"))
    shutil.make_archive("Descargas","zip",temp_folder.name)
    with open("Descargas.zip", "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos separados.",
                data=fp,
                file_name="Descargas.zip",
                mime="application/zip",
                on_click=remove_zip)
            
if uploaded_file:
    if st.button("Separar PDF"):
        separar_pdf(uploaded_file)

