try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError:
    tk = None
    filedialog = None
    messagebox = None

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import cm
import os
import io
import sys

try:
    import cairosvg
except ImportError:
    cairosvg = None

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LOGO_FILENAME = resource_path("Logo.svg")
PAGE_WIDTH_CM = 5.0
PAGE_HEIGHT_CM = 2.5
HORIZONTAL_MARGIN_CM = 0.2
VERTICAL_MARGIN_CM = 0.15
LOGO_BARCODE_GAP_CM = 0.25
BARCODE_TEXT_GAP_CM = 0.18
BARCODE_HEIGHT_CM = 0.9
BAR_WIDTH_CM = 0.045

class AssetLabelMaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Label Maker")
        self.code_entries = []
        self.setup_gui()

    def setup_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        self.entries_frame = tk.Frame(frame)
        self.entries_frame.pack()

        self.add_code_entry()

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Agregar código", command=self.add_code_entry).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Eliminar código", command=self.remove_code_entry).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text="Generar PDF", command=self.generate_pdf).pack(pady=10)

    def add_code_entry(self):
        entry = tk.Entry(self.entries_frame, width=20)
        entry.pack(pady=2)
        self.code_entries.append(entry)

    def remove_code_entry(self):
        if len(self.code_entries) > 1:
            entry = self.code_entries.pop()
            entry.destroy()

    def generate_pdf(self):
        codes = [e.get().strip() for e in self.code_entries if e.get().strip()]
        if not codes:
            messagebox.showerror("Error", "Por favor ingrese al menos un código.")
            return
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])
        if not pdf_path:
            return
        try:
            self.create_pdf(pdf_path, codes)
            messagebox.showinfo("Éxito", f"PDF creado: {pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_pdf(self, pdf_path, codes):
        c = canvas.Canvas(pdf_path, pagesize=(PAGE_WIDTH_CM * cm, PAGE_HEIGHT_CM * cm))
        for index, code in enumerate(codes):
            self.draw_label(c, code)
            if index < len(codes) - 1:
                c.showPage()
        c.save()

    def draw_label(self, c, code):
        label_w, label_h = PAGE_WIDTH_CM * cm, PAGE_HEIGHT_CM * cm
        content_width = (PAGE_WIDTH_CM - 2 * HORIZONTAL_MARGIN_CM) * cm
        y_cursor = label_h - VERTICAL_MARGIN_CM * cm

        if os.path.exists(LOGO_FILENAME):
            logo_available_height_cm = PAGE_HEIGHT_CM - (2 * VERTICAL_MARGIN_CM) - BARCODE_HEIGHT_CM - BARCODE_TEXT_GAP_CM
            max_logo_height = max(logo_available_height_cm - LOGO_BARCODE_GAP_CM, 0) * cm
            if max_logo_height > 0:
                logo = None
                is_svg = LOGO_FILENAME.lower().endswith(".svg")
                if is_svg and cairosvg is not None:
                    png_bytes = cairosvg.svg2png(url=LOGO_FILENAME)
                    logo = Image.open(io.BytesIO(png_bytes))
                elif not is_svg:
                    logo = Image.open(LOGO_FILENAME)

                if logo is not None:
                    max_logo_w = content_width
                    logo.thumbnail((int(max_logo_w), int(max_logo_height)), Image.LANCZOS)
                    logo_path = "_tmp_logo.png"
                    logo.save(logo_path)
                    logo_x = (label_w - logo.width) / 2
                    logo_y = y_cursor - logo.height
                    c.drawImage(logo_path, logo_x, logo_y, width=logo.width, height=logo.height, mask="auto")
                    os.remove(logo_path)
                    y_cursor = logo_y - LOGO_BARCODE_GAP_CM * cm

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

        c.drawCentredString(label_w / 2, text_baseline, code)

def main():
    if tk is None:
        raise RuntimeError("Tkinter is not available in this environment.")
    root = tk.Tk()
    app = AssetLabelMaker(root)
    root.mainloop()

if __name__ == "__main__":
    main() 