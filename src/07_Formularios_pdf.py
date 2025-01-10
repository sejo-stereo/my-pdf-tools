import streamlit as st
import pymupdf
from PIL import Image, ImageDraw
import io
from streamlit_image_coordinates import streamlit_image_coordinates
import ast

if "pdf_image" not in st.session_state:
    st.session_state["pdf_image"] = None

if "current_coordinates" not in st.session_state:
    st.session_state["current_coordinates"] = None

if "stored_coordinates" not in st.session_state:
    st.session_state["stored_coordinates"] = []

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
        return (
            minx,
            miny,
            maxx,
            maxy,
        )

def create_form_widget(pdf):
    pdf.seek(0)
    doc = pymupdf.open(stream=pdf.read(), filetype="pdf")
    page = doc[0]
    if st.session_state["stored_coordinates"]:
        for stored in st.session_state["stored_coordinates"]:
            field_name = stored["name"]
            str_coords = stored["coords"]
            data = ast.literal_eval(str_coords)
            x1, y1 = data[0]
            x2, y2 = data[1]
            form_field_rect = pymupdf.Rect(x1, y1, x2, y2)     
            widget = pymupdf.Widget()
            widget.rect = form_field_rect
            widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
            widget.field_name = field_name
            widget.field_value = ""
            page.add_widget(widget)
    pdf_output = io.BytesIO()
    doc.save(pdf_output)
    pdf_output.seek(0)
    
    # Descargar el PDF sin guardarlo como archivo
    st.download_button(
        label="Descargar PDF Formulado",
        data=pdf_output,
        file_name="pdf-formulado2.pdf",
        mime="application/pdf"
    )

col1,col2 = st.columns(2)

with col2:
    uploaded_pdf = st.file_uploader(label="Cargar PDF",
                accept_multiple_files=False,
                type=["pdf"],
                key="uploaded_pdf")
    
    with st.form("Agregar Forms"):
        name_val = st.text_input(label="ID del Campo")
        coords_val = st.text_input(label="Coordenadas del Campo",value=st.session_state["current_coordinates"])
        submitted = st.form_submit_button("Agregar")
        if submitted:
            st.session_state["stored_coordinates"].append({"name":name_val, "coords":coords_val})
            st.success(f"Campo '{name_val}' agregado con éxito.")

    if uploaded_pdf:
        if st.button("Procesar"):
            create_form_widget(uploaded_pdf)

with col1:
    if uploaded_pdf:
        img_data = store_pdf_image(uploaded_pdf)
        with Image.open(img_data) as img:
            draw = ImageDraw.Draw(img)

            if st.session_state["stored_coordinates"]:
                for stored in st.session_state["stored_coordinates"]:
                    coords = get_rectangle_coords(ast.literal_eval(stored["coords"]))
                    draw.rectangle(coords, fill=(213,244,200), outline="green", width=2)

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
        
