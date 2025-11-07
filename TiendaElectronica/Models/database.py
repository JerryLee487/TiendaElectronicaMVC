import mysql.connector
from tkinter import messagebox

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                database="TiendaElectronica",
                user="root",
                password="",
                port=3306,
                autocommit=False
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as error:
            if error.errno == 2003:
                messagebox.showerror("Error de Conexión", "No se puede conectar al servidor MySQL.\nVerifica que MySQL esté corriendo y que el puerto 3306 esté disponible.")
            elif error.errno == 1045:
                messagebox.showerror("Error de Autenticación", "Nombre de usuario o contraseña incorrectos.")
            else:
                messagebox.showerror("Error de Conexión", f"Error desconocido: {error}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def call_procedure(self, procedure_name, parameters=None):
        try:
            if parameters:
                self.cursor.callproc(procedure_name, parameters)
            else:
                self.cursor.callproc(procedure_name)
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())
            self.connection.commit()
            return True, results
        except mysql.connector.Error as error:
            self.connection.rollback()
            return False, str(error)