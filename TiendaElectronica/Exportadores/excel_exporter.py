from openpyxl import Workbook
from tkinter import filedialog, messagebox

class ExcelExporter:
    @staticmethod
    def exportar_productos(db):
        if not db.connection and not db.connect():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return
        success, results = db.call_procedure("sp_GetAllProductos")
        if not success:
            messagebox.showerror("Error", "No se pudieron cargar los productos.")
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Productos"
        ws.append(["ID", "Nombre", "Categoría", "Precio", "Stock"])
        for row in results:
            ws.append(row)

        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
        if file:
            wb.save(file)
            messagebox.showinfo("Éxito", "Exportado a Excel.")