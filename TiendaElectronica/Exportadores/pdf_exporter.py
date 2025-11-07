from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from tkinter import filedialog, messagebox

class PDFExporter:
    @staticmethod
    def exportar_productos(db):
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if not file:
            return

        if not db.connection and not db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        success, results = db.call_procedure("sp_GetAllProductos")
        if not success:
            messagebox.showerror("Error", "No se pudieron cargar los productos.")
            return

        c = canvas.Canvas(file, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 800, "Reporte de Productos")
        c.setFont("Helvetica", 12)
        y = 770
        for row in results:
            c.drawString(100, y, f"{row[0]} | {row[1]} | {row[2]} | ${row[3]} | Stock: {row[4]}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 770
        c.save()
        messagebox.showinfo("Éxito", "Exportado a PDF.")