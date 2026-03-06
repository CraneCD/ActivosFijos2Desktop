import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import cm
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import io
import os

LOGO_FILENAME = "Logo.svg"
PAGE_WIDTH_CM = 5.0
PAGE_HEIGHT_CM = 2.5
HORIZONTAL_MARGIN_CM = 0.2
VERTICAL_MARGIN_CM = 0.15
LOGO_BARCODE_GAP_CM = 0.25
BARCODE_TEXT_GAP_CM = 0.18
BARCODE_HEIGHT_CM = 0.9
BAR_WIDTH_CM = 0.045

def create_pdf(codes):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(PAGE_WIDTH_CM * cm, PAGE_HEIGHT_CM * cm))

    for index, code in enumerate(codes):
        draw_label(c, code)
        if index < len(codes) - 1:
            c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

def draw_label(c, code):
    label_w = PAGE_WIDTH_CM * cm
    label_h = PAGE_HEIGHT_CM * cm
    content_width = (PAGE_WIDTH_CM - 2 * HORIZONTAL_MARGIN_CM) * cm
    y_cursor = label_h - VERTICAL_MARGIN_CM * cm

    # Draw SVG logo within available space
    logo_available_height_cm = PAGE_HEIGHT_CM - (2 * VERTICAL_MARGIN_CM) - BARCODE_HEIGHT_CM - BARCODE_TEXT_GAP_CM
    if logo_available_height_cm > 0 and os.path.exists(LOGO_FILENAME):
        drawing = svg2rlg(LOGO_FILENAME)
        if drawing:
            drawing_width = drawing.width
            drawing_height = drawing.height
            max_logo_height = max(logo_available_height_cm - LOGO_BARCODE_GAP_CM, 0) * cm
            if max_logo_height > 0 and drawing_width > 0 and drawing_height > 0:
                scale = min(content_width / drawing_width, max_logo_height / drawing_height)
                if scale > 0:
                    scaled_width = drawing_width * scale
                    scaled_height = drawing_height * scale
                    x_logo = (label_w - scaled_width) / 2
                    y_logo = y_cursor - scaled_height
                    drawing.scale(scale, scale)
                    renderPDF.draw(drawing, c, x_logo, y_logo)
                    y_cursor = y_logo - LOGO_BARCODE_GAP_CM * cm

    # Draw barcode centered on the page
    barcode_height = BARCODE_HEIGHT_CM * cm
    barcode = code128.Code128(code, barHeight=barcode_height, barWidth=BAR_WIDTH_CM * cm, humanReadable=False)
    barcode_x = (label_w - barcode.width) / 2

    text_font_size = 9
    c.setFont("Helvetica-Bold", text_font_size)
    text_baseline = VERTICAL_MARGIN_CM * cm + text_font_size
    text_top = text_baseline + text_font_size * 0.6

    minimum_barcode_bottom = text_top + BARCODE_TEXT_GAP_CM * cm
    barcode_y = max(minimum_barcode_bottom, y_cursor - barcode_height)
    barcode.drawOn(c, barcode_x, barcode_y)

    # Draw text anchored to bottom margin
    c.drawCentredString(label_w / 2, text_baseline, code)

# Streamlit UI
st.title("Activos Fijos Etiquetas 2.0")

codes_input = st.text_area("Ingrese un código de archivo por línea")
if st.button("Generate PDF"):
    codes = [code.strip() for code in codes_input.splitlines() if code.strip()]
    if not codes:
        st.error("Ingrese por lo menos un código.")
    else:
        pdf_file = create_pdf(codes)
        st.success("PDF generado con etiquetas individuales")
        st.download_button("Descargar PDF", pdf_file, file_name="etiquetas.pdf", mime="application/pdf")
