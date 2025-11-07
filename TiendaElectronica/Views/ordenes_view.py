import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Models.entidades import Empleado
from Controllers.orden_controller import OrdenController
from Exportadores.excel_exporter import ExcelExporter
from Exportadores.pdf_exporter import PDFExporter

class OrdenesView:
    def __init__(self, notebook, db, app):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Órdenes")
        self.db = db
        self.app = app
        self.controller = OrdenController(db)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.frame, text="GESTIÓN DE ÓRDENES", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, padx=20, anchor="w")

        self.campos = {}
        labels = ["OrdenID", "ClienteID", "EmpleadoID", "Estado"]
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.campos[label] = entry

        ttk.Label(form_frame, text="Fecha Orden:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        self.fecha_entry = DateEntry(form_frame, width=27, date_pattern="yyyy-mm-dd")
        self.fecha_entry.grid(row=4, column=1, padx=10, pady=5)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)

    def validar(self):
        if not self.campos["ClienteID"].get().isdigit():
            messagebox.showerror("Error", "ClienteID debe ser numérico.")
            return False
        if not self.campos["EmpleadoID"].get().isdigit():
            messagebox.showerror("Error", "EmpleadoID debe ser numérico.")
            return False
        return True

    def guardar(self):
        if not self.validar(): return
        success, msg = self.controller.guardar(
            cliente_id=int(self.campos["ClienteID"].get()),
            empleado_id=int(self.campos["EmpleadoID"].get()),
            fecha_orden=self.fecha_entry.get_date(),
            estado=self.campos["Estado"].get() or "Pendiente"
        )
        if success:
            messagebox.showinfo("Éxito", "Orden guardada.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def actualizar(self):
        if not self.campos["OrdenID"].get().isdigit():
            messagebox.showerror("Error", "OrdenID es obligatorio para actualizar.")
            return
        if not self.validar(): return
        success, msg = self.controller.actualizar(
            orden_id=int(self.campos["OrdenID"].get()),
            cliente_id=int(self.campos["ClienteID"].get()),
            empleado_id=int(self.campos["EmpleadoID"].get()),
            fecha_orden=self.fecha_entry.get_date(),
            estado=self.campos["Estado"].get() or "Pendiente"
        )
        if success:
            messagebox.showinfo("Éxito", "Orden actualizada.")
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def eliminar(self):
        if not self.campos["OrdenID"].get().isdigit():
            messagebox.showerror("Error", "OrdenID es obligatorio para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar esta orden?"):
            return
        success, msg = self.controller.eliminar(int(self.campos["OrdenID"].get()))
        if success:
            messagebox.showinfo("Éxito", "Orden eliminada.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def limpiar(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)
        self.fecha_entry.set_date(self.fecha_entry._default)

    def exportar_excel(self):
        ExcelExporter.exportar_ordenes(self.db)

    def exportar_pdf(self):
        PDFExporter.exportar_ordenes(self.db)