import streamlit as st
from st_draggable_list import DraggableList
import pymupdf
import tempfile
import os

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🖇 Unir PDF")
st.write(
    "Carga tus archivos PDF y procesa para unirlos."
)

output_name_input = st.text_input("Nombre de archivo final",value="")
output_name_format = ""

uploaded_files = st.file_uploader(label="Upload files",type=["pdf"],accept_multiple_files=True)

if uploaded_files:
    elements = []
    for i,file in enumerate(uploaded_files):
        data = {}
        # data["orden"] = i
        # data["id"] = file.file_id
        data["name"] = file.name
        elements.append(data)
    
    slist = DraggableList(elements, width="100%")


def sorter_uploaded_list(ilist,uploaded_list):
    new_order = [k["name"] for k in ilist]
    new_uploaded_list = []
    for name in new_order:
        for upload in uploaded_list:
            if upload.name == name:
                new_uploaded_list.append(upload)    
    # st.write(new_order)
    # st.write(new_uploaded_list)
    return new_uploaded_list

def remove_file():
    global output_name_format
    os.remove(output_name_format)

def merge_pdf(uploaded_files): 
    main_doc = pymupdf.open()
    for file in uploaded_files:
        doc = pymupdf.open(stream=file.read(),filetype="pdf")
        main_doc.insert_pdf(doc)
    main_doc.save(output_name_format)
    main_doc.close()

    with open(output_name_format, "rb") as fp:
            btn = st.download_button(
                label="Descargar archivos",
                data=fp,
                file_name=output_name_format,
                mime="application/pdf",
                on_click=remove_file)

if st.button("Procesar"):
    new_uploaded_files = sorter_uploaded_list(slist,uploaded_files)
    if output_name_input:
        output_name_format = f"{output_name_input}.pdf"
    else:
        output_name_format = "MERGED.pdf"  
    merge_pdf(new_uploaded_files)