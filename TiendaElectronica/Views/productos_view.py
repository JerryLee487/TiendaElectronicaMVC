import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import re
from Models.entidades import Producto
from Controllers.producto_controller import ProductoController
from Exportadores.excel_exporter import ExcelExporter
from Exportadores.pdf_exporter import PDFExporter

class ProductosView:
    def __init__(self, notebook, db, app):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Productos")
        self.db = db
        self.app = app
        self.controller = ProductoController(db)
        self.imagen_path = None
        self.crear_widgets()

    def crear_widgets(self):
        tk.Label(self.frame, text="GESTIÓN DE PRODUCTOS", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(pady=10, padx=20, anchor="w")

        # Campos
        self.campos = {}
        labels = ["ProductoID", "NombreProducto", "Categoria", "Precio", "Stock"]
        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=f"{label}:", font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.campos[label] = entry

        # Imagen
        ttk.Label(form_frame, text="Imagen:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
        ttk.Button(form_frame, text="Cargar Imagen", command=self.cargar_imagen).grid(row=5, column=1, sticky="w", pady=5)
        self.label_imagen = tk.Label(form_frame, width=100, height=80, relief="sunken")
        self.label_imagen.grid(row=6, column=1, pady=5)

        # Botones
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar Excel", command=self.exportar_excel).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=5)

    def cargar_imagen(self):
        file = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
        if file:
            if not re.search(r"\.(jpg|jpeg|png|gif)$", file, re.IGNORECASE):
                messagebox.showerror("Error", "Formato no soportado.")
                return
            if os.path.getsize(file) > 5 * 1024 * 1024:
                messagebox.showerror("Error", "Tamaño > 5 MB.")
                return
            self.imagen_path = file
            img = Image.open(file)
            img.thumbnail((100, 80))
            photo = ImageTk.PhotoImage(img)
            self.label_imagen.config(image=photo)
            self.label_imagen.image = photo

    def validar(self):
        if not self.campos["NombreProducto"].get().strip():
            messagebox.showerror("Error", "NombreProducto es obligatorio.")
            return False
        if not self.campos["Precio"].get().replace('.', '', 1).isdigit():
            messagebox.showerror("Error", "Precio debe ser un número válido.")
            return False
        if not self.campos["Stock"].get().isdigit():
            messagebox.showerror("Error", "Stock debe ser un número entero.")
            return False
        return True

    def guardar(self):
        if not self.validar(): return
        producto = Producto(
            nombre_producto=self.campos["NombreProducto"].get(),
            categoria=self.campos["Categoria"].get(),
            precio=float(self.campos["Precio"].get()),
            stock=int(self.campos["Stock"].get())
        )
        success, msg = self.controller.guardar(producto)
        if success:
            messagebox.showinfo("Éxito", "Producto guardado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def actualizar(self):
        if not self.campos["ProductoID"].get().isdigit():
            messagebox.showerror("Error", "ProductoID es obligatorio para actualizar.")
            return
        if not self.validar(): return
        producto = Producto(
            producto_id=int(self.campos["ProductoID"].get()),
            nombre_producto=self.campos["NombreProducto"].get(),
            categoria=self.campos["Categoria"].get(),
            precio=float(self.campos["Precio"].get()),
            stock=int(self.campos["Stock"].get())
        )
        success, msg = self.controller.actualizar(producto)
        if success:
            messagebox.showinfo("Éxito", "Producto actualizado.")
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def eliminar(self):
        if not self.campos["ProductoID"].get().isdigit():
            messagebox.showerror("Error", "ProductoID es obligatorio para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Seguro que desea eliminar este producto?"):
            return
        success, msg = self.controller.eliminar(int(self.campos["ProductoID"].get()))
        if success:
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self.limpiar()
        else:
            messagebox.showerror("Error", f"Error: {msg}")

    def limpiar(self):
        for entry in self.campos.values():
            entry.delete(0, tk.END)
        self.imagen_path = None
        self.label_imagen.config(image="")

    def exportar_excel(self):
        ExcelExporter.exportar_productos(self.db)

    def exportar_pdf(self):
        PDFExporter.exportar_productos(self.db)