class DetalleController:
    def __init__(self, db):
        self.db = db

    def guardar(self, orden_id, producto_id, cantidad, precio_unitario):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (orden_id, producto_id, cantidad, precio_unitario)
        return self.db.call_procedure("sp_InsertDetalleOrden", params)

    def actualizar(self, detalle_id, cantidad, precio_unitario):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (detalle_id, cantidad, precio_unitario)
        return self.db.call_procedure("sp_UpdateDetalleOrden", params)

    def eliminar(self, detalle_id):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        return self.db.call_procedure("sp_DeleteDetalleOrden", (detalle_id,))