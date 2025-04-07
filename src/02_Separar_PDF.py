import streamlit as st
import pymupdf
import io
import zipfile

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def separar_pdf2(uploaded_file,number_pages_to_split):
    doc = pymupdf.open(stream=uploaded_file.read(),filetype="pdf")
    npages = len(doc)

    # Crear un zip en memoria
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(0,npages,number_pages_to_split):
            start_page = i
            end_page = min(i + number_pages_to_split,npages)

            # Crear un nuevo PDF
            temp_doc = pymupdf.open()
            temp_doc.insert_pdf(doc,from_page=start_page,to_page=end_page -1)
            
            # Guardar el PDF en la memoria
            pdf_buffer = io.BytesIO()
            temp_doc.save(pdf_buffer)
            pdf_buffer.seek(0)

            # Agregar el PDF al zip
            zip_file.writestr(f"{uploaded_file.name}_{start_page+1}_{end_page}.pdf",pdf_buffer.getvalue())
    zip_buffer.seek(0)

    # Boton para descargar el zip
    st.download_button(
        label="Descargar archivos separados",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )
     
        
st.title("✂ Separar PDF",anchor=False)
st.markdown("""
    1.  Carga el archivo PDF que deseas separar.
    2.  Indica la cantidad de páginas por separar.
    3.  Haz clic en el botón "Separar PDF" para obtener un archivo ZIP con los PDFs separados.
    4.  Descarga el archivo ZIP con los PDFs separados.
            
""")

# Cargar el archivo PDF
uploaded_file= st.file_uploader(label="Cargar PDF a separar",type=["pdf"],accept_multiple_files=False)

if uploaded_file:
    number_pages_to_split = st.number_input(label="Ingrese cantidad de páginas por separar",min_value=1,step=1)        
    # Ingresar la cantidad de páginas por separar
    if st.button("Separar PDF"):
        separar_pdf2(uploaded_file,number_pages_to_split)

