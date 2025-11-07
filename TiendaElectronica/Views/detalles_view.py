import tkinter as tk
from tkinter import ttk, messagebox
from Controllers.detalle_controller import DetalleController
from Exportadores.excel_exporter import ExcelExporter
from Exportadores.pdf_exporter import PDFExporter

class DetallesView:
    def __init__(self, notebook, db, app):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Detalles")
        self.db = db
        self.app = app
        self.controller = DetalleController(db)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.frame, text="GESTIÓN DE DETALLES DE ORDEN", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, padx=20, anchor="w")

        self.campos = {}
        labels = ["DetalleID", "OrdenID", "ProductoID", "Cantidad", "PrecioUnitario"]
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.campos[label] = entry

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)

    def validar(self, modo="guardar"):
        if modo != "eliminar":
            if not self.campos["OrdenID"].get().isdigit():
                messagebox.showerror("Error", "OrdenID debe ser numérico.")
                return False
            if not self.campos["ProductoID"].get().isdigit():
                messagebox.showerror("Error", "ProductoID debe ser numérico.")
                return False
            if not self.campos["Cantidad"].get().isdigit() or int(self.campos["Cantidad"].get()) <= 0:
                messagebox.showerror("Error", "Cantidad debe ser entero > 0.")
                return False
            if not self.campos["PrecioUnitario"].get().replace('.', '', 1).isdigit() or float(self.campos["PrecioUnitario"].get()) <= 0:
                messagebox.showerror("Error", "PrecioUnitario debe ser > 0.")
                return False
        return True

    def guardar(self):
        if not self.validar(): return
        success, msg = self.controller.guardar(
            orden_id=int(self.campos["OrdenID"].get()),
            producto_id=int(self.campos["ProductoID"].get()),
            cantidad=int(self.campos["Cantidad"].get()),
            precio_unitario=float(self.campos["PrecioUnitario"].get())
        )
        if success:
            messagebox.showinfo("Éxito", "Detalle guardado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def actualizar(self):
        if not self.campos["DetalleID"].get().isdigit():
            messagebox.showerror("Error", "DetalleID es obligatorio para actualizar.")
            return
        if not self.validar(): return
        success, msg = self.controller.actualizar(
            detalle_id=int(self.campos["DetalleID"].get()),
            cantidad=int(self.campos["Cantidad"].get()),
            precio_unitario=float(self.campos["PrecioUnitario"].get())
        )
        if success:
            messagebox.showinfo("Éxito", "Detalle actualizado.")
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def eliminar(self):
        if not self.campos["DetalleID"].get().isdigit():
            messagebox.showerror("Error", "DetalleID es obligatorio para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este detalle?"):
            return
        success, msg = self.controller.eliminar(int(self.campos["DetalleID"].get()))
        if success:
            messagebox.showinfo("Éxito", "Detalle eliminado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def limpiar(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)

    def exportar_excel(self):
        ExcelExporter.exportar_detalles(self.db)

    def exportar_pdf(self):
        PDFExporter.exportar_detalles(self.db)