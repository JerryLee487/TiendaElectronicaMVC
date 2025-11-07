# TiendaElectronicaMVC
🛒 TiendaElectrónica - Aplicación de Gestión con Tkinter
Una aplicación de escritorio moderna y funcional para gestionar una tienda electrónica, desarrollada en Python con arquitectura MVC (Modelo-Vista-Controlador) y principios de Programación Orientada a Objetos (POO).

🏗️ Arquitectura MVC
Modelo (models):
Maneja la lógica de negocio y la conexión con la base de datos MySQL. Incluye clases de entidades (Producto, Cliente, Empleado, etc.) y una conexión robusta con procedimientos almacenados.
Vista (views):
Interfaces gráficas modulares con Tkinter. Cada entidad tiene su propia pestaña con formularios completos, validaciones en tiempo real, gestión de imágenes y botones de acción.
Controlador (controllers):
Actúa como intermediario entre la vista y el modelo. Procesa las acciones del usuario (guardar, actualizar, eliminar) y coordina las llamadas a la base de datos.

✨ Funcionalidades Destacadas
✅ Validaciones estrictas:
Campos numéricos, email (regex), fechas (con tkcalendar), longitud de texto.
Confirmación antes de operaciones críticas (eliminar/actualizar).
🖼️ Gestión de imágenes:
Soporte para JPG, PNG y GIF en formularios de Productos y Empleados.
Validación de formato y tamaño (< 5 MB).
📤 Exportación profesional:
A Excel (con openpyxl) y PDF (con reportlab).
Datos reales extraídos directamente de la base de datos.
🌓 Temas personalizables:
Modo claro y oscuro intercambiable desde el menú.
🖥️ Diseño limpio y consistente:
Favicon personalizado, iconografía uniforme y estilos profesionales con ttk.
🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.x
GUI: Tkinter + tkcalendar
Base de datos: MySQL (con procedimientos almacenados)
Librerías:
mysql-connector-python
Pillow (PIL) para manejo de imágenes
openpyxl para exportar a Excel
reportlab para exportar a PDF

📁 Estructura del Proyecto
─ app.py (Punto de entrada)

─ controllers (Lógica de controladores)

─ models (Conexión a BD y entidades)

─ views (Interfaces gráficas)

─ exportadores (Módulos de exportación)

🚀 Cómo Ejecutar
Configura la base de datos TiendaElectronica en MySQL (usa el script SQL proporcionado).
Requerido tener tkcalendar, pillow, mysql-connector, o las necesarias para que nos ejecute sin errores
Instala las dependencias:

1
pip install mysql-connector-python pillow openpyxl reportlab
Ejecuta la aplicación:


2
python app.py

Video explicativo:
https://secure.vidyard.com/organizations/4401852/players/xjEk4p1Dv6cKwedvJw2xa4?edit=true&npsRecordControl=1
