class ClienteController:
    def __init__(self, db):
        self.db = db

    def guardar(self, cliente):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (cliente.nombre_cliente, cliente.email, cliente.telefono, cliente.ciudad)
        return self.db.call_procedure("sp_InsertCliente", params)

    def actualizar(self, cliente):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        params = (cliente.cliente_id, cliente.nombre_cliente, cliente.email, cliente.telefono, cliente.ciudad)
        return self.db.call_procedure("sp_UpdateCliente", params)

    def eliminar(self, cliente_id):
        if not self.db.connection and not self.db.connect():
            return False, "Error de conexión"
        return self.db.call_procedure("sp_DeleteCliente", (cliente_id,))