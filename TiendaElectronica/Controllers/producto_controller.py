class ProductoController:
    def __init__(self, db):
        self.db = db

    def guardar(self, producto):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (producto.nombre_producto, producto.categoria or None, producto.precio, producto.stock)
        return self.db.call_procedure("sp_InsertProducto", params)

    def actualizar(self, producto):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (producto.producto_id, producto.nombre_producto, producto.categoria or None, producto.precio, producto.stock)
        return self.db.call_procedure("sp_UpdateProducto", params)

    def eliminar(self, producto_id):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        return self.db.call_procedure("sp_DeleteProducto", (producto_id,))