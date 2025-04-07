import streamlit as st
from st_draggable_list import DraggableList
import pymupdf
import io

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def sorter_uploaded_list(ilist,uploaded_list):
    # Función para ordenar la lista de archivos cargados
    new_order = [k["name"] for k in ilist]
    new_uploaded_list = []
    for name in new_order:
        for upload in uploaded_list:
            if upload.name == name:
                new_uploaded_list.append(upload)    
    return new_uploaded_list

def merge_pdf(uploaded_files):
    # Función para unir los archivos PDF
    output_doc = pymupdf.open()
    for file in uploaded_files:
        doc = pymupdf.open(stream=file.read(),filetype="pdf")
        output_doc.insert_pdf(doc)
    output_pdf = io.BytesIO()
    output_doc.save(output_pdf)

    st.download_button(
        label="Descargar PDF",
        data=output_pdf,
        file_name=f"{output_name_format}.pdf",
        mime="application/pdf"
    )

st.title("🖇 Unir PDF")
st.markdown("""
    1. Carga los archivos PDF quieres unir
    2. Aparecerá una casilla donde podrás indicar un nombre para el archivo consolidado final.
    3. Se mostrará una lista con los archivos cargados, puedes cambiar el orden de los archivos arrastrando y soltando.
    4. Haz clic en el botón "Procesar" para unir los archivos y "Descargar archivos" para obtener el archivo consolidado.
    5. Si no colocas un nombre para el archivo final, se generará uno por defecto llamado "MERGED.pdf"
""")

# Cargar archivos PDF
uploaded_files = st.file_uploader(label="Cargar PDF's",type=["pdf"],accept_multiple_files=True)

# Solo se activa si hay pdfs cargados
if uploaded_files:
    # Nombre del archivo final
    output_name_input = st.text_input("Nombre de archivo final",value="")
    output_name_format = ""
    
    # Para generar el DraggableList
    elements = []
    for i,file in enumerate(uploaded_files):
        data = {}
        data["name"] = file.name
        elements.append(data)
    
    slist = DraggableList(elements, width="100%")

    if st.button("Procesar"):
        new_uploaded_files = sorter_uploaded_list(slist,uploaded_files)
        if output_name_input:
            output_name_format = f"{output_name_input}.pdf"
        else:
            output_name_format = "MERGED.pdf"  
        merge_pdf(new_uploaded_files)



