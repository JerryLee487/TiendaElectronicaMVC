class Producto:
    def __init__(self, producto_id=None, nombre_producto="", categoria="", precio=0.0, stock=0, imagen_path=None):
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.categoria = categoria
        self.precio = precio
        self.stock = stock
        self.imagen_path = imagen_path

class Cliente:
    def __init__(self, cliente_id=None, nombre_cliente="", email="", telefono="", ciudad=""):
        self.cliente_id = cliente_id
        self.nombre_cliente = nombre_cliente
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad

class Empleado:
    def __init__(self, empleado_id=None, nombre="", apellido="", cargo="", fecha_contratacion=None, foto_path=None):
        self.empleado_id = empleado_id
        self.nombre = nombre
        self.apellido = apellido
        self.cargo = cargo
        self.fecha_contratacion = fecha_contratacion
        self.foto_path = foto_path