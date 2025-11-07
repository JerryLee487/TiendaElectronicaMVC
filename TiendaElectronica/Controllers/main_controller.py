import tkinter as tk
from tkinter import ttk
from Models.database import DatabaseConnection
from Views import productos_view, clientes_view, empleado_view, ordenes_view, detalles_view
from Views.clientes_view import ClientesView
from Views.detalles_view import DetallesView
from Views.empleado_view import EmpleadosView
from Views.ordenes_view import OrdenesView
from Views.productos_view import ProductosView


class MainController:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseConnection()
        self.tema_actual = "claro"
        self.configurar_ventana()
        self.crear_menu()
        self.crear_notebook()
        self.aplicar_tema()

    def configurar_ventana(self):
        self.root.title("TiendaElectrónica Management")
        self.root.geometry("1050x750")
        try:
            self.root.iconbitmap("favicon.ico")
        except:
            pass

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Cambiar Tema", command=self.cambiar_tema)

    def cambiar_tema(self):
        self.tema_actual = "oscuro" if self.tema_actual == "claro" else "claro"
        self.aplicar_tema()

    def aplicar_tema(self):
        estilo = ttk.Style()
        if self.tema_actual == "oscuro":
            self.root.configure(bg="#2e2e2e")
            estilo.configure("TFrame", background="#2e2e2e")
            estilo.configure("TLabel", background="#2e2e2e", foreground="white")
            estilo.configure("TButton", background="#555", foreground="white")
        else:
            self.root.configure(bg="#f0f0f0")
            estilo.configure("TFrame", background="#f0f0f0")
            estilo.configure("TLabel", background="#f0f0f0", foreground="black")
            estilo.configure("TButton", background="#ddd", foreground="black")

    def crear_notebook(self):
        self.notebook = ttk.Notebook(self.root)  # ← Guardamos como atributo
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        ProductosView(self.notebook, self.db, self)
        ClientesView(self.notebook, self.db, self)
        EmpleadosView(self.notebook, self.db, self)
        OrdenesView(self.notebook, self.db, self)
        DetallesView(self.notebook, self.db, self)