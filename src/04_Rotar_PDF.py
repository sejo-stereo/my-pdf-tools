import streamlit as st
import pymupdf
import tempfile
import zipfile
import os
import shutil
from PIL import Image
import io

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_img(pdf_stream,rotation):
    pdf_stream.seek(0)
    doc = pymupdf.open(stream=pdf_stream.read(),filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap(dpi=300)
    img_data = io.BytesIO(pix.tobytes("png"))
    img = Image.open(img_data)
    rotated_img = img.rotate(rotation,expand=True)
    doc.close()
    return rotated_img

def save_rotated_pdf(pdf_stream,rotation):
    pdf_stream.seek(0)
    rotated_pdf_name = f"{uploaded_pdf.name[:-4]}_rotated.pdf"
    doc = pymupdf.open(stream=pdf_stream.read(),filetype="pdf")
    for page in doc:
        page.set_rotation(rotation*-1)
    doc.save(rotated_pdf_name)    
    doc.close()
    with open(rotated_pdf_name, "rb") as fp:
            btn = st.download_button(
                label="Descargar PDF",
                data=fp,
                file_name=rotated_pdf_name,
                mime="application/pdf",
                # on_click=remove_file
                )
    os.remove(rotated_pdf_name)



st.title("🎈 Rotar PDF")
st.write(
    "Carga tu archivo PDF y modifica la rotación."
)

uploaded_pdf= st.file_uploader(label="Cargar PDF",type=["pdf"],key="uploaded_pdf",accept_multiple_files=False)
if uploaded_pdf:
    values = st.slider("Angulos",-180,180,value=0,step=90)
    if st.button("Download"):
        save_rotated_pdf(uploaded_pdf,values)
if uploaded_pdf:
    st.image(render_img(uploaded_pdf,values),use_container_width =True)