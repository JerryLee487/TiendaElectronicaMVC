import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import re
from Models.entidades import Empleado
from Controllers.empleado_controller import EmpleadoController
from Exportadores.excel_exporter import ExcelExporter
from Exportadores.pdf_exporter import PDFExporter

class EmpleadosView:
    def __init__(self, notebook, db, app):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Empleados")
        self.db = db
        self.app = app
        self.controller = EmpleadoController(db)
        self.foto_path = None
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.frame, text="GESTIÓN DE EMPLEADOS", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, padx=20, anchor="w")

        self.campos = {}
        labels = ["EmpleadoID", "Nombre", "Apellido", "Cargo"]
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.campos[label] = entry

        ttk.Label(form_frame, text="Fecha Contratación:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        from tkcalendar import DateEntry
        self.fecha_entry = DateEntry(form_frame, width=27, date_pattern="yyyy-mm-dd")
        self.fecha_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Foto:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
        ttk.Button(form_frame, text="Cargar Foto", command=self.cargar_foto).grid(row=5, column=1, sticky="w", pady=5)
        self.label_foto = tk.Label(form_frame, width=100, height=80, relief="sunken")
        self.label_foto.grid(row=6, column=1, pady=5)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)

    def cargar_foto(self):
        file = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
        if file:
            if not re.search(r"\.(jpg|jpeg|png|gif)$", file, re.IGNORECASE):
                messagebox.showerror("Error", "Formato no soportado.")
                return
            if os.path.getsize(file) > 5 * 1024 * 1024:
                messagebox.showerror("Error", "Tamaño > 5 MB.")
                return
            self.foto_path = file
            img = Image.open(file)
            img.thumbnail((100, 80))
            photo = ImageTk.PhotoImage(img)
            self.label_foto.config(image=photo)
            self.label_foto.image = photo

    def validar(self):
        if not self.campos["Nombre"].get().strip() or not self.campos["Apellido"].get().strip():
            messagebox.showerror("Error", "Nombre y Apellido son obligatorios.")
            return False
        return True

    def guardar(self):
        if not self.validar(): return
        empleado = Empleado(
            nombre=self.campos["Nombre"].get(),
            apellido=self.campos["Apellido"].get(),
            cargo=self.campos["Cargo"].get() or None,
            fecha_contratacion=self.fecha_entry.get_date()
        )
        success, msg = self.controller.guardar(empleado)
        if success:
            messagebox.showinfo("Éxito", "Empleado guardado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def actualizar(self):
        if not self.campos["EmpleadoID"].get().isdigit():
            messagebox.showerror("Error", "EmpleadoID es obligatorio para actualizar.")
            return
        if not self.validar(): return
        empleado = Empleado(
            empleado_id=int(self.campos["EmpleadoID"].get()),
            nombre=self.campos["Nombre"].get(),
            apellido=self.campos["Apellido"].get(),
            cargo=self.campos["Cargo"].get() or None,
            fecha_contratacion=self.fecha_entry.get_date()
        )
        success, msg = self.controller.actualizar(empleado)
        if success:
            messagebox.showinfo("Éxito", "Empleado actualizado.")
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def eliminar(self):
        if not self.campos["EmpleadoID"].get().isdigit():
            messagebox.showerror("Error", "EmpleadoID es obligatorio para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este empleado?"):
            return
        success, msg = self.controller.eliminar(int(self.campos["EmpleadoID"].get()))
        if success:
            messagebox.showinfo("Éxito", "Empleado eliminado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def limpiar(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)
        self.fecha_entry.set_date(self.fecha_entry._default)
        self.foto_path = None
        self.label_foto.config(image="")

    def exportar_excel(self):
        ExcelExporter.exportar_empleados(self.db)

    def exportar_pdf(self):
        PDFExporter.exportar_empleados(self.db)