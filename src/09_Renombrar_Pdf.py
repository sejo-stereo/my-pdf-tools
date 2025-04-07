import streamlit as st
import pymupdf
from PIL import Image, ImageDraw
import io
from streamlit_image_coordinates import streamlit_image_coordinates
import ast
import zipfile
import re

if "pdf_image" not in st.session_state:
    st.session_state["pdf_image"] = None

if "current_coordinates" not in st.session_state:
    st.session_state["current_coordinates"] = None

def get_text_from_pdf(pdf):
    pdf.seek(0)
    doc = pymupdf.open(stream=pdf.read(), filetype="pdf")
    pdf_coords = get_rectangle_coords(st.session_state["current_coordinates"])
    page = doc[0]
    text = page.get_textbox(rect = pdf_coords).strip()
    formatted_text = re.sub(r'[\\/:*?"<>|]', '', text).strip()
    return formatted_text

def store_pdf_image(pdf):
    pdf.seek(0)
    doc = pymupdf.open(stream=pdf.read(), filetype="pdf")
    page = doc[0]
    pix = page.get_pixmap()
    img_data = io.BytesIO(pix.tobytes("png"))
    return img_data

def get_rectangle_coords(
        points: tuple[tuple[int, int], tuple[int, int]],
    ) -> tuple[int, int, int, int]:
        point1, point2 = points
        minx = min(point1[0], point2[0])
        miny = min(point1[1], point2[1])
        maxx = max(point1[0], point2[0])
        maxy = max(point1[1], point2[1])
        return (minx,miny,maxx,maxy,)

def separar_documentos(pdf,tipo_documento):
    pdf.seek(0)
    selected_rect = get_rectangle_coords(st.session_state["current_coordinates"])
    doc = pymupdf.open(stream=pdf.read(),filetype="pdf")
    zip_buffer = io.BytesIO()

    text_to_pages = {}

    for i in range(len(doc)):
        page = doc[i]
        pure_text = page.get_textbox(rect=selected_rect).strip()
        text = re.sub(r'[\\/:*?"<>|]', '', pure_text).strip()

        if text in text_to_pages:
            text_to_pages[text].append(i)
        else:
            text_to_pages[text] = [i]

    with zipfile.ZipFile(zip_buffer,"w",zipfile.ZIP_DEFLATED) as zip_file:
        # Crear nuevos documentos según las páginas agrupadas
        for text, pages in text_to_pages.items():
            new_filename = f"{text} {tipo_documento}.pdf"
            pdf_buffer = io.BytesIO()
            new_doc = pymupdf.open()  # Crear un PDF vacío

            for page_num in pages:
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            new_doc.save(pdf_buffer,garbage=4,deflate=True)
            pdf_buffer.seek(0)
            zip_file.writestr(new_filename,pdf_buffer.getvalue())  

    zip_buffer.seek(0)

    st.download_button(
        label="Descargar PDFs Separados",
        data=zip_buffer,
        file_name="Descargas.zip",
        mime="application/zip"
    )  


col1,col2 = st.columns(2)

with col2:
    uploaded_pdf = st.file_uploader(label="Cargar PDF",
                accept_multiple_files=False,
                type=["pdf"],
                key="uploaded_pdf")
    
    if uploaded_pdf:
        selected_coords = st.text_input(
            label="Coordenadas del Campo",
            value=st.session_state["current_coordinates"],
            disabled=True,)
        
        selected_text = st.text_input(
            label="Texto del Campo",
            value=get_text_from_pdf(uploaded_pdf),
            disabled=True,
        )

        suffix_input = st.text_input(
            label="Tipo de Documento",
            value="",
            placeholder="Ingrese el tipo de documento",
        )

        if selected_coords and selected_text and suffix_input:
            if st.button("Separar Documentos"):
                try:
                    separar_documentos(uploaded_pdf,suffix_input)
                except:
                    st.error("Error al separar documentos. Asegúrese de que el PDF tenga texto seleccionable.")
    
with col1:
    if uploaded_pdf:
        img_data = store_pdf_image(uploaded_pdf)
        with Image.open(img_data) as img:
            draw = ImageDraw.Draw(img)

            if st.session_state["current_coordinates"]:
                coords = get_rectangle_coords(st.session_state["current_coordinates"])
                draw.rectangle(coords, fill=None, outline="red", width=2)

            value = streamlit_image_coordinates(img,key="rect",click_and_drag=True)

            if value is not None:
                point1 = value["x1"], value["y1"]
                point2 = value["x2"], value["y2"]

                if (
                    point1[0] != point2[0]
                    and point1[1] != point2[1]
                    and st.session_state["current_coordinates"] != (point1, point2)
                ):
                    st.session_state["current_coordinates"] = (point1, point2)
                    st.rerun()    
        
