class EmpleadoController:
    def __init__(self, db):
        self.db = db

    def guardar(self, empleado):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (empleado.nombre, empleado.apellido, empleado.cargo, empleado.fecha_contratacion)
        return self.db.call_procedure("sp_InsertEmpleado", params)

    def actualizar(self, empleado):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (empleado.empleado_id, empleado.nombre, empleado.apellido, empleado.cargo, empleado.fecha_contratacion)
        return self.db.call_procedure("sp_UpdateEmpleado", params)

    def eliminar(self, empleado_id):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        return self.db.call_procedure("sp_DeleteEmpleado", (empleado_id,))