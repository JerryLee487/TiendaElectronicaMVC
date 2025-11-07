import tkinter as tk
from tkinter import ttk, messagebox
import re
from Models.entidades import Cliente
from Controllers.cliente_controller import ClienteController
from Exportadores.excel_exporter import ExcelExporter
from Exportadores.pdf_exporter import PDFExporter

class ClientesView:
    def __init__(self, notebook, db, app):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Clientes")
        self.db = db
        self.app = app
        self.controller = ClienteController(db)
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.frame, text="GESTIÓN DE CLIENTES", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, padx=20, anchor="w")

        self.campos = {}
        labels = ["ClienteID", "NombreCliente", "Email", "Telefono", "Ciudad"]
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.campos[label] = entry
            if label == "Email":
                entry.bind("<FocusOut>", self.validar_email)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)

    def validar_email(self, event=None):
        email = self.campos["Email"].get()
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showwarning("Advertencia", "Formato de email inválido.")

    def validar(self):
        if not self.campos["NombreCliente"].get().strip():
            messagebox.showerror("Error", "NombreCliente es obligatorio.")
            return False
        if self.campos["Email"].get() and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.campos["Email"].get()):
            messagebox.showerror("Error", "Formato de email inválido.")
            return False
        return True

    def guardar(self):
        if not self.validar(): return
        cliente = Cliente(
            nombre_cliente=self.campos["NombreCliente"].get(),
            email=self.campos["Email"].get() or None,
            telefono=self.campos["Telefono"].get() or None,
            ciudad=self.campos["Ciudad"].get() or None
        )
        success, msg = self.controller.guardar(cliente)
        if success:
            messagebox.showinfo("Éxito", "Cliente guardado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def actualizar(self):
        if not self.campos["ClienteID"].get().isdigit():
            messagebox.showerror("Error", "ClienteID es obligatorio para actualizar.")
            return
        if not self.validar(): return
        cliente = Cliente(
            cliente_id=int(self.campos["ClienteID"].get()),
            nombre_cliente=self.campos["NombreCliente"].get(),
            email=self.campos["Email"].get() or None,
            telefono=self.campos["Telefono"].get() or None,
            ciudad=self.campos["Ciudad"].get() or None
        )
        success, msg = self.controller.actualizar(cliente)
        if success:
            messagebox.showinfo("Éxito", "Cliente actualizado.")
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def eliminar(self):
        if not self.campos["ClienteID"].get().isdigit():
            messagebox.showerror("Error", "ClienteID es obligatorio para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este cliente?"):
            return
        success, msg = self.controller.eliminar(int(self.campos["ClienteID"].get()))
        if success:
            messagebox.showinfo("Éxito", "Cliente eliminado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def limpiar(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)

    def exportar_excel(self):
        ExcelExporter.exportar_clientes(self.db)

    def exportar_pdf(self):
        PDFExporter.exportar_clientes(self.db)