class OrdenController:
    def __init__(self, db):
        self.db = db

    def guardar(self, cliente_id, empleado_id, fecha_orden, estado):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (cliente_id, empleado_id, fecha_orden, estado)
        return self.db.call_procedure("sp_InsertOrden", params)

    def actualizar(self, orden_id, cliente_id, empleado_id, fecha_orden, estado):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (orden_id, cliente_id, empleado_id, fecha_orden, estado)
        return self.db.call_procedure("sp_UpdateOrden", params)

    def eliminar(self, orden_id):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        return self.db.call_procedure("sp_DeleteOrden", (orden_id,))